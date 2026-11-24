import fs from 'node:fs';import crypto from 'node:crypto';
// Specialized natural-number quartic source -> eight certified integer inputs.
// All computations are exact and symbolic; input monomials use 1-based z indices.
function source(poly,old){
 const nu=poly.variables;if(!Number.isInteger(nu)||nu<1||nu>58)throw Error("1..58 source variables");
 const coeff=new Map();
 for(const t of poly.terms){if(!Array.isArray(t.monomial)||t.monomial.length>4||t.monomial.some(i=>!Number.isInteger(i)||i<1||i>nu))throw Error("source monomial");let m=t.monomial.slice().sort((a,b)=>a-b).join(","),a=BigInt(t.coefficient);coeff.set(m,(coeff.get(m)||0n)+a)}
 for(const [m,a] of coeff)if(a===0n)coeff.delete(m);
 const a0=coeff.get("")||0n;if(a0===0n)return {trivial:true,yes:true};
 let delta=0;for(const m of coeff.keys())delta=Math.max(delta,m?m.split(",").length:0);if(delta===0)return {trivial:true,yes:false};
 if(a0<0n)for(const [m,a] of coeff)coeff.set(m,-a);
 const fac=n=>{let x=1n;for(let i=2;i<=n;i++)x*=BigInt(i);return x},norm=[...coeff.values()].reduce((s,x)=>s+(x<0n?-x:x),0n);
 let beta=1n;while(beta<=2n*fac(delta)*norm*BigInt(nu+2)**BigInt(delta))beta*=4n;
 const inputs=["f","g","w","s","h","gamma","j","i_half"], names=[...inputs],idx=new Map(names.map((n,i)=>[n,i+1])),rows=[];
 const reg=n=>{if(idx.has(n))throw Error("duplicate "+n);names.push(n);idx.set(n,names.length);return new Map([[String(names.length),1n]])};
 const V=n=>new Map([[String(idx.get(n)||(()=>{throw Error("missing "+n)})()),1n]]);
 const C=n=>new Map([["",BigInt(n)]]);
 const add=(...args)=>{let out=new Map();for(const p of args)for(const [m,c] of p){const b=(out.get(m)||0n)+c;if(b)out.set(m,b);else out.delete(m)}return out};
 const scale=(p,c)=>new Map([...p].filter(([m,a])=>a*BigInt(c)!==0n).map(([m,a])=>[m,a*BigInt(c)]));
 const sub=(a,b)=>add(a,scale(b,-1));
 const mul=(a,b)=>{let out=new Map();for(const [m,c] of a)for(const [n,d] of b){let k=[...m.split(",").filter(Boolean),...n.split(",").filter(Boolean)].map(Number).sort((x,y)=>x-y).join(",");const e=(out.get(k)||0n)+c*d;if(e)out.set(k,e);else out.delete(k)}return out};
 const one=C(1);const row=(n,p)=>{let terms=[...p].filter(([m,c])=>c!==0n).map(([m,c])=>({coefficient:String(c),monomial:m?m.split(",").map(Number):[]}));if(!terms.length||terms.some(t=>t.monomial.length>2))throw Error("bad row "+n);rows.push({name:"jones1980."+n,terms})};
 const def=(n,p)=>{const z=reg(n);row(n,sub(z,p));return z};
 let counter=0;const pow=(n,x,e)=>{if(e===0)return one;if(e===1)return x;let q=pow(n,x,Math.floor(e/2)),v=def(n+"_pow"+(++counter),mul(q,q));if(e%2)v=def(n+"_pow"+(++counter),mul(v,x));return v};
 const f=V("f"),g=V("g"),b=def("b",add(one,scale(f,3))),B=def("BD_B",scale(pow("BD_b",b,delta),beta));
 let H=[B];for(let i=1;i<=nu+1;i++)H.push(pow("BD_H"+i,H[i-1],delta+1));
 const N0=def("BD_N0",mul(B,H[nu])),N1=def("BD_N1",scale(mul(B,pow("BD_N1base",H[nu],2*delta+1)),4)),N=def("n",mul(N0,N1)),M=def("n2",mul(N,N));
 const mu=def("BD_mu",mul(b,H[nu])),mask=def("BD_mask",sub(sub(N0,one),mul(sub(b,one),add(...H.slice(1,nu+1)))));
 let inv=[];for(let i=1;i<=nu;i++){let x=reg("BD_inv"+i);row("BD_inv"+i,sub(mul(H[i],x),one));inv.push(x)}
 const pairs=new Map();const pair=(i,j)=>{let k=i+","+j;if(!pairs.has(k))pairs.set(k,def("BD_pair"+i+"_"+j,mul(inv[i-1],inv[j-1])));return pairs.get(k)};
 let polyval=new Map();
 for(const [m,c] of coeff){const a=m?m.split(",").map(Number):[],counts=new Map();for(const i of a)counts.set(i,(counts.get(i)||0)+1);let weight=c*fac(delta-a.length);for(const n of counts.values())weight*=fac(n);
 let p;if(a.length===0)p=one;else if(a.length===1)p=inv[a[0]-1];else if(a.length===2)p=mul(inv[a[0]-1],inv[a[1]-1]);else if(a.length===3)p=mul(pair(a[0],a[1]),inv[a[2]-1]);else p=mul(pair(a[0],a[1]),pair(a[2],a[3]));
 for(const [key,value] of p){const v=(polyval.get(key)||0n)+weight*value;if(v)polyval.set(key,v);else polyval.delete(key)}}
 const scaled=def("BD_coeff_scaled",polyval),co=def("BD_coeff",mul(H[nu+1],scaled));
 const geom=reg("BD_geom");row("BD_geom",add(scale(mul(sub(B,one),geom),4),scale(N1,-1),C(4)));
 const cp=pow("BD_c",add(one,g),delta),K=reg("BD_K");row("BD_K",sub(scale(K,2),add(scale(mul(cp,co),2),mul(B,geom))));
 const S=def("BD_S",add(g,scale(mul(K,N0),2))),mid=def("BD_mid",mul(H[nu+1],N0)),T=def("BD_T",add(mask,mul(sub(B,C(2)),mid)));
 const R=def("BD_R",add(mul(add(S,T,one),N),T,one)),r=def("r",mul(sub(N,one),R));
 const tri=(n,p)=>{let s=new Map();for(let i=0;i<3;i++){let x=reg(n+"_"+i);s=add(s,x,mul(x,x))}row(n,sub(scale(p,2),s))};
 tri("BD_positive_f",sub(f,one));tri("BD_g_interval",mul(sub(g,one),sub(sub(scale(mu,2),one),g)));
 const keep=new Set(["sr.definition","U.definition","p.definition","Y.definition","a.definition","k.definition","pk.definition","tau.norm","YK.definition","d.definition","ac.definition","d.norm","E.odd_quotient","AE.definition","F2.definition","F.norm","G.definition","H.definition","GH.definition","I.norm","positive.eta","c_square.definition","crt.cF.definition","c_integrality.halftrace"].map(n=>"jones1980."+n));
 const found=old.residuals.filter(q=>keep.has(q.name));if(found.length!==keep.size)throw Error("core row count");
 for(const q of found){let terms=q.terms.map(t=>({coefficient:t.coefficient,vs:t.monomial.map(i=>old.variable_names[i-1])})).filter(t=>!t.vs.includes("power_C"));
 if(q.name!=="jones1980.positive.eta"&&terms.length!==q.terms.length)throw Error("unexpected removed power_C");
 for(const t of terms){if(!/^-?\d+$/.test(t.coefficient))throw Error("nonconstant core coefficient");for(const n of t.vs)if(!idx.has(n))reg(n)}
 rows.push({name:q.name,terms:terms.map(t=>({coefficient:t.coefficient,monomial:t.vs.map(n=>idx.get(n)).sort((a,b)=>a-b)}))})}
 // Generic interface drops unused source registers. Keep all prefix definitions; every output is in its own defining row.
 if(new Set(rows.map(r=>r.name)).size!==rows.length)throw Error("duplicate rows");
 if(rows.some(r=>r.terms.some(t=>t.monomial.length>2)))throw Error("degree");
 return {variable_names:names,residuals:rows,ordinary_integer_inputs:inputs,parameters:[],source_coding_theorem:"BDHMS arXiv:2506.20909v3 Theorem 1; v95/v101/v106 signed binomial core",source_prefix:{nu,delta,beta:String(beta),pair_helpers:pairs.size,core_rows:found.length,variables:names.length,quadratic_rows:rows.length}};
}

