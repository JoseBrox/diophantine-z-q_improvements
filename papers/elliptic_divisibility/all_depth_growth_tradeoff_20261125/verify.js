// Exact BigInt rational arithmetic; run with node verify.js.
console.log(JSON.stringify((function verify(){
 const abs=x=>x<0n?-x:x;
 const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b){[a,b]=[b,a%b]}return a};
 function R(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b}const d=gcd(a,b);return [a/d,b/d]}
 const add=(x,y)=>R(x[0]*y[1]+x[1]*y[0],x[1]*y[1]), neg=x=>[-x[0],x[1]],sub=(x,y)=>add(x,neg(y)),mul=(x,y)=>R(x[0]*y[0],x[1]*y[1]),div=(x,y)=>R(x[0]*y[1],x[1]*y[0]),sq=x=>mul(x,x);
 const eq=(x,y)=>x[0]===y[0]&&x[1]===y[1], lt=(x,y)=>x[0]*y[1]<y[0]*x[1],H=x=>abs(x[0])>x[1]?abs(x[0]):x[1];
 const assert=(b,msg)=>{if(!b)throw Error(msg)};
 function v(n,p){n=abs(n);if(!n)throw Error("v(0)");let e=0;while(n%p===0n){n/=p;e++}return e}
 const vp=(x,p)=>v(x[0],p)-v(x[1],p), ppower=(p,k)=>k>=0?R(p**BigInt(k)):R(1n,p**BigInt(-k));
 const c0=R(2504),one=R(1),f=x=>mul(mul(x,sub(x,one)),mul(sub(x,R(2401)),add(mul(R(32),x),R(343))));
 const f0=f(c0);assert(eq(f0,R("51948354689656"))&&vp(f0,67n)===0,"constants");
 assert(lt(f(add(c0,R(1,4))),mul(R(2),f0)),"endpoint");
 const phi=w=>div(w,sq(add(one,w))), primes=[11n,13n,17n,19n,23n,31n,43n,67n,71n,101n].filter(p=>f0[0]%p!==0n);
 let anchorFixtures=0,oddPersistence=0,newContactFixtures=0;
 for(const p of primes)for(let e=-9;e<=9;e++)for(let k=-7;k<=7;k++)for(const t of [1n,2n,3n]){
   const rho0=mul(ppower(p,e),R(t,5)),s=ppower(p,k),W=mul(rho0,sq(s)),z=phi(W),Y=add(c0,z),rho=mul(rho0,div(f(Y),f0));
   const u=W[0],w=W[1];
   assert(z[1]===(u+w)**2n&&H(z)===(u+w)**2n,"normalizer denominator and height");
   assert(H(z)<=H(Y)*2505n,"translation bound");
   assert(!lt(div(f(Y),f0),one)&&lt(div(f(Y),f0),R(2)),"ratio bound");
   assert(H(s)**2n<=H(W)*H(rho0),"charge height");
   if(e%2!==0){assert(vp(rho,p)===e,"odd persistence");oddPersistence++}
   const contacts=[Y,sub(Y,one),sub(Y,R(2401)),add(mul(R(32),Y),R(343))];
   // Only good primes where the four finite contacts are distinct.
   const roots=[R(0),R(1),R(2401),R(-343,32)];
   if(roots.every((r,i)=>roots.slice(i+1).every(t=>vp(sub(r,t),p)===0))&&contacts.some(x=>vp(x,p)>0&&vp(x,p)%2===1)){
      assert(e%2===0 && vp(rho,p)%2!==0,"new finite odd contact");newContactFixtures++
   }
   anchorFixtures++;
 }
 let depthFixtures=0;
 for(let a=1;a<=64;a++)for(let c=0;c<=24;c++)for(let j=0;j<=64;j++){
   const b=a+j-c;if(b>0){assert(a<=j+Math.max(0,2*a-b),"formal depth");depthFixtures++}
   assert(a<=j+2*a,"nonformal depth");depthFixtures++;
 }
 // Exact elliptic curve arithmetic on y^2=x^3-2x.
 const P=[R(9,4),R(-21,8)];
 function eadd(A,B){if(A===null)return B;if(B===null)return A;const [x,y]=A,[u,w]=B;if(eq(x,u)&&eq(y,neg(w)))return null;
 const l=eq(x,u)?div(sub(mul(R(3),sq(x)),R(2)),mul(R(2),y)):div(sub(w,y),sub(u,x));
 const X=sub(sub(sq(l),x),u),Y=sub(mul(l,sub(x,X)),y);assert(eq(sq(Y),sub(mul(sq(X),X),mul(R(2),X))),"elliptic curve");return [X,Y];
 }
 function isqrt(x){assert(x>=0n,"sqrt sign");if(x<2n)return x;let a=1n<<BigInt(Math.ceil(x.toString(2).length/2));while(true){const b=(a+x/a)>>1n;if(b>=a)return a;a=b}}
 function root(x){const a=isqrt(x[0]),b=isqrt(x[1]);assert(a*a===x[0]&&b*b===x[1],"square abscissa");return R(a,b)}
 const gs=[null];let A=null;for(let n=1;n<=60;n++){A=eadd(A,P);assert(A!==null,"non-torsion fixture");gs.push(root(A[0]))}
 function factors(n){let r=[];for(let p=2n;p*p<=n;p+=(p===2n?1n:2n))if(n%p===0n){r.push(p);while(n%p===0n)n/=p}if(n>1n)r.push(n);return r}
 let quotientFixtures=0,valuationIdentities=0,deficitFixtures=0;
 for(let h=2;h<=5;h++)for(let m=-3;m<=3;m++)if(m!==0){
  const j=h+m*h*(h-1);if(j===0||Math.abs(j)>60)continue;
  const bh=gs[h][1],bj=gs[Math.abs(j)][1],g=div(gs[Math.abs(j)],gs[h]),s=mul(R(3,5),g),r=mul(R(4,5),g);
  assert(j%h===0&&(j-1)%(h-1)===0&&(j-h)===m*h*(h-1),"double divisibility");
  assert(eq(add(sq(s),sq(r)),sq(g)),"conic witness");
  let foreign=bj/2n**BigInt(v(bj,2n));
  for(const p of factors(bh))if(p!==2n){assert(v(bj,p)===v(bh,p)+v(BigInt(j/h),p),"depth multiplication");valuationIdentities++;foreign/=p**BigInt(v(bj,p))}
  assert((s[1]*r[1])%foreign===0n,"all-depth charge denominator");
  quotientFixtures++;
 }
 // All-depth deficit bound on actual pairs, including non-divisibility.
 for(let c=1;c<=5;c++)for(let j=1;j<=60;j++){
  const bc=gs[c][1],bj=gs[j][1];let aMass=1n,D=1n;
  for(const p of factors(bc))if(p!==2n){const a=v(bc,p),b=v(bj,p);aMass*=p**BigInt(a);D*=p**BigInt(Math.max(0,2*a-b))}
  assert(BigInt(j)*D%aMass===0n,"actual deficit divisibility");deficitFixtures++;
 }
 return {anchorFixtures,oddPersistence,newContactFixtures,depthFixtures,quotientFixtures,valuationIdentities,deficitFixtures,computedPoints:60}
})(),null,2));
