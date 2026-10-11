"""Reglas deterministas y edición OOXML. No realiza consultas a un modelo."""
import copy
import hashlib
import io
import re
import unicodedata
import zipfile
from datetime import datetime, timezone
from lxml import etree as ET

VERSION = '0.4.0'
RULES_VERSION = 'uy-identity-1'
PROMPT_VERSION = 'disabled-1'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
ET.register_namespace('w', W)
CI = re.compile(r'(?<!\d)(?:\d{1,2}\.\d{3}\.\d{3}-\d|\d{6,7}-\d|\d{7,8})(?!\d)')

def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()

def upper_name(name):
    return unicodedata.normalize('NFC', name.strip()).upper()

def ci_digits(value):
    if not re.fullmatch(r'(?:\d{6,7}-\d|\d{7,8}|\d{1,2}\.\d{3}\.\d{3}-\d)', value.strip()):
        raise ValueError('Formato de cédula no admitido')
    digits = re.sub(r'\D', '', value)
    if not 7 <= len(digits) <= 8:
        raise ValueError('La cédula debe contener 7 u 8 dígitos')
    return digits.zfill(8)

def valid_ci(value):
    try:
        digits = ci_digits(value)
        return (10 - sum(int(a) * b for a, b in zip(digits[:7], [2,9,8,7,6,3,4])) % 10) % 10 == int(digits[7])
    except ValueError:
        return False

def pseudonymize(text, parties, extra_terms=()):
    """Sustitución reversible local; nunca se denomina anonimización."""
    mapping = {}
    items = []
    for i, party in enumerate(parties, 1):
        for field in ('name', 'ci'):
            token = f'[[PERSONA_{i}_{field.upper()}]]'
            mapping[token] = party[field]
            items.append((party[field], token))
    for i, term in enumerate(extra_terms, 1):
        if len(term.strip()) < 3:
            raise ValueError('Las referencias adicionales deben tener al menos 3 caracteres')
        token = f'[[DATO_{i}]]'; mapping[token] = term; items.append((term, token))
    # One substitution pass prevents a real input from recursively changing tokens.
    if '[[' in text or ']]' in text:
        raise ValueError('El texto contiene delimitadores reservados')
    if items:
        by_value = {unicodedata.normalize('NFC', v).casefold(): token for v, token in items}
        pattern = re.compile(r'(?<!\w)(?:'+'|'.join(re.escape(v) for v, _ in sorted(items, key=lambda p:len(p[0]), reverse=True))+r')(?!\w)', re.I)
        text = pattern.sub(lambda m: by_value[unicodedata.normalize('NFC',m[0]).casefold()], unicodedata.normalize('NFC', text))
    # Detect alternate CI formatting too.
    def ci_replace(m):
        for i,p in enumerate(parties,1):
            if ci_digits(m[0]) == ci_digits(p['ci']): return f'[[PERSONA_{i}_CI]]'
        return m[0]
    text = CI.sub(ci_replace, text)
    residuals = []
    for pattern,label in [(CI,'cédula no cotejada'),(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b','correo'),(r'(?:\+598\s*)?\b09\d[\d\s-]{5,}\d\b','teléfono'),(r'(?i)\b(?:calle|avenida|domicilio|padrón|padron|cuenta|matrícula|matricula)\b','ubicación u otro identificador')]:
        if re.search(pattern,text): residuals.append(label)
    return text, mapping, sorted(set(residuals))

def reinsert(text, mapping):
    found = re.findall(r'\[\[[^\[\]]+\]\]', text)
    if any(t not in mapping for t in found): raise ValueError('Referencia desconocida: reinserción bloqueada')
    result = re.sub(r'\[\[[^\[\]]+\]\]', lambda m:mapping[m[0]], text)
    if '[[' in result or ']]' in result: raise ValueError('Referencia incompleta')
    return result

def read_docx(blob):
    if len(blob) > 10 * 1024 * 1024: raise ValueError('Límite: 10 MB')
    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            entries=z.infolist()
            if len(entries)>2000 or sum(e.file_size for e in entries)>40*1024*1024: raise ValueError('DOCX demasiado grande al descomprimir')
            if len({e.filename for e in entries}) != len(entries): raise ValueError('Entradas ZIP duplicadas')
            if 'word/document.xml' not in z.namelist(): raise ValueError('No es un DOCX')
            warnings=[]; segments=[]
            for filename in z.namelist():
                if filename.endswith('.bin') or 'embeddings/' in filename: warnings.append('Objeto embebido o macro: '+filename)
                if filename.endswith('.rels') and b'TargetMode="External"' in z.read(filename): warnings.append('Relación externa: '+filename)
                if not (filename=='word/document.xml' or re.match(r'word/(?:header|footer)\d*\.xml$',filename)): continue
                raw=z.read(filename)
                if b'<!DOCTYPE' in raw or b'<!ENTITY' in raw: raise ValueError('XML con entidades no admitido')
                tree=ET.fromstring(raw)
                paragraphs={p:i for i,p in enumerate(tree.iter('{'+W+'}p'))}
                for tag in ['ins','del','fldChar','instrText','drawing','object','altChunk','txbxContent','tab','br','cr','sdt']:
                    pattern='.//w:r/w:tab' if tag=='tab' else './/w:'+tag
                    if tree.find(pattern,NS) is not None: warnings.append(f'Elemento requiere revisión: {tag} en {filename}')
                texts=list(tree.iter('{'+W+'}t')) + list(tree.iter('{'+W+'}delText'))
                for j,t in enumerate(texts):
                    paragraph=next((p for p in t.iterancestors() if p.tag=='{'+W+'}p'),None)
                    segments.append({'id':f'{filename}:{j}', 'part':filename, 'index':j, 'paragraph':paragraphs.get(paragraph,-1), 'text':t.text or '', 'deleted':t.tag.endswith('delText')})
            for filename in z.namelist():
                if re.match(r'word/(footnotes|endnotes|comments|glossary/).*',filename): warnings.append('Parte conservada sin analizar: '+filename)
            return segments,sorted(set(warnings))
    except (zipfile.BadZipFile,ET.ParseError) as e: raise ValueError('DOCX inválido') from e

def analyzed_text(segments):
    # Concatenating runs keeps identities split by Word styling detectable.
    keys=dict.fromkeys((s['part'],s['paragraph']) for s in segments)
    return '\n'.join(''.join(s['text'] for s in segments if (s['part'],s['paragraph'])==key and not s['deleted']) for key in keys)

def export_docx(original, changes, author, template=None):
    out=io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(original)) as src, zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            raw=src.read(info.filename)
            selected=[c for c in changes if c['part']==info.filename and c['status']=='accepted']
            if selected or (template and info.filename=='word/document.xml'):
                root=ET.fromstring(raw); nodes=list(root.iter('{'+W+'}t'))+list(root.iter('{'+W+'}delText'))
                parents={child:parent for parent in root.iter() for child in parent}
                for n,c in enumerate(selected,1):
                    node=nodes[c['index']]
                    if node.text != c['before']: raise ValueError('El original cambió')
                    run=parents[node]; parent=parents[run]
                    if run.tag!='{'+W+'}r' or len(run.findall('w:t',NS))!=1: raise ValueError('Run complejo: no se puede exportar con seguridad')
                    if parent.tag in ('{'+W+'}ins','{'+W+'}del'): raise ValueError('Cambio controlado preexistente: no editable')
                    pos=list(parent).index(run); parent.remove(run)
                    for offset,(tag,value) in enumerate([('del',c['before']),('ins',c['after'])]):
                        wrapper=ET.Element('{'+W+'}'+tag,{'{'+W+'}id':str(n*2+offset),'{'+W+'}author':author,'{'+W+'}date':datetime.now(timezone.utc).isoformat()})
                        clone=copy.deepcopy(run); t=clone.find('w:t',NS); t.tag='{'+W+'}delText' if tag=='del' else '{'+W+'}t'; t.text=value
                        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); wrapper.append(clone); parent.insert(pos+offset,wrapper)
                if template:
                    for paragraph in root.findall('.//w:p',NS):
                        properties=paragraph.find('w:pPr',NS)
                        if properties is None: properties=ET.Element('{'+W+'}pPr'); paragraph.insert(0,properties)
                        spacing=properties.find('w:spacing',NS)
                        if spacing is None: spacing=ET.SubElement(properties,'{'+W+'}spacing')
                        spacing.set('{'+W+'}line',str(round(8*1440/25.4)));spacing.set('{'+W+'}lineRule','atLeast')
                    for section in root.findall('.//w:sectPr',NS):
                        for tag in ('pgSz','pgMar'):
                            item=section.find('w:'+tag,NS)
                            if item is None: item=ET.SubElement(section,'{'+W+'}'+tag)
                            keys=('w','h') if tag=='pgSz' else ('top','bottom','left','right','header','footer','gutter')
                            for key in keys: item.set('{'+W+'}'+key,str(round(template[key]*1440/25.4)))
                raw=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            if template and info.filename=='word/settings.xml':
                root=ET.fromstring(raw)
                if root.find('w:mirrorMargins',NS) is None: ET.SubElement(root,'{'+W+'}mirrorMargins')
                raw=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            dst.writestr(info,raw)
    return out.getvalue()