function build(src,contacts){
 const old=src.variable_names, rows=src.residuals.filter(q=>q.name.startsWith("jones1980."));
 const used=new Set(rows.flatMap(q=>q.terms.flatMap(t=>t.monomial)));
 const names=old.filter((n,i)=>used.has(i+1)), idx=new Map(names.map((n,i)=>[n,i+1]));
 const residuals=rows.map(q=>({name:q.name,terms:q.terms.map(t=>({coefficient:t.coefficient,monomial:t.monomial.map(i=>idx.get(old[i-1]))}))}));
 // Polynomial ring arithmetic over Q, exact coefficients. Field components use rho^2=2.
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a||1n};
 const rat=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]};
 const ra=(x,y)=>rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1]), rm=(x,y)=>rat(x[0]*y[0],x[1]*y[1]);
 const con=(a,b=1n)=>new Map([["",rat(a,b)]]);
 const variable=n=>{if(!idx.has(n))throw Error("unknown "+n);return new Map([[String(idx.get(n)),[1n,1n]]])};
 const reg=n=>{if(idx.has(n))throw Error("duplicate "+n);names.push(n);idx.set(n,names.length);return variable(n)};
 const add=(...pp)=>{let out=new Map();for(let p of pp)for(let [m,a] of p){let b=out.has(m)?ra(out.get(m),a):a;if(b[0])out.set(m,b);else out.delete(m)}return out};
 const sc=(p,a,b=1n)=>new Map([...p].map(([m,c])=>[m,rm(c,rat(a,b))]));
 const sub=(p,q)=>add(p,sc(q,-1));
 const mul=(p,q)=>{let out=new Map();for(let [m,a] of p)for(let [n,b] of q){let k=[...m.split(",").filter(Boolean),...n.split(",").filter(Boolean)].map(Number).sort((a,b)=>a-b).join(",");let c=rm(a,b);let z=out.has(k)?ra(out.get(k),c):c;if(z[0])out.set(k,z);else out.delete(k)}return out};
 const sq=p=>mul(p,p);
 const row=(n,p)=>{let d=1n;for(let [a,b] of p.values())d=d/gcd(d,b)*b;let ts=[...p].filter(([,c])=>c[0]!==0n).map(([m,[a,b]])=>({coefficient:String(a*(d/b)),monomial:m?m.split(",").map(Number):[]}));if(ts.some(t=>t.monomial.length>2))throw Error("not quadratic "+n);residuals.push({name:n,terms:ts})};
 const define=(n,p)=>{let x=reg(n);row(n,sub(x,p));return x};
 const fcon=(a,b=0)=>[con(a),con(b)], asF=x=>[x,con(0)], freg=n=>[reg(n+"_0"),reg(n+"_1")];
 const fa=(...pp)=>[add(...pp.map(x=>x[0])),add(...pp.map(x=>x[1]))];
 const fs=(x,y)=>fa(x,fscale(y,-1));const fscale=(x,a,b=1)=>[sc(x[0],a,b),sc(x[1],a,b)];
 const fm=(x,y)=>[add(mul(x[0],y[0]),sc(mul(x[1],y[1]),2)),add(mul(x[0],y[1]),mul(x[1],y[0]))];
 const fq=x=>fm(x,x), fc=x=>[x[0],sc(x[1],-1)], trace=x=>sc(x[0],2), norm=x=>sub(sq(x[0]),sc(sq(x[1]),2));
 const fr=(n,x)=>{row(n+".0",x[0]);row(n+".1",x[1])};
 const fd=(n,p)=>{let x=freg(n);fr(n,fs(x,p));return x};
 const D=fcon(11,-6), d=fcon(3,-1), one=con(1), zero=con(0), Fone=fcon(1);
 const C=reg("G_c"), u=reg("G_u");row("gauge.inverse",sub(mul(C,u),one));
 const u2=define("G_u2",sq(u)),u4=define("G_u4",sq(u2)),u5=define("G_u5",mul(u4,u)),u7=define("G_u7",mul(u5,u2));
 const failures=[];
 const failure=(n,L,up)=>{const J=freg(n);fr(n,fs(fm(J,fa(asF(up),L)),L));failures.push(J);return J};
 const failSquare=(n,E,up)=>failure(n,fd(n+"_sq",fq(E)),up);
 const pole=(n,b)=>{let e=reg(n+"_e"),p=reg(n+"_p"),q=reg(n+"_q"),v=reg(n+"_v"),w=reg(n+"_w"),p2=define(n+"_p2",sq(p)),q2=define(n+"_q2",sq(q));row(n+".first",sub(add(sq(e),mul(b,p2)),one));row(n+".middle",sub(mul(v,w),mul(e,sub(one,b))));row(n+".last",sub(sub(sq(v),sq(w)),mul(b,q2)))};
 const pair=(n,k4=one)=>{let S=freg(n+"_s"),T=freg(n+"_t"),F=freg(n+"_F"),G=freg(n+"_G"),eta=freg(n+"_eta"),dd=freg(n+"_d");
  let pi=fa(eta,S,T);fr(n+".d1",fs(dd,fm(pi,F)));fr(n+".d2",fs(dd,fm(eta,G)));fr(n+".curve",fs(fm(D,fa(F,G)),fs(fm(fs(S,T),eta),fq(T))));fr(n+".unit",fs(fs(fm(dd,fs(S,T)),fm(D,fm(F,G))),asF(k4))); // scaled unit; k4=1 for reference/growth
  return {S,T,F,G,eta,dd,absc:fm(eta,pi)};};
 let H=pair("G_ref");
 // P0=2R0; exact affine doubling in K computed by rational coefficients.
 // R0=(1+rho,2rho), slope=(3x^2-D)/(2y) = (12rho-2)/(4rho) = 3-rho/4.
 // xP = (3-rho/4)^2-2(1+rho)=57/8-(7/2)rho;
 // yP = slope*(xR-xP)-yR = -165/8+(417/32)rho.
 const xP=[con(57,8),con(-7,2)], yP=[con(-165,8),con(417,32)];
 fr("reference.x",fs(H.absc,xP));fr("reference.y",fa(fm(fa(H.eta,H.T),xP),fm(D,H.dd),yP));
 let f2=fd("G_ref_f2",fq(H.F));
 const labels=["a","t","b"].map(n=>({id:n,...pair("G_L_"+n)}));
 const aa=labels[0],pi=fa(aa.eta,aa.S,aa.T),ly=fd("G_scalar_ordinate_scaled",fscale(fa(fm(fa(aa.eta,aa.T),pi),fm(D,aa.G)),-1));
 const Z=freg("G_scalar_Z");fr("scalar.ratio",fs(fm(Z,ly),fscale(fm(H.S,pi),2))); // nonzero pi, H.S and ly follow at 149
 const Z2=fd("G_scalar_Z2",fq(Z)),Tn=trace(Z2),An=reg("G_scalar_A"),Bn=reg("G_scalar_B"),Cn=reg("G_scalar_C");
 row("scalar.A",sub(mul(An,Tn),norm(Z2)));row("scalar.B",sub(mul(Bn,Tn),trace(fm(Z2,fc(f2)))));row("scalar.C",sub(mul(Cn,Tn),norm(f2)));
 const inputs=src.ordinary_integer_inputs;
 if(inputs.length!==8)throw Error("input count");
 let pairs=[],weights=[];
 const pbase=51948354689656n;let chain=reg("G_scalar_seed");row("scalar.seed",chain);residuals[residuals.length-1].terms.push({coefficient:"-"+String(5n*(2n**20n)*149n)+"*C_parameter**2",monomial:[]});
 const formal=(n,p)=>{failure(n+"_formalF",p.F,u);failure(n+"_formalG",fc(p.G),u)};
 formal("G_H",H);
 for(let i=0;i<inputs.length;i++){
  let name=inputs[i],n="G_I"+i, X=variable(name);
  // The source's canonical b,g are positive; shift every other canonical input by one.
  let k=name==="i_half"?add(X,one):X;
  let k2=define(n+"_X2",sq(k));
  // The recharted denominator is (1+w)^2/k^2, so these very rows force k != 0.
  let w=define(n+"_scalar_w",mul(chain,k2)),den=reg(n+"_scalar_wden"),Y=reg(n+"_scalar_y");
  row(n+".scalar_wden",sub(mul(k2,den),sq(add(one,w))));
  row(n+".scalar_y",sub(mul(sub(Y,con(2504)),den),chain));
  let P=define(n+"_P",add(sq(Y),sc(Y,-76521,64))),r=define(n+"_r",add(sc(sq(P),32),sc(P,-5951086353,128),sc(Y,-455376332353657n,8192)));
  chain=define(n+"_scalar_chain",sc(mul(chain,r),1,pbase));
  let p=pair(n+"_pair",sq(k2));pairs.push(p);weights.push(k2);
  // target k is linear in the source coordinate and nonzero by the scalar-chain guard.
  let aerr=fs(p.S,fscale(H.S,2)),berr=fs(fc(p.T),fscale(fc(H.T),2));
  formal(n,p);failSquare(n+"_primaryFailure",aerr,u);failSquare(n+"_oppositeFailure",berr,u);
 }
 // One final scalar normalizer and one BB pole for the entire tuple.
 const endden=define("G_scalar_chain_den",sq(add(one,chain))),R=reg("G_scalar_R");
 row("scalar.normalizer",mul(R,endden));residuals[residuals.length-1].terms.push({coefficient:"-"+String((2n**64n)*(149n**2n))+"*C_parameter**2",monomial:[idx.get("G_I"+(inputs.length-1)+"_scalar_chain")]});
 const Rsq=define("G_scalar_Rsq",sq(R)),R4=define("G_scalar_R4",sq(Rsq)),T=reg("G_scalar_tauR");
 row("scalar.tauR",sub(mul(T,R4),add(An,mul(R,Bn),mul(Rsq,Cn))));
 const T2=define("G_scalar_tauR2",sq(T)),Bpole=reg("G_scalar_bs");
 row("scalar.bs",sub(mul(R,Bpole),sc(mul(add(R,con(9792)),T2),7,9)));pole("G_scalar_pole",Bpole);
 const ratios=[];
 for(let lab of labels){
  let n="G_test_"+lab.id,r=freg(n+"_r");fr(n+".ratio",fs(fm(r,lab.S),fscale(H.S,2)));ratios.push(r);
  let e=fd(n+"_E",fs(fm(r,fc(lab.T)),fscale(fc(H.T),2)));formal(n,lab);failSquare(n+"_oppositeFailure",e,u5);
 }
 let [a,t,m]=ratios,b=fa(fscale(m,2),Fone);
 let a2=fd("G_pell_a2",fq(a)),g=fd("G_pell_am1sq",fq(fs(a,Fone))),b2=fd("G_pell_b2",fq(b)),l=fd("G_pell_left",fm(fs(a2,Fone),g)),Delta=fd("G_pell_Delta",fs(fs(fq(t),fm(l,b2)),Fone));
 failSquare("G_pell_failure",Delta,u7);
 const W=fa(asF(u),...failures);
 const E=reg("G_error");row("global.norm_trace",sub(mul(E,trace(W)),norm(W)));const Escaled=reg("G_error_scaled");row("global.error_scaled",sub(mul(u,Escaled),E));const E2=define("G_error2",sq(Escaled));
 let all=pairs.concat(labels),agg=fa(...all.map(p=>p.absc),...weights.map(w=>fm(asF(w),d)),fscale(d,labels.length),fcon(20));
 let U=define("G_aggregate_U",agg[0]);let V=contacts===3?define("G_aggregate_V",agg[1]):null;
 let lambda=reg("G_lambda"),ts=[lambda,add(lambda,U)];if(contacts===3){let V2=define("G_aggregate_V2",sq(V));ts.push(add(ts[1],con(10),V2))}
 const theta0=[[0n,1n],[-1n,2n],[-1n,1n],[1n,2399n],[-32n,407n]];const ref=contacts===2?rat(2):rat(3,11);const center=rat(ref[0],2n*ref[1]);
 const roots=theta0.map(t=>{let a=ra(t,rat(-center[0],center[1]));return rm(a,a)});
 let co=[rat(1)];for(let a of roots){let next=Array.from({length:co.length+1},()=>rat(0));for(let i=0;i<co.length;i++){next[i]=ra(next[i],rm(co[i],rat(-a[0],a[1])));next[i+1]=ra(next[i+1],co[i])}co=next;}if(co.length!==6||co[5][0]!==1n||co[5][1]!==1n)throw Error("quintic");
 // q=(t+3)^8/G(t); G is a quintic in the centered square.
 const qs=[];
 for(let j=0;j<contacts;j++){
  let n="G_contact"+j,t=ts[j],d=add(t,con(3)),d2=define(n+"_d2",sq(d)),d4=define(n+"_d4",sq(d2)),d8=sq(d4);
  let T=define(n+"_center2",sq(sub(t,con(...center)))),T2=define(n+"_center4",sq(T)),T3=define(n+"_center6",mul(T2,T));
  let prod=define(n+"_denominator",add(mul(T2,add(T3,sc(T2,...co[4]),sc(T,...co[3]))),sc(T2,...co[2]),sc(T,...co[1]),con(...co[0])));
  let q=reg(n+"_q");row(n+".contact",sub(mul(q,prod),d8));qs.push(q);
  let g=reg(n+"_gate");row(n+".gate",sub(mul(q,sub(sub(g,one),E2)),sq(sub(C,q))));
  // q=0 is excluded by the gate and global inverse. At q=-1 no prime is consumed.
  let tau=reg(n+"_tau");row(n+".tau",sub(mul(tau,add(one,q)),g));let tau2=define(n+"_tau2",sq(tau));let b=define(n+"_pole_input",sc(mul(q,tau2),7));pole(n+"_pole",b);
 }
 row("global.gauge",sub(C,add(...qs)));
 const supports=new Set(residuals.flatMap(q=>q.terms.flatMap(t=>t.monomial)));
 if(supports.size!==names.length||residuals.some(q=>q.terms.some(t=>t.monomial.length>2||!t.coefficient)))throw Error("support");
 return {schema:"zq-undecidability-eight-input-v141",variables:names.length,quadratic_rows:residuals.length,parameters:[...src.parameters.filter(x=>x!=="B_abc"),"C_parameter"],variable_names:names,residuals,degree:4,source_inputs:inputs,integer_certificates:8,comparison_poles:contacts,scalar_poles:1,instance_input_in_coefficients:true,source_coding_theorem:src.source_coding_theorem,retains_all_arithmetic_premises:true,arithmetic_scope:"see README; v139 with eight targets, BDHMS coding theorem and signed binomial core",source_prefix:src.source_prefix,predecessor_git_blob:"94da64905107446920903f889265038b161f2f6f"};
}
export {source,build};
const raw=fs.readFileSync(new URL('../abc_curve_chart_elimination_v128/abc_quadrics.json',import.meta.url));
const hash=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');if(hash!=='94da64905107446920903f889265038b161f2f6f')throw Error('core pin');
export const old=JSON.parse(raw);
if(process.argv[2]&&!process.argv[2].startsWith('--')){const p=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),s=source(p,old);if(s.trivial){console.log(JSON.stringify({trivial:s.yes,constant:s.yes?0:1}));}else{const contacts=Number(process.argv[3]||2);if(![2,3].includes(contacts))throw Error("contacts");const t=build(s,contacts);console.log(JSON.stringify(t,null,2));}}
