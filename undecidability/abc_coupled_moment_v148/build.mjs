import fs from "node:fs";
import {fileURLToPath} from "node:url";

function build(t){
  if(t.variables!==291||t.quadratic_residuals!==240)throw Error("unexpected predecessor");
  const removed=["n_variance","n_variance2","n_failTrace","n_failWeighted2","n_Z0","n_Z","n_trace_h_unit4"];
  const added=["n_comb_F","n_comb_G","n_comb_L","n_comb_W","n_comb_W2","n_comb_Z"];
  const removedRows=new Set(["new.variance2","new.failWeighted2","new.variance","new.failWeighted","new.Z0","new.trace_h_unit4","new.Z","new.alpha","new.tau"]);
  const names=t.variable_names.filter(n=>!removed.includes(n)).concat(added);
  const index=new Map(names.map((n,i)=>[n,i+1]));
  function term(c,...ns){return {coefficient:String(c),monomial:ns.map(n=>{if(!index.has(n))throw Error("missing "+n);return index.get(n)}).sort((a,b)=>a-b)}}
  const retained=t.residuals.filter(r=>!removedRows.has(r.name)).map(r=>({name:r.name,terms:r.terms.map(v=>term(v.coefficient,...v.monomial.map(i=>t.variable_names[i-1])))}));
  if(retained.length!==231)throw Error("retained rows");
  const rs=Array.from({length:12},(_,i)=>"n_r"+i), fs=rs.map((_,i)=>"n_fail"+i+"_0");
  const X2=rs.map((_,i)=>i===1?"int_g_29":"n_X2_"+i);
  const [F,G,L,W,W2,Z]=added,a="n_center",c="n_c",u="n_u",T="n_trace_h_unit2",D="n_common_harmonic",alpha="n_alpha",tau="n_tau";
  const rows=[
    {name:"new.combined.F",terms:[term(1,F),...rs.map((r,i)=>term(-1,r,fs[i]))]},
    {name:"new.combined.G",terms:[term(1,G),term(-1,a,F)]},
    {name:"new.combined.L",terms:[term(1,a,L),term(-1,T)]},
    {name:"new.combined.W",terms:[...rs.map(r=>term(1,r,W)),term(12,"n_mean","n_mX"),...rs.map((r,i)=>term(-12,r,X2[i])),term(-12,F,G),term(-12,L,T)]},
    {name:"new.combined.W2",terms:[term(1,W2),term(-1,W,W)]},
    {name:"new.combined.Z",terms:[term(1,Z),term(-1,D,D),term(-1,c,W2)]},
    {name:"new.alpha",terms:[term(1,alpha),term(-1,u),term(-1,Z,Z)]},
    {name:"new.tau",terms:[term(1,tau),term(1,tau,alpha),term(-1,alpha)]}
  ];
  const residuals=retained.concat(rows);
  const support=new Set(residuals.flatMap(r=>r.terms.flatMap(v=>v.monomial)));
  if(names.length!==290||residuals.length!==239||support.size!==names.length||residuals.some(r=>r.terms.some(v=>v.monomial.length>2||v.monomial.some(i=>i<1||i>names.length))))throw Error("census or support");
  const named=(r,ns)=>JSON.stringify(r.terms.map(v=>[v.coefficient,v.monomial.map(i=>ns[i-1]).sort()]).sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b))));
  for(const r of retained){const orig=t.residuals.find(z=>z.name===r.name);if(named(orig,t.variable_names)!==named(r,names))throw Error("changed retained row "+r.name)}
  return {...t,predecessor:"abc_scaled_unit_v145",predecessor_git_blob:"33e936c934153dc454f4683979b2f408083a94ff",variables:names.length,variable_names:names,residuals,quadratic_residuals:residuals.length,verification:{method:"exact quadratic substitution of coupled weighted moment; retained named rows compared",removed_coordinates:removed,added_coordinates:added,physical_alpha:"u+(D^2+c*(variance+c*J^2+u*T^2)^2)^2",retained_all_arithmetic_premises:true}};
}

export {build};
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const t=JSON.parse(fs.readFileSync(new URL("../abc_scaled_unit_v145/abc_quadrics.json",import.meta.url),"utf8"));
 fs.writeFileSync(new URL("./abc_quadrics.json",import.meta.url),JSON.stringify(build(t),null,2)+"\n");
}
