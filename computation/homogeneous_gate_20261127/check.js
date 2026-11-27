"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),assert=require("node:assert/strict");
function build(parent) {
 const n=parent.variables, abc=n===50, family=n===161;
 const mon=(a,...is)=>new Map([[is.sort((a,b)=>a-b).join(","),BigInt(a)]]);
 const add=(...ps)=>{let out=new Map;for(let p of ps)for(let [k,a]of p){let b=(out.get(k)||0n)+a;if(b)out.set(k,b);else out.delete(k)}return out};
 const scale=(p,n)=>new Map([...p].filter(([k,a])=>a*BigInt(n)).map(([k,a])=>[k,a*BigInt(n)]));
 const mul=(p,q)=>add(...[...p].flatMap(([k,a])=>[...q].map(([l,b])=>mon(a*b,...[k,l].filter(Boolean).flatMap(t=>t.split(",").map(Number))))));
 const x=i=>mon(1,i),one=mon(1),zero=new Map(),F=i=>[x(i),x(i+1)],re=p=>[p,zero],fa=(...ps)=>[add(...ps.map(p=>p[0])),add(...ps.map(p=>p[1]))],sc=(p,n)=>p.map(q=>scale(q,n)),fs=(p,q)=>fa(p,sc(q,-1)),fm=(a,b)=>[add(mul(a[0],b[0]),scale(mul(a[1],b[1]),2)),add(mul(a[0],b[1]),mul(a[1],b[0]))],conj=p=>[p[0],scale(p[1],-1)],prod=(...ps)=>ps.reduce(fm);
 const order=(a,b)=>{for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length};
 const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
 const rows=[];
 const emit=(name,p)=>{let g=[...p.values()].reduce(gcd,0n);const terms=[...p].filter(([k,a])=>a).map(([k,a])=>({parameterPower:0,monomial:k?k.split(",").map(Number):[],coefficient:(a/g).toString()}));terms.sort((a,b)=>order(a.monomial,b.monomial));rows.push({name,terms})};
 const field=(name,p)=>p.forEach((q,i)=>emit(name+"."+i,q));
 if(abc){
  const drop=new Set(["joint.primaryReciprocal.0","joint.primaryReciprocal.1","joint.linearReciprocalDetector.0","joint.linearReciprocalDetector.1","sharedD","single.reciprocalGate","single.reciprocalPoleInput"]);
  for(const row of parent.residuals){if(drop.has(row.name))continue;for(const t of row.terms)if(t.monomial.some(i=>i===21||i===22))throw Error("deleted var");rows.push({name:row.name,terms:row.terms.map(t=>({...t,monomial:t.monomial.map(i=>i>22?i-2:i)}))})}
  const A=F(6),T=F(4),Y=F(13),Z=F(15),P=F(21),Q=F(23),W=F(27),r=re(x(29)),K=re(x(30)),D=re(x(38)),c=re(x(39)),u=re(x(40)),u2=fm(u,u);
  const Er=fa(sc(A,-1),sc(T,-1),[mon(-4),mon(2)]),Delta=[mon(11),mon(-6)];
  field("homogeneous.detector",fs(sc(fs(fm(u2,W),fm(r,fa(u2,prod(c,P,Q)))),49),fm(r,fa(prod(u,conj(Delta),Er,Y),prod(c,Delta,conj(fm(Er,Z)))))));
  emit("homogeneous.norm",add(mul(x(27),x(27)),scale(mul(x(28),x(28)),-2),scale(mul(x(29),x(27)),-2),mul(x(29),x(29)),scale(mul(x(38),x(27)),-2)));
  emit("homogeneous.poleInput",fs(fm(u,fa(K,sc(u,-1),sc(r,-2))),fm(r,r))[0]);
  emit("homogeneous.normalizer",fa(fm(D,D),K,sc(u,-1),sc(r,-2),sc(fm(c,r),-1))[0]);
  return {variables:48,parameter:"B",input:1,residuals:rows};
 }
 if(!family&&n!==175)throw Error("parent count");
 const u=family?158:160,v=u+1,mid=family?160:174,W=family?152:153;
 const L=fa(re(x(v)),conj(F(133)),[x(19),scale(x(20),-2)]);
 const phi=fa(re(x(v)),fm(re(x(v)),F(143)),fm(F(119),F(119)));
 const dropped=parent.residuals.filter(t=>/^(shared\.partial_pair\.|new\.det0\.factor3\.|amplified\.det0\.product3\.)/.test(t.name));
 if(dropped.length!==6)throw Error("stage rows");
 for(const row of parent.residuals){if(dropped.includes(row))continue;if(row.terms.some(t=>t.monomial.some(i=>[mid,mid+1,95,96].includes(i))))throw Error("private occurrence");rows.push(row)}
 field("mixed.factor",fs(fm(re(family?x(u):one),F(95)),phi));
 field("mixed.product4a",fs(fm(re(family?x(u):one),F(mid)),fm(F(99),F(95))));
 field("mixed.product4b",fs(fm(re(family?x(v):x(u)),F(W)),fm(F(mid),L)));
 if(rows.some(row=>row.terms.some(t=>t.monomial.length>2)))throw Error("degree");
 return {...parent,residuals:rows};
}
function stats(q,N) {
 let sym=new Map(),p=new Map();
 for(const r of q.residuals)for(const t of r.terms)for(const s of r.terms){const m=t.monomial.concat(s.monomial).sort((a,b)=>a-b),k=(t.parameterPower+s.parameterPower)+"|"+m.join(",");sym.set(k,(sym.get(k)||0n)+BigInt(t.coefficient)*BigInt(s.coefficient))}
 sym=new Map([...sym].filter(([k,v])=>v));
 const C=q.variables===48?1n:331n**BigInt(N);for(const [k,v]of sym){const [e,m]=k.split("|");p.set(m,(p.get(m)||0n)+v*C**BigInt(e))}
 p=new Map([...p].filter(([k,v])=>v));let max=0n,degree=0,vars=new Set(),s="";
 const sorted=[...p].map(([k,v])=>[k?k.split(",").map(Number):[],v]).sort(([a],[b])=>{for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length});
 for(const [m,v]of sorted){const abs=v<0n?-v:v;if(abs>max)max=abs;degree=Math.max(degree,m.length);m.forEach(i=>vars.add(i));let parts=[];for(let i=0;i<m.length;){let j=i+1;while(j<m.length&&m[j]===m[i])j++;parts.push("x"+m[i]+(j-i>1?"^"+(j-i):""));i=j}const coef=abs===1n&&parts.length?"":abs.toString();s+=(v<0n?"-":s?"+":"")+coef+(coef&&parts.length?"*":"")+parts.join("*")}
 if(vars.size!==q.variables||p.get("1,1,1,1")!==1n||degree!==(q.variables===48?8:4))throw Error("census");
 return {literal:s,statistics:{variables:q.variables,rows:q.residuals.length,quadratic_rows:q.residuals.filter(r=>r.terms.every(t=>t.monomial.length<=2)).length,degree,content:1,symbolic_terms:sym.size,monomials:p.size,height:max.toString(),height_bits:max.toString(2).length,bytes:s.length,parameter:q.variables===48?"B=1":"N="+N}};
}
const cases=[{"source":"computation/linear_reciprocal50_20261127/quadrics.json","parent_blob":"db36624fe070015ccda873f2602f08508a3ba351","table":"system48.json","expansion":"expanded48-B1.txt","census":{"variables":48,"rows":38,"quadratic_rows":36,"degree":8,"content":1,"symbolic_terms":1137,"monomials":1133,"height":"5531402752","height_bits":33,"bytes":21592,"parameter":"B=1"}},{"source":"computation/projective_contacts_20261126/quartic161.json","parent_blob":"5b081b081082022282681bb4b3ceeeee00a92898","table":"system161.json","expansion":"expanded161-N21.txt","census":{"variables":161,"rows":135,"quadratic_rows":135,"degree":4,"content":1,"symbolic_terms":2819,"monomials":2813,"height":"22666702618137718096290059557074087834954306818699071227692301260102451961485531472453904409770491528137229463682457888956698376800126860959280482821926070222028985439076816412060761395146574123162323880370059551886093579006449010343936000001","height_bits":802,"bytes":64683,"parameter":"N=21"}},{"source":"computation/projective_contacts_20261126/quadrics.json","parent_blob":"dbb2dfb22b92d1bef2c179a6142f4dae3d9d6d25","table":"system175.json","expansion":"expanded175-N21.txt","census":{"variables":175,"rows":147,"quadratic_rows":147,"degree":4,"content":1,"symbolic_terms":3168,"monomials":3162,"height":"22666702618137718096290059557074087834954306818699071227692301260102451961485531472453904409770491528137229463682457888956698376800126860959280482821926070222028985439076816412060761395146574123162323880370059551886093579006449010343936000001","height_bits":802,"bytes":72390,"parameter":"N=21"}}];
for(const item of cases){const raw=fs.readFileSync(path.resolve(__dirname,'../..',item.source));assert.equal(crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex'),item.parent_blob);const q=build(JSON.parse(raw));assert.deepEqual(q,JSON.parse(fs.readFileSync(path.join(__dirname,item.table),'utf8')));const r=stats(q,21);assert.deepEqual(r.statistics,item.census);assert.equal(r.literal,fs.readFileSync(path.join(__dirname,item.expansion),'ascii'));console.log(r.statistics)}
