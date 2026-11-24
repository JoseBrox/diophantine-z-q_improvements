import fs from 'node:fs';
import crypto from 'node:crypto';
const raw=fs.readFileSync(new URL('../abc_curve_chart_elimination_v128/abc_quadrics.json',import.meta.url));
const hash=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
if(hash!=='94da64905107446920903f889265038b161f2f6f')throw Error('predecessor blob');
function build(src){
 const gone=new Set(["n_chi_0","n_chi_1","n_nestedV2_0","n_nestedV2_1"]);
 const names=src.variable_names.filter(n=>!gone.has(n)).concat("n_common_harmonic");
 const idx=new Map(names.map((n,i)=>[n,i+1]));
 const old=src.variable_names;
 const drop=new Set(["new.nestedV2.0","new.nestedV2.1","new.nestedChi.0","new.nestedChi.1","new.Z0"]);
 const residuals=src.residuals.filter(q=>!drop.has(q.name)).map(q=>({name:q.name,terms:q.terms.map(t=>({coefficient:t.coefficient,monomial:t.monomial.map(i=>{let n=old[i-1];if(gone.has(n))throw Error("live "+n);return idx.get(n)}).sort((a,b)=>a-b)}))}));
 const row=(name,ts)=>({name,terms:ts.map(([c,...vs])=>({coefficient:String(c),monomial:vs.map(v=>{if(!idx.has(v))throw Error(v);return idx.get(v)}).sort((a,b)=>a-b)}))});
 residuals.push(row("new.common_harmonic",[[2,"n_common_harmonic","n_nestedV_0"],[-1,"n_nestedV_0","n_nestedV_0"],[2,"n_nestedV_1","n_nestedV_1"]]));
 residuals.push(row("new.Z0",[[1,"n_Z0"],[-1,"n_common_harmonic","n_common_harmonic"],[-1,"n_c","n_failWeighted2"]]));
 const used=new Set(residuals.flatMap(q=>q.terms.flatMap(t=>t.monomial)));
 if(names.length!==292||residuals.length!==241||used.size!==names.length||residuals.some(q=>q.terms.some(t=>t.monomial.length>2||t.monomial.some(i=>!i))))throw Error("census/support");
 return {...src,variables:names.length,variable_names:names,quadratic_residuals:residuals.length,residuals,predecessor:"abc_curve_chart_elimination_v128",verification:{method:"harmonic selector, named occurrence scan",predecessor_git_blob:"94da64905107446920903f889265038b161f2f6f",degree:4,full_support:true,old_rows_retained:239,removed_variables:[...gone],added_variables:["n_common_harmonic"]}};
}
const result=JSON.stringify(build(JSON.parse(raw)),null,2)+'\n';
const dest=new URL('./abc_quadrics.json',import.meta.url);
if(process.argv.includes('--write'))fs.writeFileSync(dest,result);else if(result!==fs.readFileSync(dest,'utf8'))throw Error('table mismatch');
console.log('292 variables, 241 quadratics: exact replay');
