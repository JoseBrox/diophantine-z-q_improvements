import fs from "node:fs";
import crypto from "node:crypto";
import assert from "node:assert/strict";
function build(t){
  const old=t.variable_names, drop=new Set(["n_au","n_mX2","n_failSum_0"]), names=old.filter(n=>!drop.has(n)), ix=new Map(names.map((n,i)=>[n,i+1]));
  const row=(name,terms)=>({name,terms:terms.map(([c,...ns])=>({coefficient:String(c),monomial:ns.map(n=>{if(!ix.has(n))throw Error("unknown "+n);return ix.get(n)}).sort((a,b)=>a-b)}))});
  const kill=new Set(["new.au","new.derivative_sum","new.mX2","new.mean","new.variance","new.failSum.scalar","new.failWeighted"]);
  const keep=t.residuals.filter(q=>!kill.has(q.name)).map(q=>row(q.name,q.terms.map(z=>[z.coefficient,...z.monomial.map(i=>old[i-1])])));
  if(t.residuals.length-keep.length!==7)throw Error("source row count");
  const rs=Array.from({length:12},(_,i)=>"n_r"+i);
  const R=[row("new.derivative_sum",[[ -12,"n_c"],...rs.map(n=>[1,"n_center",n])]),
     row("new.mean",[[ -1,"n_mX"],...rs.map(n=>[1,"n_mean",n])]),
     row("new.variance",[[12,"n_mean","n_mX"],...rs.map(n=>[1,"n_variance",n]),...rs.map((n,i)=>[-12,n,i===1?"int_g_29":"n_X2_"+i])]),
     row("new.failWeighted",[...rs.map(n=>[1,"n_failTrace",n]),...rs.map((n,i)=>[-12,n,"n_fail"+i+"_0"])])];
  const residuals=keep.concat(R);const supp=new Set(residuals.flatMap(q=>q.terms.flatMap(z=>z.monomial)));
  if(names.length!==309||residuals.length!==257||supp.size!==309||residuals.some(q=>q.terms.some(z=>z.monomial.length>2)))throw Error("census");
  return {...t,predecessor:"undecidability/abc_scalar_failures_v123/abc_quadrics.json",predecessor_git_blob:"cf078c133131eb5550e165854ec94f7b9cb5857b",variables:names.length,variable_names:names,residuals,verification:{removed_coordinates:[...drop],removed_rows:[...kill],replacement_rows:R.length,quadratic_rows:residuals.length,full_support:true,unchanged_rows:keep.length}};
}
const raw=fs.readFileSync(new URL("../abc_scalar_failures_v123/abc_quadrics.json",import.meta.url));
assert.equal(crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex"),"cf078c133131eb5550e165854ec94f7b9cb5857b");
const result=build(JSON.parse(raw));const out=new URL("./abc_quadrics.json",import.meta.url);
if(process.argv.includes("--write"))fs.writeFileSync(out,JSON.stringify(result,null,2)+"\n");else assert.deepEqual(result,JSON.parse(fs.readFileSync(out,"utf8")));console.log(result.variables,result.residuals.length,result.verification);
