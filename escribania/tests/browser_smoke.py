"""Prueba real en Chromium con viewport móvil; no acredita Safari físico."""
import io
import os
import secrets
import time
from pathlib import Path
from docx import Document
from playwright.sync_api import sync_playwright,expect
from store import Store,password_hash,totp

BASE=os.environ.get('ESCRIBANIA_TEST_URL','http://127.0.0.1:8001')
store=Store(os.environ.get('ESCRIBANIA_DATA','/tmp/escribania-dev'))
name='browser'+secrets.token_hex(5);password=secrets.token_urlsafe(24);secret='JBSWY3DPEHPK3PXP'
with store.connect() as db:db.execute('INSERT INTO users VALUES(?,?,?)',(name,password_hash(password),store.fernet.encrypt(secret.encode())))
doc=Document();doc.add_paragraph('Comparece MARÍA MUÑOZ PÉREZ, cédula 1.234.567-2. Objeto ficticio para laboratorio.');out=io.BytesIO();doc.save(out)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(BASE);page.get_by_label('Usuario',exact=True).fill(name);page.get_by_label('Contraseña',exact=True).fill(password);page.get_by_label('Código del autenticador').fill(totp(secret,time.time()));page.get_by_role('button',name='Ingresar con verificación reforzada').click()
    page.locator('#workspace').wait_for(state='visible')
    page.locator('input[type=file]').set_input_files({'name':'expediente-ficticio.docx','mimeType':'application/vnd.openxmlformats-officedocument.wordprocessingml.document','buffer':out.getvalue()})
    page.get_by_role('button',name='Abrir expediente').click();page.locator('#case-title').get_by_text('expediente-ficticio.docx',exact=True).wait_for()
    page.get_by_role('button',name='02 Identidades').click()
    form=page.locator('#party-form');form.get_by_label('Nombres y apellidos completos').fill('María Muñoz Pérez');form.get_by_label('Cédula',exact=True).fill('1.234.567-2');form.get_by_label('Evidencia consultada').fill('Documento ficticio de laboratorio');form.get_by_label('Fundamento del cotejo').fill('Cotejo ficticio integral realizado para la prueba');form.get_by_role('button',name='Cotejar y bloquear ficha').click()
    page.locator('#parties').get_by_text('MARÍA MUÑOZ PÉREZ',exact=True).wait_for()
    page.get_by_role('button',name='03 Fundamentos').click();page.get_by_role('button',name='Analizar versión actual').click();page.locator('#observations .observation').first.wait_for()
    page.get_by_role('button',name='04 Protección').click();page.get_by_role('button',name='Ver texto sustituido localmente').click();expect(page.locator('#privacy-preview')).to_contain_text('[[PERSONA_1_NAME]]')
    assert 'MARÍA' not in page.locator('#privacy-preview').inner_text()
    page.get_by_role('button',name='05 Registro').click();page.get_by_role('button',name='Verificar y consultar').click();expect(page.locator('#audit-events')).to_contain_text('identity_verified')
    page.get_by_role('button',name='06 Cierre').click();assert page.locator('#approve').is_disabled();assert 'Perfil normativo único' in page.locator('#blockers').inner_text()
    page.get_by_role('button',name='01 Documento').click()
    with page.expect_download() as dl:page.locator('#draft-link').click()
    path=dl.value.path();assert Path(path).read_bytes().startswith(b'PK')
    assert page.evaluate('() => document.documentElement.scrollWidth <= innerWidth'), 'Desbordamiento horizontal'
    Path('/tmp/escribania-artifacts').mkdir(exist_ok=True)
    page.screenshot(path='/tmp/escribania-artifacts/mobile.png',full_page=True)
    page.set_viewport_size({'width':1440,'height':1000});page.screenshot(path='/tmp/escribania-artifacts/desktop.png',full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    template=page.locator('#template-list .panel').first
    expect(template).to_contain_text('Compraventa de automotor')
    use=template.get_by_role('button',name='Abrir borrador de automotor');assert use.is_disabled()
    template.locator('summary').click();expect(template).to_contain_text('PRECIO_EN_LETRAS')
    template.get_by_role('checkbox').check();assert use.is_enabled();use.click()
    expect(page.locator('#case-title')).to_contain_text('Compraventa de automotor')
    expect(page.locator('#segments')).to_contain_text('[VENDEDOR_NOMBRES_APELLIDOS]')
    template.locator('summary').click()
    page.get_by_role('button',name='06 Cierre').click();assert page.locator('#approve').is_disabled()
    expect(page.locator('#blockers')).to_contain_text('Campos entre corchetes')
    assert page.evaluate('() => document.documentElement.scrollWidth <= innerWidth')
    with page.expect_download() as dl:template.get_by_role('link',name='Descargar plantilla Word').click()
    assert Path(dl.value.path()).read_bytes().startswith(b'PK')
    assert not errors,errors
    page.get_by_role('button',name='Cerrar sesión').click();page.locator('#login').wait_for(state='visible');assert page.locator('#workspace').is_hidden()
    browser.close()
print('Chromium móvil y escritorio: revisión documental y plantilla de automotor con adaptaciones, reconocimiento previo, expediente, bloqueo por pendientes y descarga Word: OK')
