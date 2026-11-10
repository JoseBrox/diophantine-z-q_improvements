from fractions import Fraction as F
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import json

ROOT=Path('/workspace/scratch/191d4e871efa/repo/computation/quartic')

def canonical(p):
    p={k:F(v) for k,v in p.items() if v}
    den=lcm(*(v.denominator for v in p.values()))
    p={k:int(v*den) for k,v in p.items()}
    g=reduce(gcd,p.values())
    if p[min(p)]<0:g=-g
    return {k:v//g for k,v in p.items()}

def polynomial(terms):
    d={}
    for c,m in terms:
        k=(0,tuple(sorted(m)))
        d[k]=d.get(k,0)+c
    return canonical(d)

def rows(data):
    ids={c['id']:c['sourceId'] for c in data['coordinates']}
    return {r['name']:canonical({(t['parameterPower'],tuple(sorted(ids[i] for i in t['monomial']))):F(t['coefficient']) for t in r['terms']}) for r in data['residuals']}

theta=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
coeff=[F(1)]
for t in theta:
    z=(1-t)**2
    q=[F(0)]*(len(coeff)+1)
    for i,c in enumerate(coeff):q[i]-=z*c;q[i+1]+=c
    coeff=q
e1,e2,e3,e4,e5=-coeff[4],coeff[3],-coeff[2],coeff[1],-coeff[0]
assert e5 and coeff[0]==F(-82429855236,7878870169)
reports=[]
for oldcount,newcount in [(228,226),(265,262)]:
    old=json.loads((ROOT/f'family{oldcount}_v19/quadratic-family{oldcount}-v19.json').read_text())
    new=json.loads((ROOT/f'family{newcount}_v21/quadratic-family{newcount}-v21.json').read_text())
    op,np=rows(old),rows(new)
    blocks=[(346,347,20000,348,352,360),(392,393,20020,394,400,408)]
    if newcount==262:blocks.append((50004,50005,50018,50006,50007,50008))
    changed=set()
    for j,(r,u,v,P,q,s) in enumerate(blocks):
        name=f'reflected.detector{j}.'
        expected_old_P=polynomial([(1,[P]),(-1,[u,v]),(e1,[r,v]),(-e2,[v]),(e3,[u]),(-e4,[r]),(e5,[])])
        assert op[name+'contactPolynomial.definition']==expected_old_P
        assert op[name+'deltaSixthPower.definition']==polynomial([(1,[v]),(-1,[r,u])])
        assert op[name+'weight.definition']==polynomial([(1,[P]),(1,[q,P]),(-1,[u,v])])
        qinverse=polynomial([(1,[q,s]),(-1,[])])
        assert qinverse in op.values() and qinverse in np.values()
        usquare=polynomial([(1,[u]),(-1,[r,r])])
        assert usquare in op.values() and usquare in np.values()
        old_uses={k for k,p in op.items() if any(v in mon for _,mon in p)}
        assert old_uses=={name+'contactPolynomial.definition',name+'deltaSixthPower.definition',name+'weight.definition'}
        assert {k for k,p in op.items() if any(P in mon for _,mon in p)}=={name+'contactPolynomial.definition',name+'weight.definition'}
        assert np[f'inverseContact.detector{j}.quadraticOutput.definition']==polynomial([(1,[v]),(-1,[r,u]),(e1,[u]),(e1,[s,u]),(-e2,[r]),(-e2,[s,r])])
        assert np[f'inverseContact.detector{j}.normalization']==polynomial([(1,[u,v]),(-e3,[u]),(-e3,[s,u]),(e4,[r]),(e4,[s,r]),(-e5,[]),(-e5,[s])])
        changed|=old_uses
    for name,p in op.items():
        if name not in changed:assert np[name]==p,name
    removed={b[3] for b in blocks}
    assert {c['sourceId'] for c in new['coordinates']}=={c['sourceId'] for c in old['coordinates']}-removed
    assert len(new['coordinates'])==newcount
    assert len(new['residuals'])==len(old['residuals'])-len(blocks)
    assert all(len(mon)<=2 for p in np.values() for _,mon in p)
    # Independent support and fixed-parameter height profile from the exact table.
    expanded=json.loads((ROOT/f'family{newcount}_v21/polynomial-family{newcount}-v21.json').read_text())
    profiles={}
    for t in expanded['terms']:
        m=tuple(t['monomial']);a=t['parameterPower'];c=int(t['coefficient'])
        profiles.setdefault(m,{})[a]=c
    mixed=[(m,p) for m,p in profiles.items() if len(p)>1]
    assert len(mixed)==1 and mixed[0][1]=={0:1,2:1}
    assert len(profiles)=={226:2835,262:3494}[newcount]
    reports.append({'old_variables':oldcount,'new_variables':newcount,'detectors':len(blocks),'quadratic_rows':len(new['residuals']),'ordinary_monomials':len(profiles),'unchanged_rows_verified':len(op)-len(changed),'removed_source_coordinates':sorted(removed),'all_repurposed_output_uses_accounted_for':True})
out={'status':'PASS','P5_constant':str(coeff[0]),'coefficient_comparisons':'Exact primitive rational-row equality, after recovering persistent source IDs','families':reports,'zero_set_proof':'u=r²; substitute v to obtain r^5-(1+s1)*(r^5-P5(r))=0. With q*s1=1 this is q*P5(r)=r^5-P5(r). P5=0 forces r=0, contradicting P5(0) nonzero. r=0 gives u=v=0,q=s1=-1.'}
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
