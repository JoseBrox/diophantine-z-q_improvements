import assert from "node:assert/strict";
import fs from "node:fs";
import crypto from "node:crypto";
function audit(){
 const prime=n=>{if(n<2)return false;for(let d=2;d*d<=n;d++)if(n%d===0)return false;return true};
 const P=x=>(x*x*x-x-1n)*(x*x-x+6n),der=x=>(3n*x*x-1n)*(x*x-x+6n)+(x*x*x-x-1n)*(2n*x-1n);
 const mod=(x,p)=>(x%p+p)%p;let primeChecks=0,liftChecks=0,cutoffChecks=0;
 for(let n=2;n<=5000;n++)if(prime(n)){
   const p=BigInt(n);let a=0n;while(a<p&&(mod(P(a),p)!==0n||mod(der(a),p)===0n))a++;if(a===p)throw Error("no simple root "+p);primeChecks++;
   if(n<=101)for(const depth of [1,2,3]){
       let target=p**BigInt(depth)*(p-1n),x=a,pm=p;
       for(let j=1;j<depth+3;j++){let found=false;for(let k=0n;k<p;k++)if(mod(P(x+k*pm)-target,pm*p)===0n){x+=k*pm;found=true;break;}if(!found)throw Error("Hensel");pm*=p}
       if(mod(P(x)-target,pm)!==0n||mod(der(x),p)===0n||mod(P(x)/p**BigInt(depth),p)!==p-1n)throw Error("exact depth");
       liftChecks++;
   }
 }
 for(let D=1;D<=2000;D++){
   const L=Math.floor(D/2)+1;if(2*L-D<1)throw Error("precision");
   for(let p0 of [3,7,101,4*Math.ceil(L/4)+2]){
     const log=(x,p)=>{let k=0;while(x>=p){x=Math.floor(x/p);k++}return k};
     let r=1;while(4*r-log(4*r+1,p0)<L)r++;
     if(r>Math.ceil(L/3)||p0>4*Math.ceil(L/4)+1&&r!==Math.ceil(L/4))throw Error("cutoff");
     cutoffChecks++;
   }
 }
 return {primeChecks,liftChecks,cutoffChecks}
}
const root=new URL("../../../",import.meta.url);
const read=p=>fs.readFileSync(new URL(p,root));
const blob=b=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex");
const ledger=JSON.parse(read("undecidability/frontier_20261124_v128.json"));
const reg=JSON.parse(read("undecidability/results.json"));
assert.deepEqual(ledger,reg.current_frontier_v128);
const out=[];
for(const [dir,N,R] of [["abc_interpolated_mean_v125",303,252],["abc_paired_height_v126",302,251],["abc_curve_chart_elimination_v128",295,244]]){
 const raw=read("undecidability/"+dir+"/abc_quadrics.json"),t=JSON.parse(raw),sha=blob(raw);
 assert.equal(t.variables,N);assert.equal(t.residuals.length,R);assert.equal(t.variable_names.length,N);
 assert.equal(new Set(t.residuals.flatMap(q=>q.terms.flatMap(z=>z.monomial))).size,N);
 assert.equal(Math.max(...t.residuals.flatMap(q=>q.terms.map(z=>z.monomial.length))),2);
 assert(ledger.quartic_table_audit.some(q=>q.table_git_blob===sha&&q.variables===N&&q.quadratic_rows===R));out.push([N,R,sha]);
}
const checks=audit();assert.deepEqual(checks,{primeChecks:669,liftChecks:78,cutoffChecks:8000});
console.log({checks,tables:out,quartic:ledger.quartic_counts,unrestricted:ledger.unrestricted_counts});
