// Independent symbolic-support, exact modular-prefix and small carry fixtures.
import fs from 'node:fs';
import {naturalSource,source,build,old} from './build.mjs';
const fixtures=[{x:"100",z:"1",u:"1",y:"1"},{x:"257",z:"7",u:"19",y:"23"},{x:"9999",z:"21",u:"1",y:"2"}];
const base=naturalSource(old,fixtures[0]),first=source(base,old);
// Symbolic support of the natural-number source, BEFORE evaluating x,z,u,y.
const drop=new Set(["positive.g","positive.ell_minus_u","positive.e_minus_y","c_integrality.halftrace"].map(n=>"jones1980."+n)),shifted=new Set(["g","t","m"]);
const edges=new Set(),certvars=new Set();
function ec(t){let p=new Map();for(let q of t.replace(/\s/g,"").match(/[+-]?[^+-]+/g)||[]){let c=q[0]==="-"?-1n:1n;let v=[];for(const x of q.replace(/^[+-]/,"").split("*")){if(/^\d+$/.test(x))c*=BigInt(x);else v.push(x)}let k=v.sort().join("*");p.set(k,(p.get(k)||0n)+c)}return p}
function add(p,vs,c){const k=vs.slice().sort().join("*"),q=p.get(k)||new Map();for(const [m,a] of c){const v=(q.get(m)||0n)+a;if(v)q.set(m,v);else q.delete(m)}if(q.size)p.set(k,q);else p.delete(k)}
function assess(p){for(const [k,c] of p){let ns=k?k.split("*"):[];if(c.size===1&&c.has("")&&c.get("")!==0n)for(let n of ns)certvars.add(n);while(ns.length<2)ns.push("@dummy");edges.add(ns.sort().join("*"))}}
for(const r of old.residuals.filter(r=>r.name.startsWith("jones1980.")&&!drop.has(r.name))){let p=new Map();for(const t of r.terms){let ns=t.monomial.map(i=>old.variable_names[i-1]);if(ns.some(n=>/^positive_(alpha|eta)_/.test(n)))continue;let parts=[[]];for(let n of ns){let q=parts.map(m=>[...m,n]);if(shifted.has(n))q.push(...parts);parts=q;}for(let m of parts)add(p,m,ec(t.coefficient))}
if(r.name.endsWith("positive.alpha"))add(p,["slack_alpha"],new Map([["",-2n]]));if(r.name.endsWith("positive.eta"))add(p,["slack_eta"],new Map([["",-2n]]));assess(p)}
for(const [name,terms] of [["b_square",[[1,"source_b2"],[-1,"b","b"]]],["b_fourth",[[1,"int_b_30"],[-1,"source_b2","source_b2"]]],["g_square",[[1,"int_g_29"],[-1,"g","g"],[-2,"g"],[-1]]]]){let p=new Map();for(const [c,...v] of terms)add(p,v,new Map([["",BigInt(c)]]));assess(p)}
if(certvars.size!==63||edges.size!==136||base.variables.some(n=>!certvars.has(n)))throw Error("uniform support");
if(first.source_prefix.pairs.some(p=>edges.has(p.slice().sort().join("*"))))throw Error("uniform matching");
// Direct modular evaluation: no huge integer exponent is ever materialized.
const mod=(x,p)=>((x%p)+p)%p;
function pow(b,e,p){let t=1n;b=mod(b,p);while(e>0n){if(e&1n)t=t*b%p;b=b*b%p;e>>=1n}return t}
function div(a,b,p){b=mod(b,p);if(b===0n)throw Error("zero modular denominator");return mod(a*pow(b,p-2n,p),p)}
function evaluatePrefix(sys,s,f,g,p){
 const names=s.variable_names,values=new Map([["f",mod(f,p)],["g",mod(g,p)]]);
 for(const q of s.residuals){if(q.name.includes("BD_positive_f")||q.name.includes("BD_g_interval"))break;let unknown=new Set(q.terms.flatMap(t=>t.monomial.map(i=>names[i-1])).filter(n=>!values.has(n)));if(unknown.size!==1)throw Error("nontriangular "+q.name);let v=[...unknown][0],a=0n,b=0n;for(const t of q.terms){let c=BigInt(t.coefficient),k=0;for(const i of t.monomial){let n=names[i-1];if(n===v)k++;else c=mod(c*values.get(n),p)}if(k===0)a+=c;else if(k===1)b+=c;else throw Error("degree in "+v)}if(mod(b,p)===0n)return false;values.set(v,div(-a,b,p));}
 const E=BigInt(sys.equations.length),meta=s.source_prefix,D=BigInt(meta.center),L=BigInt(meta.spacing),beta=BigInt(meta.beta),b=f*f,B=beta*b*b,pos=new Map();
 meta.pairs.forEach(([a,c],i)=>{let d=L*(1n<<BigInt(meta.exponents[i]));pos.set(a,D+d);pos.set(c,D-d)});
 const BP=e=>pow(B,e,p),N0=BP(2n*D),N02=BP(4n*D),Qmax=BP(8n*D),seed=BP(E);
 let sum=0n;for(const v of sys.variables)sum=mod(sum+BP(pos.get(v)),p);
 const mask=mod(N0-1n-(b-1n)*sum,p),dummy=BP(pos.get("@dummy")),g2=mod((g+dummy)**2n,p);
 let eqs=sys.equations.map(r=>({name:r.name,p:new Map(r.p)}));const j0=eqs.findIndex(r=>(r.p.get("")||0n)!==0n);let [last]=eqs.splice(j0,1);if(last.p.get("")<0n)last.p=new Map([...last.p].map(([k,v])=>[k,-v]));eqs.push(last);
 let pack=0n;
 for(let j=0;j<eqs.length;j++)for(let [k,c] of eqs[j].p){let v=k?k.split("*"):[];while(v.length<2)v.push("@dummy");let w=v[0]===v[1]?2n:1n;let exponent=4n*D+BigInt(j)-pos.get(v[0])-pos.get(v[1]);pack=mod(pack+c*w*BP(exponent),p)}
 const geom=div(Qmax-1n,B-1n,p),K=mod(g2*pack+div(B*geom,2n,p),p),gm=div(seed-1n,B-1n,p),shift1=mod(N0*N02,p),shift2=mod(shift1*gm,p),S=mod(g+2n*K*N0,p),T=mod(mask+(B-2n)*shift2,p),N=mod(4n*N0*Qmax,p),R=mod((S+T+1n)*N+T+1n,p),r=mod((N-1n)*R,p);
 for(const [n,v] of Object.entries({b,BD_B:B,BD_N0:N0,BD_N02:N02,BD_Qmax:Qmax,BD_code_sum:sum,BD_dummy:dummy,BD_g2:g2,BD_coeffPack:pack,BD_geom:geom,BD_K:K,BD_testshift1:shift1,BD_testshift2:shift2,BD_ST:S+T,n:N,n2:N*N,BD_R:R,r}))if(values.get(n)!==mod(v,p))throw Error("modular prefix "+n);
 return true;
}
let modular=0,builds=0;
for(const pms of fixtures){const sys=naturalSource(old,pms),s=source(sys,old);if(s.variable_names.length!==197||s.residuals.length!==183)throw Error("source count");
 for(const f of [2n,4n,6n])for(const g of [0n,12345n])for(const p of [101n,103n,107n,109n,127n,149n,157n])if(evaluatePrefix(sys,s,f,g,p))modular++;
 for(const c of [2,3]){const t=build(s,c);if(t.variables!==(c===2?612:632)||t.quadratic_rows!==(c===2?547:565)||t.integer_certificates!==8||new Set(t.residuals.flatMap(q=>q.terms.flatMap(t=>t.monomial))).size!==t.variables||t.residuals.some(q=>q.terms.some(t=>t.monomial.length>2)))throw Error("table count");builds++}
}
// Small actual radix example. Pair x1,x2; pair x3,dummy. Exponents 0,1 (no triples).
const b=4n,B=65536n,L=2n,D=16n,nn=[D+1n*L,D-1n*L,D+2n*L,D-2n*L],N0=B**(2n*D),Qmax=B**(8n*D),N=4n*N0*Qmax;
const q=[[[1n,0,0],[1n,1,3],[-3n,3,3]],[[1n,2,2],[-1n,0,3]]];
let coeff=0n;for(let j=0;j<q.length;j++)for(const [c,i,k] of q[j])coeff+=(i===k?2n:1n)*c*B**(4n*D+BigInt(j)-nn[i]-nn[k]);
if(coeff<0n){coeff=-coeff;for(const x of q)for(const t of x)t[0]=-t[0]}
const mask=N0-1n-(b-1n)*(B**nn[0]+B**nn[1]+B**nn[2]),test=(B-2n)*(B**(4n*D)+B**(4n*D+1n)),bias=B*(Qmax-1n)/(2n*(B-1n)),T=mask+N0*test;
function carry(g){const K=(g+B**nn[3])**2n*coeff+bias,S=g+2n*K*N0; if(!(0n<=S&&S<N&&0n<=T&&T<N))throw Error("bounds");let r=(N-1n)*((S+T+1n)*N+T+1n),pop=r.toString(2).replace(/0/g,"").length,threshold=2*(N.toString(2).length-1);return {pass:(S&T)===0n,divisible:pop>=threshold}}
let digits=0,yes=0;
for(let x=0n;x<b;x++)for(let y=0n;y<b;y++)for(let z=0n;z<b;z++){let g=x*B**nn[0]+y*B**nn[1]+z*B**nn[2],truth=x*x+y===3n&&z*z===x,r=carry(g);if(r.pass!==truth||r.divisible!==truth)throw Error("digit condition");digits++;if(truth)yes++}
for(let g of [1n,b*B**nn[0],B**nn[3],N0-1n]){let r=carry(g);if(r.pass||r.divisible)throw Error("invalid mask");digits++}
if(yes===0||yes===64)throw Error("bad toy source");
const receipt={uniform_source_support:certvars.size,symbolic_forbidden_edges:edges.size,uniform_matching:32,modular_prefix_fixtures:modular,table_builds:builds,exact_carry_fixtures:digits,yes_carry_fixtures:yes};
console.log(JSON.stringify(receipt));
