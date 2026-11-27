"use strict";
function verifyLocal(){
 const assert=(ok,msg)=>{if(!ok)throw Error(msg||"assertion")},mod=(a,b)=>(a%b+b)%b;
 function pow(a,n,m){let v=1n;a=mod(a,m);while(n){if(n&1n)v=v*a%m;a=a*a%m;n>>=1n}return v}
 function fmod(p,r,n,k=3){
  const M=p**BigInt(k), x=mod(1n+r,M), y=mod(2n*r,M), A=mod(-11n+6n*r,M);
  const inv=a=>pow(a,p**BigInt(k-1)*(p-1n)-1n,M), i2=inv(2n*y);
  const memo=new Map([[0,0n],[1,1n],[2,mod(2n*y,M)],[3,mod(3n*x**4n+6n*A*x*x-A*A,M)],[4,mod(4n*y*(x**6n+5n*A*x**4n-5n*A*A*x*x-A**3n),M)]]);
  function psi(n){if(memo.has(n))return memo.get(n);let j=Math.floor(n/2),z;if(n%2)z=psi(j+2)*psi(j)**3n-psi(j-1)*psi(j+1)**3n;else z=psi(j)*i2*(psi(j+2)*psi(j-1)**2n-psi(j-2)*psi(j+1)**2n);z=mod(z,M);memo.set(n,z);return z}
  let den=mod(x*psi(n)**2n-psi(n-1)*psi(n+1),M);
  assert(den%p!==0n,"denominator not a unit");
  return mod(psi(n)**2n*inv(den),M);
 }
 const examples=[];
 for(const [p,r,h] of [[31n,2767n,13143],[167n,1052280n,1070541]]){
  let M=p**3n;assert(mod(r*r-2n,M)===0n,"sqrt2");let inv=a=>pow(a,p*p*(p-1n)-1n,M);
  let D=mod(11n-6n*r,M),Db=mod(11n+6n*r,M),fH=fmod(p,r,h),fOpp=fmod(p,-r,h-1),fT=fmod(p,r,h-1);
  assert(fH%p!==0n&&fOpp%p!==0n&&fT%p!==0n,"unit points");
  let J=mod(-inv(D),M),K=mod(fOpp*fOpp,M),other=mod(fT*fT-inv(Db),p);
  assert(mod(J+K,M)===0n&&other!==0n,"bad sum fixture");
  assert(mod(BigInt(1-2*h),p)!==1n,"wrong label");
  examples.push({p:Number(p),h,root2_mod_p3:Number(r),primary_f:Number(fH),alternate_f:Number(fOpp),J:Number(J),K:Number(K),opposite_sum_mod_p:Number(other),label_mod_p:Number(mod(BigInt(1-2*h),p))})
 }
 // Overapproximations of all possible unit-input valuation profiles.
 const up=new Map;
 for(let d=0;d<=6;d++)for(let e=0;e<=6;e++)for(let a of [-1,1])for(let b of [-1,1]){
  let J=2*(a*d+b*e);for(let C of (d!==e?[-Math.max(d,e)]:[...Array.from({length:7+d},(_,i)=>i-d),Infinity])){
   if(mod(J,4)===2)assert(4*C<=-Math.abs(J)-2,"unit pair bound");
   up.set([C,J].join(","),[C,J]);
  }
 }
 const unit=[...up.values()];
 const actual=new Map();
 for(let e=0;e<=3;e++){
  for(let d=1;d<=6;d++){
   for(let J of [4*(d+e),4*e,-4*d])for(let C of [...Array.from({length:19},(_,i)=>i-10),Infinity])actual.set([C,J].join(","),[C,J]);
   for(let J of [2*e+2*d,2*e-2*d])for(let C of (e<d?[e-d]:[...Array.from({length:7},(_,i)=>i),Infinity]))actual.set([C,J].join(","),[C,J]);
  }
  for(let C of [...Array.from({length:7},(_,i)=>i),Infinity])actual.set([C,2*e].join(","),[C,2*e])
 }
 for(const [C,J] of actual.values())if(J<0&&mod(J,4)===2)assert(C===J/2,"actual identity");
 let unitCases=0,foreignCases=0,depthCases=0;
 for(let mu=1;mu<=15;mu+=2)for(let [C,J] of unit)for(let [I,K] of unit){
  let vs=[-3*mu+4*C,-5*mu+4*I,-2*mu+J,-4*mu+K],m=Math.min(...vs);
  if(m<0)assert(vs.filter(v=>v===m).length===1,"consumed negative minimum");
  if(4*m>-3*mu)assert(16*C>9*mu&&16*I>17*mu&&4*J>5*mu&&4*K>13*mu,"local threshold");
  unitCases++;
 }
 for(let j=1;j<=11;j+=2)for(let [C,J] of actual.values())for(let [I,K] of actual.values()){
  let vs=[3*j+4*C,5*j+4*I,2*j+J,4*j+K],m=Math.min(...vs);
  if(m<0)assert(vs.filter(v=>v===m).length===1,"foreign negative minimum");
  foreignCases++;
 }
 for(let mu=1;mu<=20001;mu+=2){
  let d1=1+Math.floor(5*mu/16),d2=1+Math.floor(13*mu/16),e=2+Math.floor(9*mu/16)+Math.floor(5*mu/16);
  assert(Math.min(4*d1,4*d2,1+Math.floor(9*mu/16)+d1,1+Math.floor(17*mu/16)+d2)>=e&&e>=2,"precision");
  depthCases++;
 }
 return {examples,unit_profiles:unitCases,foreign_profiles:foreignCases,depth_profiles:depthCases}
}
console.log(JSON.stringify(verifyLocal(),null,2));
