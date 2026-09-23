/* Engine J v0.1 frozen implementation.
 * Governed by strategies/engine-j-volatility-compression-breakout/SPEC-v0.1.md
 */
(function(root){
"use strict";

const MIN=60000, TICK_USD=0.01;
const ENGINE_ID="engine-j-volatility-compression-breakout";
const ENGINE_VERSION="0.1";
const SYMBOL="XAUUSD";
const SOURCE_COMMIT="922f83a60cc574e7395fb27397077288055a1ef6";

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

function previous30SameDay(active5,b){
  if(active5.length<30)return null;
  const prev=active5.slice(-30);
  const ds=dayStart(b.closeTs);
  if(prev.some(x=>x.startTs<ds||x.closeTs>b.startTs))return null;
  return prev;
}

function compressionStats(prev30){
  assert(prev30.length===30,"need_30_bars");
  const base=prev30.slice(0,24),comp=prev30.slice(24);
  const ranges=base.map(x=>x.h-x.l).sort((a,b)=>a-b);
  const medianNum=ranges[11]+ranges[12];
  const compSum=comp.reduce((s,x)=>s+(x.h-x.l),0);
  const boxHigh=Math.max(...comp.map(x=>x.h));
  const boxLow=Math.min(...comp.map(x=>x.l));
  const boxWidth=boxHigh-boxLow;
  return{
    medianNum,compSum,boxHigh,boxLow,boxWidth,
    compressionAveragePass:medianNum>0&&5*compSum<=12*medianNum,
    compactBoxPass:medianNum>0&&boxWidth>0&&2*boxWidth<=3*medianNum
  };
}

function breakoutDecision(b,s){
  const R=b.h-b.l,BODY=Math.abs(b.c-b.o);
  let dir=null;
  if(b.c>s.boxHigh)dir="LONG";
  else if(b.c<s.boxLow)dir="SHORT";
  if(!dir)return{ok:false,reason:"breakout_close_not_beyond_box",dir:null,R,BODY};

  if((dir==="LONG"&&b.o>s.boxHigh)||(dir==="SHORT"&&b.o<s.boxLow))
    return{ok:false,reason:"breakout_open_already_outside_box",dir,R,BODY};

  if(8*R<5*s.medianNum)
    return{ok:false,reason:"breakout_range_below_1_25_median",dir,R,BODY};

  if(5*BODY<3*R)
    return{ok:false,reason:"body_below_60pct",dir,R,BODY};

  if((dir==="LONG"&&4*(b.h-b.c)>R)||(dir==="SHORT"&&4*(b.c-b.l)>R))
    return{ok:false,reason:"weak_close_location",dir,R,BODY};

  return{ok:true,reason:null,dir,R,BODY};
}

function structuralStop(dir,b,entry){
  const stop=dir==="LONG"?b.l-1:b.h+1;
  const valid=dir==="LONG"?stop<entry:entry<stop;
  return{stop,valid,stopDist:Math.abs(entry-stop)};
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
  const v=a.filter(x=>Number.isFinite(x));
  if(!v.length)return{n:0,mean:null,median:null,p10:null,p90:null,min:null,max:null};
  return{n:v.length,mean:v.reduce((x,y)=>x+y,0)/v.length,median:pctile(v,.5),p10:pctile(v,.1),p90:pctile(v,.9),min:Math.min(...v),max:Math.max(...v)};
}
function inc(o,k,n=1){o[k]=(o[k]||0)+n;}

function eligibleDates(start,end){
  const out=[];
  for(let ts=dayStart(start);ts<end;ts+=24*60*MIN)if(eligibleWeekday(ts))out.push(utcDate(ts));
  return out;
}

function summarizePeriod(setups,trades,start,end){
  const ss=setups.filter(s=>s.candidateTs>=start&&s.candidateTs<end);
  const tt=trades.filter(t=>t.breakoutTs>=start&&t.breakoutTs<end);
  const reasons={};for(const s of ss)if(s.terminal)inc(reasons,s.terminal);
  const exits={};for(const t of tt)inc(exits,t.exitReason);
  const labels={};
  for(const d of[3000,4000,5000,7000,10000]){
    const a=tt.map(t=>t.labels[d]);
    labels[d]={
      target:a.filter(x=>x==="target_before_stop").length,
      stop:a.filter(x=>x==="stop_before_target").length,
      horizon:a.filter(x=>x==="horizon_without_target_or_stop").length,
      n:a.length
    };
  }

  const dates=eligibleDates(start,end),daily={};for(const d of dates)daily[d]=0;
  for(const t of tt){const d=utcDate(t.fillTs);if(daily[d]!==undefined)daily[d]+=t.netUSD500;}
  const dv=dates.map(d=>daily[d]);

  function avg(field){return tt.length?tt.reduce((s,t)=>s+t[field],0)/tt.length:null;}
  function pf(field){
    let p=0,n=0;
    for(const t of tt){const x=t[field];if(x>0)p+=x;else if(x<0)n-=x;}
    return n?p/n:(p>0?Infinity:null);
  }
  let eq=500,peak=500,mdd=0;
  for(const t of [...tt].sort((a,b)=>a.fillTs-b.fillTs)){
    eq+=t.netUSD500;peak=Math.max(peak,eq);mdd=Math.max(mdd,peak-eq);
  }
  let bestN=0,bestLoss=0,curN=0,curLoss=0;
  for(const t of [...tt].sort((a,b)=>a.fillTs-b.fillTs)){
    if(t.netUSD500<0){
      curN++;curLoss+=t.netUSD500;
      if(curN>bestN||(curN===bestN&&curLoss<bestLoss)){bestN=curN;bestLoss=curLoss;}
    }else{curN=0;curLoss=0;}
  }
  function consec(pred){let b=0,c=0;for(const x of dv){if(pred(x)){c++;b=Math.max(b,c);}else c=0;}return b;}

  const total=tt.reduce((s,t)=>s+t.netUSD500,0),direction={};
  for(const t of tt){
    if(!direction[t.dir])direction[t.dir]={n:0,netUSD500:0};
    direction[t.dir].n++;direction[t.dir].netUSD500+=t.netUSD500;
  }

  const eventCounts={
    eligible_weekdays:dates.length,
    active_5m_eligible_weekday:ss.length,
    breakout_window_candidates:ss.filter(s=>s.windowCandidate).length,
    same_day_30_history:ss.filter(s=>s.historyOk).length,
    positive_baseline:ss.filter(s=>s.baselinePositive).length,
    compression_average_pass:ss.filter(s=>s.compressionAveragePass).length,
    compact_box_pass:ss.filter(s=>s.compactBoxPass).length,
    qualifying_breakouts:ss.filter(s=>s.qualifyingBreakout).length,
    qualifying_long_breakouts:ss.filter(s=>s.qualifyingBreakout&&s.dir==="LONG").length,
    qualifying_short_breakouts:ss.filter(s=>s.qualifyingBreakout&&s.dir==="SHORT").length,
    accepted_filled_trades:tt.length
  };

  return{
    split:{start:new Date(start).toISOString(),end_exclusive:new Date(end).toISOString()},
    event_counts:eventCounts,setup_count:ss.length,terminal_reasons:reasons,
    accepted_filled_trades:tt.length,exits,
    target_hit_rate:tt.length?(exits.exit_t40||0)/tt.length:null,
    stop_rate:tt.length?((exits.exit_stop||0)+(exits.exit_stop_entry_bar||0))/tt.length:null,
    timeout_rate:tt.length?((exits.exit_timeout_120||0)+(exits.exit_session_2000||0)+(exits.exit_data_end||0))/tt.length:null,
    label_rates:labels,
    expectancy:{gross_usd:avg("grossUSD"),net_usd_0:avg("netUSD0"),net_usd_025:avg("netUSD250"),net_usd_050:avg("netUSD500")},
    profit_factor:{gross:pf("grossUSD"),net_0:pf("netUSD0"),net_025:pf("netUSD250"),net_050:pf("netUSD500")},
    total_net_usd_050:total,
    daily:{
      mean:dv.length?dv.reduce((a,b)=>a+b,0)/dv.length:null,
      median:pctile(dv,.5),
      losing_pct:dv.length?dv.filter(x=>x<0).length/dv.length:null,
      le50_pct:dv.length?dv.filter(x=>x<=50).length/dv.length:null,
      ge100_pct:dv.length?dv.filter(x=>x>=100).length/dv.length:null,
      ge150_pct:dv.length?dv.filter(x=>x>=150).length/dv.length:null,
      ge200_pct:dv.length?dv.filter(x=>x>=200).length/dv.length:null
    },
    max_drawdown_usd:mdd,recovery_factor:mdd>0?total/mdd:null,
    worst_losing_trade_run:{count:bestN,netLoss:bestLoss},
    max_consecutive_losing_weekdays:consec(x=>x<0),
    max_consecutive_le50_weekdays:consec(x=>x<=50),
    stop_distance_ticks:dist(tt.map(t=>t.stopDist)),
    gross_stop_usd:dist(tt.map(t=>t.stopDist*TICK_USD)),
    actual_mfe_ticks:dist(tt.map(t=>t.actualMFE)),
    actual_mae_ticks:dist(tt.map(t=>t.actualMAE)),
    potential_mfe_ticks:dist(tt.map(t=>t.potentialMFE)),
    potential_mae_ticks:dist(tt.map(t=>t.potentialMAE)),
    breakout_range_ticks:dist(tt.map(t=>t.breakoutRange)),
    breakout_body_ticks:dist(tt.map(t=>t.breakoutBody)),
    baseline_median_range_ticks:dist(tt.map(t=>t.baselineMedianNum/2)),
    compression_sum_range_ticks:dist(tt.map(t=>t.compressionSum)),
    compression_avg_range_ticks:dist(tt.map(t=>t.compressionSum/6)),
    compression_box_width_ticks:dist(tt.map(t=>t.boxWidth)),
    direction,
    daily_series:dates.map(d=>({date:d,netUSD500:daily[d]})),
    trades:tt,setups:ss
  };
}

function runEngineJ(months,splitStart,splitEnd){
  const rows=buildRows(months),bars5=buildBars(rows,5);
  const b5End=new Map(bars5.map(b=>[b.closeTs,b]));
  const activeM1=[],active5=[],setups=[],trades=[];
  let pending=[],openTrade=null,shadows=[],setupSeq=0,tradeSeq=0;
  const consumed=new Set();
  const inSplit=ts=>ts>=splitStart&&ts<splitEnd;

  function baseSetup(b){
    const s={
      id:"J-S"+(++setupSeq),seq:setupSeq,
      engineId:ENGINE_ID,engineVersion:ENGINE_VERSION,symbol:SYMBOL,sourceCommit:SOURCE_COMMIT,
      candidateTs:b.closeTs,candidateStartTs:b.startTs,
      breakoutOpen:b.o,breakoutHigh:b.h,breakoutLow:b.l,breakoutClose:b.c,
      windowCandidate:false,historyOk:false,baselinePositive:false,
      compressionAveragePass:false,compactBoxPass:false,qualifyingBreakout:false,
      dir:null,state:"screening",terminal:null,terminalTs:null
    };
    setups.push(s);return s;
  }

  function reject(s,reason,ts){
    if(s.state==="done")return;
    s.state="done";s.terminal=reason;s.terminalTs=ts;
  }

  function createPending(s,b,stats,bd){
    s.state="entry_next";s.dir=bd.dir;s.qualifyingBreakout=true;
    s.breakoutRange=bd.R;s.breakoutBody=bd.BODY;
    s.baselineMedianNum=stats.medianNum;s.compressionSum=stats.compSum;
    s.boxHigh=stats.boxHigh;s.boxLow=stats.boxLow;s.boxWidth=stats.boxWidth;
    s.entryOrd=(activeM1.length?activeM1[activeM1.length-1].activeOrd:-1)+1;
    pending.push(s);
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
    const b={l:s.breakoutLow,h:s.breakoutHigh};
    const g=structuralStop(s.dir,b,m.o);
    if(!g.valid){reject(s,"invalid_entry_stop_geometry",m.ts);return false;}
    if(g.stopDist>4000){reject(s,"structural_risk_above_40",m.ts);return false;}
    s.entry=m.o;s.stop=g.stop;s.stopDist=g.stopDist;
    s.target=s.dir==="LONG"?m.o+4000:m.o-4000;
    return true;
  }

  function fillTrade(s,m){
    const t={
      id:"J-T"+(++tradeSeq),setupId:s.id,
      engineId:ENGINE_ID,engineVersion:ENGINE_VERSION,symbol:SYMBOL,sourceCommit:SOURCE_COMMIT,
      dir:s.dir,breakoutTs:s.candidateTs,breakoutStartTs:s.candidateStartTs,
      breakoutOpen:s.breakoutOpen,breakoutHigh:s.breakoutHigh,breakoutLow:s.breakoutLow,breakoutClose:s.breakoutClose,
      breakoutRange:s.breakoutRange,breakoutBody:s.breakoutBody,
      baselineMedianNum:s.baselineMedianNum,compressionSum:s.compressionSum,
      boxHigh:s.boxHigh,boxLow:s.boxLow,boxWidth:s.boxWidth,
      fillTs:m.ts,fillOrd:m.activeOrd,entry:s.entry,stop:s.stop,target:s.target,stopDist:s.stopDist,
      horizonCount:1,closed:false,shadowDone:false,
      actualMFE:0,actualMAE:0,potentialMFE:0,potentialMAE:0,
      labels:{3000:null,4000:null,5000:null,7000:null,10000:null},labelTimes:{}
    };
    trades.push(t);s.tradeId=t.id;s.state="done";openTrade=t;shadows.push(t);

    for(const other of pending)if(other!==s&&other.state!=="done")reject(other,"suppressed_one_open",m.ts);

    const out=barOutcome(t.dir,m,t.stop,t.target);
    if(out==="stop"){
      t.actualMAE=t.stopDist;t.potentialMAE=t.stopDist;
      for(const k of Object.keys(t.labels))t.labels[k]="stop_before_target";
      t.shadowDone=true;
      closeTrade(t,"exit_stop_entry_bar",t.stop,m.ts+MIN);
      return;
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
      .sort((a,b)=>a.candidateTs-b.candidateTs||a.seq-b.seq);
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

  function on5Close(b){
    if(!b.active)return;

    if(inSplit(b.closeTs)&&eligibleWeekday(b.closeTs)){
      const s=baseSetup(b),mm=minsUTC(b.closeTs);
      if(mm<360||mm>=1080){
        reject(s,"outside_breakout_window",b.closeTs);
        active5.push(b);return;
      }
      s.windowCandidate=true;

      const prev=previous30SameDay(active5,b);
      if(!prev){
        reject(s,"same_day_30_active5_unavailable",b.closeTs);
        active5.push(b);return;
      }
      s.historyOk=true;

      const stats=compressionStats(prev);
      s.baselineMedianNum=stats.medianNum;s.compressionSum=stats.compSum;
      s.boxHigh=stats.boxHigh;s.boxLow=stats.boxLow;s.boxWidth=stats.boxWidth;

      if(stats.medianNum<=0){
        reject(s,"baseline_zero_range",b.closeTs);
        active5.push(b);return;
      }
      s.baselinePositive=true;

      if(stats.boxWidth<=0){
        reject(s,"compression_zero_width",b.closeTs);
        active5.push(b);return;
      }

      if(!stats.compressionAveragePass){
        reject(s,"compression_average_failed",b.closeTs);
        active5.push(b);return;
      }
      s.compressionAveragePass=true;

      if(!stats.compactBoxPass){
        reject(s,"compression_box_too_wide",b.closeTs);
        active5.push(b);return;
      }
      s.compactBoxPass=true;

      const bd=breakoutDecision(b,stats);
      s.dir=bd.dir;s.breakoutRange=bd.R;s.breakoutBody=bd.BODY;
      if(!bd.ok){
        reject(s,bd.reason,b.closeTs);
        active5.push(b);return;
      }

      const key=utcDate(b.closeTs)+"|"+bd.dir;
      if(consumed.has(key)){
        reject(s,"side_already_consumed_today",b.closeTs);
        active5.push(b);return;
      }
      consumed.add(key);
      s.qualifyingBreakout=true;

      if(openTrade)reject(s,"suppressed_one_open",b.closeTs);
      else createPending(s,b,stats,bd);
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

  for(const s of pending){
    if(s.state!=="done")reject(s,"entry_window_closed_1800",rows[rows.length-1].ts+MIN);
  }

  const summary=summarizePeriod(setups,trades,splitStart,splitEnd);
  return{
    source_rows:rows.length,market_active_m1:rows.filter(x=>x.active).length,
    ...summary,
    trades:summary.trades,setups:summary.setups,daily_series:summary.daily_series
  };
}

function bootstrap(metrics,reps=10000,seed=21021){
  const days=metrics.daily_series;
  const byDate=new Map(days.map(x=>[x.date,[]]));
  for(const t of metrics.trades){
    const d=utcDate(t.fillTs);if(byDate.has(d))byDate.get(d).push(t.netUSD500);
  }
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

  const prev=[];
  for(let i=0;i<24;i++)prev.push({h:1100,l:1000,startTs:i*5*MIN,closeTs:(i+1)*5*MIN});
  for(let i=0;i<6;i++)prev.push({h:1080,l:1000,startTs:(24+i)*5*MIN,closeTs:(25+i)*5*MIN});
  const st=compressionStats(prev);
  assert(st.medianNum===200,"baseline_median_num");
  assert(st.compSum===480,"compression_sum");
  assert(5*st.compSum===12*st.medianNum&&st.compressionAveragePass,"compression_equality_pass");
  assert(st.boxWidth===80&&st.compactBoxPass,"compact_box_pass");

  const wider=[...prev.slice(0,24)];
  for(let i=0;i<6;i++)wider.push({h:1301,l:1000,startTs:(24+i)*5*MIN,closeTs:(25+i)*5*MIN});
  const sw=compressionStats(wider);
  assert(!sw.compressionAveragePass,"compression_average_fail");

  const boxBars=[...prev.slice(0,24)];
  boxBars.push({h:1301,l:1000},{h:1080,l:1000},{h:1080,l:1000},{h:1080,l:1000},{h:1080,l:1000},{h:1080,l:1000});
  const sb=compressionStats(boxBars);
  assert(sb.boxWidth===301&&!sb.compactBoxPass,"box_width_fail");

  const stats={medianNum:200,boxHigh:1100,boxLow:900};
  let bd=breakoutDecision({o:1090,h:1240,l:990,c:1220},stats);
  assert(bd.ok&&bd.dir==="LONG","long_breakout");
  bd=breakoutDecision({o:910,h:1010,l:760,c:780},stats);
  assert(bd.ok&&bd.dir==="SHORT","short_breakout");
  bd=breakoutDecision({o:1110,h:1240,l:1000,c:1220},stats);
  assert(!bd.ok&&bd.reason==="breakout_open_already_outside_box","open_outside_reject");
  bd=breakoutDecision({o:1000,h:1100,l:900,c:1000},stats);
  assert(!bd.ok&&bd.reason==="breakout_close_not_beyond_box","close_inside_reject");

  const prior=[];
  const day=Date.UTC(2025,0,6);
  for(let i=0;i<30;i++)prior.push({startTs:day+i*5*MIN,closeTs:day+(i+1)*5*MIN});
  const cb={startTs:day+30*5*MIN,closeTs:day+31*5*MIN};
  const got=previous30SameDay(prior,cb);
  assert(got&&got.length===30&&got[29].closeTs===cb.startTs,"previous30_excludes_candidate");
  const cross=[{startTs:day-MIN,closeTs:day},...prior.slice(1)];
  assert(previous30SameDay(cross,cb)===null,"same_day_strict");

  let g=structuralStop("LONG",{l:1000,h:2000},5001);
  assert(g.valid&&g.stop===999&&g.stopDist===4002,"structural_stop_long");
  g=structuralStop("SHORT",{l:1000,h:2000},-2001);
  assert(g.valid&&g.stop===2001&&g.stopDist===4002,"structural_stop_short");
  assert(Math.abs(5000-1000)===4000,"risk_cap_boundary");
  assert(!(Math.abs(5001-1000)<=4000),"risk_cap_over");

  assert(barOutcome("LONG",{h:120,l:80},90,110)==="stop","same_bar_stop_first");
  assert(barOutcome("LONG",{h:120,l:95},90,110)==="target","target_when_no_stop");

  return{ok:true,tests:[
    "tick_parse","off_grid_reject","baseline_median_num","compression_equality",
    "compression_average_fail","compact_box","box_width_fail","long_breakout","short_breakout",
    "open_outside_reject","close_inside_reject","previous30_excludes_candidate","same_day_strict",
    "structural_stop","risk_cap","same_bar_stop_first"
  ]};
}

root.EngineJv01={
  runEngineJ,bootstrap,summarizePeriod,selfTest,parseTick,
  _test:{previous30SameDay,compressionStats,breakoutDecision,structuralStop,barOutcome}
};
})(globalThis);
