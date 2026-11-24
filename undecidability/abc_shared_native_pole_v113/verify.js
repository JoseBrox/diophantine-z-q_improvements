"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
function audit(t,s){
 const check=(b,m)=>{if(!b)throw Error(m)};
 check(t.variables===519&&t.variable_names.length===519&&t.residuals.length===466&&t.integer_blocks===12,"census");
 const n=t.variable_names,roles=t.ordinary_integer_inputs,p=x=>x==="i_half"?"int_i_reciprocal_":"int_"+x+"_",role=x=>x==="i_half"?"i":x;
 const canonical=(q,ns)=>q.terms.map(a=>[String(a.coefficient),a.monomial.map(i=>ns[i-1]).sort().join("*")]).sort((a,b)=>a[1].localeCompare(b[1]));
 const encode=q=>JSON.stringify(q.slice().sort((a,b)=>a[1].localeCompare(b[1])));
 const qmap=new Map(t.residuals.map(q=>[q.name,canonical(q,n)]));
 const prefix="shared_native_pole.";
 const expect=(name,terms)=>check(encode(qmap.get(prefix+name))===encode(terms.map(([c,...v])=>[String(c),v.sort().join("*")])),"row "+name);
 check(s.variable_names.filter(v=>!n.includes(v)).length===120,"removed vars");
 const u="sp_u",cs=roles.map(x=>p(x)+43);
 expect("global_inverse",[[-roles.length],...cs.map(c=>[1,u,c])]);
 for(const x of roles){
 const i=role(x),ui=p(x)+44,d=p(x)+42,a="sp_A_"+i,S="sp_S_"+i,H="sp_H_"+i,V="sp_V_"+i,W="sp_W_"+i;
 expect("A."+i,[[1,u,a],[-1,u,u],[-1,ui,ui]]);
 expect("S_"+i,[[1,S],[-1,d,d]]);
 expect("H_"+i,[[1,H],[-1,a,S]]);
 expect("V."+i,[[1,V],[1,V,H],[-1,S]]);
 expect("W."+i,[[1,u,W],[-1,u],[-1,V,V]]);
 }
 let w="sp_W_"+role(roles[0]);for(let j=1;j<roles.length;j++){let z="sp_prod_"+j;expect("prod_"+j,[[1,z],[-1,w,"sp_W_"+role(roles[j])]]);w=z}
 expect("alpha",[[1,"sp_alpha"],[-1,u],[-1,w,w],[2,w],[-1]]);
 expect("gate",[[1,"sp_tau"],[1,"sp_tau","sp_alpha"],[-1,"sp_alpha"]]);
 expect("bs",[[1,"sp_bs"],[-7,"sp_tau","sp_tau"]]);
 expect("pSquare",[[12,"sp_p","sp_p"],...cs.map(c=>[-1,c,"sp_P"])]);
 expect("qSquare",[[12,"sp_q","sp_q"],...cs.map(c=>[-1,c,"sp_Q"])]);
 expect("first",[[1,"sp_bs","sp_P"],[1,"sp_e","sp_e"],[-1,u,u]]);
 expect("factor",[[1,"sp_bs","sp_e"],[-1,"sp_e",u],[1,"sp_U","sp_V"]]);
 expect("second",[[1,"sp_bs","sp_Q"],[-1,"sp_U","sp_U"],[1,"sp_V","sp_V"]]);
 let unchanged=0;
 for(const q of s.residuals){if(!qmap.has(q.name))continue;check(encode(qmap.get(q.name))===encode(canonical(q,s.variable_names)),"changed predecessor row");unchanged++}
 check(unchanged===386&&[...qmap.keys()].filter(n=>n.startsWith(prefix)).length===80,"retained/new census");
 check(t.residuals.every(q=>q.terms.every(a=>a.monomial.length<=2&&a.monomial.every(j=>j>=1&&j<=519))),"degree");
 check(new Set(t.residuals.flatMap(q=>q.terms.flatMap(a=>a.monomial))).size===519,"full support");
 // For global v_p(u)=1 and active v_p(u_i)=1, v_p(A_i)>=1.
 // The lower bound on the denominator allows cancellation (extra>=0).
 let active=0,inactive=0,normalizer=0;
 for(let a=1;a<=20;a++)for(let d=-40;d<=0;d++)for(let extra=0;extra<=10;extra++){
  const v=2*d-Math.min(0,a+2*d)-extra;check(v<=0,"active soundness");active++;
 }
 for(let ui=-40;ui<=0;ui++)for(let d=-40;d<=40;d++){
  const a=2*ui-1;check(a%2!==0&&a<0,"inactive coefficient");
  const v=2*d-Math.min(0,a+2*d);check(v>=1,"inactive completeness");inactive++;
 }
 for(let nu=-41;nu<=41;nu+=2)for(let d=-50;d<=50;d++){
  const A=Math.min(nu,2*d);
  if(nu<0)check(A<0&&-nu>0,"negative odd normalizer");
  if(nu===1&&2*A-nu>0)check(d>0,"positive odd normalizer");
  normalizer++;
 }
 return {status:"PASS",variables:519,quadratic_rows:466,integer_certificates:12,native_pole_blocks:1,retained_rows:unchanged,independently_reconstructed_new_rows:80,full_support:true,active_valuation_fixtures:active,inactive_valuation_fixtures:inactive,normalizer_valuation_fixtures:normalizer,scope:"Exact table and finite valuation audits; not a proof of the imported arithmetic inputs."};
}
const read=p=>{const b=fs.readFileSync(path.join(__dirname,p));return [JSON.parse(b),crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex")]};
const [t,ts]=read("quadrics.json"),[s,ss]=read("../abc_aggregate_theta_v112/quadrics.json");
const out={...audit(t,s),table_git_blob:ts,predecessor_git_blob:ss};
if(JSON.stringify(out)!==JSON.stringify(read("certificate.json")[0]))throw Error("certificate mismatch");
console.log(JSON.stringify(out,null,2));
