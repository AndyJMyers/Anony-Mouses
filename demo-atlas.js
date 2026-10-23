'use strict';
(function(root){
  const sites=[...AnonyDemoAtlasData.districts,...AnonyDemoAtlasData.extraAreas].map(([code,place,lat,lon])=>({code,place,lat,lon,kind:'demo'}));
  const lookup=new Map(sites.map(s=>[s.code,s]));let originals=[];
  const men=['Silver Fox','Racer','Copper','Woodsman','Dapper','Bruiser','Professor','Rocker','Old School'];
  const women=['Velvet','Rouge','Midnight','Wildflower','Pearl','Rosie','Goldie','Bookish','Emerald'];
  const stories=[
    ['A table for two, perhaps?','I cook a very good supper, collect terrible jokes and know when to leave my phone in my pocket.','A grown-up spark: a drink, a little flirtation, and another meeting if we both want one.','afternoon'],
    ['A wicked smile, good manners','I dress for the occasion and laugh more easily than my photograph would suggest—if I were showing one.','Warm company, honest intentions and the delicious possibility of a mutual attraction.','night'],
    ['The long way home','Walking boots by the door, records by the sofa. I like a conversation that takes an unexpected turn.','A country walk, a cosy pub and a slow kiss only if the feeling is mutual.','slow'],
    ['Just one more record','Jazz after dark, strong coffee in the morning, and an unreasonable fondness for old bookshops.','Wit, warmth and a little chemistry. No grand promises; let us enjoy finding out.','night'],
    ['An afternoon worth stealing','I make time for galleries, long lunches and people who can make me forget to check the clock.','An unhurried drink with an independent adult who is clear about what they want.','afternoon'],
    ['A spark beneath the tweed','Practical hands, a curious mind and a soft spot for a mischievous invitation. Happy outdoors, happier with good company.','A discreet introduction, some laughter and the freedom to decide together what happens next.','slow'],
    ['Dress up. Stay curious.','A little perfume, a well-cut jacket, a favourite cocktail. I enjoy the anticipation as much as the evening.','A playful equal: attraction, good conversation and boundaries we can talk about comfortably.','night'],
    ['Sea air and a little mischief','I take my walks and my coffee seriously. Most other things benefit from a sense of humour.','Fresh air, warm company and an honest flirtation between adults. A hello is a fine beginning.','afternoon'],
    ['An excellent excuse to meet','I read widely, cook enthusiastically and believe that an afternoon can improve with the right person across the table.','Somebody kind and experienced enough to know that chemistry cannot be promised—but can be explored.','slow']
  ];
  function hash(s){let n=0;for(const c of s)n=(n*31+c.charCodeAt(0))>>>0;return n;}
  function distance(a,b){const r=Math.PI/180,dlat=(a.lat-b.lat)*r,dlon=(a.lon-b.lon)*r,v=Math.sin(dlat/2)**2+Math.cos(a.lat*r)*Math.cos(b.lat*r)*Math.sin(dlon/2)**2;return 3958.7613*2*Math.asin(Math.min(1,Math.sqrt(v)));}
  function person(site,index){const n=hash(site.code),style=(index?women:men)[n%9],story=stories[(n+index*4)%stories.length],config=AnonyMouse.presets.find(([name])=>name===style)[1];return {id:'demo-'+site.code+'-'+index,name:style,age:['30s','40s','50s','60s'][(n+index)%4],hint:story[0],bio:story[1],wants:story[2],tags:['Fictional adult','No real meeting available'],moods:[story[3]],reply:'This is a scripted demo reply from a fictional character. In the real service, the other adult would choose whether and how to reply.',avatar:AnonyMouse.normalise({...config,trim:n%4===0?'gold':'none',sparkles:n%5===0?'stars':'none'}),site,kind:'demo'};}
  function sitePeople(site){return [person(site,0),person(site,1),...originals.filter(p=>p.site.code===site.code)];}
  function matches(p,mood){return mood==='all'||p.moods.includes(mood);}
  root.AnonyDemoAtlas={sites,lookup,distance,registerOriginals(list){originals=list;},nearby(centre,mood='all'){const found=[];for(const site of sites){const d=distance(centre,site);if(d<=30)for(const p of sitePeople(site))if(matches(p,mood))found.push({...p,distanceMiles:d});}return found.sort((a,b)=>a.distanceMiles-b.distanceMiles||a.id.localeCompare(b.id)).slice(0,12);},mapSites(mood='all'){return sites.map(site=>({...site,count:sitePeople(site).filter(p=>matches(p,mood)).length})).filter(s=>s.count);},coverage:AnonyDemoAtlasData.coverage};
})(globalThis);
