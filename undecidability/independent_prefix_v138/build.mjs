import fs from 'node:fs';
import crypto from 'node:crypto';
const L=5n**60n;
const pins={general:'f047561a7b54d15c0ad18a142d018b630b8a9224',specified:'2c4cd7b70b35e46b924f2cf08c9990d952cc8cfb'};
function build(src){
 const rename=n=>n==='power_delta'?'power_geom':n==='power_alpha'?'power_crt':n;
 const names=src.variable_names.map(rename);
 const remove=['A.definition','C.definition','modulus.definition','q.congruence'].map(n=>'jones1980.pell_power.'+n);
 const residuals=src.residuals.filter(r=>!remove.includes(r.name));
 if(residuals.length!==src.residuals.length-4)throw Error('removed rows');
 for(const n of ['power_qs','power_V','power_V2','power_b2s','power_Cq','power_inner']){if(names.includes(n))throw Error(n);names.push(n);}
 const ix=new Map(names.map((n,i)=>[n,i+1]));
 const row=(name,terms)=>residuals.push({name:'jones1980.pell_power.'+name,terms:terms.map(([c,...vs])=>({coefficient:String(c),monomial:vs.map(n=>{if(!ix.has(n))throw Error(n);return ix.get(n)}).sort((a,b)=>a-b)}))});
 row('qs.definition',[[1,'power_qs'],[-1,'q','s']]);
 row('A.definition',[[2,'power_A'],[-1,'b'],[-2,'G_I0_X2','power_qs'],[2,'power_qs']]);
 row('modulus.definition',[[1,'power_modulus'],[-2,'b','power_A'],[1,'b','b'],[1]]);
 row('V.definition',[[1,'power_V','b'],[-1,'power_V'],[-2,'power_A'],[1]]);
 row('V2.definition',[[1,'power_V2'],[-1,'power_V','power_V']]);
 row('b2s.definition',[[1,'power_b2s'],[-1,'G_I0_X2','s']]);
 row('Cq.definition',[[1,'power_Cq'],[-2,'power_b2s','q2'],[2,'power_b2s']]);
 row('inner.definition',[[1,'power_inner'],[-1,'power_crt','power_A'],[1,'power_crt'],[L,'power_V2'],[-1,'power_V2','power_Cq']]);
 row('C.definition',[[1,'power_C'],[-1,'power_Cq'],[-1,'power_modulus','power_inner']]);
 row('q.congruence',[[1,'q'],[-1],[-1,'B5','power_geom'],[1,'power_geom']]);
 const support=new Set(residuals.flatMap(r=>r.terms.flatMap(t=>t.monomial)));
 if(support.size!==names.length||residuals.some(r=>r.terms.some(t=>t.monomial.length>2||!t.coefficient)))throw Error('support/degree');
 return {...src,schema:'zq-undecidability-independent-prefix-v138',variables:names.length,quadratic_rows:residuals.length,variable_names:names,residuals,source_inputs:src.source_inputs.map(rename),arithmetic_scope:'v137 plus independent geometric-prefix and packed CRT power proof; see README',predecessor_git_blob:pins[src.comparison_poles===2?'general':'specified']};
}
for(const route of ['general','specified']){
 const raw=fs.readFileSync(new URL('../guarded_target_v137/'+route+'_quadrics.json',import.meta.url));
 const hash=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
 if(hash!==pins[route])throw Error('predecessor');
 const o=build(JSON.parse(raw)),s=JSON.stringify(o,null,2)+'\n',p=new URL(route+'_quadrics.json',import.meta.url);
 if(process.argv.includes('--write'))fs.writeFileSync(p,s);else if(fs.readFileSync(p,'utf8')!==s)throw Error('replay mismatch');
 console.log(route,o.variables,o.quadratic_rows);
}
