const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
require("./engine-h-v0.3.js");
const E=globalThis.EngineHv03;
if(!E) throw new Error("EngineHv03 missing");
E.selfTest();

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

function gitBlobSha(buf){
  const header=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(Buffer.concat([header,buf])).digest("hex");
}
function pctile(a,p){
  if(!a.length)return null;
  const b=[...a].sort((x,y)=>x-y),z=(b.length-1)*p,l=Math.floor(z),h=Math.ceil(z);
  return l===h?b[l]:b[l]+(b[h]-b[l])*(z-l);
}
function dist(a){
  if(!a.length)return{n:0,mean:null,median:null,p10:null,p90:null,min:null,max:null};
  return{n:a.length,mean:a.reduce((x,y)=>x+y,0)/a.length,median:pctile(a,.5),p10:pctile(a,.1),p90:pctile(a,.9),min:Math.min(...a),max:Math.max(...a)};
}
function utcDate(ts){return new Date(ts).toISOString().slice(0,10);}
function summarizeSubperiod(metrics,start,end){
  const trades=metrics.trades.filter(t=>t.sweepTs>=start&&t.sweepTs<end);
  const setups=metrics.setups.filter(s=>(s.sweepTs||s.terminalTs||0)>=start&&(s.sweepTs||s.terminalTs||0)<end);
  const reasons={};for(const s of setups)if(s.terminal)reasons[s.terminal]=(reasons[s.terminal]||0)+1;
  const exits={};for(const t of trades)exits[t.exitReason]=(exits[t.exitReason]||0)+1;
  const labels={};for(const d of[3000,4000,5000,7000,10000]){
    const a=trades.map(t=>t.labels[d]);labels[d]={target:a.filter(x=>x==="target_before_stop").length,stop:a.filter(x=>x==="stop_before_target").length,horizon:a.filter(x=>x==="horizon_without_target_or_stop").length,n:a.length};
  }
  const ds=metrics.daily_series.filter(x=>{
    const ts=Date.parse(x.date+"T00:00:00Z");return ts>=start&&ts<end;
  });
  const dv=ds.map(x=>x.netUSD500);
  const avg=f=>trades.length?trades.reduce((s,t)=>s+t[f],0)/trades.length:null;
  const pf=f=>{let p=0,n=0;for(const t of trades){const x=t[f];if(x>0)p+=x;else if(x<0)n-=x;}return n?p/n:(p>0?Infinity:null);};
  let eq=500,peak=500,mdd=0;for(const t of [...trades].sort((a,b)=>a.fillTs-b.fillTs)){eq+=t.netUSD500;peak=Math.max(peak,eq);mdd=Math.max(mdd,peak-eq);}
  let bn=0,bl=0,cn=0,cl=0;for(const t of [...trades].sort((a,b)=>a.fillTs-b.fillTs)){if(t.netUSD500<0){cn++;cl+=t.netUSD500;if(cn>bn||(cn===bn&&cl<bl)){bn=cn;bl=cl;}}else{cn=0;cl=0;}}
  const direction={};for(const t of trades){if(!direction[t.dir])direction[t.dir]={n:0,netUSD500:0};direction[t.dir].n++;direction[t.dir].netUSD500+=t.netUSD500;}
  return{
    split:{start:new Date(start).toISOString(),end_exclusive:new Date(end).toISOString()},
    setup_count:setups.length,terminal_reasons:reasons,accepted_filled_trades:trades.length,exits,
    target_hit_rate:trades.length?(exits.exit_t40||0)/trades.length:null,
    stop_rate:trades.length?((exits.exit_stop||0)+(exits.exit_stop_entry_bar||0))/trades.length:null,
    timeout_rate:trades.length?((exits.exit_timeout_120||0)+(exits.exit_session_2000||0)+(exits.exit_data_end||0))/trades.length:null,
    label_rates:labels,
    expectancy:{gross_usd:avg("grossUSD"),net_usd_0:avg("netUSD0"),net_usd_025:avg("netUSD250"),net_usd_050:avg("netUSD500")},
    profit_factor:{gross:pf("grossUSD"),net_0:pf("netUSD0"),net_025:pf("netUSD250"),net_050:pf("netUSD500")},
    total_net_usd_050:trades.reduce((s,t)=>s+t.netUSD500,0),
    weekdays:ds.length,
    daily:{mean:dv.length?dv.reduce((a,b)=>a+b,0)/dv.length:null,median:pctile(dv,.5),losing_pct:dv.length?dv.filter(x=>x<0).length/dv.length:null,le50_pct:dv.length?dv.filter(x=>x<=50).length/dv.length:null,ge100_pct:dv.length?dv.filter(x=>x>=100).length/dv.length:null,ge150_pct:dv.length?dv.filter(x=>x>=150).length/dv.length:null,ge200_pct:dv.length?dv.filter(x=>x>=200).length/dv.length:null},
    max_drawdown_usd:mdd,worst_losing_trade_run:{count:bn,netLoss:bl},
    actual_mfe_ticks:dist(trades.map(t=>t.actualMFE)),actual_mae_ticks:dist(trades.map(t=>t.actualMAE)),
    potential_mfe_ticks:dist(trades.map(t=>t.potentialMFE)),potential_mae_ticks:dist(trades.map(t=>t.potentialMAE)),
    stop_distance_ticks:dist(trades.map(t=>t.stopDist)),gross_stop_usd:dist(trades.map(t=>t.stopDist*0.01)),
    location_fvg_age_active5:dist(trades.map(t=>t.locationFvgAge)),location_distance_ticks:dist(trades.map(t=>t.locationDistance)),
    opposite_range_delta_ticks:dist(trades.map(t=>t.oppositeRangeDelta)),direction
  };
}

