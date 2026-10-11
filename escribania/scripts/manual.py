"""Manual de cuatro páginas, basado en el v0.3 aportado y con paleta de la web."""
import html,re,hashlib,json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,PageBreak
ROOT=Path(__file__).resolve().parents[1]
GREEN=colors.HexColor('#173e34');PAPER=colors.HexColor('#f6f5f0');INK=colors.HexColor('#263c35');MUTED=colors.HexColor('#69756e')
styles={
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=9,leading=12,spaceAfter=7,textColor=INK),
 'title':ParagraphStyle('title',fontName='Helvetica',fontSize=25,leading=30,spaceAfter=13,textColor=GREEN),
 'cover':ParagraphStyle('cover',fontName='Helvetica',fontSize=38,leading=43,spaceAfter=15,textColor=GREEN),
 'heading':ParagraphStyle('heading',fontName='Helvetica-Bold',fontSize=10.5,leading=14,spaceBefore=5,spaceAfter=5,textColor=GREEN),
 'lead':ParagraphStyle('lead',fontName='Helvetica',fontSize=16,leading=20,spaceAfter=16,textColor=INK)
}
def inline(s):
 s=html.escape(s);return re.sub(r'(https://[^\s]+)',r'<link href="\1" color="#173e34">\1</link>',s)
def page(canvas,doc):
 canvas.saveState();canvas.setFillColor(PAPER);canvas.rect(0,0,A4[0],A4[1],fill=1,stroke=0)
 canvas.setStrokeColor(GREEN);canvas.line(48,A4[1]-35,A4[0]-48,A4[1]-35)
 canvas.setFont('Helvetica',7);canvas.setFillColor(MUTED);canvas.drawString(48,25,'ESCRIBANIA / MANUAL DE USO · adaptación v0.3 · 11/10/2026');canvas.drawRightString(A4[0]-48,25,str(doc.page));canvas.restoreState()
chunks=(ROOT/'docs/manual-uso.md').read_text().split('---PAGE---');assert len(chunks)==4
story=[]
for i,chunk in enumerate(chunks):
 if i:story.append(PageBreak())
 buffer=[];first_body=True
 def flush():
  global first_body
  if buffer:
   story.append(Paragraph(inline(' '.join(buffer)),styles['lead'] if first_body else styles['body']));buffer.clear();first_body=False
 for line in chunk.strip().splitlines():
  if line.startswith('# '):flush();story.append(Paragraph(inline(line[2:]),styles['cover'] if i==0 else styles['title']))
  elif line.startswith('## '):flush();story.append(Paragraph(inline(line[3:]),styles['heading']))
  elif not line.strip():flush()
  else:buffer.append(line.strip())
 flush()
SimpleDocTemplate(str(ROOT/'docs/manual.pdf'),pagesize=A4,topMargin=52,bottomMargin=48,leftMargin=48,rightMargin=48,title='EscribanIA — Manual de uso',author='EscribanIA').build(story,onFirstPage=page,onLaterPages=page)
original=ROOT/'docs/manual-original-v03.pdf'
manifest={'source_filename':'Manual_EscribanIA_v03.pdf','source_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'source_pages':4,'adaptation':'Paleta verde/crema de la web y ajustes de funciones vigentes; original conservado sin modificar','content_file':'manual-uso.md','content_sha256':hashlib.sha256((ROOT/'docs/manual-uso.md').read_bytes()).hexdigest(),'published_file':'manual.pdf'}
(ROOT/'docs/manual-procedencia.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Manual basado en v0.3 generado con paleta de la web.')
