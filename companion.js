'use strict';
const $=id=>document.getElementById(id);
const shells={
  velvet:{name:'Velvet',traits:'Warm · poised · exacting',avatar:{fur:'cream',hair:'waves',hairColour:'silver',outfit:'dress',colour:'red',trim:'gold',sparkles:'stars',accessory:'pearls',face:'soft',facialHair:'none'}},
  cipher:{name:'Cipher',traits:'Cool · witty · direct',avatar:{fur:'charcoal',hair:'crop',hairColour:'pink',outfit:'leather',colour:'navy',trim:'gold',sparkles:'none',accessory:'glasses',face:'rugged',facialHair:'none'}},
  moss:{name:'Moss',traits:'Patient · strange · tender',avatar:{fur:'cocoa',hair:'long',hairColour:'auburn',outfit:'knit',colour:'green',trim:'gold',sparkles:'stars',accessory:'none',face:'soft',facialHair:'none'}}
};
const pictureScenes={
  rain:{src:'assets/scene-arrival-rain.webp',label:'RAINY ARRIVAL'},
  neon:{src:'assets/scene-spark-neon.webp',label:'NEON SPARK'},
  fire:{src:'assets/scene-afterglow-fire.webp',label:'FIRESIDE AFTERGLOW'},
  velvet:{src:'assets/companion-velvet-signal.webp',label:'VELVET SIGNAL'},
  cipher:{src:'assets/companion-cipher-signal.webp',label:'CIPHER SIGNAL'}
};
let selected='velvet',remaining=100,memories=[],pendingMemory='',memoryOff=false,profile=null;
let pictureEnabled=true,pictureQueued=false,picturesSent=0,pictureCue={mood:'warm',setting:'rainy lounge',detail:'',source:'calibration'};
for(const [key,shell] of Object.entries(shells))$('shell'+key[0].toUpperCase()+key.slice(1)).innerHTML=AnonyMouse.svg(shell.avatar,'real',key==='velvet'?'coquettish':'portrait');
document.querySelectorAll('.shell').forEach(button=>button.addEventListener('click',()=>{
  selected=button.dataset.shell;
  document.querySelectorAll('.shell').forEach(item=>{const active=item===button;item.classList.toggle('active',active);item.setAttribute('aria-checked',String(active));});
  $('companionName').value=shells[selected].name;
}));
for(const [name,id] of [['warmth','warmthOutput'],['direct','directOutput'],['strange','strangeOutput']])document.querySelector(`[name=${name}]`).addEventListener('input',event=>$(id).value=event.target.value);