const dir=path.resolve("data/engine-h-v03"),months=[];
for(const [name,sha,size,expectedRows] of manifest){
  const p=path.join(dir,name),buf=fs.readFileSync(p);
  if(buf.length!==size)throw new Error("size_mismatch:"+name+":"+buf.length);
  const got=gitBlobSha(buf);if(got!==sha)throw new Error("sha_mismatch:"+name+":"+got);
  months.push({name,content:buf.toString("utf8"),expectedRows});
}

const combinedStart=Date.UTC(2023,0,1),combinedEnd=Date.UTC(2025,2,1);
const metrics=E.runEngineH(months,combinedStart,combinedEnd);
const bootstrap=E.bootstrap(metrics,10000,19019);
const devA=summarizeSubperiod(metrics,Date.UTC(2023,0,1),Date.UTC(2024,0,1));
const devB=summarizeSubperiod(metrics,Date.UTC(2024,0,1),Date.UTC(2025,2,1));

const out={...metrics,bootstrap,development_subperiods:{DEV_A_2023:devA,DEV_B_2024_to_2025_02:devB},execution_metadata:{
  engine_implementation:"research/code/engine-h-v0.3.js",
  data_source_repo:"kevingtlin/Market-Data-Lab",
  data_source_commit:"922f83a60cc574e7395fb27397077288055a1ef6",
  split:"combined_development_2023_01_to_2025_02",
  validation_or_holdout_loaded:false
}};
delete out.trades;delete out.setups;delete out.daily_series;

fs.mkdirSync("research/results",{recursive:true});
fs.writeFileSync("research/results/EXP-019-development-summary-v0.3.json",JSON.stringify(out,null,2)+"\n");
fs.writeFileSync("research/results/EXP-019-development-setups-v0.3.jsonl",metrics.setups.map(x=>JSON.stringify(x)).join("\n")+"\n");
fs.writeFileSync("research/results/EXP-019-development-trades-v0.3.jsonl",metrics.trades.map(x=>JSON.stringify(x)).join("\n")+"\n");

console.log("EXP019_DEVELOPMENT_SUMMARY",JSON.stringify({
  accepted_filled_trades:metrics.accepted_filled_trades,
  t40_hit_rate:metrics.target_hit_rate,
  net_expectancy_usd_050:metrics.expectancy.net_usd_050,
  net_profit_factor_050:metrics.profit_factor.net_050,
  total_net_usd_050:metrics.total_net_usd_050,
  dev_a_trades:devA.accepted_filled_trades,
  dev_a_expectancy_050:devA.expectancy.net_usd_050,
  dev_b_trades:devB.accepted_filled_trades,
  dev_b_expectancy_050:devB.expectancy.net_usd_050,
  max_drawdown_usd:metrics.max_drawdown_usd,
  bootstrap_expectancy_95:[bootstrap.expectancy_net_usd_050.lo,bootstrap.expectancy_net_usd_050.hi]
}));
