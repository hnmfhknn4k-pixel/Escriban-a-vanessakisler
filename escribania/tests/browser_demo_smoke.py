"""Prueba funcional de demostración pública; solo datos ficticios."""
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844});errors=[];requests=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append((r.method,r.url)))
 page.goto('http://127.0.0.1:8001/demo')
 expect(page.locator('#demo-document')).to_contain_text('María Muñoz Pérez')
 page.get_by_role('button',name='Comparar con las fichas').click();expect(page.locator('#demo-findings')).to_contain_text('Discrepancia')
 page.get_by_role('button',name='Aceptar cambio del ejemplo').click();expect(page.locator('#demo-document')).to_contain_text('MARÍA MUÑOZ PÉREZ')
 expect(page.locator('#demo-document')).to_contain_text('JOSÉ NÚÑEZ GARCÍA')
 expect(page.locator('#demo-document')).to_contain_text('2.345.678-3')
 page.get_by_role('button',name='Ver texto con referencias').click();expect(page.locator('#demo-private')).to_contain_text('[[PERSONA_1_CI]]')
 assert '1.234.567' not in page.locator('#demo-private').inner_text()
 page.get_by_role('button',name='Deshacer cambio').click();expect(page.locator('#demo-document')).to_contain_text('María Muñoz Pérez')
 page.get_by_role('button',name='Rechazar propuesta').click();expect(page.locator('#demo-history')).to_contain_text('rechazada')
 page.get_by_role('button',name='Reiniciar prueba').click();assert page.locator('#demo-history li').count()==1
 assert page.get_by_role('button',name='Aprobar instrumento final').is_disabled()
 assert page.locator('input[type=file]').count()==1;assert not page.locator('textarea').count()
 assert not any(method!='GET' or '/api/' in url for method,url in requests)
 assert page.evaluate('() => document.documentElement.scrollWidth <= innerWidth');assert not errors,errors
 browser.close();print('Demo móvil sin autenticación: cotejo, aceptar/rechazar/deshacer, sustitución local y ausencia de llamadas API: OK')
