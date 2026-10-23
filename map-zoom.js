'use strict';
(function(root){
  const MIN=1, MAX=4, STEP=.25;
  const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
  function attach(viewport,world){
    let zoom=1,panX=0,panY=0,turning=false,drag=null,suppressClick=false;
    viewport.classList.add('map-zoomable');world.classList.add('map-world');
    viewport.tabIndex=0;
    viewport.setAttribute('role','region');
    if(!viewport.hasAttribute('aria-label'))viewport.setAttribute('aria-label','Illustrative neighbourhood map');
    viewport.setAttribute('aria-description','Use the permanent half-dial to zoom. Turn it, use plus or minus, or scroll over the dial. Drag the enlarged map to move around.');
    const dial=document.createElement('div');dial.className='map-zoom-dial';dial.setAttribute('role','group');dial.setAttribute('aria-label','Map zoom controls');
    const ticks=Array.from({length:13},(_,i)=>{const angle=(-90+i*15)*Math.PI/180,inner=i%3===0?69:74;return `<line x1="${100+inner*Math.sin(angle)}" y1="${100-inner*Math.cos(angle)}" x2="${100+80*Math.sin(angle)}" y2="${100-80*Math.cos(angle)}"/>`;}).join('');
    dial.innerHTML='<span class="zoom-caption">MAGNIFICATION</span><div class="zoom-ring" role="slider" tabindex="0" aria-label="Map zoom" aria-valuemin="100" aria-valuemax="400" aria-valuenow="100"><svg viewBox="0 0 200 110" aria-hidden="true"><path class="zoom-track" d="M20 100 A80 80 0 0 1 180 100" pathLength="100"/><path class="zoom-progress" d="M20 100 A80 80 0 0 1 180 100" pathLength="100"/><g class="zoom-ticks">'+ticks+'</g><path class="zoom-needle" d="M100 99 L100 36"/><circle class="zoom-hub" cx="100" cy="100" r="7"/></svg><span class="zoom-knob" aria-hidden="true"></span></div><button type="button" class="zoom-reset" aria-label="Reset map zoom and position"><strong>1×</strong><span>RESET</span></button><button type="button" class="zoom-less" aria-label="Zoom out">−</button><button type="button" class="zoom-more" aria-label="Zoom in">+</button>';

    viewport.append(dial);
    const ring=dial.querySelector('.zoom-ring'),progress=dial.querySelector('.zoom-progress'),knob=dial.querySelector('.zoom-knob'),needle=dial.querySelector('.zoom-needle'),readout=dial.querySelector('strong'),less=dial.querySelector('.zoom-less'),more=dial.querySelector('.zoom-more');
    function bounds(){panX=clamp(panX,-viewport.clientWidth*(zoom-1)/2,viewport.clientWidth*(zoom-1)/2);panY=clamp(panY,-viewport.clientHeight*(zoom-1)/2,viewport.clientHeight*(zoom-1)/2);}
    function render(){bounds();world.style.transform=`translate(${panX}px,${panY}px) scale(${zoom})`;viewport.style.setProperty('--map-zoom',String(zoom));viewport.classList.toggle('map-enlarged',zoom>1);const fraction=(zoom-MIN)/(MAX-MIN),angle=(-90+180*fraction)*Math.PI/180;knob.style.left=(100+80*Math.sin(angle))+'px';knob.style.top=(100-80*Math.cos(angle))+'px';progress.style.strokeDasharray=(fraction*100)+' 100';needle.setAttribute('transform','rotate('+(-90+180*fraction)+' 100 100)');ring.setAttribute('aria-valuenow',String(Math.round(zoom*100)));ring.setAttribute('aria-valuetext',zoom.toFixed(2)+' times');readout.textContent=Number(zoom.toFixed(2))+'×';less.disabled=zoom<=MIN;more.disabled=zoom>=MAX;}
    function setZoom(value,point){const next=clamp(value,MIN,MAX);if(point){const x=point.x-viewport.clientWidth/2,y=point.y-viewport.clientHeight/2;panX=x-(x-panX)*next/zoom;panY=y-(y-panY)*next/zoom;}zoom=next;render();}
    function position(event){const r=viewport.getBoundingClientRect();return {x:event.clientX-r.left,y:event.clientY-r.top};}
    function turn(event){const r=ring.getBoundingClientRect(),x=event.clientX-r.left-100,y=event.clientY-r.top-100;if(Math.hypot(x,y)<25)return;const angle=Math.atan2(x,-y)*180/Math.PI;setZoom(MIN+(clamp(angle,-90,90)+90)/180*(MAX-MIN));}
    ring.addEventListener('pointerdown',event=>{if(event.button!==0)return;event.preventDefault();event.stopPropagation();turning=true;ring.setPointerCapture(event.pointerId);turn(event);});
    ring.addEventListener('pointermove',event=>{if(turning)turn(event);});
    const stopTurn=()=>{turning=false;};ring.addEventListener('pointerup',stopTurn);ring.addEventListener('pointercancel',stopTurn);
    less.addEventListener('click',()=>setZoom(zoom-STEP));more.addEventListener('click',()=>setZoom(zoom+STEP));dial.querySelector('.zoom-reset').addEventListener('click',()=>{panX=panY=0;setZoom(1);});
    function keys(event){if(event.target!==viewport&&event.target!==ring)return;const actions={'+':()=>setZoom(zoom+STEP),'=':()=>setZoom(zoom+STEP),'-':()=>setZoom(zoom-STEP),ArrowUp:()=>setZoom(zoom+STEP),ArrowRight:()=>setZoom(zoom+STEP),ArrowDown:()=>setZoom(zoom-STEP),ArrowLeft:()=>setZoom(zoom-STEP),Home:()=>{panX=panY=0;setZoom(1);},End:()=>setZoom(MAX)};if(actions[event.key]){event.preventDefault();actions[event.key]();}}
    viewport.addEventListener('keydown',keys);
    viewport.addEventListener('click',event=>{if(suppressClick){suppressClick=false;event.preventDefault();event.stopPropagation();return;}});
    viewport.addEventListener('wheel',event=>{if(!event.ctrlKey&&!event.target.closest('.map-zoom-dial'))return;event.preventDefault();const p=position(event);setZoom(zoom-event.deltaY*.003,p);},{passive:false});
    viewport.addEventListener('pointerdown',event=>{if(event.button!==0||event.target.closest('button,a,input,.map-zoom-dial'))return;drag={id:event.pointerId,x:event.clientX,y:event.clientY,panX,panY,moved:false};if(zoom>1)viewport.setPointerCapture(event.pointerId);});
    viewport.addEventListener('pointermove',event=>{if(!drag||drag.id!==event.pointerId||zoom<=1)return;const dx=event.clientX-drag.x,dy=event.clientY-drag.y;if(Math.hypot(dx,dy)>5)drag.moved=true;if(drag.moved){panX=drag.panX+dx;panY=drag.panY+dy;viewport.classList.add('is-panning');render();}});
    function stopDrag(event){if(!drag||drag.id!==event.pointerId)return;suppressClick=drag.moved;drag=null;viewport.classList.remove('is-panning');}
    viewport.addEventListener('pointerup',stopDrag);viewport.addEventListener('pointercancel',stopDrag);
    new ResizeObserver(render).observe(viewport);
    render();return {reset(){panX=panY=0;zoom=1;render();}};
  }
  root.AnonyMapZoom={attach};
})(globalThis);
