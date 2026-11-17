#!/usr/bin/env python3
"""Standard-library check of source binding and the exact stored supports."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import itertools,json,argparse
ROOT=Path(__file__).resolve().parent
SOURCE='304f94843c1a4ac94fcd5f1295fee8b532e7f0424e638314d892c556e2fbfdf9'
BASE={77:(1,0),78:(-1,0),90:(0,1),91:(0,-1),92:(-1,-2)}
DELETED=set(range(152,182))|{21,22,25,26,27,28,52,53,56,57,58,59}

def parse(row):
    p=defaultdict(Q)
    for t in row['terms']:p[t['parameterPower'],tuple(t['monomial'])]+=Q(t['coefficient'])
    return {k:c for k,c in p.items()if c}

def plus(*polys):
    p=defaultdict(Q)
    for a in polys:
        for m,c in a.items():p[m]+=c
    return {m:c for m,c in p.items()if c}

def scale(p,c):return {m:c*d for m,d in p.items()if c*d}
def mul(a,b):
    p=defaultdict(Q)
    for (m,e),c in a.items():
        for (n,f),d in b.items():p[tuple(sorted(m+n)),tuple(x+y for x,y in zip(e,f))]+=c*d
    return {m:c for m,c in p.items()if c}
def con(a):return {((),(0,0)):Q(a)}if a else{}
def var(i):return {((i,),(0,0)):Q(1)}
def unit(e):return {((),tuple(e)):Q(1)}
def fp(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def fs(a,c):return scale(a[0],c),scale(a[1],c)
def fm(a,b):return plus(mul(a[0],b[0]),scale(mul(a[1],b[1]),2)),plus(mul(a[0],b[1]),mul(a[1],b[0]))
def fv(i):return var(i),var(i+1)
def support(f):return set(f[0])|set(f[1])
def row_support(row):return {(tuple(m),tuple(e))for m,e in row['terms']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'model_certificate.json');args=ap.parse_args()
    raw=(ROOT/'source195.json').read_bytes();assert sha256(raw).hexdigest()==SOURCE
    original=json.loads(raw);changed=json.loads((ROOT/'reversed_reference_basis.json').read_text())
    mapping=json.loads((ROOT/'reference-row-map.json').read_text())
    names=mapping['names'];matrix=[[Q(c)for c in row]for row in mapping['matrix']]
    elimination=[row[:]for row in matrix];det=Q(1)
    for j in range(8):
        k=next(k for k in range(j,8)if elimination[k][j])
        if k!=j:elimination[j],elimination[k]=elimination[k],elimination[j];det=-det
        pivot=elimination[j][j];det*=pivot
        for k in range(j+1,8):
            a=elimination[k][j]/pivot
            elimination[k]=[c-a*d for c,d in zip(elimination[k],elimination[j])]
    assert det==Q(mapping['determinant'])and det
    old={r['name']:parse(r)for r in original['residuals']}
    for row in changed['residuals']:
        name=row['name'];expected=old[name]
        if name in names:
            j=names.index(name);expected=plus(*[scale(old[n],matrix[j][k])for k,n in enumerate(names)])
        assert parse(row)==expected
    retained={}
    for row in changed['residuals']:
        name=row['name']
        if(name.startswith('pair')or name.startswith('residue.det')and'.factor'in name or name=='inverse_vieta.unweighted.aggregate'or name.endswith('inverseWeight.definition')or name.endswith('inverseWeightSquared.definition')):continue
        acc=defaultdict(Q)
        for (p,m),c in parse(row).items():
            n=[];e=[0,0]
            for i in m:
                assert i not in DELETED
                if i in BASE:e=[a+b for a,b in zip(e,BASE[i])]
                else:n.append(i)
            acc[p,tuple(n),tuple(e)]+=c
        retained[name]={(m,e)for(p,m,e),c in acc.items()if c}
    pairs={1:(201,203,205,207,209,211),3:(213,215,217,219,221,223),4:(225,227,229,231,233,235)}
    base_new={};D=(con(11),con(-6));one=(con(1),{});u=(unit((1,0)),{})
    aggregate=plus(scale(var(2),2),scale(var(86),-2),scale(unit((1,0)),14),var(192))
    raws={}
    for role,ids in pairs.items():
        s,t,F,G,h,d=map(fv,ids)
        p=fp(fp(h,s),t)
        base_new[f'new{role}.d_piF']=support(fp(d,fs(fm(p,F),-1)))
        base_new[f'new{role}.sum']=support(fp(fp(fm(D,fp(F,G)),fs(fm(fp(s,fs(t,-1)),h),-1)),fm(t,t)))
        base_new[f'new{role}.d_Gh']=support(fp(d,fs(fm(G,h),-1)))
        base_new[f'new{role}.unit']=support(fp(fp(one,fs(fm(d,fp(s,fs(t,-1))),-1)),fm(D,fm(F,G))))
        L,L0,k={1:(29,31,1),3:(37,39,2),4:(41,43,4)}[role]
        for tag,Lv,Sv,st in [('primary',L,17,s),('alternate',L0,150,t)]:
            expr=fp(fm(fv(Lv),st),fs(fv(Sv),-k))
            if role==4:expr=fp(expr,fs(fm(u,st),-1))
            base_new[f'new{role}.ratio.{tag}']=support(expr)
        aggregate=plus(aggregate,mul(unit((1,0)),fm(h,p)[0]))
        raws['A'+str(role)]=F;raws['B'+str(role)]=G
    base_new['new.aggregate']=set(aggregate)
    certificates=[]
    for name in ['A4_B4','A1_B3','A1_A3']:
        path=ROOT/'models'/(name+'.json');raw=path.read_bytes();data=json.loads(raw)
        assert sha256((ROOT/'reversed_reference_basis.json').read_bytes()).hexdigest()==data['source_sha256']
        assert {int(i):tuple(e)for i,e in data['base_units'].items()}==BASE
        P=[(0,0)]+list(BASE.values())
        allowed={(a[0]+b[0]-c[0],a[1]+b[1]-c[1])for a,b,c in itertools.product(P,repeat=3)}-set(P)
        assert {tuple(e)for e in data['extra_unit_candidates']}==allowed and len(allowed)==32
        expected=dict(retained)|base_new
        for output,label in zip((237,239),data['helpers']):expected[f'new.square.{output}']=support(fp(fv(output),fs(fm(raws[label],raws[label]),-1)))
        for det in(0,1):
            for factor in range(5):
                output=118+16*det+2*factor
                expr=fp(one,fs(fm((unit((1,2*det)),{}),fv(output)),-1))
                if factor==4:expr=fp(expr,fm((unit((-2,4*det)),{}),fm(fv(116),fv(116))))
                expected[f'new.det{det}.factor{factor}']=support(expr)
        actual={r['name']:row_support(r)for r in data['rows']}
        assert actual==expected
        quadratic_tests={'C2':[66,[-6,0],9],'C3':[68,[-6,0],9],'C4':[70,[-6,0],9],'GL':[72,[-6,0],9]}
        raw_ids={prefix+str(role):ids[2 if prefix=='A'else 3]for role,ids in pairs.items()for prefix in('A','B')}
        quadratic_tests.update({label:[i,[0,0],1]for label,i in raw_ids.items()if label not in data['helpers']})
        linear_tests={'DH':[64,[-1,0]],'B0':[19,[-1,0]],'A2':[54,[-1,0]],'B2':[23,[-1,0]],data['helpers'][0]:[237,[0,0]],data['helpers'][1]:[239,[0,0]],'C1':[114,[-1,0]]}
        assert data['quadratic_tests']==quadratic_tests and data['linear_tests']==linear_tests
        assert data['physical_contact_weights']==['u','u*v']
        assert data['factor_output_unit_exponents']==[[1,0],[1,2]]
        assert data['common_field_row_multiplier']is True
        for key,j in data['factor_rows'].items():
            det,k=map(int,key.split(','));assert data['rows'][j]['name']==f'new.det{det}.factor{k}'
        active=set(range(1,196))-DELETED-set(BASE);active.update(range(201,241))
        assert set(data['active'])==active
        assert len(active)+len(BASE)+1==194
        assert len(expected)==134
        assert all(set(m)<=active and len(m)<=2 for terms in actual.values()for m,e in terms)
        certificates.append(dict(model=name,model_sha256=sha256(raw).hexdigest(),row_groups=len(actual),extra_unit_candidates=len(allowed),nominal_coordinates=194,status='PASS'))
    result=dict(schema='support194-source-model-check/v69',status='PASS',source_sha256=SOURCE,reference_change_rank=8,source_rows=175,scalar_aggregate='Exact real-part matching products; no imaginary cross terms',scope='Source row identities and support construction only. This does not establish a lower bound or any new polynomial.',models=certificates)
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