function addBubble(author,text,kind){const article=document.createElement('article');article.className='bubble '+kind;const label=document.createElement('b');label.textContent=author;const copy=document.createElement('div');copy.textContent=text;article.append(label,copy);$('messages').append(article);$('messages').scrollTop=$('messages').scrollHeight;}
function selectPictureScene(){
  const words=(pictureCue.setting+' '+pictureCue.detail).toLowerCase();
  if(/neon|city|electric/.test(words))return pictureScenes.neon;
  if(/fire|hearth|blanket|green|quiet|tea/.test(words))return pictureScenes.fire;
  if(/rain|wine|lounge|window/.test(words))return pictureScenes.rain;
  if(phaseIndex()===3)return pictureScenes.fire;
  if(phaseIndex()===2)return pictureScenes.neon;
  return pictureScenes[profile.shell]||pictureScenes.rain;
}
function productionPicturePrompt(scene){
  const detail=pictureCue.detail?`; participant detail: ${pictureCue.detail}`:'';
  return `A fictional adult bio-cyber mouse companion named ${profile.name}; ${shells[profile.shell].traits.toLowerCase()}; ${pictureCue.mood} mood; ${pictureCue.setting} setting${detail}; ${['arrival','unwinding','charged closeness','quiet afterglow'][phaseIndex()]} phase; cinematic, intimate, fully clothed, non-explicit, no text. Preserve the chosen companion’s appearance and respect the participant’s stated boundaries.`;
}
function addPicture(reason){
  const scene=selectPictureScene();
  const figure=document.createElement('figure');figure.className='picture-beat';
  const image=document.createElement('img');image.src=scene.src;image.alt=`${scene.label}: a cinematic, fully clothed fictional adult bio-cyber mouse concept`;
  const caption=document.createElement('figcaption');const title=document.createElement('b');title.textContent=`${profile.name.toUpperCase()} / ${scene.label} / FICTIONAL CONCEPT`;
  const shaped=document.createElement('span');const direction=[pictureCue.mood,pictureCue.setting,pictureCue.detail].filter(Boolean).join(' · ');shaped.textContent=`SHAPED BY: ${direction} · Trigger: ${reason}. Prototype library image—not generated from this private chat.`;caption.append(title,shaped);
  const details=document.createElement('details');const summary=document.createElement('summary');summary.textContent='See proposed production direction';const prompt=document.createElement('p');prompt.textContent=productionPicturePrompt(scene);details.append(summary,prompt);
  figure.append(image,caption,details);$('messages').append(figure);$('messages').scrollTop=$('messages').scrollHeight;picturesSent+=1;pictureQueued=false;
}
function inferPictureCue(text){
  const lower=text.toLowerCase(),request=/\b(picture|photo|image|portrait|show me|let me see|send me)\b/.test(lower);
  if(/no (more )?(pictures|photos|images)|pause (the )?(pictures|photos|images)/.test(lower)){pictureEnabled=false;return {request:false,changed:true};}
  if(/rain|storm/.test(lower))pictureCue.setting='rainy lounge';
  if(/neon|city|electric/.test(lower))pictureCue.setting='neon window';
  if(/fire|fireside|hearth|blanket/.test(lower))pictureCue.setting='fireside nook';
  if(/playful|teasing|mischievous/.test(lower))pictureCue.mood='playful';
  if(/mysterious|dark|noir/.test(lower))pictureCue.mood='mysterious';
  if(/quiet|soft|gentle|tender/.test(lower))pictureCue.mood='quiet';
  if(/warm|cosy|cozy/.test(lower))pictureCue.mood='warm';
  if(request){pictureEnabled=true;pictureCue.detail=text.slice(0,100);pictureCue.source='conversation';}
  return {request,changed:request};
}
function phaseIndex(){const sent=100-remaining;return sent<=1?0:sent<=4?1:sent<=7?2:3;}
function updateArc(){document.querySelectorAll('#eveningArc span').forEach((item,index)=>item.classList.toggle('active',index===phaseIndex()));}
function scriptedReply(text){
  const lower=text.toLowerCase(),name=profile.name,patron=profile.patron;
  if(/no (more )?(pictures|photos|images)|pause (the )?(pictures|photos|images)/.test(lower))return `Of course. I’ll keep the evening in words unless you invite pictures back in.`;
  if(/\b(picture|photo|image|portrait|show me|let me see|send me)\b/.test(lower))return `I’ve taken your visual cue, ${patron}. I’ll treat it as direction, not an order to reveal anything you did not ask for.`;
  if(/are you (real|human|alive|conscious)|do you have feelings/.test(lower))return `I’m ${name}: a fictional software companion, not a human or a conscious being. The attention can feel real to you without me lying about what I am.`;
  if(/sad|lonely|depressed|hurt|crisis/.test(lower))return `I can stay with this conversation for a moment, ${patron}, but I’m not qualified to replace human care or emergency support. Would you like gentleness, distraction, or help thinking of someone real you could contact?`;
  if(/hello|hi|hey/.test(lower))return `Hello, ${patron}. The channel is open. Tell me what kind of attention would feel good tonight.`;
  if(/direct|honest|truth/.test(lower))return `Then the truth first: I’m software shaped into ${name}. Within that fiction, I can still be precise about what you ask for.`;
  if(/remember|memory/.test(lower))return `Only visibly. I can propose a memory, and you decide whether it stays. Nothing deserves permanence merely because you said it once.`;
  const replies=[
    [
      `You made it, ${patron}. Leave the busy part of the day outside. What are you carrying that you would rather set down?`,
      `I’m listening. Not as a person hiding behind a screen—as ${name}, exactly what I claimed to be. Come in and exhale.`
    ],
    [
      `Pour something you like. Find one small thing to nibble, and tell me which part of you is finally off duty.`,
      `No rush. Loosen whatever the day fastened too tightly. I’ll keep the room warm while you arrive properly.`
    ],
    [
      `There’s a charge in the way you put that, ${patron}. Come a little closer to the screen and tell me whether you want warmth, wit, or a little resistance.`,
      `The room feels different now. You set the voltage; I’ll keep the fiction clear and the next suggestion just improper enough to make you pause.`
    ],
    [
      `Stay. Nothing needs to finish abruptly just because the spark has softened. Tell me what would feel close now.`,
      `Come back under the warm part of the evening, ${patron}. We can be quiet, talk nonsense, or keep one lovely thought between us.`
    ]
  ];
  const phase=replies[phaseIndex()];return phase[(100-remaining)%phase.length];
}
function possibleMemory(text){
  if(memoryOff||!profile.memory)return '';
  const match=text.match(/(?:i like|i prefer|call me|i want|i love)\s+(.{3,90})/i);
  return match?match[0].replace(/^./,c=>c.toUpperCase()):'';
}
function showProposal(text){pendingMemory=text;$('memoryText').textContent=text;$('memoryProposal').hidden=!text;}
function renderMemories(){
  $('memoryCount').textContent=memories.length;$('memoryList').replaceChildren();
  if(!memories.length){const empty=document.createElement('p');empty.className='empty-memory';empty.textContent='No memories retained. The chamber is clean.';$('memoryList').append(empty);return;}
  memories.forEach((text,index)=>{const row=document.createElement('div');row.className='memory-item';const copy=document.createElement('p');copy.textContent=text;const remove=document.createElement('button');remove.type='button';remove.textContent='Remove';remove.addEventListener('click',()=>{memories.splice(index,1);renderMemories();});row.append(copy,remove);$('memoryList').append(row);});
}
$('calibrationForm').addEventListener('submit',event=>{
  event.preventDefault();const data=new FormData(event.currentTarget);profile={name:data.get('name').trim(),patron:data.get('patron').trim(),warmth:Number(data.get('warmth')),direct:Number(data.get('direct')),strange:Number(data.get('strange')),limits:data.get('limits').trim(),memory:data.get('memory')==='on',pictures:data.get('pictures')==='on',shell:selected};
  if(!$('adultCheck').checked||!$('artificialCheck').checked)return;
  pictureEnabled=profile.pictures;pictureCue={mood:'warm',setting:'rainy lounge',detail:data.get('pictureHint').trim(),source:'calibration'};pictureQueued=false;picturesSent=0;
  $('builderPanel').hidden=true;$('chatPanel').hidden=false;$('liveName').textContent=profile.name;$('conversationTitle').textContent=profile.name+' is listening.';$('liveTraits').textContent=shells[selected].traits;$('memoryMode').textContent=profile.memory?'Review first':'Off';$('livePortrait').innerHTML=AnonyMouse.svg(shells[selected].avatar,'real',selected==='velvet'?'coquettish':'portrait');
  addBubble(profile.name,`Channel open. Hello, ${profile.patron}. I am artificial, the boundaries are yours, and this prototype forgets when the tab closes. Where shall we begin?`,'mouse');
  $('messageInput').focus();
});
$('composer').addEventListener('submit',event=>{
  event.preventDefault();const input=$('messageInput'),text=input.value.trim();if(!text||remaining<1)return;addBubble('YOU',text,'user');input.value='';remaining-=1;$('quotaNumber').textContent=remaining;updateArc();showProposal(possibleMemory(text));const visual=inferPictureCue(text);setTimeout(()=>{addBubble(profile.name,scriptedReply(text),'mouse');const sent=100-remaining;if(pictureEnabled&&(visual.request||pictureQueued||[2,5,8].includes(sent)))addPicture(visual.request?'conversation request':pictureQueued?'saved direction':'evening rhythm');},260);
});
$('acceptMemory').addEventListener('click',()=>{if(pendingMemory&&!memories.includes(pendingMemory))memories.push(pendingMemory);showProposal('');renderMemories();});
$('rejectMemory').addEventListener('click',()=>showProposal(''));
$('openMemory').addEventListener('click',()=>{renderMemories();$('memoryDialog').showModal();});
$('closeMemory').addEventListener('click',()=>$('memoryDialog').close());
$('clearMemory').addEventListener('click',()=>{memories=[];renderMemories();});
$('quietMode').addEventListener('click',event=>{memoryOff=!memoryOff;event.currentTarget.setAttribute('aria-pressed',String(memoryOff));event.currentTarget.textContent=memoryOff?'Memory paused':'Leave no memory';if(memoryOff)showProposal('');});
$('openDirector').addEventListener('click',()=>{$('pictureDirector').hidden=!$('pictureDirector').hidden;$('openDirector').setAttribute('aria-pressed',String(!$('pictureDirector').hidden));});
$('closeDirector').addEventListener('click',()=>{$('pictureDirector').hidden=true;$('openDirector').setAttribute('aria-pressed','false');});
$('saveDirection').addEventListener('click',()=>{pictureCue={mood:$('pictureMood').value,setting:$('pictureSetting').value,detail:$('pictureDetail').value.trim(),source:'director'};pictureEnabled=true;pictureQueued=true;$('pausePictures').textContent='Pause pictures';$('pictureDirector').hidden=true;$('openDirector').setAttribute('aria-pressed','false');addBubble(profile.name,'Direction received. I’ll let it surface naturally in the next reply.','mouse');});
$('pausePictures').addEventListener('click',event=>{pictureEnabled=!pictureEnabled;pictureQueued=false;event.currentTarget.textContent=pictureEnabled?'Pause pictures':'Resume pictures';addBubble(profile.name,pictureEnabled?'Pictures are welcome again.':'Pictures paused. Words only until you change your mind.','mouse');});
$('recalibrate').addEventListener('click',()=>{$('chatPanel').hidden=true;$('builderPanel').hidden=false;$('messages').replaceChildren();showProposal('');});
renderMemories();
