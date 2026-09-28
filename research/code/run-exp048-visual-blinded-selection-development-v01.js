#!/usr/bin/env node
"use strict";

const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
const {execSync}=require("child_process");

const ROOT=path.resolve(__dirname,"../..");
const SOURCE_REPO=path.resolve(process.env.EXP048_SOURCE_REPO||"/tmp/market-data-lab");
const SOURCE_COMMIT="922f83a60cc574e7395fb27397077288055a1ef6";
const LABELS_PATH=path.join(ROOT,"research/results/EXP-048-visual-replay-labels-v0.1.jsonl");
const LABEL_SUMMARY_PATH=path.join(ROOT,"research/results/EXP-048-visual-replay-label-summary-v0.1.json");
const PACKETS_PATH=path.join(ROOT,"research/results/EXP-048-blinded-replay-packets-v0.1.jsonl");
const EXPECTED_LABEL_BLOB="c40a4bb56298d4206ce08ddab2ba9199a45a5732";
const EXPECTED_LABEL_SUMMARY_BLOB="df5254b4f3b542a4595c2a2247de50685f4c2b89";
const EXPECTED_PACKET_BLOB="7ad151791071f86737c31315ae55e8fdfc4800c8";
const PROTOCOL_COMMIT="dd9d1a4a7ad68845c7feea757ec4b505d27cbe48";
const MIN=60000;
const START=Date.UTC(2022,0,1), END=Date.UTC(2025,2,1);

