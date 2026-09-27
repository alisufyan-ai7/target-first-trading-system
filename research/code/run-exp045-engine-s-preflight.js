const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
const {execSync}=require("child_process");

require("./engine-s-v0.1.js");
const E=globalThis.EngineSv01;
if(!E)throw new Error("EngineSv01 missing");
const selfTests=E.selfTest();

const manifest=[
["xauusd_bid_m1_2023_12.csv","56dbf8a5316c48f4ec3300126c0decda03f8325f",2231969,44640],
["xauusd_bid_m1_2024_01.csv","f439cc6e17e39addc1a464eb0ccf8fe2eb71de99",2231993,44640],
["xauusd_bid_m1_2024_02.csv","b3ad49d5e784fb8c879f8e12095640f454f8f5fb",2087847,41760],
["xauusd_bid_m1_2024_03.csv","cdd53e37cc41773cc0d5c9210daefbf5ef6c3535b",2231983,44640],
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
function sha256(buf){return crypto.createHash("sha256").update(buf).digest("hex");}

const dir=path.resolve("data/engine-s");
const months=[];
const verified=[];
for(const [name,blobSha,size,expectedRows] of manifest){
  const p=path.join(dir,name),buf=fs.readFileSync(p);
  if(buf.length!==size)throw new Error("size_mismatch:"+name+":"+buf.length+":"+size);
  const got=gitBlobSha(buf);
  if(got!==blobSha)throw new Error("blob_sha_mismatch:"+name+":"+got+":"+blobSha);
  months.push({name,content:buf.toString("utf8"),expectedRows});
  verified.push({name,git_blob_sha:got,bytes:buf.length,expected_rows:expectedRows,sha256:sha256(buf)});
}

const metrics=E.runEngineS(months,Date.UTC(2024,0,1),Date.UTC(2025,2,1));
const candidates=metrics.accepted_candidates;
const setups=metrics.setups;
delete metrics.accepted_candidates;
delete metrics.setups;

const engineBuf=fs.readFileSync(path.resolve("research/code/engine-s-v0.1.js"));
const runnerBuf=fs.readFileSync(__filename);
const testedSha=process.env.GITHUB_SHA||execSync("git rev-parse HEAD",{encoding:"utf8"}).trim();

const out={
  ...metrics,
  self_tests:selfTests,
  execution_metadata:{
    tested_repository_sha:testedSha,
    engine_implementation:"research/code/engine-s-v0.1.js",
    engine_sha256:sha256(engineBuf),
    runner:"research/code/run-exp045-engine-s-preflight.js",
    runner_sha256:sha256(runnerBuf),
    data_source_repo:"kevingtlin/Market-Data-Lab",
    data_source_commit:"922f83a60cc574e7395fb27397077288055a1ef6",
    downloaded_files:verified,
    warmup:"2023-12-01 through 2023-12-31",
    development:"2024-01-01 through 2025-02-28",
    validation_or_holdout_files_downloaded:false
  }
};

fs.mkdirSync("research/results",{recursive:true});
fs.writeFileSync(
  "research/results/EXP-045-zero-outcome-preflight-v0.1.json",
  JSON.stringify(out,null,2)+"\n"
);
fs.writeFileSync(
  "research/results/EXP-045-zero-outcome-candidates-v0.1.jsonl",
  candidates.map(x=>JSON.stringify(x)).join("\n")+(candidates.length?"\n":"")
);
fs.writeFileSync(
  "research/results/EXP-045-zero-outcome-setups-v0.1.jsonl",
  setups.map(x=>JSON.stringify(x)).join("\n")+(setups.length?"\n":"")
);

console.log("EXP045_ZERO_OUTCOME_PREFLIGHT",JSON.stringify({
  disposition:out.disposition,
  preflight_pass:out.preflight_pass,
  accepted_filled_candidates:out.accepted_filled_candidates,
  accepted_by_branch:out.accepted_by_branch,
  accepted_by_branch_direction:out.accepted_by_branch_direction,
  accepted_signal_days:out.accepted_signal_days,
  median_candidates_per_active_day:out.accepted_candidates_per_active_day.distribution.median,
  stop_distance_ticks:out.stop_distance_ticks,
  target_labels_calculated:out.target_labels_calculated,
  mfe_mae_calculated:out.mfe_mae_calculated,
  pnl_calculated:out.pnl_calculated,
  post_entry_path_evaluated:out.post_entry_path_evaluated
}));
