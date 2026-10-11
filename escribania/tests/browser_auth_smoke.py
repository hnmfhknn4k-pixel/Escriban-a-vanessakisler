"""UI Supabase simulada: sin llamadas al proveedor ni credenciales reales."""
from playwright.sync_api import sync_playwright,expect
import json
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844});errors=[];verified=False;headers=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 def route(r):
  global verified
  path=r.request.url.split('8001')[-1]
  data=None;status=200
  if path=='/api/auth/config':data={'enabled':True}
  elif path=='/api/auth/signup':data={'message':'Confirmá el correo ficticio'}
  elif path=='/api/auth/begin':data={'csrf':'setup-csrf','enrollment_secret':'SECRET-FICTITIOUS-ONLY'}
  elif path=='/api/auth/finish':
   headers.append(r.request.headers.get('x-csrf-token'));assert headers[-1]=='setup-csrf';verified=True;data={'user':'supabase:fixture','csrf':'session-csrf'}
  elif path=='/api/me':
   data={'user':'supabase:fixture','csrf':'session-csrf'} if verified else {'detail':'Iniciá sesión con contraseña y TOTP'};status=200 if verified else 401
  elif path in ('/api/cases','/api/templates'):data=[]
  if data is None:r.continue_()
  else:r.fulfill(status=status,content_type='application/json',body=json.dumps(data))
 page.route('**/api/**',route)
 page.goto('http://127.0.0.1:8001/');expect(page.locator('#email-form')).to_be_visible();expect(page.locator('#login-form')).to_be_hidden()
 page.locator('#email-form input[name=email]').fill('persona@example.test');page.locator('#email-form input[name=password]').fill('FicticiaPassword123')
 page.get_by_role('button',name='Crear mi cuenta',exact=True).click();expect(page.locator('#message')).to_contain_text('Confirmá el correo')
 page.locator('#email-form input[name=password]').fill('FicticiaPassword123');page.locator('#email-form button[type=submit]').click()
 expect(page.locator('#mfa-form')).to_be_visible();expect(page.locator('#workspace')).to_be_hidden();expect(page.locator('#mfa-secret')).to_have_value('SECRET-FICTITIOUS-ONLY')
 page.locator('#mfa-form input[name=otp]').fill('123456');page.locator('#mfa-form button.primary').click()
 expect(page.locator('#workspace')).to_be_visible();expect(page.locator('#mfa-secret')).to_have_value('')
 assert page.evaluate('() => document.documentElement.scrollWidth <= innerWidth');assert not errors,errors
 browser.close()
 print('Acceso por correo, registro, preautenticación, TOTP, CSRF y vista móvil simulados: OK')
