// Exact coefficient and census check for the single-cover criterion.
const gcd=(a,b)=>{while(b)[a,b]=[b,a%b];return a<0n?-a:a;};
const R=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let g=gcd(a,b);if(b<0n)g=-g;return[a/g,b/g];};
const mul=(a,b)=>R(a[0]*b[0],a[1]*b[1]);
const sub=(a,b)=>R(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const div=(a,b)=>R(a[0]*b[1],a[1]*b[0]);
const add=(a,b)=>R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const out=a=>a.map(String).join("/");
function check(){
 const rows=[];
 for(const v of [[201,200,4,10,2,88922601,46027474],
                 [16,15,4,8,5,256,135],
                 [121,100,6,12,5,13484361,6781360]]){
  const[kn,kd,e,d,m,qn,qd]=v,k=R(kn,kd);
  const epsilon=sub(R(d),mul(k,R(d/2+2)));
  const C=add(div(mul(k,R(3*d/2+1)),epsilon),R(2));
  const alpha=sub(div(R(e),k),R(3)),gamma=sub(div(R(8),k),R(6));
  const q=div(C,mul(R(m),mul(alpha,gamma)));
  if(epsilon[0]<=0n||alpha[0]<=0n||gamma[0]<=0n||q[0]>=2n*q[1]||out(q)!==out(R(qn,qd)))throw Error("height coefficient mismatch");
  rows.push({kappa:out(k),e,d,m,exponent:d*m,epsilon:out(epsilon),C:out(C),alpha:out(alpha),gamma:out(gamma),soundness_coefficient:out(q),less_than_two:true});
 }
 return{status:"PASS",rows,point_algebra_rank:4**3,single_square_rank:4**3*2,total_variables_under_realization:1+6+1+1,actual_realization_proved:false};
}

console.log(JSON.stringify(check(),null,2));
