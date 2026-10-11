"""Manual reproducible desde documentación versionada; sin documentos reales."""
import html
import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Preformatted,Table,TableStyle

ROOT=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyES',fontName='Helvetica',fontSize=10,leading=15,spaceAfter=9,textColor=colors.HexColor('#263c35')))
styles.add(ParagraphStyle(name='CodeES',fontName='Courier',fontSize=7.5,leading=10,spaceAfter=12))
styles['Heading1'].textColor=styles['Heading2'].textColor=colors.HexColor('#173e34')
styles['Heading1'].fontSize=22;styles['Heading1'].leading=28
styles['Heading2'].fontSize=15;styles['Heading2'].leading=20

def inline(text):
    text=html.escape(text)
    text=re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)',r'<link href="\2" color="#173e34">\1</link>',text)
    text=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',text)
    return text

def chapter(filename):
    items=[];buffer=[];code=[];in_code=False;rows=[]
    def flush():
        if buffer:items.append(Paragraph(inline(' '.join(buffer)),styles['BodyES']));buffer.clear()
    def table_flush():
        if rows:
            table=Table([[Paragraph(inline(c),styles['BodyES']) for c in row] for row in rows],colWidths=[75,420],repeatRows=1)
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5ece6')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#d6ddd4')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]));items.append(table);items.append(Spacer(1,12));rows.clear()
    for line in (ROOT/filename).read_text().splitlines():
        if line.startswith('```'):
            flush();table_flush()
            if in_code:
                # Long commands wrap to avoid overflow in printed PDF.
                import textwrap
                wrapped='\n'.join('\n'.join(textwrap.wrap(x,90,replace_whitespace=False,drop_whitespace=False)) or ' ' for x in code)
                items.append(Preformatted(wrapped,styles['CodeES']));code=[]
            in_code=not in_code;continue
        if in_code:code.append(line);continue
        if line.startswith('|'):
            flush()
            if not re.match(r'^\|[-: |]+\|$',line):rows.append([c.strip() for c in line.strip('|').split('|')])
            continue
        table_flush()
        if line.startswith('# '):flush();items.append(Paragraph(inline(line[2:]),styles['Heading1']))
        elif line.startswith('## '):flush();items.append(Paragraph(inline(line[3:]),styles['Heading2']))
        elif line.startswith('- '):flush();items.append(Paragraph('• '+inline(line[2:]),styles['BodyES']))
        elif not line.strip():flush()
        else:buffer.append(line)
    flush();table_flush();return items

def page(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#d6ddd4'));canvas.line(48,48,A4[0]-48,48)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#69756e'));canvas.drawString(48,32,'EscribanIA · Manual v0.4 · 11/10/2026 · prototipo de desarrollo')
    canvas.drawRightString(A4[0]-48,32,str(doc.page));canvas.restoreState()

story=[Spacer(1,65),Paragraph('EscribanIA',styles['Title']),Spacer(1,20),Paragraph('Asistencia notarial para Uruguay',styles['Heading1']),Paragraph('Manual de uso y administración · versión 0.4',styles['BodyES']),Paragraph('Edición: 11 de octubre de 2026',styles['BodyES']),Spacer(1,25),Paragraph('Identidades cotejadas. Cambios visibles. Decisiones fundadas.',styles['Heading2']),Paragraph('Versión web con servidor y datos cifrados, basada en el prototipo v0.3 adjunto. Puede contener errores; no acredita identidad, validez jurídica ni cumplimiento normativo integral.',styles['BodyES']),Paragraph('Estado de entrega: funciones locales probadas con datos ficticios; IA real y publicación HTTPS pendientes. Registro con protección local HMAC, sin firma, fechado ni anclaje independiente. Dimensiones y márgenes de papel notarial pendientes de plantilla técnica oficial validada; un único perfil para todos.',styles['BodyES']),Paragraph('Las hojas A4 de este manual no constituyen una plantilla de papel notarial.',styles['BodyES']),PageBreak()]
for name in ['README.md','docs/plantillas.md','docs/fuentes.md','docs/seguridad.md']:
    story+=chapter(name)+[PageBreak()]
SimpleDocTemplate(str(ROOT/'docs/manual.pdf'),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=48,bottomMargin=65,title='EscribanIA — Manual v0.4',author='EscribanIA').build(story,onFirstPage=page,onLaterPages=page)
print('Manual PDF actualizado generado.')
