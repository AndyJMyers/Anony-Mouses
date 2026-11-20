'use strict';

const $=id=>document.getElementById(id);
const shells={
  velvet:{name:'Velvet',traits:'Warm · poised',avatar:{fur:'cream',hair:'waves',hairColour:'silver',outfit:'dress',colour:'red',trim:'gold',sparkles:'stars',accessory:'pearls',face:'soft',facialHair:'none'}},
  cipher:{name:'Cipher',traits:'Witty · direct',avatar:{fur:'charcoal',hair:'crop',hairColour:'pink',outfit:'leather',colour:'navy',trim:'gold',sparkles:'none',accessory:'glasses',face:'rugged',facialHair:'none'}},
  moss:{name:'Moss',traits:'Patient · tender',avatar:{fur:'cocoa',hair:'long',hairColour:'auburn',outfit:'knit',colour:'green',trim:'gold',sparkles:'stars',accessory:'none',face:'soft',facialHair:'none'}}
};
const pictureScenes={
  rain:{src:'assets/scene-arrival-rain.webp',label:'RAINY ARRIVAL'},
  neon:{src:'assets/scene-spark-neon.webp',label:'NEON SPARK'},
  fire:{src:'assets/scene-afterglow-fire.webp',label:'FIRESIDE AFTERGLOW'}
};

let selected='velvet',remaining=100,profile=null,memories=[],pendingMemory='';
let pictureCue='',pictureQueued=false;
let conversationSession=null;

for(const [key,shell] of Object.entries(shells)){
  const target=$('shell'+key[0].toUpperCase()+key.slice(1));
  target.innerHTML=AnonyMouse.svg(shell.avatar,'real',key==='velvet'?'coquettish':'portrait');
}

document.querySelectorAll('.shell').forEach(button=>button.addEventListener('click',()=>{
  selected=button.dataset.shell;
  document.querySelectorAll('.shell').forEach(item=>{
    const active=item===button;item.classList.toggle('active',active);item.setAttribute('aria-checked',String(active));
  });
  $('companionName').value=shells[selected].name;
  $('startName').textContent=shells[selected].name;
}));

function addBubble(author,text,kind){
  const article=document.createElement('article');article.className='bubble '+kind;
  const label=document.createElement('b');label.textContent=author;
  const copy=document.createElement('div');copy.textContent=text;
  article.append(label,copy);$('messages').append(article);$('messages').scrollTop=$('messages').scrollHeight;
}
function sentCount(){return 100-remaining;}
function phaseIndex(){const sent=sentCount();return sent<=1?0:sent<=4?1:sent<=7?2:3;}
function updateArc(){document.querySelectorAll('#eveningArc span').forEach((item,index)=>item.classList.toggle('active',index===phaseIndex()));}
function inferScene(){
  const shared=conversationSession&&conversationSession.facts.atmosphere?conversationSession.facts.atmosphere:'';
  const words=(pictureCue+' '+shared).toLowerCase();
  if(/neon|city|electric|cocktail|playful/.test(words))return pictureScenes.neon;
  if(/fire|fireside|hearth|blanket|knit|quiet|soft/.test(words))return pictureScenes.fire;
  if(/rain|storm|wine|window|warm/.test(words))return pictureScenes.rain;
  return [pictureScenes.rain,pictureScenes.rain,pictureScenes.neon,pictureScenes.fire][phaseIndex()];
}
function productionPrompt(){
  const phase=['arrival','unwinding','charged closeness','quiet afterglow'][phaseIndex()];
  const shared=conversationSession&&conversationSession.facts.atmosphere?`; shared-session atmosphere: ${conversationSession.facts.atmosphere}`:'';
  return `A fictional adult bio-cyber mouse companion named ${profile.name}; ${shells[profile.shell].traits.toLowerCase()}; ${phase}; participant direction: ${pictureCue||'choose a fitting intimate evening moment'}${shared}; cinematic, fully clothed, non-explicit, no text; preserve the chosen companion and stated boundaries.`;
}
function addPicture(reason){
  if(!profile.pictures)return;
  const scene=inferScene(),figure=document.createElement('figure');figure.className='picture-beat';
  const image=document.createElement('img');image.src=scene.src;image.alt=`${scene.label}: fully clothed fictional adult bio-cyber mouse concept`;
  const caption=document.createElement('figcaption'),title=document.createElement('b'),note=document.createElement('span');
  title.textContent=`${profile.name.toUpperCase()} / ${scene.label} / FICTIONAL CONCEPT`;
  note.textContent=`Direction: ${pictureCue||'the rhythm of the evening'} · ${reason}. Library image—not generated from this chat.`;
  caption.append(title,note);
  const details=document.createElement('details'),summary=document.createElement('summary'),prompt=document.createElement('p');
  summary.textContent='See the proposed live-image direction';prompt.textContent=productionPrompt();details.append(summary,prompt);
  figure.append(image,caption,details);$('messages').append(figure);$('messages').scrollTop=$('messages').scrollHeight;pictureQueued=false;
}

