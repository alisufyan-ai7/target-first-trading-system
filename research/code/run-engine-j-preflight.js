const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
require("./engine-j-v0.1.js");
const E=globalThis.EngineJv01;
if(!E)throw new Error("EngineJv01 missing");

const manifest=[
["xauusd_bid_m1_2022_12.csv","b654f2e8033584ba3aad37a9c197fae3fe044b08",2231796,44640],
["xauusd_bid_m1_2023_01.csv","ad56ac464c6844640a3f7ae4e5d8b3c7c30a4e33",2231952,44640],
["xauusd_bid_m1_2023_02.csv","95d40f88c4200f9163144e108aff0b03eb079a3b",2016006,40320],
["xauusd_bid_m1_2023_03.csv","5f2d85e197a9bf19b9aca7db49ec7dfdb6b466c7",2231984,44640],
["xauusd_bid_m1_2023_04.csv","9a3a8e99038d555880e7d2da7ad9047ba48850ff",2159920,43200],
["xauusd_bid_m1_2023_05.csv","95eadc1e3b8cb9636935e8d80e46384fa5ab3438",2231972,44640],
["xauusd_bid_m1_2023_06.csv","c603c32760c193c90c54906c2b388172c881616f",2159976,43200],
["xauusd_bid_m1_2023_07.csv","a24667621441f3fa400d1c9bcce4f4a32ee30a09",2231931,44640],
["xauusd_bid_m1_2023_08.csv","7f2838f0bb6212bea9aec1aca004d22fecaa141d",2231974,44640],
["xauusd_bid_m1_2023_09.csv","b37bd67b75e3fd59d1e818e0618f26d6929a9042",2159931,43200],
["xauusd_bid_m1_2023_10.csv","93a551f1e7371b7cc3f57ac3c50a2edb1e27c0d3",2231917,44640],
["xauusd_bid_m1_2023_11.csv","e739d6a6cdf868dc83d37406a6a7d068f29d5de4",2159884,43200],
["xauusd_bid_m1_2023_12.csv","56dbf8a5316c48f4ec3300126c0decda03f8325f",2231969,44640],
["xauusd_bid_m1_2024_01.csv","f439cc6e17e39addc1a464eb0ccf8fe2eb71de99",2231993,44640],
["xauusd_bid_m1_2024_02.csv","b3ad49d5e784fb8c879f8e12095640f454f8f5fb",2087847,41760],
["xauusd_bid_m1_2024_03.csv","cdd53e37cc41773cc0d5c9210daefbf5ef6c3535",2231983,44640],
["xauusd_bid_m1_2024_04.csv","f2e7801f91829e9aeeebbd88f9177350cc6ba043",2159936,43200],
["xauusd_bid_m1_2024_05.csv","b49cd640075396bf656578c52e7dac0d9e472a22",2232006,44640],
["xauusd_bid_m1_2024_06.csv","6c4dc31818a7e04d90f165df0930489cdf5e7121",2159852,43200],
["xauusd_bid_m1_2024_07.csv","1a9877d863a7cadcfb47388a2d7b6657b57873ed",2231718,44640],
["xauusd_bid_m1_2024_08.csv","29c3275f68b15d33325a7a989e322565fca4a64e",2231775,44640],
["xauusd_bid_m1_2024_09.csv","075fc0b3c4f01bfebdbdb21af82c66595c2fd6cc",2159940,43200],
["xauusd_bid_m1_2024_10.csv","ab734d9cea86c2441b2592e6aa0537829bd093f5",2231815,44640],
["xauusd_bid_m1_2024_11.csv","4fe07a39a96512d4264202d4817fafedb3b97e79",2159626,43200],
["xauusd_bid_m1_2024_12.csv","a5a219ccee1e3808593f349a56274d6242fe31dd",2231444,44640],
["xauusd_bid_m1_2025_01.csv","f0211e901b6f8b26996ba1a48aeba73f599bd5fe",2231746,44640],
["xauusd_bid_m1_2025_02.csv","e3beb3def6e2502975046d07f43db777604110b2",2015844,40320]
];

function assert(x,m){if(!x)throw new Error(m);}
function gitBlobSha(buf){
  const header=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(Buffer.concat([header,buf])).digest("hex");
}
function expectedMonthBounds(name,rows){
  const m=/_(\d{4})_(\d{2})\.csv$/.exec(name);assert(m,"bad_month_name:"+name);
  const y=Number(m[1]),mo=Number(m[2])-1,start=Date.UTC(y,mo,1);
  return[start,start+(rows-1)*60000];
}
function verifyCsv(name,buf,expectedRows){
  const lines=buf.toString("utf8").trimEnd().split("\n");
  assert(lines[0].trim()==="timestamp,open,high,low,close","bad_header:"+name);
  assert(lines.length===expectedRows+1,"bad_rows:"+name);
  let prev=null,first=null,last=null;
  for(let i=1;i<lines.length;i++){
    const p=lines[i].trim().split(",");assert(p.length===5,"bad_cols:"+name+":"+i);
    const ts=Number(p[0]);assert(Number.isInteger(ts)&&ts%60000===0,"bad_ts:"+name+":"+i);
    if(prev!==null)assert(ts-prev===60000,"gap:"+name+":"+i);
    prev=ts;if(first===null)first=ts;last=ts;
    const o=E.parseTick(p[1]),h=E.parseTick(p[2]),l=E.parseTick(p[3]),c=E.parseTick(p[4]);
    assert(o>0&&h>0&&l>0&&c>0&&h>=o&&h>=c&&l<=o&&l<=c&&h>=l,"bad_ohlc:"+name+":"+i);
  }
  const [wantFirst,wantLast]=expectedMonthBounds(name,expectedRows);
  assert(first===wantFirst,"bad_first_ts:"+name+":"+new Date(first).toISOString());
  assert(last===wantLast,"bad_last_ts:"+name+":"+new Date(last).toISOString());
  return{rows:expectedRows,first:new Date(first).toISOString(),last:new Date(last).toISOString()};
}

