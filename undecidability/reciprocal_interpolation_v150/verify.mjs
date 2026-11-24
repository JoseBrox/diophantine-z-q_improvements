// Independent integer/rational checks for v149/v150 and the shifted Pell estimate.
import assert from "node:assert/strict";
import {build,source,naturalSource,old} from "./build.mjs";

const abs=x=>x<0n?-x:x;
const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a;};
const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);assert(b!==0n);if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];};
const A=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const M=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
const D=(x,y)=>Q(x[0]*y[1],x[1]*y[0]);
const S=(x,y)=>A(x,Q(-y[0],y[1]));
const eq=(x,y)=>x[0]===y[0]&&x[1]===y[1];
const vp=(n,p)=>{if(n===0n)return Infinity;let j=0;n=abs(n);while(n%p===0n){n/=p;j++;}return j;};
const v=(x,p)=>vp(x[0],p)-vp(x[1],p);
const power=(p,e)=>e>=0?Q(p**BigInt(e)):Q(1n,p**BigInt(-e));
const r=y=>M(M(y,S(y,Q(1))),M(S(y,Q(2401)),A(M(Q(32),y),Q(343))));
const base=51948354689656n;
const Y=w=>A(Q(2504),D(w,A(Q(1),w)));
const update=(s,k)=>{let y=Y(M(s,M(k,k)));return M(s,D(r(y),M(Q(base),S(y,Q(2503)))));};
assert(eq(r(Q(2504)),Q(base)));
assert(eq(r(Q(2505)),Q(52515494466240n)));
assert(52515494466240n<2n*base);
assert.equal(vp(base,2n),3);
assert.equal(base%149n,75n);
assert.equal(52515494466240n%149n,134n);

