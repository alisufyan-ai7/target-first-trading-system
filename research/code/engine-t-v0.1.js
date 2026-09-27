/* Engine T v0.1 zero-outcome preflight.
 * Governed by research/experiments/EXP-046-engine-t-v0.1-failed-auction-trap-zero-outcome.md.
 * Intentionally contains NO target/path/P&L evaluation.
 */
(function(root){
"use strict";

const MIN=60000;
const TICK_USD_010=0.01;

function assert(c,m){if(!c)throw new Error(m);}
function utcDate(ts){return new Date(ts).toISOString().slice(0,10);}
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
      active:q.some(x=>x.active),activeOrd:-1
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

function runEngineT(months,splitStart,splitEnd){
  const rows=buildRows(months);
  const bars5=buildBars(rows,5);
  const bar5ByClose=new Map(bars5.map(b=>[b.closeTs,b]));
  const stats=buildDayStats(rows);
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
    attack_immediate_rejection_ignored:0,
    breakout_setups_created:0,
    acceptance_confirmed:0,
    acceptance_confirm_failed:0,
    qualifying_failed_auctions:0,
    failed_auction_timeout_6:0,
    boundary_retest_fills:0
  };
  const attackByLevel={},terminalReasons={};

  const inSplit=ts=>ts>=splitStart&&ts<splitEnd;

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
      a.push({id:d+":PDH",cls:"PDH",side:"HIGH",priority:1,price:p.high,knownTs:ds,consumed:false});
      a.push({id:d+":PDL",cls:"PDL",side:"LOW",priority:1,price:p.low,knownTs:ds,consumed:false});
    }
    const as=stats.asia.get(d);
    if(as&&as.rows===360&&as.activeM1>0&&as.high>as.low){
      a.push({id:d+":ASIA_HIGH",cls:"ASIA_HIGH",side:"HIGH",priority:2,price:as.high,knownTs:ds+360*MIN,consumed:false});
      a.push({id:d+":ASIA_LOW",cls:"ASIA_LOW",side:"LOW",priority:2,price:as.low,knownTs:ds+360*MIN,consumed:false});
    }
    const op=stats.opening.get(d);
    if(op&&op.rows===180&&op.activeM1>0&&op.high>op.low){
      a.push({id:d+":OPEN_HIGH",cls:"OPEN_HIGH",side:"HIGH",priority:3,price:op.high,knownTs:ds+540*MIN,consumed:false});
      a.push({id:d+":OPEN_LOW",cls:"OPEN_LOW",side:"LOW",priority:3,price:op.low,knownTs:ds+540*MIN,consumed:false});
    }
    levelCache.set(d,a);return a;
  }

  function reject(s,reason,ts){
    if(s.state==="done")return;
    s.state="done";s.terminal=reason;s.terminalTs=ts;inc(terminalReasons,reason);
  }

  function createSetup(b,level,breakDir){
    const s={
      id:"T-S"+(++setupSeq),
      breakoutDirection:breakDir,
      tradeDirection:breakDir==="LONG"?"SHORT":"LONG",
      levelId:level.id,levelClass:level.cls,levelSide:level.side,levelPrice:level.price,levelKnownTs:level.knownTs,
      attackStartTs:b.startTs,attackCloseTs:b.closeTs,attack5Ord:b.activeOrd,
      excursionHigh:b.h,excursionLow:b.l,
      state:"accept_confirm",
      confirmSeen:false,failureBarsSeen:0,entryBarsSeen:0,
      terminal:null
    };
    setups.push(s);pending.push(s);counts.breakout_setups_created++;
  }

  function bodyPass(b,tradeDir){
    const range=b.h-b.l;
    if(range<=0)return false;
    const body=Math.abs(b.c-b.o);
    if(2*body<range)return false;
    return tradeDir==="SHORT"?b.c<b.o:b.c>b.o;
  }

  function process5mState(b){
    for(const s of pending){
      if(s.state==="done")continue;
      if(s.state==="accept_confirm"){
        if(!b.active||b.activeOrd<=s.attack5Ord)continue;
        if(s.confirmSeen)continue;
        s.confirmSeen=true;
        s.excursionHigh=Math.max(s.excursionHigh,b.h);
        s.excursionLow=Math.min(s.excursionLow,b.l);
        const held=s.breakoutDirection==="LONG"?b.c>s.levelPrice:b.c<s.levelPrice;
        if(!held){
          counts.acceptance_confirm_failed++;
          reject(s,"ACCEPTANCE_CONFIRM_FAILED",b.closeTs);
          continue;
        }
        s.acceptanceConfirmTs=b.closeTs;
        s.acceptanceConfirm5Ord=b.activeOrd;
        s.state="failed_auction";
        counts.acceptance_confirmed++;
        continue;
      }

      if(s.state==="failed_auction"){
        if(!b.active||b.activeOrd<=s.acceptanceConfirm5Ord)continue;
        s.failureBarsSeen++;
        s.excursionHigh=Math.max(s.excursionHigh,b.h);
        s.excursionLow=Math.min(s.excursionLow,b.l);
        const backInside=s.tradeDirection==="SHORT"?b.c<s.levelPrice:b.c>s.levelPrice;
        if(backInside&&bodyPass(b,s.tradeDirection)){
          s.failedAuctionTs=b.closeTs;
          s.failedAuction5Ord=b.activeOrd;
          s.failureBarOpen=b.o;s.failureBarHigh=b.h;s.failureBarLow=b.l;s.failureBarClose=b.c;
          s.entry=s.levelPrice;
          s.stop=s.tradeDirection==="SHORT"?s.excursionHigh+1:s.excursionLow-1;
          if((s.tradeDirection==="SHORT"&&!(s.entry<s.stop))||(s.tradeDirection==="LONG"&&!(s.stop<s.entry))){
            reject(s,"INVALID_STOP_GEOMETRY",b.closeTs);continue;
          }
          s.stopDistanceTicks=Math.abs(s.entry-s.stop);
          s.grossStopUSD=s.stopDistanceTicks*TICK_USD_010;
          if(s.stopDistanceTicks>4000){
            reject(s,"STRUCTURAL_RISK_ABOVE_40",b.closeTs);continue;
          }
          s.state="entry";
          s.entryBarsSeen=0;
          counts.qualifying_failed_auctions++;
          continue;
        }
        if(s.failureBarsSeen>=6){
          counts.failed_auction_timeout_6++;
          reject(s,"FAILED_AUCTION_TIMEOUT_6",b.closeTs);
        }
      }
    }
  }

  function acceptCandidate(s,m){
    const c={
      id:"T-C"+(++candidateSeq),setupId:s.id,
      direction:s.tradeDirection,
      breakoutDirection:s.breakoutDirection,
      levelClass:s.levelClass,levelSide:s.levelSide,levelPrice:s.levelPrice,levelKnownTs:s.levelKnownTs,
      attackStartTs:s.attackStartTs,attackCloseTs:s.attackCloseTs,
      acceptanceConfirmTs:s.acceptanceConfirmTs,
      failedAuctionTs:s.failedAuctionTs,
      fillBarStartTs:m.ts,fillSignalTs:m.ts+MIN,
      failureBarsSeen:s.failureBarsSeen,
      entry:s.entry,stop:s.stop,
      stopDistanceTicks:s.stopDistanceTicks,grossStopUSD:s.grossStopUSD,
      excursionHigh:s.excursionHigh,excursionLow:s.excursionLow,
      causality:{
        level_known_before_attack:s.levelKnownTs<=s.attackStartTs,
        acceptance_after_attack:s.acceptanceConfirmTs>s.attackCloseTs,
        failed_auction_after_acceptance:s.failedAuctionTs>s.acceptanceConfirmTs,
        fill_after_failed_auction:(m.ts+MIN)>s.failedAuctionTs
      }
    };
    accepted.push(c);
    counts.boundary_retest_fills++;
    s.state="done";s.candidateId=c.id;s.fillTs=m.ts+MIN;
  }

  function processM1(m){
    const ct=m.ts+MIN;
    for(const s of pending){
      if(s.state!=="entry")continue;
      if(ct<=s.failedAuctionTs)continue;
      if(minsUTC(ct)>=18*60){reject(s,"ENTRY_WINDOW_CLOSED_1800",ct);continue;}
      s.entryBarsSeen++;
      const stopHit=s.tradeDirection==="SHORT"?m.h>=s.stop:m.l<=s.stop;
      if(stopHit){reject(s,"PREENTRY_STRUCTURAL_INVALIDATION",ct);continue;}
      const fill=s.tradeDirection==="SHORT"?m.h>=s.entry:m.l<=s.entry;
      if(fill){acceptCandidate(s,m);continue;}
      if(s.entryBarsSeen>=15)reject(s,"ENTRY_TIMEOUT_15",ct);
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
    for(const x of hi.concat(lo))inc(attackByLevel,x.cls);

    const setupWindow=weekday(b.startTs)&&minsUTC(b.closeTs)>=360&&minsUTC(b.closeTs)<1020&&inSplit(b.closeTs);
    if(!setupWindow){counts.attacks_consumed_outside_setup_window++;return;}
    if(hi.length&&lo.length){counts.dual_sided_attack_ambiguous++;return;}

    const arr=hi.length?hi:lo;
    arr.sort((a,b)=>a.priority-b.priority||a.cls.localeCompare(b.cls));
    const level=arr[0];
    if(level.side==="HIGH"){
      if(b.c>level.price)createSetup(b,level,"LONG");
      else counts.attack_immediate_rejection_ignored++;
    }else{
      if(b.c<level.price)createSetup(b,level,"SHORT");
      else counts.attack_immediate_rejection_ignored++;
    }
  }

  for(const m of rows){
    if(m.active)processM1(m);
    const b=bar5ByClose.get(m.ts+MIN);
    if(b){
      if(b.active&&inSplit(b.closeTs))counts.market_active_5m++;
      process5mState(b);
      processAttacks5m(b);
    }
  }

  for(const s of pending)if(s.state!=="done")reject(s,"DATA_END_PENDING",rows[rows.length-1].ts+MIN);

  const byDirection={},byLevel={},dayCounts={};
  for(const c of accepted){
    inc(byDirection,c.direction);inc(byLevel,c.levelClass);inc(dayCounts,utcDate(c.fillSignalTs-1));
  }
  const activeDays=Object.keys(dayCounts).sort();
  const perActiveDay=activeDays.map(d=>dayCounts[d]);
  const causal=accepted.every(c=>
    c.causality.level_known_before_attack&&
    c.causality.acceptance_after_attack&&
    c.causality.failed_auction_after_acceptance&&
    c.causality.fill_after_failed_auction
  );
  const gates={
    accepted_candidates_ge_100:accepted.length>=100,
    long_candidates_ge_25:(byDirection.LONG||0)>=25,
    short_candidates_ge_25:(byDirection.SHORT||0)>=25,
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
    experiment:"EXP-046",
    engine:"Engine T v0.1",
    stage:"zero_outcome_development_preflight",
    split:{start:new Date(splitStart).toISOString(),end_exclusive:new Date(splitEnd).toISOString()},
    source_rows:rows.length,
    market_active_m1:rows.filter(x=>x.active).length,
    counts,
    attacks_by_level:attackByLevel,
    setup_count:setups.filter(s=>inSplit(s.attackCloseTs)).length,
    terminal_reasons:terminalReasons,
    accepted_filled_candidates:accepted.length,
    accepted_by_direction:byDirection,
    accepted_by_level:byLevel,
    accepted_signal_days:activeDays.length,
    accepted_candidates_per_active_day:{distribution:dist(perActiveDay),by_date:dayCounts},
    stop_distance_ticks:dist(accepted.map(x=>x.stopDistanceTicks)),
    gross_stop_usd:dist(accepted.map(x=>x.grossStopUSD)),
    failure_wait_active_m5_bars:dist(accepted.map(x=>x.failureBarsSeen)),
    causality_all_candidates_pass:causal,
    preflight_gates:gates,
    preflight_pass:pass,
    disposition:pass?"EXP046_ZERO_OUTCOME_PREFLIGHT_PASS":"EXP046_ZERO_OUTCOME_PREFLIGHT_FAIL",
    validation_or_holdout_loaded:false,
    target_labels_calculated:false,
    mfe_mae_calculated:false,
    pnl_calculated:false,
    win_rate_calculated:false,
    post_entry_path_evaluated:false,
    accepted_candidates:accepted,
    setups:setups.filter(s=>inSplit(s.attackCloseTs))
  };
}

function selfTest(){
  assert(parseTick("2062.688")===2062688,"tick_parse");
  let threw=false;try{parseTick("1.2345");}catch(e){threw=true;}assert(threw,"off_grid");
  assert(bodyPassForTest({o:115,h:120,l:90,c:95},"SHORT"),"body_short");
  assert(bodyPassForTest({o:85,h:110,l:80,c:105},"LONG"),"body_long");
  return{ok:true,tests:["tick_parse","off_grid","failed_auction_body_short","failed_auction_body_long"]};
}
function bodyPassForTest(b,dir){
  const range=b.h-b.l,body=Math.abs(b.c-b.o);
  if(range<=0||2*body<range)return false;
  return dir==="SHORT"?b.c<b.o:b.c>b.o;
}

root.EngineTv01={runEngineT,selfTest,parseTick};
})(globalThis);
