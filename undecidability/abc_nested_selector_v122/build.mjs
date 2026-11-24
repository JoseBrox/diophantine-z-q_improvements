import fs from "node:fs";
import crypto from "node:crypto";
import assert from "node:assert/strict";
function build(j){
 const old=j.variable_names, drop=new Set(["chi0","chiU","chiE","chiP"].flatMap(n=>[0,1].map(k=>"n_"+n+"_"+k))), kill=/^new\.(chi0|chiU|chiE|chiP|chi)\.[01]$/;
 const names=old.filter(n=>!drop.has(n)).concat(["n_nestedA_0","n_nestedA_1","n_nestedV_0","n_nestedV_1"]);
 const ix=new Map(names.map((n,i)=>[n,i+1]));
 const row=(name,terms)=>({name,terms:terms.map(([c,...ns])=>({coefficient:String(c),monomial:ns.map(n=>{if(!ix.has(n))throw Error(n);return ix.get(n)}).sort((a,b)=>a-b)}))});
 const keep=j.residuals.filter(x=>!kill.test(x.name)).map(x=>row(x.name,x.terms.map(t=>[t.coefficient,...t.monomial.map(i=>old[i-1])])));
 if(j.residuals.length-keep.length!==10||old.length-names.length!==4)throw Error("counts");
 const field=(n)=>["n_"+n+"_0","n_"+n+"_1"];
 const [a,b]=field("nestedA"),[v,w]=field("nestedV"),[s,t]=field("slotR"),[q0,q1]=field("unitT2"),[e,f]=field("primaryE2"),[x,y]=field("chi");
 const extra=[
 row("new.nestedA.0",[[1,a],[-1,s,s],[-2,t,t],[-1,"n_u",q0]]),
 row("new.nestedA.1",[[1,b],[-2,s,t],[-1,"n_u",q1]]),
 row("new.nestedV.0",[[1,v],[-1,a,a],[-2,b,b],[-1,"n_c",e]]),
 row("new.nestedV.1",[[1,w],[-2,a,b],[-1,"n_c",f]]),
 row("new.nestedChi.0",[[1,x],[1,v,x],[2,w,y],[-1]]),
 row("new.nestedChi.1",[[1,y],[1,v,y],[1,w,x]])];
 const residuals=keep.concat(extra), support=new Set(residuals.flatMap(q=>q.terms.flatMap(t=>t.monomial)));
 if(names.length!==319||residuals.length!==268||support.size!==319||residuals.some(q=>q.terms.some(t=>t.monomial.length>2)))throw Error("final verification");
 let cases=0;
 const vals=[...Array.from({length:41},(_,i)=>i-20),Infinity];
 for(const R of vals.filter(x=>x!==0))for(const T of vals.filter(x=>x<=0))for(const E of vals){
   const A=Math.min(2*R,1+2*T),V=Math.min(2*A,-1+2*E);
   if((A>0)!==(R>0&&T>=0)||(V>0)!==(R>0&&T>=0&&E>0)||A===0||V===0)throw Error("valuation test");
   cases++;
 }
 return {...j,predecessor:"undecidability/exact_multiroute_elimination_v121/abc_quadrics.json",predecessor_git_blob:"6a73cdb44e17e73024650d8977bbf759653ac53a",variables:names.length,variable_names:names,residuals,verification:{full_support:true,quadratic_rows:residuals.length,nested_selector_valuation_fixtures:cases,removed_fields:["chi0","chiU","chiE","chiP"],added_fields:["nestedA","nestedV"],unchanged_rows:keep.length}};
}
const path=new URL("../exact_multiroute_elimination_v121/abc_quadrics.json",import.meta.url);
const raw=fs.readFileSync(path);
const sha=crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex");
assert.equal(sha,"6a73cdb44e17e73024650d8977bbf759653ac53a");
const result=build(JSON.parse(raw));
const out=new URL("./abc_quadrics.json",import.meta.url);
if(process.argv.includes("--write"))fs.writeFileSync(out,JSON.stringify(result,null,2)+"\n");else assert.deepEqual(result,JSON.parse(fs.readFileSync(out,"utf8")));
console.log(result.variables,result.residuals.length,result.verification);
