#!/usr/bin/env node
"use strict";

const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
const {execSync}=require("child_process");

const MIN=60000;
const SOURCE_COMMIT="922f83a60cc574e7395fb27397077288055a1ef6";
const SOURCE_REPO=path.resolve(process.env.EXP048_SOURCE_REPO||"/tmp/market-data-lab");
const DATA_DIR=path.join(SOURCE_REPO,"xauusd/bid/m1");
const START=Date.UTC(2022,0,1);
const END=Date.UTC(2025,2,1);

function assert(c,m){if(!c)throw new Error(m);}
function sha256(x){return crypto.createHash("sha256").update(x).digest("hex");}
function gitBlobSha(buf){
  const h=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(Buffer.concat([h,buf])).digest("hex");
}
function utcDate(ts){return new Date(ts).toISOString().slice(0,10);}
function minsUTC(ts){const d=new Date(ts);return d.getUTCHours()*60+d.getUTCMinutes();}
function weekday(ts){const w=new Date(ts).getUTCDay();return w>=1&&w<=5;}
function inDev(ts){return ts>=START&&ts<END;}

function parseTick(s){
  const m=/^([0-9]+)(?:\.([0-9]+))?$/.exec(String(s).trim());
  if(!m)throw new Error("invalid_price_text:"+s);
  let f=m[2]||"";
  if(f.length>3){
    const x=f.slice(3);
    if(!/^0*$/.test(x))throw new Error("off_grid_price:"+s);
    f=f.slice(0,3);
  }
  return Number(m[1])*1000+Number(f.padEnd(3,"0"));
}
function expectedRows(y,m){return new Date(Date.UTC(y,m,0)).getUTCDate()*1440;}
function monthRange(){
  const out=[];let y=2021,m=12;
  while(y<2025||(y===2025&&m<=2)){out.push([y,m]);m++;if(m===13){m=1;y++;}}
  return out;
}
function loadRows(){
  const head=execSync("git rev-parse HEAD",{cwd:SOURCE_REPO,encoding:"utf8"}).trim();
  assert(head===SOURCE_COMMIT,"source_commit_mismatch:"+head);
  assert(execSync("git status --porcelain",{cwd:SOURCE_REPO,encoding:"utf8"}).trim()==="","source_worktree_dirty");
  const rows=[],verified=[];
  let prevTs=null,prevClose=null,activeOrd=0;
  for(const [y,m] of monthRange()){
    const mm=String(m).padStart(2,"0"),name=`xauusd_bid_m1_${y}_${mm}.csv`;
    const rel=`xauusd/bid/m1/${name}`,p=path.join(DATA_DIR,name);
    const buf=fs.readFileSync(p);
    const tree=execSync(`git ls-tree ${SOURCE_COMMIT} -- ${rel}`,{cwd:SOURCE_REPO,encoding:"utf8"}).trim();
    const mt=/^\d+ blob ([0-9a-f]{40})\t/.exec(tree);assert(mt,"tree_missing:"+name);
    assert(gitBlobSha(buf)===mt[1],"blob_mismatch:"+name);
    const lines=buf.toString("utf8").trimEnd().split("\n");
    assert(lines[0].trim()==="timestamp,open,high,low,close","bad_header:"+name);
    assert(lines.length===expectedRows(y,m)+1,"bad_row_count:"+name);
    for(let i=1;i<lines.length;i++){
      const q=lines[i].trim().split(",");assert(q.length===5,"bad_cols:"+name+":"+i);
      const ts=Number(q[0]);assert(Number.isInteger(ts)&&ts%MIN===0,"bad_ts:"+name+":"+i);
      if(prevTs!==null)assert(ts-prevTs===MIN,"timestamp_gap:"+name+":"+i);
      const o=parseTick(q[1]),h=parseTick(q[2]),l=parseTick(q[3]),c=parseTick(q[4]);
      assert(h>=o&&h>=c&&l<=o&&l<=c&&h>=l,"bad_ohlc:"+name+":"+i);
      const carry=prevClose!==null&&o===h&&h===l&&l===c&&c===prevClose;
      rows.push({ts,o,h,l,c,active:!carry,activeOrd:carry?-1:activeOrd++});
      prevTs=ts;prevClose=c;
    }
    verified.push({name,git_blob_sha:mt[1],bytes:buf.length,sha256:sha256(buf)});
  }
  return{rows,verified,head};
}

