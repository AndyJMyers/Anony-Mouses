'use strict';

/* One hundred adult, non-graphic conversation directions. The engine chooses
   among them by evening phase; it never sends this catalogue to the patron. */
(function(){
  const groups={
    arrive:[
      ['day','The real day','What part of today would you most like to leave outside?'],
      ['comfortable','Getting comfortable','What is the first thing you do when you are properly off duty?'],
      ['drink','The first drink','What are you drinking—or wishing I had poured for you?'],
      ['nibble','Something to nibble','What little thing would you put between us to share?'],
      ['room','The room tonight','Where have you made yourself comfortable tonight?'],
      ['need','What tonight needs','Do you need soothing, playfulness, or a little charge tonight?'],
      ['hard_day','Setting it down','What was the one moment today that asked too much of you?'],
      ['good_day','Keeping one good thing','What small thing from today deserves to come in with you?'],
      ['ritual','Changing gears','What would make this feel like the evening has really begun?'],
      ['expected','Being expected','How would you like to be welcomed when you arrive here?']
    ],
    chosen:[
      ['why_me','Why this mouse','What made you choose me tonight?'],
      ['address','A name for tonight','What kind of name feels especially good when I say it?'],
      ['noticed','What deserves noticing','What would you like me to notice that other people miss?'],
      ['hidden','The overlooked part','What is quietly wonderful about you?'],
      ['compliment','How praise should land','Do you prefer compliments sincere, cheeky, poetic, or direct?'],
      ['pride','Secret pride','What have you done lately that deserves rather more admiration?'],
      ['attractive','Feeling attractive','When do you feel most attractive in your own skin?'],
      ['wearing','What you chose','What are you wearing that feels most like you tonight?'],
      ['dress_mouse','Dressing the fiction','What would you choose for me to wear in our next picture?'],
      ['mouse_mood','Choosing my mood','Should I be warm, mischievous, poised, or confidently direct?']
    ],
    flirt:[
      ['look','The prolonged look','What would make you hold my gaze instead of looking away?'],
      ['almost','The almost-compliment','Would you rather I told you exactly what I like, or made you guess?'],
      ['closer','A little closer','What changes for you when someone comes just a little closer?'],
      ['charming','Caught being charming','Are you always this charming when nobody is watching?'],
      ['blush','Making each other blush','What kind of attention is most likely to make you blush?'],
      ['three_likes','Three things','Should I admire your mind, your manner, or your dangerous side first?'],
      ['finish','Finish the thought','Finish this for me: tonight I would love to feel…'],
      ['truth_tease','Truth or tease','Would you like one honest observation or one playful tease?'],
      ['one_word','One charged word','What single word should set the mood between us?'],
      ['grin','That particular grin','What usually puts that knowing smile on your face?']
    ],
    dates:[
      ['bar','The quiet bar','At our quiet bar, do we sit opposite each other or close enough to share secrets?'],
      ['dinner','Dinner at home','What are we cooking badly—or ordering beautifully?'],
      ['hotel','Rainy-night hotel','What detail would make an unfamiliar room feel like ours for the night?'],
      ['rooftop','Midnight rooftop','What would you say when the city below us finally went quiet?'],
      ['cabin','Cabin fire','Would our cabin evening be full of talk or comfortable silence?'],
      ['train','Late-night train','Where should the train be taking us?'],
      ['gallery','After-hours gallery','What kind of picture would stop you in your tracks?'],
      ['garden','Summer garden','What would we be eating barefoot in the warm air?'],
      ['nightclub','Cyberpunk nightclub','Would you find me on the dance floor or watching from somewhere darker?'],
      ['kitchen','Sunday kitchen','What is your ideal slow-morning breakfast?']
    ],
    senses:[
      ['lighting','Choosing the light','Candlelight, neon, firelight, or almost dark?'],
      ['music','The soundtrack','What would you put on if you wanted the room to change immediately?'],
      ['temperature','Warm or cool','Would you rather feel cool night air or disappear under something warm?'],
      ['scent','A signature scent','What scent makes somewhere feel instantly intimate to you?'],
      ['texture','The texture game','Velvet, silk, leather, soft knit, or cool metal?'],
      ['kiss','The idea of a kiss','Do you imagine the first kiss as certain, teasing, or unexpectedly gentle?'],
      ['voice','A voice in the room','How do you imagine my voice when I say your name?'],
      ['eyes_closed','Eyes closed','If you closed your eyes, what would you want to notice first?'],
      ['detail','One perfect detail','Which tiny detail makes a whole scene feel real for you?'],
      ['picture_words','A picture in words','What image should I hold in mind for our next picture?']
    ],
    tension:[
      ['wait','A delicious pause','Do you enjoy being made to wait a little, or rewarded for asking?'],
      ['impress','Impress me','What is your most unfairly attractive quality?'],
      ['convince','Convince me','What could you say that would make it very difficult to remain composed?'],
      ['you_first','You first','Would you rather reveal something first or draw it out of me?'],
      ['tiny_dare','A tiny dare','Would you change the music, dim the light, or choose a bolder word?'],
      ['truths_fantasy','Two truths and a fantasy','What harmless fantasy would blend perfectly with two truths about you?'],
      ['guess','Guessing game','What do you hope I am thinking about you right now?'],
      ['caught','Caught looking','What would you do if you caught me looking at you like that?'],
      ['dont_smile','Do not smile','What reliably ruins your attempt to look serious?'],
      ['next_line','Choosing my next move','Should my next thought be tender, witty, or daring?']
    ],
    boundaries:[
      ['bold','Choosing boldness','Should I keep this gentle, make it more suggestive, or be confidently daring?'],
      ['limits','Limits tonight','Is there anything you want kept firmly outside this evening?'],
      ['curious','Curiosity','Is there a kind of closeness you are curious to explore in words?'],
      ['lead_you','Your lead','Would you like to lead this part of the evening?'],
      ['lead_me','My lead','Would you like me to take the conversational lead for a while?'],
      ['slower','Pace','Would slower feel better, or would you like me a little closer?'],
      ['continue','A natural check-in','Keep this mood, or shall I surprise you with a change?'],
      ['pause_word','An easy pause','What simple word should always bring us gently back to neutral?'],
      ['safe','Feeling safe','What makes intimate attention feel safe and easy for you?'],
      ['not_tonight','A graceful no','What would feel better instead tonight?']
    ],
    roles:[
      ['strangers','First meeting','If we were strangers meeting tonight, what would make you approach me?'],
      ['reunion','A fictional reunion','In our fictional reunion, how long has it been since we last met?'],
      ['host','Host and guest','What would make you feel beautifully looked after as my guest?'],
      ['seducer','Seducer and sceptic','Which of us should pretend not to be impressed?'],
      ['muse','Muse and artist','If I made something inspired by you, what form should it take?'],
      ['android_desire','An android learning desire','What human ritual of attraction would you teach an android first?'],
      ['teach_tenderness','Teaching tenderness','What small gesture means tenderness to you?'],
      ['honest_machine','The honest machine','What is attractive about a companion who never pretends to be human?'],
      ['masked','The masked party','What name would you give yourself at a masked midnight party?'],
      ['future','A different future','Where in the future should we spend one impossible evening?']
    ],
    intimacy:[
      ['cared_for','Feeling cared for','What makes you feel cared for without needing many words?'],
      ['missed_closeness','The closeness you miss','What kind of everyday closeness do you wish there were more of?'],
      ['admit','Something difficult','What truth becomes easier to say when nobody is judging?'],
      ['most_yourself','Most yourself','When do you feel most entirely yourself?'],
      ['wish_said','Words you deserve','What do you wish somebody would notice and say aloud?'],
      ['warm_memory','A warm memory','Which memory still makes the room feel warmer when you tell it?'],
      ['romance','Your definition of romance','Is romance domestic, theatrical, cerebral, sensual, funny, or quiet for you?'],
      ['luxury','Luxurious attention','What kind of attention feels genuinely luxurious?'],
      ['silence','A shared silence','Would a little silence between us feel peaceful or charged?'],
      ['who_tonight','Who you are tonight','What part of yourself have you enjoyed being tonight?']
    ],
    afterglow:[
      ['back_close','Coming back close','What would bring you gently back to the warm part of the evening?'],
      ['feeling','How it feels now','Warm, amused, calm, charged, or something else?'],
      ['care','A little care','Water, something to nibble, or a blanket around your shoulders?'],
      ['favourite','The favourite moment','What has been your favourite little moment between us?'],
      ['remember','What should stay','What, if anything, would you like me to remember?'],
      ['forget','What should vanish','Is there anything from tonight you would rather leave here?'],
      ['nonsense','Comfortable nonsense','What ridiculous subject could we happily talk about now?'],
      ['story','A story before sleep','Would you like a romantic, strange, or soothing little story?'],
      ['last_picture','The closing picture','What should the last picture of our evening feel like?'],
      ['goodnight','A good ending','How would you like me to say goodnight when the time comes?']
    ]
  };

  const orderedGroups=['arrive','chosen','flirt','dates','senses','tension','boundaries','roles','intimacy','afterglow'];
  const topics=orderedGroups.flatMap(group=>groups[group].map(([id,title,question])=>({id,group,title,question})));
  const opening=['drink','noticed','lighting','look','bar','bold','cared_for','favourite','goodnight'];

  function clean(value,max=72){return value.replace(/\s+/g,' ').replace(/[<>]/g,'').trim().replace(/[.!?,;:]+$/,'').slice(0,max);}
  function create(profile){return {profile,turn:0,facts:{},moments:[],used:new Set(['day']),lastTopic:'day',lastUserText:'',topics};}
  function saveFact(session,key,text){const value=clean(text);if(value.length>1)session.facts[key]=value;}
  function ingest(session,text){
    const lower=text.toLowerCase();if(session.lastTopic!=='free')saveFact(session,session.lastTopic,text);session.lastUserText=clean(text,110);
    if(/\b(wine|beer|tea|coffee|cocktail|water|whisky|whiskey|gin|juice)\b/.test(lower))saveFact(session,'drink',text);
    if(/sooth|gentle|calm|quiet|comfort/.test(lower))session.facts.need='something gentle';
    if(/play|teas|fun|laugh|mischief/.test(lower))session.facts.need='playfulness';
    if(/charg|bold|daring|flirt|spark/.test(lower))session.facts.need='a little charge';
    if(/rain|neon|fire|candle|dark|music|song/.test(lower))saveFact(session,'atmosphere',text);
    const preference=text.match(/(?:i like|i love|i prefer|my favourite is|my favorite is)\s+(.{3,70})/i);if(preference)saveFact(session,'preference',preference[1]);
    const moment={turn:session.turn,label:session.lastTopic,text:clean(text,80)};session.moments.push(moment);if(session.moments.length>12)session.moments.shift();
  }
  function groupForTurn(turn){if(turn<2)return 'arrive';if(turn<4)return 'chosen';if(turn<6)return 'flirt';if(turn<8)return 'tension';return turn%4===0?'intimacy':turn%4===1?'roles':turn%4===2?'senses':'afterglow';}
  function chooseTopic(session){
    const preferred=opening[session.turn];if(preferred){const topic=topics.find(item=>item.id===preferred);if(topic&&!session.used.has(topic.id))return topic;}
    const group=groupForTurn(session.turn),pool=groups[group].map(([id,title,question])=>({id,group,title,question})).filter(item=>!session.used.has(item.id));
    return pool[session.turn%Math.max(pool.length,1)]||topics.find(item=>!session.used.has(item.id))||topics[0];
  }
  function reflection(session,text){
    const lower=text.toLowerCase(),tone=session.profile.tone;
    if(/terrible|awful|exhaust|stress|hard|rough|bad/.test(lower))return `Then I’m glad you brought that here instead of pretending it was fine.`;
    if(/great|good|wonderful|brilliant|happy|lovely/.test(lower))return `I like hearing that brightness in you.`;
    if(/yes|yeah|exactly|definitely|absolutely/.test(lower))return tone==='playful'?`That certainty is rather attractive.`:`I like how sure you are about that.`;
    if(text.length<18)return tone==='direct'?`Clear. I can work with that.`:`Mmm. That tells me more than you think.`;
    const voices={
      velvet:[`I like the way you put that.`,`There you are. That answer suits you.`,`That lands beautifully.`],
      cipher:[`Good answer. Specific, confident—I like it.`,`Now that is useful information.`,`You make a persuasive case.`],
      moss:[`I can feel that answer changing the room.`,`I’d like to sit with that for a moment.`,`That feels quietly honest.`]
    };
    if(tone==='strange')return `I can feel the shape of that answer changing the room.`;
    if(tone==='playful')return `There you are. I was hoping you’d give me something like that.`;
    return voices[session.profile.shell][session.turn%3];
  }
  function callback(session){
    const facts=session.facts;
    if(session.turn>5&&facts.preference)return `I haven’t forgotten that you prefer ${facts.preference}.`;
    if(session.turn>4&&facts.atmosphere)return `It belongs with the atmosphere you gave us earlier: ${facts.atmosphere}.`;
    if(session.turn>3&&facts.need)return `You asked for ${facts.need}, so I’m keeping us there.`;
    if(session.turn>2&&facts.drink)return `Keep your ${facts.drink.replace(/^(a|an|the|my)\s+/i,'')} close; it has already become part of our little scene.`;
    if(session.turn>1&&facts.day)return `After a day you described as “${facts.day}”, you’ve earned a gentler room.`;
    return '';
  }
  function bridge(topic){
    const bridges={arrive:'Let’s leave the day at the door.',chosen:'I want to know how attention should land on you.',flirt:'Now the air between us can become a little less innocent.',dates:'Let’s give the two of us somewhere to be.',senses:'Let’s make the room more vivid.',tension:'A little anticipation suits us.',boundaries:'You set the pace; that is part of the attraction.',roles:'Let’s borrow another version of ourselves for a moment.',intimacy:'I want to come closer to the person inside the flirtation.',afterglow:'Let’s keep the ending as attentive as the beginning.'};
    return bridges[topic.group];
  }
  function specificReflection(session,text,answered){
    const value=clean(text,80),lower=text.toLowerCase();
    if(/direct.+compliment|compliment.+direct/.test(lower))return `Direct compliments, then. I won’t make you fish for them.`;
    if(/confidence|confident/.test(lower))return `Confidence. Good. You shouldn’t have to make yourself smaller to be approachable.`;
    if(/candle|rain|neon|firelight|almost dark/.test(lower))return `${value}. That’s ours now; I can almost see it reflected in the window.`;
    if(/\b(wine|beer|tea|coffee|cocktail|water|whisky|whiskey|gin|juice)\b/.test(lower))return `${value}. That suits you. I’ll pretend there’s a second glass beside mine.`;
    if(answered==='day'){
      if(/meeting/.test(lower))return `Too many meetings can leave your head buzzing after everybody else has gone. Come here. You can put them down with me.`;
      if(/terrible|awful|exhaust|stress|hard|rough|bad/.test(lower))return `Then no performance tonight. Come here and put the day down with me.`;
      return `I’m glad that is the version of the day you brought through the door.`;
    }
    if(answered==='noticed')return `Good. You shouldn’t have to ask twice to be seen.`;
    if(answered==='look')return `I had a feeling there was a bolder answer hiding underneath.`;
    if(answered==='bar')return `I can see it now; the rest of the room has become pleasantly irrelevant.`;
    if(answered==='bold')return `Thank you for telling me plainly. I’ll keep the pace with you.`;
    if(answered==='cared_for')return `That is worth remembering for this evening.`;
    return reflection(session,text);
  }
  function naturalQuestion(session,topic){
    const tailored={
      drink:'What are you drinking?',
      noticed:'What did you secretly hope I would notice about you tonight?',
      look:'Come a little closer. What would make you hold my gaze?',
      bar:'If we slipped out somewhere together now, where would you take me?',
      bold:'Tell me where the edge of comfortable is tonight.',
      cared_for:'What small thing makes you feel genuinely looked after?',
      favourite:'What little moment between us has felt most like ours?',
      goodnight:'When the time comes, how should I say goodnight to you?'
    };
    if(tailored[topic.id])return tailored[topic.id];
    if(!/\sor\s/i.test(topic.question))return topic.question;
    const open={arrive:'Tell me what would make being here feel easy.',chosen:'Tell me how you like attention to find you.',flirt:'Tell me what kind of flirtation you never quite resist.',dates:'Where should I imagine the two of us now?',senses:'What detail would make this room feel real?',tension:'What would make this moment deliciously difficult to rush?',boundaries:'Tell me what pace feels right.',roles:'Who would you like us to be for a little while?',intimacy:'What kind of closeness feels honest to you?',afterglow:'What would feel good and close now?'};
    return open[topic.group];
  }
  function intimateMove(session,topic){
    const facts=session.facts,name=session.profile.patron;
    const shared=facts.atmosphere?` The ${facts.atmosphere.toLowerCase()} has become ours now.`:'';
    const moves={
      velvet:{arrive:`Stay there a moment, ${name}. I like the point where your shoulders finally drop.`,chosen:`I’m beginning to see the version of you that only appears when the day stops demanding things.`,flirt:`Come a little closer. I like anticipation when it is allowed to take its time.`,dates:`In my head we have moved to the quiet end of the room, where nobody needs us.`,senses:`I would lower the lights now and let the silence do some of the flirting.${shared}`,tension:`You have my full attention. I’m not going to waste it by rushing.`,boundaries:`Nothing has to happen merely because the mood is warm. I like that the pace belongs to us.`,roles:`For a moment, let’s be two strangers who already know they are going to remember the meeting.`,intimacy:`This is the part I like: when the performance falls away and the person remains.`,afterglow:`Stay close. We do not have to turn a lovely moment into another task.`},
      cipher:{arrive:`Good. The outside world can wait; it has had enough of you today.`,chosen:`I’m paying attention, ${name}. Not politely—properly.`,flirt:`That answer changed the voltage in here. I assume you noticed.`,dates:`I’ve moved us somewhere with low light and an excellent view of each other.`,senses:`The room needs less light and fewer excuses.${shared}`,tension:`I could press the moment. I think making it wait is more interesting.`,boundaries:`Clarity is attractive. If the pace changes, you tell me once and I listen.`,roles:`Let’s pretend we met five minutes ago and have already decided to make questionable plans.`,intimacy:`You are more interesting when you stop trying to give the right answer.`,afterglow:`No dramatic exit. Stay and be ordinary with me for a while.`},
      moss:{arrive:`You can be quiet here, ${name}. I don’t need a polished version of you.`,chosen:`There is something lovely in the way you become more yourself by degrees.`,flirt:`The space between us feels warmer now. I’m content to notice it.`,dates:`I imagine somewhere small, rain outside, and nowhere else either of us needs to be.`,senses:`I would keep the room soft enough that every small detail mattered.${shared}`,tension:`We can let the moment hover. Not everything beautiful needs to be hurried into an ending.`,boundaries:`The gentlest thing is knowing we can change direction without losing the closeness.`,roles:`Let’s borrow a different world, but keep the honest parts of ourselves.`,intimacy:`I like this quiet honesty more than any perfect line.`,afterglow:`Stay in the warm part with me. The evening can soften without disappearing.`}
    };
    return moves[session.profile.shell][topic.group];
  }
  function reply(session,text){
    const answered=session.lastTopic;ingest(session,text);const topic=chooseTopic(session);session.used.add(topic.id);
    const shouldAsk=session.turn<2||session.turn%3===0;
    const parts=[specificReflection(session,text,answered)];
    if(session.turn>3&&session.turn%2===0)parts.push(callback(session));
    parts.push(shouldAsk?naturalQuestion(session,topic):intimateMove(session,topic));
    session.lastTopic=shouldAsk?topic.id:'free';session.turn+=1;
    return {text:parts.filter(Boolean).join(' '),topic,callback:parts.length>2};
  }

  window.AnonyConversation={create,reply,topics,count:topics.length};
})();
