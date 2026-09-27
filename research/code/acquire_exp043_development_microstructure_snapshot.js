#!/usr/bin/env node
"use strict";

const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
const {once}=require("events");
const {getHistoricalRates}=require("dukascopy-node");

const MARKETS=[
  ["XAUUSD","xauusd"],["EURUSD","eurusd"],["GBPUSD","gbpusd"],["USDJPY","usdjpy"],
  ["EURJPY","eurjpy"],["AUDUSD","audusd"],["USDCAD","usdcad"],["USDCHF","usdchf"]
];
const START=new Date("2025-07-01T00:00:00.000Z");
const END=new Date("2026-06-30T00:00:00.000Z");
const SESSION_START_MIN=5*60;
const SESSION_END_MIN=18*60;
const OUTDIR=process.env.EXP043_OUTDIR||"/tmp/exp043-microstructure";

const HEADER=[
  "minute_start_utc","tick_count","distinct_timestamp_count",
  "median_interarrival_ms","p90_interarrival_ms",
  "spread_bps_median","spread_bps_p90","spread_bps_last","last_quote_age_ms",
  "bid_update_count","ask_update_count","both_price_update_count",
  "bid_volume_median","ask_volume_median",
  "signed_quote_imbalance_mean","signed_quote_imbalance_median",
  "bid_heavy_fraction","ask_heavy_fraction"
];

function utcDateString(d){ return d.toISOString().slice(0,10); }
function isWeekday(d){ const x=d.getUTCDay(); return x>=1&&x<=5; }
function dayAt(date,minutes){
  return new Date(Date.UTC(date.getUTCFullYear(),date.getUTCMonth(),date.getUTCDate(),0,0,0,0)+minutes*60000);
}
function weekdays(){
  const out=[];
  for(let t=new Date(START);t<END;t=new Date(t.getTime()+86400000)){
    if(isWeekday(t)) out.push(new Date(t));
  }
  return out;
}
function q(sorted,p){
  if(sorted.length===0) return null;
  if(sorted.length===1) return sorted[0];
  const k=(sorted.length-1)*p;
  const lo=Math.floor(k), hi=Math.ceil(k);
  if(lo===hi) return sorted[lo];
  return sorted[lo]*(hi-k)+sorted[hi]*(k-lo);
}
function median(vals){
  if(vals.length===0) return null;
  const x=vals.slice().sort((a,b)=>a-b);
  return q(x,0.5);
}
function quant(vals,p){
  if(vals.length===0) return null;
  const x=vals.slice().sort((a,b)=>a-b);
  return q(x,p);
}
function fmt(v){
  if(v===null||v===undefined||Number.isNaN(v)) return "";
  if(Number.isInteger(v)) return String(v);
  return String(v);
}
function canonicalTickLine(ts,ask,bid,av,bv){
  return [String(ts),String(ask),String(bid),String(av),String(bv)].join(",")+"\n";
}

function newBucket(ms){
  return {
    ms,tickCount:0,distinctTs:0,lastTs:null,
    inter:[],spreads:[],bidVol:[],askVol:[],imb:[],
    bidHeavy:0,askHeavy:0,validImb:0,
    bidUpd:0,askUpd:0,bothUpd:0,
    prevBid:null,prevAsk:null,lastSpread:null,lastTick:null
  };
}
function addTick(b,ts,ask,bid,av,bv){
  const mid=(ask+bid)/2;
  const spread=10000*(ask-bid)/mid;
  b.tickCount++;
  if(b.lastTs===null||ts!==b.lastTs) b.distinctTs++;
  if(b.lastTs!==null) b.inter.push(ts-b.lastTs);
  if(b.prevBid!==null){
    const bc=bid!==b.prevBid, ac=ask!==b.prevAsk;
    if(bc)b.bidUpd++;
    if(ac)b.askUpd++;
    if(bc&&ac)b.bothUpd++;
  }
  b.spreads.push(spread);
  b.bidVol.push(bv); b.askVol.push(av);
  const den=av+bv;
  if(den>0){
    const z=(bv-av)/den;
    b.imb.push(z);b.validImb++;
    if(z>0)b.bidHeavy++;
    else if(z<0)b.askHeavy++;
  }
  b.lastSpread=spread;b.lastTick=ts;b.lastTs=ts;b.prevBid=bid;b.prevAsk=ask;
}
function finalize(b){
  const interMed=b.inter.length>=2?median(b.inter):null;
  const interP90=b.inter.length>=2?quant(b.inter,0.9):null;
  const imbMean=b.imb.length?b.imb.reduce((a,x)=>a+x,0)/b.imb.length:null;
  const imbMed=b.imb.length?median(b.imb):null;
  return [
    new Date(b.ms).toISOString(),b.tickCount,b.distinctTs,
    interMed,interP90,
    median(b.spreads),quant(b.spreads,0.9),b.lastSpread,(b.ms+60000)-b.lastTick,
    b.bidUpd,b.askUpd,b.bothUpd,
    median(b.bidVol),median(b.askVol),
    imbMean,imbMed,
    b.validImb?b.bidHeavy/b.validImb:null,
    b.validImb?b.askHeavy/b.validImb:null
  ].map(fmt).join(",")+"\n";
}

