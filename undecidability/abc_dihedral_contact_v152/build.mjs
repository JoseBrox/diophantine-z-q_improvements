import fs from "node:fs";
import crypto from "node:crypto";
import {fileURLToPath} from "node:url";

export function build(old) {
  const fail=m=>{throw Error(m)};
  const assert=(x,m)=>{if(!x)fail(m)};
  assert(old.variables===290&&old.quadratic_residuals===239,"parent size");
  const seeds=[2,4,6,8,10,11,12,13,14,16,17,18];
  const removed=["n_z2","n_contactT","n_contactP","n_PP","n_PS","n_SS","n_TP","n_TS",...Array.from({length:6},(_,i)=>"n_Fcoef"+i),"n_M4","n_M8","n_comb_G","n_comb_L"];
  const rm=new Set(removed);
  const changedNames=new Set(["new.center","new.derivative_sum","new.combined.W",...seeds.map((_,i)=>"new.deriv"+i)]);
  const names=old.variable_names.filter(n=>!rm.has(n));
  const helpers=["s","Q","A","R","q","a","t"];
  for(const side of ["x","y"])for(const n of helpers)names.push("n_dih_"+side+"_"+n);
  names.push("n_dih_P");
  assert(new Set(names).size===names.length,"duplicate names");
  const idx=new Map(names.map((x,i)=>[x,i+1]));
  function tr(c,ns=[]){
    const monomial=ns.map(n=>{assert(idx.has(n),"unknown variable "+n);return idx.get(n)}).sort((a,b)=>a-b);
    return {coefficient:String(c),monomial};
  }
  const named=(row,vn)=>JSON.stringify(row.terms.map(t=>[t.coefficient,t.monomial.map(i=>vn[i-1]).sort()]).sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b))));
  const rows=[], dropped=[];
  for(const row of old.residuals){
    const hasRemoved=row.terms.some(t=>t.monomial.some(i=>rm.has(old.variable_names[i-1])));
    if(hasRemoved||changedNames.has(row.name)){dropped.push(row.name);continue}
    const nr={name:row.name,terms:row.terms.map(t=>tr(t.coefficient,t.monomial.map(i=>old.variable_names[i-1])))};
    assert(named(row,old.variable_names)===named(nr,names),"retained "+row.name);
    rows.push(nr);
  }
  assert(dropped.length===33,"dropped row count "+dropped.length);
  assert(!dropped.some(n=>n.startsWith("jones1980.")),"source rows changed");
  function row(n,terms){
    let m=new Map();
    for(const [c,...ns] of terms){
      const k=ns.map(x=>idx.get(x)).sort((a,b)=>a-b).join(",");
      assert(!ns.some(x=>!idx.has(x)),"unknown term "+ns);
      m.set(k,(m.get(k)||0n)+BigInt(c));
    }
    rows.push({name:n,terms:[...m].filter(([,v])=>v!==0n).map(([k,c])=>({coefficient:String(c),monomial:k?k.split(",").map(Number):[]}))});
  }
  const z="n_z",a="n_center",center2="n_treesq3_0";
  row("new.center",[[1,a],[-1,center2,center2],[-784]]);
  for(const [side,sign] of [["x",-1],["y",1]]){
    const [s,Q,A,R,q,ax,tx]=helpers.map(n=>"n_dih_"+side+"_"+n);
    row("dihedral."+side+".square",[[1,s],[-1,a,a],[-2*sign,a,z],[-1,z,z]]);
    row("dihedral."+side+".Q",[[1,Q],[-1,s,s],[10,s],[-9]]);
    row("dihedral."+side+".A",[[1,A],[-1,s,Q],[35,s,s],[-126,s],[27]]);
    row("dihedral."+side+".R",[[1,A,R],[-6,a,Q],[-6*sign,z,Q]]);
    row("dihedral."+side+".q",[[1,q],[-1,R,R]]);
    row("dihedral."+side+".a",[[1,A,ax],[-6,a,Q],[-6*sign,z,Q],[120,a,s],[120*sign,z,s],[-216,a],[-216*sign,z]]);
    row("dihedral."+side+".t",[[1,A,tx],[-30,R,Q],[-120,R,s],[216,R]]);
  }
  const [qx,ax,tx]=["q","a","t"].map(n=>"n_dih_x_"+n);
  const [qy,ay,ty]=["q","a","t"].map(n=>"n_dih_y_"+n);
  const P="n_dih_P";
  row("dihedral.P",[[1,P],[-1,qx,qy]]);
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a};
  const kappas=[];
  for(const [i,seed] of seeds.entries()){
    const t=BigInt(seed),s=t*t,A=s*s*s-45n*s*s+135n*s-27n,B=6n*t*(s-1n)*(s-9n);
    const g=gcd(A*A,B*B),K=A*A/g,D=B*B/g,rr="n_r"+i;
    kappas.push([String(K),String(D)]);
    row("new.deriv"+i,[
      [12n*D*D,rr],[-12n*K*D,rr,qx],[-12n*K*D,rr,qy],[12n*K*K,rr,P],
      [D*D,ax],[D*D,ay],[-K*D,ax,qy],[-K*D,ay,qx],[-K*D,tx],[-K*D,ty],
      [K*K,tx,qy],[K*K,ty,qx]
    ]);
  }
  row("new.derivative_sum",[[-12,"n_c"],...seeds.map((_,i)=>[1,"n_r"+i])]);
  const origW=old.residuals.find(x=>x.name==="new.combined.W");
  const wterms=origW.terms.map(t=>[BigInt(t.coefficient),...t.monomial.map(i=>old.variable_names[i-1])]).filter(t=>!t.slice(1).some(n=>n==="n_comb_G"||n==="n_comb_L"));
  wterms.push([-12,"n_comb_F","n_comb_F"],[-12,"n_trace_h_unit2","n_trace_h_unit2"]);
  row("new.combined.W",wterms);
  assert(names.length===287&&rows.length===236,"new size "+names.length+"/"+rows.length);
  assert(rows.every(r=>r.terms.every(t=>t.monomial.length<=2&&t.monomial.every(i=>i>=1&&i<=names.length))),"quadratic");
  assert(new Set(rows.flatMap(r=>r.terms.flatMap(t=>t.monomial))).size===names.length,"full support");
  const Cnum=1001n**4n,Cden=997n**4n;
  assert(893n*Cden>800n*Cnum,"strict abc margin");
  return {...old,predecessor:"abc_coupled_moment_v148",predecessor_git_blob:"b2e9a603c74e8290ce92f9f6b3193ab3fa9a5639",variables:names.length,variable_names:names,quadratic_residuals:rows.length,residuals:rows,contact_scales:undefined,contact_fibers:{seeds,kappas,center:"M^4+784",group_degree:12},verification:{method:"exact retained-row comparison, dihedral rational derivative and normalized moment substitution",retained_rows:old.residuals.length-dropped.length,source_rows:rows.filter(r=>r.name.startsWith("jones1980.")).length,removed_coordinates:removed,added_coordinates:names.filter(n=>!old.variable_names.includes(n)),radical_coefficient:"893/100",physical_alpha:old.verification.physical_alpha,retained_all_arithmetic_premises:true}};
}

if(process.argv[1]===fileURLToPath(import.meta.url)){
 const raw=fs.readFileSync(new URL("../abc_coupled_moment_v148/abc_quadrics.json",import.meta.url));
 const sha=crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex");
 if(sha!=="b2e9a603c74e8290ce92f9f6b3193ab3fa9a5639")throw Error("parent pin");
 const out=JSON.stringify(build(JSON.parse(raw)),null,2)+"\n";
 if(process.argv.includes("--write"))fs.writeFileSync(new URL("./abc_quadrics.json",import.meta.url),out);
 else if(fs.readFileSync(new URL("./abc_quadrics.json",import.meta.url),"utf8")!==out)throw Error("rebuild mismatch");
 console.log("287 coordinates, 236 quadrics; exact parent and retained-row check passed");
}
