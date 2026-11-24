import fs from "node:fs";import crypto from "node:crypto";import assert from "node:assert/strict";
function reduce(t){
 const names=t.variable_names.slice();
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let q=a%b;a=b;b=q}return a};
 const sort=a=>a.sort();
 const key=(vs,ps)=>sort(vs).join("|")+";"+sort(ps).join("|");
 const unpack=k=>k.split(";").map(s=>s?s.split("|"):[]);
 const add=(m,k,c)=>{let z=(m.get(k)||0n)+c;if(z)m.set(k,z);else m.delete(k)};
 function parse(c){
  let s=c.replace(/\s+/g,"").replace(/-/g,"+-").replace(/^\+/,""),out=[];
  for(let q of s.split("+")){
   if(!q)continue;let sign=q[0]==="-"?-1n:1n;if(sign<0n)q=q.slice(1);
   const factors=q.replace(/\*\*(\d+)/g,"^$1").split("*");let a=sign,p=[];
   for(let f of factors){if(/^\d+$/.test(f))a*=BigInt(f);else{let [v,n="1"]=f.split("^");if(!t.parameters.includes(v)||!/^\d+$/.test(n))throw Error("bad coeff "+c);p.push(...Array(+n).fill(v))}}
   out.push([p,a])
  }return out;
 }
 let rows=t.residuals.map(q=>{let m=new Map;for(let a of q.terms)for(let [ps,c]of parse(a.coefficient))add(m,key(a.monomial.map(i=>names[i-1]),ps),c);return{name:q.name,m}});
 const degree=k=>unpack(k)[0].length;
 const primitive=m=>{let d=0n;for(let c of m.values()){d=gcd(d,c);if(d===1n)break}if(d>1n)for(let [k,c] of m)m.set(k,c/d);return m};
 const mul=(a,b)=>{let o=new Map;for(let [k,c] of a)for(let [l,d] of b){let [v,p]=unpack(k),[w,q]=unpack(l);add(o,key(v.concat(w),p.concat(q)),c*d)}return o};
 const serialized=m=>[...m].map(([k,c])=>[k,c.toString()]);
 const log=[];
 function eliminate(n,i){
   let row=rows[i],a=row.m.get(n+";");if(!a)throw Error("pivot");
   let P=new Map([...row.m].filter(([k])=>k!==n+";").map(([k,c])=>[k,-c]));
   if([...P.keys()].some(k=>unpack(k)[0].includes(n)))throw Error("self");
   if(a<0n){a=-a;for(let [k,c]of P)P.set(k,-c)}
   let powers=[new Map([[";",1n]]),P,mul(P,P)];
   const changed=[];
   for(let j=0;j<rows.length;j++){
    if(j===i)continue;let R=rows[j],max=0;for(let k of R.m.keys()){let vs=unpack(k)[0];max=Math.max(max,vs.filter(v=>v===n).length)}
    if(!max)continue;let out=new Map;
    for(let [k,c]of R.m){let [v,p]=unpack(k),cnt=v.filter(w=>w===n).length;v=v.filter(w=>w!==n);
     for(let [l,d]of powers[cnt]){let [w,q]=unpack(l);add(out,key(v.concat(w),p.concat(q)),c*d*a**BigInt(max-cnt))}
    }
    if([...out.keys()].some(k=>degree(k)>2))throw Error("degree overflow");
    R.m=primitive(out);changed.push(R.name)
   }
   log.push({type:"solve",variable:n,row:row.name,denominator:String(a),numerator:serialized(P),changed});
   rows.splice(i,1);names.splice(names.indexOf(n),1);
 }
 function choose(){
  let maxOcc=new Map,nOcc=new Map;
  for(let R of rows)for(let k of R.m.keys()){let [vs]=unpack(k);for(let n of vs){maxOcc.set(n,Math.max(maxOcc.get(n)||0,vs.length));nOcc.set(n,(nOcc.get(n)||0)+1)}}
  let best=null;
  for(let i=0;i<rows.length;i++){let m=rows[i].m, deg=Math.max(0,...[...m.keys()].map(degree));
   for(let [k,c] of m){let [vs,ps]=unpack(k);if(vs.length!==1||ps.length)continue;let n=vs[0];
    if(deg===2&&maxOcc.get(n)>1)continue;
    if([...m.keys()].some(l=>l!==k&&unpack(l)[0].includes(n)))continue;
    let cost=(m.size-1)*(nOcc.get(n)-1);
    if(!best||cost<best.cost||(cost===best.cost&&n<best.n))best={i,n,cost};
   }
  }return best
 }
 // Any row with an exclusive quadratic monomial has zero coefficient
 // in every affine row-space relation. Repeated pruning makes the
 // subsequent exact elimination small.
 function linearConsequence(){
  let active=new Set(rows.map((_,i)=>i)),support=rows.map(q=>[...q.m.keys()].filter(k=>degree(k)===2));
  for(let i=0;i<rows.length;i++)if(!support[i].length)active.delete(i);
  while(true){let count=new Map;for(let i of active)for(let k of support[i])count.set(k,(count.get(k)||0)+1);
   let del=[...active].filter(i=>support[i].some(k=>count.get(k)===1));if(!del.length)break;for(let i of del)active.delete(i)
  }
  const pivots=new Map;
  for(let i of [...active].sort((a,b)=>support[a].length-support[b].length||a-b)){
   let m=new Map(rows[i].m), combo=new Map([[i,1n]]);
   function clean(){let g=0n;for(let c of combo.values())g=gcd(g,c);if(g>1n){for(let [k,c]of combo)combo.set(k,c/g);for(let [k,c]of m){if(c%g)throw Error("gcd");m.set(k,c/g)}}}
   for(let iter=0;iter<rows.length+1;iter++){
    let qs=[...m.keys()].filter(k=>degree(k)===2).sort();
    if(!qs.length){
     if(m.size&&[...m.keys()].some(k=>{let[v,p]=unpack(k);return v.length===1&&!p.length&&[...m.keys()].filter(l=>unpack(l)[0].includes(v[0])).length===1})){
       let orig=rows[i].name;log.push({type:"rowCombination",replaced:orig,combination:[...combo].map(([j,c])=>[rows[j].name,String(c)])});if(!combo.get(i))throw Error("noninvertible");rows[i].m=primitive(m);return true;
     }break;
    }
    let q=qs[0];if(!pivots.has(q)){pivots.set(q,{m,combo});break}
    let other=pivots.get(q),a=m.get(q),b=other.m.get(q),d=gcd(a,b);a/=d;b/=d;
    for(let [k,c]of m)m.set(k,c*b);for(let [k,c]of other.m)add(m,k,-a*c);
    for(let [k,c]of combo)combo.set(k,c*b);for(let [k,c]of other.combo){let z=(combo.get(k)||0n)-a*c;if(z)combo.set(k,z);else combo.delete(k)}
    clean();if(m.size>20000||[...combo.values()].some(c=>String(c).length>5000))break;
   }
  }
  return false
 }
 for(let i=0;i<1000;i++){let b=choose();if(b){eliminate(b.n,b.i);continue}if(!linearConsequence())break;}
 const ids=new Map(names.map((n,i)=>[n,i+1]));
 function coeffStr(m){let s="";for(let [p,c] of m){if(!c)continue;let a=c<0n?-c:c;let term=p?(a===1n?"":a.toString()+"*")+p.split("|").join("*"):String(a);s+=(s?(c<0n?" - ":" + "):(c<0n?"-":""))+term}return s}
 const residuals=rows.map(R=>{
   let by=new Map;for(let [k,c]of R.m){let [v,p]=unpack(k),m=v.map(n=>ids.get(n)).sort((a,b)=>a-b).join(",");if(!by.has(m))by.set(m,new Map);add(by.get(m),p.join("|"),c)}
   return {name:R.name,terms:[...by].filter(([m,cs])=>cs.size).map(([m,cs])=>({coefficient:coeffStr(cs),monomial:m?m.split(",").map(Number):[]}))}
 }).filter(q=>q.terms.length);
 const supp=new Set(residuals.flatMap(q=>q.terms.flatMap(a=>a.monomial)));
 if(supp.size!==names.length||residuals.some(q=>q.terms.some(a=>a.monomial.length>2)))throw Error("support/degree");
 const out={...t,variables:names.length,variable_names:names,residuals,verification:{exact_eliminations:log,previous_verification:t.verification||null,full_support:true}};
 if("quadratic_rows" in out)out.quadratic_rows=residuals.length;
 return out;
}
const specs=[
  {
    "label": "general",
    "p": "undecidability/positivity_theta_reduction_20261124/general_quadrics.json",
    "sha": "701e02a4de8a66143be55233f91d958f235af493",
    "n0": 884,
    "m0": 749,
    "n": 884,
    "m": 749
  },
  {
    "label": "specified",
    "p": "undecidability/positivity_theta_reduction_20261124/specified_quadrics.json",
    "sha": "e58e736a99765611a3298b07ae77b6c2b3a12ddd",
    "n0": 1049,
    "m0": 912,
    "n": 1049,
    "m": 912
  },
  {
    "label": "abc",
    "p": "undecidability/abc_mean_shifted_curve_v120/quadrics.json",
    "sha": "b566b6ffca43c3be8372f7f8a130c94b91bbd7ea",
    "n0": 324,
    "m0": 273,
    "n": 323,
    "m": 272
  }
];
for(const s of specs){const raw=fs.readFileSync(new URL("../.."+"/"+s.p,import.meta.url));const blob=crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex");assert.equal(blob,s.sha);const out=reduce(JSON.parse(raw));assert.equal(out.variables,s.n);assert.equal(out.residuals.length,s.m);const dest=new URL(s.label+"_quadrics.json",import.meta.url);if(process.argv.includes("--write"))fs.writeFileSync(dest,JSON.stringify(out)+"\n");else assert.deepEqual(JSON.parse(fs.readFileSync(dest)),out);console.log(s.label,s.n0,s.n,s.m)}
