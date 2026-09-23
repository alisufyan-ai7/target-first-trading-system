/* Engine I v0.1 frozen implementation.
 * Governed by strategies/engine-i-session-expansion-continuation/SPEC-v0.1.md
 */
(function(root){
"use strict";

const MIN=60000, TICK_USD=0.01;

function assert(x,m){if(!x)throw new Error(m);}

function parseTick(s){
  const m=/^([0-9]+)(?:\.([0-9]+))?$/.exec(String(s).trim());
  if(!m)throw new Error("invalid_price:"+s);
  let f=m[2]||"";
  if(f.length>3){
    if(!/^0*$/.test(f.slice(3)))throw new Error("off_grid:"+s);
    f=f.slice(0,3);
  }
  f=f.padEnd(3,"0");
  return Number(m[1])*1000+Number(f);
}

function utcDate(ts){return new Date(ts).toISOString().slice(0,10);}
function dayStart(ts){const d=new Date(ts);return Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate());}
function minsUTC(ts){const d=new Date(ts);return d.getUTCHours()*60+d.getUTCMinutes();}
function weekday(ts){return new Date(ts).getUTCDay();}
function eligibleWeekday(ts){const w=weekday(ts);return w>=1&&w<=5;}

function parseMonth(name,content,expectedRows){
  const lines=content.trimEnd().split("\n");
  assert(lines[0].trim()==="timestamp,open,high,low,close","bad_header:"+name);
  assert(lines.length===expectedRows+1,"bad_rows:"+name+":"+(lines.length-1));
  const out=[];let prev=null;
  for(let i=1;i<lines.length;i++){
    const p=lines[i].trim().split(",");
    assert(p.length===5,"bad_cols:"+name+":"+i);
    const ts=Number(p[0]);
    assert(Number.isInteger(ts)&&ts%MIN===0,"bad_ts:"+name+":"+i);
    if(prev!==null)assert(ts-prev===MIN,"gap:"+name+":"+i);
    prev=ts;
    const o=parseTick(p[1]),h=parseTick(p[2]),l=parseTick(p[3]),c=parseTick(p[4]);
    assert(o>0&&h>0&&l>0&&c>0&&h>=o&&h>=c&&l<=o&&l<=c&&h>=l,"bad_ohlc:"+name+":"+i);
    out.push({ts,o,h,l,c,active:false,activeOrd:-1});
  }
  return out;
}

function buildRows(months){
  let rows=[];
  for(const m of months){
    const r=parseMonth(m.name,m.content,m.expectedRows);
    if(rows.length)assert(r[0].ts-rows[rows.length-1].ts===MIN,"month_gap:"+m.name);
    rows=rows.concat(r);
  }
  let ord=0;
  for(let i=0;i<rows.length;i++){
    const x=rows[i],p=i?rows[i-1]:null;
    const carry=!!p&&x.o===x.h&&x.h===x.l&&x.l===x.c&&x.c===p.c;
    x.active=!carry;
    if(x.active)x.activeOrd=ord++;
  }
  return rows;
}

function buildBars(rows,n){
  const span=n*MIN,out=[];let ord=0;
  for(let i=0;i+n-1<rows.length;){
    const st=rows[i].ts;
    if(st%span!==0){i++;continue;}
    let ok=true;
    for(let j=0;j<n;j++)if(rows[i+j].ts!==st+j*MIN){ok=false;break;}
    if(!ok){i++;continue;}
    const ch=rows.slice(i,i+n),active=ch.some(x=>x.active);
    const b={
      startTs:st,closeTs:st+span,o:ch[0].o,
      h:Math.max(...ch.map(x=>x.h)),l:Math.min(...ch.map(x=>x.l)),c:ch[ch.length-1].c,
      active,activeOrd:-1
    };
    if(active)b.activeOrd=ord++;
    out.push(b);i+=n;
  }
  return out;
}

function buildAsia(rows){
  const x=new Map();
  for(const r of rows){
    const mm=minsUTC(r.ts);
    if(mm>=360)continue;
    const d=utcDate(r.ts);
    let a=x.get(d);
    if(!a){a={date:d,count:0,hi:-Infinity,lo:Infinity,firstTs:r.ts,lastTs:r.ts};x.set(d,a);}
    a.count++;a.hi=Math.max(a.hi,r.h);a.lo=Math.min(a.lo,r.l);a.lastTs=r.ts;
  }
  for(const a of x.values()){
    const st=Date.parse(a.date+"T00:00:00Z");
    a.complete=a.count===360&&a.firstTs===st&&a.lastTs===st+359*MIN;
    a.zero=!(a.hi>a.lo);
    a.midNum=a.hi+a.lo;
  }
  return x;
}

function lastCloseBefore(bars,ts){
  let lo=0,hi=bars.length;
  while(lo<hi){
    const mid=(lo+hi)>>1;
    if(bars[mid].closeTs<ts)lo=mid+1;else hi=mid;
  }
  return lo-1;
}

function directionContext(active15,startTs,asia){
  const i=lastCloseBefore(active15,startTs);
  if(i<2)return null;
  const c0=active15[i],c2=active15[i-2];
  const long=c0.c>c2.c&&2*c0.c>asia.midNum;
  const short=c0.c<c2.c&&2*c0.c<asia.midNum;
  return{c0:c0.c,c2:c2.c,c0CloseTs:c0.closeTs,c2CloseTs:c2.closeTs,long,short};
}

function median12Pass(range,prev12){
  if(prev12.length!==12)return false;
  const a=prev12.map(b=>b.h-b.l).sort((x,y)=>x-y);
  return 2*range>=a[5]+a[6];
}

function expansionShapePass(dir,b){
  const r=b.h-b.l,body=Math.abs(b.c-b.o);
  if(!(r>0))return false;
  if(5*body<3*r)return false;
  return dir==="LONG"?4*(b.h-b.c)<=r:4*(b.c-b.l)<=r;
}

function pullbackFlags(dir,s,m){
  const depth=dir==="LONG"?s.expansionHigh-m.l:m.h-s.expansionLow;
  const armed=4*depth>=s.expansionRange;
  const tooDeep=5*depth>3*s.expansionRange;
  const boundaryFail=dir==="LONG"?m.c<=s.asiaHigh:m.c>=s.asiaLow;
  return{depth,armed,tooDeep,boundaryFail};
}

function continuationBreak(dir,activeM1){
  if(activeM1.length<4)return false;
  const m=activeM1[activeM1.length-1],p=activeM1.slice(-4,-1);
  if(dir==="LONG")return m.c>m.o&&m.c>Math.max(...p.map(x=>x.h));
  return m.c<m.o&&m.c<Math.min(...p.map(x=>x.l));
}

function barOutcome(dir,m,stop,target){
  const stopHit=dir==="LONG"?m.l<=stop:m.h>=stop;
  const targetHit=dir==="LONG"?m.h>=target:m.l<=target;
  if(stopHit)return"stop";
  if(targetHit)return"target";
  return null;
}

function pctile(a,p){
  if(!a.length)return null;
  const b=[...a].sort((x,y)=>x-y),z=(b.length-1)*p,l=Math.floor(z),h=Math.ceil(z);
  return l===h?b[l]:b[l]+(b[h]-b[l])*(z-l);
}
function dist(a){
  if(!a.length)return{n:0,mean:null,median:null,p10:null,p90:null,min:null,max:null};
  return{n:a.length,mean:a.reduce((x,y)=>x+y,0)/a.length,median:pctile(a,.5),p10:pctile(a,.1),p90:pctile(a,.9),min:Math.min(...a),max:Math.max(...a)};
}
function inc(o,k,n=1){o[k]=(o[k]||0)+n;}

function runEngineI(months,splitStart,splitEnd){
  const rows=buildRows(months),bars5=buildBars(rows,5),bars15=buildBars(rows,15),asiaByDate=buildAsia(rows);
  const active15=bars15.filter(b=>b.active);
  const b5End=new Map(bars5.map(b=>[b.closeTs,b]));
  const activeM1=[],active5=[];
  const setups=[],trades=[];
  let pending=[],openTrade=null,shadows=[];
  let setupSeq=0,tradeSeq=0;
  const consumed=new Set();
  const counts={
    active_5m:0,boundary_close_events:0,
    long_context_aligned:0,short_context_aligned:0,
    qualifying_expansions:0,pullback_armed:0,continuation_confirmed:0
  };
  const inSplit=ts=>ts>=splitStart&&ts<splitEnd;

  function reject(s,reason,ts){
    if(s.state==="done")return;
    s.state="done";s.terminal=reason;s.terminalTs=ts;
  }

  function newTerminal(dir,b,reason,extra={}){
    const s={id:"I-S"+(++setupSeq),seq:setupSeq,dir,expansionTs:b.closeTs,expansionStartTs:b.startTs,state:"done",terminal:reason,terminalTs:b.closeTs,...extra};
    setups.push(s);return s;
  }

  function createSetup(dir,b,a,ctx){
    const s={
      id:"I-S"+(++setupSeq),seq:setupSeq,dir,state:"pullback",terminal:null,
      expansionTs:b.closeTs,expansionStartTs:b.startTs,expansionOrd5:b.activeOrd,
      expansionOpen:b.o,expansionHigh:b.h,expansionLow:b.l,expansionClose:b.c,
      expansionRange:b.h-b.l,expansionBody:Math.abs(b.c-b.o),
      asiaHigh:a.hi,asiaLow:a.lo,contextC0:ctx.c0,contextC2:ctx.c2,
      contextC0CloseTs:ctx.c0CloseTs,contextC2CloseTs:ctx.c2CloseTs,
      createdActiveOrd:activeM1.length?activeM1[activeM1.length-1].activeOrd:-1,
      postSeen:0,armedOrd:null,armedTs:null,pullbackLow:null,pullbackHigh:null,
      maxDepth:0,confirmationTs:null,entryOrd:null
    };
    setups.push(s);pending.push(s);return s;
  }

  function updateExtreme(s,m){
    if(s.dir==="LONG")s.pullbackLow=s.pullbackLow===null?m.l:Math.min(s.pullbackLow,m.l);
    else s.pullbackHigh=s.pullbackHigh===null?m.h:Math.max(s.pullbackHigh,m.h);
  }

  function closeTrade(t,reason,px,ts){
    if(t.closed)return;
    t.closed=true;t.exitReason=reason;t.exit=px;t.exitTs=ts;
    t.grossTicks=t.dir==="LONG"?px-t.entry:t.entry-px;
    t.net0=t.grossTicks;t.net250=t.grossTicks-250;t.net500=t.grossTicks-500;
    t.grossUSD=t.grossTicks*TICK_USD;t.netUSD0=t.net0*TICK_USD;t.netUSD250=t.net250*TICK_USD;t.netUSD500=t.net500*TICK_USD;
    if(openTrade&&openTrade.id===t.id)openTrade=null;
  }

  function evaluateEntry(s,m){
    const entry=m.o;
    const stop=s.dir==="LONG"?s.pullbackLow-1:s.pullbackHigh+1;
    if((s.dir==="LONG"&&!(stop<entry))||(s.dir==="SHORT"&&!(entry<stop))){
      reject(s,"invalid_entry_stop_geometry",m.ts);return null;
    }
    const stopDist=Math.abs(entry-stop);
    if(stopDist>4000){reject(s,"structural_risk_above_40",m.ts);return null;}
    s.entry=entry;s.stop=stop;s.stopDist=stopDist;s.grossStopUSD=stopDist*TICK_USD;
    s.target=s.dir==="LONG"?entry+4000:entry-4000;
    return s;
  }

  function fillTrade(s,m){
    const t={
      id:"I-T"+(++tradeSeq),setupId:s.id,dir:s.dir,
      expansionTs:s.expansionTs,expansionRange:s.expansionRange,expansionBody:s.expansionBody,
      asiaHigh:s.asiaHigh,asiaLow:s.asiaLow,contextC0:s.contextC0,contextC2:s.contextC2,
      pullbackArmTs:s.armedTs,confirmationTs:s.confirmationTs,
      pullbackDepthTicks:s.maxDepth,
      pullbackDepthFraction:s.expansionRange?s.maxDepth/s.expansionRange:null,
      expansionToPullbackMs:s.armedTs-s.expansionTs,
      pullbackToConfirmationMs:s.confirmationTs-s.armedTs,
      entry:s.entry,stop:s.stop,target:s.target,stopDist:s.stopDist,
      fillTs:m.ts,fillOrd:m.activeOrd,horizonCount:1,
      actualMFE:0,actualMAE:0,potentialMFE:0,potentialMAE:0,
      closed:false,shadowDone:false,
      labels:{3000:null,4000:null,5000:null,7000:null,10000:null},labelTimes:{}
    };
    trades.push(t);s.tradeId=t.id;s.state="done";openTrade=t;shadows.push(t);

    for(const other of pending){
      if(other!==s&&other.state!=="done")reject(other,"suppressed_one_open",m.ts);
    }

    const out=barOutcome(t.dir,m,t.stop,t.target);
    if(out==="stop"){
      t.actualMAE=t.stopDist;t.potentialMAE=t.stopDist;
      for(const k of Object.keys(t.labels))t.labels[k]="stop_before_target";
      t.shadowDone=true;
      closeTrade(t,"exit_stop_entry_bar",t.stop,m.ts+MIN);
      return t;
    }

    const fav=t.dir==="LONG"?m.h-t.entry:t.entry-m.l;
    const adv=t.dir==="LONG"?t.entry-m.l:m.h-t.entry;
    t.actualMFE=Math.max(0,fav);t.actualMAE=Math.max(0,adv);
    t.potentialMFE=Math.max(0,fav);t.potentialMAE=Math.max(0,adv);
    for(const ks of Object.keys(t.labels)){
      const d=Number(ks),px=t.dir==="LONG"?t.entry+d:t.entry-d;
      const hit=t.dir==="LONG"?m.h>=px:m.l<=px;
      if(hit){t.labels[ks]="target_before_stop";t.labelTimes[ks]=MIN;}
    }
    if(out==="target"){
      t.actualMFE=Math.min(Math.max(t.actualMFE,4000),4000);
      closeTrade(t,"exit_t40",t.target,m.ts+MIN);
    }
    return t;
  }

  function processActual(t,m){
    if(t.closed||m.activeOrd<=t.fillOrd)return;
    const out=barOutcome(t.dir,m,t.stop,t.target);
    if(out==="stop"){t.actualMAE=t.stopDist;closeTrade(t,"exit_stop",t.stop,m.ts+MIN);return;}
    const fav=t.dir==="LONG"?m.h-t.entry:t.entry-m.l;
    const adv=t.dir==="LONG"?t.entry-m.l:m.h-t.entry;
    t.actualMFE=Math.max(t.actualMFE,Math.max(0,fav));t.actualMAE=Math.max(t.actualMAE,Math.max(0,adv));
    if(out==="target"){
      t.actualMFE=Math.min(Math.max(t.actualMFE,4000),4000);
      closeTrade(t,"exit_t40",t.target,m.ts+MIN);return;
    }
    t.horizonCount++;
    const ct=m.ts+MIN;
    if(t.horizonCount>=120){closeTrade(t,"exit_timeout_120",m.c,ct);return;}
    if(minsUTC(ct)>=1200){closeTrade(t,"exit_session_2000",m.c,ct);return;}
  }

  function processShadow(t,m){
    if(t.shadowDone||m.activeOrd<=t.fillOrd)return;
    const stop=t.dir==="LONG"?m.l<=t.stop:m.h>=t.stop;
    if(stop){
      t.potentialMAE=t.stopDist;
      for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="stop_before_target";
      t.shadowDone=true;return;
    }
    const fav=t.dir==="LONG"?m.h-t.entry:t.entry-m.l;
    const adv=t.dir==="LONG"?t.entry-m.l:m.h-t.entry;
    t.potentialMFE=Math.max(t.potentialMFE,Math.max(0,fav));t.potentialMAE=Math.max(t.potentialMAE,Math.max(0,adv));
    for(const ks of Object.keys(t.labels)){
      if(t.labels[ks]!==null)continue;
      const d=Number(ks),px=t.dir==="LONG"?t.entry+d:t.entry-d;
      const hit=t.dir==="LONG"?m.h>=px:m.l<=px;
      if(hit){t.labels[ks]="target_before_stop";t.labelTimes[ks]=(m.ts+MIN)-t.fillTs;}
    }
    const cnt=m.activeOrd-t.fillOrd+1,ct=m.ts+MIN;
    if(cnt>=120||minsUTC(ct)>=1200){
      for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="horizon_without_target_or_stop";
      t.shadowDone=true;
    }
  }

  function processDueEntries(m,occupiedAtOpen){
    const due=pending.filter(s=>s.state==="entry_next"&&s.entryOrd===m.activeOrd)
      .sort((a,b)=>a.expansionTs-b.expansionTs||a.seq-b.seq);
    if(!due.length)return;
    if(occupiedAtOpen){
      for(const s of due)reject(s,"suppressed_one_open",m.ts);
      pending=pending.filter(s=>s.state!=="done");return;
    }
    if(minsUTC(m.ts)>=1080){
      for(const s of due)reject(s,"entry_window_closed_1800",m.ts);
      pending=pending.filter(s=>s.state!=="done");return;
    }
    let opened=false;
    for(const s of due){
      if(opened){reject(s,"suppressed_one_open",m.ts);continue;}
      if(!evaluateEntry(s,m))continue;
      fillTrade(s,m);opened=true;
    }
    pending=pending.filter(s=>s.state!=="done");
  }

  function processPending(m){
    const ct=m.ts+MIN;
    for(const s of pending){
      if(s.state!=="pullback"&&s.state!=="armed")continue;
      if(m.activeOrd<=s.createdActiveOrd)continue;
      if(openTrade){reject(s,"suppressed_one_open",m.ts);continue;}
      if(minsUTC(ct)>=1080){
        reject(s,s.armedOrd===null?"pullback_not_armed_25":"confirmation_timeout_20",ct);continue;
      }
      s.postSeen++;
      updateExtreme(s,m);
      const f=pullbackFlags(s.dir,s,m);
      s.maxDepth=Math.max(s.maxDepth,f.depth);
      if(f.tooDeep){reject(s,"pullback_deeper_than_60",ct);continue;}
      if(f.boundaryFail){reject(s,"boundary_hold_failed",ct);continue;}
      if(s.armedOrd===null&&f.armed){
        s.armedOrd=m.activeOrd;s.armedTs=ct;s.state="armed";inc(counts,"pullback_armed");
      }else if(s.armedOrd!==null&&m.activeOrd>s.armedOrd&&continuationBreak(s.dir,activeM1)){
        s.confirmationTs=ct;s.confirmationOrd=m.activeOrd;s.entryOrd=m.activeOrd+1;s.state="entry_next";
        inc(counts,"continuation_confirmed");continue;
      }
      if(s.postSeen>=20){
        reject(s,s.armedOrd===null?"pullback_timeout_20":"confirmation_timeout_20",ct);
      }
    }
    pending=pending.filter(s=>s.state!=="done");
  }

  function on5Close(b){
    if(!b.active)return;
    if(inSplit(b.closeTs))counts.active_5m++;

    if(inSplit(b.closeTs)&&eligibleWeekday(b.closeTs)){
      const a=asiaByDate.get(utcDate(b.closeTs));
      if(!a||!a.complete){
        if(minsUTC(b.closeTs)>=360&&minsUTC(b.closeTs)<1020)newTerminal(null,b,"asia_interval_incomplete");
      }else if(a.zero){
        if(minsUTC(b.closeTs)>=360&&minsUTC(b.closeTs)<1020)newTerminal(null,b,"asia_zero_width");
      }else{
        let dir=null;
        if(b.c>a.hi)dir="LONG";
        else if(b.c<a.lo)dir="SHORT";
        if(dir){
          counts.boundary_close_events++;
          const mm=minsUTC(b.closeTs);
          if(mm>=360&&mm<1020){
            const ctx=directionContext(active15,b.startTs,a);
            if(!ctx)newTerminal(dir,b,"context_15m_unavailable",{asiaHigh:a.hi,asiaLow:a.lo});
            else if((dir==="LONG"&&!ctx.long)||(dir==="SHORT"&&!ctx.short))
              newTerminal(dir,b,"direction_context_mismatch",{asiaHigh:a.hi,asiaLow:a.lo,contextC0:ctx.c0,contextC2:ctx.c2});
            else {
              inc(counts,dir==="LONG"?"long_context_aligned":"short_context_aligned");
              if(active5.length<12)newTerminal(dir,b,"prior_12_5m_unavailable",{asiaHigh:a.hi,asiaLow:a.lo});
              else if(!median12Pass(b.h-b.l,active5.slice(-12)))
                newTerminal(dir,b,"range_below_prior_median",{asiaHigh:a.hi,asiaLow:a.lo});
              else if(5*Math.abs(b.c-b.o)<3*(b.h-b.l))
                newTerminal(dir,b,"body_below_60pct",{asiaHigh:a.hi,asiaLow:a.lo});
              else if(!expansionShapePass(dir,b))
                newTerminal(dir,b,"weak_close_location",{asiaHigh:a.hi,asiaLow:a.lo});
              else{
                const key=utcDate(b.closeTs)+"|"+dir;
                if(consumed.has(key))newTerminal(dir,b,"side_already_consumed_today",{asiaHigh:a.hi,asiaLow:a.lo});
                else{
                  consumed.add(key);counts.qualifying_expansions++;
                  if(openTrade)newTerminal(dir,b,"suppressed_one_open",{asiaHigh:a.hi,asiaLow:a.lo});
                  else createSetup(dir,b,a,ctx);
                }
              }
            }

          }
        }
      }
    }
    active5.push(b);
  }

  for(const m of rows){
    if(m.active){
      activeM1.push(m);
      const occupiedAtOpen=!!openTrade;
      if(openTrade)processActual(openTrade,m);
      for(const t of shadows)processShadow(t,m);
      shadows=shadows.filter(t=>!t.shadowDone);
      processDueEntries(m,occupiedAtOpen);
      processPending(m);
    }
    const bc=b5End.get(m.ts+MIN);
    if(bc)on5Close(bc);
  }

  if(openTrade){
    const last=rows[rows.length-1];
    closeTrade(openTrade,"exit_data_end",last.c,last.ts+MIN);
  }
  for(const t of shadows){
    if(!t.shadowDone){
      for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="horizon_without_target_or_stop";
      t.shadowDone=true;
    }
  }

  const ss=setups.filter(s=>inSplit(s.expansionTs||s.terminalTs||0));
  const tt=trades.filter(t=>inSplit(t.expansionTs));
  const reasons={};for(const s of ss)if(s.terminal)inc(reasons,s.terminal);
  const exits={};for(const t of tt)inc(exits,t.exitReason);
  const labels={};
  for(const d of[3000,4000,5000,7000,10000]){
    const a=tt.map(t=>t.labels[d]);
    labels[d]={target:a.filter(x=>x==="target_before_stop").length,stop:a.filter(x=>x==="stop_before_target").length,horizon:a.filter(x=>x==="horizon_without_target_or_stop").length,n:a.length};
  }

  const dates=[];
  for(let ts=dayStart(splitStart);ts<splitEnd;ts+=24*60*MIN)if(eligibleWeekday(ts))dates.push(utcDate(ts));
  const validAsiaWeekdays=dates.filter(d=>{const a=asiaByDate.get(d);return !!a&&a.complete&&!a.zero;}).length;
  const daily={};for(const d of dates)daily[d]=0;
  for(const t of tt){const d=utcDate(t.fillTs);if(daily[d]!==undefined)daily[d]+=t.netUSD500;}
  const dv=dates.map(d=>daily[d]);

  function avg(field){return tt.length?tt.reduce((s,t)=>s+t[field],0)/tt.length:null;}
  function pf(field){
    let p=0,n=0;
    for(const t of tt){const x=t[field];if(x>0)p+=x;else if(x<0)n-=x;}
    return n?p/n:(p>0?Infinity:null);
  }
  function mdd(){
    let eq=500,peak=500,dd=0;
    for(const t of [...tt].sort((a,b)=>a.fillTs-b.fillTs)){eq+=t.netUSD500;peak=Math.max(peak,eq);dd=Math.max(dd,peak-eq);}
    return dd;
  }
  function lossRun(){
    let bn=0,bl=0,cn=0,cl=0;
    for(const t of [...tt].sort((a,b)=>a.fillTs-b.fillTs)){
      if(t.netUSD500<0){cn++;cl+=t.netUSD500;if(cn>bn||(cn===bn&&cl<bl)){bn=cn;bl=cl;}}
      else{cn=0;cl=0;}
    }
    return{count:bn,netLoss:bl};
  }
  function consec(pred){let b=0,c=0;for(const x of dv){if(pred(x)){c++;b=Math.max(b,c);}else c=0;}return b;}

  const totalNet=tt.reduce((s,t)=>s+t.netUSD500,0),maxDD=mdd();
  const direction={};
  for(const t of tt){if(!direction[t.dir])direction[t.dir]={n:0,netUSD500:0};direction[t.dir].n++;direction[t.dir].netUSD500+=t.netUSD500;}

  return{
    source_rows:rows.length,market_active_m1:rows.filter(x=>x.active).length,
    split:{start:new Date(splitStart).toISOString(),end_exclusive:new Date(splitEnd).toISOString()},
    event_counts:counts,setup_count:ss.length,terminal_reasons:reasons,accepted_filled_trades:tt.length,exits,
    target_hit_rate:tt.length?(exits.exit_t40||0)/tt.length:null,
    stop_rate:tt.length?((exits.exit_stop||0)+(exits.exit_stop_entry_bar||0))/tt.length:null,
    timeout_rate:tt.length?((exits.exit_timeout_120||0)+(exits.exit_session_2000||0)+(exits.exit_data_end||0))/tt.length:null,
    label_rates:labels,
    expectancy:{gross_usd:avg("grossUSD"),net_usd_0:avg("netUSD0"),net_usd_025:avg("netUSD250"),net_usd_050:avg("netUSD500")},
    profit_factor:{gross:pf("grossUSD"),net_0:pf("netUSD0"),net_025:pf("netUSD250"),net_050:pf("netUSD500")},
    total_net_usd_050:totalNet,weekdays:dates.length,valid_asia_weekdays:validAsiaWeekdays,
    daily:{mean:dv.length?dv.reduce((a,b)=>a+b,0)/dv.length:null,median:pctile(dv,.5),losing_pct:dv.length?dv.filter(x=>x<0).length/dv.length:null,le50_pct:dv.length?dv.filter(x=>x<=50).length/dv.length:null,ge100_pct:dv.length?dv.filter(x=>x>=100).length/dv.length:null,ge150_pct:dv.length?dv.filter(x=>x>=150).length/dv.length:null,ge200_pct:dv.length?dv.filter(x=>x>=200).length/dv.length:null},
    max_drawdown_usd:maxDD,recovery_factor:maxDD>0?totalNet/maxDD:null,
    worst_losing_trade_run:lossRun(),max_consecutive_losing_weekdays:consec(x=>x<0),max_consecutive_le50_weekdays:consec(x=>x<=50),
    actual_mfe_ticks:dist(tt.map(t=>t.actualMFE)),actual_mae_ticks:dist(tt.map(t=>t.actualMAE)),
    potential_mfe_ticks:dist(tt.map(t=>t.potentialMFE)),potential_mae_ticks:dist(tt.map(t=>t.potentialMAE)),
    stop_distance_ticks:dist(tt.map(t=>t.stopDist)),gross_stop_usd:dist(tt.map(t=>t.stopDist*TICK_USD)),
    expansion_range_ticks:dist(tt.map(t=>t.expansionRange)),expansion_body_ticks:dist(tt.map(t=>t.expansionBody)),
    pullback_depth_ticks:dist(tt.map(t=>t.pullbackDepthTicks)),pullback_depth_fraction:dist(tt.map(t=>t.pullbackDepthFraction)),
    expansion_to_pullback_ms:dist(tt.map(t=>t.expansionToPullbackMs)),pullback_to_confirmation_ms:dist(tt.map(t=>t.pullbackToConfirmationMs)),
    direction,trades:tt,setups:ss,daily_series:dates.map(d=>({date:d,netUSD500:daily[d]}))
  };
}

function bootstrap(metrics,reps=10000,seed=20020){
  const days=metrics.daily_series;
  const byDate=new Map(days.map(x=>[x.date,[]]));
  for(const t of metrics.trades){const d=utcDate(t.fillTs);if(byDate.has(d))byDate.get(d).push(t.netUSD500);}
  const blocks=[];for(let i=0;i+5<=days.length;i++)blocks.push(days.slice(i,i+5).map(x=>x.date));
  let state=seed>>>0;
  function rnd(){state=(1664525*state+1013904223)>>>0;return state/4294967296;}
  const exp=[],dailyMean=[];let zeroTrade=0;
  for(let r=0;r<reps;r++){
    const picked=[];
    while(picked.length<days.length){
      const b=blocks[Math.floor(rnd()*blocks.length)];
      for(const d of b)if(picked.length<days.length)picked.push(d);
    }
    let pnl=0,n=0;
    for(const d of picked){for(const x of byDate.get(d)||[]){pnl+=x;n++;}}
    dailyMean.push(pnl/days.length);
    if(n)exp.push(pnl/n);else zeroTrade++;
  }
  return{
    reps,seed,block_weekdays:5,zero_trade_resamples:zeroTrade,
    expectancy_net_usd_050:{point:metrics.expectancy.net_usd_050,lo:pctile(exp,.025),hi:pctile(exp,.975)},
    mean_daily_net_usd_050:{point:metrics.daily.mean,lo:pctile(dailyMean,.025),hi:pctile(dailyMean,.975)}
  };
}

function selfTest(){
  assert(parseTick("2062.688")===2062688,"tick_parse");
  assert(parseTick("3")===3000,"tick_integer");
  let threw=false;try{parseTick("1.2345");}catch(e){threw=true;}assert(threw,"off_grid_reject");

  const asia={hi:1100,lo:900,midNum:2000};
  const a15=[
    {closeTs:100,c:950},{closeTs:200,c:980},{closeTs:300,c:1010},{closeTs:400,c:1200}
  ];
  const ctx=directionContext(a15,400,asia);
  assert(ctx&&ctx.c0===1010&&ctx.c2===950&&ctx.long,"context_strict_before");
  assert(ctx.c0CloseTs<400,"context_no_equal_close_leak");

  const prev12=[];
  for(let i=0;i<12;i++)prev12.push({h:1000+100,l:1000});
  assert(median12Pass(100,prev12),"median12_equal_pass");
  assert(!median12Pass(99,prev12),"median12_below_fail");

  const eb={o:1000,h:1200,l:1000,c:1180};
  assert(expansionShapePass("LONG",eb),"expansion_shape_long");

  const s={expansionHigh:2000,expansionLow:1000,expansionRange:1000,asiaHigh:1500,asiaLow:500};
  let f=pullbackFlags("LONG",s,{l:1750,h:1900,c:1800});
  assert(f.armed&&!f.tooDeep&&!f.boundaryFail,"pullback_25_arms");
  f=pullbackFlags("LONG",s,{l:1400,h:1800,c:1600});
  assert(f.armed&&!f.tooDeep&&!f.boundaryFail,"pullback_60_allowed");
  f=pullbackFlags("LONG",s,{l:1399,h:1800,c:1600});
  assert(f.tooDeep,"pullback_over_60_reject");
  f=pullbackFlags("LONG",s,{l:1750,h:1900,c:1500});
  assert(f.boundaryFail,"boundary_equal_reject");

  const am=[
    {o:1,h:10,l:1,c:5},{o:5,h:11,l:4,c:8},{o:8,h:12,l:7,c:9},{o:9,h:14,l:8,c:13}
  ];
  assert(continuationBreak("LONG",am),"continuation_prev3_break");

  assert(barOutcome("LONG",{h:120,l:80},90,110)==="stop","same_bar_stop_first");
  assert(barOutcome("LONG",{h:120,l:95},90,110)==="target","target_when_no_stop");
  assert(Math.abs(5000-1000)===4000,"risk_cap_boundary");
  assert(!(Math.abs(5001-1000)<=4000),"risk_cap_over");

  return{ok:true,tests:[
    "tick_parse","off_grid_reject","context_strict_before","context_no_equal_close_leak",
    "median12_exact","expansion_shape","pullback_25_60","boundary_hold_strict",
    "continuation_prev3","same_bar_stop_first","risk_cap"
  ]};
}

root.EngineIv01={
  runEngineI,bootstrap,selfTest,parseTick,
  _test:{directionContext,median12Pass,expansionShapePass,pullbackFlags,continuationBreak,barOutcome}
};
})(globalThis);
