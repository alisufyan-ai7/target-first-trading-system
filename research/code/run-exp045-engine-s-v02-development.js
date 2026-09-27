#!/usr/bin/env node
"use strict";

const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
const {execSync}=require("child_process");

const ROOT=path.resolve(__dirname,"../..");
const SOURCE_REPO=path.resolve(process.env.EXP045_SOURCE_REPO||"/tmp/market-data-lab");
const SOURCE_COMMIT="922f83a60cc574e7395fb27397077288055a1ef6";
const CANDIDATE_PATH=path.join(ROOT,"research/results/EXP-045-zero-outcome-candidates-v0.2-extended.jsonl");
const PREFLIGHT_PATH=path.join(ROOT,"research/results/EXP-045-zero-outcome-preflight-v0.2-extended.json");
const EXPECTED_CANDIDATE_BLOB="e49f13b7b558ccd4b35130596ec103eedc800b55";
const EXPECTED_PREFLIGHT_BLOB="717b3f99edd58d47d3e7088b845ddb8a4d0a4583";
const START=Date.UTC(2022,0,1), END=Date.UTC(2025,2,1), MIN=60000;
const PRIMARY_COST_010=5.0, STRESS_COST_010=10.0;

function assert(c,m){if(!c)throw new Error(m);}
function gitBlobSha(buf){
  const h=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(Buffer.concat([h,buf])).digest("hex");
}
function sha256(buf){return crypto.createHash("sha256").update(buf).digest("hex");}
function parseTick(s){
  const m=/^([0-9]+)(?:\.([0-9]+))?$/.exec(String(s).trim());
  if(!m)throw new Error("invalid_price:"+s);
  let f=m[2]||"";
  if(f.length>3){const x=f.slice(3);if(!/^0*$/.test(x))throw new Error("off_grid:"+s);f=f.slice(0,3);}
  return Number(m[1])*1000+Number(f.padEnd(3,"0"));
}
function dateStr(ts){return new Date(ts).toISOString().slice(0,10);}
function dayStart(ts){const d=new Date(ts);return Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate());}
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
function monthRange(){
  const out=[];let y=2021,m=12;
  while(y<2025||(y===2025&&m<=2)){out.push([y,m]);m++;if(m===13){m=1;y++;}}
  return out;
}
function expectedRows(y,m){return new Date(Date.UTC(y,m,0)).getUTCDate()*1440;}

function loadRows(){
  const head=execSync("git rev-parse HEAD",{cwd:SOURCE_REPO,encoding:"utf8"}).trim();
  assert(head===SOURCE_COMMIT,"source_commit_mismatch");
  assert(execSync("git status --porcelain",{cwd:SOURCE_REPO,encoding:"utf8"}).trim()==="","source_dirty");
  const rows=[],verified=[];let prevTs=null,prevClose=null,activeOrd=0;
  for(const [y,m] of monthRange()){
    const mm=String(m).padStart(2,"0"),name=`xauusd_bid_m1_${y}_${mm}.csv`;
    const rel=`xauusd/bid/m1/${name}`,p=path.join(SOURCE_REPO,rel),buf=fs.readFileSync(p);
    const tree=execSync(`git ls-tree ${SOURCE_COMMIT} -- ${rel}`,{cwd:SOURCE_REPO,encoding:"utf8"}).trim();
    const mt=/^\d+ blob ([0-9a-f]{40})\t/.exec(tree);assert(mt,"tree_missing:"+name);
    assert(gitBlobSha(buf)===mt[1],"blob_mismatch:"+name);
    const lines=buf.toString("utf8").trimEnd().split("\n");
    assert(lines[0].trim()==="timestamp,open,high,low,close","header:"+name);
    assert(lines.length===expectedRows(y,m)+1,"row_count:"+name);
    for(let i=1;i<lines.length;i++){
      const q=lines[i].trim().split(",");assert(q.length===5,"cols:"+name+":"+i);
      const ts=Number(q[0]);assert(Number.isInteger(ts)&&ts%MIN===0,"ts:"+name+":"+i);
      if(prevTs!==null)assert(ts-prevTs===MIN,"gap:"+name+":"+i);
      const o=parseTick(q[1]),h=parseTick(q[2]),l=parseTick(q[3]),c=parseTick(q[4]);
      assert(h>=o&&h>=c&&l<=o&&l<=c&&h>=l,"ohlc:"+name+":"+i);
      const carry=prevClose!==null&&o===h&&h===l&&l===c&&c===prevClose;
      rows.push({ts,o,h,l,c,active:!carry,activeOrd:carry?-1:activeOrd++});
      prevTs=ts;prevClose=c;
    }
    verified.push({name,git_blob_sha:mt[1],bytes:buf.length,sha256:sha256(buf)});
  }
  return{rows,verified,head};
}

