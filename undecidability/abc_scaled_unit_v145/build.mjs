import fs from 'node:fs';import crypto from 'node:crypto';
function build(old) {
 const removed = new Set(["n_nestedA_0","n_nestedA_1"]);
 const names=old.variable_names.filter(n=>!removed.has(n)).concat("n_trace_h_unit4");
 const index=new Map(names.map((n,i)=>[n,i+1]));
 const row=(name,terms)=>({name,terms:terms.map(([coefficient,...ns])=>({coefficient:String(coefficient),monomial:ns.map(n=>{if(!index.has(n))throw Error(n);return index.get(n)}).sort((a,b)=>a-b)}))});
 const skipped=new Set(["new.nestedA.0","new.nestedA.1","new.alpha","new.tau","new.Z"]);
 const rows=old.residuals.filter(r=>!skipped.has(r.name)).map(r=>row(r.name,r.terms.map(t=>[t.coefficient,...t.monomial.map(i=>{const n=old.variable_names[i-1];if(removed.has(n)&&!r.name.startsWith("new.nestedV."))throw Error("unexpected use "+r.name);return n.replace(/^n_nestedA_([01])$/,"n_slotR_$1")})])));
 rows.push(row("new.trace_h_unit4",[[1,"n_trace_h_unit4"],[-1,"n_trace_h_unit2","n_trace_h_unit2"]]),
 row("new.Z",[[1,"n_u","n_Z"],[-1,"n_Z0","n_Z0"],[-1,"n_c","n_variance2"]]),
 row("new.alpha",[[1,"n_alpha"],[-1,"n_c"],[-1,"n_Z","n_Z"],[-1,"n_u","n_trace_h_unit4"]]),
 row("new.tau",[[1,"n_c2","n_tau"],[1,"n_alpha","n_tau"],[-1,"n_alpha"]]));
 const support=new Set(rows.flatMap(r=>r.terms.flatMap(t=>t.monomial)));
 if(names.length!==291||rows.length!==240||new Set(rows.map(r=>r.name)).size!==240||support.size!==291||rows.some(r=>r.terms.some(t=>t.monomial.length>2)))throw Error("count/degree/support");
 return {...old,predecessor:"abc_harmonic_selector_v130",predecessor_git_blob:"a3c2a09ea67d6e1af5e21479b2c402424ce74c3e",variables:names.length,variable_names:names,quadratic_residuals:rows.length,residuals:rows,verification:{method:"scaled pole unit test; complete named sparse rechart; degree and support checked",removed_coordinates:[...removed],added_coordinates:["n_trace_h_unit4"],physical_alpha:"u+Z_old^2+u^3*t^4",retained_all_arithmetic_premises:true}};
}
const raw=fs.readFileSync(new URL('../abc_harmonic_selector_v130/abc_quadrics.json',import.meta.url));
if(crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex")!=="a3c2a09ea67d6e1af5e21479b2c402424ce74c3e")throw Error("predecessor pin");
const out=JSON.stringify(build(JSON.parse(raw)),null,2)+"\n";
const dest=new URL('./abc_quadrics.json',import.meta.url);
if(process.argv.includes("--write"))fs.writeFileSync(dest,out);else if(out!==fs.readFileSync(dest,"utf8"))throw Error("mismatch");
console.log("291 variables / 240 residuals; exact sparse replay");
