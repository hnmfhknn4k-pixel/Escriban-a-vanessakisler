"""Autenticación Supabase por servidor. No almacena expedientes en Supabase."""
import base64
import json
import os
import re
from urllib.parse import quote
import httpx

class AuthError(ValueError):
    pass

def config():
    url=os.environ.get('SUPABASE_URL','').rstrip('/')
    key=os.environ.get('SUPABASE_PUBLISHABLE_KEY','')
    allowed={e.strip().casefold() for e in os.environ.get('ESCRIBANIA_ALLOWED_EMAILS','').split(',') if e.strip()}
    if not re.fullmatch(r'https://[a-z0-9]+\.supabase\.co',url) or not key.startswith('sb_publishable_') or not allowed:
        raise AuthError('Acceso por correo pendiente de configuración del servidor.')
    return url,key,allowed

def readiness():
    try: config();return {'enabled':True}
    except AuthError:return {'enabled':False}

def allowed_email(email):
    if str(email).strip().casefold() not in config()[2]:
        raise AuthError('Esta cuenta no está habilitada para EscribanIA.')

async def call(method,path,token=None,data=None):
    url,key,_=config()
    headers={'apikey':key}
    if token:headers['Authorization']='Bearer '+token
    try:
        async with httpx.AsyncClient(timeout=25,follow_redirects=False) as client:
            response=await client.request(method,url+'/auth/v1/'+path,headers=headers,json=data)
    except httpx.HTTPError:
        raise AuthError('No se pudo conectar con el servicio de acceso. Intentá nuevamente.') from None
    if response.status_code>=400:
        # Never expose provider bodies, request credentials or tokens in errors/logs.
        raise AuthError('No se pudo verificar el acceso. Revisá contraseña, confirmación del correo y código del autenticador.')
    if response.status_code==204:return {}
    try:return response.json()
    except ValueError:raise AuthError('Respuesta de acceso inválida.') from None

async def signup(email,password,origin):
    allowed_email(email)
    if not isinstance(password,str) or not 12<=len(password)<=256:raise AuthError('Usá una contraseña de entre 12 y 256 caracteres.')
    return await call('POST','signup?redirect_to='+quote(origin,safe=''),data={'email':email.strip(),'password':password})

async def begin(email,password):
    allowed_email(email)
    if not isinstance(password,str) or not 12<=len(password)<=256:raise AuthError('Revisá la contraseña.')
    data=await call('POST','token?grant_type=password',data={'email':email.strip(),'password':password})
    token=data.get('access_token')
    if not isinstance(token,str):raise AuthError('Confirmá tu correo antes de ingresar.')
    user=await call('GET','user',token)
    allowed_email(user.get('email',''))
    if not user.get('email_confirmed_at'):raise AuthError('Confirmá tu correo antes de ingresar.')
    uid=user.get('id','')
    if not re.fullmatch(r'[0-9a-f-]{36}',uid):raise AuthError('Identidad de cuenta inválida.')
    factors=[f for f in user.get('factors',[]) if f.get('factor_type')=='totp' and f.get('status')=='verified']
    secret=None
    if factors:factor=factors[0]['id']
    else:
        # A failed enrollment may leave an unverified factor. Only remove unverified TOTP factors.
        for f in user.get('factors',[]):
            if f.get('factor_type')=='totp' and f.get('status')=='unverified':
                await call('DELETE','factors/'+f['id'],token)
        enrollment=await call('POST','factors',token,{'factor_type':'totp','friendly_name':'EscribanIA'})
        factor=enrollment['id'];secret=enrollment['totp']['secret']
    return {'token':token,'factor':factor,'uid':uid,'secret':secret}

async def finish(pending,code):
    if not re.fullmatch(r'\d{6}',str(code)):raise AuthError('Ingresá los seis dígitos del autenticador.')
    challenge=await call('POST','factors/'+pending['factor']+'/challenge',pending['token'])
    data=await call('POST','factors/'+pending['factor']+'/verify',pending['token'],{'challenge_id':challenge['id'],'code':code})
    token=data.get('access_token','')
    # JWT claims are read only AFTER remote verification by this project's /user endpoint.
    user=await call('GET','user',token)
    allowed_email(user.get('email',''))
    try:
        payload=token.split('.')[1];claims=json.loads(base64.urlsafe_b64decode(payload+'='*(-len(payload)%4)))
    except (ValueError,IndexError):raise AuthError('Token de acceso inválido.') from None
    if claims.get('aal')!='aal2' or claims.get('sub')!=pending['uid'] or user.get('id')!=pending['uid']:
        raise AuthError('Falta completar la verificación reforzada.')
    return 'supabase:'+pending['uid']
