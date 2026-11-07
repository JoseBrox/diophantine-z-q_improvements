'use strict';
// Independent reconstruction of the public Brox v3 arithmetic system.
// No author gate program or coefficient table is imported.
const fs=require('node:fs'), path=require('node:path'), crypto=require('node:crypto');
const OUT=__dirname;
function abs(a){return a<0n?-a:a;}
function gcd(a,b){a=abs(a);b=abs(b);while(b){let c=a%b;a=b;b=c;}return a;}
function Q(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error('zero rational denominator');if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return[n/g,d/g];}
const qadd=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const qmul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const qneg=a=>[-a[0],a[1]], qinv=a=>Q(a[1],a[0]);
const qstr=a=>`${a[0]}/${a[1]}`;
const key=(m,s=0)=>s+'|'+m.join(',');
function unpack(k){let [s,m]=k.split('|');return[Number(s),m?m.split(',').map(Number):[]];}
function term(c,m=[],s=0){c=Array.isArray(c)?c:Q(c);return c[0]?new Map([[key(m,s),c]]):new Map();}
const C=(n,d=1)=>term(Q(n,d)), zero=C(0), one=C(1);
function add(...ps){let r=new Map();for(let p of ps)for(let[k,c]of p){let v=qadd(r.get(k)||Q(0),c);if(v[0])r.set(k,v);else r.delete(k);}return r;}
function scale(p,c){c=Array.isArray(c)?c:Q(c);return new Map([...p].map(([k,a])=>[k,qmul(a,c)]).filter(([,a])=>a[0]));}
const sub=(a,b)=>add(a,scale(b,-1));
function mul(a,b){let r=new Map();for(let[k,c]of a)for(let[l,d]of b){let[sk,m]=unpack(k),[sl,n]=unpack(l);let z=key([...m,...n].sort((x,y)=>x-y),sk+sl);let v=qadd(r.get(z)||Q(0),qmul(c,d));if(v[0])r.set(z,v);else r.delete(z);}return r;}
const sq=a=>mul(a,a);
function degree(p){return Math.max(0,...[...p.keys()].map(k=>unpack(k)[1].length));}
function encode(p){return[...p].sort(([a],[b])=>a.localeCompare(b)).map(([k,c])=>{let[s,m]=unpack(k);return{monomial:m,sPower:s,coefficient:qstr(c)};});}
function signature(p){return JSON.stringify(encode(p));}
function constant(p){if(!p.size)return Q(0);if(p.size!==1||!p.has('0|'))return null;return p.get('0|');}
let coords=[],residuals=[],gates=[],values={},guards=[],cse=new Map(),divisionCse=new Map(),census=[];
let block='base', src=[2354,2487];
function fresh(name,kind='gate',protect=false){let id=coords.length;coords.push({id,name,kind,protected:protect,block,sourceLines:src});return term(1,[id]);}
function idof(p){let t=[...p];if(t.length!==1)throw Error('not variable');let[s,m]=unpack(t[0][0]);if(s||m.length!==1||qstr(t[0][1])!=='1/1')throw Error('not variable');return m[0];}
function residual(name,p,kind='structural'){if(degree(p)>2)throw Error(`${name} has degree ${degree(p)}`);let id=residuals.length;residuals.push({id,name,kind,block,sourceLines:src,terms:encode(p)});return id;}
function deps(...ps){return[...new Set(ps.flatMap(p=>[...p.keys()].flatMap(k=>unpack(k)[1])))].sort((a,b)=>a-b);}
function save(name,p){values[name]={terms:encode(p),block,sourceLines:src};return p;}
function saveF(name,a){save(name+'.0',a[0]);save(name+'.1',a[1]);return a;}
function assign(name,p){
 if(degree(p)>2)throw Error(`${name} assignment degree ${degree(p)}`);
 if(degree(p)<=1)return save(name,p);
 let h=new Map(),l=new Map();for(let[k,c]of p)(unpack(k)[1].length===2?h:l).set(k,c);
 let lead=[...h].sort(([a],[b])=>a.localeCompare(b))[0][1], norm=scale(h,qinv(lead)), sig=signature(norm), v=cse.get(sig);
 if(!v){v=fresh(name+'.quadratic');let ri=residual(name+'.definition',sub(v,norm),'gate');gates.push({coordinateId:idof(v),definitionResidualId:ri,operation:'quadratic_assignment',expression:encode(norm),dependencies:deps(norm),block,sourceLines:src});cse.set(sig,v);}
 return save(name,add(scale(v,lead),l));
}
const rm=(name,a,b)=>assign(name,mul(a,b));
const rsq=(name,a)=>assign(name,sq(a));
function rp(name,a,n){if(n===0)return one;if(n===1)return a;let v=rp(name+'.half',a,Math.floor(n/2));v=rsq(name+'.square',v);return n%2?rm(name+'.odd',v,a):v;}
function rquot(name,a,b,domain){
 let bc=constant(b);if(bc){if(!bc[0])throw Error('division by constant zero');return assign(name,scale(a,qinv(bc)));}
 if(degree(b)>1||degree(a)>2)throw Error('quotient degree');
 let sig='Q:'+signature(a)+'/'+signature(b),old=divisionCse.get(sig);if(old)return save(name,old);
 let v=fresh(name);let ri=residual(name+'.definition',sub(mul(b,v),a),'gate');gates.push({coordinateId:idof(v),definitionResidualId:ri,operation:'rational_quotient',numerator:encode(a),denominator:encode(b),domain,dependencies:deps(a,b),block,sourceLines:src});divisionCse.set(sig,v);return save(name,v);
}
function inv(name,a){let v=rquot(name,one,a,'equation_enforces_nonzero');guards.push({name,expression:encode(a),inverse:encode(v),sourceLines:src});return v;}
const F=(a,b=0)=>[Array.isArray(a)&&a[0] instanceof Map?a[0]:a instanceof Map?a:C(a),b instanceof Map?b:C(b)];
const fadd=(a,b)=>[add(a[0],b[0]),add(a[1],b[1])], fsub=(a,b)=>[sub(a[0],b[0]),sub(a[1],b[1])];
const fconj=a=>[a[0],scale(a[1],-1)];
const fc=(a,b=0)=>[Array.isArray(a)?term(a):C(a),Array.isArray(b)?term(b):C(b)];
const fscale=(a,c)=>[scale(a[0],c),scale(a[1],c)];
const rawFmul=(a,b)=>[add(mul(a[0],b[0]),scale(mul(a[1],b[1]),2)),add(mul(a[0],b[1]),mul(a[1],b[0]))];
function fmul(name,a,b){return saveF(name,[assign(name+'.0',add(mul(a[0],b[0]),scale(mul(a[1],b[1]),2))),assign(name+'.1',add(mul(a[0],b[1]),mul(a[1],b[0])))]);}
function fsq(name,a){return fmul(name,a,a);}
function fscalar(name,a,b){return saveF(name,[rm(name+'.0',a[0],b),rm(name+'.1',a[1],b)]);}
function fquot(name,a,b,domain){
 let b0=constant(b[0]),b1=constant(b[1]);
 if(b0&&b1){let norm=qadd(qmul(b0,b0),qneg(qmul(Q(2),qmul(b1,b1))));if(!norm[0])throw Error('field constant denominator zero');return fmul(name,a,[term(qmul(b0,qinv(norm))),term(qneg(qmul(b1,qinv(norm))))]);}
 let sig='FQ:'+signature(a[0])+','+signature(a[1])+'/'+signature(b[0])+','+signature(b[1]);let old=divisionCse.get(sig);if(old)return saveF(name,old);
 let z=[fresh(name+'.0'),fresh(name+'.1')];
 let eqs=[sub(add(mul(b[0],z[0]),scale(mul(b[1],z[1]),2)),a[0]),sub(add(mul(b[0],z[1]),mul(b[1],z[0])),a[1])];
 for(let j=0;j<2;j++){let ri=residual(name+'.definition.'+j,eqs[j],'gate');gates.push({coordinateId:idof(z[j]),definitionResidualId:ri,operation:'field_quotient_component',component:j,numerator:a.map(encode),denominator:b.map(encode),output:z.map(encode),domain,dependencies:deps(...a,...b),block,sourceLines:src});}
 divisionCse.set(sig,z);return saveF(name,z);
}
function finv(name,a){let z=fquot(name,fc(1),a,'equations_enforce_nonzero');guards.push({name,fieldExpression:a.map(encode),fieldInverse:z.map(encode),sourceLines:src});return z;}
function start(name,lines){block=name;src=lines;census.push({block,startCoordinates:coords.length,startResiduals:residuals.length});}
// Allocate the displayed 90 base coordinates before arithmetic gates.
const X=fresh('input','input',true), names=['A','S','T','Z','H','UA','US','UT','UZ'];
let half={};for(let n of names)half[n]={x:[fresh(n+'.chart.h0','base'),fresh(n+'.chart.h1','base')],y:[fresh(n+'.chart.j0','base'),fresh(n+'.chart.j1','base')]};
const lambda=fresh('lambda','base');
let poles=[];for(let r=0;r<3;r++)poles.push({e:fresh('detector'+r+'.scaled_e','base'),s:fresh('detector'+r+'.s','base'),p:fresh('detector'+r+'.p','base'),q:fresh('detector'+r+'.q','base')});
const scalar={t:fresh('scalar.preparation','base'),e:fresh('scalar.scaled_e','base'),s:fresh('scalar.s','base'),p:fresh('scalar.p','base'),q:fresh('scalar.q','base')};
const anchor=[fresh('anchor.u','base',true),fresh('anchor.v','base',true),fresh('anchor.w','base',true)];
const booleans=[2,3,5,7,11,13,17,'sign'].map(p=>fresh('correction.partial.'+p,'base'));
if(coords.length!==66)throw Error('base count '+coords.length);

