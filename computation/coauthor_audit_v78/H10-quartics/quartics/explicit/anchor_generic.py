"""Anchor a compatible, independently validated three-detector quadratic family.

python anchor_generic.py SOURCE.json --sha256 EXPECTED --out NEW_DIRECTORY
For an archived optimized representation, also give --preset PACKAGE_DIRECTORY.
Uses Python's standard library. The source-specific gate and height proof is separate.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb, gcd, prod
from pathlib import Path
import json
import subprocess
import sys

PRIMES = (23,149,263,337,631,1063,1093,1171,1439,2161,2437,2837,2851,3187,3343,3793)
FORCED = 'scalar.forced_prime.definition'
def load(path): return json.loads(path.read_bytes())
def save(path,value): path.write_text(json.dumps(value,separators=(',',':'))+'\n')
def primitive(p):
    p={m:c for m,c in p.items() if c}
    unit=gcd(*p.values())
    return {m:c//unit for m,c in p.items()}
def records(p): return [{'monomial':list(m),'coefficient':str(c)} for m,c in sorted(p.items())]
def square_sum(rows):
    result=Counter()
    for row in rows:
        for (m,c),(n,d) in combinations_with_replacement(row.items(),2):
            result[tuple(sorted(m+n))]+=(1+(m!=n))*c*d
    return {m:c for m,c in result.items() if c}
def shear(p,i,j,c):
    out=Counter(p)
    for m,v in p.items():
        n=m.count(i)
        if not n: continue
        rest=[k for k in m if k!=i]
        for a in range(1,n+1):
            output=rest+[i]*(n-a)+([j]*a if j else [])
            out[tuple(sorted(output))]+=v*comb(n,a)*c**a
    return {m:c for m,c in out.items() if c}
def certify_parameter(source,forced_ids):
    """Solve the monomial-weight equalities by exact sparse elimination."""
    n=source['variables']; basis={}
    def add(eq,rhs):
        q={i:Fraction(x) for i,x in eq.items() if x}; rhs=Fraction(rhs)
        while q:
            i=min(q); pivot=q[i]
            if i not in basis:
                basis[i]=({j:c/pivot for j,c in q.items()},rhs/pivot);return
            vect,v=basis[i];rhs-=pivot*v
            for j,c in vect.items():
                q[j]=q.get(j,0)-pivot*c
                if not q[j]:del q[j]
        if rhs:raise ValueError('The non-scalar parameter does not admit the required common gauge.')
    add({1:1},0)
    for i,e in forced_ids: add({i:1},e)
    for row in source['residuals']:
        if row['name']==FORCED:continue
        first,*rest=row['terms']
        for t in rest:
            a=Counter(t['monomial']);a.subtract(first['monomial'])
            add(a,first['parameterPower']-t['parameterPower'])
    result=[Fraction(0)]*(n+1)
    for i,(vec,rhs) in sorted(basis.items(),reverse=True):
        result[i]=rhs-sum(c*result[j] for j,c in vec.items() if j!=i)
    if any(x.denominator!=1 for x in result):raise ValueError('No integral gauge was recovered with zero free weights.')
    return list(map(int,result[1:]))
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('source',type=Path);a.add_argument('--sha256',required=True)
    a.add_argument('--out',type=Path,required=True);a.add_argument('--preset',type=Path)
    args=a.parse_args()
    raw=args.source.read_bytes(); actual=sha256(raw).hexdigest()
    if actual!=args.sha256:raise ValueError(f'Source hash mismatch: {actual}')
    data=json.loads(raw);n=data['variables']
    roles={x['source_id']:x['id'] for x in data['coordinates']}
    i,j,cunit=[roles[k] for k in (101,113,400)]
    target=next(r for r in data['residuals'] if r['name']==FORCED)
    shape={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in target['terms']}
    mixed=tuple(sorted((i,j)))
    if shape not in [{(0,mixed):22201,(1,(i,)):-149,(0,m):1} for m in ((),(cunit,cunit))]:
        raise ValueError('The scalar row is outside the supported physical presentations.')
    gauge=certify_parameter(data,[(i,1),(j,-1),(cunit,0)])
    A=prod(PRIMES)
    assert A>149**22
    for p in PRIMES:
        for x in range(p):
            b=51*x*x+2504;r=b*(b-1)*(b-2401)*(32*b+343)
            assert r%p and (1+25*r)%p
    out=args.out;out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise ValueError('Output directory must be empty.')
    if args.preset:
        preset=args.preset
        if sha256((preset/'source.json').read_bytes()).hexdigest()!=actual:raise ValueError('Preset source hash mismatch.')
        choices=load(preset/'fixed-map.json');U=int(choices['U']);weights=choices['weights']
        operations=load(preset/'operations.json');shears=load(preset/'shears.json')
    else:
        U=1;weights=[0]*n;operations=[];shears=[]
    V=A//U
    assert A==U*V and len(weights)==n and weights[0]==0
    rows=[]
    for row in data['residuals']:
        items=[]
        for t in row['terms']:
            m=tuple(t['monomial']);e=t['parameterPower'];z=int(t['coefficient'])
            if row['name']==FORCED:
                z=(25 if m==mixed else -V if m==(i,) else 1);e=0
            items.append((m,z,e+sum(weights[k-1] for k in m)))
        emin=min(e for m,z,e in items);q=Counter()
        for m,z,e in items:q[m]+=z*U**(e-emin)
        rows.append(primitive(q))
    for i,j,b,d in operations:
        assert i!=j and d>0
        q=Counter({m:d*z for m,z in rows[i-1].items()});q.update({m:b*z for m,z in rows[j-1].items()})
        rows[i-1]=primitive(q)
    poly=square_sum(rows)
    freq=Counter(i for m in poly for i in set(m))
    order=[1]+sorted((i for i in freq if i!=1),key=lambda i:(-freq[i],i))
    index={i:k for k,i in enumerate(order,1)}
    def rename(p):return {tuple(sorted(index[i] for i in m)):z for m,z in p.items()}
    rows=list(map(rename,rows));poly=rename(poly)
    for i,j,z in shears:
        assert 1<i<=n and 0<=j<=n and i!=j
        rows=[shear(q,i,j,z) for q in rows];poly=shear(poly,i,j,z)
    assert square_sum(rows)==poly and max(map(len,poly))==4
    save(out/'parameter-map.json',gauge)
    save(out/'quadrics.json',dict(variables=n,inputCoordinate=1,residuals=[dict(id=k,terms=records(q)) for k,q in enumerate(rows,1)]))
    save(out/'polynomial.json',dict(variables=n,inputCoordinate=1,terms=records(poly)))
    tool=Path(__file__).resolve().parent/'measure_plain_text.py'
    cmd=[sys.executable,str(tool),str(out/'polynomial.json'),'--output',str(out/f'quartic{n}.txt')]
    proc=subprocess.run(cmd,capture_output=True,text=True)
    if proc.returncode not in (0,1) or not proc.stdout:raise ValueError(proc.stderr)
    receipt=json.loads(proc.stdout);h=max(map(abs,poly.values()))
    receipt.update(source_sha256=actual,physical_anchor=str(A),U=str(U),V=str(V),rows=len(rows),height=str(h),height_bits=h.bit_length())
    save(out/'certificate.json',receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
