import fs from "node:fs";
import crypto from "node:crypto";
import assert from "node:assert/strict";
function build(t){
 const old=t.variable_names;
 const drop=new Set(["n_xU2_0","n_xU2_1","n_fHP2_0","n_fHP2_1","n_xstar_0","n_xstar_1","n_curve_K_0","n_curve_K_1"]);
 const names=old.filter(x=>!drop.has(x)).concat("n_curve_K_trace");
 const ix=new Map(names.map((n,i)=>[n,i+1]));
 const copy=q=>q.terms.map(z=>[z.coefficient,...z.monomial.map(i=>old[i-1])]);
 // Coefficient collection is exact. Only modified numerical-coefficient rows are collected.
 const row=(name,terms,collect=false)=>{
   if(collect){const m=new Map;for(const [c,...ns] of terms){const key=ns.sort().join(" ");m.set(key,(m.get(key)||0n)+BigInt(c))}terms=[...m].filter(([k,c])=>c!==0n).map(([k,c])=>[String(c),...(k?k.split(" "):[])])}
   return {name,terms:terms.map(([coefficient,...ns])=>({coefficient:String(coefficient),monomial:ns.map(n=>{if(!ix.has(n))throw Error(n+" in "+name);return ix.get(n)}).sort((a,b)=>a-b)}))};
 };
 const F=(n)=>[[[1,n+"_0"]],[[1,n+"_1"]]];
 const C=(a,b=0)=>[[[a]],[[b]]];
 const plus=(...xs)=>[xs.flatMap(x=>x[0]),xs.flatMap(x=>x[1])];
 const scale=(a,x)=>x.map(v=>v.map(([c,...ns])=>[a*c,...ns]));
 const mult=(a,b)=>{const p=(x,y)=>x.flatMap(([c,...ns])=>y.map(([d,...ms])=>[c*d,...ns,...ms]));return [p(a[0],b[0]).concat(p(a[1],b[1]).map(([c,...ns])=>[2*c,...ns])),p(a[0],b[1]).concat(p(a[1],b[0]))]};
 const scalar=(n)=>[[[1,n]],[]];
 const sq=x=>mult(x,x);
 const eq=(name,a,b)=>{const terms=plus(a,scale(-1,b));return terms.map((ts,i)=>row(name+"."+i,ts,true))};
 const kill=/^new\.(xU2\.[01]|U\.(curve|h)\.[01]|fHP2\.[01]|xstar\.[01]|curve_L\.[01]|curve\.(S|K)\.[01]|trace|point\.\d+\.(square|curve)\.[01]|fail\d+\.scalar)$/;
 const kept=[];
 const replacement=[];
 for(const q of t.residuals){
   if(kill.test(q.name))continue;
   let ts=copy(q);let changed=false;
   ts=ts.flatMap(([c,...ns])=>{
      if(ns.length===1 && ["n_fHP2_0","n_fHP2_1"].includes(ns[0])){
        changed=true;
        const comp=ns[0].endsWith("_0")?0:1;
        return sq(F("n_fHP"))[comp].map(([d,...ms])=>[BigInt(c)*BigInt(d),...ms])
      }
      return [[c,...ns]]
   });
   (changed?replacement:kept).push(row(q.name,ts,changed))
 }
 const x=F("n_xU"),y=F("n_yU"),f=F("n_fU"),h=F("n_hU"),d=F("n_chord_d"),D=F("n_dsq"),I=F("n_chord_di"),L=F("n_curve_L"),T=F("n_curve_S"),mu=scalar("n_mean"),Delta=C(11,-6),LI=sq(L),DI=mult(Delta,sq(I)),K=plus(scale(3,LI),scale(-1,DI));
 const rows=[
 ...eq("new.U.homogeneous_h",plus(mult(y,f),mult(h,x)),C(0)),
 ...eq("new.U.homogeneous_curve",plus(mult(h,y),x),mult(Delta,f)),
 ...eq("new.curve_L",mult(D,L),plus(x,scale(-1,mult(d,mu)))),
 ...eq("new.curve.S",T,plus(scale(-8,LI),scale(2,DI))),
 row("new.curve.K_trace",[[1,"n_curve_K_trace"],...K[0].map(([c,...ns])=>[-2*c,...ns])],true)
 ];
 const traceTerms=[[1,"n_trace"],[-24,"n_xU_0"],[24,"n_chord_d_0","n_mean"]];
 for(let i=0;i<12;i++){
   const e=F("n_err_"+i),Q=F("n_err_square_"+i),Y=F("n_ord_"+i),fail="n_fail"+i+"_0",q0="n_err_square_"+i+"_0";
   rows.push(...eq("new.point."+i+".square",Q,plus(sq(e),K)));
   rows.push(...eq("new.point."+i+".curve",sq(Y),plus(mult(plus(e,scale(3,L)),Q),mult(L,T))));
   rows.push(row("new.fail"+i+".scalar",[[1,"n_u",fail],[2,q0,fail],[-1,"n_curve_K_trace",fail],[-2,q0],[1,"n_curve_K_trace"]],true));
   traceTerms.push([-2,"n_err_"+i+"_0","n_dsq_0"],[-4,"n_err_"+i+"_1","n_dsq_1"]);
 }
 rows.push(row("new.trace",traceTerms,true));
 const residuals=kept.concat(replacement,rows),support=new Set(residuals.flatMap(q=>q.terms.flatMap(z=>z.monomial)));
 if(names.length!==295||residuals.length!==244||support.size!==295||residuals.some(q=>q.terms.some(z=>z.monomial.length>2)))throw Error("census "+[names.length,residuals.length,support.size,kept.length,replacement.length,rows.length]);
 return {...t,predecessor:"undecidability/abc_paired_height_v126/abc_quadrics.json",predecessor_git_blob:"96e04188e2e6e059fdd284c7fa3860417a0ada79",variables:names.length,variable_names:names,residuals,verification:{removed_coordinates:[...drop],added_coordinates:["n_curve_K_trace"],unchanged_rows:kept.length,substituted_rows:replacement.length,replacement_rows:rows.length,quadratic_rows:residuals.length,full_support:true,contact_exponent:12}};
}
const raw=fs.readFileSync(new URL("../abc_paired_height_v126/abc_quadrics.json",import.meta.url));
assert.equal(crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex"),"96e04188e2e6e059fdd284c7fa3860417a0ada79");
const out=JSON.stringify(build(JSON.parse(raw)),null,2)+"\n";
const target=new URL("abc_quadrics.json",import.meta.url);
if(process.argv.includes("--write"))fs.writeFileSync(target,out);else assert.equal(out,fs.readFileSync(target,"utf8"));
console.log(JSON.parse(out).verification);
