"use strict";
// Finite overapproximations of the universally proved valuation profiles in README.md.
function verifyValuations(){
 const A=(ok,msg)=>{if(!ok)throw Error(msg||"valuation assertion")};
 const uniq=(p)=>[...new Map(p.map(x=>[x.join(","),x])).values()];
 let unit=[],actual=[];
 for(let d=0;d<=8;d++)for(let e=0;e<=8;e++)for(let s of [-1,1])for(let t of [-1,1]){
  const J=2*(s*d+t*e),err=d!==e?[-Math.max(d,e)]:[...Array.from({length:9+d},(_,i)=>i-d),Infinity];
  for(let C of err){if((J%4+4)%4===2)A(C<0&&4*C<=-Math.abs(J)-2,"unit mismatch");if(C>0&&J>0)A(d===e&&d>0&&s===1&&t===1&&J===4*d,"formal");unit.push([C,J])}
 }
 unit=uniq(unit);
 for(let e=0;e<=4;e++){
 for(let d=1;d<=8;d++){
  for(let J of [4*(d+e),4*e,-4*d])for(let C of [...Array.from({length:19},(_,i)=>i-10),Infinity])actual.push([C,J]);
  for(let J of [2*e+2*d,2*e-2*d])for(let C of e<d?[e-d]:[...Array.from({length:9},(_,i)=>i),Infinity])actual.push([C,J]);
 }
 for(let C of [...Array.from({length:9},(_,i)=>i),Infinity])actual.push([C,2*e])
 }
 actual=uniq(actual);
 for(let [C,J] of actual)if(J<0&&(J%4+4)%4===2)A(C===J/2,"actual valuation identity");
 const v=(C,J,I,K,c)=>[c+4*C,4*c+2*J,3*c+4*I,2*c+K];
 let nunit=0,nforeign=0,nselected=0;
 for(let mu=1;mu<=31;mu+=2)for(let [C,J] of unit)for(let [I,K] of unit){let vs=v(C,J,I,K,-mu),m=Math.min(...vs);
 if(m<0)A(vs.filter(x=>x===m).length===1,"unit tie");
 if(2*m>-mu){A(8*C>mu&&4*J>7*mu&&8*I>5*mu&&2*K>3*mu,"threshold");A(J%4===0&&K%4===0&&J>0&&K>0,"formal products")}
 nunit++;
 }
 for(let j=1;j<=15;j+=2)for(let [C,J] of actual)for(let [I,K] of actual){let vs=v(C,J,I,K,j),m=Math.min(...vs);if(m<0)A(vs.filter(x=>x===m).length===1,"foreign tie");else A(m>0,"foreign unit");nforeign++}
 const selected=unit.filter(([C,J])=>J!==2||C===-1);
 for(let [C,J] of selected)for(let [I,K] of selected){let vs=v(C,J,I,K,-1),m=Math.min(...vs);if(m<0)A(vs.filter(x=>x===m).length===1,"selected tie");else A(m>0,"selected unit");nselected++}
 for(let mu=1;mu<=20001;mu+=2){let dp=1+Math.floor(7*mu/16),dm=1+Math.floor(3*mu/8),e=2+Math.floor(mu/8)+Math.floor(7*mu/16);A(Math.min(4*dp,4*dm,Math.floor(mu/8)+1+dp,Math.floor(5*mu/8)+1+dm)>=e&&e>=2,"precision")}
 A(347n*997n-13n*501n*50n===20309n,"margin");
 return {unit_input_profiles:nunit,foreign_profiles:nforeign,selected_profiles:nselected,depth_checks:10001,height_margin:"20309/199400"}
}
console.log(verifyValuations());
