import assert from 'node:assert/strict';
import fs from 'node:fs';
import {naturalSource,source,build,old} from './build.mjs';
import * as parent from '../packed_quadrics_v142/build.mjs';
let completion=0,descent=0;
for(let a=6n;a<=120n;a+=6n){
 let u=0n,v=1n;
 for(let j=0n;j<a-1n;j++)[u,v]=[v,(a+1n)*v-u];
 assert.equal(u%(a-1n),0n);
 assert.equal(u%2n,1n);
 assert.equal(v*v-(a+1n)*u*v+u*u,1n);
 completion++;
}
for(let a=3n;a<=20n;a++){
 let seen=new Set(['0,1']);let x=1n,y=a;
 while(x<=200n){seen.add(x+','+y);[x,y]=[y,a*y-x]}
 for(let u=1n;u<=200n;u++)for(let v=u;v<=200n;v++)if(u*u-a*u*v+v*v===1n){
  assert(seen.has(u+','+v));descent++;
 }
}
assert.equal(11n*11n-2n*6n*6n,49n);
const p={x:'100',z:'1',u:'1',y:'1'};
let replays=0;
for(const [api,path] of [[{naturalSource,source,build,old},'./'],[parent,'../packed_quadrics_v142/']]){
 const src=api.source(api.naturalSource(api.old,p),api.old);
 for(const c of [2,3]){
  const q=api.build(src,c);
  const file=c===2?'general_fixture_quadrics.json':'specified_fixture_quadrics.json';
  assert.equal(JSON.stringify(q,null,2)+'\n',fs.readFileSync(new URL(path+file,import.meta.url),'utf8'));
  replays++;
 }
}
console.log(JSON.stringify({completion,descent,replays}));
