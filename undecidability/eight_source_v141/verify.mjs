// Independent exact prefix evaluator. This does not solve the elliptic or Pell systems.
import {source,build,old} from './build.mjs';
const fixtures=[
  {
    "variables": 1,
    "terms": [
      {
        "coefficient": "1",
        "monomial": []
      },
      {
        "coefficient": "-1",
        "monomial": [
          1
        ]
      }
    ]
  },
  {
    "variables": 2,
    "terms": [
      {
        "coefficient": "5",
        "monomial": []
      },
      {
        "coefficient": "-2",
        "monomial": [
          1
        ]
      },
      {
        "coefficient": "-4",
        "monomial": [
          2
        ]
      },
      {
        "coefficient": "1",
        "monomial": [
          1,
          1
        ]
      },
      {
        "coefficient": "1",
        "monomial": [
          2,
          2
        ]
      },
      {
        "coefficient": "7",
        "monomial": [
          1,
          1,
          2,
          2
        ]
      }
    ]
  },
  {
    "variables": 58,
    "terms": [
      {
        "coefficient": "1",
        "monomial": []
      },
      {
        "coefficient": "-1",
        "monomial": [
          1,
          1,
          1,
          1
        ]
      },
      {
        "coefficient": "1",
        "monomial": [
          58,
          58,
          58,
          58
        ]
      }
    ]
  }
];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a||1n}
function rat(a,b=1n){if(!b)throw Error("division");if(b<0n){a=-a;b=-b}let d=gcd(a,b);return [a/d,b/d]}
const add=(x,y)=>rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1]),mul=(x,y)=>rat(x[0]*y[0],x[1]*y[1]),neg=x=>[-x[0],x[1]],div=(x,y)=>rat(x[0]*y[1],x[1]*y[0]);
const equal=(x,y)=>x[0]===y[0]&&x[1]===y[1],fac=n=>{let x=1n;for(let i=2;i<=n;i++)x*=BigInt(i);return x};
function verifyPrefix(p,f,g){let s=source(p,old),a=new Map([["f",rat(f)],["g",rat(g)]]),names=s.variable_names,delta=s.source_prefix.delta,nu=p.variables,beta=BigInt(s.source_prefix.beta);
 for(const q of s.residuals){if(q.name.includes("BD_positive_f")||q.name.includes("BD_g_interval"))break;
  let x=new Set(q.terms.flatMap(t=>t.monomial.map(i=>names[i-1])).filter(n=>!a.has(n)));if(x.size!==1)throw Error(q.name+" not triangular");let u=[...x][0],constant=rat(0n),slope=rat(0n);
  for(let t of q.terms){let z=rat(BigInt(t.coefficient)),degree=0;for(let i of t.monomial){let n=names[i-1];if(n===u)degree++;else z=mul(z,a.get(n))}if(degree===0)constant=add(constant,z);else if(degree===1)slope=add(slope,z);else throw Error("nonlinear output "+q.name)}
  a.set(u,div(neg(constant),slope));
 }
 const b=1n+3n*f,B=beta*b**BigInt(delta),d=BigInt(delta+1),h=Array.from({length:nu+2},(_,i)=>B**(d**BigInt(i))),N0=B*h[nu],N1=4n*B*h[nu]**BigInt(2*delta+1),N=N0*N1;
 const sign=BigInt(p.terms.find(t=>t.monomial.length===0).coefficient)>0n?1n:-1n;
 let coeff=0n;for(let t of p.terms){let exponent=d**BigInt(nu+1),mult=fac(delta-t.monomial.length),cnt=new Map();for(const i of t.monomial){exponent-=d**BigInt(i);cnt.set(i,(cnt.get(i)||0)+1)}for(const k of cnt.values())mult*=fac(k);coeff+=sign*BigInt(t.coefficient)*mult*B**exponent}
 let geom=(N1/4n-1n)/(B-1n),K=(1n+g)**BigInt(delta)*coeff+B*geom/2n,mask=N0-1n-(b-1n)*h.slice(1,nu+1).reduce((s,x)=>s+x,0n),S=g+2n*K*N0,T=mask+(B-2n)*h[nu+1]*N0,R=(S+T+1n)*N+T+1n;
 for(const [n,v] of Object.entries({b,BD_B:B,BD_N0:N0,BD_N1:N1,n:N,n2:N*N,BD_mu:b*h[nu],BD_mask:mask,BD_coeff:coeff,BD_geom:geom,BD_K:K,BD_S:S,BD_T:T,BD_R:R,r:(N-1n)*R}))if(!equal(a.get(n),rat(v)))throw Error("prefix mismatch "+n);
 if((N-1n)*R%3n||N*N<4n*b||N*N<16n)throw Error("core domain");
}
let fixtureCount=0;for(let p of fixtures.slice(0,2))for(const f of [1n,2n,5n])for(const g of [1n,3n]){verifyPrefix(p,f,g);fixtureCount++}
for(const p of fixtures){const s=source(p,old);for(const contacts of [2,3]){const t=build(s,contacts);if(t.variables-s.variable_names.length!== (contacts===2?423:443)||t.quadratic_rows-s.residuals.length!==(contacts===2?372:390)||new Set(t.residuals.flatMap(q=>q.terms.flatMap(t=>t.monomial))).size!==t.variables)throw Error("count/support");if(t.integer_certificates!==8)throw Error("certificate count")}}
if(!source({variables:1,terms:[]},old).yes||source({variables:1,terms:[{coefficient:"-2",monomial:[]}]},old).yes)throw Error("trivial case");
console.log(JSON.stringify({prefix_fixtures:fixtureCount,table_builds:6,source_bound:2011,quartic_bounds:[2434,2454]}));
