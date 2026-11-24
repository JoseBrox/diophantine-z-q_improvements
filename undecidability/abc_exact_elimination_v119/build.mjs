// Exact named-monomial elimination. Run node build.js [--write].
import fs from "node:fs";
import assert from "node:assert/strict";
function reduce(t){
 const names=t.variable_names.slice(); const rows=t.residuals.map(q=>({name:q.name,terms:q.terms.map(a=>({c:a.coefficient,m:a.monomial.map(i=>names[i-1]).sort()}))}));
 const changes=[];
 function sum(terms){
 const a=new Map();for(const z of terms){const key=z.m.join("\u0001");if(!/^-?\d+$/.test(z.c))throw Error("non-numeric changed coefficient");a.set(key,(a.get(key)||0n)+BigInt(z.c))}
 return [...a].filter(([k,c])=>c!==0n).map(([k,c])=>({c:String(c),m:k?k.split("\u0001"):[]}));
 }
 function elim(n,row){
 const i=rows.findIndex(q=>q.name===row);if(i<0)throw Error(row);const q=rows[i];const a=q.terms.find(z=>z.m.length===1&&z.m[0]===n);
 if(!a||!["1","-1"].includes(a.c)||q.terms.filter(z=>z.m.includes(n)).length!==1)throw Error("bad solved row");
 const P=q.terms.filter(z=>z!==a).map(z=>({c:String(-BigInt(z.c)*BigInt(a.c)),m:z.m}));
 rows.splice(i,1);const affected=[];
 for(const s of rows){if(!s.terms.some(z=>z.m.includes(n)))continue;let terms=s.terms;while(terms.some(z=>z.m.includes(n))){
 terms=terms.flatMap(z=>{const j=z.m.indexOf(n);if(j<0)return [z];return P.map(w=>({c:String(BigInt(z.c)*BigInt(w.c)),m:[...z.m.slice(0,j),...z.m.slice(j+1),...w.m].sort()}))});}
 if(terms.some(z=>z.m.length>2))throw Error("degree overflow");
 s.terms=sum(terms);affected.push(s.name);
 }changes.push({variable:n,solved_row:row,formula:P,affected});names.splice(names.indexOf(n),1);
 }
 const F=rows.find(q=>q.name==="new.Fcoef6"),S=rows.find(q=>q.name==="new.SS");
 F.terms=sum([...F.terms,...S.terms.map(a=>({c:String(-847974400n*BigInt(a.c)),m:a.m}))]);if(F.terms.some(a=>a.m.length>1))throw Error("nonlinear Fcoef6");
 for(const [n,q] of [["n_H0_0","new.H0.0"],["n_H0_1","new.H0.1"],["n_sigsum_0","new.sigsum.0"],["n_sigsum_1","new.sigsum.1"],["n_Fcoef6","new.Fcoef6"]])elim(n,q);
 const ids=new Map(names.map((n,i)=>[n,i+1]));const residuals=rows.map(q=>({name:q.name,terms:q.terms.map(a=>({coefficient:a.c,monomial:a.m.map(n=>ids.get(n)).sort((a,b)=>a-b)})).sort((a,b)=>a.monomial.length-b.monomial.length||a.monomial.join(",").localeCompare(b.monomial.join(",")))}));
 if(residuals.some(q=>q.terms.some(z=>z.monomial.length>2||z.monomial.some(i=>!i))))throw Error("bad output");const support=new Set(residuals.flatMap(q=>q.terms.flatMap(a=>a.monomial)));if(support.size!==names.length)throw Error("support");
 const {verification,...rest}=t;return {...rest,predecessor:"../abc_primary_moments_v118/quadrics.json",predecessor_git_blob:"e54ea8acafa206a53a504fa17516db3f9513b2e4",variables:names.length,variable_names:names,verification:{eliminated:changes,linear_row_operation:"new.Fcoef6 -= 847974400*new.SS",outer_rows:52,new_rows:residuals.length-52,full_support:true,previous_verification:verification},residuals};
}
const t=JSON.parse(fs.readFileSync(new URL("../abc_primary_moments_v118/quadrics.json",import.meta.url),"utf8"));
const out=reduce(t);
assert.equal(out.variables,368);assert.equal(out.residuals.length,317);
const dest=new URL("quadrics.json",import.meta.url);
if(process.argv.includes("--write"))fs.writeFileSync(dest,JSON.stringify(out,null,2)+"\n");else assert.deepEqual(JSON.parse(fs.readFileSync(dest,"utf8")),out);
console.log("368 variables, 317 residuals: exact reversible elimination verified");
