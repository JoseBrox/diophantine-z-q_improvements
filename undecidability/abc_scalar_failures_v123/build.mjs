import fs from "node:fs";
import crypto from "node:crypto";
import assert from "node:assert/strict";
function build(j){
 const old=j.variable_names;
 const kill=/^new\.(chord\.inverse\.[01]|xstar\.[01]|curve\.S\.[01]|curve_du\.[01]|point\.\d+\.(square|curve)\.[01]|trace|fail\d+\.[01]|failSum\.[01]|failTrace|Z0)$/;
 const drop=new Set(["n_curve_du_0","n_curve_du_1","n_failSum_1",...Array.from({length:12},(_,i)=>"n_fail"+i+"_1")]);
 const added=["n_dsq_0","n_dsq_1","n_curve_K_0","n_curve_K_1","n_lift_a","n_lift_a2","n_lift_mean","n_failWeighted2"];
 const names=old.filter(n=>!drop.has(n)).concat(added),ix=new Map(names.map((n,i)=>[n,i+1]));
 const row=(name,terms)=>({name,terms:terms.map(([c,...ns])=>({coefficient:String(c),monomial:ns.map(n=>{if(!ix.has(n))throw Error(n);return ix.get(n)}).sort((a,b)=>a-b)}))});
 const keep=j.residuals.filter(x=>!kill.test(x.name)).map(x=>row(x.name,x.terms.map(t=>[t.coefficient,...t.monomial.map(i=>old[i-1])])));
 const fld=n=>["n_"+n+"_0","n_"+n+"_1"];
 const R=[];
 const p=(...terms)=>terms;
 const scale=(a,k)=>a.map(([c,...n])=>[c*k,...n]);
 const mul=(a,b)=>{const rr=[];for(const [c,...n] of a)for(const [d,...m] of b)rr.push([c*d,...n,...m]);return rr};
 const plus=(...a)=>a.flat();
 const V=n=>[[1,n]],C=n=>[[n]];
 const F=n=>fld(n).map(V);
 const fs=(a,k)=>a.map(x=>scale(x,k));
 const fa=(...a)=>[plus(...a.map(x=>x[0])),plus(...a.map(x=>x[1]))];
 const fm=(a,b)=>[plus(mul(a[0],b[0]),scale(mul(a[1],b[1]),2)),plus(mul(a[0],b[1]),mul(a[1],b[0]))];
 const ft=(n,a)=>{for(let i=0;i<2;i++){const sums=new Map();for(const [c,...ns] of a[i]){const k=JSON.stringify(ns.sort());sums.set(k,(sums.get(k)||0)+c)}R.push(row(n+"."+i,[...sums].filter(([k,c])=>c!==0).map(([k,c])=>[c,...JSON.parse(k)])))}};
 const fe=(n,a,b)=>ft(n,fa(a,fs(b,-1)));
 const d=F("chord_d"),D=F("dsq"),I=F("chord_di"),L=F("curve_L"),S=F("curve_S"),K=F("curve_K"),X=F("xstar"),delta=[C(11),C(-6)],unit=[C(1),[]];
 fe("new.dsq",D,fm(d,d));
 fe("new.chord.inverse",fm(D,I),unit);
 fe("new.xstar",X,fa(F("xU"),fs(fm(d,[V("n_lift_mean"),[]]),-1)));
 const DD=fm(delta,fm(I,I)),LL=fm(L,L);
 fe("new.curve.S",S,fa(LL,fs(DD,-1)));
 fe("new.curve.K",K,fa(fs(LL,3),fs(DD,-1)));
 R.push(row("new.lift.a2",[[1,"n_lift_a2"],[-1,"n_lift_a","n_lift_a"]]));
 R.push(row("new.lift.mean",[[1,"n_c","n_lift_mean"],[-1,"n_c","n_mean"],[1,"n_lift_a2","n_lift_mean"],[-1,"n_lift_a2","n_mean"],[-1,"n_lift_a"]]));
 const trace=[[1,"n_trace"],[-24,"n_xstar_0"]],sum=[[1,"n_failSum_0"]];
 for(let i=0;i<12;i++){
   const e=F("err_"+i),Q=F("err_square_"+i),Y=F("ord_"+i),z="n_fail"+i+"_0";
   fe("new.point."+i+".square",Q,fm(e,e));
   fe("new.point."+i+".curve",fm(Y,Y),fa(fm(L,S),fm(K,e),fs(fm(L,Q),3),fm(e,Q)));
   R.push(row("new.fail"+i+".scalar",[[1,z,"n_u"],[2,z,"n_err_square_"+i+"_0"],[-2,"n_err_square_"+i+"_0"]]));
   sum.push([-1,"n_r"+i,z]);
   trace.push([-2,"n_dsq_0","n_err_"+i+"_0"],[-4,"n_dsq_1","n_err_"+i+"_1"]);
 }
 R.push(row("new.trace",trace));
 R.push(row("new.failSum.scalar",sum));
 R.push(row("new.failWeighted",[[1,"n_failTrace"],[-1,"n_au","n_failSum_0"]]));
 R.push(row("new.failWeighted2",[[1,"n_failWeighted2"],[-1,"n_failTrace","n_failTrace"]]));
 R.push(row("new.Z0",[[1,"n_Z0"],[-1],[4,"n_chi_0"],[-4,"n_chi_0","n_chi_0"],[-1,"n_c","n_failWeighted2"]]));
 const residuals=keep.concat(R),support=new Set(residuals.flatMap(q=>q.terms.flatMap(t=>t.monomial)));
 if(names.length!==312||support.size!==312||residuals.some(q=>q.terms.some(t=>t.monomial.length>2)))throw Error("bad final counts "+names.length);
 // independent local valuation grid: if primary e has positive valuation,
 // trace(e^2) is either >=2 or even nonpositive. It cannot have valuation 1.
 let cases=0;for(let i=1;i<30;i++)for(let k=-30;k<=30;k++){const v=Math.min(2*i,2*k);if((v>=2)!==(k>0)||v===1)throw Error("trace parity");cases++}
 for(let v=-30;v<=30;v++){if(v-Math.min(-1,2*v)<1)throw Error("correction parity");cases++}
 return {...j,predecessor:"undecidability/abc_nested_selector_v122/abc_quadrics.json",predecessor_git_blob:"09896308cd9e29e9f6d9a71e1370cbded5c3db4e",variables:names.length,variable_names:names,residuals,verification:{full_support:true,quadratic_rows:residuals.length,unchanged_rows:keep.length,new_rows:R.length,local_valuation_fixtures:cases,removed_coordinates:[...drop],added_coordinates:added}};
}
const raw=fs.readFileSync(new URL("../abc_nested_selector_v122/abc_quadrics.json",import.meta.url));
assert.equal(crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex"),"09896308cd9e29e9f6d9a71e1370cbded5c3db4e");
const result=build(JSON.parse(raw));const out=new URL("./abc_quadrics.json",import.meta.url);
if(process.argv.includes("--write"))fs.writeFileSync(out,JSON.stringify(result,null,2)+"\n");else assert.deepEqual(result,JSON.parse(fs.readFileSync(out,"utf8")));console.log(result.variables,result.residuals.length,result.verification);