function buildBars5(rows){
  const out=[];
  for(let i=0;i+4<rows.length;){
    const st=rows[i].ts;
    if(st%(5*MIN)!==0){i++;continue;}
    let ok=true;for(let j=0;j<5;j++)if(rows[i+j].ts!==st+j*MIN){ok=false;break;}
    if(!ok){i++;continue;}
    const q=rows.slice(i,i+5);
    out.push({startTs:st,closeTs:st+5*MIN,h:Math.max(...q.map(x=>x.h)),l:Math.min(...q.map(x=>x.l)),
      c:q[4].c,active:q.some(x=>x.active)});
    i+=5;
  }
  return out;
}

function buildDaily(rows,bars5){
  const days=new Map(),asia=new Map(),opening=new Map(),barsByDay=new Map();
  function add(map,d,r){
    let z=map.get(d);if(!z){z={high:-Infinity,low:Infinity,rows:0,activeM1:0};map.set(d,z);}
    z.high=Math.max(z.high,r.h);z.low=Math.min(z.low,r.l);z.rows++;if(r.active)z.activeM1++;
  }
  for(const r of rows){
    const d=dateStr(r.ts),mins=new Date(r.ts).getUTCHours()*60+new Date(r.ts).getUTCMinutes();
    add(days,d,r);if(mins<360)add(asia,d,r);if(mins>=360&&mins<540)add(opening,d,r);
  }
  for(const b of bars5){
    const d=dateStr(b.startTs);if(!barsByDay.has(d))barsByDay.set(d,[]);barsByDay.get(d).push(b);
  }
  function previousActive(d){
    let t=dayStart(Date.parse(d+"T00:00:00Z"))-86400000;
    for(let k=0;k<10;k++,t-=86400000){
      const ds=dateStr(t),x=days.get(ds);if(x&&x.activeM1>0&&x.high>x.low)return{date:ds,...x};
    }return null;
  }
  const cache=new Map();
  function attackClose(level,side,knownTs,bs){
    for(const b of bs){
      if(!b.active||b.startTs<knownTs)continue;
      if(side==="HIGH"?b.h>level:b.l<level)return b.closeTs;
    }return null;
  }
  function levelsForDate(d){
    if(cache.has(d))return cache.get(d);
    const ds=Date.parse(d+"T00:00:00Z"),bs=barsByDay.get(d)||[],out=[];
    const p=previousActive(d);
    if(p){
      out.push({cls:"PDH",side:"HIGH",price:p.high,priority:1,knownTs:ds});
      out.push({cls:"PDL",side:"LOW",price:p.low,priority:1,knownTs:ds});
    }
    const a=asia.get(d);
    if(a&&a.rows===360&&a.activeM1>0&&a.high>a.low){
      out.push({cls:"ASIA_HIGH",side:"HIGH",price:a.high,priority:2,knownTs:ds+360*MIN});
      out.push({cls:"ASIA_LOW",side:"LOW",price:a.low,priority:2,knownTs:ds+360*MIN});
    }
    const o=opening.get(d);
    if(o&&o.rows===180&&o.activeM1>0&&o.high>o.low){
      out.push({cls:"OPEN_HIGH",side:"HIGH",price:o.high,priority:3,knownTs:ds+540*MIN});
      out.push({cls:"OPEN_LOW",side:"LOW",price:o.low,priority:3,knownTs:ds+540*MIN});
    }
    for(const z of out)z.firstAttackCloseTs=attackClose(z.price,z.side,z.knownTs,bs);
    cache.set(d,out);return out;
  }
  return{levelsForDate};
}

