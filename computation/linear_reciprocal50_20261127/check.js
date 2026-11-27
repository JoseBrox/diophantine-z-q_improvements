"use strict";
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
function build(old){
 const m=(a=1,...xs)=>new Map([[xs.sort((a,b)=>a-b).join(","),BigInt(a)]]);
 const add=(...pp)=>{let r=new Map;for(let p of pp)for(let [k,v]of p)r.set(k,(r.get(k)||0n)+v);return new Map([...r].filter(([k,v])=>v))};
 const scale=(p,a)=>new Map([...p].map(([k,v])=>[k,v*BigInt(a)]).filter(([k,v])=>v));
 const sub=(p,q)=>add(p,scale(q,-1));
 const mul=(p,q)=>add(...[...p].flatMap(([a,v])=>[...q].map(([b,w])=>m(v*w,...[a,b].filter(Boolean).flatMap(k=>k.split(",").map(Number))))));
 const x=i=>m(1,i),zero=new Map(),f=i=>[x(i),x(i+1)],constf=(a,b=0)=>[m(a),m(b)],fp=p=>[p,zero],fa=(...a)=>[add(...a.map(q=>q[0])),add(...a.map(q=>q[1]))],fs=(a,b)=>fa(a,[scale(b[0],-1),scale(b[1],-1)]),fc=a=>[a[0],scale(a[1],-1)],fm=(a,b)=>[add(mul(a[0],b[0]),scale(mul(a[1],b[1]),2)),add(mul(a[0],b[1]),mul(a[1],b[0]))],fscl=(a,n)=>a.map(p=>scale(p,n)),sq=a=>fm(a,a);
 const S=f(2),T=f(4),A=f(6),s=f(9),t=f(11),Y=f(13),Z=f(15),h=f(17),d=f(19),L=f(21),P=f(23),Q=f(25),Ws=f(29),c=fp(x(41)),u=fp(x(42)),X4=fp(x(28));
 const a=constf(1,1),b=constf(4,-2),delta=constf(-23,17),Delta=constf(11,-6),Br=fa(A,S,T),E=fs(constf(0),fa(A,T,b)),v=fa(S,A,b);
 const C=fs(s,S),I=fs(t,T),p=fa(h,s,t);
 let rows=[];
 function cmp(a,b){for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length}
 const order=(a,b)=>a.parameterPower-b.parameterPower||cmp(a.monomial,b.monomial);
 function row(name,q){let terms=[...q].map(([k,v])=>({parameterPower:0,monomial:k?k.split(",").map(Number):[],coefficient:v.toString()})).filter(t=>t.coefficient!=="0");terms.sort(order);let g=0n;const gcd=(a,b)=>b?gcd(b,a%b):a;for(let t of terms){let z=BigInt(t.coefficient);g=gcd(g,z<0n?-z:z)} if(g===0n)throw Error(name);for(let t of terms){t.coefficient=(BigInt(t.coefficient)/g).toString();if(t.monomial.length>2)throw Error("degree "+name)}rows.push({name,terms})}
 function field(name,z){row(name+".0",z[0]);row(name+".1",z[1])}
 function inherit(r){rows.push({...r,terms:r.terms.map(t=>({...t,monomial:t.monomial.map(i=>{if(i===21||i===22)throw Error("deleted coordinate");return i>22?i-2:i})})).sort(order)})}
 field("reference.product",fs(fm(A,Br),a));
 field("reference.inverse",fs(fm(E,v),delta));
 row("pair.differenceReal",sub(x(8),fm(h,p)[0]));
 field("joint.firstProduct",fs(fm(A,d),fm(p,Y)));
 field("joint.secondProduct",fs(fm(Br,d),fm(h,Z)));
 field("joint.secant",fs(fscl(fa(fm(Br,Y),fm(A,Z)),49),fm(constf(23,17),fs(fm(fs(s,t),h),sq(t)))));
 field("joint.scale",fa(fs(X4,fm(d,fs(s,t))),fm(delta,fm(Y,Z))));
 field("joint.primaryReciprocal",fs(fm(Delta,fm(u,L)),fm(E,Y)));
 old.residuals.slice(17,19).forEach(inherit);
 field("joint.primaryComparison",fs(fa(P,fm(c,Q)),fscl(sq(C),2)));
 field("joint.alternateComparison",fs(fs(fm(u,P),Q),fscl(sq(fc(I)),2)));
 field("joint.linearReciprocalDetector",fs(fscl(fs(fm(u,Ws),fa(sq(u),fm(P,Q),sq(L))),49),fm(Delta,fc(fm(E,Z)))));
 old.residuals.slice(25).forEach(inherit);
 if(rows.length!==40)throw Error("row count "+rows.length);
 return {variables:50,parameter:"B",input:1,residuals:rows}
}
function expand(q){
 let terms=new Map;const put=(r,k,a)=>r.set(k,(r.get(k)||0n)+a);
 for(let r of q.residuals)for(let t of r.terms)for(let s of r.terms){let m=[...t.monomial,...s.monomial].sort((a,b)=>a-b);put(terms,(t.parameterPower+s.parameterPower)+"|"+m.join(","),BigInt(t.coefficient)*BigInt(s.coefficient))}
 terms=new Map([...terms].filter(([k,v])=>v));
 const polys=[...terms].map(([k,v])=>{const [p,m]=k.split("|");return {parameterPower:+p,monomial:m?m.split(",").map(Number):[],coefficient:v.toString()}}).sort((a,b)=>a.parameterPower-b.parameterPower||cmp(a.monomial,b.monomial));
 function cmp(a,b){for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length}
 let fixture=new Map,coords=new Set;for(let [k,v]of terms){let m=k.split("|")[1];put(fixture,m,v);for(let i of m.split(",").filter(Boolean))coords.add(+i)}
 fixture=new Map([...fixture].filter(([k,v])=>v));
 let max=0n,degree=0,parts=[];for(let [m,v] of [...fixture].sort(([m],[n])=>cmp(m?m.split(",").map(Number):[],n?n.split(",").map(Number):[]))){const mag=v<0n?-v:v,ids=m?m.split(",").map(Number):[];if(mag>max)max=mag;degree=Math.max(degree,ids.length);let f=[];for(let i=0;i<ids.length;){let j=i+1;while(j<ids.length&&ids[j]===ids[i])j++;f.push("x"+ids[i]+(j-i>1?"^"+(j-i):""));i=j}const a=mag===1n&&f.length?"":mag.toString();parts.push((v<0n?"-":parts.length?"+":"")+a+(a&&f.length?"*":"")+f.join("*"))}
 const literal=parts.join("");
 return {polynomial:{variables:q.variables,input:1,parameter:"B",terms:polys},literal,stats:{variables:coords.size,rows:q.residuals.length,parameterSeparatedTerms:terms.size,coordinateMonomials:new Set([...terms.keys()].map(k=>k.split("|")[1])).size,fixtureMonomials:fixture.size,fixtureHeight:max.toString(),degree,inputFourth:fixture.get("1,1,1,1").toString(),fixtureBytes:literal.length}}
}
const here=__dirname;
const raw=fs.readFileSync(path.join(here,'../denominator_radical52_20261125/quadrics.json'));
assert.equal(crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex'),'8c9ba17ddfa6f4e2900c9d65c30ea24a1d71c026');
const q=JSON.parse(fs.readFileSync(path.join(here,'quadrics.json'),'utf8'));assert.deepEqual(q,build(JSON.parse(raw)));
const e=expand(q);assert.deepEqual(e.polynomial,JSON.parse(fs.readFileSync(path.join(here,'polynomial.json'),'utf8')));assert.equal(e.literal,fs.readFileSync(path.join(here,'expanded-B1.txt'),'ascii'));assert.deepEqual(e.stats,JSON.parse(fs.readFileSync(path.join(here,'census.json'),'utf8')));console.log(e.stats);