async function fetchDay(id,date){
  const from=dayAt(date,SESSION_START_MIN);
  const to=dayAt(date,SESSION_END_MIN);
  let data=await getHistoricalRates({
    instrument:id,
    dates:{from,to},
    timeframe:"tick",
    format:"json",
    batchSize:24,
    pauseBetweenBatchesMs:100
  });
  if(typeof data==="string") data=JSON.parse(data);
  if(!Array.isArray(data)) throw new Error(id+" "+utcDateString(date)+": expected array");
  return {from,to,data};
}

async function main(){
  fs.mkdirSync(OUTDIR,{recursive:true});
  const days=weekdays();
  const manifest={
    snapshot_id:"EXP-043 development quote/tick microstructure minute snapshot v1",
    created_from_repository_sha:process.env.GITHUB_SHA||null,
    source:{
      authority:"Dukascopy Bank historical tick/quote data",
      transport_helper:"dukascopy-node",
      transport_version:"1.50.0",
      timeframe:"tick",
      semantics:"broker quote/tick microstructure proxy; not centralized traded order flow"
    },
    interval:["2025-07-01T00:00:00Z","2026-06-30T00:00:00Z"],
    session_utc:["05:00:00","18:00:00"],
    requested_weekdays:days.map(utcDateString),
    markets:{}
  };
  console.log("Requested weekdays:",days.length);

  for(const [name,id] of MARKETS){
    const file=path.join(OUTDIR,name+".csv");
    const ws=fs.createWriteStream(file,{encoding:"utf8"});
    ws.write(HEADER.join(",")+"\n");
    const entries=[];
    let aggregateRows=0,totalTicks=0;

    for(let di=0;di<days.length;di++){
      const d=days[di], ds=utcDateString(d);
      console.log(name,ds,di+1+"/"+days.length);
      const {from,to,data}=await fetchDay(id,d);
      const rawHash=crypto.createHash("sha256");
      let rawCount=0,first=null,last=null,prev=null;
      let bucket=null;

      for(const r of data){
        const ts=Number(r.timestamp),ask=Number(r.askPrice),bid=Number(r.bidPrice),
              av=Number(r.askVolume),bv=Number(r.bidVolume);
        if(![ts,ask,bid,av,bv].every(Number.isFinite)) throw new Error(name+" "+ds+": nonfinite tick");
        if(ts<from.getTime()||ts>=to.getTime()) continue;
        if(prev!==null&&ts<prev) throw new Error(name+" "+ds+": timestamp decrease");
        if(!(ask>0&&bid>0&&ask>=bid&&av>=0&&bv>=0)) throw new Error(name+" "+ds+": invalid quote");
        prev=ts;
        rawHash.update(canonicalTickLine(ts,ask,bid,av,bv));
        rawCount++; totalTicks++;
        if(first===null)first=ts; last=ts;

        const ms=Math.floor(ts/60000)*60000;
        if(bucket===null) bucket=newBucket(ms);
        if(ms!==bucket.ms){
          if(ms<bucket.ms) throw new Error(name+" "+ds+": minute decrease");
          if(!ws.write(finalize(bucket))) await once(ws,"drain");
          aggregateRows++;
          bucket=newBucket(ms);
        }
        addTick(bucket,ts,ask,bid,av,bv);
      }
      if(bucket!==null){
        if(!ws.write(finalize(bucket))) await once(ws,"drain");
        aggregateRows++;
      }

      entries.push({
        date:ds,
        request_start_utc:from.toISOString(),
        request_end_utc_exclusive:to.toISOString(),
        tick_count:rawCount,
        raw_canonical_sha256:rawHash.digest("hex"),
        first_tick_timestamp_ms:first,
        last_tick_timestamp_ms:last,
        no_data:rawCount===0
      });
    }
    ws.end(); await once(ws,"finish");
    manifest.markets[name]={
      instrument_id:id,
      aggregate_file:name+".csv",
      aggregate_rows:aggregateRows,
      total_source_ticks:totalTicks,
      days:entries
    };
  }

  fs.writeFileSync(path.join(OUTDIR,"SOURCE-MANIFEST.json"),JSON.stringify(manifest,null,2)+"\n");
  console.log(JSON.stringify({
    outdir:OUTDIR,
    markets:Object.fromEntries(MARKETS.map(([n])=>[n,{
      rows:manifest.markets[n].aggregate_rows,
      ticks:manifest.markets[n].total_source_ticks
    }]))
  },null,2));
}

main().catch(err=>{
  console.error(err&&err.stack?err.stack:err);
  process.exit(1);
});
