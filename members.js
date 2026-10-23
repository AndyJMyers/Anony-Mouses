'use strict';
const $ = id => document.getElementById(id);
const mapZoom=AnonyMapZoom.attach($('memberMap'),$('memberMapWorld'));
const signupMouse=AnonyMouse.builder($('memberSignupMouse'));
const editMouse=AnonyMouse.builder($('memberEditMouse'));
let session = null, draft = null, activeThread = null, threads = [], matches = [], districts = [], refreshTimer = null, epoch = 0;
let entranceAction = null, busy = false, previewUrl = null, renderedSignature = '';
const revealedImages = new Set();
function clearImageDraft(){if(previewUrl)URL.revokeObjectURL(previewUrl);previewUrl=null;$('sendImage').reset();$('imagePreview').removeAttribute('src');$('imagePreview').hidden=true;}
function appendImage(container,m){if(!m.image)return;const image=node('img');image.alt='Private picture shared in this conversation';image.className='message-image';image.hidden=!revealedImages.has(m.id);if(!image.hidden)image.src=m.image.url;const reveal=button(image.hidden?'View picture':'Hide picture',async()=>{image.hidden=!image.hidden;if(image.hidden){image.removeAttribute('src');revealedImages.delete(m.id);reveal.textContent='View picture';}else{revealedImages.add(m.id);image.src=m.image.url;reveal.textContent='Hide picture';}});image.addEventListener('error',()=>{image.hidden=true;image.removeAttribute('src');revealedImages.delete(m.id);reveal.textContent='Picture unavailable';status('Picture unavailable: it may have expired or access changed.');});container.append(reveal,image);}
function status(message) { $('status').textContent = message; }
function node(tag, text, cls) { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; if (cls) n.className = cls; return n; }
function button(text, action, cls = 'quiet') { const b = node('button', text, cls); b.type = 'button'; b.addEventListener('click', () => run(action)); return b; }
function formData(form) { return Object.fromEntries(new FormData(form)); }
async function api(path, method = 'GET', data) {
  const binary=data instanceof Blob; const headers = {}; if (data !== undefined) headers['Content-Type'] = binary ? data.type : 'application/json';
  if (method !== 'GET' && session) headers['X-CSRF-Token'] = session.csrf;
  const res = await fetch('/api/' + path, { method, credentials: 'same-origin', cache: 'no-store', headers, body: data === undefined ? undefined : binary ? data : JSON.stringify(data) });
  const result = await res.json();
  if (!res.ok) { if (res.status === 401 && session) signedOut(); throw new Error(result.error || 'Please try again.'); }
  return result;
}
async function run(action) {
  if (busy) return;
  busy = true; document.querySelectorAll('button').forEach(b => b.disabled = true);
  try { await action(); } catch (e) { status(e.message || 'Unable to reach the local service.'); }
  finally { busy = false; document.querySelectorAll('button').forEach(b => b.disabled = false); }
}
function tab(name) {
  for (const id of ['signin', 'signup', 'trial', 'recovery', 'recoveryResult']) $(id).hidden = id !== name;
  if (name !== 'trial') draft = null;
}
function signedOut() {
  epoch++; revealedImages.clear(); renderedSignature=''; clearImageDraft(); clearInterval(refreshTimer); refreshTimer = null; session = null; activeThread = null; threads = []; matches = []; draft = null; entranceAction = null;
  for (const id of ['matches','memberMap','threads','messages','kept']) $(id).replaceChildren();
  $('recoveryCode').textContent = ''; $('messageBody').value = ''; $('account').hidden = true; $('entrance').hidden = false; $('logout').hidden = true; $('chat').hidden = true; $('keepCount').textContent = '0';
  $('signup').reset(); $('signin').reset(); $('recovery').reset(); tab('signin');
}
function date(ts) { return new Date(ts * 1000).toLocaleDateString(undefined, { day:'numeric', month:'short', year:'numeric' }); }
async function enter() {
  session = await api('session'); epoch++;
  $('entrance').hidden = true; $('account').hidden = false; $('logout').hidden = false;
  $('recoveryCode').textContent = ''; draft = null;
  $('welcome').textContent = 'Welcome, ' + session.profile.alias + '.';
  $('membership').textContent = session.membership.active ? 'Access until ' + date(session.membership.access_until) : session.membership.scheduled ? 'Your paid month starts ' + date(session.membership.starts_at) + ' · until ' + date(session.membership.access_until) : 'Payment required · website month £20, planned standard £50 · checkout not connected';
  for (const field of ['alias','bio','wants','district','age_range']) $('editProfile').elements[field].value = session.profile[field];
  editMouse.set(session.profile.avatar);
  $('editProfile').elements.visible.checked = session.profile.visible;
  $('search').elements.district.value = session.profile.district;
  status('Your local test account is signed in. A hello is only a hello.');
  await view('discover'); await refreshKeepsakes();
  clearInterval(refreshTimer);
  refreshTimer = setInterval(() => { if (session && !busy && document.visibilityState === 'visible' && !$('inbox').hidden) run(async () => { await refreshInbox(); if (activeThread) await readMessages(); }); }, 10000);
}
async function view(name) {
  for (const id of ['discover','inbox','keepsakes','settings']) $(id).hidden = id !== name;
  document.querySelectorAll('[data-view]').forEach(b => { b.className = b.dataset.view === name ? 'gold' : 'quiet'; b.setAttribute('aria-pressed', String(b.dataset.view === name)); });
  if (name === 'discover' && session.membership.active) await search();
  if (name === 'inbox') await refreshInbox();
  if (name === 'keepsakes') await refreshKeepsakes();
}
function showCode(code, action) { $('recoveryCode').textContent = code; tab('recoveryResult'); entranceAction = action; }
document.querySelectorAll('[data-tab]').forEach(b => b.addEventListener('click', () => tab(b.dataset.tab)));
document.querySelectorAll('[data-view]').forEach(b => b.addEventListener('click', () => run(() => view(b.dataset.view))));
$('signin').addEventListener('submit', e => { e.preventDefault(); run(async () => { const data = formData(e.target); await api('login','POST',data); e.target.reset(); await enter(); }); });
$('signup').addEventListener('submit', e => { e.preventDefault(); draft = { ...formData(e.target), avatar:signupMouse.get(), adult:true, consent:true }; $('trialAlias').textContent = draft.alias; tab('trial'); });
$('backSignup').addEventListener('click', () => tab('signup'));
$('startTrial').addEventListener('click', () => run(async () => {
  if (!draft) throw new Error('Please complete your details first.');
  const result = await api('register','POST',draft);
  // Once registration succeeds, never offer a second submission, even if login fails.
  const credentials = { login:draft.login, password:draft.password }; draft = null; $('signup').reset();
  showCode(result.recovery_code, async () => { await api('login','POST',credentials); await enter(); });
  status('Unpaid test account created. Save your recovery code. The operator can add a fictional paid-month fixture locally.');
}));
$('continueEntrance').addEventListener('click', () => run(async () => { const action = entranceAction; entranceAction = null; $('recoveryCode').textContent = ''; if (action) await action(); else tab('signin'); }));
$('recovery').addEventListener('submit', e => { e.preventDefault(); run(async () => { const result = await api('recover','POST',formData(e.target)); e.target.reset(); showCode(result.recovery_code, async () => { tab('signin'); status('Access recovered. Sign in with your new password.'); }); status('Recovery succeeded. Save the replacement code.'); }); });
$('logout').addEventListener('click', () => run(async () => { await api('logout','POST',{}); signedOut(); status('Signed out.'); }));
async function search() {
  const values = formData($('search')); const found = await api('discover','POST',{district:values.district,radius_km:Number(values.radius_km)});
  matches = found; $('matches').replaceChildren(); $('memberMapWorld').replaceChildren();mapZoom.reset();
  const centre = districts.find(d => d.code === values.district);
  if (!found.length) $('matches').append(node('p','No sparks here yet. Create another fictional adult account in a separate browser session.'));
  for (const p of found) {
    const card = node('article',undefined,'match'); const avatar=node('div',undefined,'mouse-mini');AnonyMouse.mountPortrait(avatar,p.avatar);card.append(avatar,node('h3',p.alias),node('small',p.age_range + ' · ' + p.district + ' · identity unverified'),node('p',p.bio),node('strong','What I’m looking for'),node('p',p.wants));
    card.append(button('Send a little hello ↗', async () => { const result = await api('conversations','POST',{target:p.id}); await view('inbox'); await openThread(result.id); status('Hello requested. Messages begin when the recipient accepts.'); },'gold'));
    $('matches').append(card);
    const pin = button('', async () => { card.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center'}); },'pin');
    pin.setAttribute('aria-label',p.alias + ', ' + p.district + ', ' + p.wants);
    // District centre only; decorative offsets avoid stacking. This is deliberately a schematic.
    const latScale = 111, lonScale = 111 * Math.cos((centre?.lat || 51) * Math.PI / 180), span = Number(values.radius_km);
    const x = centre ? (p.district_centre.lon-centre.lon)*lonScale/span*32 : 0;
    const y = centre ? -(p.district_centre.lat-centre.lat)*latScale/span*32 : 0;
    pin.style.left = Math.max(15,Math.min(85,50+x+p.marker_offset.x)) + '%'; pin.style.top = Math.max(20,Math.min(80,50+y+p.marker_offset.y)) + '%';
    pin.append(node('span','✦','pin-avatar'),node('span',p.alias + ' · ' + p.wants.slice(0,55),'pin-hint')); $('memberMapWorld').append(pin);
  }
  status(found.length + ' test profile' + (found.length === 1 ? '' : 's') + ' near ' + values.district + '.');
}
$('search').addEventListener('submit', e => { e.preventDefault(); run(search); });
$('still').addEventListener('change', e => $('memberMap').classList.toggle('still',e.target.checked));
async function refreshInbox() {
  threads = await api('conversations'); $('threads').replaceChildren();
  if (!threads.length) $('threads').append(node('p','No conversations yet. Find a spark and send a hello.'));
  for (const t of threads) { const b = button(t.other_alias + ' · ' + (t.status === 'accepted' ? 'Conversation open' : t.incoming ? 'Would like to say hello' : 'Awaiting their hello'), () => openThread(t.id),'thread'); b.setAttribute('aria-pressed',String(activeThread?.id===t.id)); $('threads').append(b); }
  if (activeThread) { const current = threads.find(t => t.id === activeThread.id); if (!current) { activeThread = null; revealedImages.clear(); clearImageDraft(); renderedSignature=''; $('chat').hidden = true; $('messages').replaceChildren(); } else activeThread = current; }
}
async function openThread(id) { activeThread = threads.find(t => t.id === id); if (!activeThread) throw new Error('Conversation unavailable.'); $('messageBody').value = ''; clearImageDraft(); renderedSignature=''; await readMessages(); }
async function readMessages() {
  if (!activeThread) return;
  const current = activeThread; const version = epoch; const messages = await api('conversations/' + current.id + '/messages');
  if (version !== epoch || activeThread?.id !== current.id) return;
  $('chat').hidden = false; $('chatTitle').textContent = current.other_alias;
  $('chatNote').textContent = current.status === 'accepted' ? 'Private text and picture conversation · messages expire after 14 days unless you keep your copy. Refreshes every 10 seconds while this view is open.' : current.incoming ? 'Accept only if you fancy a conversation. You can block at any time.' : 'Your hello is waiting for their acceptance.';
  $('accept').hidden = current.status === 'accepted' || !current.incoming; $('send').hidden = current.status !== 'accepted'; $('sendImage').hidden=current.status!=='accepted'; const signature=JSON.stringify([current.id,current.status,messages]);if(signature===renderedSignature)return;renderedSignature=signature; $('messages').replaceChildren();
  for (const m of messages) {
    const bubble = node('article',undefined,'bubble' + (m.sender === session.profile.id ? ' mine' : '')); if(m.body)bubble.append(node('p',m.body));appendImage(bubble,m);bubble.append(node('small',m.saved ? 'Kept by you' : 'Expires ' + date(m.expires)));
    bubble.append(button(m.saved ? 'Remove keepsake' : '♡ Keep this', async () => { await api('keepsakes/' + m.id,m.saved?'DELETE':'POST',m.saved?undefined:{}); await readMessages(); await refreshKeepsakes(); }));
    if (m.sender !== session.profile.id) bubble.append(button('Report this message', () => report(m.id)));
    $('messages').append(bubble);
  }
}
$('refreshInbox').addEventListener('click', () => run(async () => { await refreshInbox(); if (activeThread) await readMessages(); }));
$('accept').addEventListener('click', () => run(async () => { await api('conversations/'+activeThread.id+'/accept','POST',{}); await refreshInbox(); await readMessages(); status('Conversation accepted. Say hello when you fancy.'); }));
$('send').addEventListener('submit', e => { e.preventDefault(); run(async () => { const body = $('messageBody').value.trim(); if (!body) return; await api('conversations/'+activeThread.id+'/messages','POST',{body}); $('messageBody').value = ''; await readMessages(); status('Message sent.'); }); });
async function refreshKeepsakes() {
  const kept = await api('keepsakes'); $('keepCount').textContent = kept.length; $('kept').replaceChildren();
  if (!kept.length) $('kept').append(node('p','Nothing tucked away yet.'));
  for (const m of kept) { const b = node('article',undefined,'bubble'); if(m.body)b.append(node('p',m.body));appendImage(b,m);b.append(button('Remove keepsake', async () => { await api('keepsakes/'+m.id,'DELETE'); await refreshKeepsakes(); })); $('kept').append(b); }
}
$('block').addEventListener('click', () => run(async () => { if (!confirm('Block '+activeThread.other_alias+'? You will disappear from each other’s discovery and conversations.')) return; await api('block','POST',{target:activeThread.other}); activeThread = null; revealedImages.clear(); clearImageDraft(); renderedSignature=''; $('chat').hidden = true; $('messages').replaceChildren(); await refreshInbox(); await refreshKeepsakes(); status('Patron blocked.'); }));
async function report(message_id) { const reason = prompt('Describe your concern. This stores a local test report; it does not alert a support team.'); if (!reason?.trim()) return; await api('report','POST',{target:activeThread.other,reason,message_id}); status('Local test report saved under the separate 90-day evidence rule.'); }
$('report').addEventListener('click', () => run(() => report()));
$('editProfile').addEventListener('submit', e => { e.preventDefault(); run(async () => { const profile = await api('profile','POST',{...formData(e.target),avatar:editMouse.get(),visible:e.target.elements.visible.checked}); session.profile = profile; $('welcome').textContent = 'Welcome, '+profile.alias+'.'; status('Your introduction is saved.'); }); });
$('deleteAccount').addEventListener('click', () => run(async () => { if (!confirm('Permanently delete this test account, its shared conversations and keepsakes? Report evidence follows its separate retention rule.')) return; await api('account','DELETE'); signedOut(); status('Test account deleted. Separately retained report evidence expires under the development rule.'); }));
async function boot() {
  if (location.protocol !== 'http:' || location.hostname !== '127.0.0.1') { $('unavailable').hidden = false; status('Public memberships are not open. This interface is for loopback-only testing.'); return; }
  try { const health = await api('health'); if (health.production_enabled !== false || health.status !== 'local-development') throw new Error('Expected local development service.'); districts = await api('districts'); }
  catch (e) { $('unavailable').hidden = false; status('Local service unavailable: '+e.message); return; }
  try { session = await api('session'); await enter(); }
  catch (e) { signedOut(); status(e.message === 'Sign in required' ? 'Use invented adult test details. Your accounts persist in the local database.' : e.message); }
}
boot();

$('imageFile').addEventListener('change',()=>{if(previewUrl)URL.revokeObjectURL(previewUrl);previewUrl=null;$('imagePreview').hidden=true;$('imagePreview').removeAttribute('src');$('imageConsent').checked=false;const file=$('imageFile').files[0];if(!file)return;if(!['image/jpeg','image/png','image/webp'].includes(file.type)||file.size>5*1024*1024){$('imageFile').value='';status('Choose a still JPG, PNG or WebP up to 5 MB.');return;}previewUrl=URL.createObjectURL(file);$('imagePreview').src=previewUrl;$('imagePreview').hidden=false;});
$('sendImage').addEventListener('submit',e=>{e.preventDefault();run(async()=>{const file=$('imageFile').files[0];if(!file||!$('imageConsent').checked)return;await api('conversations/'+activeThread.id+'/images','POST',file);clearImageDraft();await readMessages();status('Picture sent. The stored copy has no source metadata.');});});

$('quoteForm').addEventListener('submit',e=>{e.preventDefault();run(async()=>{try{const q=await api('/api/quote','POST',{voucher_code:$('memberVoucher').value});$('memberQuote').textContent='£'+(q.amount_minor/100).toFixed(2)+' for one calendar month. No automatic renewal.'+(q.expires_at?' Example invitation expires 30 November 2026, 23:59 UK time. One use per account. No affiliation implied.':'')+' Quote only; no payment taken or price reserved.';}catch(error){$('memberQuote').textContent=error.message;}});});