def identity_issues(text,parties):
    issues=[]
    if not parties: issues.append('No hay fichas cotejadas')
    seen={ci_digits(p['ci']) for p in parties}
    for m in CI.finditer(text):
        if not valid_ci(m[0]): issues.append('Dígito verificador inválido: '+m[0])
        elif ci_digits(m[0]) not in seen: issues.append('Cédula no cotejada: '+m[0])
    for p in parties:
        matches=list(re.finditer(r'(?<!\w)'+re.escape(p['name'])+r'(?!\w)',text,re.I))
        if not matches: issues.append('Compareciente sin mención completa: '+p['name'])
        if any(m[0]!=p['name'] for m in matches): issues.append('Nombre fuera de la forma cotejada: '+p['name'])
        if not any(ci_digits(m[0])==ci_digits(p['ci']) for m in CI.finditer(text) if valid_ci(m[0])): issues.append('Cédula cotejada sin mención: '+p['name'])
    for match in re.finditer(r'(?i)\b(?:comparece|comparecen|señor|señora|nombre)\s*:?\s*([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑa-záéíóúüñ ’\'-]+?)(?=,|;|\n|$)',text):
        candidate=upper_name(match[1])
        if candidate not in {p['name'] for p in parties}: issues.append('Mención de identidad no cotejada: '+match[1])
    for line in text.splitlines():
        names=[p for p in parties if re.search(r'(?<!\w)'+re.escape(p['name'])+r'(?!\w)',line,re.I)]
        numbers=[ci_digits(m[0]) for m in CI.finditer(line) if valid_ci(m[0])]
        if len(names)==1 and numbers and any(n!=ci_digits(names[0]['ci']) for n in numbers): issues.append('Asociación nombre-cédula contradictoria: '+names[0]['name'])
    return sorted(set(issues))