function lowerBound(rows,ts){
  let lo=0,hi=rows.length;
  while(lo<hi){const mid=(lo+hi)>>1;if(rows[mid].ts<ts)lo=mid+1;else hi=mid;}
  return lo;
}

function targetPlan(c,daily){
  const levels=daily.levelsForDate(dateStr(c.fillSignalTs))
    .filter(z=>z.knownTs<c.fillSignalTs&&(z.firstAttackCloseTs===null||z.firstAttackCloseTs>c.fillSignalTs))
    .filter(z=>c.direction==="LONG"?z.price>c.entry:z.price<c.entry);
  levels.sort((a,b)=>{
    const da=Math.abs(a.price-c.entry),db=Math.abs(b.price-c.entry);
    return da-db||a.priority-b.priority||a.cls.localeCompare(b.cls);
  });
  const dedup=[],seen=new Set();
  for(const z of levels){if(!seen.has(z.price)){seen.add(z.price);dedup.push(z);}}
  if(!dedup.length)return{admitted:false,rejectReason:"REJECT_NO_FRESH_STRUCTURAL_TARGET"};
  const tp1=dedup[0],r=c.stopDistanceTicks,room1=Math.abs(tp1.price-c.entry)/r;
  if(room1<1.5)return{admitted:false,rejectReason:"REJECT_STRUCTURAL_ROOM_LT_1_50R",tp1,room1};
  const second=dedup[1]||null;
  const room2=second?Math.abs(second.price-c.entry)/r:null;
  const runner=!!second&&room2>=3.0;
  return{admitted:true,tp1,room1,tp2:runner?second:null,room2:runner?room2:null,runnerEligible:runner};
}

function simulateSignal(c,plan,rows){
  const sign=c.direction==="LONG"?1:-1,stop=c.stop,tp1=plan.tp1.price,tp2=plan.tp2?plan.tp2.price:null;
  const cutoff=dayStart(c.fillSignalTs)+20*60*MIN;
  let idx=lowerBound(rows,c.fillSignalTs),active=0,last=null,tp1Hit=false,tp1Ts=null;
  let gross=0,outcome=null,exitTs=null,exitPrice=null;
  while(idx<rows.length&&rows[idx].ts<cutoff&&active<120){
    const r=rows[idx++];if(!r.active)continue;active++;last=r;
    const stopHit=c.direction==="LONG"?r.l<=stop:r.h>=stop;
    if(!tp1Hit){
      const t1=c.direction==="LONG"?r.h>=tp1:r.l<=tp1;
      if(stopHit){gross=-c.grossStopUSD;outcome="STOP";exitTs=r.ts+MIN;exitPrice=stop;break;}
      if(t1){
        tp1Hit=true;tp1Ts=r.ts+MIN;
        if(!plan.runnerEligible){
          gross=Math.abs(tp1-c.entry)*0.01;outcome="TP1_FULL";exitTs=r.ts+MIN;exitPrice=tp1;break;
        }
        gross=0.5*Math.abs(tp1-c.entry)*0.01;
        continue;
      }
    }else{
      const beHit=c.direction==="LONG"?r.l<=c.entry:r.h>=c.entry;
      if(beHit){outcome="TP1_THEN_BE";exitTs=r.ts+MIN;exitPrice=c.entry;break;}
      const t2=c.direction==="LONG"?r.h>=tp2:r.l<=tp2;
      if(t2){
        gross+=0.5*Math.abs(tp2-c.entry)*0.01;outcome="TP1_THEN_TP2";exitTs=r.ts+MIN;exitPrice=tp2;break;
      }
    }
  }
  if(outcome===null){
    if(!last){
      outcome=tp1Hit?"TP1_THEN_TIMEOUT":"TIMEOUT";
      exitTs=Math.min(c.fillSignalTs,cutoff);exitPrice=c.entry;
    }else{
      const pnlTicks=sign*(last.c-c.entry);
      if(tp1Hit)gross+=0.5*pnlTicks*0.01;else gross=pnlTicks*0.01;
      outcome=tp1Hit?"TP1_THEN_TIMEOUT":"TIMEOUT";
      exitTs=Math.min(last.ts+MIN,cutoff);exitPrice=last.c;
    }
  }
  const risk=c.grossStopUSD;
  return{
    ...c,targetPlan:plan,outcome,exitTs,exitPrice,activeM1Bars:active,tp1Hit,tp1Ts,
    grossPnlUSD010:gross,primaryNetUSD010:gross-PRIMARY_COST_010,stressNetUSD010:gross-STRESS_COST_010,
    grossR:gross/risk,primaryR:(gross-PRIMARY_COST_010)/risk,stressR:(gross-STRESS_COST_010)/risk
  };
}