const tests=E.selfTest();
const dir=path.resolve("data/engine-j-v01");
const expectedNames=manifest.map(x=>x[0]).sort();
const actualNames=fs.readdirSync(dir).filter(x=>x.endsWith(".csv")).sort();
assert(JSON.stringify(actualNames)===JSON.stringify(expectedNames),"unexpected_data_files");

const files=[];
let totalRows=0,totalBytes=0;
for(const [name,sha,size,expectedRows] of manifest){
  const p=path.join(dir,name),buf=fs.readFileSync(p);
  assert(buf.length===size,"size_mismatch:"+name+":"+buf.length);
  const got=gitBlobSha(buf);assert(got===sha,"sha_mismatch:"+name+":"+got);
  const chronology=verifyCsv(name,buf,expectedRows);
  files.push({name,blob_sha:got,bytes:buf.length,...chronology});
  totalRows+=expectedRows;totalBytes+=buf.length;
}

const forbidden=[
"xauusd_bid_m1_2025_03.csv","xauusd_bid_m1_2025_04.csv","xauusd_bid_m1_2025_05.csv",
"xauusd_bid_m1_2025_06.csv","xauusd_bid_m1_2025_07.csv","xauusd_bid_m1_2025_08.csv",
"xauusd_bid_m1_2025_09.csv","xauusd_bid_m1_2025_10.csv","xauusd_bid_m1_2025_11.csv",
"xauusd_bid_m1_2025_12.csv","xauusd_bid_m1_2026_01.csv","xauusd_bid_m1_2026_02.csv"
];
const devRunner=fs.readFileSync("research/code/run-engine-j-development.js","utf8");
const devWorkflow=fs.readFileSync(".github/workflows/exp021-engine-j-development.yml","utf8");
for(const x of forbidden){
  assert(!devRunner.includes(x),"validation_holdout_name_in_runner:"+x);
  assert(!devWorkflow.includes(x),"validation_holdout_name_in_workflow:"+x);
}

const engineText=fs.readFileSync("research/code/engine-j-v0.1.js","utf8");
const engineSha256=crypto.createHash("sha256").update(engineText,"utf8").digest("hex");
assert(engineText.includes("5*compSum<=12*medianNum"),"missing_exact_compression_average");
assert(engineText.includes("2*boxWidth<=3*medianNum"),"missing_exact_compact_box");
assert(engineText.includes("8*R<5*s.medianNum"),"missing_exact_breakout_expansion");
assert(engineText.includes("previous30SameDay(active5,b)"),"missing_previous30_causal_path");
assert(engineText.includes("stop_before_target"),"missing_conservative_same_bar");
assert(engineText.includes("side_already_consumed_today"),"missing_first_side_consumption");
assert(engineText.includes('closeTs===dayStart(openTrade.fillTs)+20*60*MIN'),"missing_chronological_session_close");
assert(!/EngineIv0|EngineHv0|EngineGv0/.test(engineText),"cross_engine_export_contamination");

const out={
  experiment:"EXP-021",
  engine:"Engine J v0.1",
  checkpoint:"preflight_before_outcomes",
  engine_outcomes_calculated:false,
  development_backtest_run:false,
  validation_or_holdout_loaded:false,
  tested_repository_sha:process.env.GITHUB_SHA||null,
  engine_file_sha256:engineSha256,
  source_repo:"kevingtlin/Market-Data-Lab",
  source_commit:"922f83a60cc574e7395fb27397077288055a1ef6",
  self_test:tests,
  manifest:{file_count:files.length,total_rows:totalRows,total_bytes:totalBytes,files},
  harness_checks:{
    exact_development_file_set:true,
    validation_holdout_names_absent:true,
    exact_integer_compression:true,
    exact_integer_breakout_expansion:true,
    candidate_excludes_breakout_bar:true,
    conservative_same_bar_present:true,
    first_side_consumption_present:true,
    chronological_session_close_present:true,
    cross_engine_export_contamination:false
  }
};
fs.mkdirSync("research/results",{recursive:true});
fs.writeFileSync("research/results/EXP-021-preflight-v0.1.json",JSON.stringify(out,null,2)+"\n");
console.log("EXP021_PREFLIGHT_OK",JSON.stringify({files:files.length,totalRows,tests:tests.tests.length,outcomes:false}));
