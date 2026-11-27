"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),assert=require("node:assert/strict");
function reconstruct(parent){
 const n=parent.variables, family=n===161;
 if(!family&&n!==175)throw Error("wrong parent");
 const u=family?158:160, v=family?159:161, mid=family?160:174, W=family?152:153;
 const M=(a,...is)=>new Map([[is.sort((a,b)=>a-b).join(","),BigInt(a)]]);
 function add(...ps){let out=new Map;for(let p of ps)for(let [k,a]of p){let b=(out.get(k)||0n)+a;if(b)out.set(k,b);else out.delete(k)}return out}
 function mul(p,q){return add(...[...p].flatMap(([k,a])=>[...q].map(([l,b])=>M(a*b,...[k,l].filter(Boolean).flatMap(t=>t.split(",").map(Number))))))}
 const neg=p=>new Map([...p].map(([k,a])=>[k,-a])),scale=(p,n)=>new Map([...p].map(([k,a])=>[k,a*BigInt(n)])),x=i=>M(1,i),one=M(1),zero=new Map(),F=i=>[x(i),x(i+1)],fa=(a,b)=>[add(a[0],b[0]),add(a[1],b[1])],fm=(a,b)=>[add(mul(a[0],b[0]),scale(mul(a[1],b[1]),2)),add(mul(a[0],b[1]),mul(a[1],b[0]))],fc=a=>[a[0],neg(a[1])],real=p=>[p,zero],fs=(a,b)=>fa(a,b.map(neg)),fscl=(a,k)=>a.map(p=>scale(p,k));
 const a=fa(real(x(u)),F(119)),b=fa(real(one),F(143)),d=fa(real(x(v)),fa(fc(F(133)),fc([x(19),scale(x(20),2)])));
 // Previous physical product = c^2*x99 in the family and u^2*x99 in the fixed route.
 // In the family W_s=u^2 W, fixed W_s=u W. For the family
 // each output is multiplied by u, for the fixed member no output multiplier.
 const unit=family?x(u):one, e=[];
 const emit=(name,p)=>{for(let j=0;j<2;j++){const terms=[...p[j]].map(([k,a])=>({parameterPower:0,monomial:k?k.split(",").map(Number):[],coefficient:a.toString()}));terms.sort((a,b)=>{for(let i=0;i<Math.min(a.monomial.length,b.monomial.length);i++)if(a.monomial[i]!==b.monomial[i])return a.monomial[i]-b.monomial[i];return a.monomial.length-b.monomial.length});if(terms.some(t=>t.monomial.length>2))throw Error("degree");e.push({name:name+"."+j,terms})}}
 const factorRows=(out,lhs,rhs)=>fs(fm(real(unit),F(out)),fm(lhs,rhs));
 emit("affine.product4a",factorRows(mid,F(99),a));
 emit("affine.product4b",factorRows(95,F(mid),b));
 emit("affine.product4c",factorRows(W,F(95),d));
 const drop=parent.residuals.filter(t=>/^(shared\.partial_pair\.|new\.det0\.factor3\.|amplified\.det0\.product3\.)/.test(t.name));
 if(drop.length!==6)throw Error("parent rows");
 const privateSet=new Set([mid,mid+1,95,96]);
 if(parent.residuals.some(t=>!drop.includes(t)&&t.terms.some(s=>s.monomial.some(i=>privateSet.has(i)))))throw Error("private register occurrence");
 const rows=parent.residuals.filter(t=>!drop.includes(t)).concat(e);
 if(rows.length!==parent.residuals.length)throw Error("row count");
 return {...parent,residuals:rows}
}
function stats(q,N){
 let a=new Map(),p=new Map;
 for(let r of q.residuals)for(let t of r.terms)for(let s of r.terms){let m=t.monomial.concat(s.monomial).sort((a,b)=>a-b),k=(t.parameterPower+s.parameterPower)+"|"+m.join(",");a.set(k,(a.get(k)||0n)+BigInt(t.coefficient)*BigInt(s.coefficient))}
 a=new Map([...a].filter(([k,v])=>v));
 const C=331n**BigInt(N);for(let [k,v]of a){let [e,m]=k.split("|");p.set(m,(p.get(m)||0n)+v*C**BigInt(e))}
 p=new Map([...p].filter(([k,v])=>v));let max=0n,degree=0,vars=new Set(),s="";
 const sorted=[...p].map(([k,v])=>[k?k.split(",").map(Number):[],v]).sort(([a],[b])=>{for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length});
 for(let [m,v]of sorted){let abs=v<0n?-v:v;if(abs>max)max=abs;degree=Math.max(degree,m.length);m.forEach(i=>vars.add(i));let parts=[];for(let i=0;i<m.length;){let j=i+1;while(j<m.length&&m[i]===m[j])j++;parts.push("x"+m[i]+(j-i>1?"^"+(j-i):""));i=j}let coef=abs===1n&&parts.length?"":abs.toString();s+=(v<0n?"-":s?"+":"")+coef+(coef&&parts.length?"*":"")+parts.join("*")}
 if(vars.size!==q.variables||p.get("1,1,1,1")!==1n||degree!==4)throw Error("census");
 return {literal:s,statistics:{variables:q.variables,rows:q.residuals.length,symbolic_terms:a.size,monomials:p.size,degree,content:1,height_bits:max.toString(2).length,bytes:s.length,N}}
}
const cases=[{"source":"computation/projective_contacts_20261126/quartic161.json","parent_blob":"5b081b081082022282681bb4b3ceeeee00a92898","old":{"variables":161,"rows":135,"symbolic_terms":2852,"monomials":2846,"degree":4,"content":1,"height_bits":802,"bytes":65282,"N":21},"new":{"variables":161,"rows":135,"symbolic_terms":2827,"monomials":2821,"degree":4,"content":1,"height_bits":802,"bytes":64787,"N":21}},{"source":"computation/projective_contacts_20261126/quadrics.json","parent_blob":"dbb2dfb22b92d1bef2c179a6142f4dae3d9d6d25","old":{"variables":175,"rows":147,"symbolic_terms":3202,"monomials":3196,"degree":4,"content":1,"height_bits":802,"bytes":73080,"N":21},"new":{"variables":175,"rows":147,"symbolic_terms":3173,"monomials":3167,"degree":4,"content":1,"height_bits":802,"bytes":72396,"N":21}}];
for (const r of cases) {const raw=fs.readFileSync(path.resolve(__dirname,"../..",r.source));assert.equal(crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex"),r.parent_blob);const parent=JSON.parse(raw);const q=reconstruct(parent);const n=q.variables;assert.deepEqual(q,JSON.parse(fs.readFileSync(path.join(__dirname,"quartic"+n+".json"),"utf8")));const e=stats(q,21);assert.deepEqual(e.statistics,r.new);if(n===175)assert.equal(e.literal,fs.readFileSync(path.join(__dirname,"expanded175.txt"),"ascii"));console.log(e.statistics)}


function separated(q){
 let a=new Map();for(const r of q.residuals)for(const t of r.terms)for(const s of r.terms){
 let k=(t.parameterPower+s.parameterPower)+"|"+t.monomial.concat(s.monomial).sort((x,y)=>x-y).join(",");
 a.set(k,(a.get(k)||0n)+BigInt(t.coefficient)*BigInt(s.coefficient));
 }return new Map([...a].filter(([k,v])=>v));
}
const parent161=JSON.parse(fs.readFileSync(path.resolve(__dirname,"../..",cases[0].source)));
const new161=JSON.parse(fs.readFileSync(path.join(__dirname,"quartic161.json")));
const pa=separated(parent161),pb=separated(new161);
const moving=new Set([...pa.keys(),...pb.keys()].filter(k=>!k.startsWith("0|")).map(k=>k.split("|")[1]));
const changes=[...new Set([...pa.keys(),...pb.keys()])].filter(k=>(pa.get(k)||0n)!==(pb.get(k)||0n));
assert.equal(moving.size,17);assert.equal(changes.length,158);
assert(changes.every(k=>k.startsWith("0|")&&!moving.has(k.split("|")[1])));
assert.equal(stats(new161,289).statistics.bytes,99902);
assert.equal(stats(new161,290).statistics.bytes,100032);
console.log("Constant-only profile changes: 158; 17 varying profiles unchanged; strict size boundary 289/290.");
