"use strict";
const fs=require("fs"),path=require("path");
const certificate=function certificate(){
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const k=9,base=[-10,-8,-5,1,2,3,4,6,7],scales=[11,13,17,19,23,29,31,37,41];
 const shifts=scales.flatMap(s=>base.map(c=>s*c));
 assert(shifts.length===81&&new Set(shifts).size===81,"distinct shifts");
 assert(base.reduce((a,b)=>a+b,0)===0,"center");
 assert(shifts.every(c=>c!==0&&!shifts.includes(-c)),"opposite shifts");
 assert(Math.max(...shifts.map(Math.abs))<11**16,"real center");
 // Degree operator bound for rational expressions over the wrapper/point algebra.
 // [numerator degree, scalar denominator degree], common to both K components.
 const d0=2n**211n, guards=[];
 const c=(d=0n)=>[BigInt(d),0n], add=(a,b)=>[a[0]+b[1]>b[0]+a[1]?a[0]+b[1]:b[0]+a[1],a[1]+b[1]],mul=(a,b)=>[a[0]+b[0],a[1]+b[1]],pow=(a,k)=>[a[0]*BigInt(k),a[1]*BigInt(k)],nonzero=a=>{guards.push(2n*a[0]);return a},inv=a=>{nonzero(a);return[a[0]+a[1],2n*a[0]]},div=(a,b)=>mul(a,inv(b));
 const product=xs=>xs.reduce(mul,c()),sum=xs=>xs.reduce(add,c());
 const point=()=>{const h=c(1n),x=pow(h,2),y=mul(h,c(4n));nonzero(h);nonzero(y);return{x,y}};
 const P={x:c(),y:c()},A=Array.from({length:k},point),H=point(),U=point();
 const diff=(p,q)=>{let l=div(add(p.y,q.y),add(p.x,q.x)),x=add(add(pow(l,2),p.x),q.x),y=add(mul(l,add(p.x,x)),p.y);return{x,y}};
 const Hm=diff(H,P),Um=A.map(a=>diff(U,a));
 const f=p=>inv(p.x),z=p=>div(p.x,p.y);
 const R=div(z(U),z(H)),R2=Um.map(p=>div(z(p),z(Hm)));
 const X=Array.from({length:k},(_,i)=>i<8?c(1n):div(c(d0),pow(c(d0),2)));
 const Y=X.map(x=>add(pow(x,2),c()));
 const beta=Y.map(y=>add(pow(y,2),c())),T=A.map(a=>a.x);
 let layer=beta.map((b,i)=>add(pow(b,4),pow(T[i],4)));
 let depth=0;while(layer.length>1){const next=[];for(let j=0;j<layer.length;j+=2)next.push(j+1===layer.length?layer[j]:add(pow(layer[j],4),pow(layer[j+1],4)));layer=next;depth++}
 const M=layer[0],a=pow(M,4),slope=c(1n),xx=add(a,slope),yy=add(a,slope);
 const G=(x,i)=>product(base.map(b=>add(x,c())));
 const GX=Array.from({length:k},(_,i)=>G(xx,i)),GY=Array.from({length:k},(_,i)=>G(yy,i));
 const F=product([...GX,...GY]);nonzero(F);
 // Derivative = sum over 162 products, each obtained by deleting one factor.
 const ff=[...shifts.map(b=>add(xx,c())),...shifts.map(b=>add(yy,c()))];
 const Fa=sum(ff.map((_,i)=>product(ff.filter((_,j)=>j!==i))));
 const u=div(F,Fa);nonzero(u);
 const D=(C)=>div(pow(C,2),add(c(),mul(u,pow(C,2))));
 const w=(L)=>div(u,add(u,pow(L,2)));
 const factors=[];
 for(let i=0;i<k;i++){
   const tests=[f(H),f(U),f(Hm),f(Um[i]),add(R,R2[i]),add(R,Y[i])];
   for(const C of tests){const d=D(C);for(const L of [GX[i],GY[i]])factors.push(add(c(),div(pow(mul(pow(w(L),2),d),2),u)))}
 }
 const W=product(factors),V=inv(W);nonzero(V);
 const eta=div(u,pow(mul(add(c(),u),V),2)),dd=u;
 const rad=mul(add(c(),eta),mul(add(pow(c(1n),4),pow(dd,2)),add(pow(c(1n),4),pow(dd,2))));
 // All fraction denominators are products of already guarded norms.
 guards.push(rad[1],d0);const dg=guards.reduce((a,b)=>a+b,0n);
 const dt=rad[0]+rad[1]>2n*d0+2n?rad[0]+rad[1]:2n*d0+2n;
 const d=dg+dt;
 const n=2n**27n,ell=25n,J=ell*(n+1n)**2n;
 const deg=2n*n*(J+1n)*(1n+d*(1n+2n*J*(1n+ell*(J+1n))));
 assert(100n*1001n**5n<2n*393n*997n**5n,"height margin");
 assert(8+2*(k+2)+1+2+2+1===36,"count");
 // At a selected prime, v(u)=1 and the active gate has v=0; all
 // inactive tests have v(weighted D)>=1. Exhaust finite valuation ranges.
 let checked=0;for(let nu=-21;nu<=21;nu+=2)for(let v=-30;v<=30;v++)for(let l=-30;l<=30;l++){
   const d=Math.max(2*v,-nu),w=Math.max(0,nu-2*l),weighted=d+2*w;
   if(nu<0)assert(2*weighted-nu>0,"negative odd valuation");
   if(nu===1&&l<=0)assert(weighted>=1,"inactive");
   if(nu===1&&l>=1)assert(w===0&&((weighted>0)===(v>0)),"active");
   checked++;
 }
 return {variables:36,unrestricted_degree:true,integer_inputs:k,point_charts:k+2,pole_blocks:1,finite_rank:String(n),separating_elements:Number(ell),aggregate_tree_depth:depth,shift_scales:scales,shifts,valuation_fixtures:checked,degree_upper_bound:deg.toString(),strict_power_of_two_ceiling:deg.toString(2).length,operator_degree_bound:d.toString(),scope:"Exact combinatorial, valuation-integer and degree-ledger checks; not a proof of arithmetic premises."};
};
const c=certificate();
if(JSON.stringify(c)!==JSON.stringify(JSON.parse(fs.readFileSync(path.join(__dirname,"certificate.json")))))throw Error("certificate mismatch");
console.log(JSON.stringify(c,null,2));