function buildBars(rows,minutes){
  const size=minutes,out=[];
  for(let i=0;i<rows.length;){
    const st=rows[i].ts;
    if(st%(size*MIN)!==0){i++;continue;}
    if(i+size>rows.length)break;
    let ok=true;
    for(let j=0;j<size;j++)if(rows[i+j].ts!==st+j*MIN){ok=false;break;}
    if(!ok){i++;continue;}
    const q=rows.slice(i,i+size);
    out.push({
      startTs:st,closeTs:st+size*MIN,
      o:q[0].o,h:Math.max(...q.map(x=>x.h)),l:Math.min(...q.map(x=>x.l)),c:q[q.length-1].c,
      active:q.some(x=>x.active)
    });
    i+=size;
  }
  return out;
}

function buildDayStats(rows,bars5){
  const days=new Map(),asia=new Map(),opening=new Map(),barsByDay=new Map();
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
  for(const b of bars5){
    const d=utcDate(b.startTs);
    if(!barsByDay.has(d))barsByDay.set(d,[]);
    barsByDay.get(d).push(b);
  }
  function previousActive(d){
    let t=Date.parse(d+"T00:00:00Z")-86400000;
    for(let k=0;k<10;k++,t-=86400000){
      const ds=utcDate(t),x=days.get(ds);
      if(x&&x.activeM1>0&&x.high>x.low)return{date:ds,...x};
    }
    return null;
  }
  function makeLevels(d){
    const ds=Date.parse(d+"T00:00:00Z"),out=[],p=previousActive(d);
    if(p){
      out.push({cls:"PDH",side:"HIGH",priority:1,price:p.high,knownTs:ds});
      out.push({cls:"PDL",side:"LOW",priority:1,price:p.low,knownTs:ds});
    }
    const a=asia.get(d);
    if(a&&a.rows===360&&a.activeM1>0&&a.high>a.low){
      out.push({cls:"ASIA_HIGH",side:"HIGH",priority:2,price:a.high,knownTs:ds+360*MIN});
      out.push({cls:"ASIA_LOW",side:"LOW",priority:2,price:a.low,knownTs:ds+360*MIN});
    }
    const o=opening.get(d);
    if(o&&o.rows===180&&o.activeM1>0&&o.high>o.low){
      out.push({cls:"OPEN_HIGH",side:"HIGH",priority:3,price:o.high,knownTs:ds+540*MIN});
      out.push({cls:"OPEN_LOW",side:"LOW",priority:3,price:o.low,knownTs:ds+540*MIN});
    }
    return out;
  }
  return{days,asia,opening,barsByDay,makeLevels};
}

function eraFor(ts){
  if(ts<Date.UTC(2023,0,1))return"ERA1";
  if(ts<Date.UTC(2024,0,1))return"ERA2";
  return"ERA3";
}
function sessionBucket(ts){
  const m=minsUTC(ts);
  if(m<600)return"06_10";
  if(m<840)return"10_14";
  return"14_1630";
}
function activeDecisionAfter(rows,attackCloseTs,n){
  let seen=0;
  for(const r of rows){
    if(r.ts<attackCloseTs||!r.active)continue;
    seen++;
    if(seen===n)return r.ts+MIN;
  }
  return null;
}
function relation(c,level){
  if(c>level)return"BEYOND_HIGHER";
  if(c<level)return"BEYOND_LOWER";
  return"ON_LEVEL";
}

function buildUniverse(rows,bars5,ctx){
  const byDate=new Map();
  const events=[];
  const counts={attacks:0,dual_ambiguous:0,outside_window:0,no_decision:0,eligible:0};
  for(const b of bars5){
    const d=utcDate(b.startTs);
    if(!byDate.has(d))byDate.set(d,ctx.makeLevels(d).map(x=>({...x,consumed:false})));
    const levels=byDate.get(d);
    const elig=levels.filter(x=>!x.consumed&&x.knownTs<=b.startTs);
    const hi=elig.filter(x=>x.side==="HIGH"&&b.h>x.price);
    const lo=elig.filter(x=>x.side==="LOW"&&b.l<x.price);
    if(!hi.length&&!lo.length)continue;
    for(const x of hi.concat(lo))x.consumed=true;
    counts.attacks++;
    if(!b.active||!weekday(b.closeTs)||!inDev(b.closeTs)||minsUTC(b.closeTs)<360||minsUTC(b.closeTs)>=990){
      counts.outside_window++;continue;
    }
    if(hi.length&&lo.length){counts.dual_ambiguous++;continue;}
    const arr=hi.length?hi:lo;
    arr.sort((a,b)=>a.priority-b.priority||a.cls.localeCompare(b.cls));
    const level=arr[0];
    const decisionTs=activeDecisionAfter(rows,b.closeTs,15);
    if(decisionTs===null||utcDate(decisionTs-1)!==d||minsUTC(decisionTs)>=1080){
      counts.no_decision++;continue;
    }
    const identity=`${d}|${level.cls}|${b.closeTs}|${level.price}`;
    const e={
      identity,
      eventHash:sha256(identity),
      era:eraFor(b.closeTs),
      eventDate:d,
      levelClass:level.cls,
      levelSide:level.side,
      levelPrice:level.price,
      levelKnownTs:level.knownTs,
      attackStartTs:b.startTs,
      attackCloseTs:b.closeTs,
      attackOpen:b.o,attackHigh:b.h,attackLow:b.l,attackClose:b.c,
      attackCloseRelation:relation(b.c,level.price),
      decisionTs,
      sessionBucket:sessionBucket(b.closeTs)
    };
    events.push(e);counts.eligible++;
  }
  return{events,counts};
}

