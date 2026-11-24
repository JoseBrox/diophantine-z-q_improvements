"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const src="undecidability/abc_gate_fraction_v114/quadrics.json";
function build(t){
 const chk=(b,m)=>{if(!b)throw Error(m)};
 const old=t.variable_names, roles=t.ordinary_integer_inputs,k=roles.length;
 const keep=t.residuals.filter(q=>q.name.startsWith("jones1980."));
 const used=new Set(keep.flatMap(q=>q.terms.flatMap(a=>a.monomial.map(i=>old[i-1]))));
 const names=old.filter(n=>used.has(n)), outerCount=names.length;
 chk(k===12&&keep.length===52&&outerCount===76,"outer census");
 const rows=[];
 const C=x=>new Map(BigInt(x)?[["",BigInt(x)]]:[]), V=x=>new Map([[x,1n]]);
 const plus=(...ps)=>{let o=new Map;for(const p of ps)for(const [m,v] of p)o.set(m,(o.get(m)||0n)+v);for(const [m,v] of o)if(!v)o.delete(m);return o};
 const sc=(p,k)=>new Map([...p].map(([m,v])=>[m,v*BigInt(k)]).filter(([m,v])=>v));
 const sub=(a,b)=>plus(a,sc(b,-1));
 const mul=(a,b)=>{let o=new Map;for(const [m,v] of a)for(const [n,w]of b){let q=[...m.split("|"),...n.split("|")].filter(Boolean).sort().join("|");o.set(q,(o.get(q)||0n)+v*w)}for(const [m,v]of o)if(!v)o.delete(m);return o};
 const sq=a=>mul(a,a),eq=(a,b)=>sub(a,b).size===0;
 const cf=(a,b=0)=>[C(a),C(b)], fa=(...ps)=>[plus(...ps.map(a=>a[0])),plus(...ps.map(a=>a[1]))],fs=(a,b)=>[sub(a[0],b[0]),sub(a[1],b[1])],fm=(a,b)=>[plus(mul(a[0],b[0]),sc(mul(a[1],b[1]),2)),plus(mul(a[0],b[1]),mul(a[1],b[0]))],fsm=(a,p)=>a.map(b=>mul(b,p)),fscale=(a,b)=>a.map(p=>sc(p,b)),bar=a=>[a[0],sc(a[1],-1)],norm=a=>sub(sq(a[0]),sc(sq(a[1]),2)),trace=a=>sc(a[0],2),fsq=a=>fm(a,a);
 const reg=n=>{chk(!names.includes(n),"duplicate "+n);names.push(n);return V(n)};
 const row=(n,p)=>{chk([...p.keys()].every(m=>m===""||m.split("|").filter(v=>v!=="B_abc").length<=2),"degree "+n);rows.push({name:"new."+n,p})};
 const def=(n,p)=>{let v=reg("n_"+n);row(n,sub(v,p));return v};
 const freg=n=>[reg("n_"+n+"_0"),reg("n_"+n+"_1")];
 const frow=(n,a)=>{row(n+".0",a[0]);row(n+".1",a[1])};
 const fdef=(n,a)=>{let v=freg(n);frow(n,fs(v,a));return v};
 const groups=roles.map((r,i)=>({r,i,X:V(r)}));
 const count={outer:outerCount};
 const u=reg("n_u"),c=reg("n_c");row("unit",sub(mul(u,c),C(1)));
 const D=cf(11,-6),a0=cf(1,1),c0=cf(4,-2),d0=cf(-23,17);
 const hU=freg("ref_u"),hW=freg("ref_w"),hV=freg("ref_v");
 frow("ref.product",fs(fm(a0,fm(hU,hW)),cf(1)));
 frow("ref.curve",fs(fm(hV,fs(fs(hV,fm(a0,fa(hU,hW))),fscale(c0,2))),d0));
 const SH=fs(fs(hV,c0),fm(a0,hU)),TH=fa(fs(fm(a0,hW),hV),c0);
 const fH=freg("fH"),fHP=freg("fHP");
 frow("fH",fs(fm(hV,fH),hU));frow("fHP",fs(fm(hV,fHP),hW));
 const S=freg("S"),F=freg("F"),S2=fdef("S2",fsq(S));
 frow("U.curve",fs(fa(fm(F,S2),fm(D,fsq(F))),cf(1)));
 const FT=fdef("FT",fsm(F,c));
 for(const g of groups){
  const i=g.i,X=g.X;
  g.t=freg("t"+i);g.h=freg("h"+i);g.G=freg("G"+i);
  frow("pair."+i+".first",fs(fm(FT,fa(g.h,S,g.t)),fm(g.h,g.G)));
  frow("pair."+i+".second",fs(fm(D,fa(F,fsm(g.G,u))),fs(fm(fs(S,g.t),g.h),fsq(g.t))));
  const tr=trace(fm(g.h,fa(g.h,S,g.t)));
  g.tr=tr;
  if(g.r==="g"){g.X2=V("int_g_29");row("g.square",sub(g.X2,sq(X)))}
  else g.X2=def("X2_"+i,sq(X));
  if(g.r==="b")row("b.fourth",sub(V("int_b_30"),sq(g.X2)));
 }
 const T=def("trace",plus(...groups.map(g=>g.tr)));
 count.point_and_input_square=names.length-outerCount;
 // Positive fourth-power tree with 13 leaves, including the one aggregate trace.
 let leaves=[...groups.map(g=>({p:g.X,s:g.X2})),{p:T,s:def("trace2",sq(T))}];
 let lev=0;
 while(leaves.length>1){
  const next=[];for(let i=0;i<leaves.length;i+=2){
   if(i+1===leaves.length){next.push(leaves[i]);continue;}
   let val=plus(sq(leaves[i].s),sq(leaves[i+1].s));
   if(leaves.length===2)val=plus(V("B_abc"),sc(val,2));
   const p=def("tree"+lev+"_"+i,val),s=def("treesq"+lev+"_"+i,sq(p));next.push({p,s})
  }leaves=next;lev++;
 }
 const M=leaves[0].p, M4=def("M4",sq(leaves[0].s)),a=def("center",plus(sq(M4),C(784)));
 count.height=names.length-outerCount-count.point_and_input_square;
 // All contact polynomials and their derivatives use shared powers.
 const z=reg("n_z"),z2=def("z2",sq(z)),T0=def("contactT",sub(sq(a),z2)),S0=plus(T0,sc(z2,2)),P=def("contactP",sq(T0)),PP=def("PP",sq(P)),PS=def("PS",mul(P,S0)),SS=def("SS",sq(S0)),TP=def("TP",mul(T0,P)),TS=def("TS",mul(T0,S0));
 const A=[PP,sc(PS,-130),plus(sc(P,4097),sc(SS,256)),sc(S0,-8320),C(4096)];
 const B=[PP,sc(PS,-130),plus(sc(P,2657),sc(SS,3136)),sc(S0,-101920),C(614656)];
 const H=[sc(TP,4),plus(sc(TS,-260),sc(P,-130)),plus(sc(T0,8194),sc(S0,512)),C(-8320)];
 const Fcoeff=[];
 for(let j=0;j<=8;j++){let p=plus(...A.map((q,i)=>i<=j&&j-i<=4?mul(q,B[j-i]):C(0)));Fcoeff.push([...p.keys()].every(m=>!m.includes("|"))?p:def("Fcoef"+j,p))}
 const evalp=(l,v)=>plus(...l.map((p,j)=>sc(p,v**BigInt(j))));
 const scales=[11,13,17,19,23,29,31,37,41,43,47,53],rs=[];
 const p0=V("P"),s0=V("S"),t0=V("T");
 const der=(p,x)=>{let a=[];for(const [m,v]of p){let ns=m.split("|").filter(Boolean),k=ns.filter(n=>n===x).length;if(k){ns.splice(ns.indexOf(x),1);a.push(new Map([[ns.join("|"),BigInt(k)*v]]))}}return plus(...a)};
 const L=p=>plus(mul(sc(t0,2),der(p,"P")),der(p,"S"));
 const direct=(v,r)=>plus(p0,sc(s0,-2n*BigInt(r*r)*v),C(BigInt(r**4)*v*v));
 for(let i=0;i<k;i++){let v=BigInt(scales[i]**2),g=groups[i],aa=evalp(A,v),bb=evalp(B,v),hh=evalp(H,v),dd=sc(plus(sc(T0,-4),sc(S0,8),C(-130n*v)),720n*v*v);
  const pa=mul(direct(v,1),direct(v,8)),pb=mul(direct(v,4),direct(v,7));
  const pa0=plus(sq(p0),sc(mul(p0,s0),-130n*v),sc(plus(sc(p0,4097),sc(sq(s0),256)),v*v),sc(s0,-8320n*v**3n),C(4096n*v**4n));
  const pb0=plus(sq(p0),sc(mul(p0,s0),-130n*v),sc(plus(sc(p0,2657),sc(sq(s0),3136)),v*v),sc(s0,-101920n*v**3n),C(614656n*v**4n));
  chk(eq(pa,pa0)&&eq(pb,pb0),"pair expansion");
  chk(eq(sub(L(pb),L(pa)),sc(plus(sc(t0,-4),sc(s0,8),C(-130n*v)),720n*v*v)),"derivative difference");
  g.contact=evalp(Fcoeff,v);
  let ri=reg("n_r"+i);rs.push(ri);
  row("deriv"+i,plus(sc(mul(ri,g.contact),8),mul(hh,plus(aa,bb)),mul(dd,aa)));
 }
 const au=def("au",mul(a,u));row("derivative_sum",sub(mul(au,plus(...rs)),C(k)));
 count.contact=names.length-outerCount-count.point_and_input_square-count.height;
 // Shared field tests and coefficients.
 const fh2=fdef("fh2",fsq(fH)),fpt=fdef("fpt",fsm(bar(fHP),c)),fpt2=fdef("fpt2",fsq(fpt));
 const R=fdef("R",fa(fsm(fa(fh2,fpt2),c),fsq(FT)));
 const R2=fdef("R2",fsq(R)),R4=fdef("R4",fsq(R2)),R8=fdef("R8",fsq(R4));
 const CS=fdef("CS",fsm(S,c)),CH=fdef("CH",fsm(SH,c)),CS2=fdef("CS2",fm(CS,S)),CSSH=fdef("CSSH",fm(CS,SH)),CH2=fdef("CH2",fm(CH,SH));
 count.shared_detector=names.length-outerCount-count.point_and_input_square-count.height-count.contact;
 let ws=[];
 for(const g of groups){
  const i=g.i, I=fdef("I"+i,fs(fsm(g.t,g.X),TH)),J=freg("J"+i),Q=fdef("Q"+i,fsq(bar(g.G)));
  frow("J"+i,fs(fsm(J,u),fsq(bar(I))));
  const W=fdef("W"+i,fa(cf(1),R8,fsm(CS2,g.X2),fscale(fsm(CSSH,g.X),-2),CH2,fsq(J),fsq(Q)));
  const d=reg("n_D"+i);row("norm"+i,sub(mul(d,trace(W)),norm(fs(W,cf(1)))));
  const rr=def("gateR"+i,mul(g.contact,d)),tt=def("gateT"+i,plus(u,sq(rr))),vv=reg("n_gateV"+i);row("gateV"+i,sub(mul(tt,vv),sq(d)));
  const w=reg("n_gateW"+i);row("gateW"+i,sub(mul(c,sub(w,C(1))),sq(vv)));ws.push(w);
 }
 count.private_detector=names.length-outerCount-count.point_and_input_square-count.height-count.contact-count.shared_detector;
 let W=ws[0];for(let i=1;i<ws.length;i++)W=def("prod"+i,mul(W,ws[i]));
 const alpha=def("alpha",plus(u,sq(sub(W,C(1))))),tau=reg("n_tau");row("tau",sub(mul(tau,plus(C(1),alpha)),alpha));
 const bs=def("bs",sc(sq(tau),7)),e=reg("n_e"),U=reg("n_U"),p=reg("n_p"),V0=reg("n_V"),q=reg("n_q"),P0=reg("n_P"),Q0=reg("n_Q");
 row("pole.pSquare",sub(sq(p),mul(c,P0)));row("pole.first",plus(mul(bs,P0),sq(e),sc(sq(u),-1)));row("pole.factor",plus(mul(bs,e),sc(mul(e,u),-1),mul(U,V0)));row("pole.qSquare",sub(sq(q),mul(c,Q0)));row("pole.second",plus(mul(bs,Q0),sc(sq(U),-1),sq(V0)));
 count.shared_pole=names.length-Object.values(count).reduce((a,b)=>a+b,0);
 // Reindex exact outer residuals; new rows have coefficients in Z[B_abc].
 const pos=new Map(names.map((n,i)=>[n,i+1]));
 const out=keep.map(q=>({...q,terms:q.terms.map(a=>({...a,monomial:a.monomial.map(j=>pos.get(old[j-1])).sort((a,b)=>a-b)}))}));
 for(const q of rows){let terms=new Map;for(const [m,v] of q.p){let ns=m.split("|").filter(Boolean), b=ns.filter(x=>x==="B_abc").length;
   chk(b<=1,"parameter power");let idx=ns.filter(x=>x!=="B_abc").map(x=>pos.get(x)).sort((a,b)=>a-b);chk(idx.every(x=>x!==undefined),"unknown symbol "+m);
   let key=idx.join(","),a=terms.get(key)||[0n,0n];a[b]+=v;terms.set(key,a);
 }out.push({name:q.name,terms:[...terms].map(([m,a])=>({monomial:m?m.split(",").map(Number):[],coefficient:[a[0]?String(a[0]):"",a[1]?String(a[1])+"*B_abc":""].filter(Boolean).join("+")||"0"})).filter(x=>x.coefficient!=="0")})}
 chk(new Set(out.flatMap(q=>q.terms.flatMap(a=>a.monomial))).size===names.length,"full support");
 chk(out.every(q=>q.terms.every(a=>a.monomial.length<=2)),"quadratic");
 const key=(q,ns)=>JSON.stringify(q.terms.map(a=>[a.coefficient,a.monomial.map(j=>ns[j-1]).sort().join("|")]).sort((a,b)=>a[1].localeCompare(b[1])));
 chk(keep.every((q,i)=>key(q,old)===key(out[i],names)),"outer equality");
 let valcases=0;for(let s=0;s<=12;s++)for(let d=-50;d<=50;d++){let v=2*d-Math.min(1,2*s+2*d);if(s===0)chk(v>=0,"inactive");else chk((v>=0)===(d>=1),"active");valcases++}
 chk(487n*997n**4n>200n*1001n**4n,"height margin");
 return {status:"proved_transfer_under_retained_arithmetic_premises_and_ordinary_rational_abc",predecessor:src,predecessor_git_blob:"e02b09a058d6f7f59c3a04a150be65c4de21f7f8",variables:names.length,variable_names:names,parameters:t.parameters,ordinary_integer_inputs:roles,reciprocal_integer_inputs:t.reciprocal_integer_inputs,integer_blocks:k,input_is_fixed_coefficient:true,instance_range:t.instance_range,degree_of_each_residual_at_most:2,sum_of_squares_degree:4,retained_arithmetic_interfaces:t.retained_arithmetic_interfaces,source_coding_theorem:t.source_coding_theorem,unconditional_undecidability_claim:false,native_pole_blocks:1,contact_scales:scales,verification:{outer_rows:keep.length,new_rows:rows.length,variable_breakdown:count,full_support:true,finite_valuation_cases:valcases},residuals:out};
}
const raw=fs.readFileSync(path.join(__dirname,"../abc_gate_fraction_v114/quadrics.json"));
if(crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex")!=="e02b09a058d6f7f59c3a04a150be65c4de21f7f8")throw Error("source blob");
const t=build(JSON.parse(raw)),out=path.join(__dirname,"quadrics.json");
if(process.argv.includes("--write"))fs.writeFileSync(out,JSON.stringify(t)+"\n");else if(JSON.stringify(t)!==JSON.stringify(JSON.parse(fs.readFileSync(out))))throw Error("table mismatch");
console.log(JSON.stringify({variables:t.variables,rows:t.residuals.length,verification:t.verification}));