function assert(c,m){if(!c)throw new Error(m);}
function sha256(buf){return crypto.createHash("sha256").update(buf).digest("hex");}
function gitBlobSha(buf){
  const h=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(Buffer.concat([h,buf])).digest("hex");
}
function dateStr(ts){return new Date(ts).toISOString().slice(0,10);}
function parseTickText(s){
  const m=/^([0-9]+)(?:\.([0-9]+))?$/.exec(String(s).trim());
  if(!m)throw new Error("bad_price:"+s);
  let f=m[2]||"";
  if(f.length>3){const rest=f.slice(3);if(!/^0*$/.test(rest))throw new Error("off_grid:"+s);f=f.slice(0,3);}
  return Number(m[1])*1000+Number(f.padEnd(3,"0"));
}
function priceToTick(x){
  assert(Number.isFinite(x)&&x>0,"invalid_label_price:"+x);
  const t=Math.round(x*1000);
  assert(Math.abs(t/1000-x)<1e-9,"label_price_off_grid:"+x);
  return t;
}
function expectedRows(y,m){return new Date(Date.UTC(y,m,0)).getUTCDate()*1440;}
function monthRange(){const out=[];let y=2021,m=12;while(y<2025||(y===2025&&m<=2)){out.push([y,m]);m++;if(m===13){m=1;y++;}}return out;}
function percentile(xs,p){
  if(!xs.length)return null;
  const a=[...xs].sort((x,y)=>x-y),pos=(a.length-1)*p,lo=Math.floor(pos),hi=Math.ceil(pos);
  return lo===hi?a[lo]:a[lo]+(a[hi]-a[lo])*(pos-lo);
}
function dist(xs){
  if(!xs.length)return{n:0,mean:null,median:null,p10:null,p90:null,min:null,max:null};
  return{n:xs.length,mean:xs.reduce((a,b)=>a+b,0)/xs.length,median:percentile(xs,.5),
    p10:percentile(xs,.1),p90:percentile(xs,.9),min:Math.min(...xs),max:Math.max(...xs)};
}
function pf(xs){
  const pos=xs.filter(x=>x>0).reduce((a,b)=>a+b,0);
  const neg=-xs.filter(x=>x<0).reduce((a,b)=>a+b,0);
  return neg>0?pos/neg:(pos>0?Infinity:null);
}
function inc(o,k,n=1){o[k]=(o[k]||0)+n;}
function lowerBound(rows,ts){
  let lo=0,hi=rows.length;
  while(lo<hi){const mid=(lo+hi)>>1;if(rows[mid].ts<ts)lo=mid+1;else hi=mid;}
  return lo;
}
function loadRows(){
  const head=execSync("git rev-parse HEAD",{cwd:SOURCE_REPO,encoding:"utf8"}).trim();
  assert(head===SOURCE_COMMIT,"source_commit_mismatch:"+head);
  assert(execSync("git status --porcelain",{cwd:SOURCE_REPO,encoding:"utf8"}).trim()==="","source_dirty");
  const rows=[],verified=[];let prevTs=null,prevClose=null,ord=0;
  for(const ym of monthRange()){
    const y=ym[0],m=ym[1],mm=String(m).padStart(2,"0");
    const name="xauusd_bid_m1_"+y+"_"+mm+".csv";
    const rel="xauusd/bid/m1/"+name,p=path.join(SOURCE_REPO,rel),buf=fs.readFileSync(p);
    const tree=execSync("git ls-tree "+SOURCE_COMMIT+" -- "+rel,{cwd:SOURCE_REPO,encoding:"utf8"}).trim();
    const mt=/^\d+ blob ([0-9a-f]{40})\t/.exec(tree);assert(mt,"source_tree_missing:"+name);
    assert(gitBlobSha(buf)===mt[1],"source_blob_mismatch:"+name);
    const lines=buf.toString("utf8").trimEnd().split("\n");
    assert(lines[0].trim()==="timestamp,open,high,low,close","bad_header:"+name);
    assert(lines.length===expectedRows(y,m)+1,"bad_row_count:"+name);
    for(let i=1;i<lines.length;i++){
      const q=lines[i].trim().split(",");assert(q.length===5,"bad_cols:"+name+":"+i);
      const ts=Number(q[0]);assert(Number.isInteger(ts)&&ts%MIN===0,"bad_ts:"+name+":"+i);
      if(prevTs!==null)assert(ts-prevTs===MIN,"gap:"+name+":"+i);
      const o=parseTickText(q[1]),h=parseTickText(q[2]),l=parseTickText(q[3]),c=parseTickText(q[4]);
      assert(h>=o&&h>=c&&l<=o&&l<=c&&h>=l,"bad_ohlc:"+name+":"+i);
      const carry=prevClose!==null&&o===h&&h===l&&l===c&&c===prevClose;
      rows.push({ts,o,h,l,c,active:!carry,activeOrd:carry?-1:ord++});
      prevTs=ts;prevClose=c;
    }
    verified.push({name,git_blob_sha:mt[1],bytes:buf.length,sha256:sha256(buf)});
  }
  return{rows,verified,head};
}
function loadFrozen(){
  const lb=fs.readFileSync(LABELS_PATH),sb=fs.readFileSync(LABEL_SUMMARY_PATH),pb=fs.readFileSync(PACKETS_PATH);
  assert(gitBlobSha(lb)===EXPECTED_LABEL_BLOB,"labels_blob_changed");
  assert(gitBlobSha(sb)===EXPECTED_LABEL_SUMMARY_BLOB,"label_summary_blob_changed");
  assert(gitBlobSha(pb)===EXPECTED_PACKET_BLOB,"packets_blob_changed");
  const summary=JSON.parse(sb.toString("utf8"));
  assert(summary.feasibility_pass===true,"label_gate_not_passed");
  assert(summary.post_decision_path_loaded===false&&summary.target_outcomes_evaluated===false&&summary.pnl_calculated===false,"outcome_already_loaded");
  const labels=lb.toString("utf8").trim().split("\n").filter(Boolean).map(JSON.parse);
  const packets=pb.toString("utf8").trim().split("\n").filter(Boolean).map(JSON.parse);
  assert(labels.length===126&&packets.length===126,"frozen_count_changed");
  return{labels,packetMap:new Map(packets.map(x=>[x.replayId,x]))};
}
function makeOrder(label,packet){
  assert(packet,"packet_missing:"+label.replayId);
  return{
    replayId:label.replayId,decision:label.decision,confidence:label.confidence||null,entryStyle:label.entryStyle||null,
    referenceEntryTick:label.entryPrice==null?null:priceToTick(label.entryPrice),
    stopTick:label.stopPrice==null?null:priceToTick(label.stopPrice),
    tpTick:label.tp1Price==null?null:priceToTick(label.tp1Price),
    decisionTs:packet.decisionTs,era:packet.era,eventDate:packet.eventDate
  };
}
function resolveFill(order,rows){
  if(order.decision==="NO_TRADE")return{filled:false,reason:"NO_TRADE_LABEL"};
  const dir=order.decision,cutoff=Date.parse(order.eventDate+"T18:00:00Z");
  let idx=lowerBound(rows,order.decisionTs);
  if(order.entryStyle==="MARKET_NEXT_OPEN"){
    while(idx<rows.length){
      const r=rows[idx++];
      if(r.ts>=cutoff||dateStr(r.ts)!==order.eventDate)return{filled:false,reason:"NO_FILL_MARKET_AFTER_1800"};
      if(!r.active)continue;
      const entry=r.o,stop=order.stopTick,tp=order.tpTick;
      const geom=dir==="LONG"?(stop<entry&&entry<tp):(tp<entry&&entry<stop);
      if(!geom)return{filled:false,reason:"NO_FILL_MARKET_INVALID_GEOMETRY"};
      return{filled:true,entryTick:entry,fillTs:r.ts,scanStartIndex:idx-1,includeFillBar:true};
    }
    return{filled:false,reason:"NO_FILL_DATA_END"};
  }
  assert(order.entryStyle==="LEVEL_RETEST","unexpected_entry_style:"+order.replayId+":"+order.entryStyle);
  let activeSeen=0;
  while(idx<rows.length&&activeSeen<60){
    const r=rows[idx++];
    if(r.ts>=cutoff||dateStr(r.ts)!==order.eventDate)return{filled:false,reason:"NO_FILL_RETEST_EXPIRED"};
    if(!r.active)continue;
    activeSeen++;
    const stopHit=dir==="LONG"?r.l<=order.stopTick:r.h>=order.stopTick;
    if(stopHit)return{filled:false,reason:"NO_FILL_PREENTRY_INVALIDATION"};
    const touch=dir==="LONG"?r.l<=order.referenceEntryTick:r.h>=order.referenceEntryTick;
    if(touch){
      const entry=order.referenceEntryTick,stop=order.stopTick,tp=order.tpTick;
      const geom=dir==="LONG"?(stop<entry&&entry<tp):(tp<entry&&entry<stop);
      if(!geom)return{filled:false,reason:"NO_FILL_RETEST_INVALID_GEOMETRY"};
      return{filled:true,entryTick:entry,fillTs:r.ts+MIN,scanStartIndex:idx,includeFillBar:false,waitActiveM1:activeSeen};
    }
  }
  return{filled:false,reason:"NO_FILL_RETEST_EXPIRED"};
}
function simulate(order,fill,rows){
  const dir=order.decision,sign=dir==="LONG"?1:-1,entry=fill.entryTick,stop=order.stopTick,tp=order.tpTick;
  const riskTicks=Math.abs(entry-stop);assert(riskTicks>0,"zero_risk:"+order.replayId);
  const cutoff=Date.parse(dateStr(fill.fillTs)+"T20:00:00Z");
  let idx=fill.scanStartIndex,active=0,last=null,outcome=null,exitTick=null,exitTs=null;
  while(idx<rows.length&&active<120){
    const r=rows[idx++];
    if(r.ts>=cutoff||dateStr(r.ts)!==dateStr(fill.fillTs))break;
    if(!r.active)continue;
    active++;last=r;
    const stopHit=dir==="LONG"?r.l<=stop:r.h>=stop;
    const tpHit=dir==="LONG"?r.h>=tp:r.l<=tp;
    if(stopHit){outcome="STOP";exitTick=stop;exitTs=r.ts+MIN;break;}
    if(tpHit){outcome="TP1";exitTick=tp;exitTs=r.ts+MIN;break;}
  }
  if(outcome===null){
    if(last){outcome="TIMEOUT";exitTick=last.c;exitTs=Math.min(last.ts+MIN,cutoff);}
    else{outcome="TIMEOUT";exitTick=entry;exitTs=fill.fillTs;}
  }
  const grossTicks=sign*(exitTick-entry),grossUsd010=grossTicks*0.01,riskUsd010=riskTicks*0.01;
  return{
    replayId:order.replayId,direction:dir,confidence:order.confidence,entryStyle:order.entryStyle,
    era:order.era,eventDate:order.eventDate,decisionTs:order.decisionTs,fillTs:fill.fillTs,
    entryTick:entry,stopTick:stop,tpTick:tp,riskTicks,riskUsd010,waitActiveM1:fill.waitActiveM1||0,
    outcome,exitTs,exitTick,activeM1Bars:active,grossUsd010,
    primaryUsd010:grossUsd010-5,stressUsd010:grossUsd010-10,
    grossR:grossUsd010/riskUsd010,primaryR:(grossUsd010-5)/riskUsd010,stressR:(grossUsd010-10)/riskUsd010
  };
}
function safeLot(t){
  for(let n=10;n>=1;n--){const lot=n/100,scale=lot/0.10;if(t.riskUsd010*scale+100*lot<=40+1e-9)return lot;}
  return 0;
}
function scaledTrade(t,lot){const scale=lot/0.10,gross=t.grossUsd010*scale;return{...t,lot,grossUSD:gross,primaryUSD:gross-50*lot,stressUSD:gross-100*lot};}
function maxDrawdown(xs){let eq=0,peak=0,mdd=0;for(const x of xs){eq+=x;peak=Math.max(peak,eq);mdd=Math.max(mdd,peak-eq);}return mdd;}
function consecutive(flags){let best=0,cur=0;for(const x of flags){cur=x?cur+1:0;best=Math.max(best,cur);}return best;}
function allWeekdays(){const out=[];for(let t=START;t<END;t+=86400000){const w=new Date(t).getUTCDay();if(w>=1&&w<=5)out.push(dateStr(t));}return out;}
function portfolio(signals){
  const candidates=signals.map(t=>({...t,safeLot:safeLot(t)})).filter(t=>t.safeLot>=0.01);
  candidates.sort((a,b)=>a.fillTs-b.fillTs||
    ({"A":0,"B":1,"C":2}[a.confidence]-({"A":0,"B":1,"C":2}[b.confidence]))||
    a.riskUsd010-b.riskUsd010||a.replayId.localeCompare(b.replayId));
  let busy=-Infinity,blockedOpen=0,blockedDay=0;const trades=[],dailyRealized={};
  for(const t of candidates){
    if(t.fillTs<busy){blockedOpen++;continue;}
    const d=dateStr(t.fillTs),real=dailyRealized[d]||0;
    if(real<=-40||real>=150){blockedDay++;continue;}
    const q=scaledTrade(t,t.safeLot);trades.push(q);busy=q.exitTs;dailyRealized[d]=(dailyRealized[d]||0)+q.primaryUSD;
  }
  const weekdays=allWeekdays(),pd=Object.fromEntries(weekdays.map(d=>[d,0])),sd=Object.fromEntries(weekdays.map(d=>[d,0]));
  for(const t of trades){const d=dateStr(t.fillTs);pd[d]+=t.primaryUSD;sd[d]+=t.stressUSD;}
  const pDaily=weekdays.map(d=>pd[d]),sDaily=weekdays.map(d=>sd[d]);
  const rolling=[];for(let i=4;i<pDaily.length;i++)rolling.push(pDaily.slice(i-4,i+1).reduce((a,b)=>a+b,0));
  const pvals=trades.map(x=>x.primaryUSD),svals=trades.map(x=>x.stressUSD);
  return{
    actual_trades:trades.length,blocked_due_one_open:blockedOpen,blocked_due_daily_state:blockedDay,
    distinct_trade_weekdays:new Set(trades.map(x=>dateStr(x.fillTs))).size,lot:dist(trades.map(x=>x.lot)),
    primary_expectancy_usd:trades.length?pvals.reduce((a,b)=>a+b,0)/trades.length:null,
    stress_expectancy_usd:trades.length?svals.reduce((a,b)=>a+b,0)/trades.length:null,
    primary_profit_factor:pf(pvals),stress_profit_factor:pf(svals),
    total_primary_pnl_usd:pvals.reduce((a,b)=>a+b,0),total_stress_pnl_usd:svals.reduce((a,b)=>a+b,0),
    primary_max_drawdown_usd:maxDrawdown(pvals),stress_max_drawdown_usd:maxDrawdown(svals),
    all_development_weekdays:weekdays.length,trades_per_all_weekday:trades.length/weekdays.length,
    primary_daily:{
      mean:pDaily.reduce((a,b)=>a+b,0)/pDaily.length,median:percentile(pDaily,.5),
      losing_pct:pDaily.filter(x=>x<0).length/pDaily.length,le_50_pct:pDaily.filter(x=>x<=50).length/pDaily.length,
      ge_100_pct:pDaily.filter(x=>x>=100).length/pDaily.length,ge_150_pct:pDaily.filter(x=>x>=150).length/pDaily.length,
      ge_200_pct:pDaily.filter(x=>x>=200).length/pDaily.length,
      max_consecutive_losing_days:consecutive(pDaily.map(x=>x<0)),rolling_5day:dist(rolling)
    },trades
  };
}
function signalMetrics(xs){
  const gross=xs.map(x=>x.grossR),primary=xs.map(x=>x.primaryR),stress=xs.map(x=>x.stressR),eras={},directions={},confidence={};
  for(const era of ["ERA1","ERA2","ERA3"]){const q=xs.filter(x=>x.era===era);eras[era]={n:q.length,stress_r_expectancy:q.length?q.reduce((s,x)=>s+x.stressR,0)/q.length:null,primary_r_expectancy:q.length?q.reduce((s,x)=>s+x.primaryR,0)/q.length:null};}
  for(const d of ["LONG","SHORT"]){const q=xs.filter(x=>x.direction===d);directions[d]={n:q.length,stress_r_expectancy:q.length?q.reduce((s,x)=>s+x.stressR,0)/q.length:null,primary_r_expectancy:q.length?q.reduce((s,x)=>s+x.primaryR,0)/q.length:null};}
  for(const c of ["A","B"]){const q=xs.filter(x=>x.confidence===c);confidence[c]={n:q.length,stress_r_expectancy:q.length?q.reduce((s,x)=>s+x.stressR,0)/q.length:null,primary_r_expectancy:q.length?q.reduce((s,x)=>s+x.primaryR,0)/q.length:null};}
  return{
    n:xs.length,by_direction:Object.fromEntries(["LONG","SHORT"].map(d=>[d,xs.filter(x=>x.direction===d).length])),
    by_confidence:Object.fromEntries(["A","B"].map(c=>[c,xs.filter(x=>x.confidence===c).length])),
    outcomes:Object.fromEntries([...new Set(xs.map(x=>x.outcome))].sort().map(k=>[k,xs.filter(x=>x.outcome===k).length])),
    risk_usd_at_010:dist(xs.map(x=>x.riskUsd010)),
    gross_r_expectancy:xs.length?gross.reduce((a,b)=>a+b,0)/xs.length:null,
    primary_r_expectancy:xs.length?primary.reduce((a,b)=>a+b,0)/xs.length:null,
    stress_r_expectancy:xs.length?stress.reduce((a,b)=>a+b,0)/xs.length:null,
    primary_r_profit_factor:pf(primary),stress_r_profit_factor:pf(stress),eras,directions,confidence_descriptive:confidence
  };
}
function developmentGate(sm,pm){
  const positiveEras=Object.values(sm.eras).filter(x=>x.stress_r_expectancy!==null&&x.stress_r_expectancy>0).length;
  const g={
    filled_signals_ge_30:sm.n>=30,reference_trades_ge_25:pm.actual_trades>=25,distinct_trade_weekdays_ge_20:pm.distinct_trade_weekdays>=20,
    gross_r_expectancy_gt_0_20:sm.gross_r_expectancy!==null&&sm.gross_r_expectancy>0.20,
    primary_r_expectancy_gt_0:sm.primary_r_expectancy!==null&&sm.primary_r_expectancy>0,
    stress_r_expectancy_gt_0:sm.stress_r_expectancy!==null&&sm.stress_r_expectancy>0,
    primary_r_pf_ge_1_10:sm.primary_r_profit_factor!==null&&sm.primary_r_profit_factor>=1.10,
    stress_r_pf_ge_1_05:sm.stress_r_profit_factor!==null&&sm.stress_r_profit_factor>=1.05,
    positive_stress_eras_ge_2:positiveEras>=2,
    long_stress_r_expectancy_gt_0:sm.directions.LONG.n>0&&sm.directions.LONG.stress_r_expectancy>0,
    short_stress_r_expectancy_gt_0:sm.directions.SHORT.n>0&&sm.directions.SHORT.stress_r_expectancy>0,
    reference_primary_expectancy_gt_0:pm.primary_expectancy_usd!==null&&pm.primary_expectancy_usd>0,
    reference_stress_expectancy_gt_0:pm.stress_expectancy_usd!==null&&pm.stress_expectancy_usd>0,
    reference_primary_pf_ge_1_10:pm.primary_profit_factor!==null&&pm.primary_profit_factor>=1.10,
    reference_stress_pf_ge_1_05:pm.stress_profit_factor!==null&&pm.stress_profit_factor>=1.05,
    stress_mdd_le_150:pm.stress_max_drawdown_usd<=150,protected_periods_sealed:true
  };
  g.pass=Object.values(g).every(Boolean);return g;
}
function main(){
  const frozen=loadFrozen(),labels=frozen.labels,packetMap=frozen.packetMap,{rows,verified,head}=loadRows();
  const orders=labels.map(x=>makeOrder(x,packetMap.get(x.replayId))),noTrade=orders.filter(x=>x.decision==="NO_TRADE"),tradeOrders=orders.filter(x=>x.decision!=="NO_TRADE");
  assert(noTrade.length===75&&tradeOrders.length===51,"frozen_decision_counts_changed");
  const noFillReasons={},filled=[],orderAudit=[];
  for(const o of tradeOrders){
    const fill=resolveFill(o,rows);
    if(!fill.filled){inc(noFillReasons,fill.reason);orderAudit.push({replayId:o.replayId,decision:o.decision,confidence:o.confidence,entryStyle:o.entryStyle,decisionTs:o.decisionTs,filled:false,reason:fill.reason});continue;}
    const t=simulate(o,fill,rows);filled.push(t);
    orderAudit.push({replayId:o.replayId,decision:o.decision,confidence:o.confidence,entryStyle:o.entryStyle,decisionTs:o.decisionTs,filled:true,fillTs:t.fillTs,entryTick:t.entryTick,stopTick:t.stopTick,tpTick:t.tpTick});
  }
  const sm=signalMetrics(filled),pm=portfolio(filled),gate=developmentGate(sm,pm);
  const disposition=gate.pass?"EXP048_VISUAL_BLINDED_SELECTION_READY_FOR_SEALED_VALIDATION":"EXP048_VISUAL_BLINDED_SELECTION_FAIL_CLOSE_BEFORE_VALIDATION";
  const result={
    experiment:"EXP-048",stage:"visual_blinded_label_outcome_development",
    tested_repository_sha:process.env.GITHUB_SHA||execSync("git rev-parse HEAD",{cwd:ROOT,encoding:"utf8"}).trim(),
    frozen_protocol_commit:PROTOCOL_COMMIT,parent_protocol_commit:"59d426bd56c82a7d48a6081bc695a7a8eaa657e7",
    complete_label_checkpoint_commit:"8ad19cccdf061afa02c878c0a88dde4700ad95ad",
    label_blob:EXPECTED_LABEL_BLOB,label_summary_blob:EXPECTED_LABEL_SUMMARY_BLOB,packet_blob:EXPECTED_PACKET_BLOB,
    development:["2022-01-01","2025-02-28"],validation_or_holdout_loaded:false,
    source:{repo:"kevingtlin/Market-Data-Lab",commit:SOURCE_COMMIT,head_verified:head,files:verified},
    frozen_label_counts:{all:126,no_trade:75,long:26,short:25,trades:51,confidence_a:14,confidence_b:37},
    execution_protocol:{market_entry:"first active M1 open at/after decision",level_retest_life_active_m1:60,level_retest_expiry_utc:"18:00",outcome_horizon_active_m1:120,hard_exit_utc:"20:00",same_bar_stop_first:true,retest_fill_bar_tp_not_credited:true,primary_cost_usd_at_010:5,stress_cost_usd_at_010:10},
    trade_orders:tradeOrders.length,filled_signals:filled.length,no_fill_count:tradeOrders.length-filled.length,no_fill_reasons:noFillReasons,
    signal_metrics:sm,reference_account:{...pm,trades:undefined},development_gate:gate,disposition
  };
  fs.mkdirSync(path.join(ROOT,"research/results"),{recursive:true});
  fs.writeFileSync(path.join(ROOT,"research/results/EXP-048-visual-blinded-selection-development-summary-v0.1.json"),JSON.stringify(result,null,2)+"\n");
  fs.writeFileSync(path.join(ROOT,"research/results/EXP-048-visual-blinded-selection-order-audit-v0.1.jsonl"),orderAudit.map(x=>JSON.stringify(x)).join("\n")+"\n");
  fs.writeFileSync(path.join(ROOT,"research/results/EXP-048-visual-blinded-selection-filled-signals-v0.1.jsonl"),filled.map(x=>JSON.stringify(x)).join("\n")+(filled.length?"\n":""));
  fs.writeFileSync(path.join(ROOT,"research/results/EXP-048-visual-blinded-selection-reference-trades-v0.1.jsonl"),pm.trades.map(x=>JSON.stringify(x)).join("\n")+(pm.trades.length?"\n":""));
  console.log(JSON.stringify({disposition,trade_orders:tradeOrders.length,filled_signals:filled.length,no_fill_reasons:noFillReasons,signal_metrics:sm,reference_account:{...pm,trades:undefined},development_gate:gate},null,2));
}
main();
