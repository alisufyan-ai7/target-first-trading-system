#!/usr/bin/env node
"use strict";

const fs=require("fs");
const path=require("path");
const {once}=require("events");
const {getHistoricalRates}=require("dukascopy-node");

const SYMBOLS=["XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCAD","USDCHF"];
const FROM=new Date("2026-03-23T00:00:00.000Z");
const TO=new Date("2026-07-01T00:00:00.000Z");
const OUTDIR=process.env.EXP041_DIAG_DIR||"/tmp/exp041-cross-feed";

async function writeCsv(symbol,rows){
  fs.mkdirSync(OUTDIR,{recursive:true});
  const out=path.join(OUTDIR,symbol+".csv");
  const ws=fs.createWriteStream(out,{encoding:"utf8"});
  ws.write("datetime,open,high,low,close,volume\n");
  let n=0;
  for(const row of rows){
    const ms=Number(row[0]);
    if(ms<FROM.getTime()||ms>=TO.getTime()) continue;
    const nums=row.slice(1,6).map(Number);
    if(!Number.isFinite(ms)||nums.some(v=>!Number.isFinite(v))) throw new Error(symbol+": invalid row");
    if(!ws.write([new Date(ms).toISOString(),...nums].join(",")+"\n")) await once(ws,"drain");
    n++;
  }
  ws.end(); await once(ws,"finish");
  if(!n) throw new Error(symbol+": zero rows");
  console.log(symbol+": "+n+" rows");
}

(async()=>{
  for(const symbol of SYMBOLS){
    const rows=await getHistoricalRates({
      instrument:symbol.toLowerCase(),
      dates:{from:FROM,to:TO},
      timeframe:"m1",
      format:"array",
      batchSize:10,
      pauseBetweenBatchesMs:1000
    });
    await writeCsv(symbol,rows);
  }
})().catch(e=>{console.error(e.stack||e);process.exit(1);});
