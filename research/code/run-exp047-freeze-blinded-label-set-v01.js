#!/usr/bin/env node
"use strict";

const fs=require("fs");
const crypto=require("crypto");

const PARTS=[
  ["research/results/EXP-047-blinded-replay-labels-v0.1-part1.jsonl","028937653bf035bf0935e0fba905851631821342"],
  ["research/results/EXP-047-blinded-replay-labels-v0.1-part2.jsonl","9967f9337a2795327ae33a4821ca45d16a06090d"],
  ["research/results/EXP-047-blinded-replay-labels-v0.1-part3.jsonl","ebe5b3e661c0925df44de8642192e1d9bd5c50fe"]
];
const OUT="research/results/EXP-047-blinded-replay-labels-v0.1.jsonl";
const SUMMARY="research/results/EXP-047-blinded-replay-label-summary-v0.1.json";

function assert(c,m){if(!c)throw new Error(m);}
function sha256(buf){return crypto.createHash("sha256").update(buf).digest("hex");}
function gitBlobSha(buf){
  const h=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(Buffer.concat([h,buf])).digest("hex");
}
function countBy(xs,key){const o={};for(const x of xs){const k=key(x);o[k]=(o[k]||0)+1;}return o;}

let raw="";
for(const [p,blob] of PARTS){
  const b=fs.readFileSync(p);
  assert(gitBlobSha(b)===blob,"part_blob_changed:"+p);
  raw+=b.toString("utf8");
}
assert(raw.endsWith("\n"),"combined_missing_final_newline");
const labels=raw.trim().split("\n").filter(Boolean).map(JSON.parse);
assert(labels.length===126,"label_count:"+labels.length);

const seen=new Set();
for(let i=0;i<labels.length;i++){
  const x=labels[i],expected="R"+String(i+1).padStart(3,"0");
  assert(x.replayId===expected,"sequence:"+i+":"+x.replayId+":"+expected);
  assert(!seen.has(x.replayId),"duplicate:"+x.replayId);seen.add(x.replayId);
  assert(["NO_TRADE","LONG","SHORT"].includes(x.decision),"decision:"+x.replayId);
  const forbidden=["outcome","pnl","mfe","mae","win","loss","realizedR","futurePath"];
  for(const k of forbidden)assert(!(k in x),"outcome_field:"+x.replayId+":"+k);
  if(x.decision==="NO_TRADE"){
    assert(typeof x.reason==="string"&&x.reason.length>0,"no_trade_reason:"+x.replayId);
    assert(typeof x.dominantConflict==="string"&&x.dominantConflict.length>0,"no_trade_conflict:"+x.replayId);
  }else{
    assert(["A","B","C"].includes(x.confidence),"confidence:"+x.replayId);
    assert(["MARKET_NEXT_OPEN","LEVEL_RETEST","FVG_RETRACE","OTHER_CAUSAL_LIMIT"].includes(x.entryStyle),"entry_style:"+x.replayId);
    assert(Number.isFinite(x.entryPrice)&&Number.isFinite(x.stopPrice)&&Number.isFinite(x.tp1Price),"trade_prices:"+x.replayId);
    assert(typeof x.rationale==="string"&&x.rationale.length>0,"rationale:"+x.replayId);
    assert(typeof x.counterEvidence==="string"&&x.counterEvidence.length>0,"counter:"+x.replayId);
    if(x.decision==="LONG"){
      assert(x.stopPrice<x.entryPrice,"long_stop:"+x.replayId);
      assert(x.tp1Price>x.entryPrice,"long_tp:"+x.replayId);
    }else{
      assert(x.stopPrice>x.entryPrice,"short_stop:"+x.replayId);
      assert(x.tp1Price<x.entryPrice,"short_tp:"+x.replayId);
    }
  }
}

const decisionCounts=countBy(labels,x=>x.decision);
const trades=labels.filter(x=>x.decision!=="NO_TRADE");
const confidenceCounts=countBy(trades,x=>x.confidence);
const entryStyleCounts=countBy(trades,x=>x.entryStyle);
const gate={
  all_126_labeled:labels.length===126,
  trade_labels_ge_30:trades.length>=30,
  long_ge_10:(decisionCounts.LONG||0)>=10,
  short_ge_10:(decisionCounts.SHORT||0)>=10,
  a_or_b_ge_20:trades.filter(x=>x.confidence==="A"||x.confidence==="B").length>=20,
  all_trade_labels_have_causal_entry_stop_target:trades.every(x=>
    Number.isFinite(x.entryPrice)&&Number.isFinite(x.stopPrice)&&Number.isFinite(x.tp1Price)
  ),
  no_outcome_fields:true
};
gate.pass=Object.values(gate).every(Boolean);

fs.writeFileSync(OUT,raw);
const summary={
  experiment:"EXP-047",
  stage:"blinded_label_set_frozen",
  parent_protocol_commit:"e5792f4d5980d288d339a82dc1271981534b7867",
  reviewer_rubric_commit:"688f90e8d81eed9dd6098b11f377e4f88e423564",
  packet_checkpoint_commit:"58ed6163c925b9081b35e53fd46dfa1043653bf6",
  compact_review_checkpoint_commit:"5b6ee178bf9f51e8c8415909574e7ee0c9366aab",
  source_part_blobs:Object.fromEntries(PARTS),
  label_count:labels.length,
  decision_counts:decisionCounts,
  trade_labels:trades.length,
  confidence_counts:confidenceCounts,
  entry_style_counts:entryStyleCounts,
  label_jsonl_sha256:sha256(Buffer.from(raw,"utf8")),
  validation_or_holdout_loaded:false,
  post_decision_path_loaded:false,
  target_outcomes_evaluated:false,
  feasibility_gate:gate,
  disposition:gate.pass
    ?"EXP047_BLINDED_LABEL_SET_FROZEN_READY_FOR_OUTCOME_EVALUATION"
    :"EXP047_BLINDED_LABEL_SET_FEASIBILITY_FAIL"
};
fs.writeFileSync(SUMMARY,JSON.stringify(summary,null,2)+"\n");
console.log(JSON.stringify(summary,null,2));
