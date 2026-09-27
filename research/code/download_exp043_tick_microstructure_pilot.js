#!/usr/bin/env node
"use strict";

const fs=require("fs");
const path=require("path");
const {once}=require("events");
const {getHistoricalRates}=require("dukascopy-node");

const MARKETS=[
  ["XAUUSD","xauusd"],
  ["EURUSD","eurusd"],
  ["GBPUSD","gbpusd"],
  ["USDJPY","usdjpy"],
  ["EURJPY","eurjpy"],
  ["AUDUSD","audusd"],
  ["USDCAD","usdcad"],
  ["USDCHF","usdchf"],
];

const DATES=[
  "2025-07-09",
  "2025-09-10",
  "2025-11-12",
  "2026-01-14",
  "2026-03-11",
  "2026-05-13",
];

const OUTDIR=process.env.EXP043_TICK_DIR||"/tmp/exp043-ticks";

function dayRange(d){
  const from=new Date(d+"T00:00:00.000Z");
  const to=new Date(from.getTime()+24*60*60*1000);
  return {from,to};
}

async function writeCanonical(file,rows){
  fs.mkdirSync(path.dirname(file),{recursive:true});
  const ws=fs.createWriteStream(file,{encoding:"utf8"});
  ws.write("timestamp_ms,ask_price,bid_price,ask_volume,bid_volume\n");
  let n=0;
  let prev=null;
  for(const r of rows){
    const ts=Number(r.timestamp);
    const ask=Number(r.askPrice);
    const bid=Number(r.bidPrice);
    const av=Number(r.askVolume);
    const bv=Number(r.bidVolume);
    if(!Number.isFinite(ts)||!Number.isFinite(ask)||!Number.isFinite(bid)||!Number.isFinite(av)||!Number.isFinite(bv)){
      throw new Error("non-finite tick field");
    }
    if(prev!==null && ts<prev) throw new Error("source timestamps decreased");
    prev=ts;
    const line=[String(ts),String(ask),String(bid),String(av),String(bv)].join(",")+"\n";
    if(!ws.write(line)) await once(ws,"drain");
    n++;
  }
  ws.end();
  await once(ws,"finish");
  if(n===0) throw new Error("zero canonical ticks");
  return n;
}

(async()=>{
  console.log(JSON.stringify({
    source:"Dukascopy via dukascopy-node",
    package_version:"1.50.0",
    timeframe:"tick",
    dates:DATES,
    markets:MARKETS,
    outdir:OUTDIR
  },null,2));

  for(const [name,id] of MARKETS){
    for(const d of DATES){
      const {from,to}=dayRange(d);
      console.log("Downloading "+name+" "+d);
      let data=await getHistoricalRates({
        instrument:id,
        dates:{from,to},
        timeframe:"tick",
        format:"json",
        batchSize:10,
        pauseBetweenBatchesMs:500
      });
      if(typeof data==="string") data=JSON.parse(data);
      if(!Array.isArray(data)) throw new Error(name+" "+d+": expected array");
      const file=path.join(OUTDIR,name,d+".csv");
      const n=await writeCanonical(file,data);
      console.log(name+" "+d+": "+n+" ticks");
    }
  }
})().catch(err=>{
  console.error(err&&err.stack?err.stack:err);
  process.exit(1);
});
