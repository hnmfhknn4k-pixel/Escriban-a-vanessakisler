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

let loadedFile=null,loadVersion=0,localChecks=null;
function clearLoadedFile(){loadVersion++;loadedFile=null;localChecks=null;d('download-review').disabled=true;d('review-file').value='';d('file-text').textContent='';d('file-hashes').textContent='';d('file-warnings').replaceChildren();d('file-sections').replaceChildren();d('file-checks').replaceChildren();d('file-result').hidden=true;d('validate-file').disabled=true;d('clear-file').disabled=true;d('file-state').textContent='Archivo retirado de esta página.';}
d('clear-file').onclick=clearLoadedFile;
d('review-file').onchange=async e=>{
 const file=e.target.files[0];const version=++loadVersion;loadedFile=null;localChecks=null;d('download-review').disabled=true;d('file-result').hidden=true;d('validate-file').disabled=true;d('file-checks').replaceChildren();
 if(!file){clearLoadedFile();return;}
 d('file-state').textContent='Leyendo en tu navegador…';
 try{
  const result=await EscribaniaFileReview.read(file);if(version!==loadVersion)return;loadedFile=result;
  d('file-text').textContent=result.text||'(Sin texto legible)';d('file-hashes').textContent='Archivo: '+result.fileHash+'\nTexto: '+result.textHash;
  d('file-warnings').replaceChildren(...result.warnings.map(text=>{const li=document.createElement('li');li.textContent=text;return li;}));
  d('file-sections').replaceChildren(...result.sections.map((s,i)=>{const p=document.createElement('p');p.textContent='Sección '+(i+1)+' · márgenes leídos en mm: '+Object.entries(s).map(([k,v])=>k+': '+(v===null?'no detectado':v)).join(' · ')+'. No se verifica adecuación normativa.';return p;}));
  d('file-result').hidden=false;d('validate-file').disabled=!result.text.trim();d('clear-file').disabled=false;d('file-state').textContent='Archivo leído localmente. Pulsá «Validar archivo cargado». El original no cambió.';
 }catch(error){if(version!==loadVersion)return;d('file-text').textContent='';d('file-hashes').textContent='';d('file-state').textContent=error.message||'No se pudo leer el archivo.';d('clear-file').disabled=false;}
};
d('validate-file').onclick=()=>{
 if(!loadedFile)return;
 const checks=EscribaniaFileReview.checks(loadedFile.text);localChecks=checks;d('download-review').disabled=false;
 d('file-checks').replaceChildren(...checks.map(c=>{const panel=document.createElement('article');panel.className='observation';const h=document.createElement('h4');h.textContent=c.kind;const quote=document.createElement('blockquote');quote.textContent=c.fragment;const p=document.createElement('p');p.textContent=c.basis;panel.append(h,quote,p);return panel;}));
 d('file-state').textContent='Controles locales ejecutados. Revisá cada señal y cotejá el original; no es aprobación notarial.';
};

d('download-review').onclick=()=>{
 if(!loadedFile||!localChecks)return;
 const text=['ESCRIBANIA — REVISION LOCAL DE PRUEBA','Fecha del dispositivo: '+new Date().toISOString(),'No acredita identidad, autoría, fecha confiable ni validez jurídica. Registro editable, sin firma, sellado de tiempo ni auditoría protegida.','Archivo SHA-256: '+loadedFile.fileHash,'Texto SHA-256: '+loadedFile.textHash,'ADVERTENCIAS',...loadedFile.warnings,'SEÑALES',...localChecks.map(c=>c.kind+' | '+c.fragment+' | '+c.basis),'TEXTO EXTRAÍDO',loadedFile.text,'Este archivo puede contener datos personales. Protegelo como el documento original.'].join('\n\n');
 const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const link=document.createElement('a');link.href=url;link.download='EscribanIA-revision-local.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
