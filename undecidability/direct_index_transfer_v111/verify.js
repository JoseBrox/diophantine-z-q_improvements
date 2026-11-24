const verify=function verify(){
  const assert=x=>{if(!x)throw Error("failed")};
  const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
  const theta=[[0n,1n],[-1n,2n],[-1n,1n],[1n,2399n],[-32n,407n]];
  const contacts=[2n,4n].flatMap(s=>theta.map(([a,b])=>{const n=s*b+a,g=gcd(n,b);return [(n/g).toString(),(b/g).toString()]}));
  assert(new Set(contacts.map(t=>t.join("/"))).size===10);
  assert(contacts.every(([n,d])=>BigInt(n)+BigInt(d)!==0n));
  // verify local signed valuations, including extraction from strict pole inequality
  let cases=0,negative=0,active=0;
  for(let nu=-41;nu<=41;nu+=2)for(let c=-100;c<=100;c++){
    const dd=Math.max(2*c,-nu), w=Math.min(0,2*dd-nu);
    if(nu<0){assert(2*dd-nu>0);negative++;}
    if(nu>0 && 2*w>-nu){assert(dd>nu/4&&c>0);active++;}
    cases++;
  }
  for(let r=1;r<=100;r++)assert(3n**BigInt(2*r)>BigInt(4*r+1));
  const e0=[112,10201];assert(e0[0]<e0[1]&&gcd(BigInt(e0[0]),BigInt(e0[1]))===1n);
  assert(112===7*16&&10201===101*101&&101%2===1);
  const result=[];
  for(const k of [11,10])for(const c of [2,3]){
    const N=2*(2*k+1)+1+2*c+1;
    const rank=2n**BigInt(2*(2*k+1)+c);
    const r=k+1, ar=(r-1)*2**(r-1), Kr=18+ar**2+2*r*2**(r-1);
    result.push({k,contact_arguments:c,N,rank:rank.toString(),generators:2*(2*k+1)+c,explicit_sum_constant:Kr});
  }
  assert(result.map(x=>x.N).join()==="52,54,48,50");
  return {status:"PASS",contacts,pole_limit:e0,valuation_cases:cases,negative,active,tail_cases:100,results:result,scope:"finite algebraic and valuation checks; not verification of arithmetic premises"};
};
const fs=require('fs');
const expected=JSON.parse(fs.readFileSync(__dirname+'/certificate.json','utf8'));
const out=verify();
if(JSON.stringify(out)!==JSON.stringify(expected))throw Error('certificate mismatch');
console.log(JSON.stringify(out,null,2));
