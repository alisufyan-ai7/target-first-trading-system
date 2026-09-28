#!/usr/bin/env node
"use strict";

const fs=require("fs");
const crypto=require("crypto");

const INPUT="research/results/EXP-047-blinded-replay-packets-v0.1.jsonl";
const EXPECTED_PACKET_SHA256="1b436900a9b2cd3193763d6076d5d75f670294da96c92791b76a4d372558c1f1";
const OUT_MD="research/results/EXP-047-blinded-replay-review-deck-v0.1.md";
const OUT_JSON="research/results/EXP-047-blinded-replay-review-cards-v0.1.jsonl";

function assert(c,m){if(!c)throw new Error(m);}
function sha256(s){return crypto.createHash("sha256").update(s).digest("hex");}
function iso(ts){return new Date(ts).toISOString();}
function px(t){return Number((t/1000).toFixed(3));}
function off(t,level){return Number(((t-level)/1000).toFixed(3));}
function avg(a){return a.length?a.reduce((x,y)=>x+y,0)/a.length:null;}
function rangePos(bars){
  if(!bars.length)return null;
  const hi=Math.max(...bars.map(x=>x[2])),lo=Math.min(...bars.map(x=>x[3])),c=bars[bars.length-1][4];
  return hi===lo?0.5:(c-lo)/(hi-lo);
}
function avgRange(bars,n){
  const q=bars.slice(-n);
  return q.length?avg(q.map(x=>x[2]-x[3])):null;
}
function change(bars,n){
  if(bars.length<2)return 0;
  const i=Math.max(0,bars.length-1-n);
  return bars[bars.length-1][4]-bars[i][4];
}
function directionBalance(bars,n){
  const q=bars.slice(-n);let up=0,down=0,flat=0;
  for(const x of q){if(x[4]>x[1])up++;else if(x[4]<x[1])down++;else flat++;}
  return{up,down,flat};
}
function summarizeTf(bars){
  const q24=bars.slice(-24);
  return{
    close:px(bars[bars.length-1][4]),
    change_6_usd:px(change(bars,6)),
    change_12_usd:px(change(bars,12)),
    change_24_usd:px(change(bars,24)),
    range_pos_24:Number((rangePos(q24)??0.5).toFixed(3)),
    avg_range_12_usd:px(avgRange(bars,12)||0),
    candle_balance_8:directionBalance(bars,8)
  };
}
function recentBars(bars,n,level){
  return bars.slice(-n).map(x=>({
    t:iso(x[0]),
    o:off(x[1],level),h:off(x[2],level),l:off(x[3],level),c:off(x[4],level)
  }));
}
function relation(close,level,side){
  if(close===level)return"ON";
  if(side==="HIGH")return close>level?"BEYOND":"INSIDE";
  return close<level?"BEYOND":"INSIDE";
}
function reaction(packet){
  const bars=packet.windows.m1.filter(x=>x[0]>=packet.attackCloseTs&&x[0]+60000<=packet.decisionTs);
  const lvl=packet.levelPrice,side=packet.levelSide;
  const closes=bars.map(x=>x[4]),highs=bars.map(x=>x[2]),lows=bars.map(x=>x[3]);
  const beyond=closes.filter(c=>relation(c,lvl,side)==="BEYOND").length;
  const inside=closes.filter(c=>relation(c,lvl,side)==="INSIDE").length;
  const current=closes.length?closes[closes.length-1]:packet.attackClose;
  const maxBeyond=side==="HIGH"?Math.max(0,Math.max(...highs)-lvl):Math.max(0,lvl-Math.min(...lows));
  const maxInside=side==="HIGH"?Math.max(0,lvl-Math.min(...lows)):Math.max(0,Math.max(...highs)-lvl);
  return{
    observed_m1_bars:bars.length,
    closes_beyond:beyond,
    closes_inside:inside,
    final_relation:relation(current,lvl,side),
    final_offset_usd:off(current,lvl),
    max_excursion_beyond_usd:px(maxBeyond),
    max_excursion_inside_usd:px(maxInside),
    last_5_close_change_usd:px(change(bars,5))
  };
}
function levels(packet,current){
  return packet.causalLevelSnapshot
    .map(x=>({
      cls:x.levelClass,side:x.side,price:px(x.price),
      distance_from_current_usd:off(x.price,current),
      attacked_by_decision:x.attackedByDecision
    }))
    .sort((a,b)=>Math.abs(a.distance_from_current_usd)-Math.abs(b.distance_from_current_usd));
}
function localExtremes(packet){
  const b=packet.windows.m1.slice(-30);
  const hi=Math.max(...b.map(x=>x[2])),lo=Math.min(...b.map(x=>x[3]));
  return{recent_30m_high:px(hi),recent_30m_low:px(lo),range_usd:px(hi-lo)};
}

