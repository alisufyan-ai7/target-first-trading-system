#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { once } = require("events");
const { getHistoricalRates } = require("dukascopy-node");

const SYMBOLS = [
  "XAUUSD","EURUSD","GBPUSD","USDJPY",
  "EURJPY","AUDUSD","USDCAD","USDCHF"
];
const FROM = new Date("2025-07-01T00:00:00.000Z");
const TO = new Date("2026-07-01T00:00:00.000Z");
const OUTDIR = process.env.EXP041_DATA_DIR || "/tmp/exp041-dukas-m1";

async function writeCsv(symbol, rows) {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const out = path.join(OUTDIR, symbol + ".csv");
  const ws = fs.createWriteStream(out, { encoding: "utf8" });
  ws.write("datetime,open,high,low,close,volume\n");

  let kept = 0;
  let prev = null;
  for (const row of rows) {
    if (!Array.isArray(row) || row.length < 6) throw new Error(symbol + ": malformed row");
    const ms = Number(row[0]);
    if (!Number.isFinite(ms)) throw new Error(symbol + ": invalid timestamp");
    if (ms < FROM.getTime() || ms >= TO.getTime()) continue;
    if (prev !== null && ms < prev) throw new Error(symbol + ": non-monotonic source rows");
    prev = ms;

    const nums = row.slice(1,6).map(Number);
    if (nums.some(v => !Number.isFinite(v))) throw new Error(symbol + ": invalid numeric row at " + ms);
    const line = [new Date(ms).toISOString(), ...nums].join(",") + "\n";
    if (!ws.write(line)) await once(ws, "drain");
    kept++;
  }

  ws.end();
  await once(ws, "finish");
  if (kept === 0) throw new Error(symbol + ": zero rows kept");
  return { out, kept };
}

async function main() {
  console.log(JSON.stringify({
    source: "Dukascopy via dukascopy-node",
    package_version: "1.50.0",
    from: FROM.toISOString(),
    to_exclusive: TO.toISOString(),
    timeframe: "m1",
    symbols: SYMBOLS,
    target_outdir: OUTDIR
  }, null, 2));

  for (const symbol of SYMBOLS) {
    const instrument = symbol.toLowerCase();
    console.log("Downloading " + symbol + "...");
    const rows = await getHistoricalRates({
      instrument,
      dates: { from: FROM, to: TO },
      timeframe: "m1",
      format: "array",
      batchSize: 10,
      pauseBetweenBatchesMs: 1000
    });
    if (!Array.isArray(rows)) throw new Error(symbol + ": expected array result");
    const info = await writeCsv(symbol, rows);
    console.log(symbol + ": source rows=" + rows.length + " normalized rows=" + info.kept + " path=" + info.out);
  }
}

main().catch(err => {
  console.error(err && err.stack ? err.stack : err);
  process.exit(1);
});
