const SPN=Object.keys(window.SPELLS||{}).filter(k=>SPELLS[k].u).sort((a,b)=>b.length-a.length);
const SPRX=new RegExp("(?<![\\w'])("+SPN.map(n=>n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+")(?![\\w'])","g");
function spLink(n){const v=SPELLS[n];return `<a class="sp" href="${v.u}" target="_blank" rel="noopener"><img class="ic" src="icons/spells/${v.i}.jpg" alt="">${n}</a>`}
function linkHTML(h){return h.split(/(<[^>]+>)/).map(p=>p.startsWith('<')?p:p.replace(SPRX,m=>spLink(m))).join('')}
const S={get:(k,d)=>{try{return JSON.parse(localStorage.getItem('gm:'+k))??d}catch(e){return d}},set:(k,v)=>localStorage.setItem('gm:'+k,JSON.stringify(v))};
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function showTab(){const id=(location.hash||'#start').slice(1);const t=$('#t-'+id)?id:'start';
 $$('.tab').forEach(x=>x.classList.toggle('on',x.id==='t-'+t));$$('.tabs a').forEach(a=>a.classList.toggle('on',a.hash==='#'+t));window.scrollTo(0,0)}
addEventListener('hashchange',showTab);showTab();
const sel=$('#lvSel');for(let i=1;i<=90;i++)sel.add(new Option(i,i));
// ---- rotation (levels from Warcraft Wiki ability table / Wowhead leveling priority)
function rotFor(l){
 if(l<10)return `<b>Levels 1-9 (before the Brewmaster abilities)</b><ol><li>Jab to build Chi</li>${l>=3?'<li>Tiger Palm to spend Chi</li>':''}${l>=7?'<li>Blackout Kick to spend Chi</li>':''}${l>=5?'<li>Roll to move around quickly</li>':''}</ol><span class="note">Mobs are trivial here; this is the basic loop only.</span>`;
 const L=[];
 if(l>=45)L.push('Expel Harm any time Desperate Measures is active (under 35% health)');
 if(l>=34)L.push('Blackout Kick if Shuffle is missing (keep it up, at least every 6 s)');
 if(l>=22)L.push('Touch of Death on an elite or big quest enemy you can finish (3 Chi)');
 if(l>=36)L.push('Elusive Brew (off the global) at 13+ stacks');
 L.push('Keg Smash on cooldown, mostly when you have 2 or less Chi');
 if(l>=26)L.push('Expel Harm on cooldown if not at full health (builds Chi)');
 if(l<34)L.push('Blackout Kick on a single target to spend Chi');
 else L.push('Blackout Kick to maintain Shuffle');
 if(l>=18&&l<34)L.push('Breath of Fire on 3+ enemies');
 if(l>=30)L.push('Chi Wave on cooldown');
 if(l>=46)L.push('Spinning Crane Kick on 3+ enemies');
 L.push(l>=34?'Jab at 70+ Energy (skip it if it would overcap Chi)':'Jab at 70+ Energy or when you need Chi');
 L.push(l>=34?'Tiger Palm as the filler':'Tiger Palm as the filler (costs 1 Chi until 34)');
 let ex=[];
 if(l>=26)ex.push('Guard (2 Chi, off the global) when you expect damage; cast Tiger Palm first for a stronger shield');
 if(l>=75)ex.push('Purifying Brew (1 Chi) after a big hit; Shuffle matters more');
 if(l>=24)ex.push('Fortifying Brew before heavy damage');
 return `<b>Level ${l} priority</b> <span class="note">(Stance of the Sturdy Ox)</span><ol>${L.map(x=>`<li>${x}</li>`).join('')}</ol>${ex.length?'<b>Defensives</b><ul>'+ex.map(x=>`<li>${x}</li>`).join('')+'</ul>':''}`;
}
// ---- bars: slot -> [name, minLevel]; 7/7/7
const TOP=[['Provoke',14],["Tiger's Lust",15],['Touch of Death',22],['Fortifying Brew',24],['Guard',26],['Elusive Brew',36],['Purifying Brew',75]];
const BOT=[['Food',1],['Legacy of the Emperor',22],['Zen Pilgrimage',20],['Summon Black Ox Statue',70],['Detox',20],['Hearthstone',1],['Mount',20]];
function MID(l){const tp=l>=34;return [l>=1?(tp?'Tiger Palm':'Jab'):null,l>=3?(tp?'Jab':'Tiger Palm'):null,l>=7?'Blackout Kick':null,l>=11?'Keg Smash':null,l>=5?'Roll':null,l>=26?'Expel Harm':null,l>=30?'Chi Wave':(l>=18?'Breath of Fire':null)]}
function barsAt(l){return{top:TOP.map(([n,m])=>l>=m?n:null),mid:MID(l),bot:BOT.map(([n,m])=>l>=m?n:null)}}
const SH={'Summon Black Ox Statue':'Black Ox Statue','Legacy of the Emperor':'Legacy Emperor','Fortifying Brew':'Fortify Brew','Touch of Death':'Touch of Death',"Tiger's Lust":"Tiger's Lust",'Zen Pilgrimage':'Zen Pilgr.','Purifying Brew':'Purify Brew','Elusive Brew':'Elusive Brew','Blackout Kick':'Blackout Kick','Breath of Fire':'Breath of Fire'};
const TALS=new Set(["Tiger's Lust",'Chi Wave']);
function renderBars(l){
 const b=barsAt(l),p=l>1?barsAt(l-1):{top:[],mid:[],bot:[]};const lab={top:['Top','click · combat cooldowns'],mid:['Middle','keys 1-7 · pressed constantly'],bot:['Bottom','out of combat']};
 const ch=[];
 $('#barLv').textContent='(Lv '+l+')';
 $('#barsBox').innerHTML=['top','mid','bot'].map(r=>`<div class="brow"><div class="blab"><b>${lab[r][0]}</b> ${lab[r][1]}</div><div class="bslots">`+b[r].map((n,i)=>{
  if(!n)return`<div class="bs empty">${r==='mid'?i+1:''}</div>`;
  const nw=p[r][i]!==n;if(nw)ch.push(`${r==='mid'?'Key '+(i+1):lab[r][0]+' '+(i+1)}: ${n}`);
  const v=SPELLS[n]||{};const tag=v.u?'a':'div';
  return`<${tag} class="bs${nw?' new':''}" ${v.u?`href="${v.u}" target="_blank" rel="noopener"`:''} title="${n}">${v.i?`<img src="icons/spells/${v.i}.jpg" alt="">`:''}${r==='mid'?`<i>${i+1}</i>`:''}<span>${SH[n]||n}</span>${nw?'<em>NEW</em>':''}${TALS.has(n)?'':''}</${tag}>`}).join('')+'</div></div>').join('');
 $('#barChange').innerHTML=ch.length?'<b>New this level:</b> '+ch.join(' · ')+(l>=15&&l<30?'<br><span class="tiny">Tiger\'s Lust and Chi Wave are talents: pick them at 15 and 30 (Spec tab).</span>':''):'<b>No bar changes this level.</b>';
}
// ---- level handling
const rows=$$('.row');
function setLv(l){l=Math.max(1,Math.min(90,+l||1));sel.value=l;S.set('lv',l);$('#curLv').textContent=l;
 let cur=null;rows.forEach(r=>{if(+r.dataset.lo<=l&&l<=+r.dataset.hi)cur=r;r.classList.remove('cur')});if(cur)cur.classList.add('cur');
 $('#rotTag').textContent='(Lv '+l+')';$('#rot').innerHTML=linkHTML(rotFor(l));renderBars(l);}
sel.onchange=()=>setLv(sel.value);$('#lvDown').onclick=()=>setLv(+sel.value-1);$('#lvUp').onclick=()=>setLv(+sel.value+1);
$('#rotBtn').onclick=()=>{const r=$('#rot');r.hidden=!r.hidden;$('#rotBtn').setAttribute('aria-expanded',!r.hidden)};
// ---- rows + checks
const done=S.get('done',{});
rows.forEach(r=>{const k=r.querySelector('.chk').dataset.k;if(done[k])r.classList.add('done');
 r.querySelector('.row-head').onclick=e=>{if(e.target.closest('.chk')){done[k]=!done[k];S.set('done',done);r.classList.toggle('done',!!done[k]);return}r.classList.toggle('open')}});
const hd=$('#hideDone');hd.checked=S.get('hide',false);document.body.classList.toggle('hidedone',hd.checked);hd.onchange=()=>{S.set('hide',hd.checked);document.body.classList.toggle('hidedone',hd.checked)};
const cb=S.get('cb',{});$$('input[type=checkbox][data-k]').forEach(i=>{i.checked=!!cb[i.dataset.k];i.onchange=()=>{cb[i.dataset.k]=i.checked;S.set('cb',cb)}});
setLv(S.get('lv',1));
(()=>{const q=new URLSearchParams(location.search);if(q.get('lv'))setLv(+q.get('lv'));if(q.get('rot'))$('#rotBtn').click();if(q.get('open'))rows.forEach(r=>r.classList.add('open'))})();
if('serviceWorker' in navigator){navigator.serviceWorker.register('sw.js',{updateViaCache:'none'}).then(r=>r.update());let rl=0;navigator.serviceWorker.addEventListener('controllerchange',()=>{if(!rl){rl=1;location.reload()}})}
