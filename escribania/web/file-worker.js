'use strict';
importScripts('/static/vendor/fflate-0.8.2.js');
const LIMIT=40*1024*1024,XML_LIMIT=16*1024*1024;
function xmlPart(name){return /^(?:word\/(?:document|header\d+|footer\d+|footnotes|endnotes|comments)\.xml|.*\.rels|\[Content_Types\]\.xml)$/.test(name);}
function zipDirectory(bytes){
 const v=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength);let end=-1;
 for(let i=bytes.length-22;i>=Math.max(0,bytes.length-65557);i--){if(v.getUint32(i,true)===0x06054b50&&i+22+v.getUint16(i+20,true)===bytes.length){end=i;break;}}
 if(end<0)throw Error('DOCX inválido: falta el directorio ZIP.');
 const count=v.getUint16(end+10,true),offset=v.getUint32(end+16,true),size=v.getUint32(end+12,true);
 if(v.getUint16(end+4,true)||v.getUint16(end+6,true)||count!==v.getUint16(end+8,true)||count===65535||size===0xffffffff||offset===0xffffffff)throw Error('ZIP dividido o ZIP64 no admitido.');
 if(count>2000||offset+size>end)throw Error('El DOCX excede los límites o tiene un directorio inválido.');
 let p=offset,total=0,xmlTotal=0;const names=new Set();
 for(let i=0;i<count;i++){
  if(p+46>offset+size||v.getUint32(p,true)!==0x02014b50)throw Error('Directorio DOCX inválido.');
  const flags=v.getUint16(p+8,true),method=v.getUint16(p+10,true),compressed=v.getUint32(p+20,true),uncompressed=v.getUint32(p+24,true),n=v.getUint16(p+28,true),extra=v.getUint16(p+30,true),comment=v.getUint16(p+32,true);
  if(p+46+n+extra+comment>offset+size||(flags&1)||![0,8].includes(method)||compressed===0xffffffff||uncompressed===0xffffffff)throw Error('DOCX cifrado, corrupto o con compresión no admitida.');
  const name=new TextDecoder('utf-8',{fatal:true}).decode(bytes.subarray(p+46,p+46+n));
  if(names.has(name)||name.includes('..')||name.includes('\\'))throw Error('Partes DOCX duplicadas o rutas no admitidas.');names.add(name);
  total+=uncompressed;if(xmlPart(name))xmlTotal+=uncompressed;
  if(total>LIMIT||xmlTotal>XML_LIMIT)throw Error('El contenido descomprimido excede el límite de seguridad.');
  p+=46+n+extra+comment;
 }
 if(p!==offset+size||!names.has('word/document.xml')||!names.has('[Content_Types].xml'))throw Error('El archivo no es un DOCX válido.');
 return [...names];
}
onmessage=e=>{
 try{
  const bytes=new Uint8Array(e.data);if(bytes.length>8*1024*1024)throw Error('El archivo supera 8 MB.');
  const names=zipDirectory(bytes);const entries=fflate.unzipSync(bytes,{filter:f=>xmlPart(f.name)&&f.originalSize<=XML_LIMIT});
  const parts={};let actual=0;
  for(const [name,data] of Object.entries(entries)){
   actual+=data.length;if(actual>XML_LIMIT)throw Error('Texto XML demasiado extenso.');
   const encoding=data[0]===255&&data[1]===254?'utf-16le':data[0]===254&&data[1]===255?'utf-16be':'utf-8';
   parts[name]=new TextDecoder(encoding,{fatal:true}).decode(data);
  }
  postMessage({names,parts});
 }catch(error){postMessage({error:error.message||'No se pudo leer el DOCX.'});}
};