// Odd-index root witnesses: Q in P+4E(K), with P=2R0, R0=(1+sqrt(2),2sqrt(2)).
const oddChartWitnesses={};for(let n of ['A','S','T','Z'])oddChartWitnesses[n]={
 t:[fresh(n+'.odd.t0','base'),fresh(n+'.odd.t1','base')],
 r:[fresh(n+'.odd.r0','base'),fresh(n+'.odd.r1','base')]};

const D=fc(11,-6), P={x:fc(Q(57,8),Q(-7,2)),y:fc(Q(-165,8),Q(417,32)),h:fc(-1,Q(7,4)),j:fc(Q(39,8),Q(-9,2))};
function double(name,Qp,withCurve=false){
 if(withCurve)throw Error('new double expects the already certified square-abscissa chart');
 const k=fquot(name+'.k',fadd(rawFmul(Qp.x,Qp.x),D),fscale(Qp.j,2),'nonzero_j_on_square_abscissa_chart');
 const h=fquot(name+'.h',k,Qp.h,'nonzero_h_on_square_abscissa_chart');
 const x=fsq(name+'.xSquare',h);
 const u=fquot(name+'.tSquare',rawFmul(Qp.j,Qp.j),fscale(Qp.x,2),'nonzero_x_on_square_abscissa_chart');
 const j=fsub(u,x),y=rawFmul(h,j);
 return {h:saveF(name+'.h',h),j:saveF(name+'.j',j),x:saveF(name+'.x',x),y:saveF(name+'.y',y)};
}
start('point_modules',[4311,4348]);
// Square-abscissa Kummer chart; y=h*j is kept as an expression only.
let points={};for(let n of names){
 const h=half[n].x,j=half[n].y,x=fsq(n+'.chart.x',h);
 residual(n+'.chart.equation.0',add(sq(j[0]),scale(sq(j[1]),2),scale(sq(x[0]),-1),scale(sq(x[1]),-2),D[0]));
 residual(n+'.chart.equation.1',add(scale(mul(j[0],j[1]),2),scale(mul(x[0],x[1]),-2),D[1]));

 if(oddChartWitnesses[n]){
  const t=oddChartWitnesses[n].t,r=oddChartWitnesses[n].r;
  const tt=fsub(rawFmul(t,t),fscale(fadd(x,j),2));
  const aa=fsub(fadd(rawFmul(t,h),fadd(x,j)),rawFmul(fc(1,1),rawFmul(r,r)));
  for(let k=0;k<2;k++){
   residual(n+'.odd.halfParameter.'+k,tt[k]);
   residual(n+'.odd.halfAbscissaClass.'+k,aa[k]);
  }
 }
 const y=rawFmul(h,j);
 points[n]={h:saveF(n+'.h',h),j:saveF(n+'.j',j),x:saveF(n+'.x',x),y:saveF(n+'.y',y)};
}

