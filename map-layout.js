'use strict';
(function(root){
  const clamp=(n,a,b)=>Math.min(b,Math.max(a,n));
  function seed(text){let n=2166136261;for(const c of text)n=Math.imul(n^c.charCodeAt(0),16777619);return n>>>0;}
  function random(text){let n=seed(text)||1;return ()=>{n^=n<<13;n^=n>>>17;n^=n<<5;return (n>>>0)/4294967296;};}
  function local(profiles,centre,width,height){
    const w=Math.max(280,width),h=Math.max(280,height),placed=[];
    // Geographic district centres suggest loose neighbourhoods. All offsets are decorative.
    for(const p of [...profiles].sort((a,b)=>a.id.localeCompare(b.id))){
      const rng=random(p.id+':'+centre.lat+':'+centre.lon),site=p.site||p.district_centre||centre;
      const east=(site.lon-centre.lon)*69*Math.cos(centre.lat*Math.PI/180),north=(site.lat-centre.lat)*69;
      const anchorX=.5+Math.tanh(east/9)*.29,anchorY=.47-Math.tanh(north/9)*.27;
      let best,score=-Infinity;
      for(let trial=0;trial<48;trial++){
        const x=clamp((anchorX+(rng()+rng()+rng()-1.5)*.32)*w,55,w-55);
        const y=clamp((anchorY+(rng()+rng()+rng()-1.5)*.29)*h,78,h-58);
        // Reserve space for the permanent dial and district label, rather than hiding people.
        const dial=x>w-245&&y>h-185,label=x<175&&y<95;
        const gap=placed.length?Math.min(...placed.map(q=>Math.hypot((x-q.x)/1.22,y-q.y))):120;
        const candidate=Math.min(gap,110)-(dial?220:0)-(label?160:0)-trial*.035;
        if(candidate>score){score=candidate;best={id:p.id,x,y};}
        if(gap>83&&!dial&&!label)break;
      }
      placed.push(best);
    }
    return new Map(placed.map(p=>[p.id,{x:p.x/w*100,y:p.y/h*100}]));
  }
  function clusters(points,radius=52){
    // Spatial buckets accelerate neighbour lookup only; badges use true weighted centroids.
    const buckets=new Map(),visited=new Set(),groups=[];
    for(const p of points){const key=Math.floor(p.x/radius)+','+Math.floor(p.y/radius);if(!buckets.has(key))buckets.set(key,[]);buckets.get(key).push(p);}
    const ordered=[...points].sort((a,b)=>b.site.count-a.site.count||seed(a.site.code)-seed(b.site.code)||a.site.code.localeCompare(b.site.code));
    for(const point of ordered){if(visited.has(point.site.code))continue;const members=[];const col=Math.floor(point.x/radius),row=Math.floor(point.y/radius);
      for(let dx=-1;dx<=1;dx++)for(let dy=-1;dy<=1;dy++)for(const p of buckets.get((col+dx)+','+(row+dy))||[]){if(!visited.has(p.site.code)&&Math.hypot(p.x-point.x,p.y-point.y)<=radius){visited.add(p.site.code);members.push(p);}}
      const count=members.reduce((n,p)=>n+p.site.count,0),x=members.reduce((n,p)=>n+p.x*p.site.count,0)/count,y=members.reduce((n,p)=>n+p.y*p.site.count,0)/count;
      groups.push({x,y,count,sites:members.map(p=>p.site),diameter:clamp(32+Math.log2(count+1)*3,42,65)});
    }
    // Separate only overlapping badges, with small bounded offsets from their true centroids.
    for(const g of groups){g.anchorX=g.x;g.anchorY=g.y;}
    for(let pass=0;pass<8;pass++)for(let i=0;i<groups.length;i++)for(let j=i+1;j<groups.length;j++){
      const a=groups[i],b=groups[j],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy),min=(a.diameter+b.diameter)/2+3;
      if(d>=min)continue;const angle=d>.01?Math.atan2(dy,dx):(seed(a.sites[0].code)%628)/100,push=(min-d)*.28;
      a.x=clamp(a.x-Math.cos(angle)*push,a.anchorX-18,a.anchorX+18);a.y=clamp(a.y-Math.sin(angle)*push,a.anchorY-18,a.anchorY+18);
      b.x=clamp(b.x+Math.cos(angle)*push,b.anchorX-18,b.anchorX+18);b.y=clamp(b.y+Math.sin(angle)*push,b.anchorY-18,b.anchorY+18);
    }
    return groups;
  }
  root.AnonyMapLayout={local,clusters};if(typeof module!=='undefined')module.exports={local,clusters};
})(globalThis);