function selectEvents(events){
  const eras=["ERA1","ERA2","ERA3"];
  const classes=["PDH","PDL","ASIA_HIGH","ASIA_LOW","OPEN_HIGH","OPEN_LOW"];
  const selected=[],cells={};
  for(const era of eras){
    for(const cls of classes){
      const q=events.filter(x=>x.era===era&&x.levelClass===cls).sort((a,b)=>a.eventHash.localeCompare(b.eventHash));
      cells[era+":"+cls]={available:q.length,selected:Math.min(7,Math.max(0,q.length-7)),rank_start:8,rank_end:14};
      assert(q.length>=14,"insufficient_cell_for_disjoint_replication:"+era+":"+cls+":"+q.length);
      selected.push(...q.slice(7,14));
    }
  }
  selected.sort((a,b)=>a.attackCloseTs-b.attackCloseTs||a.levelClass.localeCompare(b.levelClass));
  return{selected,cells};
}

function takeCompletedBars(bars,decisionTs,n){
  const q=bars.filter(b=>b.closeTs<=decisionTs);
  return q.slice(Math.max(0,q.length-n)).map(b=>[b.startTs,b.o,b.h,b.l,b.c]);
}
function takeCompletedM1(rows,decisionTs,n){
  const q=rows.filter(r=>r.ts+MIN<=decisionTs);
  return q.slice(Math.max(0,q.length-n)).map(r=>[r.ts,r.o,r.h,r.l,r.c]);
}
function attackedByDecision(level,bars,decisionTs){
  for(const b of bars){
    if(!b.active||b.startTs<level.knownTs||b.closeTs>decisionTs)continue;
    if(level.side==="HIGH"?b.h>level.price:b.l<level.price)return true;
  }
  return false;
}
function packetFor(e,rows,bars5,bars15,bars60,ctx,index){
  const dayBars=ctx.barsByDay.get(e.eventDate)||[];
  const levels=ctx.makeLevels(e.eventDate)
    .filter(x=>x.knownTs<=e.decisionTs)
    .map(x=>({
      levelClass:x.cls,side:x.side,price:x.price,knownTs:x.knownTs,
      attackedByDecision:attackedByDecision(x,dayBars,e.decisionTs)
    }));
  const windows={
    h1:takeCompletedBars(bars60,e.decisionTs,96),
    m15:takeCompletedBars(bars15,e.decisionTs,96),
    m5:takeCompletedBars(bars5,e.decisionTs,144),
    m1:takeCompletedM1(rows,e.decisionTs,180)
  };
  const allEnds=[];
  for(const [tf,arr] of Object.entries(windows)){
    const dur=tf==="h1"?60:tf==="m15"?15:tf==="m5"?5:1;
    for(const b of arr)allEnds.push(b[0]+dur*MIN);
  }
  const maxEnd=Math.max(...allEnds);
  assert(maxEnd<=e.decisionTs,"future_bar_leak:"+e.identity);
  return{
    replayId:"R"+String(index+1).padStart(3,"0"),
    eventHash:e.eventHash,
    era:e.era,eventDate:e.eventDate,sessionBucket:e.sessionBucket,
    levelClass:e.levelClass,levelSide:e.levelSide,levelPrice:e.levelPrice,levelKnownTs:e.levelKnownTs,
    attackStartTs:e.attackStartTs,attackCloseTs:e.attackCloseTs,
    attackOpen:e.attackOpen,attackHigh:e.attackHigh,attackLow:e.attackLow,attackClose:e.attackClose,
    attackCloseRelation:e.attackCloseRelation,
    decisionTs:e.decisionTs,
    maxPacketBarEndTs:maxEnd,
    causalLevelSnapshot:levels,
    windows,
    futureDataIncluded:false,
    outcomeFieldsIncluded:false,
    reviewStatus:"UNLABELED"
  };
}

