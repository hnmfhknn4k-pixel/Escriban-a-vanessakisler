export type Section={margins:Record<string,number|null>;width:number|null;height:number|null};
const cm=(value:string|null)=>value===null?null:Math.round(Number(value)*2.54/1440*100)/100;
export async function extractXml(buffer:ArrayBuffer){
const bytes=new Uint8Array(buffer),view=new DataView(buffer),limit=12*1024*1024;
function u16(n:number){if(n<0||n+2>bytes.length)throw new Error('Word dañado.');return view.getUint16(n,true)}
function u32(n:number){if(n<0||n+4>bytes.length)throw new Error('Word dañado.');return view.getUint32(n,true)}
let end=-1;for(let i=bytes.length-22;i>=Math.max(0,bytes.length-65557);i--){if(u32(i)===0x06054b50&&i+22+u16(i+20)===bytes.length){end=i;break}}
if(end<0||u16(end+4)!==0||u16(end+6)!==0)throw new Error('ZIP Word no compatible.');
let offset=u32(end+16);const entries=u16(end+10);if(entries>10000)throw new Error('Demasiadas entradas en el Word.');
for(let i=0;i<entries;i++){if(u32(offset)!==0x02014b50)throw new Error('Word dañado.');const flags=u16(offset+8),method=u16(offset+10),size=u32(offset+20),uncompressed=u32(offset+24),nameLength=u16(offset+28),extra=u16(offset+30),comment=u16(offset+32),local=u32(offset+42);if(offset+46+nameLength>bytes.length)throw new Error('Word dañado.');const name=new TextDecoder().decode(bytes.slice(offset+46,offset+46+nameLength));
if(name==='word/document.xml'){if(flags&1)throw new Error('No se admiten documentos cifrados.');if(size>limit||uncompressed>limit)throw new Error('El contenido del Word excede el límite.');if(u32(local)!==0x04034b50)throw new Error('Word dañado.');const start=local+30+u16(local+26)+u16(local+28);if(start+size>bytes.length)throw new Error('Word incompleto.');const compressed=bytes.slice(start,start+size);if(method===0)return new TextDecoder().decode(compressed);if(method!==8)throw new Error('Compresión no compatible.');let stream:ReadableStream<Uint8Array>;try{stream=new Blob([compressed]).stream().pipeThrough(new DecompressionStream('deflate-raw'))}catch{throw new Error('Este navegador no permite abrir Word. Actualizalo o pegá el texto.')}const reader=stream.getReader(),chunks:Uint8Array[]=[];let total=0;while(true){const result=await reader.read();if(result.done)break;total+=result.value.length;if(total>limit){await reader.cancel();throw new Error('Word demasiado grande al descomprimir.')}chunks.push(result.value)}if(total!==uncompressed)throw new Error('El Word está incompleto o dañado.');const output=new Uint8Array(total);let pos=0;for(const chunk of chunks){output.set(chunk,pos);pos+=chunk.length}return new TextDecoder().decode(output)}offset+=46+nameLength+extra+comment}
throw new Error('No se encontró el documento dentro del Word.');}
export async function readDocx(buffer:ArrayBuffer){
const xml=await extractXml(buffer);const parsed=new DOMParser().parseFromString(xml,'application/xml');if(parsed.getElementsByTagName('parsererror').length)throw new Error('El XML del Word está dañado.');
const ns='http://schemas.openxmlformats.org/wordprocessingml/2006/main';
const sections:Section[]=Array.from(parsed.getElementsByTagNameNS(ns,'sectPr')).map(s=>{const m=s.getElementsByTagNameNS(ns,'pgMar')[0],z=s.getElementsByTagNameNS(ns,'pgSz')[0];return {margins:Object.fromEntries([['superior','top'],['inferior','bottom'],['izquierdo','left'],['derecho','right']].map(([label,key])=>[label,cm(m?.getAttributeNS(ns,key)??null)])),width:cm(z?.getAttributeNS(ns,'w')??null),height:cm(z?.getAttributeNS(ns,'h')??null)}});
const paragraphs=Array.from(parsed.getElementsByTagNameNS(ns,'p')).filter(p=>!p.closest('del')).map(p=>Array.from(p.getElementsByTagName('*')).map(el=>el.namespaceURI!==ns?'':el.localName==='t'?el.textContent:el.localName==='tab'?'\t':['br','cr'].includes(el.localName)?'\n':'').join(''));
return {text:paragraphs.join('\n'),sections};
}
