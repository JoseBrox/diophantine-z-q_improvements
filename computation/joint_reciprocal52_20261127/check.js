const fs=require('node:fs'),assert=require('node:assert/strict');
function build(old){
 const m=(a=1,...xs)=>new Map([[xs.sort((a,b)=>a-b).join(","),BigInt(a)]]);
 const plus=(...pp)=>{let r=new Map;for(let p of pp)for(let [k,v]of p)r.set(k,(r.get(k)||0n)+v);return new Map([...r].filter(([k,v])=>v))};
 const scale=(p,a)=>new Map([...p].map(([k,v])=>[k,v*BigInt(a)]).filter(([k,v])=>v));
 const minus=(p,q)=>plus(p,scale(q,-1));
 const mul=(p,q)=>plus(...[...p].flatMap(([a,v])=>[...q].map(([b,w])=>m(v*w,...[a,b].filter(Boolean).flatMap(k=>k.split(",").map(Number))))));
 const x=i=>m(1,i),one=m(), zero=new Map(),f=(i)=>[x(i),x(i+1)], constf=(a,b=0)=>[m(a),m(b)], fp=(p)=>[p,zero],fa=(...a)=>[plus(...a.map(q=>q[0])),plus(...a.map(q=>q[1]))],fs=(a,b)=>fa(a,[scale(b[0],-1),scale(b[1],-1)]),fc=a=>[a[0],scale(a[1],-1)],fm=(a,b)=>[plus(mul(a[0],b[0]),scale(mul(a[1],b[1]),2)),plus(mul(a[0],b[1]),mul(a[1],b[0]))],fscl=(a,n)=>a.map(p=>scale(p,n)),sq=a=>fm(a,a);
 let l=f(2),w=f(4),v=f(6),s=f(9),t=f(11),Y=f(13),Z=f(15),h=f(17),d=f(19),ks=f(21),Bs=f(23),Pc=f(25),Qc=f(27),Ws=f(31),c=fp(x(43)),u=fp(x(44)),X4=fp(x(30));
 let a=constf(1,1),b=constf(4,-2),delta=constf(-23,17),Delta=constf(11,-6),aD=fm(a,Delta),rho=fs(fs(v,fm(a,fa(l,w))),fscl(b,2)),Knum=fm(constf(23,17),rho),S=fs(fs(v,b),fm(a,l)),T=fa(fs(fm(a,w),v),b),C=fs(s,S),I=fs(t,T),p=fa(h,s,t);
 let rows=[];function row(name,q){let terms=[...q].map(([k,v])=>({parameterPower:0,monomial:k?k.split(",").map(Number):[],coefficient:v.toString()})).filter(t=>t.coefficient!=="0"); terms.sort((a,b)=>a.monomial.length-b.monomial.length||JSON.stringify(a.monomial).localeCompare(JSON.stringify(b.monomial))); let g=0n;const gcd=(a,b)=>b?gcd(b,a%b):a;for(let t of terms){let z=BigInt(t.coefficient);g=gcd(g,z<0n?-z:z)} if(g===0n)throw Error(name);for(let t of terms){t.coefficient=(BigInt(t.coefficient)/g).toString();if(t.monomial.length>2)throw Error("degree "+name)}rows.push({name,terms})}
 function field(name,z){row(name+".0",z[0]);row(name+".1",z[1])}
 field("reference.unit",fs(fm(a,fm(l,w)),constf(1)));
 field("reference.secant",fs(fm(v,rho),delta));
 row("pair.differenceReal",minus(x(8),fm(h,p)[0]));
 field("joint.firstProduct",fs(fm(l,d),fm(p,Y)));
 field("joint.secondProduct",fs(fm(w,d),fm(h,Z)));
 field("joint.secant",fa(fs(fm(aD,fa(fm(w,Y),fm(l,Z))),fm(fs(s,t),h)),sq(t)));
 field("joint.scale",fa(fs(X4,fm(d,fs(s,t))),fm(aD,fm(Y,Z))));
 field("joint.scaledInverse",fs(fscl(ks,49),fm(c,Knum)));
 field("joint.combinedReciprocal",fs(fscl(Bs,49),fa(fscl(fm(ks,Y),49),fc(fm(Knum,Z)))));
 rows.push(...old.residuals.slice(17,19));
 field("joint.primaryComparison",fs(fa(Pc,fm(c,Qc)),fscl(sq(C),2)));
 field("joint.alternateComparison",fs(fs(fm(u,Pc),Qc),fscl(sq(fc(I)),2)));
 field("joint.detector",fs(fm(u,Ws),fa(sq(u),fm(Pc,Qc),sq(Bs))));
 rows.push(...old.residuals.slice(25));
 if(rows.length!==42)throw Error("row count");
 return {variables:52,parameter:"B",input:1,residuals:rows}
}
function census(q){
 let terms=new Map();for(let r of q.residuals)for(let t of r.terms)for(let s of r.terms){let m=[...t.monomial,...s.monomial].sort((a,b)=>a-b);let k=(t.parameterPower+s.parameterPower)+"|"+m.join(",");terms.set(k,(terms.get(k)||0n)+BigInt(t.coefficient)*BigInt(s.coefficient))}
 terms=new Map([...terms].filter(([k,v])=>v));let fixture=new Map(),coords=new Set;for(let [k,v]of terms){let m=k.split("|")[1];fixture.set(m,(fixture.get(m)||0n)+v);for(let i of m.split(",").filter(Boolean))coords.add(+i)}
 fixture=new Map([...fixture].filter(([k,v])=>v));let max=0n,degree=0;for(let [k,v] of fixture){max=[max,v<0n?-v:v].reduce((a,b)=>a>b?a:b);degree=Math.max(degree,k?k.split(",").length:0)} 
 const upper=mu=>2+Math.floor(mu/8)+Math.floor(7*mu/16);
 for(let mu=1;mu<=20001;mu+=2){let e=upper(mu),d1=1+Math.floor(7*mu/16),d2=1+Math.floor(3*mu/16);if(Math.min(4*d1,4*d2,2+Math.floor(5*mu/8)+Math.floor(3*mu/16))<e)throw Error("depth "+mu)}
 return {variables:coords.size,rows:q.residuals.length,parameterSeparatedTerms:terms.size,coordinateMonomials:new Set([...terms.keys()].map(k=>k.split("|")[1])).size,fixtureMonomials:fixture.size,fixtureHeight:max.toString(),degree,inputFourth:fixture.get("1,1,1,1").toString(),oddDepthChecks:10001}
}
const path=require('node:path');const here=__dirname;const parent=JSON.parse(fs.readFileSync(path.join(here,'../denominator_radical52_20261125/quadrics.json'),'utf8'));const actual=JSON.parse(fs.readFileSync(path.join(here,'quadrics.json'),'utf8'));assert.deepEqual(actual,build(parent));console.log(census(actual));
