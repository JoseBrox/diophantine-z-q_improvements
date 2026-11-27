import fs from 'node:fs';

function verify(csv){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const mod=(x,p)=>(x%p+p)%p;
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a};
 function pow(x,n,p){x=mod(x,p);let v=1n;while(n){if(n&1n)v=v*x%p;x=x*x%p;n>>=1n}return v;}
 const inv=(x,p)=>{assert(mod(x,p)!==0n,"nonunit");return pow(x,p-2n,p)};
 function pell(a,n,m){let X=1n,Y=0n,U=mod(a,m),V=1n,D=mod(a*a-1n,m);while(n){if(n&1n)[X,Y]=[mod(X*U+D*Y*V,m),mod(X*V+Y*U,m)];[U,V]=[mod(U*U+D*V*V,m),mod(2n*U*V,m)];n>>=1n}return[X,Y]}
 const primes=[[13n,2n],[17n,3n],[97n,5n],[193n,5n],[257n,3n],[769n,11n],[12289n,11n],[65537n,3n],[786433n,10n],[3221225473n,5n],[206158430209n,22n],[6597069766657n,5n]];
 const factors=new Map();
 for(const [p,a] of primes){
  let odd=p-1n,k=0n;while(odd%2n===0n){odd/=2n;k++}
  assert(odd===1n||odd===3n,"factorization");
  assert(k<=41n,"fixed exponent");
  assert(pow(a,p-1n,p)===1n,"Fermat certificate");
  for(const q of odd===3n?[2n,3n]:[2n])assert(gcd(pow(a,(p-1n)/q,p)-1n,p)===1n,"order certificate");
  factors.set(p,{odd,k});
 }
 const rows=csv.trim().split("\n").slice(1).map(x=>x.split(",").map(BigInt));
 let seen=new Set(),profileCount=0,liftCount=0,periodCount=0,baseInvariance=0;
 for(const [t,bc,p,u,sg,m,V,sa,sd,l,ratio] of rows){
  const {odd,k}=factors.get(p);
  assert(bc===-1n||[0n,1n,2n].includes(bc),"beta class");
  assert(bc!==-1n||odd===1n,"wildcard");
  assert([1n,-1n].includes(sg)&&[1n,3n].includes(m)&&0n<=l&&l<odd,"row choices");
  for(const be of bc===-1n?[0n,1n,2n]:[bc]){
   assert(!seen.has(t+":"+be),"duplicate profile");seen.add(t+":"+be);
   // Use actual positive beta exponent representative. E_N is the
   // packed base exponent, not an approximation or a recurrence index.
   const z=be+3n,L=2n*z+4n*u,E_N=2n+10n*(1n<<45n)*L;
   const N=pow(2n,E_N,p),M=N*N%p,b=pow(4n,u,p),U=mod(2n*M*inv(b,p),p);
   assert(N!==1n&&U!==p-1n&&V!==0n,"nondegenerate radix");
   for(const add of [3n,27n,999n]){
    assert(pow(2n,E_N+20n*(1n<<45n)*add,p)===N,"beta invariance");baseInvariance++;
   }
   const a=mod((U+1n)*V,p),P=mod(1n+2n*U*V*V,p),A=mod(P*P-1n,p);
   assert(mod(2n*a,p)===mod(sg,p),"a=sign/2");
   assert(A!==0n&&mod(sa*sa,p)===A,"small split");
   const pair6=pell(a,6n,p);assert(pair6[0]===1n&&pair6[1]===0n,"a-unit sixth power");periodCount++;
   const [F,Yq]=pell(a,4n*m,p);
   assert(m===1n?F===mod(-inv(2n,p),p)&&Yq===mod(-sg,p):F===1n&&Yq===0n,"second norm residue");
   const G=mod(a+F*F*(2n-a),p),D=mod(G*G-1n,p);
   assert(F!==0n&&D!==0n&&mod(sd*sd,p)===D,"third split");
   const H=mod(pow(P+sa,1n+(1n<<k)*l,p)*inv(2n*sa*M*M,p),p);
   const J=mod((G+sd)*inv(2n*sd*F,p),p);
   assert(H!==0n&&J!==0n&&mod(J*inv(H,p),p)===ratio,"normalized ordinate ratio");
   assert(pow(ratio,1n<<t,p)===p-1n&&pow(ratio,1n<<(t+1n),p)===1n,"exact 2-power order");
   profileCount++;
   // Independent finite lift verification. The representative r is
   // divisible by every possible p-1 and has the required parity.
   // Use actual coefficients modulo p^2 and compute F with the reduced
   // exponent 4 B m modulo 6p, as proved in the note.
   const R=3n*(1n<<41n),pp=p*p,Mp=pow(2n,2n*E_N,pp);
   const bp=pow(4n,u,pp);
   let got=0;
   for(let i=1n;got<4;i++){
    const r=R*i,B=2n*r+1n;
    if(r%p===0n||B%p===0n)continue;
    const der=mod(m===3n?(-2n*sg*(B-1n))*inv(3n,p):(sg===1n?(70n*B+11n):(7n-118n*B))*inv(12n,p),p);
    if(!der)continue;
    // division by b is 2-power division modulo odd p^2, which is
    // implemented by exponent subtraction, not a field inverse mod p^2.
    const Up=pow(2n,B+2n*E_N-2n*u,pp);
    const slope=mod((Up+1n)*r*Mp,p);
    assert(slope!==0n,"s lift");
    const s0=mod(V*inv(r*M,p),p);
    const v=s=>{
      const aa=mod((Up+1n)*r*s*Mp,pp);
      const [dd,c]=pell(aa,B,pp);
      assert(c%p===1n,"c residue");
      const q=mod(4n*B*m,6n*p);
      const FF=pell(aa,q,pp)[0];
      const GG=mod(aa+FF*FF*(c+1n-aa),pp);
      assert(GG%p===G,"G residue");
      const [X,Y]=pell(GG,p-1n,pp);
      assert(Y%p===0n&&X%p===1n,"third local order");
      return{GG,Y};
    };
    const x=v(s0),y=v(s0+p);
    assert(mod(y.GG-x.GG,pp)===p*mod(der*slope,p),"G derivative check");
    assert(x.Y!==y.Y&&(x.Y!==0n||y.Y!==0n),"non-Wieferich lift");
    assert(mod(y.Y-x.Y,pp)===p*mod(-der*slope*inv(D,p),p),"Y derivative check");
    got++;liftCount++;
   }
  }
 }
 assert(rows.length===106&&seen.size===120,"coverage census");
 for(let t=1;t<=40;t++)for(let z=0;z<3;z++)assert(seen.has(t+":"+z),"missing exponent/beta class");
 return {literal_rows:rows.length,prime_certificates:primes.length,covered_2adic_exponents:[1,40],profiles:profileCount,beta_invariance_checks:baseInvariance,sixth_power_checks:periodCount,mod_p2_lifts:liftCount,maximum_prime:"6597069766657",scope:"Exact modular certificates for the global existence theorem. Not a numerical full-source rational witness."};
}

console.log(JSON.stringify(verify(fs.readFileSync(new URL('./residue_certificates.csv',import.meta.url),'utf8')),null,2));
