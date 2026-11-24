#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent
root=here.parents[1]
for c in json.loads((here/'certificate.json').read_text()):
    p=c['prime']
    assert all(p%d for d in range(2, __import__('math').isqrt(p)+1))
    raw=(root/c['path']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==c['git_blob']
    q=json.loads(raw); n=c['rows']
    assert len(q['residuals'])==n==c['rank']
    assert q['variables']==c['variables']
    cols=list(map(tuple,c['minor_columns']))
    assert len(cols)==len(set(cols))==n
    matrix=[]
    for r in q['residuals']:
        d={}
        for t in r['terms']:
            if len(t['monomial'])!=2: continue
            assert t['parameterPower']==0
            m=tuple(t['monomial'])
            d[m]=(d.get(m,0)+int(t['coefficient']))%p
        matrix.append([d.get(col,0) for col in cols])
    det=1
    for i in range(n):
        j=next(j for j in range(i,n) if matrix[j][i])
        if i!=j:
            matrix[i],matrix[j]=matrix[j],matrix[i]
            det=-det
        v=matrix[i][i]
        det=det*v%p
        v=pow(v,-1,p)
        for j in range(i+1,n):
            a=matrix[j][i]*v%p
            if a:
                for l in range(i,n):
                    matrix[j][l]=(matrix[j][l]-a*matrix[i][l])%p
    assert det%p==c['determinant_mod_p']!=0
    print('PASS',c['variables'],'rank',n,'determinant',det%p)