start('direct_targets',[2394,2399]);
let four={P};for(let n of ['A','S','T','Z'])four[n]=points[n];
start('five_differences',[2394,2399]);
function subtract(name,Qp,Rp){
 const dx=fsub(Qp.x,Rp.x),dy=fadd(Qp.y,Rp.y),di=finv(name+'.dxInverse',dx);
 const m=fquot(name+'.slope',dy,dx,'retained_dxInverse');
 const x=fsub(fsub(fsq(name+'.slopeSquare',m),Qp.x),Rp.x);
 const yr=fsub(rawFmul(m,fsub(Qp.x,x)),Qp.y),y=yr.map((v,j)=>assign(name+'.yProduct.'+j,v));
 return{x:saveF(name+'.x',x),y:saveF(name+'.y',y)};
}

const U=[points.H,points.UA,points.US,points.UT,points.UZ], R=[four.P,four.A,four.S,four.T,four.Z];
const V=U.map((p,i)=>subtract('V'+i,p,R[i]));
start('parameters_and_logarithms',[2401,2411]);
function parameters(name,p){return{point:p,f:finv(name+'.f',p.x),z:(name==='V0')?null:(p.h?fquot(name+'.z',fscale(p.h,-1),p.j,'nonzero_h_and_j_on_square_abscissa_chart'):fquot(name+'.z',fscale(p.x,-1),p.y,'finite_double_or_difference_nonzero_y_Brox4311_4348'))};}
const PU=U.map((p,i)=>parameters('U'+i,p)),PV=V.map((p,i)=>parameters('V'+i,p));
const aCoeffs=[Q(1),Q(-2,5)];for(let j=2;j<=9;j++)aCoeffs.push(qmul(aCoeffs[j-1],Q(4*j-5,4*j+1)));
// Field polynomial helpers for the degree-nine block circuit.

