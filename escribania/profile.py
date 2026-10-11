"""Perfil único; no se permite elegir márgenes por expediente."""
import json
import math
from pathlib import Path

def validate_profile(data):
    if not data.get('source','').startswith(('https://www.impo.com.uy/','https://www.poderjudicial.gub.uy/')):
        raise ValueError('Fuente oficial requerida')
    for key in ('authority','normative_version','evidence','reviewer','validated_at','print_test'):
        if len(str(data.get(key,'')))<8: raise ValueError('Falta '+key)
    if not data.get('duplex_validated'): raise ValueError('Falta validación de anverso y reverso')
    for key in ('w','h','top','bottom','left','right','header','footer','gutter'):
        val=float(data[key])
        if not math.isfinite(val) or not 0<=val<=500 or (key in ('w','h') and val<100): raise ValueError('Medida inválida: '+key)
        data[key]=val
    if data['left']+data['right']+data['gutter']>=data['w'] or data['top']+data['bottom']>=data['h']: raise ValueError('Área de escritura inválida')
    data['paper']='liso'; data['mirror']=True
    return data

def load_profile(directory):
    path=Path(directory)/'notarial-profile.json'
    if not path.exists(): return None
    return validate_profile(json.loads(path.read_text()))
