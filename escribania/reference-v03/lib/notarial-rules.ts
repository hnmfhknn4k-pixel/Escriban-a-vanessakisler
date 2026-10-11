/** Verified regulatory requirements. No unverified numerical margin is supplied. */
export const NOTARIAL_RULES = Object.freeze({
 id:'UY-PAPEL-NOTARIAL-ART39-v1',
 source:'https://www.impo.com.uy/bases/acordadas-scj-originales/7533-2004',
 authority:'Suprema Corte de Justicia',
 rule:'Acordada 7533, artículo 39',
 checkedAt:'2026-10-11',
 scope:'Papel notarial rayado o liso',
 defaultPaper:'liso',
 workflow:'Impresión desde PC sobre papel notarial liso',
 maxLinesPerSide:25,
 maxCharactersPerLine:55,
 minLineSpacingMm:8,
 marginRequirement:'El papel liso debe respetar los márgenes establecidos para el rayado.',
 marginCm:Object.freeze({superior:null,inferior:null,izquierdo:null,derecho:null}),
 marginStatus:'Pendiente de especificación técnica validada del papel rayado',
 measurementStatus:'El texto extraído no permite determinar renglones impresos, caracteres por renglón ni espaciado físico.',
});
