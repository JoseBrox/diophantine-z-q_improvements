import {old,naturalSource,source,build} from './build.mjs';
function verify(old,{naturalSource,source,build}){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const fixtures=[[100,1,1,1],[33,1,2,3],[257,8,11,7],[1001,31,1,2],["900719925474099312345",7,3,5]];
 const params=a=>Object.fromEntries(["x","z","u","y"].map((n,i)=>[n,a[i]]));
 const src=source(naturalSource(old,params(fixtures[0])),old);
 const {pairs,exponents}=build(src,2).source_prefix;
 // Independent conservative parameter-uniform support, without evaluating coefficients.
 const edges=new Set(), edge=(a,b)=>[a,b].sort().join("*");
 const add=ns=>{assert(ns.length<=2,"degree");while(ns.length<2)ns.push("@dummy");edges.add(edge(...ns))};
 const drop=new Set(["positive.g","positive.ell_minus_u","positive.e_minus_y","c_integrality.halftrace"].map(n=>"jones1980."+n));
 for(const r of old.residuals){
  if(!r.name.startsWith("jones1980.")||drop.has(r.name))continue;
  for(const t of r.terms){
   const names=t.monomial.map(i=>old.variable_names[i-1]);
   if(names.some(n=>/^positive_(alpha|eta)_/.test(n)))continue;
   for(let mask=0;mask<1<<names.length;mask++){
    if(names.some((n,i)=>(mask>>i&1)&&!["g","t","m"].includes(n)))continue;
    add(names.filter((n,i)=>!(mask>>i&1)));
   }
  }
 }
 for(const ns of [["slack_alpha"],["slack_eta"],["source_b2"],["b","b"],["int_b_30"],["source_b2","source_b2"],["int_g_29"],["g","g"],["g"],[]])add(ns.slice());
 const positions=new Map();pairs.forEach(([a,b],i)=>{positions.set(a,1n<<BigInt(exponents[i]));positions.set(b,-(1n<<BigInt(exponents[i])))});
 assert(positions.size===64,"positions");
 const entries=[...positions], classes=new Map();
 for(let i=0;i<64;i++)for(let j=i;j<64;j++){
  const [a,x]=entries[i],[b,y]=entries[j],s=x+y;
  if(!classes.has(s))classes.set(s,[]);
  classes.get(s).push(edge(a,b));
 }
 const all=new Set([...classes.values()].flat());for(const e of edges)assert(all.has(e),"missing edge "+e);
 const collisions=[...classes.values()].filter(es=>es.length>1);
 for(const es of collisions)for(const e of es)assert(!edges.has(e),"used collision "+e);
 // Valuation check for the only potential threshold equality and for the
 // ordinary-abc negative odd normalizer. Infinity is covered by the proof.
 let checks=0;
 for(let mu=1;mu<=19;mu+=2)for(let f=-20;f<=20;f+=2)for(let e=-20;e<=20;e++){
  const l=Math.min(2*e,mu+f);
  if(l===mu){assert(f===0&&2*e>mu,"threshold");for(let s=-20;s<0;s++)for(let k=0;k<=10;k++){assert(f+2*s<4*k,"curve contradiction");checks++}}
  if(l>mu)assert(f>0&&2*e>mu,"pass");
 }
 for(let n=-21;n<0;n+=2)for(let t=-20;t<=20;t++){assert((2*n+4*t)%4!==0,"odd tie");checks++}
 const counts=fixtures.map(a=>{const s=source(naturalSource(old,params(a)),old);return [2,3].map(c=>{const b=build(s,c);assert(b.variables===(c===2?566:584)&&b.quadratic_rows===(c===2?501:517),"census");return [b.variables,b.quadratic_rows]})});
 return {uniform_edges:edges.size,pairs:all.size,collision_classes:collisions.length,valuation_checks:checks,counts};
}
console.log(JSON.stringify(verify(old,{naturalSource,source,build}),null,2));
