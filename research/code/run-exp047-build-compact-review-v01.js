#!/usr/bin/env node
"use strict";
const fs=require("fs");
const crypto=require("crypto");
const IN="research/results/EXP-047-blinded-replay-review-cards-v0.1.jsonl";
const EXPECTED="965c9ff4ef2a3eab32df6dafa05f8d0b5d61c43aa210f923d0c255a8ae915879";
function sha256(s){return crypto.createHash("sha256").update(s).digest("hex");}
function closes(a){return a.map(x=>x.c);}
const raw=fs.readFileSync(IN,"utf8");
if(sha256(raw)!==EXPECTED)throw new Error("review_cards_changed");
const cards=raw.trim().split("\n").filter(Boolean).map(JSON.parse);
if(cards.length!==126)throw new Error("card_count");
const compact=cards.map(c=>({
  replayId:c.replayId,era:c.era,date:c.eventDate,session:c.sessionBucket,
  level:c.level,attack_relation:c.attack.close_relation,
  attack_ohlc:[c.attack.o,c.attack.h,c.attack.l,c.attack.c],
  current:c.currentPrice,current_vs_level:c.current_vs_level_usd,
  h1:c.h1,m15:c.m15,m5:c.m5,reaction:c.reaction,local:c.local,
  levels:c.nearest_known_levels,
  h1_closes_vs_level:closes(c.recent_h1_vs_level),
  m15_closes_vs_level:closes(c.recent_m15_vs_level),
  m5_closes_vs_level:closes(c.recent_m5_vs_level),
  m1_post_attack_closes_vs_level:closes(c.post_attack_m1_vs_level),
  m1_post_attack_highs_vs_level:c.post_attack_m1_vs_level.map(x=>x.h),
  m1_post_attack_lows_vs_level:c.post_attack_m1_vs_level.map(x=>x.l),
  reviewStatus:"UNLABELED",outcomeFieldsIncluded:false
}));
const out=compact.map(x=>JSON.stringify(x)).join("\n")+"\n";
fs.writeFileSync("research/results/EXP-047-blinded-replay-compact-review-v0.1.jsonl",out);
fs.writeFileSync("research/results/EXP-047-blinded-replay-compact-review-summary-v0.1.json",
  JSON.stringify({
    experiment:"EXP-047",stage:"compact_blinded_review",
    input_review_cards_sha256:EXPECTED,count:compact.length,
    compact_sha256:sha256(out),all_unlabeled:true,outcome_fields_included:false,
    disposition:"EXP047_COMPACT_REVIEW_READY"
  },null,2)+"\n");
console.log("EXP047_COMPACT_REVIEW_READY",compact.length,sha256(out));
