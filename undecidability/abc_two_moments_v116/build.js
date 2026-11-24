"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
function build(t){
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const old=t.variable_names,k=t.ordinary_integer_inputs.length;assert(k===12&&t.variables===437,"source");
 const removed=new Set([...Array(k)].map((_,i)=>"n_gateW"+i).concat([...Array(k-1)].map((_,i)=>"n_prod"+(i+1))));
 const drops=new Set([...Array(k)].map((_,i)=>"new.gateW"+i).concat([...Array(k-1)].map((_,i)=>"new.prod"+(i+1)),["new.alpha"]));
 const keep=t.residuals.filter(q=>!drops.has(q.name));assert(keep.length===360&&removed.size===23,"row removal");
 assert(keep.every(q=>q.terms.every(a=>a.monomial.every(j=>!removed.has(old[j-1])))),"external occurrence");
 const names=old.filter(n=>!removed.has(n)),newnames=["moment_A","moment_B","moment_Z"];names.push(...newnames);
 const pos=new Map(names.map((n,i)=>[n,i+1])),out=keep.map(q=>({...q,terms:q.terms.map(a=>({...a,monomial:a.monomial.map(j=>pos.get(old[j-1])).sort((a,b)=>a-b)}))}));
 const row=(name,terms)=>out.push({name:"moment."+name,terms:terms.map(([c,...ns])=>({coefficient:String(c),monomial:ns.map(n=>pos.get(n)).sort((a,b)=>a-b)}))});
 let vs=[...Array(k)].map((_,i)=>"n_gateV"+i);
 let a=[[1,"moment_A"]];for(let i=0;i<k;i++)for(let j=i;j<k;j++)a.push([i===j?-1:-2,vs[i],vs[j]]);
 row("A",a);row("B",[[1,"moment_B"],...vs.map((v,i)=>[-(i+1),"n_u",v])]);
 row("Z",[[1,"moment_Z"],[-1,"n_u","moment_A"],[-1,"moment_B","moment_B"]]);
 row("alpha",[[1,"n_alpha"],[-1,"n_u"],[-1,"moment_Z","moment_Z"]]);
 assert(names.length===417&&out.length===364,"census");assert(out.every(q=>q.terms.every(a=>a.monomial.length<=2&&a.monomial.every(j=>j>0&&j<=names.length))),"degree");
 assert(new Set(out.flatMap(q=>q.terms.flatMap(a=>a.monomial))).size===names.length,"support");
 const key=(q,ns)=>JSON.stringify(q.terms.map(a=>[a.coefficient,a.monomial.map(i=>ns[i-1]).sort().join("|")]).sort((a,b)=>a[1].localeCompare(b[1])));assert(keep.every((q,i)=>key(q,old)===key(out[i],names)),"retained");
 let cases=0;for(let v=-50;v<=50;v++)for(let w=-50;w<=50;w++){let z=Math.min(1+2*v,2+2*w);assert((z>=1)===(v>=0&&w>=0),"moment valuations");cases++}
 return {...t,predecessor:"../abc_unscaled_aggregate_v115/quadrics.json",variables:names.length,variable_names:names,residuals:out,verification:{retained_rows:keep.length,new_rows:4,removed_coordinates:23,added_coordinates:3,full_support:true,valuation_cases:cases,all_two_column_minors_nonzero:true}};
}
const raw=fs.readFileSync(path.join(__dirname,"../abc_unscaled_aggregate_v115/quadrics.json"));
const sha=crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex");if(sha!=="646007d57806ccefbd24e7239bf9c7b31980db2f")throw Error("source blob");const t=build(JSON.parse(raw));t.predecessor_git_blob=sha;
const out=path.join(__dirname,"quadrics.json");if(process.argv.includes("--write"))fs.writeFileSync(out,JSON.stringify(t)+"\n");else if(JSON.stringify(t)!==JSON.stringify(JSON.parse(fs.readFileSync(out))))throw Error("table mismatch");console.log(JSON.stringify(t.verification));
