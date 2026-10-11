export type Finding={title:string;detail:string;excerpt?:string};
export function reviewText(text:string):Finding[]{
 const findings:Finding[]=[];
 const placeholders=[...text.matchAll(/\[[^\]\n]+\]/g)].map(m=>m[0]);
 if(placeholders.length)findings.push({title:'Campos pendientes',detail:`${placeholders.length} campos entre corchetes. Revisá si requieren completar.`,excerpt:[...new Set(placeholders)].slice(0,20).join(' · ')});
 const cedulas=[...text.matchAll(/\b\d{1,2}\.\d{3}\.\d{3}-\d\b/g)].map(m=>m[0]);
 if(cedulas.length)findings.push({title:'Identificaciones detectadas',detail:'Comprobá estos números contra la documentación original. Este control no valida identidad.',excerpt:[...new Set(cedulas)].join(' · ')});
 const repeated=[...text.matchAll(/\b([\p{L}]+)\s+\1\b/giu)].map(m=>m[0]);
 if(repeated.length)findings.push({title:'Posibles palabras repetidas',detail:'Revisá las repeticiones en su contexto.',excerpt:repeated.slice(0,20).join(' · ')});
 if(!findings.length)findings.push({title:'Sin coincidencias en los controles locales',detail:'Solo se buscaron corchetes pendientes, identificaciones con formato habitual y palabras repetidas. No implica validez jurídica.'});
 return findings;
}
export function surnamePreview(text:string,surname:string){
 if(!surname.trim())return {text,count:0};
 const escaped=surname.trim().replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const re=new RegExp(`(?<![\\p{L}\\p{N}_])${escaped}(?![\\p{L}\\p{N}_])`,'giu');let count=0;
 const updated=text.replace(re,m=>{const upper=m.toLocaleUpperCase('es');if(m!==upper)count++;return upper});
 return {text:updated,count};
}
