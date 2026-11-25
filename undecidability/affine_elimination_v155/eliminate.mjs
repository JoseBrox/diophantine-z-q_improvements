
// Exact affine elimination over the coefficient ring; no rational division.
export function eliminate(table,variable,definingRow) {
 const check=(x,m)=>{if(!x)throw Error(m)};
 const vn=table.variable_names,iv=vn.indexOf(variable)+1;
 check(iv>0,"absent variable "+variable);
 check(![...(table.ordinary_integer_inputs||[]),...(table.reciprocal_integer_inputs||[]),...(table.source_inputs||[])].includes(variable),"certified input");
 const pivot=table.residuals.find(r=>r.name===definingRow);
 check(pivot,"missing pivot "+definingRow);
 const pt=pivot.terms.filter(t=>t.monomial.includes(iv));
 check(pt.length===1&&pt[0].monomial.length===1&&["1","-1"].includes(pt[0].coefficient),"not unit affine");
 check(pivot.terms.every(t=>t.monomial.length<=1),"nonaffine pivot");
 const params=new Set(table.parameters||[]);
 function add(a,b) {
  const c=new Map(a);
  for(const [k,v] of b){const u=(c.get(k)||0n)+v;if(u)c.set(k,u);else c.delete(k)}
  return c;
 }
 function mul(a,b) {
  let c=new Map();
  for(const [k,v] of a)for(const [l,w] of b){
   const key=[...k.split("*").filter(Boolean),...l.split("*").filter(Boolean)].sort().join("*");
   c=add(c,new Map([[key,v*w]]));
  }return c;
 }
 function parse(str) {
  let out=new Map();
  const s=String(str).replace(/\s/g,"");
  for(const raw of s.match(/[+-]?[^+-]+/g)||[]){
   let a=raw.replace(/^[+-]/,""),c=raw.startsWith("-")?-1n:1n,vs=[];
   const factors=a.match(/[A-Za-z_][A-Za-z_0-9]*(?:\*\*\d+)?|\d+/g)||[];
   check(factors.join("*")===a,"bad coefficient syntax "+str);
   for(const x of factors) {
    if(/^\d+$/.test(x)){c*=BigInt(x);continue}
    const [v,e]=x.split("**");check(params.has(v),"unknown coefficient parameter "+v);
    for(let j=0;j<Number(e||1);j++)vs.push(v);
   }
   out=add(out,new Map([[vs.sort().join("*"),c]]));
  }return out;
 }
 function fmt(a) {
  let s="";
  for(const [k,c] of [...a].sort((x,y)=>x[0].localeCompare(y[0]))) {
   if(!c)continue;
   const m=new Map();for(const v of k.split("*").filter(Boolean))m.set(v,(m.get(v)||0)+1);
   const mag=(c<0n?-c:c).toString();
   const t=[...m].map(([v,e])=>v+(e===1?"":"**"+e)).join("*");
   s+=(c<0n?"-":s?"+":"")+mag+(t?"*"+t:"");
  }return s||"0";
 }
 const scale=new Map([["",-BigInt(pt[0].coefficient)]]);
 const subst=pivot.terms.filter(t=>t!==pt[0]).map(t=>({monomial:t.monomial,coeff:mul(scale,parse(t.coefficient))}));
 const remap=i=>i<iv?i:i-1;
 const names=vn.filter(n=>n!==variable),rows=[],touched=[];
 for(const row of table.residuals){
  if(row===pivot)continue;
  if(!row.terms.some(t=>t.monomial.includes(iv))){
   rows.push({...row,terms:row.terms.map(t=>({...t,monomial:t.monomial.map(remap)}))});continue;
  }
  let poly=new Map();
  for(const t of row.terms){
   const count=t.monomial.filter(i=>i===iv).length;
   let terms=[{monomial:t.monomial.filter(i=>i!==iv),coeff:parse(t.coefficient)}];
   for(let k=0;k<count;k++)terms=terms.flatMap(a=>subst.map(b=>({monomial:[...a.monomial,...b.monomial],coeff:mul(a.coeff,b.coeff)})));
   for(const q of terms){
    const key=q.monomial.sort((a,b)=>a-b).join(",");
    poly.set(key,add(poly.get(key)||new Map(),q.coeff));
   }
  }
  const terms=[...poly].filter(([,p])=>p.size).map(([k,p])=>({coefficient:fmt(p),monomial:k?k.split(",").map(Number).map(remap):[]}));
  check(terms.length>0,"unexpected identically zero row "+row.name);
  rows.push({...row,terms});touched.push(row.name);
 }
 check(rows.length===table.residuals.length-1&&names.length===vn.length-1,"census");
 check(rows.every(r=>r.terms.every(t=>t.monomial.length<=2&&t.monomial.every(i=>i>0&&i<=names.length))),"degree/index");
 check(new Set(rows.flatMap(r=>r.terms.flatMap(t=>t.monomial))).size===names.length,"support");
 const out={...table,variable_names:names,variables:names.length,residuals:rows,affine_eliminations:[...(table.affine_eliminations||[]),{variable,definingRow,touchedRows:touched}]};
 if("quadratic_rows" in table)out.quadratic_rows=rows.length;
 if("quadratic_residuals" in table)out.quadratic_residuals=rows.length;
 return out;
}
export function general(table) {
 const a=eliminate(table,"G_scalar_seed","scalar.seed");
 const b=eliminate(a,"G_contact0_group0","global.gauge");
 if(![508,540].includes(b.variables)||![457,487].includes(b.quadratic_rows))throw Error("general census");
 return {...b,schema:"zq-undecidability-affine-elimination-v155",arithmetic_scope:b.arithmetic_scope+"; exact affine eliminations of the fixed seed and one contact weight"};
}
export function abc(table) {
 const a=eliminate(table,"n_r11","new.derivative_sum");
 if(a.variables!==286||a.quadratic_residuals!==235)throw Error("abc census");
 return {...a,predecessor:"abc_dihedral_contact_v152",verification:{...a.verification,additional_affine_elimination:true,radical_coefficient:"993/100"}};
}
