'use strict';
const $=id=>document.getElementById(id);
const shells={
  velvet:{name:'Velvet',traits:'Warm · poised · exacting',avatar:{fur:'cream',hair:'waves',hairColour:'silver',outfit:'dress',colour:'red',trim:'gold',sparkles:'stars',accessory:'pearls',face:'soft',facialHair:'none'}},
  cipher:{name:'Cipher',traits:'Cool · witty · direct',avatar:{fur:'charcoal',hair:'crop',hairColour:'pink',outfit:'leather',colour:'navy',trim:'gold',sparkles:'none',accessory:'glasses',face:'rugged',facialHair:'none'}},
  moss:{name:'Moss',traits:'Patient · strange · tender',avatar:{fur:'cocoa',hair:'long',hairColour:'auburn',outfit:'knit',colour:'green',trim:'gold',sparkles:'stars',accessory:'none',face:'soft',facialHair:'none'}}
};
let selected='velvet',remaining=100,memories=[],pendingMemory='',memoryOff=false,profile=null;
for(const [key,shell] of Object.entries(shells))$('shell'+key[0].toUpperCase()+key.slice(1)).innerHTML=AnonyMouse.svg(shell.avatar,'real',key==='velvet'?'coquettish':'portrait');
document.querySelectorAll('.shell').forEach(button=>button.addEventListener('click',()=>{
  selected=button.dataset.shell;
  document.querySelectorAll('.shell').forEach(item=>{const active=item===button;item.classList.toggle('active',active);item.setAttribute('aria-checked',String(active));});
  $('companionName').value=shells[selected].name;
}));
for(const [name,id] of [['warmth','warmthOutput'],['direct','directOutput'],['strange','strangeOutput']])document.querySelector(`[name=${name}]`).addEventListener('input',event=>$(id).value=event.target.value);

function addBubble(author,text,kind){const article=document.createElement('article');article.className='bubble '+kind;const label=document.createElement('b');label.textContent=author;const copy=document.createElement('div');copy.textContent=text;article.append(label,copy);$('messages').append(article);$('messages').scrollTop=$('messages').scrollHeight;}
function addPicture(){
  const sources={velvet:'assets/companion-velvet-signal.webp',cipher:'assets/companion-cipher-signal.webp',moss:'assets/bio-cyber-mouse-hero.webp'};
  const figure=document.createElement('figure');figure.className='picture-beat';
  const image=document.createElement('img');image.src=sources[profile.shell];image.alt='A cinematic, fully clothed portrait sent by the synthetic mouse companion';
  const caption=document.createElement('figcaption');caption.textContent=profile.name.toUpperCase()+' / PRIVATE PICTURE BEAT / FICTIONAL';
  figure.append(image,caption);$('messages').append(figure);$('messages').scrollTop=$('messages').scrollHeight;
}
function phaseIndex(){const sent=100-remaining;return sent<=1?0:sent<=4?1:sent<=7?2:3;}
function updateArc(){document.querySelectorAll('#eveningArc span').forEach((item,index)=>item.classList.toggle('active',index===phaseIndex()));}
function scriptedReply(text){
  const lower=text.toLowerCase(),name=profile.name,patron=profile.patron;
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
  event.preventDefault();const data=new FormData(event.currentTarget);profile={name:data.get('name').trim(),patron:data.get('patron').trim(),warmth:Number(data.get('warmth')),direct:Number(data.get('direct')),strange:Number(data.get('strange')),limits:data.get('limits').trim(),memory:data.get('memory')==='on',shell:selected};
  if(!$('adultCheck').checked||!$('artificialCheck').checked)return;
  $('builderPanel').hidden=true;$('chatPanel').hidden=false;$('liveName').textContent=profile.name;$('conversationTitle').textContent=profile.name+' is listening.';$('liveTraits').textContent=shells[selected].traits;$('memoryMode').textContent=profile.memory?'Review first':'Off';$('livePortrait').innerHTML=AnonyMouse.svg(shells[selected].avatar,'real',selected==='velvet'?'coquettish':'portrait');
  addBubble(profile.name,`Channel open. Hello, ${profile.patron}. I am artificial, the boundaries are yours, and this prototype forgets when the tab closes. Where shall we begin?`,'mouse');
  $('messageInput').focus();
});
$('composer').addEventListener('submit',event=>{
  event.preventDefault();const input=$('messageInput'),text=input.value.trim();if(!text||remaining<1)return;addBubble('YOU',text,'user');input.value='';remaining-=1;$('quotaNumber').textContent=remaining;updateArc();showProposal(possibleMemory(text));setTimeout(()=>{addBubble(profile.name,scriptedReply(text),'mouse');if(remaining===98||remaining===94)addPicture();},260);
});
$('acceptMemory').addEventListener('click',()=>{if(pendingMemory&&!memories.includes(pendingMemory))memories.push(pendingMemory);showProposal('');renderMemories();});
$('rejectMemory').addEventListener('click',()=>showProposal(''));
$('openMemory').addEventListener('click',()=>{renderMemories();$('memoryDialog').showModal();});
$('closeMemory').addEventListener('click',()=>$('memoryDialog').close());
$('clearMemory').addEventListener('click',()=>{memories=[];renderMemories();});
$('quietMode').addEventListener('click',event=>{memoryOff=!memoryOff;event.currentTarget.setAttribute('aria-pressed',String(memoryOff));event.currentTarget.textContent=memoryOff?'Memory paused':'Leave no memory';if(memoryOff)showProposal('');});
$('recalibrate').addEventListener('click',()=>{$('chatPanel').hidden=true;$('builderPanel').hidden=false;$('messages').replaceChildren();showProposal('');});
renderMemories();
