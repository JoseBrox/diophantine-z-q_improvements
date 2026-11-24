"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const build=function build(t){
 const chk=(b,m)=>{if(!b)throw Error(m)};
 const roles=t.ordinary_integer_inputs;
 const prefix=x=>x==="i_half"?"int_i_reciprocal_":"int_"+x+"_";
 const role=x=>x==="i_half"?"i":x;
 const removed=new Set(roles.flatMap(x=>[47,49,51,52,53,54,55].map(k=>prefix(x)+k)));
 const old=t.variable_names, n=old.length;
 chk(n===605&&t.residuals.length===528&&roles.length===12,"predecessor size");
 chk([...removed].every(x=>old.includes(x))&&removed.size===84,"deleted coordinates");
 const rmrow=q=>/^integer\.[^.]+\.contact\./.test(q.name);
 const rows=t.residuals.filter(q=>!rmrow(q));
 chk(rows.length===432,"removed row count");
 chk(rows.every(q=>q.terms.every(a=>a.monomial.every(j=>!removed.has(old[j-1])))),"external occurrence");
 const names=old.filter(x=>!removed.has(x)), added=[];
 const V=x=>new Map([[x,1n]]), C=x=>new Map(BigInt(x)?[["",BigInt(x)]]:[]);
 const plus=(...ps)=>{const out=new Map;for(const p of ps)for(const [k,c]of p)out.set(k,(out.get(k)||0n)+c);for(const [k,c]of out)if(!c)out.delete(k);return out};
 const sc=(p,c)=>new Map([...p].map(([k,v])=>[k,v*BigInt(c)]).filter(([k,v])=>v));
 const mul=(p,q)=>{const out=new Map;for(const [k,c]of p)for(const [l,d]of q){const m=[...k.split("|"),...l.split("|")].filter(Boolean).sort().join("|");out.set(m,(out.get(m)||0n)+c*d)}for(const[k,c]of out)if(!c)out.delete(k);return out};
 const sq=p=>mul(p,p), sub=(p,q)=>plus(p,sc(q,-1));
 const eq=(a,b)=>sub(a,b).size===0;
 const reg=(x)=>{chk(!names.includes(x),"duplicate variable");names.push(x);return V(x)};
 const row=(name,p)=>{chk([...p.keys()].every(k=>k===""||k.split("|").length<=2),"degree");added.push({name,p})};
 const def=(name,p)=>{const v=reg(name);row("aggregate."+name,sub(v,p));return v};
 let layer=roles.map(x=>({m:V(prefix(x)+45),s:V(prefix(x)+46),depth:0}));
 for(const x of roles){chk(old.includes(prefix(x)+45)&&old.includes(prefix(x)+46),"leaf coordinates");const q=t.residuals.find(q=>q.name==="integer."+role(x)+".height.M2");chk(q&&q.terms.length===2,"leaf square row")}
 let count=0;
 while(layer.length>1){const next=[];for(let j=0;j<layer.length;j+=2){if(j+1===layer.length){next.push(layer[j]);continue}
 const l=layer[j],r=layer[j+1],m=def("acg_M"+count,plus(C(1),sc(plus(sq(l.s),sq(r.s)),2))),s=def("acg_M"+count+"_sq",sq(m));next.push({m,s,depth:1+Math.max(l.depth,r.depth)});count++}layer=next}
 chk(count===11&&layer[0].depth===4,"tree depth");
 const a=def("acg_a",plus(sq(layer[0].s),C(432)));
 const z2=V("abc_common_contact_square");
 const T=def("acg_T",sub(sq(a),z2)), S=plus(T,sc(z2,2)),P=def("acg_P",sq(T));
 const PP=def("acg_PP",sq(P)),PS=def("acg_PS",mul(P,S)),SS=def("acg_SS",sq(S)),TP=def("acg_TP",mul(T,P)),TS=def("acg_TS",mul(T,S));
 const A=[PP,sc(PS,-130),plus(sc(P,4097),sc(SS,256)),sc(S,-8320),C(4096)];
 const B=[PP,sc(PS,-130),plus(sc(P,2657),sc(SS,3136)),sc(S,-101920),C(614656)];
 const H=[sc(TP,4),plus(sc(TS,-260),sc(P,-130)),plus(sc(T,8194),sc(S,512)),C(-8320)];
 const ev=(list,v)=>plus(...list.map((p,j)=>sc(p,v**BigInt(j))));
 const F=[];
 for(let j=0;j<=8;j++){const f=reg("acg_F"+j);F.push(f);row("aggregate.product."+j,sub(mul(a,f),plus(...A.map((p,k)=>j-k>=0&&j-k<5?mul(p,B[j-k]):C(0)))))}
 const scales=[11,13,17,19,23,29,31,37,41,43,47,53];
 const radii=new Set;
 const pa=V("P"),sa=V("S"),ta=V("T");
 const der=(p,x)=>{let out=C(0);for(const[k,c]of p){const kk=k.split("|"),j=kk.indexOf(x),d=kk.filter(s=>s===x).length;if(d){kk.splice(j,1);out=plus(out,new Map([[kk.join("|"),c*BigInt(d)]]))}}return out};
 const D=p=>plus(mul(sc(ta,2),der(p,"P")),der(p,"S"));
 const directFactor=(r,v)=>plus(pa,sc(sa,-2n*BigInt(r*r)*v),C(BigInt(r**4)*v*v));
 for(let j=0;j<12;j++){
 const s=scales[j],v=BigInt(s*s),c=V(prefix(roles[j])+43);
 for(const k of [1,4,7,8]){chk(!radii.has(k*s),"contact collision");radii.add(k*s)}
 const aa=ev(A,v),bb=ev(B,v),hh=ev(H,v),dif=sc(plus(sc(T,-4),sc(S,8),C(-130n*v)),720n*v*v);
 row("aggregate.derivative."+role(roles[j]),plus(mul(hh,plus(aa,bb)),mul(dif,aa),sc(mul(c,ev(F,v)),8)));
 // Independent formal check: expand both pairs of linear factors and differentiate.
 const As=mul(directFactor(1,v),directFactor(8,v)),Bs=mul(directFactor(4,v),directFactor(7,v));
 const Aexp=plus(sq(pa),sc(mul(pa,sa),-130n*v),sc(plus(sc(pa,4097),sc(sq(sa),256)),v*v),sc(sa,-8320n*v**3n),C(4096n*v**4n));
 const Bexp=plus(sq(pa),sc(mul(pa,sa),-130n*v),sc(plus(sc(pa,2657),sc(sq(sa),3136)),v*v),sc(sa,-101920n*v**3n),C(614656n*v**4n));
 const Hexp=plus(sc(mul(ta,pa),4),sc(plus(sc(mul(ta,sa),-260),sc(pa,-130)),v),sc(plus(sc(ta,8194),sc(sa,512)),v*v),C(-8320n*v**3n));
 const Dexp=sc(plus(sc(ta,-4),sc(sa,8),C(-130n*v)),720n*v*v);
 chk(eq(As,Aexp)&&eq(Bs,Bexp)&&eq(D(As),Hexp)&&eq(D(Bs),plus(Hexp,Dexp)),"symbolic paired derivatives");
 chk(eq(D(mul(As,Bs)),plus(mul(Hexp,plus(As,Bs)),mul(Dexp,As))),"product derivative");
 }
 chk(radii.size===48&&Math.max(...radii)<432,"disjoint positive shifts");
 chk(100n*1002n*1001n**4n<193n*997n**5n,"height margin");
 const ix=new Map(names.map((x,i)=>[x,i+1]));
 const newRows=rows.map(q=>({name:q.name,terms:q.terms.map(o=>({coefficient:o.coefficient,monomial:o.monomial.map(i=>ix.get(old[i-1])).sort((a,b)=>a-b)}))}));
 for(const {name,p}of added)newRows.push({name,terms:[...p].map(([k,c])=>({coefficient:String(c),monomial:k?k.split("|").map(x=>ix.get(x)).sort((a,b)=>a-b):[]})).sort((a,b)=>{for(let j=0;j<Math.min(a.monomial.length,b.monomial.length);j++){if(a.monomial[j]!==b.monomial[j])return a.monomial[j]-b.monomial[j]}return a.monomial.length-b.monomial.length})});
 const support=new Set(newRows.flatMap(q=>q.terms.flatMap(o=>o.monomial)));
 chk(names.length===560&&newRows.length===483&&added.length===51,"final census");
 chk(support.size===names.length&&newRows.every(q=>q.terms.every(o=>o.monomial.length<=2&&o.monomial.every(i=>i>=1&&i<=names.length))),"support");
 // Check retained rows in named monomial coordinates independently of renumbering.
 for(let j=0;j<rows.length;j++){const key=(q,nn)=>JSON.stringify(q.terms.map(t=>[t.coefficient,t.monomial.map(i=>nn[i-1]).sort()]));chk(key(rows[j],old)===key(newRows[j],names),"retained row");}
 return {status:"conditional transfer under ordinary rational abc and the retained v108 arithmetic premises",predecessor:"../abc_pell_integrality_v108/c_integrality_abc_quadrics.json",predecessor_sha256:"4cacba002f7537c2c3732fadb00f7961dffc9bfc7fc91ef42740a903bc9b1eb7",variables:names.length,variable_names:names,parameters:t.parameters,ordinary_integer_inputs:roles,reciprocal_integer_inputs:[],integer_blocks:12,input_is_fixed_coefficient:t.input_is_fixed_coefficient,instance_range:t.instance_range,degree_of_each_residual_at_most:2,sum_of_squares_degree:4,retained_arithmetic_interfaces:t.retained_arithmetic_interfaces,source_coding_theorem:t.source_coding_theorem,unconditional_undecidability_claim:false,contact_scales:scales,removed_coordinates:[...removed],removed_rows:t.residuals.filter(rmrow).map(q=>q.name),verification:{retained_rows:rows.length,added_rows:added.length,added_coordinates:names.length-(n-removed.size),tree_depth:4,formal_derivative_identities:60,full_support:true,height_margin_verified:true},residuals:newRows};
};
const raw=fs.readFileSync(path.join(__dirname,"../abc_pell_integrality_v108/c_integrality_abc_quadrics.json"));
if(crypto.createHash("sha256").update(raw).digest("hex")!=="4cacba002f7537c2c3732fadb00f7961dffc9bfc7fc91ef42740a903bc9b1eb7")throw Error("predecessor hash");
const out=build(JSON.parse(raw)), dest=path.join(__dirname,"quadrics.json");
if(process.argv.includes("--write"))fs.writeFileSync(dest,JSON.stringify(out)+"\n");
else if(JSON.stringify(JSON.parse(fs.readFileSync(dest)))!==JSON.stringify(out))throw Error("table mismatch");
console.log(out.variables,out.residuals.length,out.verification);