function signalMetrics(xs){
  const gross=xs.map(x=>x.grossR),primary=xs.map(x=>x.primaryR),stress=xs.map(x=>x.stressR);
  const eraDefs=[
    ["ERA1",Date.UTC(2022,0,1),Date.UTC(2023,0,1)],
    ["ERA2",Date.UTC(2023,0,1),Date.UTC(2024,0,1)],
    ["ERA3",Date.UTC(2024,0,1),Date.UTC(2025,2,1)]
  ];
  const eras={};
  for(const [name,a,b] of eraDefs){
    const q=xs.filter(x=>x.fillSignalTs>=a&&x.fillSignalTs<b);
    eras[name]={n:q.length,stress_r_expectancy:q.length?q.reduce((s,x)=>s+x.stressR,0)/q.length:null,
      primary_r_expectancy:q.length?q.reduce((s,x)=>s+x.primaryR,0)/q.length:null};
  }
  return{
    n:xs.length,tp1_hit_rate:xs.length?xs.filter(x=>x.tp1Hit).length/xs.length:null,
    runner_eligible:xs.filter(x=>x.targetPlan.runnerEligible).length,
    tp2_hits:xs.filter(x=>x.outcome==="TP1_THEN_TP2").length,
    outcomes:Object.fromEntries([...new Set(xs.map(x=>x.outcome))].sort().map(k=>[k,xs.filter(x=>x.outcome===k).length])),
    tp1_room_r:dist(xs.map(x=>x.targetPlan.room1)),
    gross_r_expectancy:xs.length?gross.reduce((a,b)=>a+b,0)/xs.length:null,
    primary_r_expectancy:xs.length?primary.reduce((a,b)=>a+b,0)/xs.length:null,
    stress_r_expectancy:xs.length?stress.reduce((a,b)=>a+b,0)/xs.length:null,
    primary_r_profit_factor:pf(primary),stress_r_profit_factor:pf(stress),eras
  };
}

function safeLot(c){
  const distXau=c.stopDistanceTicks/1000;
  const raw=40/(distXau*100+100);
  const lot=Math.min(0.10,Math.floor((raw+1e-12)/0.01)*0.01);
  return lot>=0.01?Number(lot.toFixed(2)):0;
}
function scaledTrade(x,lot){
  const scale=lot/0.10,gross=x.grossPnlUSD010*scale;
  return{...x,lot,grossUSD:gross,primaryUSD:gross-50*lot,stressUSD:gross-100*lot};
}
function maxDrawdown(vals){
  let eq=0,peak=0,mdd=0;for(const v of vals){eq+=v;peak=Math.max(peak,eq);mdd=Math.max(mdd,peak-eq);}return mdd;
}
function consecutive(flags){let b=0,c=0;for(const x of flags){c=x?c+1:0;b=Math.max(b,c);}return b;}

