"""Catálogo cerrado de borradores revisables derivados de modelos aportados."""
import json
from pathlib import Path
from core import digest

DIRECTORY=Path(__file__).resolve().parent/'templates'
CATALOG={'compraventa-automotor':('automotor.json','automotor.docx'),
         'automotor-certificacion-protocolizacion':('automotor-certificacion-protocolizacion.json','automotor-certificacion-protocolizacion.docx')}

def load_template(template_id):
    if template_id not in CATALOG: raise KeyError(template_id)
    manifest_name,document_name=CATALOG[template_id]
    manifest=json.loads((DIRECTORY/manifest_name).read_text())
    blob=(DIRECTORY/document_name).read_bytes()
    if digest(blob)!=manifest['template_sha256']: raise ValueError('La plantilla no coincide con su huella de referencia')
    return manifest,blob

def catalog():
    return [load_template(template_id)[0] for template_id in CATALOG]
