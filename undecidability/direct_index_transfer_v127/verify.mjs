import assert from "node:assert/strict";
import fs from "node:fs";
function ledger(c){const b=21n,n=2n*b,m=n+1n,l=c===2n?3n:5n,N0=4n**b,N=N0*2n**c,H=m+l*(n+2n),B=H*(8n*b+2n*c*N0)+(m>l?m:l);const old=2n*(N*(N+1n)*(2n*N+1n)/6n+(B+1n)*N*(N+1n)/2n+N*N);const k=N*(1n+N0+B);const bits=x=>BigInt(x.toString(2).length);let exp=bits(k);if(k>=2n**exp)throw Error();return {pole_blocks:String(c),point_blocks:String(b),point_rank:String(N0),rank:String(N),point_tags:String(m),terminal_tags:String(l),scale_exponent:String(H),separator_degree_multiplier:String(B),supplied_guarded_multiplier:String(old),whole_guard_multiplier:String(k),whole_guard_strict_power_of_2:String(exp),full_eleven_branch_multiplier:String(11n*k),full_eleven_branch_strict_power_of_2:String(bits(11n*k))}}
const rows=[ledger(2n),ledger(3n)];assert.deepEqual(rows,JSON.parse(fs.readFileSync(new URL("degree_ledger.json",import.meta.url),"utf8")));
assert.equal(rows[0].whole_guard_strict_power_of_2,"96");assert.equal(rows[1].whole_guard_strict_power_of_2,"98");
for(let D=1;D<=2000;D++){let L=Math.floor(D/2)+1;assert(2*L-D>=1);let r=1;const floorLog=(x,p)=>{let k=0;while(x>=p){x=Math.floor(x/p);k++;}return k;};while(4*r-floorLog(4*r+1,3)<L)r++;assert(r<=Math.ceil(L/3));}
console.log(rows);
