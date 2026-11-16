// Exact independent recovery verifier. Run with Node.js.

const mod=(x,m)=>((x%m)+m)%m;
function inv(x,m) {
 let a=mod(x,m), b=m, u=1n, v=0n;
 while(b){let q=a/b;[a,b]=[b,a-q*b];[u,v]=[v,u-q*v];}
 if(a!==1n)throw new Error("nonunit inverse");return mod(u,m);
}
function pow(x,n,m){let r=1n;for(;n;n>>=1n,x=x*x%m)if(n&1n)r=r*x%m;return r;}
function prime(n){if(n<2n)return false;for(let d=2n;d*d<=n;d++)if(n%d===0n)return false;return true;}
function curve(m) {
 const f=(a,b=0n)=>[mod(a,m),mod(b,m)], add=(a,b)=>f(a[0]+b[0],a[1]+b[1]),
 neg=a=>f(-a[0],-a[1]), sub=(a,b)=>add(a,neg(b)),
 mul=(a,b)=>f(a[0]*b[0]+2n*a[1]*b[1],a[0]*b[1]+a[1]*b[0]),
 inverse=a=>{let r=inv(a[0]*a[0]-2n*a[1]*a[1],m);return f(a[0]*r,-a[1]*r);},
 div=(a,b)=>mul(a,inverse(b)), eq=(a,b)=>a[0]===b[0]&&a[1]===b[1], zero=a=>eq(a,f(0n)),
 D=f(11n,-6n);
 function plus(P,Q) {
  if(P===null)return Q;if(Q===null)return P;
  const[x,y]=P,[u,v]=Q; let s;
  if(eq(x,u)){if(zero(add(y,v)))return null;s=div(sub(mul(f(3n),mul(x,x)),D),mul(f(2n),y));}
  else s=div(sub(v,y),sub(u,x));
  let X=sub(sub(mul(s,s),x),u);return [X,sub(mul(s,sub(x,X)),y)];
 }
 const times=(n,P)=>{let R=null;for(;n;n>>=1n,P=plus(P,P))if(n&1n)R=plus(R,P);return R;};
 const on=P=>P===null||eq(mul(P[1],P[1]),sub(mul(mul(P[0],P[0]),P[0]),mul(D,P[0])));
 const P=plus([f(1n,1n),f(0n,2n)],[f(1n,1n),f(0n,2n)]);
 if(!on(P))throw new Error("P off curve");
 return {P,times,on};
}
function check(c){
 const assert=(b,m)=>{if(!b)throw new Error(m);},p=BigInt(c.prime),m=p*p;
 assert(prime(p)&&p%8n===5n,"inert prime");
 const E=curve(p),N=BigInt(c.annihilator);
 assert(N%p!==0n&&E.times(N,E.P)===null,"annihilator");
 const covered=new Uint8Array(Number(p));
 for(const u of [4n*inv(5n,p)%p,3n*inv(2n,p)%p,5n]){
  const factors=[u-5n,u+2n,2n*u-3n,3n*u-1n,4n*u+1n,5n*u-4n];
  const slopes=[1n,1n,2n,3n,4n,5n];
  let derivative=0n;
  for(let i=0;i<6;i++){let term=slopes[i];for(let j=0;j<6;j++)if(i!==j)term=term*factors[j]%p;derivative=mod(derivative+term,p);}
  assert(mod(factors.reduce((a,b)=>a*b,1n),p)===0n&&derivative!==0n,"simple contact");
  const t=mod((1n-3n*u)*inv(7n*u,p),p),s=mod(-(u+2n)*inv(7n,p),p),a=mod(u*(u+2n)*inv(3n*u-1n,p),p);
  for(const g of [u,3n*u-1n,t,s,a,a-1n,t-1n,s-1n,7n*t*t+5n*t+1n,7n*s*s+5n*s+1n])assert(mod(g,p)!==0n,"contact guard");
 }
 for (const[n,T,u,y]of c.rows){
  const A=E.times(BigInt(n),E.P);assert(A!==null&&E.on(A),"row point");
  assert(mod(2n*A[0][0],p)===BigInt(T),"trace");
  assert(mod(pow(BigInt(y),4n,p)+pow(BigInt(T),4n,p),p)===BigInt(u),"fourth power");
  assert(BigInt(y)!==0n&&mod(A[0][0]*A[0][0]-2n*A[0][1]*A[0][1],p)!==0n&&mod(A[1][0]*A[1][0]-2n*A[1][1]*A[1][1],p)!==0n,"row units");
  for(let x=1n;x<p;x++)covered[Number(mod(BigInt(y)-x*x,p))]=1;
 }
 assert(covered.every(x=>x===1),"coverage");
 const f=c.fixture,E2=curve(m),A=E2.times(BigInt(f.X),E2.P);
 for(let j=0;j<2;j++){assert(A[0][j]===BigInt(f.xA[j]),"fixture x");assert(A[1][j]===BigInt(f.yA[j]),"fixture y");}
 const T=mod(2n*A[0][0],m),u=mod(pow(BigInt(f.X)**2n+BigInt(f.B),4n,m)+pow(T,4n,m),m);
 const t0=mod((1n-3n*u)*inv(7n*u,m),m),t1=mod(-(u+2n)*inv(7n,m),m),a=mod(u*(u+2n)*inv(3n*u-1n,m),m);
 const F=t=>mod(t*(t+1n)*(2n*t+1n)*(3n*t+1n)*(4n*t+1n)*(5n*t+2n)*inv(120n,m),m);
 const q=t=>mod(7n*t*t+5n*t+1n,m);
 const eta=mod(F(t0)*inv(pow(q(t0),3n,m),m),m),weight=mod(F(t0)*inv(4n*pow(t0-1n,8n,m),m),m);
 for(const[k,v]of Object.entries({trace:T,u,t0,t1,a,F0:F(t0),F1:F(t1),q0:q(t0),q1:q(t1),eta,original_weight:weight}))assert(v===BigInt(f[k]),"fixture "+k);
 assert(mod(F(t1)-pow(u,6n,m)*F(t0),m)===0n,"contact identity");
 assert(mod(F(t1)*inv(pow(q(t1),3n,m),m)-eta,m)===0n,"eta symmetry");
 assert(F(t0)/p===44771n&&F(t0)%p===0n&&F(t1)/p===73604n&&F(t1)%p===0n,"exact contact orders");
 return {status:"PASS",rows:c.rows.length,covered:covered.length,prime:c.prime,annihilator_checked:true,fixture_modulus:Number(m),fixture_checked:true};
}
const certificate={
  "schema": "diophantine-order-three-inert-recovery/v54",
  "prime": 81421,
  "prime_squared": 6629379241,
  "annihilator": 6629217184,
  "root_point": "A=[X]P",
  "scope": "Every positive odd B; infinitely many positive X; the displayed deterministic height substitution only",
  "rows": [
    [
      1,
      61080,
      16285,
      8576
    ],
    [
      1,
      61080,
      16285,
      35004
    ],
    [
      6,
      17254,
      16285,
      73321
    ],
    [
      1,
      61080,
      16285,
      46417
    ],
    [
      10,
      74125,
      40712,
      3133
    ],
    [
      9,
      45107,
      16285,
      80711
    ],
    [
      20,
      31595,
      5,
      57446
    ],
    [
      19,
      25083,
      5,
      42108
    ],
    [
      23,
      78190,
      40712,
      73
    ],
    [
      18,
      57250,
      40712,
      1060
    ],
    [
      29,
      41438,
      40712,
      77025
    ],
    [
      24,
      26788,
      40712,
      23167
    ],
    [
      2,
      21974,
      5,
      29234
    ]
  ],
  "fixture": {
    "X": 98,
    "B": 81,
    "xA": [
      1181463837,
      1902694508
    ],
    "yA": [
      3842721784,
      4607123365
    ],
    "trace": 2362927674,
    "u": 4429750217,
    "t0": 4664473388,
    "t1": 2208341072,
    "a": 4421038170,
    "F0": 3645299591,
    "F1": 5992911284,
    "q0": 81629076,
    "q1": 555352286,
    "eta": 5671705439,
    "original_weight": 4486704205,
    "contact_orders": [
      44771,
      73604
    ],
    "invariant_contact_order": 69659
  },
  "prior_checked_package": {
    "certificate_sha256": "3e3130b45776eaa722845f6651ab6bfbdb085eb6e944c86f3fca654a3449b1b7",
    "scoped_paper_sha256": "6f66969212d0be78a6b70a6364560f06d4bf3603903958e5725617b2b534d73a",
    "checker_sha256": "191557bce19d48cd160ae4eaadb4716278623faf25ed2192bd58835058db7c4a",
    "tex_build": {
      "returncode": 0,
      "pages": 5,
      "warnings": []
    }
  }
};
console.log(JSON.stringify(check(certificate), null, 2));
