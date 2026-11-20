'use strict';

/* Provider-neutral browser adapter. Production points this at a same-origin
   server gateway; provider credentials must never be shipped to the browser. */
(function(){
  function endpoint(){return document.querySelector('meta[name="anony-ai-endpoint"]')?.content.trim()||'';}
  async function reply({profile,session,transcript,memories}){
    const url=endpoint();if(!url)return null;
    const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),15000);
    try{
      const response=await fetch(url,{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},signal:controller.signal,body:JSON.stringify({
        protocol:'anony-companion-v1',
        companion:{name:profile.name,shell:profile.shell,tone:profile.tone,limits:profile.limits},
        context:{turn:session.turn,facts:session.facts,moments:session.moments.slice(-8),approvedMemories:memories.slice(-12)},
        messages:transcript.slice(-20)
      })});
      if(!response.ok)return null;const data=await response.json();
      return typeof data.text==='string'&&data.text.trim()?{text:data.text.trim(),pictureCue:data.pictureCue||''}:null;
    }catch{return null;}finally{clearTimeout(timeout);}
  }
  window.AnonyAI={reply,configured:()=>Boolean(endpoint())};
})();
