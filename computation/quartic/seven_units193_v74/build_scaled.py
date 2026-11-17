#!/usr/bin/env python3
"""Reduce parameter degree by an input-preserving diagonal C-rescaling.

The producer reads the already independently verified unscaled193 rows.
No arithmetic supplier or defining threshold is inferred by this program.
"""
from collections import defaultdict
from pathlib import Path
from hashlib import sha256
from math import gcd
import json
HERE=Path(__file__).resolve().parent
SCALED=(44,45,46,47,52,53,54,55,56,57,99,100)

def build(source_name,target_name):
    source=HERE/source_name;target=HERE/target_name;target.mkdir(exist_ok=True)
    table=json.loads((source/'quadratic-family.json').read_text())
    assert table['variables']==193 and 1 not in SCALED
    weights={i:(-1 if i in SCALED else 0) for i in range(1,194)}
    rows=[];normalizations=[]
    for row in table['residuals']:
        terms=[dict(t,parameterPower=t['parameterPower']+sum(weights[i] for i in t['monomial'])) for t in row['terms']]
        minimum=min(t['parameterPower'] for t in terms)
        for term in terms:term['parameterPower']-=minimum
        assert all(0<=t['parameterPower']<=1 for t in terms)
        assert gcd(*(int(t['coefficient'])*149**t['parameterPower'] for t in terms))==1
        rows.append(dict(row,terms=terms));normalizations.append({'name':row['name'],'C_shift':-minimum})
    table['residuals']=rows;table['format']='parameter-scaled-quartic193/v74'
    quartic=defaultdict(int)
    for row in rows:
        for term in row['terms']:
            for other in row['terms']:
                key=term['parameterPower']+other['parameterPower'],tuple(sorted(term['monomial']+other['monomial']))
                quartic[key]+=int(term['coefficient'])*int(other['coefficient'])
    quartic={k:v for k,v in quartic.items()if v}
    assert quartic[0,(1,1,1,1)]==1
    polynomial={'variables':193,'terms':[{'parameterPower':a,'monomial':list(m),'coefficient':str(c)} for (a,m),c in sorted(quartic.items())]}
    transformation={'source':source_name,'source_quadratic_sha256':sha256((source/'quadratic-family.json').read_bytes()).hexdigest(),'substitution':'old X_i = C^weights[i] * new X_i','weights':{str(i):v for i,v in weights.items()},'row_normalizations':normalizations,'fixed_nonzero_parameter':'C=149^N,N>=1','input_unchanged':True}
    for name,data in [('quadratic-family.json',table),('polynomial-family.json',polynomial),('parameter-transformation.json',transformation)]:
        (target/name).write_text(json.dumps(data,indent=2)+'\n')
    print(target_name,'variables193','quadrics',len(rows),'quartic parameter degree',max(a for a,m in quartic),'terms',len(quartic),'monomials',len({m for a,m in quartic}))

if __name__=='__main__':
    build('primitive','compact')
    build('fewer_monomials','compact_fewer_monomials')
