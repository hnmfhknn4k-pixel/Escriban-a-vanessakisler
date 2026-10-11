"""Alta local fuera de la web; contraseña y secreto MFA nunca van al repositorio."""
import argparse
import base64
import getpass
import os
import secrets
from store import Store,password_hash
from profile import validate_profile
import json
from pathlib import Path

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=['create-user','verify-audit','install-profile']); parser.add_argument('--user'); parser.add_argument('--file'); args=parser.parse_args()
    store=Store(os.environ.get('ESCRIBANIA_DATA','runtime'))
    if args.command=='verify-audit': print(store.verify())
    elif args.command=='install-profile':
        if not args.file: parser.error('--file requerido; perfil técnico validado por responsable')
        profile=validate_profile(json.loads(Path(args.file).read_text()))
        target=store.directory/'notarial-profile.json'
        target.write_text(json.dumps(profile,ensure_ascii=False,indent=2)); os.chmod(target,0o600)
        with store.connect() as db: store.event(db,'SYSTEM','local-admin','global_notarial_profile_installed',{'sha256':__import__('hashlib').sha256(target.read_bytes()).hexdigest(),'source':profile['source'],'reviewer':profile['reviewer'],'evidence':profile['evidence']})
        print('Perfil único instalado. Reiniciá el servidor; los expedientes abiertos deberán revisarse de nuevo.')
    else:
        if not args.user or not args.user.isalnum(): parser.error('--user alfanumérico requerido')
        password=getpass.getpass('Contraseña (mínimo 12 caracteres): ')
        if len(password)<12: parser.error('Contraseña insuficiente')
        if password!=getpass.getpass('Repetir contraseña: '): parser.error('No coincide')
        secret=base64.b32encode(secrets.token_bytes(20)).decode()
        with store.connect() as db: db.execute('INSERT INTO users VALUES(?,?,?)',(args.user,password_hash(password),store.fernet.encrypt(secret.encode())))
        print('Configura el autenticador TOTP (30 segundos, 6 dígitos). Guarda el secreto fuera del repositorio y no lo compartas por chat:')
        print(secret)