function countBy(xs,keyFn){
  const o={};for(const x of xs){const k=keyFn(x);o[k]=(o[k]||0)+1;}return o;
}

function main(){
  const {rows,verified,head}=loadRows();
  const bars5=buildBars(rows,5),bars15=buildBars(rows,15),bars60=buildBars(rows,60);
  const ctx=buildDayStats(rows,bars5);
  const {events,counts}=buildUniverse(rows,bars5,ctx);
  const {selected,cells}=selectEvents(events);
  assert(selected.length===126,"selected_count:"+selected.length);
  const packets=selected.map((e,i)=>packetFor(e,rows,bars5,bars15,bars60,ctx,i));
  assert(packets.every(p=>p.maxPacketBarEndTs<=p.decisionTs&&!p.futureDataIncluded&&!p.outcomeFieldsIncluded),"packet_integrity");
  const perCell=countBy(packets,p=>p.era+":"+p.levelClass);
  assert(Object.values(perCell).every(n=>n===7)&&Object.keys(perCell).length===18,"stratification_integrity");

  const priorPath="research/results/EXP-047-blinded-replay-packets-v0.1.jsonl";
  const priorBuf=fs.readFileSync(priorPath);
  const expectedPriorBlob="e6eeeed45a0e0181b23d0d3ba3497b5521677c41";
  assert(gitBlobSha(priorBuf)===expectedPriorBlob,"exp047_packet_blob_changed");
  const priorHashes=new Set(priorBuf.toString("utf8").trim().split("\n").filter(Boolean).map(JSON.parse).map(x=>x.eventHash));
  const overlap=packets.filter(p=>priorHashes.has(p.eventHash)).map(p=>p.eventHash);
  assert(overlap.length===0,"exp047_overlap:"+overlap.join(","));

  const packetText=packets.map(x=>JSON.stringify(x)).join("\n")+"\n";
  const summary={
    experiment:"EXP-048",
    stage:"zero_outcome_blinded_replay_packet_generation",
    protocol_commit:"59d426bd56c82a7d48a6081bc695a7a8eaa657e7",
    tested_repository_sha:process.env.GITHUB_SHA||execSync("git rev-parse HEAD",{encoding:"utf8"}).trim(),
    source:{repo:"kevingtlin/Market-Data-Lab",commit:SOURCE_COMMIT,head_verified:head,files:verified},
    warmup:["2021-12-01","2021-12-31"],
    development:["2022-01-01","2025-02-28"],
    validation_or_holdout_files_loaded:false,
    target_labels_calculated:false,
    mfe_mae_calculated:false,
    pnl_calculated:false,
    post_decision_path_loaded:false,
    event_universe_count:events.length,
    universe_diagnostics:counts,
    available_by_era_level:cells,
    selected_packet_count:packets.length,
    disjoint_from_exp047:true,
    exp047_packet_blob:expectedPriorBlob,
    exp047_overlap_count:overlap.length,
    selected_by_era:countBy(packets,p=>p.era),
    selected_by_level:countBy(packets,p=>p.levelClass),
    selected_by_session_bucket:countBy(packets,p=>p.sessionBucket),
    selected_by_attack_close_relation:countBy(packets,p=>p.attackCloseRelation),
    selected_cell_counts:perCell,
    all_packets_causal:packets.every(p=>p.maxPacketBarEndTs<=p.decisionTs),
    all_packets_unlabeled:packets.every(p=>p.reviewStatus==="UNLABELED"),
    packet_jsonl_sha256:sha256(packetText),
    packet_format:{
      bar_array:"[startTs,open,high,low,close] integer source ticks",
      windows:{h1:96,m15:96,m5:144,m1:180}
    },
    disposition:"EXP048_DISJOINT_VISUAL_REPLAY_PACKETS_READY"
  };

  fs.mkdirSync("research/results", {recursive:true});
  fs.writeFileSync("research/results/EXP-048-blinded-replay-packets-v0.1.jsonl",packetText);
  fs.writeFileSync("research/results/EXP-048-blinded-replay-summary-v0.1.json",JSON.stringify(summary,null,2)+"\n");

  console.log("EXP048_DISJOINT_PACKET_BUILD",JSON.stringify({
    disposition:summary.disposition,
    event_universe_count:summary.event_universe_count,
    selected_packet_count:summary.selected_packet_count,
    selected_by_era:summary.selected_by_era,
    selected_by_level:summary.selected_by_level,
    selected_by_session_bucket:summary.selected_by_session_bucket,
    packet_jsonl_sha256:summary.packet_jsonl_sha256
  }));
}
main();