function portfolio(xs){
  const ranked=[...xs].sort((a,b)=>a.fillSignalTs-b.fillSignalTs||
    b.targetPlan.room1-a.targetPlan.room1||a.stopDistanceTicks-b.stopDistanceTicks||a.id.localeCompare(b.id));
  let busyUntil=-Infinity,blockedOpen=0,blockedDay=0;
  const trades=[],dailyRealized={};
  for(const x of ranked){
    if(x.fillSignalTs<busyUntil){blockedOpen++;continue;}
    const d=dateStr(x.fillSignalTs),real=dailyRealized[d]||0;
    if(real<=-40||real>=150){blockedDay++;continue;}
    const lot=safeLot(x);if(lot<0.01)continue;
    const t=scaledTrade(x,lot);trades.push(t);busyUntil=t.exitTs;dailyRealized[d]=(dailyRealized[d]||0)+t.primaryUSD;
  }
  const weekdays=[];
  for(let t=START;t<END;t+=86400000){const w=new Date(t).getUTCDay();if(w>=1&&w<=5)weekdays.push(dateStr(t));}
  const primaryByDay=Object.fromEntries(weekdays.map(d=>[d,0])),stressByDay=Object.fromEntries(weekdays.map(d=>[d,0]));
  for(const t of trades){const d=dateStr(t.fillSignalTs);primaryByDay[d]+=t.primaryUSD;stressByDay[d]+=t.stressUSD;}
  const pDaily=weekdays.map(d=>primaryByDay[d]),sDaily=weekdays.map(d=>stressByDay[d]);
  const rolling5=[];for(let i=4;i<pDaily.length;i++)rolling5.push(pDaily.slice(i-4,i+1).reduce((a,b)=>a+b,0));
  const pvals=trades.map(x=>x.primaryUSD),svals=trades.map(x=>x.stressUSD);
  return{
    actual_trades:trades.length,blocked_due_one_open:blockedOpen,blocked_due_daily_state:blockedDay,
    distinct_trade_weekdays:new Set(trades.map(x=>dateStr(x.fillSignalTs))).size,
    lot:dist(trades.map(x=>x.lot)),
    primary_expectancy_usd:trades.length?pvals.reduce((a,b)=>a+b,0)/trades.length:null,
    stress_expectancy_usd:trades.length?svals.reduce((a,b)=>a+b,0)/trades.length:null,
    primary_profit_factor:pf(pvals),stress_profit_factor:pf(svals),
    total_primary_pnl_usd:pvals.reduce((a,b)=>a+b,0),total_stress_pnl_usd:svals.reduce((a,b)=>a+b,0),
    primary_max_drawdown_usd:maxDrawdown(pDaily),stress_max_drawdown_usd:maxDrawdown(sDaily),
    all_development_weekdays:weekdays.length,trades_per_all_weekday:trades.length/weekdays.length,
    primary_daily:{mean:pDaily.reduce((a,b)=>a+b,0)/pDaily.length,median:percentile(pDaily,.5),
      losing_pct:pDaily.filter(x=>x<0).length/pDaily.length,le_50_pct:pDaily.filter(x=>x<=50).length/pDaily.length,
      ge_100_pct:pDaily.filter(x=>x>=100).length/pDaily.length,ge_150_pct:pDaily.filter(x=>x>=150).length/pDaily.length,
      ge_200_pct:pDaily.filter(x=>x>=200).length/pDaily.length,
      max_consecutive_losing_days:consecutive(pDaily.map(x=>x<0)),
      max_consecutive_le_50_days:consecutive(pDaily.map(x=>x<=50)),
      rolling_5day:dist(rolling5)},
    trades
  };
}

