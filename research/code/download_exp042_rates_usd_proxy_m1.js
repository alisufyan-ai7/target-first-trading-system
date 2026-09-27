#!/usr/bin/env node
"use strict";

const fs=require("fs");
const path=require("path");
const {once}=require("events");
const {getHistoricalRates}=require("dukascopy-node");

const INSTRUMENTS=[
  {name:"DOLLARIDXUSD",id:"dollaridxusd"},
  {name:"USTBONDTRUSD",id:"ustbondtrusd"}
];
const FROM=new Date("2025-07-01T00:00:00.000Z");
const TO=new Date("2026-06-30T00:00:00.000Z");
const OUTDIR=process.env.EXP042_DATA_DIR||"/tmp/exp042-rates-usd";

async function writeCsv(name,rows){
  fs.mkdirSync(OUTDIR,{recursive:true});
  const out=path.join(OUTDIR,name+".csv");
  const ws=fs.createWriteStream(out,{encoding:"utf8"});
  ws.write("datetime,open,high,low,close,volume\n");
  let kept=0,prev=null;
  for(const row of rows){
    if(!Array.isArray(row)||row.length<6) throw new Error(name+": malformed row");
    const ms=Number(row[0]);
    if(!Number.isFinite(ms)) throw new Error(name+": invalid timestamp");
    if(ms<FROM.getTime()||ms>=TO.getTime()) continue;
    if(prev!==null&&ms<prev) throw new Error(name+": non-monotonic source rows");
    prev=ms;
    const nums=row.slice(1,6).map(Number);
    if(nums.some(v=>!Number.isFinite(v))) throw new Error(name+": invalid numeric row");
    const line=[new Date(ms).toISOString(),...nums].join(",")+"\n";
    if(!ws.write(line)) await once(ws,"drain");
    kept++;
  }
  ws.end();
  await once(ws,"finish");
  if(kept===0) throw new Error(name+": zero rows kept");
  return {out,kept};
}

(async()=>{
  console.log(JSON.stringify({
    source:"Dukascopy via dukascopy-node",
    package_version:"1.50.0",
    from:FROM.toISOString(),
    to_exclusive:TO.toISOString(),
    timeframe:"m1",
    instruments:INSTRUMENTS,
    outdir:OUTDIR
  },null,2));

  for(const x of INSTRUMENTS){
    console.log("Downloading "+x.name+" / "+x.id);
    const rows=await getHistoricalRates({
      instrument:x.id,
      dates:{from:FROM,to:TO},
      timeframe:"m1",
      format:"array",
      batchSize:10,
      pauseBetweenBatchesMs:1000
    });
    if(!Array.isArray(rows)) throw new Error(x.name+": expected array");
    const info=await writeCsv(x.name,rows);
    console.log(x.name+": source rows="+rows.length+" normalized="+info.kept);
  }
})().catch(err=>{
  console.error(err&&err.stack?err.stack:err);
  process.exit(1);
});
