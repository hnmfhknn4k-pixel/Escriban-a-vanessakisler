'use strict';
window.EscribaniaFileReview=(()=>{
 const W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';
 const hash=async bytes=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(n=>n.toString(16).padStart(2,'0')).join('');
 function xml(text){if(/<!DOCTYPE|<!ENTITY/i.test(text))throw Error('XML con entidades no admitidas.');const doc=new DOMParser().parseFromString(text,'application/xml');if(doc.getElementsByTagName('parsererror').length)throw Error('El DOCX contiene XML inválido.');return doc;}
 function fromDocx({names,parts}){
  const segments=[],warnings=[],sections=[];
  for(const name of names){
   if(/vbaProject|embeddings\//i.test(name))warnings.push('Macros u objetos incorporados: no procesados ni ejecutados.');
   if(/word\/(footnotes|endnotes|comments)\.xml/.test(name))warnings.push('Notas o comentarios: no integrados al texto de trabajo. Revisar en Word.');
  }
  for(const [name,text] of Object.entries(parts)){
   const doc=xml(text);
   if(name==='word/document.xml'&&(doc.documentElement.namespaceURI!==W||doc.documentElement.localName!=='document'))throw Error('Falta el documento Word principal válido.');
   if(name==='[Content_Types].xml'&&/macroEnabled/i.test(text))warnings.push('Tipo de documento con macros: no ejecutadas ni verificadas.');
   if(name.endsWith('.rels')){if([...doc.getElementsByTagNameNS('*','Relationship')].some(n=>n.getAttribute('TargetMode')==='External'))warnings.push('Relaciones externas: no seguidas ni descargadas.');continue;}
   if(!/^word\/(document|header\d+|footer\d+)\.xml$/.test(name))continue;
   if(['ins','del','delText'].some(t=>doc.getElementsByTagNameNS(W,t).length))warnings.push('Cambios controlados preexistentes: revisar aceptación/rechazo en Word; las eliminaciones no se suman al texto actual.');
   if(['drawing','pict','fldSimple','fldChar','instrText','altChunk','sdt','tab','br','txbxContent'].some(t=>doc.getElementsByTagNameNS(W,t).length))warnings.push('Campos, dibujos, controles, tabulaciones o saltos complejos: extracción parcial; revisar en Word.');
   for(const paragraph of doc.getElementsByTagNameNS(W,'p')){
    let value='';for(const node of paragraph.getElementsByTagNameNS(W,'t')){let parent=node.parentElement,excluded=false;while(parent&&parent!==paragraph){if(parent.namespaceURI===W&&['del','txbxContent'].includes(parent.localName)){excluded=true;break;}parent=parent.parentElement;}if(!excluded)value+=node.textContent;}
    if(value.trim())segments.push({part:name,text:value});
   }
   if(name==='word/document.xml')for(const section of doc.getElementsByTagNameNS(W,'sectPr')){
    const margin=section.getElementsByTagNameNS(W,'pgMar')[0];const values={};
    for(const attr of ['top','bottom','left','right','header','footer','gutter']){const n=margin?.getAttributeNS(W,attr);values[attr]=n&&/^\d+$/.test(n)?Math.round(Number(n)*25.4/1440*100)/100:null;}
    sections.push(values);
   }
  }
  const text=segments.map(s=>s.text).join('\n');if(!text.trim())warnings.push('No se encontró texto legible. Puede contener imágenes; no hay OCR.');
  return {text,segments,warnings:[...new Set(warnings)],sections};
 }
 async function read(file){
  if(!file||file.size>8*1024*1024)throw Error('Elegí un archivo de hasta 8 MB.');
  const extension=file.name.split('.').pop().toLowerCase();if(!['docx','txt'].includes(extension))throw Error('Admitimos DOCX y TXT. Para DOC, guardá una copia DOCX en Word. PDF e imágenes requieren conversión u OCR fuera de esta prueba.');
  const bytes=await file.arrayBuffer();const fileHash=await hash(bytes);let result;
  if(extension==='txt'){
   const text=new TextDecoder('utf-8',{fatal:true}).decode(bytes);result={text,segments:[{part:'Texto UTF-8',text}],warnings:['TXT: no contiene secciones, tablas ni formato Word verificable.'],sections:[]};
  }else result=fromDocx(await new Promise((resolve,reject)=>{
   const worker=new Worker('/static/file-worker.js');const timer=setTimeout(()=>{worker.terminate();reject(Error('La lectura superó el tiempo permitido.'));},12000);
   const done=()=>{clearTimeout(timer);worker.terminate();};
   worker.onmessage=e=>{done();if(e.data.error)reject(Error(e.data.error));else resolve(e.data);};worker.onerror=()=>{done();reject(Error('No se pudo leer este DOCX.'));};worker.postMessage(bytes,[bytes]);
  }));
  return {...result,fileHash,textHash:await hash(new TextEncoder().encode(result.text))};
 }
 function checks(text){
  const observations=[];
  const add=(kind,fragment,basis)=>{if(observations.length<200)observations.push({kind,fragment,basis});};
  for(const m of text.matchAll(/\[[^\]\n]+\]/g)){add('Campo pendiente',m[0],'Corroborar y completar antes de aprobar.');if(observations.length>=200)break;}
  for(const m of text.matchAll(/\b([\p{L}]+)\s+\1\b/giu)){add('Posible repetición',m[0],'Puede ser intencional; revisar el contexto y decidir.');if(observations.length>=200)break;}
  const pattern=/(?<!\d)(?:\d{1,2}\.\d{3}\.\d{3}-\d|\d{6,7}-\d|\d{7,8})(?!\d)/g;
  for(const m of text.matchAll(pattern)){
   if(observations.length>=200)break;
   const digits=m[0].replace(/\D/g,'').padStart(8,'0');const expected=(10-[2,9,8,7,6,3,4].reduce((sum,w,i)=>sum+Number(digits[i])*w,0)%10)%10;
   add('Número con formato posible de cédula',m[0],expected===Number(digits[7])?'Formato y dígito verificador compatibles; no acredita identidad. Puede ser otro número: cotejar el contexto.':'Dígito verificador incompatible si este número representa una cédula uruguaya. Cotejar el documento; no corregir automáticamente.');
  }
  if(observations.length>=200)observations.push({kind:'Alcance limitado',fragment:'',basis:'Se muestran hasta 200 señales. Puede haber otras coincidencias sin mostrar; revisar integralmente.'});
  if(!observations.length)add('Sin señales en estos controles','', 'No garantiza ausencia de errores: el alcance es limitado.');
  return observations;
 }
 return {read,checks,fromDocx};
})();
