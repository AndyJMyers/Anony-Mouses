'use strict';
(function(root){
  const MIN=0, MAX=4, STEP=1;
  const scales=[1/220,1/70,1/15,1,4],names=['Country','Region','County','District','Close'];
  function scaleAtLevel(level){const i=Math.min(3,Math.floor(clamp(level,0,4))),t=clamp(level,0,4)-i;return scales[i]*Math.pow(scales[i+1]/scales[i],t);}

  const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
  function attach(viewport,world){
    let level=3,zoom=1,panX=0,panY=0,turning=false,drag=null,suppressClick=false;
    let atlasSites=[],onSite=null;
    let district='GU2',location={lat:51.24,lon:-.59},example=false,count=0;
    viewport.classList.add('map-zoomable');world.classList.add('map-world');
    viewport.tabIndex=0;
    viewport.setAttribute('role','region');
    if(!viewport.hasAttribute('aria-label'))viewport.setAttribute('aria-label','Illustrative neighbourhood map');
    viewport.setAttribute('aria-description','Start at district level; use the half-dial to zoom out through county, region and country, or in closer. Turn it, use plus or minus, or scroll over the dial. Drag the enlarged map to move around.');
    const dial=document.createElement('div');dial.className='map-zoom-dial';dial.setAttribute('role','group');dial.setAttribute('aria-label','Map zoom controls');
    const ticks=Array.from({length:13},(_,i)=>{const angle=(-90+i*15)*Math.PI/180,inner=i%3===0?69:74;return `<line x1="${100+inner*Math.sin(angle)}" y1="${100-inner*Math.cos(angle)}" x2="${100+80*Math.sin(angle)}" y2="${100-80*Math.cos(angle)}"/>`;}).join('');
    dial.innerHTML='<span class="zoom-caption">EXPLORATION</span><div class="zoom-ring" role="slider" tabindex="0" aria-label="Map zoom" aria-valuemin="0" aria-valuemax="4" aria-valuenow="3"><svg viewBox="0 0 200 110" aria-hidden="true"><path class="zoom-track" d="M20 100 A80 80 0 0 1 180 100" pathLength="100"/><path class="zoom-progress" d="M20 100 A80 80 0 0 1 180 100" pathLength="100"/><g class="zoom-ticks">'+ticks+'</g><path class="zoom-needle" d="M100 99 L100 36"/><circle class="zoom-hub" cx="100" cy="100" r="7"/></svg><span class="zoom-knob" aria-hidden="true"></span></div><button type="button" class="zoom-reset" aria-label="Reset map zoom and position"><strong>District</strong><span>LOCAL</span></button><button type="button" class="zoom-less" aria-label="Zoom out">−</button><button type="button" class="zoom-more" aria-label="Zoom in">+</button>';

    const ns='http://www.w3.org/2000/svg',factor=Math.cos(52*Math.PI/180)*1000;
    function svgNode(tag,attrs,text){const n=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);if(text)n.textContent=text;return n;}
    const geo=document.createElementNS(ns,'svg');geo.classList.add('map-geography');geo.setAttribute('aria-hidden','true');
    for(const country of root.AnonyMapGeography){geo.append(svgNode('path',{d:country.path,class:country.name==='United Kingdom'?'geo-land geo-uk':'geo-land','fill-rule':'evenodd','vector-effect':'non-scaling-stroke'}));}
    const places=[['Scotland',-4.1,57,0,1],['Wales',-3.9,52.2,0,1],['England',-1.7,53,0,1],['Northern Ireland',-6.5,54.7,0,1],['Ireland',-8,53.2,0,1],['France',1.3,49.5,0,1],['Edinburgh',-3.19,55.95,0,1.6],['Manchester',-2.24,53.48,0,1.6],['Birmingham',-1.9,52.49,0,1.8],['London',-.13,51.51,0,2.4],['Bristol',-2.59,51.45,.7,2.1],['Southampton',-1.4,50.91,.7,2.4],['Surrey',-.43,51.18,1.7,2.9],['Hampshire',-1.1,51.08,1.7,2.9],['Berkshire',-1.25,51.62,1.7,2.9],['West Sussex',-.48,50.96,1.7,2.9],['Guildford',-.57,51.24,2,2.99],['Reading',-.97,51.45,1.7,2.9],['Brighton',-.14,50.82,1.7,2.9]];
    const labels=places.map(([name,lon,lat,min,max])=>{const n=svgNode('text',{x:lon*factor,y:-lat*1000,'text-anchor':'middle',class:'geo-label'},name);geo.append(n);return {n,min,max};});
    const caption=document.createElement('div');caption.className='map-scale-caption';caption.setAttribute('aria-live','polite');
    const cluster=document.createElement('button');cluster.type='button';cluster.className='map-cluster';cluster.addEventListener('click',()=>{panX=panY=0;setZoom(3);});
    const credit=document.createElement('span');credit.className='map-geography-credit';credit.textContent='Natural Earth · ';const geoLink=document.createElement('a');geoLink.href='https://www.geonames.org/';geoLink.textContent='GeoNames';credit.append(geoLink,document.createTextNode(' · demo locations'));
    const siteLayer=document.createElement('div');siteLayer.className='map-atlas-sites';viewport.prepend(geo);viewport.append(siteLayer,caption,cluster,credit,dial);
    function geography(){const height=60/zoom,width=height*viewport.clientWidth/Math.max(1,viewport.clientHeight);const centres=[{lon:-3.2,lat:55.3},{lon:location.lon-.8,lat:location.lat+.65},location,location,location];const i=Math.min(3,Math.floor(level)),t=level-i,cx=(centres[i].lon*(1-t)+centres[i+1].lon*t)*factor,cy=-(centres[i].lat*(1-t)+centres[i+1].lat*t)*1000;
      geo.setAttribute('viewBox',`${cx-width/2-panX*height/Math.max(1,viewport.clientHeight)} ${cy-height/2-panY*height/Math.max(1,viewport.clientHeight)} ${width} ${height}`);geo.setAttribute('preserveAspectRatio','none');
      for(const label of labels){label.n.style.display=level>=label.min&&level<=label.max?'':'none';label.n.setAttribute('font-size',String(height/Math.max(1,viewport.clientHeight)*12));}
      cluster.style.left=(50+(location.lon*factor-cx)/width*100+panX/Math.max(1,viewport.clientWidth)*100)+'%';cluster.style.top=(50+(-location.lat*1000-cy)/height*100+panY/Math.max(1,viewport.clientHeight)*100)+'%';
      cluster.textContent=count+' '+(example?'demo profiles':'in '+district)+' ↗';cluster.setAttribute('aria-label','Return to '+district+' district view, '+count+' profiles in the current search');
      cluster.hidden=atlasSites.length>0;
      siteLayer.replaceChildren();
      if(level<3&&atlasSites.length){const cells=new Map(),w=viewport.clientWidth,h=viewport.clientHeight;for(const site of atlasSites){const x=w/2+(site.lon*factor-cx)/width*w+panX,y=h/2+(-site.lat*1000-cy)/height*h+panY;if(x<0||x>w||y<0||y>h)continue;const column=Math.floor(x/78),row=Math.floor(y/52),key=column+','+row;const cell=cells.get(key)||{x:(column+.5)*78,y:(row+.5)*52,count:0,sites:[]};cell.count+=site.count;cell.sites.push(site);cells.set(key,cell);}for(const cell of cells.values()){const b=document.createElement('button');b.type='button';b.className='atlas-cluster profile-demo';b.style.left=cell.x+'px';b.style.top=cell.y+'px';b.textContent=cell.count+' demo';b.setAttribute('aria-label',cell.count+' fictional demo profiles near '+cell.sites[0].place);b.addEventListener('click',()=>{const next=Math.min(3,Math.floor(level)+1);onSite(cell.sites[0]);setZoom(next);});siteLayer.append(b);}}
      caption.textContent=names[Math.round(level)]+' view'+(level<.5?' · United Kingdom':' · '+district)+(example?' · geography example near GU2':'');
    }
    const ring=dial.querySelector('.zoom-ring'),progress=dial.querySelector('.zoom-progress'),knob=dial.querySelector('.zoom-knob'),needle=dial.querySelector('.zoom-needle'),readout=dial.querySelector('strong'),less=dial.querySelector('.zoom-less'),more=dial.querySelector('.zoom-more');
    function bounds(){const limitX=level<3?viewport.clientWidth:viewport.clientWidth*(zoom-1)/2,limitY=level<3?viewport.clientHeight:viewport.clientHeight*(zoom-1)/2;panX=clamp(panX,-limitX,limitX);panY=clamp(panY,-limitY,limitY);}
    function render(){zoom=scaleAtLevel(level);bounds();world.style.transform=`translate(${panX}px,${panY}px) scale(${zoom})`;viewport.style.setProperty('--map-zoom',String(zoom));viewport.classList.toggle('map-enlarged',level!==3);viewport.classList.toggle('map-wide',level<3);const fraction=level/4,angle=(-90+180*fraction)*Math.PI/180;knob.style.left=(100+80*Math.sin(angle))+'px';knob.style.top=(100-80*Math.cos(angle))+'px';progress.style.strokeDasharray=(fraction*100)+' 100';needle.setAttribute('transform','rotate('+(-90+180*fraction)+' 100 100)');ring.setAttribute('aria-valuenow',String(Number(level.toFixed(2))));ring.setAttribute('aria-valuetext',names[Math.round(level)]+' view; '+district+' is the local starting view');readout.textContent=names[Math.round(level)];less.disabled=level<=MIN;more.disabled=level>=MAX;geography();}
    function setZoom(value,point){const next=clamp(value,MIN,MAX);if(point&&next>=3&&level>=3){const x=point.x-viewport.clientWidth/2,y=point.y-viewport.clientHeight/2;panX=x-(x-panX)*scaleAtLevel(next)/zoom;panY=y-(y-panY)*scaleAtLevel(next)/zoom;}else if(next!==level){panX=panY=0;}level=next;render();}
    function position(event){const r=viewport.getBoundingClientRect();return {x:event.clientX-r.left,y:event.clientY-r.top};}
    function turn(event){const r=ring.getBoundingClientRect(),x=event.clientX-r.left-100,y=event.clientY-r.top-100;if(Math.hypot(x,y)<25)return;const angle=Math.atan2(x,-y)*180/Math.PI;setZoom(MIN+(clamp(angle,-90,90)+90)/180*(MAX-MIN));}
    ring.addEventListener('pointerdown',event=>{if(event.button!==0)return;event.preventDefault();event.stopPropagation();turning=true;ring.setPointerCapture(event.pointerId);turn(event);});
    ring.addEventListener('pointermove',event=>{if(turning)turn(event);});
    const stopTurn=()=>{turning=false;};ring.addEventListener('pointerup',stopTurn);ring.addEventListener('pointercancel',stopTurn);
    less.addEventListener('click',()=>setZoom(Math.ceil(level)-STEP));more.addEventListener('click',()=>setZoom(Math.floor(level)+STEP));dial.querySelector('.zoom-reset').addEventListener('click',()=>{panX=panY=0;setZoom(3);});
    function keys(event){if(event.target!==viewport&&event.target!==ring)return;const actions={'+':()=>setZoom(Math.floor(level)+STEP),'=':()=>setZoom(Math.floor(level)+STEP),'-':()=>setZoom(Math.ceil(level)-STEP),ArrowUp:()=>setZoom(Math.floor(level)+STEP),ArrowRight:()=>setZoom(Math.floor(level)+STEP),ArrowDown:()=>setZoom(Math.ceil(level)-STEP),ArrowLeft:()=>setZoom(Math.ceil(level)-STEP),Home:()=>{panX=panY=0;setZoom(3);},End:()=>setZoom(MAX)};if(actions[event.key]){event.preventDefault();actions[event.key]();}}
    viewport.addEventListener('keydown',keys);
    viewport.addEventListener('click',event=>{if(suppressClick){suppressClick=false;event.preventDefault();event.stopPropagation();return;}});
    viewport.addEventListener('wheel',event=>{if(!event.ctrlKey&&!event.target.closest('.map-zoom-dial'))return;event.preventDefault();const p=position(event);setZoom(level-event.deltaY*.003,p);},{passive:false});
    viewport.addEventListener('pointerdown',event=>{if(event.button!==0||event.target.closest('button,a,input,.map-zoom-dial'))return;drag={id:event.pointerId,x:event.clientX,y:event.clientY,panX,panY,moved:false};if(level!==3)viewport.setPointerCapture(event.pointerId);});
    viewport.addEventListener('pointermove',event=>{if(!drag||drag.id!==event.pointerId||level===3)return;const dx=event.clientX-drag.x,dy=event.clientY-drag.y;if(Math.hypot(dx,dy)>5)drag.moved=true;if(drag.moved){panX=drag.panX+dx;panY=drag.panY+dy;viewport.classList.add('is-panning');render();}});
    function stopDrag(event){if(!drag||drag.id!==event.pointerId)return;suppressClick=drag.moved;drag=null;viewport.classList.remove('is-panning');}
    viewport.addEventListener('pointerup',stopDrag);viewport.addEventListener('pointercancel',stopDrag);
    new ResizeObserver(render).observe(viewport);
    render();return {setSites(sites,handler){atlasSites=sites;onSite=handler;geography();},reset(){panX=panY=0;level=3;render();},setCount(value){count=value;geography();},setDistrict(code,centre){district=code;example=!centre;location=centre?{lat:centre.lat,lon:centre.lon}:{lat:51.24,lon:-.59};panX=panY=0;level=3;render();}};
  }
  root.AnonyMapZoom={attach,scaleAtLevel};
  if(typeof module!=='undefined')module.exports={scaleAtLevel};
})(globalThis);
