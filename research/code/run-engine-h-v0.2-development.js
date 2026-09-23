const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
require("./engine-h-v0.2.js");
const E=globalThis.EngineHv02;
if(!E) throw new Error("EngineHv02 missing");
E.selfTest();

const manifest=[
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
  const h=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(Buffer.concat([h,buf])).digest("hex");
}
const dir=path.resolve("data/engine-h-v02"),months=[];
for(const [name,sha,size,expectedRows] of manifest){
  const p=path.join(dir,name),buf=fs.readFileSync(p);
  if(buf.length!==size)throw new Error("size_mismatch:"+name+":"+buf.length);
  const got=gitBlobSha(buf);if(got!==sha)throw new Error("sha_mismatch:"+name+":"+got);
  months.push({name,content:buf.toString("utf8"),expectedRows});
}
const metrics=E.runEngineH(months,Date.UTC(2024,0,1),Date.UTC(2025,2,1));
const bootstrap=E.bootstrap(metrics,10000,18018);
const out={...metrics,bootstrap,execution_metadata:{
  engine_implementation:"research/code/engine-h-v0.2.js",
  data_source_repo:"kevingtlin/Market-Data-Lab",
  data_source_commit:"922f83a60cc574e7395fb27397077288055a1ef6",
  split:"development",
  validation_or_holdout_loaded:false
}};
delete out.trades;delete out.setups;delete out.daily_series;
fs.mkdirSync("research/results",{recursive:true});
fs.writeFileSync("research/results/EXP-018-development-summary-v0.2.json",JSON.stringify(out,null,2)+"\n");
fs.writeFileSync("research/results/EXP-018-development-setups-v0.2.jsonl",metrics.setups.map(x=>JSON.stringify(x)).join("\n")+"\n");
fs.writeFileSync("research/results/EXP-018-development-trades-v0.2.jsonl",metrics.trades.map(x=>JSON.stringify(x)).join("\n")+"\n");
console.log("EXP018_DEVELOPMENT_SUMMARY",JSON.stringify({
 accepted_filled_trades:metrics.accepted_filled_trades,
 target_hit_rate:metrics.target_hit_rate,
 stop_rate:metrics.stop_rate,
 timeout_rate:metrics.timeout_rate,
 net_expectancy_usd_050:metrics.expectancy.net_usd_050,
 net_profit_factor_050:metrics.profit_factor.net_050,
 total_net_usd_050:metrics.total_net_usd_050,
 max_drawdown_usd:metrics.max_drawdown_usd,
 bootstrap_expectancy_95:[bootstrap.expectancy_net_usd_050.lo,bootstrap.expectancy_net_usd_050.hi]
}));
