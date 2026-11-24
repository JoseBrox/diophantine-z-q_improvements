import {naturalSource,source,build,old} from "./build.mjs";

function localChecks(){
 const check=(b,m)=>{if(!b)throw Error(m)};
 const gcd=(a,b)=>{if(a<0n)a=-a;if(b<0n)b=-b;while(b)[a,b]=[b,a%b];return a};
 const R=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}const d=gcd(a,b);return [a/d,b/d]};
 const A=(x,y)=>R(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
 const M=(x,y)=>R(x[0]*y[0],x[1]*y[1]);
 const abs=x=>R(x[0]<0n?-x[0]:x[0],x[1]);
 const lt=(x,y)=>x[0]*y[1]<y[0]*x[1];
 let rootCount=0,gateCount=0,altCount=0;
 for(const r of [R(2),R(3,11)]){
   const c0=M(r,R(1,2)),theta=[R(0),R(-1,2),R(-1),R(1,2399),R(-32,407)];
   const roots=[];for(let i=0;i<8;i++)for(const t of theta)for(const sign of [-1n,1n]){
      const off=M(A(t,M(c0,R(-1))),R(sign*16n**BigInt(i)));
      roots.push(A(c0,off));
   }
   check(new Set(roots.map(t=>t.join("/"))).size===80,"root collision");
   check(roots.every(t=>lt(abs(t),R(2n**30n))),"root radius");
   rootCount+=roots.length;
 }
 const mod4=n=>(n%4+4)%4;
 for(let vq=-15;vq<=15;vq+=2)for(let ve=-12;ve<=12;ve++)for(let v1=-12;v1<=12;v1++)for(let v2=-12;v2<=12;v2++){
   const a=[-vq,4*ve,4*v1-3*vq,4*v2-2*vq];
   check(new Set(a.map(mod4)).size===4,"valuation residues");
   const m=Math.min(...a);
   if(vq<0&&2*m>-vq){check(ve>0&&v1>vq&&v2>vq,"dominance");}
   if(vq>0)check(m<0,"foreign positive odd valuation");
   gateCount++;
 }
 for(let e=1;e<=15;e+=2)for(let t=-10;t<0;t++)for(let f=-20;f<=20;f+=2)for(let err=-20;err<=20;err++){
   const u=e+2*t,l=Math.min(2*err,u+f);
   if(l===u)check(f===0&&err>t,"tie must be excluded by curve identity");
   if(l>u)check(f>0&&2*err>u,"passing implies formal and relative comparison");
   altCount++;
 }
 return {rootCount,gateCount,altCount};
}

const fixtures=[{"x":"100","z":"1","u":"1","y":"1"},{"x":"99","z":"1","u":"2","y":"3"},{"x":"1000","z":"10","u":"17","y":"42"},{"x":"100000000000000000000000000000000000","z":"97","u":"2000","y":"2001"},{"x":"101","z":"3","u":"2","y":"1"}];
for(const params of fixtures){const s=source(naturalSource(old,params),old);for(const [n,variables,rows] of [[2,527,476],[3,560,507]]){const t=build(s,n);if(t.variables!==variables||t.quadratic_rows!==rows||t.integer_certificates!==8||t.source_prefix.variables!==183||t.source_prefix.quadratic_rows!==171)throw Error("census");}}
console.log(JSON.stringify({...localChecks(),fixtureBuilds:10}));
