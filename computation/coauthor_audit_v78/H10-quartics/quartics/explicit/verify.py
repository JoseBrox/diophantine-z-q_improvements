"""Rebuild the amplitude, coefficient table and canonical notation from the hybrid 180 rows."""
from collections import Counter,defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd,isqrt,prod
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_bytes())
def write(n,j):(ROOT/n).write_text(json.dumps(j,separators=(',',':'))+'\n')
def r(x):
    b=51*x*x+2504;return b*(b-1)*(b-2401)*(32*b+343)
def primitive(p):
    p={m:c for m,c in p.items() if c}
    gg=gcd(*p.values())
    return {m:c//gg for m,c in p.items()}
def terms(p):return [dict(monomial=list(m),coefficient=str(c)) for m,c in sorted(p.items())]
def main():
    basis=(ROOT/'source.json').read_bytes()
    assert sha256(basis).hexdigest()=='1a4621da15c17eadcf914fb3d9294bb2b0f8301b814dc6c47d636eb9af9967a0'
    model=json.loads(basis);source=model['residuals']
    primes=[23,149,263,337,631,1063,1093,1171,1439,2161,2437,2837,2851,3187,3343,3793]
    A=prod(primes)
    assert A>=149**22 and A>26*2**20
    for p in primes:
        assert all(p%i for i in range(2,isqrt(p)+1))
        assert p not in (2,3,5,7,11,13,17,37,41,2399)
        assert all(r(x)%p and (1+25*r(x))%p for x in range(p))
    assert all(r(x)%16 in (4,8,12) for x in range(16))
    assert all(r(x)%3==1 for x in range(3)) and all(r(x)%17==13 for x in range(17))
    assert 9792==64*9*17
    setup=read('fixed-map.json');U=int(setup['U']);V=A//U
    assert U*V==A
    source_by_name={row['name']:row for row in source}
    def raw_terms(name):
        return {(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in source_by_name[name]['terms']}
    assert raw_terms('inputSquare.definition')=={(0,(1,1)):1,(0,(37,)):-1}
    assert raw_terms('shared.c_unit')=={(0,()):-1,(0,(163,164)):1}
    assert raw_terms('scalar.b.definition')=={(0,(81,)):9792,(1,(81,90)):1,(1,(82,90)):-1}
    pair=raw_terms('scalar.rPair1.definition')
    product=raw_terms('scalar.four_contact_product.definition')
    assert all(e==0 and len(m)<=2 for e,m in set(pair)|set(product))
    # At c=1 the rows are polynomials of degree <=4 in t=X² after solving the pair row.
    # Their ordinary homogeneity restores general c. The product x78*x90 occurs only in its displayed term.
    assert (0,(78,90)) in product and product[0,(78,90)]==1 and all((78 not in m and 90 not in m) or m==(78,90) for e,m in product)
    assert set(m for e,m in pair)=={(37,37),(37,),(77,),()}
    for t in range(5):
        b=51*t+2504;rv=b*(b-1)*(b-2401)*(32*b+343)
        val={163:1,37:t,77:Fraction((51*t+2501)**2,4),78:rv,90:1}
        assert all(sum(a*prod(val[i] for i in m) for (e,m),a in q.items())==0 for q in (pair,product))

    size=setup['weights'];gauge=read('parameter-map.json')
    assert len(size)==len(gauge)==180 and size[0]==gauge[0]==0
    assert (gauge[77],gauge[89],gauge[162])==(1,-1,0)
    rows=[]
    for row in source:
        special=row['name']=='scalar.forced_prime.definition'
        transformed=[];physical=set()
        for term in row['terms']:
            m=tuple(term['monomial']);e=term['parameterPower'];c=int(term['coefficient'])
            physical.add(e+sum(gauge[i-1] for i in m))
            if special:
                assert (m,c,e) in (((78,90),22201,0),((),1,0),((78,),-149,1))
                c={(78,90):25,():1,(78,):-V}[m];e=0
            transformed.append((m,c,e+sum(size[i-1] for i in m)))
        assert special or len(physical)==1
        emin=min(e for m,c,e in transformed)
        p=Counter()
        for m,c,e in transformed:p[m]+=c*U**(e-emin)
        rows.append(primitive(p))
    # Elementary row changes. Rows are numbered consecutively starting at one.
    for i,j,num,den in read('operations.json'):
        assert 1<=i<=len(rows) and 1<=j<=len(rows) and i!=j and den>0
        a=Counter({m:den*v for m,v in rows[i-1].items()})
        a.update({m:num*v for m,v in rows[j-1].items()})
        rows[i-1]=primitive(a)
    p=defaultdict(int)
    for row in rows:
        for m,c in row.items():
            for n,d in row.items():p[tuple(sorted(m+n))]+=c*d
    p={m:c for m,c in p.items() if c}
    frequencies=Counter(i for m in p for i in set(m))
    order=[1]+sorted((i for i in frequencies if i!=1),key=lambda i:(-frequencies[i],i))
    assert len(order)==180 and p[(1,1,1,1)]==1
    new_index={i:j for j,i in enumerate(order,1)}
    def renamed(q):return {tuple(sorted(new_index[i] for i in m)):c for m,c in q.items()}
    rows=[renamed(row) for row in rows];p=renamed(p)
    if (ROOT/'shears.json').exists():
        from math import comb
        for i,j,c in read('shears.json'):
            assert i!=1 and j!=i and 0<=j<=180 and 2<=i<=180
            def apply(q):
                out=Counter(q)
                for m,v in q.items():
                    k=m.count(i)
                    if not k:continue
                    rest=[h for h in m if h!=i]
                    for a in range(1,k+1):out[tuple(sorted(rest+([j]*a if j else [])+[i]*(k-a)))]+=v*comb(k,a)*c**a
                return {m:v for m,v in out.items() if v}
            rows=[apply(q) for q in rows];p=apply(p)
    audit=Counter()
    for row in rows:
        for (m,c),(n,d) in combinations_with_replacement(row.items(),2):
            audit[tuple(sorted(m+n))]+=(1+(m!=n))*c*d
    assert p=={m:c for m,c in audit.items() if c} and p[(1,1,1,1)]==1
    write('permutation.json',new_index)
    write('quadrics.json',dict(variables=180,inputCoordinate=1,residuals=[dict(id=i,terms=terms(row)) for i,row in enumerate(rows,1)]))
    write('polynomial.json',dict(variables=180,inputCoordinate=1,terms=terms(p)))
    result=json.loads(subprocess.check_output([sys.executable,str(ROOT/'measure_plain_text.py'),str(ROOT/'polynomial.json'),'--output',str(ROOT/'quartic180.txt')]))
    h=max(map(abs,p.values()))
    cert=dict(physical_anchor=str(A),U=str(U),V=str(V),rows=len(rows),height=str(h),height_bits=h.bit_length(),**result)
    write('certificate.json',cert)
    print(json.dumps(cert,indent=2))
if __name__=='__main__':main()
