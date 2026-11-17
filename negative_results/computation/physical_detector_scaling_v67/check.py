#!/usr/bin/env python3
"""Exact physical-contact support and obstruction checks; standard library only."""
import argparse,hashlib,json
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
def plus(*ps):
    out=defaultdict(int)
    for p in ps:
        for k,c in p.items():out[k]+=c
    return {k:c for k,c in out.items() if c}
def mul(p,q):
    out=defaultdict(int)
    for (m,e),c in p.items():
        for (n,f),d in q.items():out[tuple(sorted(m+n)),tuple(a+b for a,b in zip(e,f))]+=c*d
    return {k:c for k,c in out.items() if c}
def scale(p,c):return {k:c*v for k,v in p.items() if c*v}
def atom(name,e=(0,0),c=1):return {((name,),e):c}
def shift(p,e):return {(m,tuple(a+b for a,b in zip(f,e))):c for (m,f),c in p.items()}
def fsquare(z):return plus(mul(z[0],z[0]),scale(mul(z[1],z[1]),2)),scale(mul(z[0],z[1]),2)
def fshift(z,e):return shift(z[0],e),shift(z[1],e)
def fplus(*zs):return tuple(plus(*(z[d] for z in zs)) for d in range(2))
def factors():
    one=({((),(0,0)):1},{})
    J=(atom('j0',(-3,0)),atom('j1',(-3,0)))
    K=(atom('k0',(-3,0)),atom('k1',(-3,0)))
    DH=(atom('h0',(-1,0)),atom('h1',(-1,0),2))
    B0=(atom('v0',(-1,0)),atom('v1',(-1,0),2))
    A=(atom('a0'),atom('a1'));B=(atom('b0'),atom('b1'));L=(atom('l0'),atom('l1'))
    fs={
      'F00':fplus(one,fshift(fsquare(J),(9,0)),fshift(fsquare(K),(11,0)),fshift(DH,(2,0))),
      'F01':fplus(one,fshift(fsquare(A),(1,0)),fshift(fsquare(B),(3,0)),fshift(B0,(2,0))),
      'F10':fplus(one,fshift(fsquare(J),(11,11)),fshift(fsquare(A),(1,1)),fshift(L,(2,2))),
    }
    # Absorb only the fixed nonzero C factors into output coordinates.
    # Their physical unit factors are u for detector0 and u*v^2 for detector1.
    return {name:fplus(z,(atom(name+'_out0',(1,2 if name=='F10' else 0),-1),
                         atom(name+'_out1',(1,2 if name=='F10' else 0),-1))) for name,z in fs.items()}
def locate_source(model,supplied):
    if supplied:return supplied
    relative=Path(model['source_relative_path'])
    for parent in [HERE]+list(HERE.parents):
        for p in (parent/relative,parent/'repo'/relative):
            if p.is_file():return p
    return None
def check(output,source_path=None):
    model_raw=(HERE/'model.json').read_bytes();proof_raw=(HERE/'farkas_certificate.json').read_bytes()
    model=json.loads(model_raw);cert=json.loads(proof_raw)
    source_path=locate_source(model,source_path);source_checked=False
    if source_path:
        raw=source_path.read_bytes();assert hashlib.sha256(raw).hexdigest()==model['source_sha256']
        source=json.loads(raw)
        assert next(r for r in source['residuals'] if r['name']==model['reference_row']['name'])==model['reference_row']
        source_checked=True
    assert model['physical_contact_directions']=={'q0':[1,0],'q1':[1,1]}
    rows={r['name']:r for r in model['rows']}
    reference=defaultdict(int)
    for t in model['reference_row']['terms']:reference[t['parameterPower'],tuple(t['monomial'])]+=int(t['coefficient'])
    assert reference[0,(19,77)]==2128691946
    assert reference[0,(19,65)]==56549819456
    assert {(tuple(t['monomial']),tuple(t['unit_exponent'])) for t in rows['R3']['terms']}=={(('v0',),(1,0)),(('h1','v0'),(0,0))}
    fs=factors();selected=[]
    for name,z in fs.items():
        for term in rows[name]['terms']:
            key=(tuple(term['monomial']),tuple(term['unit_exponent']))
            coefficients=[p.get(key,0) for p in z]
            assert any(coefficients),('missing or cancelled term',name,key)
            selected.append({'row':name,**term,'component_coefficients':coefficients})
    squares={'F00':('j0','j1',(3,0)),'F01':('a0','a1',(1,0)),'F10':('j0','j1',(5,11))}
    for name,(x,y,e) in squares.items():
        real,imag=fs[name]
        assert real.get(((x,x),e),0)!=0 and real.get(((y,y),e),0)!=0
        assert imag.get((tuple(sorted((x,y))),e),0)!=0
    supports={name:{(tuple(t['monomial']),tuple(t['unit_exponent'])) for t in r['terms']} for name,r in rows.items()}
    results={}
    for basis,raw_units in model['unit_bases'].items():
        units=[(0,0)]+[tuple(x) for x in raw_units]
        total=defaultdict(int);rhs=0
        for item in cert['inequalities']:
            z=item['multiplier'];name=item['row'];m=tuple(item['monomial']);e=tuple(item['unit_exponent']);n=tuple(item['facet'])
            assert isinstance(z,int) and z>=0 and (m,e) in supports[name]
            assert len(m)<=2
            facet_bound=max(sum(a*b for a,b in zip(n,u)) for u in units)
            for d in range(2):
                total['r',name,d]-=z*n[d]
                for variable in m:total['w',variable,d]+=z*n[d]
            rhs+=z*((2-len(m))*facet_bound-sum(a*b for a,b in zip(n,e)))
        assert not any(total.values()) and rhs==cert['combined_rhs'][basis]<0
        projection=[sum(u) for u in units]
        assert max(projection)==1
        m=-min(projection);assert 2*m<12
        # Physical special-factor directions differ by(0,-1).
        forced=(0,-3)
        differences={tuple(a-b for a,b in zip(x,y)) for x in units for y in units}
        assert forced not in differences
        results[basis]={'exact_Farkas_contradiction':f'0 <= {rhs}',
           'projected_unit_interval':[-m,1],
           'forced_row_weight_difference':12,'constant_row_weight_bound':2*m,
           'shared_special_factor_difference_excluded':list(forced)}
    report={'status':'PASS','arithmetic':'exact integers; Python standard library only',
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'model_sha256':hashlib.sha256(model_raw).hexdigest(),'farkas_sha256':hashlib.sha256(proof_raw).hexdigest(),
      'source_table_sha256':model['source_sha256'],'source_table_rechecked':source_checked,
      'literal_reference_terms_checked':2,'field_factor_terms_checked':len(selected),
      'full_square_multiplier_witnesses_checked':3,
      'physical_contact_directions':model['physical_contact_directions'],
      'selected_factor_terms':selected,'nonnegative_inequalities':len(cert['inequalities']),
      'results':results,'weight_bound':'none; arbitrary real weights','scope':model['scope']}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='selected_factor_terms'},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path)
    ap.add_argument('--output',type=Path,default=HERE/'certificate.json')
    args=ap.parse_args();check(args.output,args.source)