function branchGate(branch,admitted,sm,pm){
  const rejection=branch==="REJECTION";
  const positiveStressEras=Object.values(sm.eras).filter(x=>x.stress_r_expectancy!==null&&x.stress_r_expectancy>0).length;
  const g={
    sample_signals_min:admitted.length>=(rejection?60:25),
    reference_trades_min:pm.actual_trades>=(rejection?40:20),
    distinct_trade_weekdays_min:pm.distinct_trade_weekdays>=(rejection?35:18),
    gross_r_expectancy_gt_0_20:sm.gross_r_expectancy!==null&&sm.gross_r_expectancy>0.20,
    primary_r_expectancy_gt_0:sm.primary_r_expectancy!==null&&sm.primary_r_expectancy>0,
    stress_r_expectancy_gt_0:sm.stress_r_expectancy!==null&&sm.stress_r_expectancy>0,
    primary_r_pf_ge_1_10:sm.primary_r_profit_factor!==null&&sm.primary_r_profit_factor>=1.10,
    stress_r_pf_ge_1_05:sm.stress_r_profit_factor!==null&&sm.stress_r_profit_factor>=1.05,
    positive_stress_eras_ge_2:positiveStressEras>=2,
    reference_primary_expectancy_gt_0:pm.primary_expectancy_usd!==null&&pm.primary_expectancy_usd>0,
    reference_stress_expectancy_gt_0:pm.stress_expectancy_usd!==null&&pm.stress_expectancy_usd>0,
    reference_primary_pf_ge_1_10:pm.primary_profit_factor!==null&&pm.primary_profit_factor>=1.10,
    reference_stress_pf_ge_1_05:pm.stress_profit_factor!==null&&pm.stress_profit_factor>=1.05,
    stress_mdd_le_150:pm.stress_max_drawdown_usd<=150,
    protected_periods_sealed:true
  };
  g.branch_pass=Object.values(g).every(Boolean);return g;
}

function selfTests(){
  assert(safeLot({stopDistanceTicks:1000})===0.10,"safe_lot_tight");
  assert(safeLot({stopDistanceTicks:4000})===0.08,"safe_lot_wide");
  const dummy={direction:"LONG",entry:1000,stop:900,stopDistanceTicks:100,grossStopUSD:1,fillSignalTs:10000};
  const fake={levelsForDate:()=>[
    {cls:"PDH",price:1200,priority:1,knownTs:0,firstAttackCloseTs:10000},
    {cls:"ASIA_HIGH",price:1300,priority:2,knownTs:0,firstAttackCloseTs:11000}
  ]};
  const p=targetPlan(dummy,fake);assert(p.admitted&&p.tp1.price===1300,"same_timestamp_target_not_fresh");
  return{ok:true,tests:["safe_lot_tight","safe_lot_wide","same_timestamp_target_not_fresh"]};
}

