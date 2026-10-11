'use strict';
const $=id=>document.getElementById(id); let csrf='',current=null,previewHash='';
function el(tag,text='',cls=''){const n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n;}
function message(text,error=false){$('message').textContent=text;$('message').className=error?'error':'';}
async function api(path,options={}){const headers={...(options.headers||{})};if(options.method&&options.method!=='GET')headers['X-CSRF-Token']=csrf;if(options.body&&!(options.body instanceof FormData))headers['Content-Type']='application/json';const r=await fetch(path,{...options,headers});if(!r.ok){let d;try{d=await r.json();}catch{d={detail:await r.text()};}throw new Error(Array.isArray(d.detail)?d.detail.join(' · '):d.detail||'No se pudo completar la operación');}return r.headers.get('Content-Type')?.includes('application/json')?r.json():r;}
async function perform(fn){try{message('Procesando…');await fn();message('Operación registrada.');}catch(e){message(e.message,true);}}
const post=(path,data)=>api(path,{method:'POST',body:JSON.stringify(data)});
const formData=form=>Object.fromEntries(new FormData(form));
function founded(title){return new Promise(resolve=>{const dialog=$('reason-dialog');$('reason-title').textContent=title;$('reason-form').reset();dialog.onclose=()=>resolve(dialog.returnValue==='ok'?formData($('reason-form')):null);dialog.showModal();});}
function action(label,fn,cls=''){const b=el('button',label,cls);b.type='button';b.addEventListener('click',()=>perform(fn));return b;}
async function casePost(suffix,data){current=await post('/api/cases/'+current.id+suffix,data);render();}
async function refresh(){const items=await api('/api/cases');$('cases').replaceChildren(...items.map(c=>action(c.title,async()=>{current=await api('/api/cases/'+c.id);render();})));}
function tab(name){document.querySelectorAll('.tab').forEach(n=>n.hidden=n.id!=='tab-'+name);document.querySelectorAll('[data-tab]').forEach(n=>n.classList.toggle('active',n.dataset.tab===name));}
document.querySelectorAll('[data-tab]').forEach(n=>n.onclick=()=>tab(n.dataset.tab));
function render(){const c=current;$('empty').hidden=true;$('case').hidden=false;$('case-title').textContent=c.title;$('case-badge').textContent=c.approved?'Aprobado por revisor':'Revisión abierta';$('case-state').textContent=c.id+' · '+c.parties.length+' comparecientes · '+c.changes.length+' propuestas';
 $('warnings').replaceChildren(...c.warnings.map(w=>el('p',w,'notice')));
 $('segments').replaceChildren(...c.working.map(s=>{const box=el('div','','segment');box.append(el('small',s.part+' · bloque '+s.index+(s.deleted?' · texto eliminado preexistente':'')),el('p',s.text));if(!s.deleted&&!c.approved){box.append(action('Proponer modificación',async()=>{if(box.querySelector('.editor'))return;const f=el('form','','editor');const label=el('label','Propuesta (no cambia el original)');const area=el('textarea');area.value=s.text;area.rows=4;label.append(area);f.append(label);const row=el('div','','actions');row.append(action('Ver antes / después',async()=>{const review=el('div','','diff');review.append(el('div',s.text,'before'),el('div',area.value,'after'));f.append(review);row.replaceChildren(action('Registrar propuesta',async()=>{const why=await founded('Fundamento de la propuesta');if(why)await casePost('/changes',{...why,segment:s.id,after:area.value});},'primary'),action('Cancelar',async()=>f.remove()));}),action('Cancelar',async()=>f.remove()));f.append(row);box.append(f);}));}if(!s.deleted&&!c.approved&&c.parties.length)box.append(action('Corregir discrepancia desde ficha',async()=>identityCorrectionEditor(s,box,c)));return box;}));
 $('changes').replaceChildren(...c.changes.map(ch=>{const n=el('div','','change');n.append(el('small',ch.status+' · propuesta de '+ch.author));const diff=el('div','','diff');diff.append(el('div',ch.before,'before'),el('div',ch.after,'after'));n.append(diff,el('p',ch.reason));const row=el('div','','actions');if(!c.approved){for(const [label,status] of (ch.status==='pending'?[['Aceptar','accepted'],['Rechazar','rejected'],['Deshacer','undone']]:ch.status!=='undone'?[['Deshacer','undone']]:[]))row.append(action(label,async()=>{const why=await founded(label+' cambio');if(why)await casePost('/changes/'+ch.id,{...why,status});}));}n.append(row);return n;}));
 $('parties').replaceChildren(...c.parties.map(p=>{const n=el('div','','panel');n.append(el('h3',p.name),el('p','Cédula '+p.ci),el('p','Cotejada por '+p.verified_by+' · '+p.evidence,'quiet'));return n;}));
 $('observations').replaceChildren(...c.observations.map(o=>{const n=el('article','','observation');n.append(el('span',o.kind==='hecho'?'Hecho mecánico':o.kind==='inferencia'?'Inferencia / supuesto':'Faltante o indeterminable','badge'),el('h3',o.finding),el('blockquote',o.fragment),el('p','Fundamento: '+o.basis),el('p','Alternativas: '+o.alternatives),el('p','Incertidumbre: '+o.uncertainty),el('p','Qué cambiaría el criterio: '+o.reconsider),el('p','Decisión: '+(o.decision||'pendiente'),'quiet'));const row=el('div','','actions');if(!c.approved)for(const [label,decision] of [['Aceptar observación','accepted'],['Rechazar con evidencia','rejected'],['Cuestionar / reabrir','challenged']])row.append(action(label,async()=>{const why=await founded(label);if(why)await casePost('/observations/'+o.id,{...why,decision});}));n.append(row);return n;}));
 $('blockers').replaceChildren(...(c.blockers.length?c.blockers.map(b=>el('p',b,'blocker')):[el('p','Controles completados. La decisión profesional sigue siendo necesaria.','notice')]));
 $('approve').disabled=c.approved||c.blockers.length>0;$('reopen').hidden=!c.approved;$('final-link').hidden=!c.approved;
 for(const [id,kind] of [['original-link','original'],['draft-link','draft'],['final-link','final']])$(id).href='/api/cases/'+c.id+'/download/'+kind;
 $('hashes').replaceChildren(...[['Original',c.original_hash],['Texto importado',c.text_hash],['Texto analizado',c.analysis?.sha256||'Análisis pendiente'],['Word final',c.final_hash||'Aprobación pendiente']].map(([name,hash])=>{const n=el('p',name+': ');n.append(el('code',hash));return n;}));
 $('retention').textContent='Fecha de revisión de conservación: '+new Date(c.retention_until).toLocaleDateString('es-UY')+'. Auditoría retenida cifrada; eliminación física y backups requieren procedimiento externo.';
 $('recorded-sources').replaceChildren(...c.sources.map(s=>{const n=el('div','','panel');n.append(el('h3',s.title),el('p',s.article),el('blockquote',s.excerpt),el('p',s.verification,'quiet'));return n;}));
 previewHash='';$('privacy-preview').textContent='';$('privacy-state').textContent='';$('audit-events').replaceChildren();
 for(const id of ['party-form','source-form','corroboration-form'])$(id).querySelectorAll('input,textarea,button').forEach(n=>n.disabled=c.approved);
}
async function entered(){const me=await api('/api/me');csrf=me.csrf;$('login').hidden=true;$('workspace').hidden=false;$('logout').hidden=false;await refresh();await loadTemplates();}
$('login-form').onsubmit=e=>{e.preventDefault();perform(async()=>{const data=await post('/api/login',formData(e.target));csrf=data.csrf;e.target.reset();await entered();});};
$('logout').onclick=()=>perform(async()=>{await post('/api/logout',{});location.reload();});
$('refresh').onclick=()=>perform(refresh);
$('import-form').onsubmit=e=>{e.preventDefault();perform(async()=>{current=await api('/api/cases',{method:'POST',body:new FormData(e.target)});render();tab('review');e.target.reset();await refresh();});};
$('party-form').onsubmit=e=>{e.preventDefault();perform(async()=>{await casePost('/parties',formData(e.target));e.target.reset();});};
$('source-form').onsubmit=e=>{e.preventDefault();perform(async()=>{await casePost('/source',formData(e.target));e.target.reset();});};
$('analyze').onclick=()=>perform(()=>casePost('/analyze',{}));
$('privacy-form').onsubmit=e=>{e.preventDefault();perform(async()=>{const d=await post('/api/cases/'+current.id+'/pseudonymize',{extra_terms:formData(e.target).terms.split('\n').map(x=>x.trim()).filter(Boolean)});previewHash=d.sha256;$('privacy-preview').textContent=d.text;$('privacy-state').textContent=d.notice+(d.residuals.length?' Identificadores pendientes: '+d.residuals.join(', '):' Sin coincidencias residuales automáticas; esto no descarta identificación indirecta.');});};
$('corroboration-form').onsubmit=e=>{e.preventDefault();perform(async()=>{await casePost('/corroborate',{...formData(e.target),all_mentions_checked:e.target.elements.checked.checked,print_checked:e.target.elements.printed.checked,reviewed_sha256:current.reviewed_hash});});};
$('approve').onclick=()=>perform(async()=>{const why=await founded('Aprobación final');if(why)await casePost('/approve',why);});
$('reopen').onclick=()=>perform(async()=>{const why=await founded('Reapertura y motivo de corrección');if(why)await casePost('/reopen',why);});
$('challenge').onclick=()=>perform(async()=>{const why=await founded('Cuestionamiento de posible defecto del sistema');if(why)await casePost('/challenge',why);});
$('share-form').onsubmit=e=>{e.preventDefault();perform(async()=>{await post('/api/cases/'+current.id+'/share',formData(e.target));e.target.reset();});};
$('delete').onclick=()=>perform(async()=>{const why=await founded('Eliminar expediente: auditoría y backups no se borran con esta acción');if(!why)return;await post('/api/cases/'+current.id+'/delete',why);current=null;$('case').hidden=true;$('empty').hidden=false;await refresh();});
$('load-audit').onclick=()=>perform(async()=>{const a=await api('/api/cases/'+current.id+'/audit');$('audit-events').replaceChildren(el('p',a.verification.events+' eventos en cadena · integridad local verificada','notice'),...a.events.map(e=>{const n=el('div','','event');n.append(el('h3',e.action),el('p',e.actor+' · hora declarada del servidor: '+new Date(e.server_time).toLocaleString('es-UY')),el('p',e.details.reason||e.details.evidence||'Evento técnico sin decisión profesional'),el('code',e.mac));return n;}));});
$('new-draft').onclick=()=>perform(async()=>{const title=prompt('Objeto del borrador (sin datos personales). Se generan campos pendientes para revisión.');if(!title)return;const r=await post('/api/draft',{title});const url=URL.createObjectURL(await r.blob());const a=el('a');a.href=url;a.download='EscribanIA-borrador-base.docx';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
(async()=>{try{const status=await api('/api/status');$('source-list').replaceChildren(...status.sources.map(s=>{const p=el('p');const a=el('a',s.title);a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';p.append(a);return p;}));await entered();}catch(e){if(!e.message.includes('Iniciá sesión'))message(e.message,true);}})();

$('ai-form').onsubmit=e=>{e.preventDefault();perform(async()=>{if(!previewHash)throw new Error('Primero revisá una previsualización actual');const result=await post('/api/cases/'+current.id+'/assist',{module:formData(e.target).module,reviewed:e.target.elements.reviewed.checked,preview_hash:previewHash,extra_terms:formData($('privacy-form')).terms.split('\n').map(x=>x.trim()).filter(Boolean)});current=result.case;render();$('ai-draft').textContent=result.draft||'Observaciones agregadas a Fundamentos. No se aplicaron cambios al documento.';});};

function identityCorrectionEditor(segment,box,caseData){
 if(box.querySelector('.editor'))return;
 const form=el('form','','editor'),select=el('select'),label=el('label','Dato cotejado de destino');
 for(const party of caseData.parties)for(const [field,title] of [['name','Nombre completo'],['ci','Cédula']]){const option=el('option',title+' · '+party[field]);option.value=party.id+':'+field;select.append(option);}
 label.append(select);form.append(label);const oldLabel=el('label','Mención incorrecta exacta en este bloque');const old=el('input');oldLabel.append(old);form.append(oldLabel);
 const diff=el('div','','diff');form.append(diff);
 function preview(){const [pid,field]=select.value.split(':');const party=caseData.parties.find(p=>p.id===pid);diff.replaceChildren(el('div',segment.text,'before'),el('div',old.value?segment.text.replace(old.value,party[field]):'Seleccioná el dato incorrecto; el destino se toma exclusivamente de la ficha.','after'));}
 old.oninput=preview;select.onchange=preview;preview();const row=el('div','','actions');row.append(action('Proponer corrección cotejada',async()=>{const why=await founded('Corrección determinista desde ficha cotejada');if(!why)return;const [party,field]=select.value.split(':');await casePost('/identity-fix',{...why,party,field,segment:segment.id,old:old.value});},'primary'),action('Cancelar',async()=>form.remove()));form.append(row);box.append(form);
}

$('party-form').elements.name.addEventListener('input',e=>{$('name-preview').textContent='Se registrará: '+e.target.value.trim().normalize('NFC').toLocaleUpperCase('es-UY');});

async function loadTemplates(){
 const templates=await api('/api/templates');
 $('template-list').replaceChildren(...templates.map(t=>{
  const panel=el('section','','panel');panel.append(el('h3',t.title),el('p','Borrador · '+t.fields.length+' campos y avisos pendientes','quiet'));
  const adaptations=el('details'),summary=el('summary','Revisar adaptaciones del modelo');adaptations.append(summary,el('p',t.notice,'quiet'));
  for(const change of t.changes){const diff=el('div','','diff');diff.append(el('div',change.before||'(párrafo vacío)','before'),el('div',change.after,'after'));adaptations.append(diff);}
  panel.append(adaptations,el('p',t.margin_policy,'quiet'));
  const label=el('label','','check'),check=el('input');check.type='checkbox';label.append(check,el('span','Revisé las adaptaciones y entiendo que requiere completar datos y revisión profesional.'));
  const use=action(t.id==='compraventa-automotor'?'Abrir borrador de automotor':'Abrir borrador conjunto',async()=>{current=await post('/api/templates/'+t.id+'/cases',{review_required_acknowledged:check.checked});render();tab('review');await refresh();},'primary');use.disabled=true;check.onchange=()=>use.disabled=!check.checked;
  const download=el('a','Descargar plantilla Word','button');download.href='/api/templates/'+t.id+'/download';panel.append(label,use,download);return panel;
 }));
}
