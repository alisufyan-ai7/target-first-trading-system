const fs=require("fs");
const path=require("path");
const crypto=require("crypto");
const {execSync}=require("child_process");

require("./engine-t-v0.1.js");
const E=globalThis.EngineTv01;
if(!E)throw new Error("EngineTv01 missing");
const selfTests=E.selfTest();

const SOURCE_COMMIT="922f83a60cc574e7395fb27397077288055a1ef6";
const sourceRepo=path.resolve(process.env.EXP046_SOURCE_REPO||"/tmp/market-data-lab");
const dataDir=path.join(sourceRepo,"xauusd/bid/m1");

function sha256(buf){return crypto.createHash("sha256").update(buf).digest("hex");}
function gitBlobSha(buf){
  const h=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(Buffer.concat([h,buf])).digest("hex");
}
function monthRange(){
  const out=[]; let y=2021,m=12;
  while(y<2025||(y===2025&&m<=2)){
    out.push([y,m]); m++; if(m===13){m=1;y++;}
  }
  return out;
}
function daysInMonth(y,m){return new Date(Date.UTC(y,m,0)).getUTCDate();}

const sourceHead=execSync("git rev-parse HEAD",{cwd:sourceRepo,encoding:"utf8"}).trim();
if(sourceHead!==SOURCE_COMMIT)throw new Error("source_commit_mismatch:"+sourceHead);
const status=execSync("git status --porcelain",{cwd:sourceRepo,encoding:"utf8"}).trim();
if(status)throw new Error("source_worktree_dirty");

const months=[],verified=[];
for(const [y,m] of monthRange()){
  const mm=String(m).padStart(2,"0");
  const name=`xauusd_bid_m1_${y}_${mm}.csv`;
  const rel=`xauusd/bid/m1/${name}`;
  const p=path.join(dataDir,name);
  if(!fs.existsSync(p))throw new Error("missing_source_file:"+name);
  const buf=fs.readFileSync(p);
  const gotBlob=gitBlobSha(buf);
  const tree=execSync(`git ls-tree ${SOURCE_COMMIT} -- ${rel}`,{cwd:sourceRepo,encoding:"utf8"}).trim();
  const match=/^\d+ blob ([0-9a-f]{40})\t/.exec(tree);
  if(!match)throw new Error("source_tree_missing:"+name);
  if(gotBlob!==match[1])throw new Error("blob_sha_mismatch:"+name);
  const expectedRows=daysInMonth(y,m)*1440;
  months.push({name,content:buf.toString("utf8"),expectedRows});
  verified.push({name,git_blob_sha:gotBlob,bytes:buf.length,expected_rows:expectedRows,sha256:sha256(buf)});
}

const metrics=E.runEngineT(months,Date.UTC(2022,0,1),Date.UTC(2025,2,1));
const candidates=metrics.accepted_candidates;
const setups=metrics.setups;
delete metrics.accepted_candidates;
delete metrics.setups;

const engineBuf=fs.readFileSync(path.resolve("research/code/engine-t-v0.1.js"));
const runnerBuf=fs.readFileSync(__filename);
const testedSha=process.env.GITHUB_SHA||execSync("git rev-parse HEAD",{encoding:"utf8"}).trim();

const out={
  ...metrics,
  self_tests:selfTests,
  strategy_family_new:true,
  engine_s_rules_modified:false,
  execution_metadata:{
    tested_repository_sha:testedSha,
    engine_implementation:"research/code/engine-t-v0.1.js",
    engine_sha256:sha256(engineBuf),
    runner:"research/code/run-exp046-engine-t-v01-preflight.js",
    runner_sha256:sha256(runnerBuf),
    data_source_repo:"kevingtlin/Market-Data-Lab",
    data_source_commit:SOURCE_COMMIT,
    source_git_head_verified:sourceHead,
    downloaded_files:verified,
    warmup:"2021-12-01 through 2021-12-31",
    development:"2022-01-01 through 2025-02-28",
    validation_or_holdout_files_downloaded:false
  }
};

fs.mkdirSync("research/results",{recursive:true});
fs.writeFileSync("research/results/EXP-046-zero-outcome-preflight-v0.1.json",JSON.stringify(out,null,2)+"\n");
fs.writeFileSync("research/results/EXP-046-zero-outcome-candidates-v0.1.jsonl",candidates.map(x=>JSON.stringify(x)).join("\n")+(candidates.length?"\n":""));
fs.writeFileSync("research/results/EXP-046-zero-outcome-setups-v0.1.jsonl",setups.map(x=>JSON.stringify(x)).join("\n")+(setups.length?"\n":""));

console.log("EXP046_ZERO_OUTCOME",JSON.stringify({
  disposition:out.disposition,
  preflight_pass:out.preflight_pass,
  accepted_filled_candidates:out.accepted_filled_candidates,
  accepted_by_direction:out.accepted_by_direction,
  accepted_signal_days:out.accepted_signal_days,
  median_candidates_per_active_day:out.accepted_candidates_per_active_day.distribution.median,
  target_labels_calculated:out.target_labels_calculated,
  pnl_calculated:out.pnl_calculated,
  post_entry_path_evaluated:out.post_entry_path_evaluated
}));
