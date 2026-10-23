'use strict';
(()=>{
const dial=document.getElementById('dial'), needle=document.getElementById('needle'), exposure=document.getElementById('exposure');
const buttons=[...document.querySelectorAll('[data-blend]')]; let value=50,dragging=false;
dial.setAttribute('aria-describedby','dialHelp');
const ticks=document.getElementById('ticks'),ns='http://www.w3.org/2000/svg';
for(let i=0;i<=30;i++){const angle=(-135+i*9)*Math.PI/180,line=document.createElementNS(ns,'line'),outer=117,inner=i%5===0?102:110;for(const [k,v]of Object.entries({x1:150+Math.sin(angle)*inner,y1:150-Math.cos(angle)*inner,x2:150+Math.sin(angle)*outer,y2:150-Math.cos(angle)*outer,stroke:i%5===0?'#e2c88b':'#8d805c','stroke-width':i%5===0?2:1}))line.setAttribute(k,v);ticks.append(line);}
function setBlend(next){value=Math.max(0,Math.min(100,Math.round(next)));exposure.style.setProperty('--mix',value/100);needle.style.transform=`rotate(${-135+value*2.7}deg)`;dial.setAttribute('aria-valuenow',String(value));dial.setAttribute('aria-valuetext',`${100-value} percent lagoon, ${value} percent woodland`);document.getElementById('balance').textContent=`${100-value} / ${value}`;document.getElementById('blendName').textContent=value===0?'Cool water':value===100?'Warm sparks':value===50?'A little of both':value<50?'A little more lagoon':'A little more woodland';exposure.setAttribute('aria-label',value===0?'A woman seated beside a Tahitian lagoon.':value===100?'A man splitting wood with a cyber-lit axe in an autumn woodland.':`Double exposure: ${100-value} percent woman beside a lagoon, ${value} percent man splitting wood in an autumn woodland.`);buttons.forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.blend)===value)));}
function point(e){const r=dial.getBoundingClientRect(),dx=e.clientX-r.left-r.width/2,dy=e.clientY-r.top-r.height/2;if(Math.hypot(dx,dy)<r.width*.12)return;const angle=Math.atan2(dx,-dy)*180/Math.PI;setBlend((Math.max(-135,Math.min(135,angle))+135)/2.7);}
dial.addEventListener('pointerdown',e=>{if(e.button!==0)return;dragging=true;dial.focus();dial.setPointerCapture(e.pointerId);point(e);});dial.addEventListener('pointermove',e=>{if(dragging)point(e);});for(const type of ['pointerup','pointercancel','lostpointercapture'])dial.addEventListener(type,()=>{dragging=false;});
dial.addEventListener('keydown',e=>{const change={ArrowRight:1,ArrowUp:1,ArrowLeft:-1,ArrowDown:-1,PageUp:10,PageDown:-10};if(e.key in change){e.preventDefault();setBlend(value+change[e.key]*(e.shiftKey?5:1));}else if(e.key==='Home'||e.key==='End'){e.preventDefault();setBlend(e.key==='Home'?0:100);}});
dial.addEventListener('wheel',e=>{if(!e.deltaY)return;e.preventDefault();setBlend(value+(e.deltaY>0?-2:2));},{passive:false});buttons.forEach(b=>b.addEventListener('click',()=>setBlend(Number(b.dataset.blend))));
for(const img of document.querySelectorAll('.portrait'))img.addEventListener('error',()=>{document.querySelector('.image-note').textContent='An artwork could not load. Please reload to try again.';});
const compose=document.getElementById('composeScene'),atmosphere=document.getElementById('atmosphere'),title=document.getElementById('moodTitle');
const moods={
 'sub-male':{heading:'Softly <em>does it.</em>',intro:'Rose light. An unhurried rhythm. Room to relax.',status:'Submissive man · light pink · 18-second pulse.'},
 'dom-female':{heading:'Set your <em>own pace.</em>',intro:'Deep blue. A steady presence. A little electric confidence.',status:'Dominant woman · blue · 14-second pulse.'},
 'trad-fem':{heading:'A little <em>warmth.</em>',intro:'Peach, cream and rose. Soft edges and a gentle glow.',status:'Traditional femininity · warm pastels · 22-second glow.'}
};
const reduced=matchMedia('(prefers-reduced-motion: reduce)');let paused=false;
function updateMotion(){document.body.classList.toggle('glow-paused',paused);const b=document.getElementById('pauseGlow');b.setAttribute('aria-pressed',String(paused));b.textContent=reduced.matches?'Reduced motion · still glow':paused?'Resume glow':'Pause glow';b.disabled=reduced.matches;}
reduced.addEventListener('change',updateMotion);
document.getElementById('setScene').addEventListener('click',()=>{compose.hidden=true;atmosphere.hidden=false;document.body.classList.add('scene-chosen');document.querySelector('.controls').setAttribute('aria-labelledby','moodTitle');title.focus();});
document.getElementById('editBlend').addEventListener('click',()=>{compose.hidden=false;atmosphere.hidden=true;document.body.classList.remove('scene-chosen');document.querySelector('.controls').setAttribute('aria-labelledby','title');dial.focus();});
for(const b of document.querySelectorAll('[data-mood]'))b.addEventListener('click',()=>{const key=b.dataset.mood,m=moods[key];document.body.dataset.mood=key;title.innerHTML=m.heading;document.getElementById('moodIntro').textContent=m.intro;document.getElementById('moodStatus').textContent=m.status;document.getElementById('pauseGlow').hidden=false;for(const other of document.querySelectorAll('[data-mood]'))other.setAttribute('aria-pressed',String(other===b));updateMotion();});
document.getElementById('pauseGlow').addEventListener('click',()=>{paused=!paused;updateMotion();});
setBlend(50);
})();
