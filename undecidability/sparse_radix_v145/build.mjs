import fs from 'node:fs';import crypto from 'node:crypto';
// Sparse natural-number source and symmetric binary packing.
// The integer instance x and fixed parameters z,u,y are substituted first.
function naturalSource(old,params) {
 const P={};for(const n of ["x","z","u","y"]){P[n]=BigInt(params[n]);if(P[n]<1n)throw Error("positive "+n)}
 if(P.x<=32n*P.z)throw Error("outside cofinite source range");
 const drop=new Set(["positive.g","positive.ell_minus_u","positive.e_minus_y","c_integrality.halftrace"].map(n=>"jones1980."+n));
 const shifted=new Set(["g","t","m"]);
 const add=(p,ns,c)=>{const key=ns.slice().sort().join("*");const v=(p.get(key)||0n)+c;if(v)p.set(key,v);else p.delete(key)};
 const coeff=s=>{let a=0n;for(const t of s.replace(/\s/g,"").match(/[+-]?[^+-]+/g)||[]){let c=t[0]==="-"?-1n:1n;for(const k of t.replace(/^[+-]/,"").split("*")){if(/^[0-9]+$/.test(k))c*=BigInt(k);else if(Object.hasOwn(P,k))c*=P[k];else throw Error("coefficient "+s)}a+=c}return a};
 const equations=[];
 for(const r of old.residuals.filter(r=>r.name.startsWith("jones1980."))){
  if(drop.has(r.name))continue;const p=new Map();
  for(const t of r.terms){const ns=t.monomial.map(i=>old.variable_names[i-1]);if(ns.some(n=>/^positive_(alpha|eta)_/.test(n)))continue;let parts=[[]];for(const n of ns){let q=parts.map(m=>[...m,n]);if(shifted.has(n))q.push(...parts);parts=q;}for(const m of parts)add(p,m,coeff(t.coefficient))}
  if(r.name==="jones1980.positive.alpha")add(p,["slack_alpha"],-2n);
  if(r.name==="jones1980.positive.eta")add(p,["slack_eta"],-2n);
  equations.push({name:r.name,p});
 }
 for(const [name,terms] of [["b_square",[[1,"source_b2"],[-1,"b","b"]]],["b_fourth",[[1,"int_b_30"],[-1,"source_b2","source_b2"]]],["g_square",[[1,"int_g_29"],[-1,"g","g"],[-2,"g"],[-1]]]]){const p=new Map();for(const [c,...m] of terms)add(p,m,BigInt(c));equations.push({name,p})}
 const variables=[...new Set(equations.flatMap(r=>[...r.p.keys()].flatMap(k=>k?k.split("*"):[])))].sort();
 // The source is defined over the nonnegative integers. The g,t,m coordinates mean old value minus one.
 if(variables.length!==63||equations.length!==51)throw Error("source count changed");
 return {variables,equations,parameters:Object.fromEntries(Object.entries(P).map(([k,v])=>[k,String(v)]))};
}
function source(system,old) {
 const vs=system.variables.slice(),eqs=system.equations.map(r=>({name:r.name,p:new Map(r.p)}));
 const nu=vs.length,E=eqs.length,dummy="@dummy";
 if(nu!==63||E!==51)throw Error("fixed source");
 // Move an equation with nonzero constant to the end, with positive constant.
 let last=eqs.findIndex(r=>(r.p.get("")||0n)!==0n);if(last<0)return {trivial:true,yes:true};
 let [final]=eqs.splice(last,1);if(final.p.get("")<0n)final.p=new Map([...final.p].map(([k,c])=>[k,-c]));eqs.push(final);
 const edge=(a,b)=>[a,b].sort().join("*"),hom=k=>{const a=k?k.split("*"):[];while(a.length<2)a.push(dummy);return a};
 const forbidden=new Set(eqs.flatMap(r=>[...r.p.keys()].map(k=>edge(...hom(k)))));
 const all=[...vs,dummy];if(all.length%2)throw Error("pair count");
 // Dense complement matching, with most constrained vertex first.
 function match(xs){if(!xs.length)return [];let a=xs.reduce((best,n)=>xs.filter(b=>b!==n&&!forbidden.has(edge(n,b))).length<xs.filter(b=>b!==best&&!forbidden.has(edge(best,b))).length?n:best,xs[0]);let ys=xs.filter(b=>b!==a);for(const b of ys){if(forbidden.has(edge(a,b)))continue;let tail=match(ys.filter(n=>n!==b));if(tail)return [[a,b],...tail]}return null}
 let pairs=[["G","q3"],["T","m"],["source_c_square","h"],["V","slack_eta"],["power_modulus","U"],["w","p"],["ell","t"],["Y","j"],["a","s"],["power_A","power_alpha"],["S","r"],["e","gamma"],["int_g_29","slack_alpha"],["pell_crt_cF","n2"],["el","F2"],["lam","q5"],["power_delta","i_half"],["int_b_30","c04"],["AE","c02"],["E","n"],["k","q4"],["b","sr"],["H","B5"],["tau","d"],["power_D","ac"],["YK","GH"],["power_C","pk"],["q2","source_b2"],["g","q8"],["c","q"],["power_AC","I"],["F","@dummy"]];if(pairs.flat().slice().sort().join("|")!==all.slice().sort().join("|")||pairs.some(p=>forbidden.has(edge(...p))))throw Error("fixed matching");
 const m=pairs.length,at=pairs.findIndex(x=>x.includes(dummy));let [dp]=pairs.splice(at,1);if(dp[1]!==dummy)dp.reverse();pairs.push(dp);
 const L=64n,exps=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,24,25,27,28,30,31,33,34,36,37],lastExp=exps[m-1],D=L*(1n<<BigInt(lastExp+2));
 const pos=new Map();pairs.forEach(([a,b],i)=>{const e=L*(1n<<BigInt(exps[i]));pos.set(a,D+e);pos.set(b,D-e)});
 if(pos.get(dummy)!==[...pos.values()].reduce((a,b)=>a<b?a:b))throw Error("dummy not minimal");
 const pairSums=new Map();for(let i=0;i<all.length;i++)for(let j=i;j<all.length;j++){const k=String(pos.get(all[i])+pos.get(all[j])),a=pairSums.get(k)||[];a.push(edge(all[i],all[j]));pairSums.set(k,a)}
 for(const r of eqs)for(const k of r.p.keys()){const a=hom(k),s=pairSums.get(String(pos.get(a[0])+pos.get(a[1])));if(s.length!==1||s[0]!==edge(...a))throw Error("target collision "+k)}
 const norm=eqs.reduce((s,r)=>s+[...r.p.values()].reduce((a,c)=>a+(c<0n?-c:c),0n),0n);
 let beta=1n;while(beta<=16n*(norm+1n)*BigInt(nu+1)**2n)beta*=4n;
 const inputs=["f","g","w","s","h","gamma","j","i_half"],names=[...inputs],idx=new Map(names.map((n,i)=>[n,i+1])),rows=[];
 const reg=n=>{if(idx.has(n))throw Error("duplicate "+n);names.push(n);idx.set(n,names.length);return new Map([[String(names.length),1n]])};
 const V=n=>{if(!idx.has(n))throw Error("unknown "+n);return new Map([[String(idx.get(n)),1n]])};
 const C=n=>new Map([["",BigInt(n)]]);
 const add=(...args)=>{let out=new Map();for(const p of args)for(const [m,c] of p){const b=(out.get(m)||0n)+c;if(b)out.set(m,b);else out.delete(m)}return out};
 const scale=(p,c)=>new Map([...p].filter(([m,a])=>a*BigInt(c)!==0n).map(([m,a])=>[m,a*BigInt(c)]));
 const sub=(a,b)=>add(a,scale(b,-1));
 const mul=(a,b)=>{let out=new Map();for(const [m,c] of a)for(const [n,d] of b){let k=[...m.split(",").filter(Boolean),...n.split(",").filter(Boolean)].map(Number).sort((x,y)=>x-y).join(",");let e=(out.get(k)||0n)+c*d;if(e)out.set(k,e);else out.delete(k)}return out};
 const sq=x=>mul(x,x),one=C(1);
 const row=(n,p)=>{let terms=[...p].filter(([m,c])=>c!==0n).map(([m,c])=>({coefficient:String(c),monomial:m?m.split(",").map(Number):[]}));if(!terms.length||terms.some(t=>t.monomial.length>2))throw Error("bad row "+n);rows.push({name:"jones1980."+n,terms})};
 const def=(n,p)=>{const z=reg(n);row(n,sub(z,p));return z};
 let counter=0;const pow=(n,x,e)=>{if(e===0)return one;if(e===1)return x;let q=pow(n,x,Math.floor(e/2)),v=def(n+"_pow"+(++counter),sq(q));if(e%2)v=def(n+"_pow"+(++counter),mul(v,x));return v};
 const f=V("f"),g=V("g"),b=def("b",scale(sq(f),4)),B=def("BD_B",scale(sq(b),beta));
 // b=4*f^2, with f nonzero by the outer comparison guard. b mod3 is 0 or 1.
 const seed=pow("BD_seed",B,Number(L)),powers=[seed];for(let i=1;i<=lastExp+2;i++)powers.push(def("BD_radix"+i,sq(powers[i-1])));
 const X=powers[lastExp+2],Z=new Map(),Zinv=new Map();
 for(let i=0;i<m;i++){const p=powers[exps[i]],inv=reg("BD_inverse"+i);row("BD_inverse"+i,sub(mul(p,inv),one));const [a,b]=pairs[i];Z.set(a,p);Z.set(b,inv);Zinv.set(a,inv);Zinv.set(b,p)}
 const N0=def("BD_N0",sq(X)),N02=def("BD_N02",sq(N0)),Qmax=def("BD_Qmax",sq(N02));
 const codesum=def("BD_code_sum",mul(X,add(...vs.map(n=>Z.get(n)))));
 const mask=sub(sub(N0,one),mul(sub(b,one),codesum));
 const d0=def("BD_dummy",mul(X,Z.get(dummy))),g2=def("BD_g2",sq(add(g,d0)));
 let A=null;
 for(let j=E-1;j>=0;j--){let q=new Map();for(const [key,c] of eqs[j].p){const [i,k]=hom(key);q=add(q,scale(mul(Zinv.get(i),Zinv.get(k)),(i===k?2n:1n)*c))}A=def("BD_coeff_"+j,A===null?q:add(q,mul(B,A)))}
 const coeffPack=def("BD_coeffPack",mul(N0,A));
 const geom=reg("BD_geom");row("BD_geom",sub(mul(sub(B,one),geom),sub(Qmax,one)));
 const K=reg("BD_K");row("BD_K",sub(scale(K,2),add(scale(mul(g2,coeffPack),2),mul(B,geom))));
 const shift1=def("BD_testshift1",mul(N0,N02)),shift2=reg("BD_testshift2");
 row("BD_testshift2",sub(mul(sub(B,one),shift2),mul(shift1,sub(seed,one))));
 const S=add(g,scale(mul(K,N0),2)),T=add(mask,mul(sub(B,C(2)),shift2)),ST=def("BD_ST",add(S,T));
 const N=def("n",scale(mul(N0,Qmax),4)),M=def("n2",sq(N)),R=def("BD_R",add(mul(add(ST,one),N),T,one)),r=def("r",mul(sub(N,one),R));
 const tri=(n,p)=>{let s=new Map();for(let i=0;i<3;i++){let x=reg(n+"_"+i);s=add(s,x,sq(x))}row(n,sub(scale(p,2),s))};
 // f != 0 follows from the shared scalar/target guard; require 0<=g<N0.
 tri("BD_g_interval",mul(g,sub(sub(N0,one),g)));
 const keep=new Set(["sr.definition","U.definition","p.definition","Y.definition","a.definition","k.definition","pk.definition","tau.norm","YK.definition","d.definition","ac.definition","d.norm","E.odd_quotient","AE.definition","F2.definition","F.norm","G.definition","H.definition","GH.definition","I.norm","positive.eta","c_square.definition","crt.cF.definition","c_integrality.halftrace"].map(n=>"jones1980."+n));
 const found=old.residuals.filter(q=>keep.has(q.name));if(found.length!==keep.size)throw Error("core rows");
 for(const q of found){const terms=q.terms.map(t=>({coefficient:t.coefficient,vs:t.monomial.map(i=>old.variable_names[i-1])})).filter(t=>!t.vs.includes("power_C"));if(q.name!=="jones1980.positive.eta"&&terms.length!==q.terms.length)throw Error("unexpected power term");for(const t of terms){if(!/^-?\d+$/.test(t.coefficient))throw Error("core coeff");for(const n of t.vs)if(!idx.has(n))reg(n)}rows.push({name:q.name,terms:terms.map(t=>({coefficient:t.coefficient,monomial:t.vs.map(n=>idx.get(n)).sort((a,b)=>a-b)}))})}
 if(new Set(rows.map(r=>r.name)).size!==rows.length||rows.some(r=>r.terms.some(t=>t.monomial.length>2)))throw Error("source audit");
 return {variable_names:names,residuals:rows,ordinary_integer_inputs:inputs,parameters:[],source_coding_theorem:"Jones 1980 Theorem 2 + v128 natural source; symmetric binary quadratic packing using BDHMS Lemmas 1.4,1.6; v95/v101/v106 binomial core",source_prefix:{nu,equations:E,pairs,exponents:exps,spacing:String(L),center:String(D),beta:String(beta),variables:names.length,quadratic_rows:rows.length,source_parameters:system.parameters}};
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
 const u2=define("G_u2",sq(u)),u3=define("G_u3",mul(u2,u)),u5=define("G_u5",mul(u3,u2));
 const failures=[];
 const failure=(n,L,up)=>{const J=freg(n);fr(n,fs(fm(J,fa(asF(up),L)),L));failures.push(J);return J};
 const failSquare=(n,E,up)=>failure(n,fd(n+"_sq",fq(E)),up);
 const pole=(n,b)=>{let e=reg(n+"_e"),p=reg(n+"_p"),q=reg(n+"_q"),v=reg(n+"_v"),w=reg(n+"_w"),p2=define(n+"_p2",sq(p)),q2=define(n+"_q2",sq(q));row(n+".first",sub(add(sq(e),mul(b,p2)),one));row(n+".middle",sub(mul(v,w),mul(e,sub(one,b))));row(n+".last",sub(sub(sq(v),sq(w)),mul(b,q2)))};
 const xP=[con(57,8),con(-7,2)], yP=[con(-165,8),con(417,32)];
 const Dinv=[con(11,49),con(6,49)];
 const pair=(n,k4=one,reference=false)=>{let S=freg(n+"_s"),T=freg(n+"_t"),F=freg(n+"_F"),G=freg(n+"_G"),eta=freg(n+"_eta");
  const dd=reference?fscale(fm(Dinv,fa(yP,fm(xP,fa(eta,T)))),-1):freg(n+"_d");
  let pi=fa(eta,S,T);fr(n+".d1",fs(dd,fm(pi,F)));fr(n+".d2",fs(dd,fm(eta,G)));fr(n+".curve",fs(fm(D,fa(F,G)),fs(fm(fs(S,T),eta),fq(T))));fr(n+".unit",fs(fs(fm(dd,fs(S,T)),fm(D,fm(F,G))),asF(k4)));
  return {S,T,F,G,eta,dd,absc:fm(eta,pi)};};
 let H=pair("G_ref",one,true);
 // P0=2R0; exact affine doubling in K computed by rational coefficients.
 // R0=(1+rho,2rho), slope=(3x^2-D)/(2y) = (12rho-2)/(4rho) = 3-rho/4.
 // xP = (3-rho/4)^2-2(1+rho)=57/8-(7/2)rho;
 // yP = slope*(xR-xP)-yR = -165/8+(417/32)rho.
 fr("reference.x",fs(H.absc,xP));
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
  let k=name==="i_half"||name==="g"?add(X,one):X;
  let k2=name==="f"?sc(variable("b"),1,4):define(n+"_X2",sq(k));
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
  let e=fd(n+"_E",fs(fm(r,fc(lab.T)),fscale(fc(H.T),2)));formal(n,lab);failSquare(n+"_oppositeFailure",e,u3);
 }
 let [a,t,m]=ratios,b=fa(fscale(m,2),Fone);
 let v=fd("G_lucas_v",fm(fs(a,Fone),b)),w=fd("G_lucas_w",fm(fa(a,Fone),v)),Delta=fd("G_lucas_Delta",fs(fa(fs(fq(t),fm(t,w)),fq(v)),Fone));
 failSquare("G_lucas_failure",Delta,u5);
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
  let n="G_contact"+j,t=ts[j];
  let T=define(n+"_center2",sq(sub(t,con(...center)))),T2=define(n+"_center4",sq(T)),T3=define(n+"_center6",mul(T2,T));
  const c0=con(...center), d2=add(T,mul(sc(add(c0,con(3)),2),t),sub(con(9),sq(c0))),d4=define(n+"_d4",sq(d2)),d8=sq(d4);
  let prod=define(n+"_denominator",add(mul(T2,add(T3,sc(T2,...co[4]),sc(T,...co[3]))),sc(T2,...co[2]),sc(T,...co[1]),con(...co[0])));
  let q=reg(n+"_q");row(n+".contact",sub(mul(q,prod),d8));qs.push(q);
  let tau=reg(n+"_tau"),v=define(n+"_qtau",mul(q,tau));
  row(n+".gate",sub(mul(v,add(one,q)),add(mul(q,add(one,E2)),sq(sub(C,q)))));
  let b=define(n+"_pole_input",sc(mul(v,tau),7));pole(n+"_pole",b);
 }
 row("global.gauge",sub(C,add(...qs)));
 const supports=new Set(residuals.flatMap(q=>q.terms.flatMap(t=>t.monomial)));
 if(supports.size!==names.length||residuals.some(q=>q.terms.some(t=>t.monomial.length>2||!t.coefficient)))throw Error("support");
 return {schema:"zq-undecidability-sparse-radix-v145",variables:names.length,quadratic_rows:residuals.length,parameters:[...src.parameters.filter(x=>x!=="B_abc"),"C_parameter"],variable_names:names,residuals,degree:4,source_inputs:inputs,integer_certificates:8,comparison_poles:contacts,scalar_poles:1,instance_input_in_coefficients:true,source_coding_theorem:src.source_coding_theorem,retains_all_arithmetic_premises:true,arithmetic_scope:"see README; v145 sparse packing, padded test block, nonzero base and exact contact compression",source_prefix:src.source_prefix,predecessor_git_blob:"94da64905107446920903f889265038b161f2f6f"};
}
export {naturalSource,source,build};
const raw=fs.readFileSync(new URL('../abc_curve_chart_elimination_v128/abc_quadrics.json',import.meta.url));
const hash=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');if(hash!=='94da64905107446920903f889265038b161f2f6f')throw Error('core pin');
export const old=JSON.parse(raw);
if(process.argv[2]&&!process.argv[2].startsWith('--')){const params=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),s=source(naturalSource(old,params),old);if(s.trivial){console.log(JSON.stringify({trivial:s.yes,constant:s.yes?0:1}));}else{const contacts=Number(process.argv[3]||2);if(![2,3].includes(contacts))throw Error('contacts');console.log(JSON.stringify(build(s,contacts),null,2));}}