function rawPolynomial6(coeff,basis){
 let out=fc(0);
 for(let k=0;k<coeff.length;k++){
  let term=k<=3?basis[k]:rawFmul(basis[3],basis[k-3]);
  out=fadd(out,fscale(term,coeff[k]));
 }
 return out;
}
function log(name,p,e){
 let w=fmul(name+'.w',D,fsq(name+'.fSquare',p.f));
 if(e===40){
  let w2=fsq(name+'.wPower2',w),w3=fmul(name+'.wPower3',w2,w);
  let basis=[fc(1),w,w2];
  function block(k){let out=fc(0);for(let j=0;j<3;j++)out=fadd(out,fscale(basis[j],aCoeffs[k+j]));return out;}
  let inner=fadd(block(6),fscale(w3,aCoeffs[9]));
  let midraw=fadd(block(3),rawFmul(w3,inner)),mid=midraw.map((v,j)=>assign(name+'.middle.'+j,v));
  let outraw=fadd(block(0),rawFmul(w3,mid)),out=outraw.map((v,j)=>assign(name+'.polynomial.'+j,v));
  return p.z?fmul(name,p.z,out):fquot(name,fscale(rawFmul(p.point.h||p.point.x,out),-1),p.point.j||p.point.y,'nonzero_chart_j_or_difference_y');
 }
 let rawout=fadd(fadd(fc(aCoeffs[0]),fscale(w,aCoeffs[1])),fscale(rawFmul(w,w),aCoeffs[2]));
 let out=saveF(name+'.polynomial',rawout.map((v,j)=>assign(name+'.polynomial.'+j,v)));
 return p.z?fmul(name,p.z,out):fquot(name,fscale(rawFmul(p.point.h||p.point.x,out),-1),p.point.j||p.point.y,'nonzero_chart_j_or_difference_y');
}
const LU=PU.map((p,i)=>saveF('logU'+i,p.z)),LV=PV.map((p,i)=>log('logV'+i,p,40));
let L=[],LP=[];for(let i=1;i<=4;i++){L[i]=fquot('L'+i,LU[i],LU[0],'global_reciprocal_log_nonvanishing_Brox4353_4360');LP[i]=fconj(fquot('LP'+i,LV[i],LV[0],'global_reciprocal_log_nonvanishing_Brox4353_4360'));}
start('direct_tests_and_shared_symmetric_coefficients',[4575,4605]);
const beta=save('beta',add(scale(rsq('inputSquare',X),2),C(3)));
const CC=fmul('Lucas.C',fsub(L[2],fc(2)),L[4]), AT=fmul('Lucas.AT',L[2],L[3]);
const FF=[assign('Lucas.F0',add(sq(L[3][0]),scale(sq(L[3][1]),2),scale(mul(AT[0],CC[0]),-1),scale(mul(AT[1],CC[1]),-2),sq(CC[0]),scale(sq(CC[1]),2),C(-1))),assign('Lucas.F1',add(scale(mul(L[3][0],L[3][1]),2),scale(mul(AT[0],CC[1]),-1),scale(mul(AT[1],CC[0]),-1),scale(mul(CC[0],CC[1]),2)))];
const tests=[...PU.map((p,i)=>({value:p.f,order:i===0?40:1})),...PV.map(p=>({value:fconj(p.f),order:1}))];
for(let i=1;i<=4;i++)tests.push({value:fsub(L[i],LP[i]),order:40});
tests.push({value:fsub(L[1],[beta,zero]),order:40},{value:FF,order:40});
tests.forEach((t,j)=>saveF('test'+j,t.value));
function polyProduct(name, ys) {
 if(ys.length===1)return [fc(1),ys[0]];
 let cut=Math.floor(ys.length/2),a=polyProduct(name+'.left',ys.slice(0,cut)),b=polyProduct(name+'.right',ys.slice(cut)),out=[fc(1)];
 for(let k=1;k<a.length+b.length-1;k++){
  let c=[zero,zero];
  for(let i=Math.max(0,k-b.length+1);i<=Math.min(k,a.length-1);i++){
   let u=a[i],v=b[k-i];
   c[0]=add(c[0],mul(u[0],v[0]),scale(mul(u[1],v[1]),2));
   c[1]=add(c[1],mul(u[0],v[1]),mul(u[1],v[0]));
  }
  out[k]=[assign(name+'.co'+k+'.0',c[0]),assign(name+'.co'+k+'.1',c[1])];
 }
 return out;
}
let coeffs={};
const blockSizes={"1":[3,3,3],"40":[3,4]};
for(let m of [1,40]){
 const ys=tests.filter(t=>t.order===m).map((t,j)=>fsq('testSquare.'+m+'.'+j,t.value));
 if(m===1){
  function saved(name){return new Map(values[name].terms.map(t=>[key(t.monomial,t.sPower||0),Q(...t.coefficient.split('/'))]));}
  const partitions=[[0,1,4],[2,3,5],[6,7,8]],thirdPoints=[0,1,4];
  coeffs[m]=partitions.map((ids,j)=>{
   const [a,b,c]=ids.map(i=>ys[i]),ab=fadd(a,b);
   const w2=[saved('logV'+thirdPoints[j]+'.wPower2.0'),saved('logV'+thirdPoints[j]+'.wPower2.1')];
   const c2=fconj(fmul('reusedFourthPower'+j,w2,fc(Q(193,2401),Q(132,2401))));
   const e2raw=fadd(rawFmul(a,b),rawFmul(ab,c));
   const e2=saveF('symmetric.1.block'+j+'.co2',e2raw.map((v,k)=>assign('symmetric.1.block'+j+'.co2.'+k,v)));
   const e3raw=fsub(rawFmul(e2,c),rawFmul(ab,c2));
   const e3=saveF('symmetric.1.block'+j+'.co3',e3raw.map((v,k)=>assign('symmetric.1.block'+j+'.co3.'+k,v)));
   return [fc(1),fadd(ab,c),e2,e3];
  });
 }else{
  let at=0;
  coeffs[m]=blockSizes[m].map((n,j)=>{
   const co=polyProduct('symmetric.'+m+'.block'+j,ys.slice(at,at+n));at+=n;return co;
  });
  if(at!==ys.length)throw Error('Wrong partition');
 }
}

