
export function verify() {
 const check=(b,m)=>{if(!b)throw Error(m)};
 const abs=x=>x<0n?-x:x;
 const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a};
 const f=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);check(b!==0n,"zero denominator");if(b<0n){a=-a;b=-b}const g=gcd(a,b);return[a/g,b/g]};
 const add=(a,b)=>f(a[0]*b[1]+a[1]*b[0],a[1]*b[1]), neg=a=>[-a[0],a[1]], sub=(a,b)=>add(a,neg(b)), mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]), div=(a,b)=>f(a[0]*b[1],a[1]*b[0]), sq=a=>mul(a,a);
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1], sum=a=>a.reduce(add,f(0)), prod=a=>a.reduce(mul,f(1));
 const pol=(a,b)=>{let c=Array.from({length:a.length+b.length-1},()=>f(0));for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)c[i+j]=add(c[i+j],mul(a[i],b[j]));return c};
 const A=t=>{const s=sq(t);return sum([mul(s,sq(s)),mul(f(-45),sq(s)),mul(f(135),s),f(-27)])};
 const B=t=>mul(f(6),prod([t,sub(sq(t),f(1)),sub(sq(t),f(9))]));
 const seeds=[2,4,6,8,10,11,12,13,14,16,17,18], used=new Set(), groups=[];
 let roots=0,coefficientChecks=0,derivativeChecks=0,dyadicChecks=0;
 for(const seed of seeds) {
   const start=f(seed),k=sq(div(A(start),B(start)));let t=start,orb=[];
   for(let n=0;n<6;n++){orb.push(t,neg(t));t=div(sub(mul(f(3),t),f(3)),add(t,f(3)))}
   check(eq(t,start),"period");
   for(const r of orb){const key=r.join("/");check(!used.has(key)&&r[0]!==0n&&abs(r[0])<=18n*r[1],"root collision/radius");used.add(key);check(eq(sq(A(r)),mul(k,sq(B(r)))),"root");roots++}
   const fact=orb.reduce((p,r)=>pol(p,[neg(r),f(1)]),[f(1)]);
   const a=[-27,0,135,0,-45,0,1].map(x=>f(x)),b=[0,54,0,-60,0,6].map(x=>f(x));
   const aa=pol(a,a),bb=pol(b,b);for(let i=0;i<13;i++){check(eq(fact[i],sub(aa[i],mul(k,bb[i]||f(0)))),"factorization");coefficientChecks++}
   groups.push({orb,k});
 }
 const vals=[f(1001),f(805,3),f(1000,7),f(17,11),f(-10001,19),f(0)];
 function chart(t){
   const s=sq(t),Q=mul(sub(s,f(1)),sub(s,f(9)));
   const a=sum([mul(s,Q),mul(f(-35),sq(s)),mul(f(126),s),f(-27)]);
   check(eq(a,A(t))&&a[0]!==0n,"A");
   const R=div(mul(f(6),mul(t,Q)),a),q=sq(R);
   const ax=div(mul(f(6),mul(t,sum([Q,mul(f(-20),s),f(36)]))),a);
   const tx=div(mul(f(6),mul(R,sum([mul(f(5),Q),mul(f(20),s),f(-36)]))),a);
   return {q,ax,tx};
 }
 for(const a of vals)for(const z of vals){
   if(a[0]<=0n)continue;
   const x=sub(a,z),y=add(a,z),xx=chart(x),yy=chart(y),P=mul(xx.q,yy.q);
   for(const {orb,k} of groups){
     const factors=orb.flatMap(r=>[sub(x,r),sub(y,r)]);if(factors.some(r=>r[0]===0n))continue;
     const direct=mul(f(-1,24),sum(factors.map(r=>div(f(1),r))));
     const den=sum([f(1),neg(mul(k,add(xx.q,yy.q))),mul(sq(k),P)]);
     const num=sum([xx.ax,yy.ax,neg(mul(k,sum([mul(xx.ax,yy.q),mul(yy.ax,xx.q),xx.tx,yy.tx]))),mul(sq(k),add(mul(xx.tx,yy.q),mul(yy.tx,xx.q)))]);
     check(eq(direct,div(neg(num),mul(f(12),den))),"log derivative");derivativeChecks++;
   }
 }
 function v2(n){if(!n)return Infinity;let v=0;while(n%2n===0n){n/=2n;v++}return v}
 function val(q){return v2(q[0])-v2(q[1])}
 function fourth(q){return sq(sq(q))}
 for(let i=-5;i<=4;i++)for(let j=-5;j<=4;j++)for(const l of [1,3,7])for(const r of [1,5,9]){
   const pow=e=>e>=0?f(2n**BigInt(e)):f(1n,2n**BigInt(-e));
   const M=add(f(11),mul(f(2),add(fourth(mul(f(l),pow(i))),fourth(mul(f(r),pow(j))))));
   check(val(M)===0||val(M)<=-2,"M dyadic");
   const a=add(fourth(M),f(784)),v=val(a);
   check(v%2===0,"even depth");
   const unit=div(a,pow(v));
   check((unit[0]-unit[1])%8n===0n,"square dyadic unit");dyadicChecks++;
 }
 check(893n*997n**4n>800n*1001n**4n,"margin");
 return {roots,coefficientChecks,derivativeChecks,dyadicChecks,margin:true};
}

console.log(JSON.stringify(verify(),null,2));
