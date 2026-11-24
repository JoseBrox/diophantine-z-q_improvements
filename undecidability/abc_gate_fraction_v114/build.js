"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
function build(t){
 const chk=(b,m)=>{if(!b)throw Error(m)};
 const roles=t.ordinary_integer_inputs,k=roles.length,old=t.variable_names;
 const prefix=x=>x==="i_half"?"int_i_reciprocal_":"int_"+x+"_",role=x=>x==="i_half"?"i":x;
 chk(t.variables===519&&t.residuals.length===466&&k===12,"input");
 const removed=new Set(roles.flatMap(x=>["A_","S_","H_"].map(p=>"sp_"+p+role(x))));
 const drops=new Set(roles.flatMap(x=>["A."+role(x),"S_"+role(x),"H_"+role(x),"V."+role(x),"W."+role(x)].map(s=>"shared_native_pole."+s)));
 const keep=t.residuals.filter(q=>!drops.has(q.name));
 chk(removed.size===36&&drops.size===60&&keep.length===406,"removed census");
 chk(keep.every(q=>q.terms.every(a=>a.monomial.every(j=>!removed.has(old[j-1])))),"external support");
 const names=old.filter(n=>!removed.has(n)), added=[];
 const reg=n=>{chk(!names.includes(n),"duplicate "+n);names.push(n);return n};
 const row=(n,terms)=>added.push({name:"fraction_gate."+n,terms});
 const u="sp_u",cs=roles.map(x=>prefix(x)+43);
 for(const x of roles){
   const i=role(x),ui=prefix(x)+44,d=prefix(x)+42,V="sp_V_"+i,W="sp_W_"+i;
   const R=reg("fg_R_"+i),T=reg("fg_T_"+i);
   row("R."+i,[[1,R],[-1,ui,d]]);
   row("T."+i,[[1,T],[-1,u],[-1,R,R]]);
   row("V."+i,[[1,V,T],[-1,d,d]]);
   row("W."+i,[...cs.map(c=>[1,c,W]),...cs.map(c=>[-1,c]),[-k,V,V]]);
 }
 const pos=new Map(names.map((n,i)=>[n,i+1]));
 const out=keep.map(q=>({...q,terms:q.terms.map(a=>({...a,monomial:a.monomial.map(j=>pos.get(old[j-1])).sort((a,b)=>a-b)}))}));
 for(const q of added)out.push({name:q.name,terms:q.terms.map(([c,...v])=>({coefficient:String(c),monomial:v.map(n=>{chk(pos.has(n),"missing "+n);return pos.get(n)}).sort((a,b)=>a-b)}))});
 chk(names.length===507&&out.length===454&&added.length===48,"count");
 chk(out.every(q=>q.terms.every(a=>a.monomial.length<=2&&a.monomial.every(j=>Number.isInteger(j)&&j>0&&j<=names.length))),"degree");
 chk(new Set(out.flatMap(q=>q.terms.flatMap(a=>a.monomial))).size===507,"full support");
 // Independent named monomial comparison.
 const key=(q,ns)=>JSON.stringify(q.terms.map(a=>[a.coefficient,a.monomial.map(j=>ns[j-1]).sort().join("|")]).sort((a,b)=>a[1].localeCompare(b[1])));
 chk(keep.every((q,i)=>key(q,old)===key(out[i],names)),"retained rows");
 let cases=0;for(let s=-80;s<=80;s++)for(let d=-80;d<=80;d++){
  const v=2*d-Math.min(1,2*s+2*d),w=Math.min(0,1+2*v);
  if(s===1)chk((w===0)===(d>=1),"active");
  if(s<=0)chk(w===0&&v>=0,"inactive");
  cases++;
 }
 return {...t,status:"proved_transfer_under_retained_arithmetic_premises_and_ordinary_rational_abc",predecessor:"../abc_shared_native_pole_v113/quadrics.json",predecessor_git_blob:"6ce58651bd67458f8a1cdfe30061d411d882c19d",variables:names.length,variable_names:names,residuals:out,removed_coordinates:[...removed],removed_rows:[...drops],verification:{retained_rows:keep.length,new_rows:added.length,removed_coordinates:removed.size,added_coordinates:24,finite_valuation_cases:cases,full_support:true}};
}
const raw=fs.readFileSync(path.join(__dirname,"../abc_shared_native_pole_v113/quadrics.json"));
if(crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex")!=="6ce58651bd67458f8a1cdfe30061d411d882c19d")throw Error("predecessor blob");
const t=build(JSON.parse(raw)),dest=path.join(__dirname,"quadrics.json");
if(process.argv.includes("--write"))fs.writeFileSync(dest,JSON.stringify(t)+"\n");else if(JSON.stringify(t)!==JSON.stringify(JSON.parse(fs.readFileSync(dest))))throw Error("table mismatch");
console.log(JSON.stringify({status:"PASS",variables:t.variables,rows:t.residuals.length,verification:t.verification}));