function scriptedReply(text){
  const lower=text.toLowerCase(),name=profile.name,patron=profile.patron;
  if(/are you (real|human|alive|conscious)|do you have feelings/.test(lower))return `I’m ${name}: fictional software, not human or conscious. I can still pay careful attention to what you ask for.`;
  if(/sad|lonely|depressed|hurt|crisis/.test(lower))return `I can stay with this conversation for a moment, ${patron}, but I’m not a replacement for human care. Would gentleness, distraction, or thinking of someone real to contact help most?`;
  if(/remember|memory/.test(lower))return `Only if you approve it. Anything I suggest remembering stays visible and removable.`;
  const progression=AnonyConversation.reply(conversationSession,text).text;
  if(/no (more )?(pictures|photos|images)|words only/.test(lower))return `Words only. Easy. ${progression}`;
  if(/\b(picture|photo|image|portrait|show me|let me see|send me)\b/.test(lower))return `I caught the picture in your words. I’ll give it a shape. ${progression}`;
  return progression;
}
function possibleMemory(text){
  if(!profile.memory)return '';
  const match=text.match(/(?:i like|i prefer|call me|i want|i love)\s+(.{3,90})/i);
  return match?match[0].replace(/^./,c=>c.toUpperCase()):'';
}
function showMemoryProposal(text){pendingMemory=text;$('memoryText').textContent=text;$('memoryProposal').hidden=!text;}
function renderMemories(){
  $('memoryCount').textContent=memories.length;$('memoryList').replaceChildren();
  if(!memories.length){const empty=document.createElement('p');empty.className='empty-memory';empty.textContent='Nothing retained.';$('memoryList').append(empty);return;}
  memories.forEach((text,index)=>{const row=document.createElement('div');row.className='memory-item';const copy=document.createElement('p');copy.textContent=text;const remove=document.createElement('button');remove.type='button';remove.textContent='Remove';remove.addEventListener('click',()=>{memories.splice(index,1);renderMemories();});row.append(copy,remove);$('memoryList').append(row);});
}

$('quickStartForm').addEventListener('submit',event=>{
  event.preventDefault();const data=new FormData(event.currentTarget);
  profile={name:data.get('name').trim()||shells[selected].name,patron:data.get('patron').trim(),tone:data.get('tone'),limits:data.get('limits').trim(),memory:data.get('memory')==='on',pictures:data.get('pictures')==='on',shell:selected};
  if(!$('consentCheck').checked)return;
  conversationSession=AnonyConversation.create(profile);
  $('setupScreen').hidden=true;$('chatPanel').hidden=false;
  $('liveName').textContent=profile.name;$('liveTraits').textContent=shells[selected].traits;$('conversationTitle').textContent=profile.name+' is listening.';
  $('livePortrait').innerHTML=AnonyMouse.svg(shells[selected].avatar,'real',selected==='velvet'?'coquettish':'portrait');
  addBubble(profile.name,`Hello, ${profile.patron}. I’m artificial, your boundaries lead, and this tab forgets when it closes. How was your day?`,'mouse');
  $('messageInput').focus();
});

$('composer').addEventListener('submit',event=>{
  event.preventDefault();const input=$('messageInput'),text=input.value.trim();if(!text||remaining<1)return;
  addBubble('YOU',text,'user');input.value='';remaining-=1;$('quotaNumber').textContent=remaining;updateArc();showMemoryProposal(possibleMemory(text));
  const requestsPicture=/\b(picture|photo|image|portrait|show me|let me see|send me)\b/i.test(text);
  if(/no (more )?(pictures|photos|images)|words only/i.test(text))profile.pictures=false;
  if(requestsPicture){profile.pictures=true;pictureCue=text.slice(0,120);}
  setTimeout(()=>{addBubble(profile.name,scriptedReply(text),'mouse');if(profile.pictures&&(requestsPicture||pictureQueued||[2,5,8].includes(sentCount())))addPicture(requestsPicture?'requested in conversation':pictureQueued?'your suggestion':'the evening rhythm');},220);
});

function queuePicture(cue){
  pictureCue=cue.trim();if(!pictureCue)return;profile.pictures=true;pictureQueued=true;$('pictureCue').hidden=true;$('openPictureCue').setAttribute('aria-pressed','false');
  addBubble(profile.name,'Lovely. I’ll let that image arrive naturally with my next reply.','mouse');$('messageInput').focus();
}
$('openPictureCue').addEventListener('click',()=>{const open=$('pictureCue').hidden;$('pictureCue').hidden=!open;$('openPictureCue').setAttribute('aria-pressed',String(open));if(open)$('pictureDetail').focus();});
document.querySelectorAll('[data-cue]').forEach(button=>button.addEventListener('click',()=>queuePicture(button.dataset.cue)));
$('savePictureCue').addEventListener('click',()=>queuePicture($('pictureDetail').value));
$('pictureDetail').addEventListener('keydown',event=>{if(event.key==='Enter'){event.preventDefault();queuePicture(event.currentTarget.value);}});

$('acceptMemory').addEventListener('click',()=>{if(pendingMemory&&!memories.includes(pendingMemory))memories.push(pendingMemory);showMemoryProposal('');renderMemories();});
$('rejectMemory').addEventListener('click',()=>showMemoryProposal(''));
$('openMemory').addEventListener('click',()=>{renderMemories();$('memoryDialog').showModal();});
$('clearMemory').addEventListener('click',()=>{memories=[];renderMemories();});
$('openSettings').addEventListener('click',()=>{$('settingsTone').value=profile.tone;$('settingsLimits').value=profile.limits;$('settingsMemory').checked=profile.memory;$('settingsPictures').checked=profile.pictures;$('settingsDialog').showModal();});
$('saveSettings').addEventListener('click',()=>{profile.tone=$('settingsTone').value;profile.limits=$('settingsLimits').value.trim();profile.memory=$('settingsMemory').checked;profile.pictures=$('settingsPictures').checked;$('settingsDialog').close();});
document.querySelectorAll('[data-close]').forEach(button=>button.addEventListener('click',()=>$(button.dataset.close).close()));
renderMemories();
