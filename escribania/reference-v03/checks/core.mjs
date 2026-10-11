import assert from 'node:assert/strict';
import {reviewText,surnamePreview} from '../lib/review.ts';
import {extractXml} from '../lib/docx.ts';
import {deflateRawSync} from 'node:zlib';
assert.equal(surnamePreview('Pérez, Pérez de León y Pérezano','Pérez').text,'PÉREZ, PÉREZ de León y Pérezano');
assert.equal(surnamePreview('Ana Pérez de León','Pérez de León').count,1);
assert.equal(reviewText('El el precio es [PRECIO]')[0].title,'Campos pendientes');
const xml='<w:document>texto áéñ</w:document>',name=Buffer.from('word/document.xml'),raw=Buffer.from(xml),compressed=deflateRawSync(raw);
function fixture(method){const data=method===8?compressed:raw;const local=Buffer.alloc(30);local.writeUInt32LE(0x04034b50);local.writeUInt16LE(method,8);local.writeUInt32LE(data.length,18);local.writeUInt32LE(raw.length,22);local.writeUInt16LE(name.length,26);const central=Buffer.alloc(46);central.writeUInt32LE(0x02014b50);central.writeUInt16LE(method,10);central.writeUInt32LE(data.length,20);central.writeUInt32LE(raw.length,24);central.writeUInt16LE(name.length,28);const start=local.length+name.length+data.length,end=Buffer.alloc(22);end.writeUInt32LE(0x06054b50);end.writeUInt16LE(1,8);end.writeUInt16LE(1,10);end.writeUInt32LE(central.length+name.length,12);end.writeUInt32LE(start,16);const bytes=Buffer.concat([local,name,data,central,name,end]);return bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)}
assert.equal(await extractXml(fixture(0)),xml);assert.equal(await extractXml(fixture(8)),xml);await assert.rejects(()=>extractXml(new ArrayBuffer(20)));
console.log('Controles de texto, límites de nombres y extracción ZIP: correctos.');
