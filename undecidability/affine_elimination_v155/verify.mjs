import fs from 'node:fs';
import {naturalSource,source,build} from './build_general.mjs';
import {general,abc} from './eliminate.mjs';

function compare(before, after, trials, kind) {
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const evalCoeff=(t,params)=>String(t).replace(/\s/g,"").match(/[+-]?[^+-]+/g).reduce((s,raw)=>{
   let sign=raw.startsWith("-")?-1n:1n;
   let a=raw.replace(/^[+-]/,"");
   const tokens=a.match(/[A-Za-z_][A-Za-z_0-9]*(?:\*\*\d+)?|\d+/g)||[];
   assert(tokens.join("*")===a,"bad coefficient "+a);
   for(const x of tokens){
     if(/^\d+$/.test(x)){sign*=BigInt(x);continue}
     let [name,e]=x.split("**");assert(Object.hasOwn(params,name),"missing parameter "+name);
     sign*=params[name]**BigInt(e||1);
   }
   return s+sign;
 },0n);
 const evalRows=(tab,values,params)=>new Map(tab.residuals.map(row=>[row.name,row.terms.reduce((s,t)=>s+evalCoeff(t.coefficient,params)*t.monomial.reduce((p,i)=>p*values[tab.variable_names[i-1]],1n),0n)]));
 let count=0;
 for(let t=0;t<trials;t++){
   const params=Object.fromEntries([...new Set([...(before.parameters||[]),...(after.parameters||[])])].map((n,i)=>[n,BigInt(t+2+i)]));
   const values=Object.fromEntries(after.variable_names.map((n,i)=>[n,BigInt(((i+7)*(t+11)*23+(i+3)**2)%59-29)]));
   if(kind==="general"){
      values.G_scalar_seed=781189120n*params.C_parameter**2n;
      values.G_contact0_group0=8n*values.G_c-before.variable_names.filter(n=>/^G_contact\d+_group\d+$/.test(n)&&n!=="G_contact0_group0").reduce((s,n)=>s+values[n],0n);
   }else values.n_r11=12n*values.n_c-Array.from({length:11},(_,i)=>values["n_r"+i]).reduce((s,x)=>s+x,0n);
   assert(before.variable_names.every(n=>typeof values[n]==="bigint"),"missing coordinate");
   const a=evalRows(before,values,params),b=evalRows(after,values,params);
   for(const [n,v] of a){if(!b.has(n))assert(v===0n,"pivot "+n);else assert(b.get(n)===v,"row "+n);count++;}
 }
 return count;
}

const read=p=>JSON.parse(fs.readFileSync(new URL(p,import.meta.url)));
const old=read('../abc_curve_chart_elimination_v128/abc_quadrics.json');
const fixtures=[["100","1","1","1"],["65","2","3","4"],["1000","1","5","6"],["400","3","2","9"],["9999","12","33","2"]];
let total=0,builds=[];
for(const [x,z,u,y] of fixtures)for(const contacts of [2,3]){const b=build(source(naturalSource(old,{x,z,u,y}),old),contacts),a=general(b);total+=compare(b,a,3,'general');builds.push([a.variables,a.quadratic_rows]);}
const b=read('../abc_dihedral_contact_v152/abc_quadrics.json'),a=read('./abc_quadrics.json'),fresh=abc(b);fresh.predecessor_git_blob='e9b32774029b72b286e6d96f2f49f3d5906a6803';if(JSON.stringify(fresh)!==JSON.stringify(a))throw Error('abc replay');
console.log(JSON.stringify({general_builds:builds,general_row_evaluations:total,abc_row_evaluations:compare(b,a,10,'abc'),abc_replay:true}));