function main(){
  const candBuf=fs.readFileSync(CANDIDATE_PATH),preBuf=fs.readFileSync(PREFLIGHT_PATH);
  assert(gitBlobSha(candBuf)===EXPECTED_CANDIDATE_BLOB,"candidate_blob_changed");
  assert(gitBlobSha(preBuf)===EXPECTED_PREFLIGHT_BLOB,"preflight_blob_changed");
  const pre=JSON.parse(preBuf.toString("utf8"));assert(pre.preflight_pass&&pre.accepted_filled_candidates===160,"preflight_not_authorized");
  const candidates=candBuf.toString("utf8").trim().split("\n").filter(Boolean).map(JSON.parse);
  assert(candidates.length===160,"candidate_count_changed");

  const {rows,verified,head}=loadRows(),bars5=buildBars5(rows),daily=buildDaily(rows,bars5);
  const planned=candidates.map(c=>({...c,plan:targetPlan(c,daily)}));
  const rejected=planned.filter(x=>!x.plan.admitted);
  const admitted=planned.filter(x=>x.plan.admitted).map(x=>simulateSignal(x,x.plan,rows));

  const branchResults={};
  const passing=[];
  for(const branch of ["REJECTION","ACCEPTANCE"]){
    const allBranch=planned.filter(x=>x.branch===branch);
    const a=admitted.filter(x=>x.branch===branch);
    const sm=signalMetrics(a),pm=portfolio(a);const gate=branchGate(branch,a,sm,pm);
    branchResults[branch]={
      pre_target_candidates:allBranch.length,
      target_admitted:a.length,
      target_rejected:allBranch.length-a.length,
      rejection_reasons:Object.fromEntries([...new Set(allBranch.filter(x=>!x.plan.admitted).map(x=>x.plan.rejectReason))].map(k=>[k,allBranch.filter(x=>!x.plan.admitted&&x.plan.rejectReason===k).length])),
      signal_metrics:sm,
      reference_account:{...pm,trades:undefined},
      development_gate:gate
    };
    if(gate.branch_pass)passing.push(branch);
  }
  const combinedSignal=signalMetrics(admitted),combinedPortfolio=portfolio(admitted);
  const disposition=passing.length===0?"ENGINE_S_FAIL_CLOSE_BEFORE_VALIDATION":
    passing.length===1?"ENGINE_S_ONE_BRANCH_READY_FOR_VALIDATION":"ENGINE_S_BOTH_BRANCHES_READY_FOR_VALIDATION";

  const result={
    experiment:"EXP-045",engine:"Engine S v0.2",stage:"structural_target_management_development",
    tested_repository_sha:process.env.GITHUB_SHA||execSync("git rev-parse HEAD",{cwd:ROOT,encoding:"utf8"}).trim(),
    frozen_protocol_commit:"85600a74e2e6dc3f4efaf64d5cde385f89bc4758",
    zero_outcome_result_commit:"835af4eb6a1b76026cf0f04c46ce06840d2ff287",
    zero_outcome_result_blob:EXPECTED_PREFLIGHT_BLOB,candidate_blob:EXPECTED_CANDIDATE_BLOB,
    development:["2022-01-01","2025-02-28"],validation_or_holdout_loaded:false,
    source:{repo:"kevingtlin/Market-Data-Lab",commit:SOURCE_COMMIT,head_verified:head,files:verified},
    self_tests:selfTests(),
    target_protocol:{tp1_min_room_r:1.5,tp2_runner_min_room_r:3.0,partial_fraction_tp1:0.5,
      horizon_active_m1:120,hard_cutoff_utc:"20:00",primary_cost_usd_at_0_10:5,stress_cost_usd_at_0_10:10},
    pre_target_candidates:candidates.length,target_admitted:admitted.length,target_rejected:rejected.length,
    overall_rejection_reasons:Object.fromEntries([...new Set(rejected.map(x=>x.plan.rejectReason))].map(k=>[k,rejected.filter(x=>x.plan.rejectReason===k).length])),
    branch_results:branchResults,
    combined_descriptive:{signal_metrics:combinedSignal,reference_account:{...combinedPortfolio,trades:undefined}},
    passing_branches:passing,disposition
  };

  fs.mkdirSync(path.join(ROOT,"research/results"),{recursive:true});
  fs.writeFileSync(path.join(ROOT,"research/results/EXP-045-engine-s-v0.2-development-summary.json"),JSON.stringify(result,null,2)+"\n");
  fs.writeFileSync(path.join(ROOT,"research/results/EXP-045-engine-s-v0.2-development-signals.jsonl"),
    admitted.map(x=>JSON.stringify(x)).join("\n")+(admitted.length?"\n":""));
  fs.writeFileSync(path.join(ROOT,"research/results/EXP-045-engine-s-v0.2-development-reference-trades.jsonl"),
    combinedPortfolio.trades.map(x=>JSON.stringify(x)).join("\n")+(combinedPortfolio.trades.length?"\n":""));

  console.log(JSON.stringify({
    disposition,passing_branches:passing,target_admitted:admitted.length,
    rejection:branchResults.REJECTION,
    acceptance:branchResults.ACCEPTANCE
  },null,2));
}
main();
