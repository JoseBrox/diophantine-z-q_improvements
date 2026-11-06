"""Remove coordinates exposed by proportional quadratic Hessian columns.

All accepted changes use the existing shear and rational elimination rules.
The separate certificate checker remains unchanged.
"""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import argparse,gzip,itertools,json,math,time
import polynomial_ops as p
from optimize import substitute_rational
from export_artifact import enc,export

def columns(rows):
    result=defaultdict(dict)
    for i,row in enumerate(rows):
        for mon,c in row.items():
            if len(mon)!=2:continue
            v,w=mon
            if v==w:result[v][(i,w)]=2*c
            else:
                result[v][(i,w)]=c
                result[w][(i,v)]=c
    return result

def candidates(rows):
    groups=defaultdict(list)
    for v,col in columns(rows).items():
        if v==0:continue
        g=math.gcd(*col.values())
        if col[min(col)]<0:g=-g
        key=tuple(sorted((m,c//g) for m,c in col.items()))
        groups[key].append((v,g))
    pairs=[]
    for group in groups.values():
        for (v,a),(w,b) in itertools.combinations(sorted(group),2):
            pairs.append((v,w,Fraction(a,b)))
            pairs.append((w,v,Fraction(b,a)))
    return pairs

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--parent',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--max-steps',type=int,default=500)
    parser.add_argument('--max-terms',type=int,default=96)
    a=parser.parse_args();start=time.monotonic()
    rows=[{tuple(m):c for c,m in row} for row in json.loads(gzip.decompress((a.parent/'candidate-rows.json.gz').read_bytes()))]
    records=[json.loads(line) for line in gzip.decompress((a.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    allocated=records[-1]['allocated_variables']
    records=[r for r in records if r['kind'] not in ['weights','final']]
    incidence=defaultdict(set);poly={}
    for i,row in enumerate(rows):
        for v in p.vars_in(row):incidence[v].add(i)
        p.poly_add(poly,p.square(row))
    initial=sum(bool(ids) for ids in incidence.values());history=[];accepted=0
    for step in range(a.max_steps):
        pairs=candidates(rows);history.append(len(pairs));best=None
        print(json.dumps({'step':step,'oriented_proportional_pairs':len(pairs),'variables':sum(bool(ids) for ids in incidence.values())}),flush=True)
        for v,w,k in pairs:
            affected_w=sorted(incidence[w]);num,den=k.numerator,k.denominator
            sheared={i:substitute_rational(rows[i],w,{(w,):den,(v,):-num},den) for i in affected_w}
            if any(len(row)>a.max_terms or any(abs(c).bit_length()>256 for c in row.values()) for row in sheared.values()):continue
            def after(i):return sheared.get(i,rows[i])
            affected_v=sorted(i for i in incidence[v]|set(affected_w) if v in p.vars_in(after(i)))
            assert not any(v in mon and len(mon)==2 for i in affected_v for mon in after(i))
            options=affected_v if affected_v else [None]
            for definition in options:
                changed=dict(sheared);elimination=None
                if definition is not None:
                    row=after(definition);c=row.get((v,),0)
                    if not c:continue
                    numerator={m:-d*(1 if c>0 else -1) for m,d in row.items() if m!=(v,)}
                    denominator=abs(c);g=math.gcd(denominator,*numerator.values())
                    numerator={m:d//g for m,d in numerator.items()};denominator//=g
                    others=[i for i in affected_v if i!=definition]
                    for i in others:changed[i]=substitute_rational(after(i),v,numerator,denominator)
                    changed[definition]={}
                    elimination={'kind':'eliminate','data':{'row':definition,'variable':v,'replacement':enc(numerator),
                                    'denominator':denominator,'affected':others},
                                 'patches':[[i,enc(changed[i])] for i in others]+[[definition,[]]]}
                if any(len(row)>a.max_terms or any(len(mon)>2 for mon in row) for row in changed.values()):continue
                delta={}
                for i,row in changed.items():
                    p.poly_add(delta,p.square(rows[i]),-1);p.poly_add(delta,p.square(row))
                if any(abs(poly.get(m,0)+c)>=2**80 for m,c in delta.items()):continue
                gain=sum(bool(poly.get(m,0)+c)-(m in poly) for m,c in delta.items())
                score=(gain,len(changed),v,w)
                if best is None or score<best[0]:
                    shear={'kind':'shear','data':{'variable':w,'other':v,'scalar':[-num,den],'affected':affected_w},
                           'patches':[[i,enc(row)] for i,row in sheared.items()]}
                    best=(score,v,changed,delta,shear,elimination)
        if best is None:break
        score,v,changed,delta,shear,elimination=best
        records.append(shear)
        if elimination:records.append(elimination)
        p.poly_add(poly,delta)
        for i,row in changed.items():
            for x in p.vars_in(rows[i]):incidence[x].remove(i)
            rows[i]=row
            for x in p.vars_in(row):incidence[x].add(i)
        assert not incidence[v]
        accepted+=1
    report=export(a.output,a.parent/'source-residuals.jsonl.gz',rows,records,allocated,
                  {'initial_variables':initial,'coordinate_pairs_removed':accepted,
                   'oriented_pair_counts':history,'seconds':round(time.monotonic()-start,3)})
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
