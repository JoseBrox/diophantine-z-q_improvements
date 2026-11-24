import fs from 'node:fs';import crypto from 'node:crypto';
const raw=fs.readFileSync(new URL('../abc_curve_chart_elimination_v128/abc_quadrics.json',import.meta.url));
const hash=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');if(hash!=='94da64905107446920903f889265038b161f2f6f')throw Error('predecessor');
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
 const scaledSq=(n,X,up)=>{let Y=freg(n);fr(n,fs(fm(asF(up),Y),fq(X)));return Y};
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
 const aa=labels[0],xx=fd("G_scalar_x",aa.absc),yy=fd("G_scalar_y",fscale(fa(fm(fa(aa.eta,aa.T),xx),fm(D,aa.dd)),-1)),yi=freg("G_scalar_yinv");
 fr("scalar.yinv",fs(fm(yy,yi),Fone));
 const Z=freg("G_scalar_Z");fr("scalar.ratio",fs(fm(Z,yy),fscale(fm(H.S,xx),2)));
 const Z2=fd("G_scalar_Z2",fq(Z)),An=define("G_scalar_A",norm(Z2)),Bn=define("G_scalar_B",trace(fm(Z2,fc(f2)))),Cn=define("G_scalar_C",norm(f2)),Tn=trace(Z2);
 const inputs=src.ordinary_integer_inputs;
 if(inputs.length!==12)throw Error("input count");
 let pairs=[],factorList=[],weights=[];
 // R=F+c conjugate G; val(c R^2) odd; can use u P=R^2.
 const formal=n=>{let p=n.pair;let R=fd(n.name+"_R",fa(p.F,fm(asF(C),fc(p.G))));return scaledSq(n.name+"_formal",R,u)};
 factorList.push(fa(Fone,formal({name:"G_H",pair:H})));
 for(let i=0;i<inputs.length;i++){
  let name=inputs[i],n="G_I"+i, X=variable(name);
  let X2= name==="g"?variable("int_g_29"):define(n+"_X2",sq(X));
  if(name==="g")row("outer.gsquare",sub(X2,sq(X)));
  if(name==="b")row("outer.bfourth",sub(variable("int_b_30"),sq(X2)));
  let beta=add(sc(X2,51),con(2504));
  let P=define(n+"_P",add(sq(beta),sc(beta,-76521,64))),r=define(n+"_r",add(sc(sq(P),32),sc(P,-5951086353,128),sc(beta,-455376332353657n,8192)));
  let k2=sc(add(P,sc(beta,76521,64)),4);
  // N is fixed coefficient C_parameter=149^N, not an unknown. Parameter coefficients
  // introduced in the following one row only.
  let R=reg(n+"_scalar_R");
  let rr=sub(mul(R,add(one,sc(r,22201))),zero);
  row(n+".scalar_R",rr); let sr=residuals[residuals.length-1];sr.terms.push({coefficient:"-149*C_parameter**2",monomial:[idx.get(n+"_r")]});
  let Rsq=define(n+"_Rsq",sq(R)),R4=define(n+"_R4",sq(Rsq)),R5=define(n+"_R5",mul(R4,R));
  let Ahat=reg(n+"_tauhat");row(n+".tauhat",sub(mul(Ahat,Tn),add(An,mul(R,Bn),mul(Rsq,Cn))));
  let tau=reg(n+"_tau");row(n+".tau",sub(mul(tau,R5),Ahat));let tau2=define(n+"_tau2",sq(tau)),b=define(n+"_bs",sc(mul(add(Rsq,sc(R,9792)),tau2),7,9));pole(n+"_scalarpole",b);
  let p=pair(n+"_pair",sq(k2));pairs.push(p);weights.push(k2);
  // target 2 beta is affine in X^2.
  let aerr=fs(p.S,fscale(H.S,2)),berr=fs(fc(p.T),fscale(fc(H.T),2));
  let rf=formal({name:n,pair:p}),cs=scaledSq(n+"_Cs",aerr,u),es=scaledSq(n+"_Es",berr,u),e4=fd(n+"_Esq",fq(es));
  // W=1+c R^2+c^2 C^4+c^4 E^8; tags odd,2 mod4,4 mod8.
  factorList.push(fd(n+"_factor",fa(Fone,rf,fq(cs),fq(e4))));
 }
 const ratios=[];
 for(let lab of labels){
  let n="G_test_"+lab.id,r=freg(n+"_r");fr(n+".ratio",fs(fm(r,lab.S),fscale(H.S,2)));ratios.push(r);
  let e=fd(n+"_E",fs(fm(r,fc(lab.T)),fscale(fc(H.T),2))),es=scaledSq(n+"_Es",e,u5),rf=formal({name:n,pair:lab});
  factorList.push(fd(n+"_factor",fa(Fone,rf,fq(es))));
 }
 let [a,t,m]=ratios,b=fa(fscale(m,2),Fone);
 let a2=fd("G_pell_a2",fq(a)),g=fd("G_pell_am1sq",fq(fs(a,Fone))),b2=fd("G_pell_b2",fq(b)),l=fd("G_pell_left",fm(fs(a2,Fone),g)),Delta=fd("G_pell_Delta",fs(fs(fq(t),fm(l,b2)),Fone)),ds=scaledSq("G_pell_scaled",Delta,u7);
 factorList.push(fa(Fone,ds));
 let W=factorList[0];for(let i=1;i<factorList.length;i++)W=fd("G_product_"+i,fm(W,factorList[i]));
 const E=reg("G_error");row("global.norm_trace",sub(mul(E,trace(W)),norm(fs(W,Fone))));const E2=define("G_error2",sq(E));
 let all=pairs.concat(labels),agg=fa(...all.map(p=>p.absc),...weights.map(w=>fm(asF(w),d)),fscale(d,labels.length),fcon(20));
 let U=define("G_aggregate_U",agg[0]);let V=contacts===3?define("G_aggregate_V",agg[1]):null;
 let lambda=reg("G_lambda"),ts=[lambda,add(lambda,U)];if(contacts===3){let V2=define("G_aggregate_V2",sq(V));ts.push(add(ts[1],con(10),V2))}
 const theta0=[[0n,1n],[-1n,2n],[-1n,1n],[1n,2399n],[-32n,407n]];const ref=contacts===2?rat(2):rat(3,11);const center=rat(ref[0],2n*ref[1]);
 const roots=theta0.map(t=>{let a=ra(t,rat(-center[0],center[1]));return rm(a,a)});
 let co=[rat(1)];for(let a of roots){let next=Array.from({length:co.length+1},()=>rat(0));for(let i=0;i<co.length;i++){next[i]=ra(next[i],rm(co[i],rat(-a[0],a[1])));next[i+1]=ra(next[i+1],co[i])}co=next;}if(co.length!==6||co[5][0]!==1n||co[5][1]!==1n)throw Error("quintic");
 // q=(t+3)^8/G(t); G is a quintic in the centered square.
 const qs=[];
 for(let j=0;j<contacts;j++){
  let n="G_contact"+j,t=ts[j],d=add(t,con(3)),d2=define(n+"_d2",sq(d)),d4=define(n+"_d4",sq(d2)),d8=define(n+"_d8",sq(d4));
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
 return {schema:"zq-undecidability-weighted-private-v133",variables:names.length,quadratic_rows:residuals.length,parameters:[...src.parameters.filter(x=>x!=="B_abc"),"C_parameter"],variable_names:names,residuals,degree:4,source_inputs:inputs,integer_certificates:12,comparison_poles:contacts,scalar_poles:12,instance_input_in_coefficients:true,source_coding_theorem:src.source_coding_theorem,retains_all_arithmetic_premises:true,arithmetic_scope:"see README; original reflected modular contact height for each route, scalar extraction, shared formal/CRT, weighted trace/abscissa height, BB existence",predecessor_git_blob:"94da64905107446920903f889265038b161f2f6f"};
}
for(const c of [2,3]){const out=build(JSON.parse(raw),c),s=JSON.stringify(out,null,2)+'\n',p=new URL(c===2?'general_quadrics.json':'specified_quadrics.json',import.meta.url);if(process.argv.includes('--write'))fs.writeFileSync(p,s);else if(fs.readFileSync(p,'utf8')!==s)throw Error('replay mismatch');console.log(c,out.variables,out.quadratic_rows);}
