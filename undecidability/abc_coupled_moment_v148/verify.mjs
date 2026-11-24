import fs from "node:fs";
import {build} from "./build.mjs";

function localChecks(){
  let count=0;
  for(let sv=-15;sv<=15;sv++)for(let j=0;j<=15;j++)for(let v=0;v<=15;v++){
    for(let t=0;t<=15;t++){
      if(sv!==0&&t!==-1)continue;
      const ut=sv===0?1+4*t:1-4*Math.abs(sv),cj=2*j-1;
      const a=[v,cj,ut],m=Math.min(...a);
      if(sv!==0||j===0) {
        if(m>=0||a.filter(x=>x===m).length!==1)throw Error("negative minimum");
      }else if(v===0){
        if(m!==0||a.filter(x=>x===m).length!==1)throw Error("zero minimum");
      }else if(m<=0)throw Error("positive condition");
      count++;
    }
  }
  // Include nonunit s, for which v(s+s^-1) is forced and is negative.
  for(let sv=-20;sv<=20;sv++)if(sv!==0)for(let j=0;j<=20;j++)for(let v=0;v<=20;v++){
     if(!(1-4*Math.abs(sv)<Math.min(v,2*j-1)))throw Error("unit gate");
     count++;
  }
  return {momentProfiles:count};
}

const source=JSON.parse(fs.readFileSync(new URL("../abc_scaled_unit_v145/abc_quadrics.json",import.meta.url),"utf8"));
const stored=fs.readFileSync(new URL("./abc_quadrics.json",import.meta.url),"utf8");
if(JSON.stringify(build(source),null,2)+"\n"!==stored)throw Error("table replay");
console.log(JSON.stringify({...localChecks(),variables:290,quadratic_rows:239,retainedRows:231}));
