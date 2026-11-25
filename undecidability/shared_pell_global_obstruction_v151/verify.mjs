// Independent finite checks of the identities in v151; not the infinite-point proof.
function checks() {
  const assert=(b,m)=>{if(!b)throw Error(m)};
  const abs=x=>x<0n?-x:x;
  const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a};
  const lcm=(a,b)=>a/gcd(a,b)*b;
  const mod=(x,p)=>(x%p+p)%p;
  function pell(A,n,p=0n){
    let x=1n,y=0n,u=A,v=1n,D=A*A-1n;
    const red=x=>p?mod(x,p):x;
    while(n>0n){
      if(n&1n)[x,y]=[red(x*u+D*y*v),red(x*v+y*u)];
      [u,v]=[red(u*u+D*v*v),red(2n*u*v)];
      n>>=1n;
    }return [x,y];
  }
  function val(x,p){assert(x!==0n,"valuation of zero");let e=0n;while(x%p===0n){x/=p;e++;}return e}
  const primes=[3n,5n,7n,11n,13n,17n,19n,23n,29n,31n,37n,41n,43n,47n];
  let profiles=0,good=0;
  for(const p of primes)for(let a=2n;a<=16n;a++)for(let g=2n;g<=16n;g++){
    const A=mod(a*a-1n,p),D=mod(g*g-1n,p);
    if(!A||!D)continue;
    for(let v=1n;v<=12n;v++){
      const [iv,H]=pell(g,v,p);if(iv!==0n)continue;
      assert(mod(D*H*H+1n,p)===0n,"Pell branch");
      for(let n=1n;n<=6n;n++){
        const [t,k]=pell(a,n,p);if(!t)continue;
        for(let beta=1n;beta<p;beta++){
          const base=beta*beta*D*t*t-4n*A,shift=4n*A*k*H*beta*D;
          const B=mod(base*base+16n*A*A*k*k*beta*beta*D,p);
          assert(mod((base+shift)*(base-shift),p)===B,"branch resultant identity");
          if(B!==0n){
            assert(mod(base+shift,p)!==0n,"second root excluded");
            assert(mod(t*t,p)!==0n,"first root excluded");
            good++;
          }
          profiles++;
        }
      }
    }
  }
  // Explicit example: norm, fixed sum and nonintegrality.
  const den=331837n,k=1952365n,t=-3397838n,H=-293180n,I=-606613n;
  assert(k+H===5n*den,"shared sum");
  assert(t*t-3n*k*k===den*den&&I*I-3n*H*H===den*den,"both rational norms");
  assert(k%den!==0n&&H%den!==0n,"both nonintegral");
  // Polynomial identity with integer coefficients in ascending degree.
  const mul=(a,b)=>{let c=Array(a.length+b.length-1).fill(0n);for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)c[i+j]+=a[i]*b[j];return c};
  const F=[76n,-60n,-444n,180n,684n],Q=[2993n,-1200n,-8931n];
  const L=mul(Q,Q).map((x,i)=>117649n*F[i]-x);
  const R=mul(mul(mul([-1n,3n],[-1n,3n]),[-1n,3n]),[1115n,1751n]).map(x=>15n*x);
  assert(L.every((x,i)=>x===R[i]),"osculating quartic");
  const [Iv0,Hv0]=pell(2n,2n);
  assert(Iv0===7n&&Hv0===4n,"base point");
  assert(mod(1n+3n*(1n+2n*Hv0)**2n,7n)!==0n,"good reduction example");
  assert(432n%7n!==0n,"B* unit");
  // Independently demonstrate prime-freezing for a fixed finite set.
  const S=[2n,3n,7n,11n];let T=4n;
  const mods=S.map(p=>p**(val(Iv0,p)+1n));
  for(const m of mods){
    let order=1n,x=2n%m,y=1n%m;
    while(x!==1n||y!==0n){[x,y]=[mod(2n*x+3n*y,m),mod(x+2n*y,m)];order++}
    T=lcm(T,order);
  }
  let frozen=0,hasOutside=0;
  for(let n=1n;n<=3n;n++){
    const v=2n+n*T;
    for(let i=0;i<S.length;i++){
      assert(pell(2n,v,mods[i])[0]===mod(Iv0,mods[i]),"frozen valuation");frozen++;
    }
    const [x]=pell(2n,v);
    let rest=x;
    for(const p of S)while(rest%p===0n)rest/=p;
    assert(rest>1n,"outside prime exists");hasOutside++;
  }
  return {profiles,goodReductionProfiles:good,explicitRationalPoint:true,quarticIdentity:true,frozenValuationChecks:frozen,termsWithOutsidePrime:hasOutside,progressionStep:String(T)};
}

console.log(JSON.stringify(checks(),null,2));
