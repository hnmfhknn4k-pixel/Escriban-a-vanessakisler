'use strict';
const d=id=>document.getElementById(id);
const original='Comparecen María Muñoz Pérez, cédula 1.234.567-2, y José Núñez García, cédula 2.345.678-3, para una compraventa de vehículo ficticio DEMO-001. Precio: [PRECIO_PENDIENTE].';
const after=original.replace('María Muñoz Pérez','María Muñoz Pérez'.normalize('NFC').toLocaleUpperCase('es-UY')).replace('José Núñez García','José Núñez García'.normalize('NFC').toLocaleUpperCase('es-UY'));
let current=original,state='pending';
function note(text){d('demo-message').textContent=text;const li=document.createElement('li');li.textContent=text;d('demo-history').append(li);}
function render(){d('demo-document').textContent=current;d('demo-before').textContent=original;d('demo-after').textContent=after;d('demo-accept').disabled=state!=='pending';d('demo-reject').disabled=state!=='pending';d('demo-undo').disabled=state!=='accepted';d('demo-private').hidden=true;d('demo-private').textContent='';d('demo-findings').replaceChildren();}
d('demo-compare').onclick=()=>{const findings=[];if(current!==after)findings.push('Discrepancia: los nombres del documento no están en las mismas MAYÚSCULAS que las fichas ficticias.');else findings.push('Los nombres y cédulas del ejemplo coinciden con las fichas ficticias. Esto no acredita identidad.');findings.push('Falta completar el precio. El cierre permanece bloqueado.');d('demo-findings').replaceChildren(...findings.map(text=>{const li=document.createElement('li');li.textContent=text;return li;}));note('Comparación ilustrativa realizada sobre datos ficticios.');};
d('demo-accept').onclick=()=>{current=after;state='accepted';render();note('Propuesta aceptada en la prueba: nombres completos en MAYÚSCULAS; cédulas conservadas.');};
d('demo-reject').onclick=()=>{state='rejected';render();note('Propuesta rechazada en la prueba; documento sin cambios.');};
d('demo-undo').onclick=()=>{current=original;state='pending';render();note('Cambio deshecho en la prueba; se recuperó el texto inicial.');};
d('demo-reset').onclick=()=>{current=original;state='pending';d('demo-history').replaceChildren();render();note('Prueba reiniciada con datos ficticios.');};
d('demo-pseudo').onclick=()=>{d('demo-private').textContent=current.replace(/María Muñoz Pérez/gi,'[[PERSONA_1_NOMBRE]]').replace(/José Núñez García/gi,'[[PERSONA_2_NOMBRE]]').replaceAll('1.234.567-2','[[PERSONA_1_CI]]').replaceAll('2.345.678-3','[[PERSONA_2_CI]]');d('demo-private').hidden=false;note('Sustitución ilustrativa realizada en esta página. Sin envío al servidor ni al modelo.');};
render();note('Demostración abierta sin autenticación.');
