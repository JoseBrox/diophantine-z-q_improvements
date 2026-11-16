// Exact independent reduction-order and Pell-identity check.

const mod=(x,p)=>((x%p)+p)%p;
function inv(a,p){let b=p,u=1n,v=0n;a=mod(a,p);while(b){let q=a/b;[a,b]=[b,a-q*b];[u,v]=[v,u-q*v];}if(a!==1n)throw Error("nonunit");return mod(u,p);}
function prime(n){for(let d=2n;d*d<=n;d++)if(n%d===0n)return false;return n>=2n;}
function check(){
 const p=802231n,l=100279n,r=254335n,assert=(b,s)=>{if(!b)throw Error(s);};
 assert(prime(p)&&prime(l)&&r*r%p===2n,"primes and splitting");
 function slot(r){
  const D=mod(11n-6n*r,p),P=[mod((57n-28n*r)*inv(8n,p),p),mod((-660n+417n*r)*inv(32n,p),p)];
  function add(A,B){if(!A)return B;if(!B)return A;const[x,y]=A,[u,v]=B;let s;
   if(x===u){if(mod(y+v,p)===0n)return null;s=mod((3n*x*x-D)*inv(2n*y,p),p);}
   else s=mod((v-y)*inv(u-x,p),p);
   const X=mod(s*s-x-u,p);return[X,mod(s*(x-X)-y,p)];}
  function mul(n,A){let B=null;for(;n;n>>=1n,A=add(A,A))if(n&1n)B=add(B,A);return B;}
  assert(mod(P[1]*P[1]-P[0]**3n+D*P[0],p)===0n,"point");
  return {P,mul};
 }
 const E=slot(r),Ec=slot(-r);
 assert(E.P[0]===413460n&&E.P[1]===581683n,"given point");
 assert(E.mul(l,E.P)===null,"prime order");
 assert(Ec.mul(2n*l,Ec.P)===null&&Ec.mul(l,Ec.P)!==null&&Ec.mul(2n,Ec.P)!==null,"conjugate order");
 const R=p*(p-1n)*(p-2401n)*(32n*p+343n);
 assert(R%l===10141n&&R%p===0n&&(R/p)%p!==0n,"contact");
 const aNum=87n,aDen=5n,t=111n,b=125n;
 assert(t*t*aDen*aDen-aNum*(aNum-2n*aDen)*t*b+(aNum-2n*aDen)**2n*b*b-aDen*aDen===0n,"rational Pell");
 return {status:"PASS",prime:Number(p),prime_order:Number(l),conjugate_order:Number(2n*l),R_mod_order:Number(R%l),contact_valuation:1,scalar_coordinate_saving_proved:false};
}
console.log(JSON.stringify(check(), null, 2));
