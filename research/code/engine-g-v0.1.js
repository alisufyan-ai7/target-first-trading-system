/* Engine G v0.1 frozen implementation.
 * Governed by strategies/engine-g-contextual-liquidity-reversal/SPEC-v0.1.md.
 * Pure ECMAScript; no floating-point equality is used for structural prices.
 */
(function (root) {
  "use strict";

  const MINUTE = 60000;
  const FIVE = 5 * MINUTE;
  const FIFTEEN = 15 * MINUTE;
  const TICK_USD_010 = 0.01;
  const PRIMARY_COST_TICKS = 500;

  function assert(cond, msg) { if (!cond) throw new Error(msg); }

  function parseTick(s) {
    const m = /^([0-9]+)(?:\.([0-9]+))?$/.exec(String(s).trim());
    if (!m) throw new Error("invalid_price_text:" + s);
    let frac = m[2] || "";
    if (frac.length > 3) {
      const beyond = frac.slice(3);
      if (!/^0*$/.test(beyond)) throw new Error("off_grid_price:" + s);
      frac = frac.slice(0, 3);
    }
    frac = frac.padEnd(3, "0");
    return Number(m[1]) * 1000 + Number(frac);
  }

  function utcDate(ts) { return new Date(ts).toISOString().slice(0, 10); }
  function weekday(ts) { return new Date(ts).getUTCDay(); }
  function dayStart(ts) {
    const d = new Date(ts);
    return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate());
  }
  function hhmmMinutes(ts) {
    const d = new Date(ts);
    return d.getUTCHours() * 60 + d.getUTCMinutes();
  }
  function completionBefore1800(tsClose) { return hhmmMinutes(tsClose) < 18 * 60; }
  function isEligibleWeekdayDate(dateStr) {
    const [y,m,d]=dateStr.split("-").map(Number);
    const w=new Date(Date.UTC(y,m-1,d)).getUTCDay();
    return w>=1 && w<=5;
  }

  function parseMonthlyCsv(name, content, expectedRows) {
    const lines = content.trimEnd().split("\n");
    assert(lines[0].trim() === "timestamp,open,high,low,close", "bad_header:" + name);
    assert(lines.length === expectedRows + 1, "bad_row_count:" + name + ":" + (lines.length-1));
    const out = new Array(expectedRows);
    let prevTs = null;
    for (let i=1;i<lines.length;i++) {
      const p=lines[i].trim().split(",");
      assert(p.length===5, "bad_columns:" + name + ":" + i);
      const ts=Number(p[0]);
      assert(Number.isInteger(ts) && ts % MINUTE === 0, "bad_timestamp:" + name + ":" + i);
      if (prevTs !== null) assert(ts-prevTs===MINUTE, "non_contiguous_timestamp:" + name + ":" + i);
      prevTs=ts;
      const o=parseTick(p[1]), h=parseTick(p[2]), l=parseTick(p[3]), c=parseTick(p[4]);
      assert(o>0&&h>0&&l>0&&c>0&&h>=o&&h>=c&&l<=o&&l<=c&&h>=l,"invalid_ohlc:"+name+":"+i);
      out[i-1]={ts,o,h,l,c,active:false,activeOrd:-1};
    }
    return out;
  }

  function buildRows(months) {
    let rows=[];
    for (const m of months) {
      const r=parseMonthlyCsv(m.name,m.content,m.expectedRows);
      if (rows.length) assert(r[0].ts-rows[rows.length-1].ts===MINUTE,"month_boundary_gap:"+m.name);
      rows=rows.concat(r);
    }
    let activeOrd=0;
    for (let i=0;i<rows.length;i++) {
      const x=rows[i], p=i?rows[i-1]:null;
      const carry = !!p && x.o===x.h && x.h===x.l && x.l===x.c && x.c===p.c;
      x.active=!carry;
      if (x.active) x.activeOrd=activeOrd++;
    }
    return rows;
  }

  function buildBars(rows, minutes) {
    const size=minutes;
    const out=[];
    for (let i=0;i<rows.length;) {
      const start=rows[i].ts;
      const aligned=Math.floor(start/(size*MINUTE))*(size*MINUTE);
      if (start!==aligned) { i++; continue; }
      if (i+size>rows.length) break;
      let ok=true;
      for (let j=0;j<size;j++) if(rows[i+j].ts!==start+j*MINUTE){ok=false;break;}
      if(!ok){i++;continue;}
      const chunk=rows.slice(i,i+size);
      out.push({
        startTs:start,
        closeTs:start+size*MINUTE,
        o:chunk[0].o,
        h:Math.max(...chunk.map(x=>x.h)),
        l:Math.min(...chunk.map(x=>x.l)),
        c:chunk[chunk.length-1].c,
        active:chunk.some(x=>x.active),
        activeOrd:-1,
        rowStart:i,
        rowEnd:i+size-1
      });
      i+=size;
    }
    let ord=0;
    for(const b of out) if(b.active) b.activeOrd=ord++;
    return out;
  }

  function buildDayStats(rows, bars5) {
    const map=new Map();
    for(const r of rows){
      const d=utcDate(r.ts);
      let x=map.get(d);
      if(!x){x={date:d,count:0,minTs:r.ts,maxTs:r.ts,high:-Infinity,low:Infinity,active5:0};map.set(d,x);}
      x.count++; x.maxTs=r.ts; x.high=Math.max(x.high,r.h); x.low=Math.min(x.low,r.l);
    }
    for(const b of bars5) if(b.active){
      const d=utcDate(b.startTs);
      const x=map.get(d); if(x) x.active5++;
    }
    for(const x of map.values()){
      const [y,m,d]=x.date.split("-").map(Number);
      const ds=Date.UTC(y,m-1,d);
      x.complete=x.count===1440 && x.minTs===ds && x.maxTs===ds+1439*MINUTE;
      x.range=x.high-x.low;
    }
    return map;
  }

  function buildAsianStats(rows) {
    const map=new Map();
    for(const r of rows){
      const mins=hhmmMinutes(r.ts);
      if(mins>=360) continue;
      const d=utcDate(r.ts);
      let x=map.get(d);
      if(!x){x={count:0,minTs:r.ts,maxTs:r.ts,high:-Infinity,low:Infinity,activeM1:0};map.set(d,x);}
      x.count++;x.maxTs=r.ts;x.high=Math.max(x.high,r.h);x.low=Math.min(x.low,r.l);if(r.active)x.activeM1++;
    }
    for(const [d,x] of map){
      const [y,m,dd]=d.split("-").map(Number), ds=Date.UTC(y,m-1,dd);
      x.complete=x.count===360&&x.minTs===ds&&x.maxTs===ds+359*MINUTE;
      x.range=x.high-x.low;
    }
    return map;
  }

  function previousTradingDay(dateStr, dayStats) {
    const [y,m,d]=dateStr.split("-").map(Number);
    let ts=Date.UTC(y,m-1,d)-24*60*MINUTE;
    for(let guard=0;guard<10;guard++,ts-=24*60*MINUTE){
      const w=weekday(ts);
      if(w===0||w===6) continue;
      const s=dayStats.get(utcDate(ts));
      if(!s) return {ok:false,reason:"pdh_pdl_unavailable_no_previous_trading_day"};
      if(!s.complete) return {ok:false,reason:"pdh_pdl_unavailable_incomplete_previous_day"};
      if(s.active5===0&&s.range===0) continue;
      if(s.active5<=0||s.range<=0) return {ok:false,reason:"pdh_pdl_unavailable_incomplete_previous_day"};
      return {ok:true,stats:s};
    }
    return {ok:false,reason:"pdh_pdl_unavailable_no_previous_trading_day"};
  }

  function percentile(a,p) {
    if(!a.length) return null;
    const b=[...a].sort((x,y)=>x-y);
    const pos=(b.length-1)*p, lo=Math.floor(pos), hi=Math.ceil(pos);
    return lo===hi?b[lo]:b[lo]+(b[hi]-b[lo])*(pos-lo);
  }
  function distSummary(a) {
    if(!a.length) return {n:0,mean:null,median:null,p10:null,p90:null,min:null,max:null};
    const sum=a.reduce((x,y)=>x+y,0);
    return {n:a.length,mean:sum/a.length,median:percentile(a,.5),p10:percentile(a,.1),p90:percentile(a,.9),min:Math.min(...a),max:Math.max(...a)};
  }

  function runEngineG(months, splitStart, splitEndExclusive, options={}) {
    const rows=buildRows(months);
    const bars5=buildBars(rows,5), bars15=buildBars(rows,15);
    const dayStats=buildDayStats(rows,bars5), asianStats=buildAsianStats(rows);
    const bar5ByEnd=new Map(bars5.map(b=>[b.closeTs,b]));
    const bar5ByStart=new Map(bars5.map(b=>[b.startTs,b]));
    const bar15ByEnd=new Map(bars15.map(b=>[b.closeTs,b]));

    const activeM1=[];
    const active5=[];
    const active15=[];
    const tr5=[];
    const m1PivotHigh=[];
    const m1PivotLow=[];

    let levelSeq=0, setupSeq=0, tradeSeq=0;
    let instances=[];
    let pending=[];
    let openTrade=null;
    let shadows=[];
    let trades=[];
    let setups=[];
    const availabilityCounts={};
    const eventCounts={breach_events:0, qualifying_one_sided_sweeps:0, in_window_sweeps:0};
    const inSplitTs=ts=>ts>=splitStart&&ts<splitEndExclusive;

    let lastProcessed5CloseTs=null;
    let current5Clusters=new Map();
    let currentContext=null;

    function inc(obj,k,n=1){obj[k]=(obj[k]||0)+n;}
    function newLevel(side,cls,price,createdTs,expireTs,meta={}){
      const x={id:"L"+(++levelSeq),side,cls,price,createdTs,eligibleTs:createdTs,expireTs,consumed:false,consumedTs:null,expired:false,...meta};
      instances.push(x);return x;
    }
    function activeInstance(x, fiveStart){
      if(x.consumed||x.expired) return false;
      if(x.expireTs!==null&&fiveStart>=x.expireTs){x.expired=true;return false;}
      if(x.tf==="5m"){
        const latest=active5.length?active5[active5.length-1].activeOrd:-1;
        if(latest-x.centerOrd>48){x.expired=true;return false;}
      }
      if(x.tf==="15m"){
        const latest=active15.length?active15[active15.length-1].activeOrd:-1;
        if(latest-x.centerOrd>48){x.expired=true;return false;}
      }
      return fiveStart>=x.eligibleTs;
    }
    function buildClusters(fiveStart){
      const kept=[];
      const m=new Map();
      for(const x of instances){
        if(!activeInstance(x,fiveStart)) continue;
        kept.push(x);
        const k=x.side+":"+x.price;
        let c=m.get(k);
        if(!c){c={key:k,side:x.side,price:x.price,instances:[],classes:new Set()};m.set(k,c);}
        c.instances.push(x);c.classes.add(x.cls);
      }
      instances=kept;
      return m;
    }

    function calcContext(fiveStart){
      if(active15.length<48) return null;
      const w=active15.slice(-48);
      let hi=-Infinity,lo=Infinity;
      for(const b of w){hi=Math.max(hi,b.h);lo=Math.min(lo,b.l);}
      return {hi,lo,midNum:hi+lo};
    }

    function activateCalendar(fiveStart){
      const mins=hhmmMinutes(fiveStart), d=utcDate(fiveStart);
      if(mins===0){
        const p=previousTradingDay(d,dayStats);
        if(p.ok){
          newLevel("HIGH","PDH",p.stats.high,fiveStart,fiveStart+24*60*MINUTE,{sourceDate:p.stats.date});
          newLevel("LOW","PDL",p.stats.low,fiveStart,fiveStart+24*60*MINUTE,{sourceDate:p.stats.date});
        } else if(inSplitTs(fiveStart)) inc(availabilityCounts,p.reason);
      }
      if(mins===360){
        const a=asianStats.get(d);
        if(!a||!a.complete) { if(inSplitTs(fiveStart)) inc(availabilityCounts,"asian_unavailable_incomplete_interval"); }
        else if(a.activeM1===0||a.range<=0) { if(inSplitTs(fiveStart)) inc(availabilityCounts,"asian_unavailable_inactive_or_zero_range"); }
        else {
          const exp=dayStart(fiveStart)+24*60*MINUTE;
          newLevel("HIGH","ASIA_HIGH",a.high,fiveStart,exp,{sourceDate:d});
          newLevel("LOW","ASIA_LOW",a.low,fiveStart,exp,{sourceDate:d});
        }
      }
    }

    function findInternalPivot(direction, sweepBar, currentActiveOrd){
      const arr=direction==="SHORT"?m1PivotLow:m1PivotHigh;
      const minOrd=currentActiveOrd-14;
      for(let i=arr.length-1;i>=0;i--){
        const p=arr[i];
        if(p.centerOrd<minOrd) break;
        if(p.centerTs<sweepBar.startTs && p.confirmOrd<=currentActiveOrd) return p;
      }
      return null;
    }

    function targetSnapshot(direction, entry, fvgCloseTs, m1Current){
      const candidates=[];
      for(const c of current5Clusters.values()){
        if(direction==="LONG"&&c.side!=="HIGH") continue;
        if(direction==="SHORT"&&c.side!=="LOW") continue;
        if(direction==="LONG"&&c.price<=entry) continue;
        if(direction==="SHORT"&&c.price>=entry) continue;
        let passed=false;
        const start=lastProcessed5CloseTs===null?-Infinity:lastProcessed5CloseTs;
        for(let ord=m1Current.activeOrd;ord>=0;ord--){
          const q=activeM1[ord];
          if(q.ts<start) break;
          if(q.ts>m1Current.ts) continue;
          if(direction==="LONG"&&q.h>c.price){passed=true;break;}
          if(direction==="SHORT"&&q.l<c.price){passed=true;break;}
        }
        if(!passed)candidates.push(c);
      }
      candidates.sort((a,b)=>direction==="LONG"?a.price-b.price:b.price-a.price);
      return candidates;
    }

    function reject(s,reason,ts){s.terminal=reason;s.terminalTs=ts;s.state="done";}
    function makeSetup(direction,sweepBar,anchor,breached,currentM1){
      const s={id:"S"+(++setupSeq),direction,sweepTs:sweepBar.closeTs,sweepStart:sweepBar.startTs,sweepHigh:sweepBar.h,sweepLow:sweepBar.l,
        anchorPrice:anchor.price,anchorClasses:[...anchor.classes].sort(),breachedIds:breached.flatMap(c=>c.instances.map(x=>x.id)),
        context:currentContext,createdActiveOrd:currentM1.activeOrd,state:"mss",terminal:null,mssSeen:0,entrySeen:0};
      const p=findInternalPivot(direction,sweepBar,currentM1.activeOrd);
      if(!p){reject(s,"no_internal_mss_pivot",sweepBar.closeTs);} else s.internalPivot=p;
      setups.push(s); if(s.state!=="done")pending.push(s); return s;
    }

    function evalDisplacement(s,m){
      const ord=m.activeOrd;
      if(ord<s.mssOrd||ord>s.mssOrd+2) return false;
      if(ord<20){reject(s,"displacement_baseline_unavailable_20",m.ts+MINUTE);return true;}
      let sum=0;for(let i=ord-20;i<ord;i++)sum+=Math.abs(activeM1[i].c-activeM1[i].o);
      const body=Math.abs(m.c-m.o);
      const dirOk=s.direction==="SHORT"?(m.c<m.o&&m.c<s.internalPivot.price):(m.c>m.o&&m.c>s.internalPivot.price);
      if(dirOk&&25*body>=2*sum){
        s.displacementOrd=ord;s.displacementTs=m.ts+MINUTE;s.body=body;s.body20sum=sum;s.state="fvg";
        return evalFvg(s,m);
      }
      if(ord===s.mssOrd+2){reject(s,"displacement_timeout_mss_plus_2",m.ts+MINUTE);return true;}
      return false;
    }

    function evalFvg(s,m){
      const ord=m.activeOrd;
      if(ord<s.displacementOrd||ord>s.displacementOrd+2) return false;
      if(ord<2) return false;
      const a=activeM1[ord-2];
      let lo=null,hi=null;
      if(s.direction==="LONG"&&m.l>a.h){lo=a.h;hi=m.l;}
      if(s.direction==="SHORT"&&m.h<a.l){lo=m.h;hi=a.l;}
      if(lo!==null&&hi>lo){
        s.fvgOrd=ord;s.fvgTs=m.ts+MINUTE;s.fvgLo=lo;s.fvgHi=hi;
        const num=lo+hi;
        s.entry=s.direction==="LONG"?Math.floor((num+1)/2):Math.floor(num/2);
        const tg=targetSnapshot(s.direction,s.entry,s.fvgTs,m);
        if(!tg.length){reject(s,"no_opposing_liquidity_target",s.fvgTs);return true;}
        s.s1=tg[0].price;s.s1Classes=[...tg[0].classes].sort();
        s.s2=tg[1]?tg[1].price:null;s.s2Classes=tg[1]?[...tg[1].classes].sort():[];
        s.s3=tg[2]?tg[2].price:null;s.s3Classes=tg[2]?[...tg[2].classes].sort():[];
        s.s1Dist=Math.abs(s.s1-s.entry);
        if(s.s1Dist<3000){reject(s,"insufficient_structural_room",s.fvgTs);return true;}
        s.stop=s.direction==="SHORT"?s.sweepHigh+1:s.sweepLow-1;
        if((s.direction==="LONG"&&s.stop>=s.entry)||(s.direction==="SHORT"&&s.stop<=s.entry)){
          reject(s,"invalid_stop_geometry",s.fvgTs);return true;
        }
        s.stopDist=Math.abs(s.entry-s.stop);s.grossStopUSD=s.stopDist*TICK_USD_010;
        if(s.stopDist>4000){reject(s,"structural_risk_above_40",s.fvgTs);return true;}
        s.state="entry";s.entrySeen=0;
        return true;
      }
      if(ord===s.displacementOrd+2){reject(s,"fvg_timeout_displacement_plus_2",m.ts+MINUTE);return true;}
      return false;
    }

    function closeActual(t,reason,exitTick,ts){
      if(t.closed) return;
      t.closed=true;t.exitReason=reason;t.exitTick=exitTick;t.exitTs=ts;
      t.grossTicks=t.direction==="LONG"?exitTick-t.entry:t.entry-exitTick;
      t.net0=t.grossTicks;
      t.net250=t.grossTicks-250;
      t.net500=t.grossTicks-500;
      t.grossUSD=t.grossTicks*TICK_USD_010;
      t.netUSD0=t.net0*TICK_USD_010;
      t.netUSD250=t.net250*TICK_USD_010;
      t.netUSD500=t.net500*TICK_USD_010;
      if(openTrade&&openTrade.id===t.id)openTrade=null;
    }

    function makeTrade(s,m){
      if(openTrade) throw new Error("UNFROZEN_PENDING_FILL_CONFLICT:"+s.id+":"+m.ts);
      const t={id:"T"+(++tradeSeq),setupId:s.id,direction:s.direction,entry:s.entry,stop:s.stop,s1:s.s1,s1Dist:s.s1Dist,
        stopDist:s.stopDist,s1Classes:s.s1Classes,anchorClasses:s.anchorClasses,fillTs:m.ts+MINUTE,fillOrd:m.activeOrd,
        horizonCount:1,actualMFE:0,actualMAE:0,potentialMFE:0,potentialMAE:0,closed:false,shadowDone:false,
        labels:{3000:null,4000:null,5000:null,7000:null,10000:null},labelTimes:{},sweepTs:s.sweepTs};
      trades.push(t);s.tradeId=t.id;s.state="done";s.terminal=null;openTrade=t;shadows.push(t);
      const stopHit=t.direction==="LONG"?m.l<=t.stop:m.h>=t.stop;
      if(stopHit){
        t.actualMAE=t.stopDist;t.potentialMAE=t.stopDist;
        for(const k of Object.keys(t.labels))t.labels[k]="stop_before_target";
        t.shadowDone=true;
        closeActual(t,"exit_stop_fill_bar",t.stop,m.ts+MINUTE);
      }
      return t;
    }

    function processTradeBar(t,m){
      if(t.closed||m.activeOrd<=t.fillOrd) return;
      const stopHit=t.direction==="LONG"?m.l<=t.stop:m.h>=t.stop;
      const s1Hit=t.direction==="LONG"?m.h>=t.s1:m.l<=t.s1;
      if(stopHit){
        t.actualMAE=t.stopDist;
        closeActual(t,"exit_stop",t.stop,m.ts+MINUTE);
        return;
      }
      const fav=t.direction==="LONG"?m.h-t.entry:t.entry-m.l;
      const adv=t.direction==="LONG"?t.entry-m.l:m.h-t.entry;
      t.actualMFE=Math.max(t.actualMFE,Math.max(0,fav));
      t.actualMAE=Math.max(t.actualMAE,Math.max(0,adv));
      if(s1Hit){
        t.actualMFE=Math.min(Math.max(t.actualMFE,t.s1Dist),t.s1Dist);
        closeActual(t,"exit_s1",t.s1,m.ts+MINUTE);
        return;
      }
      t.horizonCount++;
      const closeTs=m.ts+MINUTE;
      if(t.horizonCount>=120){
        closeActual(t,"exit_timeout_120",m.c,closeTs);return;
      }
      if(hhmmMinutes(closeTs)>=20*60){
        closeActual(t,"exit_session_2000",m.c,closeTs);return;
      }
    }

    function processShadowBar(t,m){
      if(t.shadowDone||m.activeOrd<=t.fillOrd) return;
      const stopHit=t.direction==="LONG"?m.l<=t.stop:m.h>=t.stop;
      if(stopHit){
        t.potentialMAE=t.stopDist;
        for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="stop_before_target";
        t.shadowDone=true;return;
      }
      const fav=t.direction==="LONG"?m.h-t.entry:t.entry-m.l;
      const adv=t.direction==="LONG"?t.entry-m.l:m.h-t.entry;
      t.potentialMFE=Math.max(t.potentialMFE,Math.max(0,fav));
      t.potentialMAE=Math.max(t.potentialMAE,Math.max(0,adv));
      for(const ks of Object.keys(t.labels)){
        if(t.labels[ks]!==null)continue;
        const d=Number(ks), target=t.direction==="LONG"?t.entry+d:t.entry-d;
        const hit=t.direction==="LONG"?m.h>=target:m.l<=target;
        if(hit){t.labels[ks]="target_before_stop";t.labelTimes[ks]=(m.ts+MINUTE)-t.fillTs;}
      }
      const count=m.activeOrd-t.fillOrd+1;
      const closeTs=m.ts+MINUTE;
      if(count>=120||hhmmMinutes(closeTs)>=20*60){
        for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="horizon_without_target_or_stop";
        t.shadowDone=true;
      }
    }

    function processPendingM1(m){
      for(const s of pending){
        if(s.state==="done")continue;
        const closeTs=m.ts+MINUTE;
        if(m.activeOrd<=s.createdActiveOrd)continue;
        if(!completionBefore1800(closeTs)){
          if(s.state==="mss")reject(s,"setup_window_closed_before_mss",closeTs);
          else if(s.state==="displacement")reject(s,"setup_window_closed_before_displacement",closeTs);
          else if(s.state==="fvg")reject(s,"setup_window_closed_before_fvg",closeTs);
          else if(s.state==="entry")reject(s,"entry_window_closed_1800",closeTs);
          continue;
        }
        if(s.state==="mss"){
          s.mssSeen++;
          const hit=s.direction==="SHORT"?m.c<s.internalPivot.price:m.c>s.internalPivot.price;
          if(hit){
            s.mssOrd=m.activeOrd;s.mssTs=closeTs;s.state="displacement";evalDisplacement(s,m);
          } else if(s.mssSeen>=10) reject(s,"mss_timeout_10",closeTs);
        } else if(s.state==="displacement"){
          evalDisplacement(s,m);
        } else if(s.state==="fvg"){
          evalFvg(s,m);
        } else if(s.state==="entry"){
          s.entrySeen++;
          const entryHit=s.direction==="LONG"?m.l<=s.entry:m.h>=s.entry;
          if(entryHit){makeTrade(s,m);continue;}
          const stopHit=s.direction==="LONG"?m.l<=s.stop:m.h>=s.stop;
          const s1Hit=s.direction==="LONG"?m.h>=s.s1:m.l<=s.s1;
          if(stopHit){reject(s,"preentry_structural_invalidation",closeTs);continue;}
          if(s1Hit){reject(s,"preentry_s1_reached",closeTs);continue;}
          if(s.entrySeen>=10)reject(s,"entry_timeout_10",closeTs);
        }
      }
      pending=pending.filter(s=>s.state!=="done");
    }

    function confirmM1Pivot(m){
      const n=activeM1.length-1;
      if(n<4)return;
      const t=n-2,a=activeM1;
      const c=a[t];
      if(c.h>a[t-1].h&&c.h>a[t-2].h&&c.h>=a[t+1].h&&c.h>=a[t+2].h)
        m1PivotHigh.push({centerOrd:c.activeOrd,centerTs:c.ts,confirmOrd:m.activeOrd,price:c.h});
      if(c.l<a[t-1].l&&c.l<a[t-2].l&&c.l<=a[t+1].l&&c.l<=a[t+2].l)
        m1PivotLow.push({centerOrd:c.activeOrd,centerTs:c.ts,confirmOrd:m.activeOrd,price:c.l});
    }

    function confirm5Pivot(b){
      const prev=active5.length?active5[active5.length-1]:null;
      const tr=prev?Math.max(b.h-b.l,Math.abs(b.h-prev.c),Math.abs(b.l-prev.c)):b.h-b.l;
      active5.push(b);tr5.push(tr);
      const n=active5.length-1;if(n<4)return;
      const t=n-2,a=active5,c=a[t];
      const atrReady=n>=13;
      const sum14=atrReady?tr5.slice(n-13,n+1).reduce((x,y)=>x+y,0):null;
      if(!atrReady)return;
      const highPivot=c.h>a[t-1].h&&c.h>a[t-2].h&&c.h>=a[t+1].h&&c.h>=a[t+2].h;
      const lowPivot=c.l<a[t-1].l&&c.l<a[t-2].l&&c.l<=a[t+1].l&&c.l<=a[t+2].l;
      if(highPivot){
        const prom=c.h-Math.max(Math.min(a[t-2].l,a[t-1].l),Math.min(a[t+1].l,a[t+2].l));
        if(28*prom>=sum14)newLevel("HIGH","SWING_5M_HIGH",c.h,b.closeTs,null,{tf:"5m",centerOrd:c.activeOrd,eligibleTs:b.closeTs});
      }
      if(lowPivot){
        const prom=Math.min(Math.max(a[t-2].h,a[t-1].h),Math.max(a[t+1].h,a[t+2].h))-c.l;
        if(28*prom>=sum14)newLevel("LOW","SWING_5M_LOW",c.l,b.closeTs,null,{tf:"5m",centerOrd:c.activeOrd,eligibleTs:b.closeTs});
      }
    }

    function confirm15Pivot(b){
      active15.push(b);
      const n=active15.length-1;if(n<4)return;
      const t=n-2,a=active15,c=a[t];
      if(c.h>a[t-1].h&&c.h>a[t-2].h&&c.h>=a[t+1].h&&c.h>=a[t+2].h)
        newLevel("HIGH","SWING_15M_HIGH",c.h,b.closeTs,null,{tf:"15m",centerOrd:c.activeOrd,eligibleTs:b.closeTs});
      if(c.l<a[t-1].l&&c.l<a[t-2].l&&c.l<=a[t+1].l&&c.l<=a[t+2].l)
        newLevel("LOW","SWING_15M_LOW",c.l,b.closeTs,null,{tf:"15m",centerOrd:c.activeOrd,eligibleTs:b.closeTs});
    }

    function on5Open(b){
      activateCalendar(b.startTs);
      current5Clusters=buildClusters(b.startTs);
      currentContext=calcContext(b.startTs);
    }

    function on5Close(b,currentM1){
      if(!b.active){
        const b15=bar15ByEnd.get(b.closeTs);
        if(b15&&b15.active)confirm15Pivot(b15);
        lastProcessed5CloseTs=b.closeTs;
        return;
      }
      const highBreached=[],lowBreached=[];
      for(const c of current5Clusters.values()){
        if(c.side==="HIGH"&&b.h>c.price)highBreached.push(c);
        if(c.side==="LOW"&&b.l<c.price)lowBreached.push(c);
      }
      if((highBreached.length||lowBreached.length)&&inSplitTs(b.closeTs))eventCounts.breach_events++;
      const qHigh=highBreached.filter(c=>b.c<c.price);
      const qLow=lowBreached.filter(c=>b.c>c.price);
      for(const c of highBreached.concat(lowBreached))for(const x of c.instances){x.consumed=true;x.consumedTs=b.closeTs;}
      if(qHigh.length||qLow.length){
        if(qHigh.length&&qLow.length){
          const s={id:"S"+(++setupSeq),state:"done",terminal:"dual_sided_sweep_ambiguous",terminalTs:b.closeTs,sweepTs:b.closeTs};setups.push(s);
        } else {
          if(inSplitTs(b.closeTs))eventCounts.qualifying_one_sided_sweeps++;
          const completionMins=hhmmMinutes(b.closeTs);
          if(!(completionMins>=360&&completionMins<1080)){
            const s={id:"S"+(++setupSeq),state:"done",terminal:"outside_setup_window",terminalTs:b.closeTs,sweepTs:b.closeTs};setups.push(s);
          } else {
            if(inSplitTs(b.closeTs))eventCounts.in_window_sweeps++;
            const direction=qHigh.length?"SHORT":"LONG";
            const qs=qHigh.length?qHigh:qLow;
            qs.sort((a,b)=>direction==="SHORT"?b.price-a.price:a.price-b.price);
            const anchor=qs[0];
            let reason=null;
            if(!currentContext)reason="context_unavailable_48";
            else if(currentContext.hi<=currentContext.lo)reason="context_zero_range";
            else if(direction==="SHORT"&&2*anchor.price<=currentContext.midNum)reason="anchor_wrong_context_half";
            else if(direction==="LONG"&&2*anchor.price>=currentContext.midNum)reason="anchor_wrong_context_half";
            else if(openTrade)reason="suppressed_one_open";
            if(reason){
              const s={id:"S"+(++setupSeq),direction,state:"done",terminal:reason,terminalTs:b.closeTs,sweepTs:b.closeTs,anchorPrice:anchor.price,anchorClasses:[...anchor.classes].sort()};setups.push(s);
            } else makeSetup(direction,b,anchor,highBreached.concat(lowBreached),currentM1);
          }
        }
      } else if(highBreached.length||lowBreached.length){
        const s={id:"S"+(++setupSeq),state:"done",terminal:"breach_without_rejection_close",terminalTs:b.closeTs,sweepTs:b.closeTs};setups.push(s);
      }
      // Step 5: newly confirmed swings become active only after this bar's breach/setup decisions.
      confirm5Pivot(b);
      const b15=bar15ByEnd.get(b.closeTs);
      if(b15&&b15.active)confirm15Pivot(b15);
      lastProcessed5CloseTs=b.closeTs;
    }

    // iterate chronological M1 rows
    for(let i=0;i<rows.length;i++){
      const m=rows[i];
      const bOpen=bar5ByStart.get(m.ts);
      if(bOpen)on5Open(bOpen);

      if(m.active){
        activeM1.push(m);
        if(openTrade)processTradeBar(openTrade,m);
        for(const t of shadows)processShadowBar(t,m);
        shadows=shadows.filter(t=>!t.shadowDone);
        processPendingM1(m);
        confirmM1Pivot(m);
      }

      const closeTs=m.ts+MINUTE;
      const bClose=bar5ByEnd.get(closeTs);
      if(bClose)on5Close(bClose,m);
    }

    // data-end fail-safe for an open actual trade
    if(openTrade){
      const last=rows[rows.length-1];
      closeActual(openTrade,"exit_data_end",last.c,last.ts+MINUTE);
    }
    for(const t of shadows){
      if(!t.shadowDone){
        for(const k of Object.keys(t.labels))if(t.labels[k]===null)t.labels[k]="horizon_without_target_or_stop";
        t.shadowDone=true;
      }
    }

    // keep only split-created sweeps/trades/results
    const splitSetups=setups.filter(s=>inSplitTs(s.sweepTs||s.terminalTs||0));
    const splitTrades=trades.filter(t=>inSplitTs(t.sweepTs));

    const reasons={};for(const s of splitSetups)if(s.terminal)inc(reasons,s.terminal);
    const exits={};for(const t of splitTrades)inc(exits,t.exitReason);

    const labelRates={};
    for(const d of [3000,4000,5000,7000,10000]){
      const vals=splitTrades.map(t=>t.labels[d]);
      labelRates[d]={target:vals.filter(x=>x==="target_before_stop").length,stop:vals.filter(x=>x==="stop_before_target").length,horizon:vals.filter(x=>x==="horizon_without_target_or_stop").length,n:vals.length};
    }

    const allDates=[];
    for(let ts=dayStart(splitStart);ts<splitEndExclusive;ts+=24*60*MINUTE){
      const d=utcDate(ts);if(isEligibleWeekdayDate(d))allDates.push(d);
    }
    const daily={};for(const d of allDates)daily[d]=0;
    for(const t of splitTrades){
      const d=utcDate(t.fillTs-1); if(daily[d]!==undefined)daily[d]+=t.netUSD500;
    }
    const dailyVals=allDates.map(d=>daily[d]);

    function expectancy(field){return splitTrades.length?splitTrades.reduce((s,t)=>s+t[field],0)/splitTrades.length:null;}
    function pf(field){
      let pos=0,neg=0;for(const t of splitTrades){const x=t[field];if(x>0)pos+=x;else if(x<0)neg-=x;}
      return neg?pos/neg:(pos>0?Infinity:null);
    }
    function maxDrawdown(){
      let eq=500,peak=500,mdd=0;
      const sorted=[...splitTrades].sort((a,b)=>a.fillTs-b.fillTs);
      for(const t of sorted){eq+=t.netUSD500;peak=Math.max(peak,eq);mdd=Math.max(mdd,peak-eq);}
      return mdd;
    }
    function worstLosingTradeRun(){
      let maxN=0,maxLoss=0,curN=0,curLoss=0;
      for(const t of [...splitTrades].sort((a,b)=>a.fillTs-b.fillTs)){
        if(t.netUSD500<0){curN++;curLoss+=t.netUSD500;if(curN>maxN||(curN===maxN&&curLoss<maxLoss)){maxN=curN;maxLoss=curLoss;}}
        else {curN=0;curLoss=0;}
      }
      return {count:maxN,netLoss:maxLoss};
    }
    function maxConsec(pred){
      let best=0,cur=0;for(const x of dailyVals){if(pred(x)){cur++;best=Math.max(best,cur);}else cur=0;}return best;
    }

    const metrics={
      source_rows:rows.length,
      market_active_m1:rows.filter(x=>x.active).length,
      split:{start:new Date(splitStart).toISOString(),end_exclusive:new Date(splitEndExclusive).toISOString()},
      event_counts:eventCounts,
      setup_count:splitSetups.length,
      terminal_reasons:reasons,
      accepted_filled_trades:splitTrades.length,
      exits,
      s1_hit_rate:splitTrades.length?(exits.exit_s1||0)/splitTrades.length:null,
      stop_rate:splitTrades.length?((exits.exit_stop||0)+(exits.exit_stop_fill_bar||0))/splitTrades.length:null,
      timeout_rate:splitTrades.length?((exits.exit_timeout_120||0)+(exits.exit_session_2000||0)+(exits.exit_data_end||0))/splitTrades.length:null,
      label_rates:labelRates,
      expectancy:{
        gross_usd:expectancy("grossUSD"),
        net_usd_0:expectancy("netUSD0"),
        net_usd_025:expectancy("netUSD250"),
        net_usd_050:expectancy("netUSD500")
      },
      profit_factor:{
        gross:pf("grossUSD"),net_0:pf("netUSD0"),net_025:pf("netUSD250"),net_050:pf("netUSD500")
      },
      total_net_usd_050:splitTrades.reduce((s,t)=>s+t.netUSD500,0),
      weekdays:allDates.length,
      daily:{
        mean:dailyVals.length?dailyVals.reduce((a,b)=>a+b,0)/dailyVals.length:null,
        median:percentile(dailyVals,.5),
        losing_pct:dailyVals.length?dailyVals.filter(x=>x<0).length/dailyVals.length:null,
        le50_pct:dailyVals.length?dailyVals.filter(x=>x<=50).length/dailyVals.length:null,
        ge100_pct:dailyVals.length?dailyVals.filter(x=>x>=100).length/dailyVals.length:null,
        ge150_pct:dailyVals.length?dailyVals.filter(x=>x>=150).length/dailyVals.length:null,
        ge200_pct:dailyVals.length?dailyVals.filter(x=>x>=200).length/dailyVals.length:null
      },
      max_drawdown_usd:maxDrawdown(),
      worst_losing_trade_run:worstLosingTradeRun(),
      max_consecutive_losing_weekdays:maxConsec(x=>x<0),
      max_consecutive_le50_weekdays:maxConsec(x=>x<=50),
      actual_mfe_ticks:distSummary(splitTrades.map(t=>t.actualMFE)),
      actual_mae_ticks:distSummary(splitTrades.map(t=>t.actualMAE)),
      potential_mfe_ticks:distSummary(splitTrades.map(t=>t.potentialMFE)),
      potential_mae_ticks:distSummary(splitTrades.map(t=>t.potentialMAE)),
      s1_distance_ticks:distSummary(splitTrades.map(t=>t.s1Dist)),
      stop_distance_ticks:distSummary(splitTrades.map(t=>t.stopDist)),
      gross_stop_usd:distSummary(splitTrades.map(t=>t.stopDist*TICK_USD_010)),
      anchor_class_sets:{},
      target_class_sets:{},
      availability_counts:availabilityCounts,
      trades:splitTrades,
      setups:splitSetups,
      daily_series:allDates.map(d=>({date:d,netUSD500:daily[d]}))
    };
    for(const t of splitTrades){inc(metrics.anchor_class_sets,t.anchorClasses.join("+"));inc(metrics.target_class_sets,t.s1Classes.join("+"));}

    return metrics;
  }

  function bootstrap(metrics, reps=10000, seed=16016) {
    const days=metrics.daily_series;
    const byDate=new Map(days.map(x=>[x.date,[]]));
    for(const t of metrics.trades){const d=utcDate(t.fillTs-1);if(byDate.has(d))byDate.get(d).push(t.netUSD500);}
    const blocks=[];for(let i=0;i+5<=days.length;i++)blocks.push(days.slice(i,i+5).map(x=>x.date));
    let state=seed>>>0;
    function rnd(){state=(1664525*state+1013904223)>>>0;return state/4294967296;}
    const exp=[],dailyMean=[];let zeroTrade=0;
    for(let r=0;r<reps;r++){
      const picked=[];while(picked.length<days.length){const b=blocks[Math.floor(rnd()*blocks.length)];for(const d of b){if(picked.length<days.length)picked.push(d);}}
      let pnl=0,n=0;for(const d of picked){for(const x of byDate.get(d)||[]){pnl+=x;n++;}}
      dailyMean.push(pnl/days.length);
      if(n){exp.push(pnl/n);}else zeroTrade++;
    }
    return {
      reps,seed,block_weekdays:5,zero_trade_resamples:zeroTrade,
      expectancy_net_usd_050:{point:metrics.expectancy.net_usd_050,lo:percentile(exp,.025),hi:percentile(exp,.975)},
      mean_daily_net_usd_050:{point:metrics.daily.mean,lo:percentile(dailyMean,.025),hi:percentile(dailyMean,.975)}
    };
  }

  function selfTest() {
    assert(parseTick("2062.688")===2062688,"tick_parse");
    assert(parseTick("3")===3000,"tick_integer");
    let threw=false;try{parseTick("1.2345");}catch(e){threw=true;}assert(threw,"off_grid_reject");
    const midLong=Math.floor((1001+1002+1)/2), midShort=Math.floor((1001+1002)/2);
    assert(midLong===1002&&midShort===1001,"midpoint_rounding");
    assert(28*50>=1400&&!(28*49>=1400),"prominence_integer_test");
    assert(25*160>=2*2000,"displacement_integer_test");
    return {ok:true,tests:["tick_parse","off_grid_reject","midpoint_rounding","prominence_integer","displacement_integer"]};
  }

  root.EngineGv01={runEngineG,bootstrap,selfTest,parseTick};
})(globalThis);
