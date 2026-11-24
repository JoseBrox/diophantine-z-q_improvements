import fs from "node:fs";
import crypto from "node:crypto";
import assert from "node:assert/strict";
function build(t){
 const old=t.variable_names,names=old.filter(x=>x!=="n_M16"),ix=new Map(names.map((n,i)=>[n,i+1]));
 function row(name,terms){return {name,terms:terms.map(([coefficient,...ns])=>({coefficient:String(coefficient),monomial:ns.map(n=>{if(!ix.has(n))throw Error(n);return ix.get(n)}).sort((a,b)=>a-b)}))}}
 const residuals=t.residuals.filter(q=>!["new.M16","new.center"].includes(q.name)).map(q=>row(q.name,q.terms.map(z=>[z.coefficient,...z.monomial.map(i=>old[i-1])])));residuals.push(row("new.center",[[1,"n_center"],[-1,"n_M8","n_M4"],[-784]]));
 const support=new Set(residuals.flatMap(q=>q.terms.flatMap(z=>z.monomial)));
 if(names.length!==302||residuals.length!==251||support.size!==302||residuals.some(q=>q.terms.some(z=>z.monomial.length>2)))throw Error("census");
 const cn=1001n**4n,cd=997n**4n,delta=881n*cd-800n*cn;if(delta<=0n)throw Error("height margin");
 return {...t,predecessor:"undecidability/abc_interpolated_mean_v125/abc_quadrics.json",predecessor_git_blob:"806e2e138bf27e0115d391dd5ccd5ecf626718ff",variables:names.length,variable_names:names,residuals,verification:{removed_coordinates:["n_M16"],unchanged_rows:250,replacement_rows:1,quadratic_rows:251,full_support:true,contact_exponent:12,margin_numerator:String(delta),margin_denominator:String(100n*cd)}};
}
const raw=fs.readFileSync(new URL("../abc_interpolated_mean_v125/abc_quadrics.json",import.meta.url));
assert.equal(crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex"),"806e2e138bf27e0115d391dd5ccd5ecf626718ff");
const out=JSON.stringify(build(JSON.parse(raw)),null,2)+"\n";
const target=new URL("abc_quadrics.json",import.meta.url);
if(process.argv.includes("--write"))fs.writeFileSync(target,out);else assert.equal(out,fs.readFileSync(target,"utf8"));
console.log(JSON.parse(out).verification);
