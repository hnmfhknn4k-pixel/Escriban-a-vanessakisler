import base64
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from cryptography.fernet import Fernet

def canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()

class Store:
    def __init__(self, directory):
        self.directory=Path(directory); self.directory.mkdir(parents=True,exist_ok=True,mode=0o700)
        self.key_path=self.directory/'keys.json'
        if not self.key_path.exists():
            if (self.directory/'data.sqlite').exists(): raise RuntimeError('Claves ausentes: no regenerar sobre datos existentes')
            fd=os.open(self.key_path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
            with os.fdopen(fd,'w') as f: json.dump({'encrypt':Fernet.generate_key().decode(),'audit':secrets.token_hex(32)},f)
        keys=json.loads(self.key_path.read_text()); self.fernet=Fernet(keys['encrypt']); self.audit_key=bytes.fromhex(keys['audit'])
        self.db=self.directory/'data.sqlite'
        with self.connect() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS users(name TEXT PRIMARY KEY,password TEXT NOT NULL,totp TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY,owner TEXT NOT NULL,payload BLOB NOT NULL);
            CREATE TABLE IF NOT EXISTS acl(case_id TEXT,user TEXT,PRIMARY KEY(case_id,user));
            CREATE TABLE IF NOT EXISTS audit(seq INTEGER PRIMARY KEY AUTOINCREMENT,case_id TEXT NOT NULL,previous TEXT NOT NULL,event BLOB NOT NULL,mac TEXT NOT NULL);
            CREATE TRIGGER IF NOT EXISTS no_audit_update BEFORE UPDATE ON audit BEGIN SELECT RAISE(ABORT,'append only'); END;
            CREATE TRIGGER IF NOT EXISTS no_audit_delete BEFORE DELETE ON audit BEGIN SELECT RAISE(ABORT,'append only'); END;''')
        os.chmod(self.db,0o600)

    @contextmanager
    def connect(self):
        db=sqlite3.connect(self.db,timeout=10); db.row_factory=sqlite3.Row
        try:
            with db: yield db
        finally: db.close()
    def encrypt(self,value): return self.fernet.encrypt(canonical(value))
    def decrypt(self,value): return json.loads(self.fernet.decrypt(value))
    def event(self,db,case_id,actor,action,details):
        last=db.execute('SELECT mac FROM audit ORDER BY seq DESC LIMIT 1').fetchone()
        previous=last['mac'] if last else '0'*64
        event=self.encrypt({'case':case_id,'actor':actor,'action':action,'details':details,'server_time':datetime.now(timezone.utc).isoformat()})
        mac=hmac.new(self.audit_key,previous.encode()+case_id.encode()+event,hashlib.sha256).hexdigest()
        db.execute('INSERT INTO audit(case_id,previous,event,mac) VALUES(?,?,?,?)',(case_id,previous,event,mac))
    def verify(self):
        previous='0'*64; count=0
        with self.connect() as db:
            for row in db.execute('SELECT * FROM audit ORDER BY seq'):
                mac=hmac.new(self.audit_key,previous.encode()+row['case_id'].encode()+row['event'],hashlib.sha256).hexdigest()
                if row['previous']!=previous or not hmac.compare_digest(mac,row['mac']): raise ValueError('Registro de auditoría alterado')
                self.decrypt(row['event']); previous=row['mac']; count+=1
        return {'events':count,'head':previous,'protection':'Cadena HMAC y cifrado local. Sin firma ni sellado de tiempo externo; no prueba autoría ni fecha por sí sola.'}
    def allowed(self,db,cid,user):
        return db.execute('SELECT id FROM cases WHERE id=? AND (owner=? OR EXISTS(SELECT 1 FROM acl WHERE case_id=cases.id AND user=?))',(cid,user,user)).fetchone()
    def get(self,cid,user):
        self.verify()
        with self.connect() as db:
            if not self.allowed(db,cid,user): raise PermissionError('Sin permiso para este expediente')
            row=db.execute('SELECT payload FROM cases WHERE id=?',(cid,)).fetchone()
            case=self.decrypt(row['payload'])
            for entry in db.execute('SELECT event FROM audit WHERE case_id=? ORDER BY seq DESC',(cid,)):
                details=self.decrypt(entry['event'])['details']
                if 'state_sha256' in details:
                    if not hmac.compare_digest(details['state_sha256'],hashlib.sha256(canonical(case)).hexdigest()): raise ValueError('Estado del expediente alterado')
                    break
            return case
    def save(self,case,user,action,details,create=False):
        self.verify()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if create:
                db.execute('INSERT INTO cases VALUES(?,?,?)',(case['id'],user,self.encrypt(case)))
            else:
                if not self.allowed(db,case['id'],user): raise PermissionError('Sin permiso')
                db.execute('UPDATE cases SET payload=? WHERE id=?',(self.encrypt(case),case['id']))
            self.event(db,case['id'],user,action,dict(details,state_sha256=hashlib.sha256(canonical(case)).hexdigest()))
    def history(self,cid,user):
        self.get(cid,user)
        with self.connect() as db: return [dict(seq=r['seq'],mac=r['mac'],**self.decrypt(r['event'])) for r in db.execute('SELECT * FROM audit WHERE case_id=? ORDER BY seq',(cid,))]

def password_hash(password,salt=None):
    salt=salt or secrets.token_bytes(16)
    return base64.b64encode(salt).decode()+':'+hashlib.scrypt(password.encode(),salt=salt,n=16384,r=8,p=1).hex()
def password_ok(password,stored):
    return hmac.compare_digest(password_hash(password,base64.b64decode(stored.split(':')[0])),stored)

def totp(secret,epoch):
    import struct
    key=base64.b32decode(secret)
    result=hmac.new(key,struct.pack('>Q',int(epoch)//30),hashlib.sha1).digest(); offset=result[-1]&15
    return str((int.from_bytes(result[offset:offset+4],'big')&0x7fffffff)%1000000).zfill(6)
