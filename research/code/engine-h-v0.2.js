/* Engine H v0.2 frozen implementation.
 * Governed by strategies/engine-h-range-raid-preexisting-fvg-reversal/SPEC-v0.2.md
 */
(function(root){
"use strict";
const MIN=60000, TICK_USD=0.01;
function assert(x,m){if(!x)throw new Error(m);}
function parseTick(s){
  const m=/^([0-9]+)(?:\.([0-9]+))?$/.exec(String(s).trim());
  if(!m)throw new Error("invalid_price:"+s);
  let f=m[2]||"";
  if(f.length>3){if(!/^0*$/.test(f.slice(3)))throw new Error("off_grid:"+s);f=f.slice(0,3);}
  f=f.padEnd(3,"0");
  return Number(m[1])*1000+Number(f);
}
function utcDate(ts){return new Date(ts).toISOString().slice(0,10);}
function dayStart(ts){const d=new Date(ts);return Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate());}
function minsUTC(ts){const d=new Date(ts);return d.getUTCHours()*60+d.getUTCMinutes();}
function weekday(ts){return new Date(ts).getUTCDay();}
function eligibleWeekday(ts){const w=weekday(ts);return w>=1&&w<=5;}
function before1800(closeTs){return minsUTC(closeTs)<1080;}
function parseMonth(name,content,expectedRows){
  const lines=content.trimEnd().split("\n");
  assert(lines[0].trim()==="timestamp,open,high,low,close","bad_header:"+name);
  assert(lines.length===expectedRows+1,"bad_rows:"+name+":"+(lines.length-1));
  const out=[];let prev=null;
  for(let i=1;i<lines.length;i++){
    const p=lines[i].trim().split(","); assert(p.length===5,"bad_cols:"+name+":"+i);
    const ts=Number(p[0]);assert(Number.isInteger(ts)&&ts%MIN===0,"bad_ts:"+name+":"+i);
    if(prev!==null)assert(ts-prev===MIN,"gap:"+name+":"+i);prev=ts;
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
    x.active=!carry;if(x.active)x.activeOrd=ord++;
  }
  return rows;
}
function build5(rows){
  const out=[];let ord=0;
  for(let i=0;i+4<rows.length;){
    const st=rows[i].ts;
    if(st%(5*MIN)!==0){i++;continue;}
    let ok=true;for(let j=0;j<5;j++)if(rows[i+j].ts!==st+j*MIN){ok=false;break;}
    if(!ok){i++;continue;}
    const ch=rows.slice(i,i+5),active=ch.some(x=>x.active);
    const b={startTs:st,closeTs:st+5*MIN,o:ch[0].o,h:Math.max(...ch.map(x=>x.h)),l:Math.min(...ch.map(x=>x.l)),c:ch[4].c,active,activeOrd:-1};
    if(active)b.activeOrd=ord++;
    out.push(b);i+=5;
  }
  return out;
}
function pctile(a,p){if(!a.length)return null;const b=[...a].sort((x,y)=>x-y),z=(b.length-1)*p,l=Math.floor(z),h=Math.ceil(z);return l===h?b[l]:b[l]+(b[h]-b[l])*(z-l);}
function dist(a){if(!a.length)return{n:0,mean:null,median:null,p10:null,p90:null,min:null,max:null};return{n:a.length,mean:a.reduce((x,y)=>x+y,0)/a.length,median:pctile(a,.5),p10:pctile(a,.1),p90:pctile(a,.9),min:Math.min(...a),max:Math.max(...a)};}

function runEngineH(months,splitStart,splitEnd){
  const rows=buildRows(months),bars5=build5(rows);
  const b5Start=new Map(bars5.map(b=>[b.startTs,b])),b5End=new Map(bars5.map(b=>[b.closeTs,b]));
  const activeM1=[],active5=[],pivH=[],pivL=[];
  let fvgSeq=0,setupSeq=0,tradeSeq=0;
  let fvgs=[],pending=[],openTrade=null,shadows=[];
  const setups=[],trades=[];
  const counts={active_5m:0,boundary_breach_bars:0,external_fvg_touch_bars:0,qualifying_raids:0,in_window_raids:0};
  let snapRange=null,snapBear=null,snapBull=null,snapFvgs=[];
  const inSplit=ts=>ts>=splitStart&&ts<splitEnd;
  function inc(o,k,n=1){o[k]=(o[k]||0)+n;}

  function fvgActive(f,currentOrd){
    if(f.mitigated||f.expired)return false;
    const age=currentOrd-f.createOrd;
    if(age>48){f.expired=true;return false;}
    return age>=1;
  }
  function pruneFvgs(currentOrd){fvgs=fvgs.filter(f=>fvgActive(f,currentOrd));}
  function selectLocations(range,currentOrd){
    pruneFvgs(currentOrd);
    const bear=fvgs.filter(f=>f.dir==="BEAR"&&fvgActive(f,currentOrd)&&f.lower>range.hi)
      .sort((a,b)=>(a.lower-range.hi)-(b.lower-range.hi)||b.createOrd-a.createOrd||a.id.localeCompare(b.id))[0]||null;
    const bull=fvgs.filter(f=>f.dir==="BULL"&&fvgActive(f,currentOrd)&&f.upper<range.lo)
      .sort((a,b)=>(range.lo-b.upper)-(range.lo-a.upper)||b.createOrd-a.createOrd||a.id.localeCompare(b.id))[0]||null;
    return{bear,bull};
  }
  function calcRange(){
    if(active5.length<12)return null;
    const w=active5.slice(-12);let hi=-Infinity,lo=Infinity;
    for(const b of w){hi=Math.max(hi,b.h);lo=Math.min(lo,b.l);}
    if(!(hi>lo))return{hi,lo,zero:true};
    return{hi,lo,zero:false};
  }
  function confirmM1(m){
    const n=activeM1.length-1;if(n<4)return;
    const t=n-2,a=activeM1,c=a[t];
    if(c.h>a[t-1].h&&c.h>a[t-2].h&&c.h>=a[t+1].h&&c.h>=a[t+2].h)pivH.push({centerOrd:c.activeOrd,centerTs:c.ts,confirmOrd:m.activeOrd,price:c.h});
    if(c.l<a[t-1].l&&c.l<a[t-2].l&&c.l<=a[t+1].l&&c.l<=a[t+2].l)pivL.push({centerOrd:c.activeOrd,centerTs:c.ts,confirmOrd:m.activeOrd,price:c.l});
  }
  function frozenPivot(dir,sweepStart,currentOrd){
    const arr=dir==="SHORT"?pivL:pivH,minOrd=currentOrd-14;
    for(let i=arr.length-1;i>=0;i--){const p=arr[i];if(p.centerOrd<minOrd)break;if(p.centerTs<sweepStart&&p.confirmOrd<=currentOrd)return p;}
    return null;
  }
  function reject(s,reason,ts){s.state="done";s.terminal=reason;s.terminalTs=ts;}
  function newSetup(dir,b,loc,range,m){
    const seq=++setupSeq;
    const s={id:"H2-S"+seq,seq,dir,sweepTs:b.closeTs,sweepStart:b.startTs,sweepHigh:b.h,sweepLow:b.l,
      rangeHigh:range.hi,rangeLow:range.lo,locationFvgId:loc.id,locationFvgLower:loc.lower,locationFvgUpper:loc.upper,
      locationFvgAge:b.activeOrd-loc.createOrd,locationDistance:dir==="SHORT"?loc.lower-range.hi:range.lo-loc.upper,
      createdOrd:m.activeOrd,state:"mss",mssSeen:0,terminal:null};
    const p=frozenPivot(dir,b.startTs,m.activeOrd);
    if(!p)reject(s,"no_internal_mss_pivot",b.closeTs); else s.pivot=p;
    setups.push(s);if(s.state!=="done")pending.push(s);return s;
  }

  function evaluateEntryAdmission(s,m){
    const entry=m.o;
    const stop=s.dir==="SHORT"?s.sweepHigh+1:s.sweepLow-1;
    const target=s.dir==="SHORT"?s.rangeLow:s.rangeHigh;
    if((s.dir==="SHORT"&&!(target<entry&&entry<stop))||(s.dir==="LONG"&&!(stop<entry&&entry<target))){
      reject(s,"invalid_entry_geometry_at_open",m.ts);return null;
    }
    const stopDist=Math.abs(entry-stop),targetDist=Math.abs(target-entry);
    if(stopDist>4000){reject(s,"structural_risk_above_40",m.ts);return null;}
    if(targetDist<3000){reject(s,"insufficient_target_room_3xau",m.ts);return null;}
    if(targetDist<2*stopDist){reject(s,"reward_risk_below_2",m.ts);return null;}
    s.entry=entry;s.stop=stop;s.target=target;s.stopDist=stopDist;s.targetDist=targetDist;s.grossStopUSD=stopDist*TICK_USD;
    return s;
  }

  function closeTrade(t,reason,px,ts){
    if(t.closed)return;t.closed=true;t.exitReason=reason;t.exit=px;t.exitTs=ts;
    t.grossTicks=t.dir==="LONG"?px-t.entry:t.entry-px;
    t.net0=t.grossTicks;t.net250=t.grossTicks-250;t.net500=t.grossTicks-500;
    t.grossUSD=t.grossTicks*TICK_USD;t.netUSD0=t.net0*TICK_USD;t.netUSD250=t.net250*TICK_USD;t.netUSD500=t.net500*TICK_USD;
    if(openTrade&&openTrade.id===t.id)openTrade=null;
  }
  function fillTradeAtOpen(s,m){
    const t={id:"H2-T"+(++tradeSeq),setupId:s.id,dir:s.dir,entry:s.entry,stop:s.stop,target:s.target,stopDist:s.stopDist,targetDist:s.targetDist,
      fillTs:m.ts,fillOrd:m.activeOrd,horizonCount:1,actualMFE:0,actualMAE:0,potentialMFE:0,potentialMAE:0,closed:false,shadowDone:false,
      labels:{3000:null,4000:null,5000:null,7000:null,10000:null},labelTimes:{},locationFvgAge:s.locationFvgAge,locationDistance:s.locationDistance,sweepTs:s.sweepTs};
    trades.push(t);s.tradeId=t.id;s.state="done";openTrade=t;shadows.push(t);

    const stopHit=t.dir==="LONG"?m.l<=t.stop:m.h>=t.stop;
    const targetHit=t.dir==="LONG"?m.h>=t.target:m.l<=t.target;
    if(stopHit){
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

    if(targetHit){
      t.actualMFE=Math.min(Math.max(t.actualMFE,t.targetDist),t.targetDist);
      closeTrade(t,"exit_target",t.target,m.ts+MIN);
    }
    return t;
  }

  function processActual(t,m){
    if(t.closed||m.activeOrd<=t.fillOrd)return;
    const stop=t.dir==="LONG"?m.l<=t.stop:m.h>=t.stop;
    const target=t.dir==="LONG"?m.h>=t.target:m.l<=t.target;
    if(stop){t.actualMAE=t.stopDist;closeTrade(t,"exit_stop",t.stop,m.ts+MIN);return;}
    const fav=t.dir==="LONG"?m.h-t.entry:t.entry-m.l,adv=t.dir==="LONG"?t.entry-m.l:m.h-t.entry;
    t.actualMFE=Math.max(t.actualMFE,Math.max(0,fav));t.actualMAE=Math.max(t.actualMAE,Math.max(0,adv));
    if(target){t.actualMFE=Math.min(Math.max(t.actualMFE,t.targetDist),t.targetDist);closeTrade(t,"exit_target",t.target,m.ts+MIN);return;}
    t.horizonCount++;const ct=m.ts+MIN;
    if(t.horizonCount>=120){closeTrade(t,"exit_timeout_120",m.c,ct);return;}
    if(minsUTC(ct)>=1200){closeTrade(t,"exit_session_2000",m.c,ct);return;}
  }

  function processShadow(t,m){
    if(t.shadowDone||m.activeOrd<=t.fillOrd)return;
    const stop=t.dir==="LONG"?m.l<=t.stop:m.h>=t.stop;
    if(stop){t.potentialMAE=t.stopDist;for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="stop_before_target";t.shadowDone=true;return;}
    const fav=t.dir==="LONG"?m.h-t.entry:t.entry-m.l,adv=t.dir==="LONG"?t.entry-m.l:m.h-t.entry;
    t.potentialMFE=Math.max(t.potentialMFE,Math.max(0,fav));t.potentialMAE=Math.max(t.potentialMAE,Math.max(0,adv));
    for(const ks of Object.keys(t.labels)){
      if(t.labels[ks]!==null)continue;
      const d=Number(ks),px=t.dir==="LONG"?t.entry+d:t.entry-d;
      const hit=t.dir==="LONG"?m.h>=px:m.l<=px;
      if(hit){t.labels[ks]="target_before_stop";t.labelTimes[ks]=(m.ts+MIN)-t.fillTs;}
    }
    const cnt=m.activeOrd-t.fillOrd+1,ct=m.ts+MIN;
    if(cnt>=120||minsUTC(ct)>=1200){for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="horizon_without_target_or_stop";t.shadowDone=true;}
  }

  function processDueEntriesAtOpen(m,occupiedAtOpen){
    const due=pending.filter(s=>s.state==="entry_next"&&s.entryOrd===m.activeOrd).sort((a,b)=>a.sweepTs-b.sweepTs||a.seq-b.seq);
    if(!due.length)return;
    if(occupiedAtOpen){
      for(const s of due)reject(s,"suppressed_one_open",m.ts);
      pending=pending.filter(s=>s.state!=="done");
      return;
    }
    if(minsUTC(m.ts)>=1080){
      for(const s of due)reject(s,"entry_window_closed_1800",m.ts);
      pending=pending.filter(s=>s.state!=="done");
      return;
    }
    let opened=false;
    for(const s of due){
      if(opened){reject(s,"suppressed_one_open",m.ts);continue;}
      if(!evaluateEntryAdmission(s,m))continue;
      fillTradeAtOpen(s,m);opened=true;
      for(const other of pending){
        if(other!==s&&other.state!=="done")reject(other,"suppressed_one_open",m.ts);
      }
    }
    pending=pending.filter(s=>s.state!=="done");
  }

  function processPendingMss(m){
    for(const s of pending){
      if(s.state!=="mss")continue;
      const ct=m.ts+MIN;if(m.activeOrd<=s.createdOrd)continue;
      if(openTrade){reject(s,"suppressed_one_open",m.ts);continue;}
      if(!before1800(ct)){reject(s,"setup_window_closed_before_mss",ct);continue;}
      s.mssSeen++;
      const hit=s.dir==="SHORT"?m.c<s.pivot.price:m.c>s.pivot.price;
      if(hit){
        s.mssOrd=m.activeOrd;s.mssTs=ct;s.entryOrd=m.activeOrd+1;s.state="entry_next";
      } else if(s.mssSeen>=20) reject(s,"mss_timeout_20",ct);
    }
    pending=pending.filter(s=>s.state!=="done");
  }

  function on5Open(b){
    snapRange=calcRange();snapFvgs=[];snapBear=null;snapBull=null;
    if(!b.active)return;
    if(snapRange&&!snapRange.zero){
      pruneFvgs(b.activeOrd);snapFvgs=fvgs.filter(f=>fvgActive(f,b.activeOrd)).map(f=>f);
      const x=selectLocations(snapRange,b.activeOrd);snapBear=x.bear;snapBull=x.bull;
    }
  }
  function create5Fvg(b){
    active5.push(b);
    const n=active5.length-1;if(n<2)return;
    const a=active5[n-2],c=active5[n];
    if(c.l>a.h)fvgs.push({id:"H2-F"+(++fvgSeq),dir:"BULL",lower:a.h,upper:c.l,createOrd:c.activeOrd,createTs:c.closeTs,mitigated:false,expired:false});
    if(c.h<a.l)fvgs.push({id:"H2-F"+(++fvgSeq),dir:"BEAR",lower:c.h,upper:a.l,createOrd:c.activeOrd,createTs:c.closeTs,mitigated:false,expired:false});
  }
  function on5Close(b,m){
    if(!b.active)return;
    if(inSplit(b.closeTs))counts.active_5m++;
    if(!snapRange){create5Fvg(b);return;}
    if(snapRange.zero){if(inSplit(b.closeTs)){const s={id:"H2-S"+(++setupSeq),sweepTs:b.closeTs,state:"done",terminal:"range_zero_width"};setups.push(s);}create5Fvg(b);return;}
    const bh=b.h>snapRange.hi,bl=b.l<snapRange.lo;
    if((bh||bl)&&inSplit(b.closeTs))counts.boundary_breach_bars++;
    const touchBear=!!snapBear&&b.h>=snapBear.lower&&b.l<=snapBear.upper;
    const touchBull=!!snapBull&&b.h>=snapBull.lower&&b.l<=snapBull.upper;
    if((touchBear||touchBull)&&inSplit(b.closeTs))counts.external_fvg_touch_bars++;
    const inside=b.c>snapRange.lo&&b.c<snapRange.hi;
    const qBear=bh&&touchBear&&inside;
    const qBull=bl&&touchBull&&inside;
    if(qBear||qBull){
      if(inSplit(b.closeTs))counts.qualifying_raids++;
      if(qBear&&qBull){
        const s={id:"H2-S"+(++setupSeq),sweepTs:b.closeTs,state:"done",terminal:"dual_sided_raid_ambiguous"};setups.push(s);
      }else{
        const dir=qBear?"SHORT":"LONG",loc=qBear?snapBear:snapBull;
        const inWin=eligibleWeekday(b.closeTs)&&minsUTC(b.closeTs)>=360&&minsUTC(b.closeTs)<1080;
        if(!inWin){const s={id:"H2-S"+(++setupSeq),dir,sweepTs:b.closeTs,state:"done",terminal:"outside_setup_window"};setups.push(s);}
        else if(openTrade){const s={id:"H2-S"+(++setupSeq),dir,sweepTs:b.closeTs,state:"done",terminal:"suppressed_one_open"};setups.push(s);}
        else{if(inSplit(b.closeTs))counts.in_window_raids++;newSetup(dir,b,loc,snapRange,m);}
      }
    }else if((bh&&touchBear)||(bl&&touchBull)){
      const s={id:"H2-S"+(++setupSeq),sweepTs:b.closeTs,state:"done",terminal:"raid_without_rejection_close"};setups.push(s);
    }else if((bh||bl)&&!snapBear&&!snapBull){
      const s={id:"H2-S"+(++setupSeq),sweepTs:b.closeTs,state:"done",terminal:"no_external_preexisting_fvg"};setups.push(s);
    }
    for(const f of snapFvgs){if(!f.mitigated&&!f.expired&&b.h>=f.lower&&b.l<=f.upper){f.mitigated=true;f.mitigatedTs=b.closeTs;}}
    create5Fvg(b);
  }

  for(const m of rows){
    const bo=b5Start.get(m.ts);if(bo)on5Open(bo);
    if(m.active){
      activeM1.push(m);
      const occupiedAtOpen=!!openTrade;
      if(openTrade)processActual(openTrade,m);
      for(const t of shadows)processShadow(t,m);
      shadows=shadows.filter(t=>!t.shadowDone);
      processDueEntriesAtOpen(m,occupiedAtOpen);
      processPendingMss(m);
      confirmM1(m);
    }
    const bc=b5End.get(m.ts+MIN);if(bc)on5Close(bc,m);
  }
  if(openTrade){const last=rows[rows.length-1];closeTrade(openTrade,"exit_data_end",last.c,last.ts+MIN);}
  for(const t of shadows){if(!t.shadowDone){for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="horizon_without_target_or_stop";t.shadowDone=true;}}

  const ss=setups.filter(s=>inSplit(s.sweepTs||s.terminalTs||0)),tt=trades.filter(t=>inSplit(t.sweepTs));
  const reasons={};for(const s of ss)if(s.terminal)inc(reasons,s.terminal);
  const exits={};for(const t of tt)inc(exits,t.exitReason);
  const labels={};for(const d of[3000,4000,5000,7000,10000]){const a=tt.map(t=>t.labels[d]);labels[d]={target:a.filter(x=>x==="target_before_stop").length,stop:a.filter(x=>x==="stop_before_target").length,horizon:a.filter(x=>x==="horizon_without_target_or_stop").length,n:a.length};}
  const dates=[];for(let ts=dayStart(splitStart);ts<splitEnd;ts+=24*60*MIN){if(eligibleWeekday(ts))dates.push(utcDate(ts));}
  const daily={};for(const d of dates)daily[d]=0;for(const t of tt){const d=utcDate(t.fillTs);if(daily[d]!==undefined)daily[d]+=t.netUSD500;}
  const dv=dates.map(d=>daily[d]);
  function avg(field){return tt.length?tt.reduce((s,t)=>s+t[field],0)/tt.length:null;}
  function pf(field){let p=0,n=0;for(const t of tt){const x=t[field];if(x>0)p+=x;else if(x<0)n-=x;}return n?p/n:(p>0?Infinity:null);}
  function mdd(){let eq=500,peak=500,dd=0;for(const t of [...tt].sort((a,b)=>a.fillTs-b.fillTs)){eq+=t.netUSD500;peak=Math.max(peak,eq);dd=Math.max(dd,peak-eq);}return dd;}
  function lossRun(){let bn=0,bl=0,cn=0,cl=0;for(const t of [...tt].sort((a,b)=>a.fillTs-b.fillTs)){if(t.netUSD500<0){cn++;cl+=t.netUSD500;if(cn>bn||(cn===bn&&cl<bl)){bn=cn;bl=cl;}}else{cn=0;cl=0;}}return{count:bn,netLoss:bl};}
  function consec(pred){let b=0,c=0;for(const x of dv){if(pred(x)){c++;b=Math.max(b,c);}else c=0;}return b;}
  const direction={};for(const t of tt){if(!direction[t.dir])direction[t.dir]={n:0,netUSD500:0};direction[t.dir].n++;direction[t.dir].netUSD500+=t.netUSD500;}
  return{
    source_rows:rows.length,market_active_m1:rows.filter(x=>x.active).length,split:{start:new Date(splitStart).toISOString(),end_exclusive:new Date(splitEnd).toISOString()},
    event_counts:counts,setup_count:ss.length,terminal_reasons:reasons,accepted_filled_trades:tt.length,exits,
    target_hit_rate:tt.length?(exits.exit_target||0)/tt.length:null,stop_rate:tt.length?((exits.exit_stop||0)+(exits.exit_stop_fill_bar||0))/tt.length:null,
    timeout_rate:tt.length?((exits.exit_timeout_120||0)+(exits.exit_session_2000||0)+(exits.exit_data_end||0))/tt.length:null,
    label_rates:labels,expectancy:{gross_usd:avg("grossUSD"),net_usd_0:avg("netUSD0"),net_usd_025:avg("netUSD250"),net_usd_050:avg("netUSD500")},
    profit_factor:{gross:pf("grossUSD"),net_0:pf("netUSD0"),net_025:pf("netUSD250"),net_050:pf("netUSD500")},
    total_net_usd_050:tt.reduce((s,t)=>s+t.netUSD500,0),weekdays:dates.length,
    daily:{mean:dv.length?dv.reduce((a,b)=>a+b,0)/dv.length:null,median:pctile(dv,.5),losing_pct:dv.length?dv.filter(x=>x<0).length/dv.length:null,le50_pct:dv.length?dv.filter(x=>x<=50).length/dv.length:null,ge100_pct:dv.length?dv.filter(x=>x>=100).length/dv.length:null,ge150_pct:dv.length?dv.filter(x=>x>=150).length/dv.length:null,ge200_pct:dv.length?dv.filter(x=>x>=200).length/dv.length:null},
    max_drawdown_usd:mdd(),worst_losing_trade_run:lossRun(),max_consecutive_losing_weekdays:consec(x=>x<0),max_consecutive_le50_weekdays:consec(x=>x<=50),
    actual_mfe_ticks:dist(tt.map(t=>t.actualMFE)),actual_mae_ticks:dist(tt.map(t=>t.actualMAE)),potential_mfe_ticks:dist(tt.map(t=>t.potentialMFE)),potential_mae_ticks:dist(tt.map(t=>t.potentialMAE)),
    target_distance_ticks:dist(tt.map(t=>t.targetDist)),stop_distance_ticks:dist(tt.map(t=>t.stopDist)),gross_stop_usd:dist(tt.map(t=>t.stopDist*TICK_USD)),
    location_fvg_age_active5:dist(tt.map(t=>t.locationFvgAge)),location_distance_ticks:dist(tt.map(t=>t.locationDistance)),direction,
    trades:tt,setups:ss,daily_series:dates.map(d=>({date:d,netUSD500:daily[d]}))
  };
}
function bootstrap(metrics,reps=10000,seed=17017){
  const days=metrics.daily_series,by=new Map(days.map(x=>[x.date,[]]));
  for(const t of metrics.trades){const d=utcDate(t.fillTs);if(by.has(d))by.get(d).push(t.netUSD500);}
  const blocks=[];for(let i=0;i+5<=days.length;i++)blocks.push(days.slice(i,i+5).map(x=>x.date));
  let state=seed>>>0;function rnd(){state=(1664525*state+1013904223)>>>0;return state/4294967296;}
  const ex=[],dm=[];let zero=0;
  for(let r=0;r<reps;r++){const pick=[];while(pick.length<days.length){const b=blocks[Math.floor(rnd()*blocks.length)];for(const d of b){if(pick.length<days.length)pick.push(d);}}let pnl=0,n=0;for(const d of pick){for(const x of by.get(d)||[]){pnl+=x;n++;}}dm.push(pnl/days.length);if(n)ex.push(pnl/n);else zero++;}
  return{reps,seed,block_weekdays:5,zero_trade_resamples:zero,expectancy_net_usd_050:{point:metrics.expectancy.net_usd_050,lo:pctile(ex,.025),hi:pctile(ex,.975)},mean_daily_net_usd_050:{point:metrics.daily.mean,lo:pctile(dm,.025),hi:pctile(dm,.975)}};
}
function selfTest(){
  assert(parseTick("2062.688")===2062688,"tick");let threw=false;try{parseTick("1.2345");}catch(e){threw=true;}assert(threw,"offgrid");
  assert(3000>=2*1500&&!(2999>=2*1500),"rr_exact");
  assert(4000*TICK_USD===40,"gross_risk_exact");
  return{ok:true,tests:["tick","offgrid","reward_risk_2.0","gross_risk_40"]};
}
root.EngineHv02={runEngineH,bootstrap,selfTest,parseTick};
})(globalThis);
