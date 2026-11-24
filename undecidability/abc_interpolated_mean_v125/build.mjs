import fs from "node:fs";
import crypto from "node:crypto";
import assert from "node:assert/strict";
function build(t){
 const old=t.variable_names;
 const drop=new Set(["n_lift_a","n_lift_a2","n_lift_mean","n_hUinv_0","n_hUinv_1","n_unitT2_0","n_unitT2_1","n_fU2_0","n_fU2_1","n_c3"]);
 const added=["n_trace_h_inv","n_trace_h_unit2","n_nestedV2_0","n_nestedV2_1"];
 const names=old.filter(n=>!drop.has(n)).concat(added);
 const kill=/^new\.(lift\.a2|lift\.mean|xstar\.[01]|U\.h\.guard\.[01]|unitT2\.[01]|fU2\.[01]|c3|slotR\.[01]|nestedA\.[01]|nestedChi\.[01])$/;
 const ix=new Map(names.map((n,i)=>[n,i+1]));
 const row=(name,terms)=>({name,terms:terms.map(([c,...ns])=>({coefficient:String(c),monomial:ns.map(n=>{if(!ix.has(n))throw Error("unknown "+n+" in "+name);return ix.get(n)}).sort((a,b)=>a-b)}))});
 const kept=t.residuals.filter(q=>!kill.test(q.name)).map(q=>row(q.name,q.terms.map(z=>[z.coefficient,...z.monomial.map(i=>old[i-1])])));
 const R=[
 row("new.xstar.0",[[1,"n_xstar_0"],[-1,"n_xU_0"],[1,"n_chord_d_0","n_mean"]]),
 row("new.xstar.1",[[1,"n_xstar_1"],[-1,"n_xU_1"],[1,"n_chord_d_1","n_mean"]]),
 row("new.trace_h_inv",[[2,"n_hU_0","n_trace_h_inv"],[-1]]),
 row("new.trace_h_unit2",[[1,"n_trace_h_unit2"],[-4,"n_hU_0","n_hU_0"],[-4,"n_hU_0","n_trace_h_inv"],[-1,"n_trace_h_inv","n_trace_h_inv"]]),
 row("new.slotR.0",[[1,"n_slotR_0"],[-1,"n_c","n_fU_0"],[-1,"n_c2","n_fH2_0"],[-1,"n_fHP2_0"]]),
 row("new.slotR.1",[[1,"n_slotR_1"],[-1,"n_c","n_fU_1"],[-1,"n_c2","n_fH2_1"],[1,"n_fHP2_1"]]),
 row("new.nestedA.0",[[1,"n_nestedA_0"],[-1,"n_slotR_0","n_slotR_0"],[-2,"n_slotR_1","n_slotR_1"],[-1,"n_u","n_trace_h_unit2"]]),
 row("new.nestedA.1",[[1,"n_nestedA_1"],[-2,"n_slotR_0","n_slotR_1"]]),
 row("new.nestedV2.0",[[1,"n_nestedV2_0"],[-1,"n_nestedV_0","n_nestedV_0"],[-2,"n_nestedV_1","n_nestedV_1"]]),
 row("new.nestedV2.1",[[1,"n_nestedV2_1"],[-2,"n_nestedV_0","n_nestedV_1"]]),
 row("new.nestedChi.0",[[1,"n_chi_0","n_u"],[1,"n_chi_0","n_nestedV2_0"],[2,"n_chi_1","n_nestedV2_1"],[-1,"n_u"]]),
 row("new.nestedChi.1",[[1,"n_chi_1","n_u"],[1,"n_chi_0","n_nestedV2_1"],[1,"n_chi_1","n_nestedV2_0"]])];
 const residuals=kept.concat(R),support=new Set(residuals.flatMap(q=>q.terms.flatMap(z=>z.monomial)));
 if(t.residuals.length-kept.length!==17||names.length!==303||residuals.length!==252||support.size!==303||residuals.some(q=>q.terms.some(z=>z.monomial.length>2)))throw Error("count "+[t.residuals.length-kept.length,names.length,residuals.length,support.size]);
 const vals=[...Array.from({length:13},(_,i)=>2*(i-6)),Infinity];
 let tests=0;
 for(const f of vals)for(const g of vals)for(const h of vals){
  const vR=Math.min(f-1,2*g-2,2*h);
  if((vR>0)!==(f>0&&g>0&&h>0))throw Error("R");
  for(const s of [-8,-3,-1,0,1,3,8]){
   for(const vT of s===0?[0,2,8,Infinity]:[-2*Math.abs(s)]){
    const vA=Math.min(2*vR,1+vT);
    for(const e of [-4,-1,0,1,4,Infinity]){
     const vV=Math.min(2*vA,2*e-1),vChi=1-Math.min(1,2*vV);
     if((vChi===0)!==(f>0&&g>0&&h>0&&s===0&&e>0))throw Error("selector");
     tests++;
    }
   }
  }
 }
 return {...t,predecessor:"undecidability/abc_normalized_moments_v124/abc_quadrics.json",predecessor_git_blob:"11b3c47d7ae7d66746a30f9881109b7cd9056555",variables:names.length,variable_names:names,residuals,verification:{removed_coordinates:[...drop],added_coordinates:added,unchanged_rows:kept.length,replacement_rows:R.length,quadratic_rows:residuals.length,full_support:true,finite_selector_cases:tests}};
}
const p = new URL("../abc_normalized_moments_v124/abc_quadrics.json",import.meta.url);
const raw=fs.readFileSync(p);
const blob=crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex");
assert.equal(blob,"11b3c47d7ae7d66746a30f9881109b7cd9056555");
const out=JSON.stringify(build(JSON.parse(raw)),null,2)+"\n";
const target=new URL("abc_quadrics.json",import.meta.url);
if(process.argv.includes("--write"))fs.writeFileSync(target,out);else assert.equal(out,fs.readFileSync(target,"utf8"));
console.log(JSON.parse(out).verification);