const raw=fs.readFileSync(INPUT,"utf8");
assert(sha256(raw)===EXPECTED_PACKET_SHA256,"packet_sha_mismatch");
const packets=raw.trim().split("\n").filter(Boolean).map(JSON.parse);
assert(packets.length===126,"packet_count");

const cards=packets.map(p=>{
  assert(p.futureDataIncluded===false&&p.outcomeFieldsIncluded===false,"outcome_leak:"+p.replayId);
  assert(p.maxPacketBarEndTs<=p.decisionTs,"future_bar:"+p.replayId);
  const current=p.windows.m1[p.windows.m1.length-1][4];
  return{
    replayId:p.replayId,eventHash:p.eventHash,era:p.era,eventDate:p.eventDate,sessionBucket:p.sessionBucket,
    level:{class:p.levelClass,side:p.levelSide,price:px(p.levelPrice)},
    attack:{
      start:iso(p.attackStartTs),close:iso(p.attackCloseTs),close_relation:p.attackCloseRelation,
      o:px(p.attackOpen),h:px(p.attackHigh),l:px(p.attackLow),c:px(p.attackClose)
    },
    decisionTs:iso(p.decisionTs),currentPrice:px(current),current_vs_level_usd:off(current,p.levelPrice),
    h1:summarizeTf(p.windows.h1),m15:summarizeTf(p.windows.m15),m5:summarizeTf(p.windows.m5),
    reaction:reaction(p),local:localExtremes(p),
    nearest_known_levels:levels(p,current).slice(0,6),
    recent_h1_vs_level:recentBars(p.windows.h1,6,p.levelPrice),
    recent_m15_vs_level:recentBars(p.windows.m15,8,p.levelPrice),
    recent_m5_vs_level:recentBars(p.windows.m5,12,p.levelPrice),
    post_attack_m1_vs_level:recentBars(
      p.windows.m1.filter(x=>x[0]>=p.attackCloseTs&&x[0]+60000<=p.decisionTs),20,p.levelPrice
    ),
    reviewStatus:"UNLABELED",outcomeFieldsIncluded:false
  };
});

const jsonText=cards.map(x=>JSON.stringify(x)).join("\n")+"\n";
fs.writeFileSync(OUT_JSON,jsonText);

let md="# EXP-047 Blinded Replay Review Deck v0.1\n\n";
md+="**Source packet SHA-256:** "+EXPECTED_PACKET_SHA256+"  \n";
md+="**Cards:** 126  \n";
md+="**Outcome fields:** none  \n\n";
md+="All OHLC offsets in compact recent-bar lists are USD relative to the attacked level.\n\n";

for(const c of cards){
  md+="## "+c.replayId+" — "+c.era+" — "+c.eventDate+" — "+c.level.class+" "+c.level.side+"\n\n";
  md+="- Decision: **UNLABELED**\n";
  md+="- Attack close: "+c.attack.close+"; decision: "+c.decisionTs+"\n";
  md+="- Level: "+c.level.price+"; current: "+c.currentPrice+"; current-vs-level: "+c.current_vs_level_usd+" USD\n";
  md+="- Attack relation: "+c.attack.close_relation+"; attack OHLC: "+[c.attack.o,c.attack.h,c.attack.l,c.attack.c].join("/")+"\n";
  md+="- H1: "+JSON.stringify(c.h1)+"\n";
  md+="- M15: "+JSON.stringify(c.m15)+"\n";
  md+="- M5: "+JSON.stringify(c.m5)+"\n";
  md+="- Post-attack reaction: "+JSON.stringify(c.reaction)+"\n";
  md+="- Local 30m: "+JSON.stringify(c.local)+"\n";
  md+="- Nearest known levels: "+JSON.stringify(c.nearest_known_levels)+"\n";
  md+="- Recent H1 offsets: "+JSON.stringify(c.recent_h1_vs_level)+"\n";
  md+="- Recent M15 offsets: "+JSON.stringify(c.recent_m15_vs_level)+"\n";
  md+="- Recent M5 offsets: "+JSON.stringify(c.recent_m5_vs_level)+"\n";
  md+="- Post-attack M1 offsets: "+JSON.stringify(c.post_attack_m1_vs_level)+"\n\n";
}
fs.writeFileSync(OUT_MD,md);

const summary={
  experiment:"EXP-047",stage:"blinded_review_deck_generation",
  input_packet_sha256:EXPECTED_PACKET_SHA256,packet_count:cards.length,
  review_cards_sha256:sha256(jsonText),review_deck_sha256:sha256(md),
  all_unlabeled:cards.every(x=>x.reviewStatus==="UNLABELED"),
  outcome_fields_included:false,disposition:"EXP047_REVIEW_DECK_READY"
};
fs.writeFileSync("research/results/EXP-047-blinded-replay-review-deck-summary-v0.1.json",JSON.stringify(summary,null,2)+"\n");
console.log(JSON.stringify(summary,null,2));