start('fixed_height_scales',[3352,3405]);
let productX=fc(1);
for(let n of ['A','S','T','Z'])productX=fmul('heightProduct.'+n,productX,points[n].x);
saveF('heightProduct',productX);
const scales=[one,rsq('heightProduct.scale0',productX[0]),rsq('heightProduct.scale1',add(one,rsq('heightProduct.x1Square',productX[1])))];
// Algebraic abbreviations for the weights: e=(A*delta)^5/F,
// R=1/(e*delta), q1=e/delta^3, q16=q1*e^30, q52=q1*e^102.
function evalSym(name,blocks,q){
 const top=Math.max(...blocks.map(c=>c.length-1));
 const powers=[one,q];
 for(let k=2;k<=top;k++)powers[k]=rm(name+'.power'+k,powers[Math.floor(k/2)],powers[Math.ceil(k/2)]);
 const evaluated=blocks.map((co,b)=>{
  const out=[zero,zero];
  for(let k=0;k<co.length;k++)for(let j=0;j<2;j++)out[j]=add(out[j],mul(co[k][j],powers[k]));
  return saveF(name+'.block'+b,[assign(name+'.block'+b+'.0',out[0]),assign(name+'.block'+b+'.1',out[1])]);
 });
 let out=evaluated[0];
 for(let j=1;j<evaluated.length;j++)out=fmul(name+'.join'+j,out,evaluated[j]);
 return saveF(name,out);
}
function pole(name,b,p,prep){
 const B=scale(b,17), pp=rsq(name+'.p2',p.p);
 residual(name+'.firstConic',sub(mul(B,pp),mul(sub(B,p.e),add(B,scale(p.e,3)))));
 let Up=b;if(prep){
  const t2=rsq(name+'.t2',p.t);
  const T=rquot(name+'.preparationT',add(one,mul(b,t2)),b,'scalar_b_guard_absorbed_into_preparation');
  Up=sub(rquot(name+'.UplusB',C(2),T,'preparation_equation_forces_nonzero_T'),b);
  save(name+'.U',Up);
 }
 let Bh=rm(name+'.Bh',p.e,sub(B,rsq(name+'.U2',Up))),ss=rsq(name+'.s2',p.s),qq=rsq(name+'.q2',p.q);
 residual(name+'.secondConic',sub(mul(B,qq),mul(sub(ss,Bh),add(ss,scale(Bh,3)))));
}
for(let r=0;r<3;r++){
 start('detector_'+r,[2424,2460]);let A=scales[r],t=rm('detector'+r+'.t',A,lambda),delta=sub(t,one);
 let roots=[Q(0),Q(1,2),Q(1),Q(-1,2399),Q(32,407)],cs=[Q(1)];
 for(let root of roots){let nx=Array(cs.length+1).fill(null).map(()=>Q(0));for(let k=0;k<cs.length;k++){nx[k]=qadd(nx[k],qmul(root,cs[k]));nx[k+1]=qadd(nx[k+1],cs[k]);}cs=nx;}
 let t2=rsq('detector'+r+'.Fsquare',t),middle=assign('detector'+r+'.Fmiddle',add(mul(t2,add(t,term(cs[4]))),scale(t,cs[3]),term(cs[2]))),Fv=assign('detector'+r+'.F',add(mul(t2,middle),scale(t,cs[1]),term(cs[0])));
 let Ad=rm('detector'+r+'.Adelta',A,delta);
 let ep=rquot('detector'+r+'.eWeight',mul(rp('detector'+r+'.Adelta4',Ad,4),Ad),Fv,'positive_scale_and_norm_equation_make_numerator_nonzero');
 let delta2=rsq('detector'+r+'.delta2',delta),delta3=rm('detector'+r+'.delta3',delta2,delta),q1=rquot('detector'+r+'.q1',ep,delta3,'norm_equation_forces_nonzero_delta');
 let em1=rquot('detector'+r+'.eMinus1',one,ep,'weight_nonzero'),
 em3=rquot('detector'+r+'.eMinus3',sq(em1),ep,'weight_nonzero'),
 em7=rquot('detector'+r+'.eMinus7',sq(em3),ep,'weight_nonzero'),
 em14=rsq('detector'+r+'.eMinus14',em7),
 em29=rquot('detector'+r+'.eMinus29',sq(em14),ep,'weight_nonzero'),
 em55=rquot('detector'+r+'.eMinus55',sq(em29),em3,'inverse_weight_power_nonzero');
 let q12=rquot('detector'+r+'.q12',mul(q1,em7),em29,'inverse_weight_power_nonzero'),
 q40=rquot('detector'+r+'.q40',mul(q12,ep),em55,'inverse_weight_power_nonzero');
 let w=fmul('detector'+r+'.W',evalSym('detector'+r+'.E1',coeffs[1],q1),evalSym('detector'+r+'.E40',coeffs[40],q40));
 let wi=inv('detector'+r+'.w0Inverse',w[0]),nw=rquot('detector'+r+'.normOver2w0',scale(sub(sq(w[0]),scale(sq(w[1]),2)),Q(1,2)),w[0],'retained_w0Inverse'),eDelta=rm('detector'+r+'.eDelta',ep,delta),bv=rquot('detector'+r+'.B',sq(nw),eDelta,'retained_w0_inverse_and_nonsquare_two_force_nonzero_norm');
 save('detector'+r+'.Bsemantic',bv);pole('detector'+r,bv,poles[r],false);
}
start('scalar_block',[2462,2489]);
residual('correction.initialSign',sub(sq(booleans[0]),one));
for(let i=1;i<8;i++){const p=[2,3,5,7,11,13,17][i-1];residual('correction.partialProduct'+i,add(sq(booleans[i]),scale(mul(booleans[i],booleans[i-1]),-p-1),scale(sq(booleans[i-1]),p)));}
let correction=booleans[7];
let r1=rm('scalar.rPair1',beta,sub(beta,one)),r2=rm('scalar.rPair2',sub(beta,C(2401)),add(scale(beta,32),C(343))),rr=rm('scalar.r',rm('scalar.rFour',r1,r2),sub(scale(beta,2),one));
let ri=inv('scalar.rInverse',rr),ri32=rp('scalar.rInverse32',ri,32);
const scalarPoint=subtract('scalar.shiftedS',points.S,P);
const PS=parameters('Sscalar',scalarPoint),zRatio=fquot('scalar.zRatio',fscale(rawFmul(PS.z,PU[0].point.j),-1),PU[0].point.h,'nonzero_h_on_square_abscissa_chart');
let leaves=[...PU[0].f,...PS.f,...zRatio].map((v,i)=>i===0||i===2?save('scalar.leaf'+i,mul(v,ri)):rm('scalar.leaf'+i,v,i<4?ri:ri32));
function normTree(name,a,b){return assign(name,add(sq(a),mul(rr,rsq(name+'.rightSquare',b))));}
let n0=rquot('scalar.n0',add(rr,sq(PU[0].f[0])),rr,'existing_scalar_r_inverse'),n1=rquot('scalar.n1',add(mul(leaves[1],PU[0].f[1]),sq(PS.f[0])),rr,'existing_scalar_r_inverse'),n3=normTree('scalar.n3',leaves[4],leaves[5]);
let nw=normTree('scalar.W',normTree('scalar.nLeft',n0,n1),normTree('scalar.nRight',leaves[3],n3));
let bs=rm('scalar.b',rm('scalar.correctedR',correction,rr),rsq('scalar.W2',nw));pole('scalar',bs,scalar,true);
start('anchor',[4160,4178]);
let fa=assign('anchor.physicalA',add(sq(PS.f[0]),mul(PS.f[0],PS.f[1]),scale(sq(PS.f[1]),-1)));
const anchorRow=residual('anchor.equation',add(sq(anchor[0]),scale(sq(anchor[1]),6),scale(sq(anchor[2]),-2),scale(sq(fa),-3),term(2,[],2)));
save('anchor.physicalA',fa);
for(let i=0;i<census.length;i++){let c=census[i],next=census[i+1];c.newCoordinates=(next?next.startCoordinates:coords.length)-c.startCoordinates;c.newResiduals=(next?next.startResiduals:residuals.length)-c.startResiduals;}
const sourceName='sources/diophantine_optimization_20261106_v3.tex';
// The source-reference digest is pinned below; no manuscript content is a computational input.
const data={format:'brox-independent-quadratic-ir-v1',source:{path:sourceName,sha256:'fc8bc7b8fae727e24f934ddd7de0a7cff8a005e89c3d0cac1ea14e5191b910ca',reconstruction:'independent_from_displayed_formulas_not_original_gate_bytes',refinements:[{name:'shared_scalar_point',lines:[2946,3044]},{name:'fixed_scales',lines:[3352,3405]},{name:'comparison_precision52',lines:[4160,4279]},{name:'scalar_order32',lines:[4285,4306]},{name:'quotient_domains',lines:[4311,4405]},{name:'direct_lucas',lines:[4575,4605]}]},fixedParameter:{name:'S',value:'3^(2^27)',coordinate:false},coordinates:coords,residuals,gates,values,guards,census,anchor:{rowId:anchorRow,privateCoordinateIds:anchor.map(idof),physicalA:encode(fa)},counts:{baseCoordinates:coords.filter(c=>c.kind==='base'||c.kind==='input').length,structuralResiduals:residuals.length-gates.length,coordinates:coords.length,residuals:residuals.length,gates:gates.length}};
fs.writeFileSync(path.join(OUT,'raw-ir.json'),JSON.stringify(data,null,2)+'\n');
// An equivalent translated system. This is 16 times the original anchor
// after u=S+(U-3V+3W)/4,v=S/2+V/4,w=3S/2+W/4.
let translated=JSON.parse(JSON.stringify(data));let[u,v,w]=anchor;
translated.residuals[anchorRow].terms=encode(add(scale(sq(fa),-48),sq(u),scale(mul(u,v),-6),scale(mul(u,w),6),scale(sq(v),15),scale(mul(v,w),-18),scale(sq(w),7),mul(term(8,[],1),u)));
translated.residuals[anchorRow].name='anchor.translatedEquation';translated.anchor.translation={oldU:'S+(U-3V+3W)/4',oldV:'S/2+V/4',oldW:'3S/2+W/4',newRowEquals:'16*oldRowAfterSubstitution',determinant:'1/64'};
translated.coordinates[anchor.map(idof)[0]].name='anchor.U';translated.coordinates[anchor.map(idof)[1]].name='anchor.V';translated.coordinates[anchor.map(idof)[2]].name='anchor.W';
fs.writeFileSync(path.join(OUT,'raw-translated-ir.json'),JSON.stringify(translated,null,2)+'\n');
fs.writeFileSync(path.join(OUT,'census.json'),JSON.stringify({counts:data.counts,blocks:census},null,2)+'\n');
console.log(JSON.stringify({counts:data.counts,census},null,2));