let identities=0,scalarProfiles=0,dyadicProfiles=0,gateProfiles=0,booleanProfiles=0,pellProfiles=0;
for(let i=-40;i<=40;i++)for(let j=1;j<=9;j++){
 const y=Q(i,j),p=S(M(y,y),M(Q(76521,64),y));
 const poly=S(S(M(Q(32),M(p,p)),M(Q(5951086353n,128),p)),M(Q(455376332353657n,8192),y));
 assert(eq(poly,r(y)));identities++;
}
const excluded=abs(r(Q(2503))[0]*base*r(Q(2505))[0])*2n*3n*5n*7n*11n*13n*17n*37n*41n*2399n;
const primes=[61n,67n,71n,73n,79n,83n,89n,97n,101n,103n,107n,109n,113n,127n,131n,137n,139n,149n,151n,157n,163n,167n,173n,179n,181n,191n,193n,197n,199n].filter(p=>excluded%p!==0n);
for(const p of primes){
 for(let e=-7;e<=7;e+=2)for(let k=-5;k<=5;k++){
  const s=power(p,e),ks=power(p,k);const next=update(s,ks);
  assert.equal(v(next,p),e);scalarProfiles++;
 }
 for(let e=1;e<=7;e+=2){
  const w=Q(p**BigInt(e)-1n),y=Y(w);assert.equal(v(y,p),-e);
  assert.equal(v(update(w,Q(1)),p),-3*e);scalarProfiles++;
  // Finite contacts: construct positive integral W, with exact odd depth at a root.
  for(const theta of [Q(0),Q(1),Q(2401),Q(-343,32)]){
   const target=D(S(theta,Q(2504)),S(Q(2505),theta));
   const modulus=p**BigInt(e+1);
   let den=target[1]%modulus;if(den<0n)den+=modulus;
   function inv(a,m){let t=0n,tt=1n,r=m,rr=a;while(rr){let q=r/rr;[t,tt]=[tt,t-q*tt];[r,rr]=[rr,r-q*rr];}assert.equal(r,1n);return (t%m+m)%m;}
   let w0=(target[0]*inv(den,modulus)%modulus+modulus)%modulus;
   const ww=Q(w0+p**BigInt(e)+modulus);
   assert.equal(v(ww,p),0);assert.equal(v(S(Y(ww),theta),p),e);
   assert.equal(v(update(ww,Q(1)),p),e);scalarProfiles++;
  }
 }
}
for(let n=1;n<=3;n++)for(let k=1;k<=12;k++){
 const c=149n**BigInt(n),s=Q(5n*2n**20n*149n*c*c),next=update(s,Q(k));
 assert.equal(v(next,2n),20);assert.equal(v(next,149n),2*n+1);
 // The odd part of next is a unit congruent to one mod 8.
 const odd=D(next,Q(2n**20n));
 assert.equal((odd[0]-odd[1])%8n,0n);dyadicProfiles++;
}
const min=Math.min, odd=x=>Math.abs(x%2)===1;
for(let e=-15;e<=15;e++)if(odd(e))for(let x=-16;x<=16;x++)for(let y=-16;y<=16;y++)for(let h=-10;h<=10;h++){
 const X=2*x-e,Y=2*y-e;
 const terms2=[-e,2*h,2*X-e];
 const terms3=[-e,2*min(2*h,Y),2*X-e];
 for(const [n,terms] of [[2,terms2],[3,terms3]]){
  assert.equal(new Set(terms.map(z=>(z%4+4)%4)).size,n===3?3:new Set(terms.map(z=>(z%4+4)%4)).size);
  // The even term cannot tie the two odd terms, which differ by 2 mod4.
  assert.equal(new Set(terms).size,3);
  const a=min(...terms);
  if(e>0)assert(a<0);
  if(e<0&&a>-e/2){
   assert(h>0);assert(x>5*e/8);
   if(n===3)assert(y>3*e/8);
  }
  gateProfiles++;
 }
}
for(let e=1;e<=21;e+=2)for(let w=0;w<=20;w++)for(let j=-20;j<=20;j++){
 const q=2*j-e;assert(odd(q));const val=q<0?q:(w===0?0:Math.min(w,q));
 assert.equal(val>0,w>0&&j>e/2);booleanProfiles++;
}
function pellY(a,n){let x=0n,y=1n;for(let i=0;i<n;i++)[x,y]=[y,2n*a*y-x];return x;}
for(let i=1;i<=12;i++)for(const U of [16n,17n,32n,64n,129n])for(const Z of [16n,19n,32n,101n])for(const sig of [-1n,1n]){
 const rr=BigInt(i),a=rr*Z*(U+sig),p=2n*U*rr*rr*Z*Z+sig;
 const C=pellY(a,2*i+1),K=pellY(p,i+1),num=(U+sig)**(2n*rr),den=U**rr;
 assert(abs(C*den-K*num)*Z*Z*U<2n*K*num);pellProfiles++;
}
let fixtures=0;
for(const p of [{x:"100",z:"1",u:"1",y:"1"},{x:"99",z:"1",u:"2",y:"3"},{x:"1000",z:"10",u:"17",y:"42"},{x:"100000000000000000000000000000000000",z:"97",u:"2000",y:"2001"},{x:"101",z:"3",u:"2",y:"1"}]){
 const src=source(naturalSource(old,p),old);
 for(const n of [2,3]){
  const t=build(src,n);assert.equal(t.variables,n===2?510:542);assert.equal(t.quadratic_rows,n===2?459:489);
  assert.equal(t.integer_certificates,8);assert.equal(t.source_prefix.variables,183);assert.equal(t.source_prefix.quadratic_rows,171);
  assert.equal(new Set(t.residuals.map(r=>r.name)).size,t.quadratic_rows);
  assert(t.residuals.every(r=>r.terms.every(m=>m.monomial.length<=2)));assert.equal(new Set(t.residuals.flatMap(r=>r.terms.flatMap(m=>m.monomial))).size,t.variables);
  fixtures++;
 }
}
console.log(JSON.stringify({identities,scalarProfiles,dyadicProfiles,gateProfiles,booleanProfiles,pellProfiles,fixtures,scope:"finite exact arithmetic and compiler checks; no proof of retained premises or joint rational Pell integrality"},null,2));
