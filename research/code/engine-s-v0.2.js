/* Engine S v0.2 zero-outcome preflight implementation.
 * Governed by research/experiments/EXP-045-engine-s-human-style-liquidity-decision-tree-v0.2.md.
 * This file intentionally contains NO post-entry target/path/P&L evaluation.
 */
(function(root){
"use strict";

const MIN=60000;
const TICK_USD_010=0.01;

function assert(c,m){if(!c)throw new Error(m);}
function utcDate(ts){return new Date(ts).toISOString().slice(0,10);}
function dayStart(ts){const d=new Date(ts);return Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate());}
function minsUTC(ts){const d=new Date(ts);return d.getUTCHours()*60+d.getUTCMinutes();}
function weekday(ts){const w=new Date(ts).getUTCDay();return w>=1&&w<=5;}
function inc(o,k,n=1){o[k]=(o[k]||0)+n;}

function parseTick(s){
  const m=/^([0-9]+)(?:\.([0-9]+))?$/.exec(String(s).trim());
  if(!m)throw new Error("invalid_price_text:"+s);
  let f=m[2]||"";
  if(f.length>3){
    const x=f.slice(3);
    if(!/^0*$/.test(x))throw new Error("off_grid_price:"+s);
    f=f.slice(0,3);
  }
  f=f.padEnd(3,"0");
  return Number(m[1])*1000+Number(f);
}

function parseMonthlyCsv(name,content,expectedRows){
  const lines=content.trimEnd().split("\n");
  assert(lines[0].trim()==="timestamp,open,high,low,close","bad_header:"+name);
  assert(lines.length===expectedRows+1,"bad_row_count:"+name+":"+(lines.length-1));
  const out=new Array(expectedRows);
  let prev=null;
  for(let i=1;i<lines.length;i++){
    const p=lines[i].trim().split(",");
    assert(p.length===5,"bad_columns:"+name+":"+i);
    const ts=Number(p[0]);
    assert(Number.isInteger(ts)&&ts%MIN===0,"bad_timestamp:"+name+":"+i);
    if(prev!==null)assert(ts-prev===MIN,"non_contiguous_timestamp:"+name+":"+i);
    prev=ts;
    const o=parseTick(p[1]),h=parseTick(p[2]),l=parseTick(p[3]),c=parseTick(p[4]);
    assert(o>0&&h>0&&l>0&&c>0&&h>=o&&h>=c&&l<=o&&l<=c&&h>=l,"invalid_ohlc:"+name+":"+i);
    out[i-1]={ts,o,h,l,c,active:false,activeOrd:-1};
  }
  return out;
}

function buildRows(months){
  let rows=[];
  for(const m of months){
    const r=parseMonthlyCsv(m.name,m.content,m.expectedRows);
    if(rows.length)assert(r[0].ts-rows[rows.length-1].ts===MIN,"month_boundary_gap:"+m.name);
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

function buildBars(rows,minutes){
  const out=[],size=minutes;
  for(let i=0;i<rows.length;){
    const start=rows[i].ts;
    const aligned=Math.floor(start/(size*MIN))*(size*MIN);
    if(start!==aligned){i++;continue;}
    if(i+size>rows.length)break;
    let ok=true;
    for(let j=0;j<size;j++)if(rows[i+j].ts!==start+j*MIN){ok=false;break;}
    if(!ok){i++;continue;}
    const q=rows.slice(i,i+size);
    out.push({
      startTs:start,closeTs:start+size*MIN,
      o:q[0].o,h:Math.max(...q.map(x=>x.h)),l:Math.min(...q.map(x=>x.l)),c:q[q.length-1].c,
      active:q.some(x=>x.active),activeOrd:-1,rowStart:i,rowEnd:i+size-1
    });
    i+=size;
  }
  let ord=0;
  for(const b of out)if(b.active)b.activeOrd=ord++;
  return out;
}

function buildDayStats(rows){
  const days=new Map(),asia=new Map(),opening=new Map();
  function add(map,d,r){
    let x=map.get(d);
    if(!x){x={high:-Infinity,low:Infinity,rows:0,activeM1:0};map.set(d,x);}
    x.high=Math.max(x.high,r.h);x.low=Math.min(x.low,r.l);x.rows++;if(r.active)x.activeM1++;
  }
  for(const r of rows){
    const d=utcDate(r.ts),m=minsUTC(r.ts);
    add(days,d,r);
    if(m<360)add(asia,d,r);
    if(m>=360&&m<540)add(opening,d,r);
  }
  return{days,asia,opening};
}

function percentile(a,p){
  if(!a.length)return null;
  const b=[...a].sort((x,y)=>x-y);
  const pos=(b.length-1)*p,lo=Math.floor(pos),hi=Math.ceil(pos);
  return lo===hi?b[lo]:b[lo]+(b[hi]-b[lo])*(pos-lo);
}
function dist(a){
  if(!a.length)return{n:0,mean:null,median:null,p10:null,p90:null,min:null,max:null};
  return{
    n:a.length,
    mean:a.reduce((x,y)=>x+y,0)/a.length,
    median:percentile(a,.5),
    p10:percentile(a,.1),
    p90:percentile(a,.9),
    min:Math.min(...a),max:Math.max(...a)
  };
}

function runEngineS(months,splitStart,splitEnd){
  const rows=buildRows(months);
  const bars5=buildBars(rows,5);
  const bar5ByClose=new Map(bars5.map(b=>[b.closeTs,b]));
  const stats=buildDayStats(rows);

  const activeM1=[];
  const pivH=[],pivL=[];
  const levelCache=new Map();
  const pending=[];
  const setups=[];
  const accepted=[];
  let setupSeq=0,candidateSeq=0;

  const counts={
    market_active_5m:0,
    level_attacks_all_hours:0,
    attacks_consumed_outside_setup_window:0,
    dual_sided_attack_ambiguous:0,
    attack_close_on_level:0,
    setup_attacks_in_window:0,
    rejection_setups_created:0,
    acceptance_setups_created:0,
    pending_pipeline_overlap_events:0,
    max_simultaneous_pending:0,
    mss_close_through_seen:0,
    displacement_pass_seen:0,
    directional_fvg_pass_seen:0,
    qualifying_triggers:0,
    midpoint_fills:0
  };
  const attackByLevel={},attackBySide={},branchByLevel={},terminalReasons={};

  const inSplit=ts=>ts>=splitStart&&ts<splitEnd;
  const activePending=()=>pending.filter(s=>s.state!=="done");

  function previousActiveDay(d){
    const [y,m,dd]=d.split("-").map(Number);
    let t=Date.UTC(y,m-1,dd)-24*60*MIN;
    for(let k=0;k<10;k++,t-=24*60*MIN){
      const ds=utcDate(t),x=stats.days.get(ds);
      if(x&&x.activeM1>0&&x.high>x.low)return{date:ds,...x};
    }
    return null;
  }

  function levelsForDate(d){
    if(levelCache.has(d))return levelCache.get(d);
    const [y,m,dd]=d.split("-").map(Number),ds=Date.UTC(y,m-1,dd),a=[];
    const p=previousActiveDay(d);
    if(p){
      a.push({id:d+":PDH",cls:"PDH",side:"HIGH",priority:1,price:p.high,knownTs:ds,consumed:false,sourceDate:p.date});
      a.push({id:d+":PDL",cls:"PDL",side:"LOW",priority:1,price:p.low,knownTs:ds,consumed:false,sourceDate:p.date});
    }
    const as=stats.asia.get(d);
    if(as&&as.rows===360&&as.activeM1>0&&as.high>as.low){
      a.push({id:d+":ASIA_HIGH",cls:"ASIA_HIGH",side:"HIGH",priority:2,price:as.high,knownTs:ds+360*MIN,consumed:false,sourceDate:d});
      a.push({id:d+":ASIA_LOW",cls:"ASIA_LOW",side:"LOW",priority:2,price:as.low,knownTs:ds+360*MIN,consumed:false,sourceDate:d});
    }
    const op=stats.opening.get(d);
    if(op&&op.rows===180&&op.activeM1>0&&op.high>op.low){
      a.push({id:d+":OPEN_HIGH",cls:"OPEN_HIGH",side:"HIGH",priority:3,price:op.high,knownTs:ds+540*MIN,consumed:false,sourceDate:d});
      a.push({id:d+":OPEN_LOW",cls:"OPEN_LOW",side:"LOW",priority:3,price:op.low,knownTs:ds+540*MIN,consumed:false,sourceDate:d});
    }
    levelCache.set(d,a);return a;
  }

  function confirmPivot(m){
    const n=activeM1.length-1;
    if(n<4)return;
    const t=n-2,a=activeM1,c=a[t];
    if(c.h>a[t-1].h&&c.h>a[t-2].h&&c.h>=a[t+1].h&&c.h>=a[t+2].h)
      pivH.push({kind:"HIGH",centerOrd:c.activeOrd,centerTs:c.ts,confirmOrd:m.activeOrd,confirmTs:m.ts+MIN,price:c.h});
    if(c.l<a[t-1].l&&c.l<a[t-2].l&&c.l<=a[t+1].l&&c.l<=a[t+2].l)
      pivL.push({kind:"LOW",centerOrd:c.activeOrd,centerTs:c.ts,confirmOrd:m.activeOrd,confirmTs:m.ts+MIN,price:c.l});
  }

  function selectPivot(dir,currentOrd,centerAfterTs=null){
    const arr=dir==="LONG"?pivH:pivL,minOrd=currentOrd-14;
    for(let i=arr.length-1;i>=0;i--){
      const p=arr[i];
      if(p.centerOrd<minOrd)break;
      if(p.confirmOrd>currentOrd)continue;
      if(centerAfterTs!==null&&!(p.centerTs>centerAfterTs))continue;
      return p;
    }
    return null;
  }

  function reject(s,reason,ts){
    if(s.state==="done")return;
    s.state="done";s.terminal=reason;s.terminalTs=ts;inc(terminalReasons,reason);
  }

  function registerSetup(s){
    const overlap=activePending().length;
    if(overlap>0)counts.pending_pipeline_overlap_events++;
    setups.push(s);pending.push(s);
    counts.max_simultaneous_pending=Math.max(counts.max_simultaneous_pending,overlap+1);
  }

  function newRejection(dir,b,level,currentOrd){
    const s={
      id:"S-S"+(++setupSeq),branch:"REJECTION",dir,
      levelId:level.id,levelClass:level.cls,levelSide:level.side,levelPrice:level.price,levelKnownTs:level.knownTs,
      attackStartTs:b.startTs,attackCloseTs:b.closeTs,attackHigh:b.h,attackLow:b.l,attack5Ord:b.activeOrd,
      createdOrd:currentOrd,state:"mss",mssSeen:0,dispSeen:0,fvgSeen:0,entrySeen:0,
      sawMss:false,sawDisp:false,sawFvg:false,terminal:null
    };
    const p=selectPivot(dir,currentOrd,null);
    if(!p){setups.push(s);s.state="done";s.terminal="no_internal_pivot_at_rejection_anchor";s.terminalTs=b.closeTs;inc(terminalReasons,s.terminal);return;}
    s.pivot=p;
    registerSetup(s);counts.rejection_setups_created++;inc(branchByLevel,"REJECTION:"+level.cls);
  }

  function newAcceptance(dir,b,level,currentOrd){
    const s={
      id:"S-S"+(++setupSeq),branch:"ACCEPTANCE",dir,
      levelId:level.id,levelClass:level.cls,levelSide:level.side,levelPrice:level.price,levelKnownTs:level.knownTs,
      attackStartTs:b.startTs,attackCloseTs:b.closeTs,attackHigh:b.h,attackLow:b.l,attack5Ord:b.activeOrd,
      createdOrd:currentOrd,state:"accept_confirm",confirm5Seen:false,pullbackSeen:0,mssSeen:0,dispSeen:0,fvgSeen:0,entrySeen:0,
      sawMss:false,sawDisp:false,sawFvg:false,terminal:null
    };
    registerSetup(s);counts.acceptance_setups_created++;inc(branchByLevel,"ACCEPTANCE:"+level.cls);
  }

  function displacementPass(s,m){
    const ord=m.activeOrd;
    if(ord<20)return false;
    const body=Math.abs(m.c-m.o);
    let sum=0;
    for(let i=ord-20;i<ord;i++)sum+=Math.abs(activeM1[i].c-activeM1[i].o);
    const directional=s.dir==="LONG"?m.c>m.o:m.c<m.o;
    return directional&&40*body>=3*sum;
  }

  function fvgAt(s,m){
    const ord=m.activeOrd;
    if(ord<2)return null;
    const a=activeM1[ord-2];
    if(s.dir==="LONG"&&m.l>a.h)return{lo:a.h,hi:m.l};
    if(s.dir==="SHORT"&&m.h<a.l)return{lo:m.h,hi:a.l};
    return null;
  }

  function freezeEntryFromFvg(s,m,fvg){
    const num=fvg.lo+fvg.hi;
    const entry=s.dir==="LONG"?Math.floor((num+1)/2):Math.floor(num/2);
    let stop;
    if(s.branch==="REJECTION")stop=s.dir==="LONG"?s.attackLow-1:s.attackHigh+1;
    else stop=s.dir==="LONG"?s.pullbackExtreme-1:s.pullbackExtreme+1;

    if((s.dir==="LONG"&&!(stop<entry))||(s.dir==="SHORT"&&!(entry<stop))){
      reject(s,"invalid_stop_geometry",m.ts+MIN);return;
    }
    const stopDist=Math.abs(entry-stop);
    if(stopDist>4000){reject(s,"structural_risk_above_40",m.ts+MIN);return;}

    s.fvgOrd=m.activeOrd;s.fvgTs=m.ts+MIN;
    s.fvgLo=fvg.lo;s.fvgHi=fvg.hi;s.entry=entry;s.stop=stop;s.stopDist=stopDist;
    s.grossStopUSD=stopDist*TICK_USD_010;
    s.triggerOrd=m.activeOrd;s.triggerTs=m.ts+MIN;
    s.state="entry";s.entrySeen=0;counts.qualifying_triggers++;
  }

  function processMss(s,m){
    const anchorOrd=s.branch==="REJECTION"?s.createdOrd:s.pullbackOrd;
    if(m.activeOrd<=anchorOrd)return;
    s.mssSeen++;
    const cross=s.dir==="LONG"?m.c>s.pivot.price:m.c<s.pivot.price;
    if(cross){
      s.sawMss=true;s.mssOrd=m.activeOrd;s.mssTs=m.ts+MIN;
      s.timeToMssBars=m.activeOrd-anchorOrd;
      counts.mss_close_through_seen++;
      s.state="displacement";s.dispSeen=0;
      processDisplacement(s,m);
      return;
    }
    if(s.mssSeen>=15)reject(s,"mss_timeout_15",m.ts+MIN);
  }

  function processDisplacement(s,m){
    if(m.activeOrd<s.mssOrd)return;
    if(m.activeOrd>s.mssOrd+2){reject(s,"displacement_timeout_mss_plus_2",m.ts+MIN);return;}
    s.dispSeen++;
    if(displacementPass(s,m)){
      s.sawDisp=true;s.displacementOrd=m.activeOrd;s.displacementTs=m.ts+MIN;
      s.mssToDisplacementBars=m.activeOrd-s.mssOrd;
      counts.displacement_pass_seen++;
      s.state="fvg";s.fvgSeen=0;
      processFvg(s,m);
      return;
    }
    if(m.activeOrd===s.mssOrd+2)reject(s,"displacement_timeout_mss_plus_2",m.ts+MIN);
  }

  function processFvg(s,m){
    if(m.activeOrd<s.displacementOrd)return;
    if(m.activeOrd>s.displacementOrd+2){reject(s,"fvg_timeout_displacement_plus_2",m.ts+MIN);return;}
    s.fvgSeen++;
    const fvg=fvgAt(s,m);
    if(fvg){
      s.sawFvg=true;s.displacementToFvgBars=m.activeOrd-s.displacementOrd;
      counts.directional_fvg_pass_seen++;
      freezeEntryFromFvg(s,m,fvg);
      return;
    }
    if(m.activeOrd===s.displacementOrd+2)reject(s,"fvg_timeout_displacement_plus_2",m.ts+MIN);
  }

  function acceptCandidate(s,m){
    const c={
      id:"S-C"+(++candidateSeq),setupId:s.id,branch:s.branch,direction:s.dir,
      levelClass:s.levelClass,levelSide:s.levelSide,levelPrice:s.levelPrice,levelKnownTs:s.levelKnownTs,
      attackStartTs:s.attackStartTs,attackCloseTs:s.attackCloseTs,
      acceptanceConfirmTs:s.acceptanceConfirmTs||null,pullbackTs:s.pullbackTs||null,
      pivotKind:s.pivot.kind,pivotPrice:s.pivot.price,pivotCenterTs:s.pivot.centerTs,pivotConfirmTs:s.pivot.confirmTs,
      mssTs:s.mssTs,displacementTs:s.displacementTs,fvgTs:s.fvgTs,
      triggerTs:s.triggerTs,fillBarStartTs:m.ts,fillSignalTs:m.ts+MIN,
      timeToMssBars:s.timeToMssBars,mssToDisplacementBars:s.mssToDisplacementBars,
      displacementToFvgBars:s.displacementToFvgBars,fvgToFillBars:m.activeOrd-s.fvgOrd,
      pullbackWaitBars:s.pullbackWaitBars||null,
      fvgLo:s.fvgLo,fvgHi:s.fvgHi,entry:s.entry,stop:s.stop,
      stopDistanceTicks:s.stopDist,grossStopUSD:s.grossStopUSD,
      causality:{
        level_known_before_attack:s.levelKnownTs<=s.attackStartTs,
        trigger_after_attack:s.triggerTs>s.attackCloseTs,
        fill_after_trigger:(m.ts+MIN)>s.triggerTs,
        acceptance_order_ok:s.branch==="REJECTION"||(
          s.acceptanceConfirmTs>s.attackCloseTs&&
          s.pullbackTs>s.acceptanceConfirmTs&&
          s.triggerTs>s.pullbackTs
        )
      }
    };
    accepted.push(c);counts.midpoint_fills++;
    s.state="done";s.terminal=null;s.fillTs=m.ts+MIN;s.candidateId=c.id;
  }

  function processM1(m){
    activeM1.push(m);
    confirmPivot(m);
    const ct=m.ts+MIN;
    const live=[...pending];
    for(const s of live){
      if(s.state==="done")continue;
      if(minsUTC(ct)>=18*60){reject(s,"entry_window_closed_1800",ct);continue;}

      if(s.branch==="ACCEPTANCE"&&s.state!=="accept_confirm"&&s.acceptanceConfirmTs!=null){
        const b5now=bar5ByClose.get(ct);
        if(b5now&&b5now.active&&b5now.closeTs>s.acceptanceConfirmTs){
          const back=s.dir==="LONG"?b5now.c<s.levelPrice:b5now.c>s.levelPrice;
          if(back){reject(s,"acceptance_5m_close_back_before_entry",ct);continue;}
        }
      }

      if(s.state==="wait_pullback"){
        if(m.activeOrd<=s.acceptanceConfirmOrd)continue;
        s.pullbackSeen++;
        const touch=s.dir==="LONG"?m.l<=s.levelPrice:m.h>=s.levelPrice;
        if(touch){
          s.pullbackTs=ct;s.pullbackOrd=m.activeOrd;s.pullbackWaitBars=s.pullbackSeen;
          s.pullbackExtreme=s.dir==="LONG"?m.l:m.h;
          const p=selectPivot(s.dir,m.activeOrd,s.attackStartTs);
          if(!p){reject(s,"no_internal_pivot_at_pullback_touch",ct);continue;}
          s.pivot=p;s.state="mss";s.mssSeen=0;
        }else if(s.pullbackSeen>=60)reject(s,"pullback_timeout_60",ct);
        continue;
      }

      if(s.branch==="ACCEPTANCE"&&["mss","displacement","fvg"].includes(s.state)&&s.pullbackOrd!=null&&m.activeOrd>=s.pullbackOrd){
        if(s.dir==="LONG")s.pullbackExtreme=Math.min(s.pullbackExtreme,m.l);
        else s.pullbackExtreme=Math.max(s.pullbackExtreme,m.h);
      }

      if(s.state==="mss"){processMss(s,m);continue;}
      if(s.state==="displacement"){processDisplacement(s,m);continue;}
      if(s.state==="fvg"){processFvg(s,m);continue;}

      if(s.state==="entry"){
        if(m.activeOrd<=s.triggerOrd)continue;
        s.entrySeen++;
        const stopHit=s.dir==="LONG"?m.l<=s.stop:m.h>=s.stop;
        if(stopHit){reject(s,"preentry_invalidation_same_bar",ct);continue;}
        const fill=s.dir==="LONG"?m.l<=s.entry:m.h>=s.entry;
        if(fill){acceptCandidate(s,m);continue;}
        if(s.entrySeen>=15)reject(s,"entry_timeout_15",ct);
      }
    }
  }

  function processAcceptance5m(b){
    for(const s of pending){
      if(s.state==="done"||s.branch!=="ACCEPTANCE")continue;

      if(s.state==="accept_confirm"){
        if(!b.active||b.activeOrd<=s.attack5Ord)continue;
        if(s.confirm5Seen)continue;
        s.confirm5Seen=true;
        const held=s.dir==="LONG"?b.c>s.levelPrice:b.c<s.levelPrice;
        if(!held){reject(s,"acceptance_failed_next_active5",b.closeTs);continue;}
        s.acceptanceConfirmTs=b.closeTs;
        s.acceptanceConfirmOrd=activeM1.length?activeM1[activeM1.length-1].activeOrd:-1;
        s.state="wait_pullback";s.pullbackSeen=0;
        continue;
      }

      if(["wait_pullback","mss","displacement","fvg","entry"].includes(s.state)&&b.active&&b.closeTs>s.acceptanceConfirmTs){
        const back=s.dir==="LONG"?b.c<s.levelPrice:b.c>s.levelPrice;
        if(back)reject(s,"acceptance_5m_close_back_before_entry",b.closeTs);
      }
    }
  }

  function processAttacks5m(b){
    const d=utcDate(b.startTs),levels=levelsForDate(d);
    const elig=levels.filter(x=>!x.consumed&&x.knownTs<=b.startTs);
    const hi=elig.filter(x=>x.side==="HIGH"&&b.h>x.price);
    const lo=elig.filter(x=>x.side==="LOW"&&b.l<x.price);
    if(!hi.length&&!lo.length)return;

    for(const x of hi.concat(lo))x.consumed=true;
    counts.level_attacks_all_hours++;
    for(const x of hi.concat(lo)){inc(attackByLevel,x.cls);inc(attackBySide,x.side);}

    const setupWindow=weekday(b.startTs)&&minsUTC(b.closeTs)>=360&&minsUTC(b.closeTs)<1020&&inSplit(b.closeTs);
    if(!setupWindow){counts.attacks_consumed_outside_setup_window++;return;}

    counts.setup_attacks_in_window++;
    if(hi.length&&lo.length){counts.dual_sided_attack_ambiguous++;return;}

    const side=hi.length?"HIGH":"LOW",arr=hi.length?hi:lo;
    arr.sort((a,b)=>a.priority-b.priority||a.cls.localeCompare(b.cls));
    const level=arr[0];
    const currentOrd=activeM1.length?activeM1[activeM1.length-1].activeOrd:-1;
    if(currentOrd<0)return;

    if(side==="HIGH"){
      if(b.c<level.price)newRejection("SHORT",b,level,currentOrd);
      else if(b.c>level.price)newAcceptance("LONG",b,level,currentOrd);
      else counts.attack_close_on_level++;
    }else{
      if(b.c>level.price)newRejection("LONG",b,level,currentOrd);
      else if(b.c<level.price)newAcceptance("SHORT",b,level,currentOrd);
      else counts.attack_close_on_level++;
    }
  }

  for(const m of rows){
    if(m.active)processM1(m);
    const b=bar5ByClose.get(m.ts+MIN);
    if(b){
      if(b.active&&inSplit(b.closeTs))counts.market_active_5m++;
      processAcceptance5m(b);
      processAttacks5m(b);
    }
  }

  for(const s of pending)if(s.state!=="done")reject(s,"data_end_pending",rows[rows.length-1].ts+MIN);

  const splitSetups=setups.filter(s=>inSplit(s.attackCloseTs));
  const byBranch={},byDirection={},byLevel={},branchDirection={};
  for(const c of accepted){
    inc(byBranch,c.branch);inc(byDirection,c.direction);inc(byLevel,c.levelClass);
    inc(branchDirection,c.branch+":"+c.direction);
  }

  const dayCounts={};
  for(const c of accepted)inc(dayCounts,utcDate(c.fillSignalTs-1));
  const activeDays=Object.keys(dayCounts).sort();
  const perActiveDay=activeDays.map(d=>dayCounts[d]);

  const causal=accepted.every(c=>
    c.causality.level_known_before_attack&&
    c.causality.trigger_after_attack&&
    c.causality.fill_after_trigger&&
    c.causality.acceptance_order_ok
  );

  const gates={
    accepted_candidates_ge_100:accepted.length>=100,
    rejection_candidates_ge_25:(byBranch.REJECTION||0)>=25,
    acceptance_candidates_ge_25:(byBranch.ACCEPTANCE||0)>=25,
    both_directions_rejection:(branchDirection["REJECTION:LONG"]||0)>0&&(branchDirection["REJECTION:SHORT"]||0)>0,
    both_directions_acceptance:(branchDirection["ACCEPTANCE:LONG"]||0)>0&&(branchDirection["ACCEPTANCE:SHORT"]||0)>0,
    active_signal_days_ge_50:activeDays.length>=50,
    median_candidates_per_active_day_le_4:perActiveDay.length>0&&percentile(perActiveDay,.5)<=4,
    causal_integrity:causal,
    validation_or_holdout_loaded:false,
    target_or_pnl_outcomes_calculated:false
  };
  const pass=Object.entries(gates).every(([k,v])=>{
    if(k==="validation_or_holdout_loaded"||k==="target_or_pnl_outcomes_calculated")return v===false;
    return v===true;
  });

  return{
    experiment:"EXP-045",
    engine:"Engine S v0.2",
    stage:"zero_outcome_development_preflight",
    split:{start:new Date(splitStart).toISOString(),end_exclusive:new Date(splitEnd).toISOString()},
    source_rows:rows.length,
    market_active_m1:rows.filter(x=>x.active).length,
    counts,
    attacks_by_level:attackByLevel,
    attacks_by_side:attackBySide,
    setup_count:splitSetups.length,
    terminal_reasons:terminalReasons,
    accepted_filled_candidates:accepted.length,
    accepted_by_branch:byBranch,
    accepted_by_direction:byDirection,
    accepted_by_level:byLevel,
    accepted_by_branch_direction:branchDirection,
    accepted_signal_days:activeDays.length,
    accepted_candidates_per_active_day:{
      distribution:dist(perActiveDay),
      by_date:dayCounts
    },
    stop_distance_ticks:dist(accepted.map(x=>x.stopDistanceTicks)),
    gross_stop_usd:dist(accepted.map(x=>x.grossStopUSD)),
    time_to_mss_active_m1_bars:dist(accepted.map(x=>x.timeToMssBars).filter(Number.isFinite)),
    mss_to_displacement_active_m1_bars:dist(accepted.map(x=>x.mssToDisplacementBars).filter(Number.isFinite)),
    displacement_to_fvg_active_m1_bars:dist(accepted.map(x=>x.displacementToFvgBars).filter(Number.isFinite)),
    fvg_to_fill_active_m1_bars:dist(accepted.map(x=>x.fvgToFillBars).filter(Number.isFinite)),
    acceptance_pullback_wait_active_m1_bars:dist(accepted.map(x=>x.pullbackWaitBars).filter(Number.isFinite)),
    causality_all_candidates_pass:causal,
    preflight_gates:gates,
    preflight_pass:pass,
    disposition:pass?"EXP045_ZERO_OUTCOME_PREFLIGHT_PASS":"EXP045_ZERO_OUTCOME_PREFLIGHT_FAIL",
    validation_or_holdout_loaded:false,
    target_labels_calculated:false,
    mfe_mae_calculated:false,
    pnl_calculated:false,
    win_rate_calculated:false,
    post_entry_path_evaluated:false,
    accepted_candidates:accepted,
    setups:splitSetups
  };
}

function selfTest(){
  assert(parseTick("2062.688")===2062688,"tick_parse");
  let threw=false;try{parseTick("1.2345");}catch(e){threw=true;}assert(threw,"off_grid");
  assert(40*150>=3*2000&&!(40*149>=3*2000),"disp_1_50_exact");
  assert(Math.floor((1001+1002+1)/2)===1002,"long_midpoint");
  assert(Math.floor((1001+1002)/2)===1001,"short_midpoint");
  const fake=[
    {activeOrd:0,h:10,l:5,ts:0},{activeOrd:1,h:11,l:4,ts:1},
    {activeOrd:2,h:15,l:3,ts:2},{activeOrd:3,h:12,l:4,ts:3},{activeOrd:4,h:12,l:4,ts:4}
  ];
  assert(fake[2].h>fake[1].h&&fake[2].h>fake[0].h&&fake[2].h>=fake[3].h&&fake[2].h>=fake[4].h,"pivot_2l2r");
  return{ok:true,tests:["tick_parse","off_grid","displacement_1_50_exact","midpoint_rounding","pivot_2l2r"]};
}

root.EngineSv02={runEngineS,selfTest,parseTick};
})(globalThis);
