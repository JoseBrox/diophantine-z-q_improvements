#!/usr/bin/env python3
"""Independent exact checker: no import of the quartic producer.

Checks arithmetic gate identities, all degree-preserving eliminations,
primitive integer residuals, and the complete sparse quartic expansion.
The separate human-readable source review checks arithmetic semantics.
"""
from collections import Counter
from fractions import Fraction as Q
import argparse
import gzip
import hashlib
import json
from math import gcd,lcm
from pathlib import Path


def add(a,m,c):
    a[m]=a.get(m,Q(0))+c
    if not a[m]:del a[m]


def product(a,b):
    r={}
    for m,c in a.items():
        for n,d in b.items():add(r,tuple(sorted(m+n)),c*d)
    return r


def affine(data):
    return {(() if i<0 else (i,)):Q(n,d) for i,n,d in data}


def decode(data):return {tuple(m):Q(n,d) for m,n,d in data}


def substitute(p,v,replacement):
    out={}
    for m,c in p.items():
        t={tuple(i for i in m if i!=v):c}
        for _ in range(m.count(v)):t=product(t,replacement)
        for n,d in t.items():add(out,n,d)
    return out


def verify(path):
    raw=gzip.decompress(path.read_bytes());o=json.loads(raw)
    d=o['derivation'];orig=d['source_rows']
    assert all(v['index']==i for i,v in enumerate(d['original_variables']))
    gate_variables=set()
    for g in d['gates']:
        v=g['variable'];assert v>0 and v not in gate_variables
        gate_variables.add(v)
        aa=[affine(x) for x in g['arguments']]
        assert all(i<v for a in aa for m in a for i in m)
        if g['operation']=='mul':
            p=product(*aa);add(p,(v,),-1)
        elif g['operation']=='inv':
            p=product(aa[0],{(v,):Q(1)});add(p,(),-1)
        elif g['operation']=='quadratic':
            p=decode(g['polynomial'])
            assert all(len(m)==2 and max(m)<v for m in p)
            add(p,(v,),-1)
        elif g['operation'] in ('field_inverse_0','field_inverse_1'):
            w=g['pair']
            assert w!=v and abs(w-v)==1
            paired=[h for h in d['gates'] if h['variable']==w]
            assert len(paired)==1 and paired[0]['pair']==v and paired[0]['arguments']==g['arguments']
            if g['operation']=='field_inverse_0':
                assert paired[0]['operation']=='field_inverse_1' and v<w
                p=product(aa[0],{(v,):Q(1)})
                for m,c in product(aa[1],{(w,):Q(2)}).items():add(p,m,c)
                add(p,(),-1)
            else:
                assert paired[0]['operation']=='field_inverse_0' and w<v
                assert all(i<w for a in aa for m in a for i in m)
                p=product(aa[0],{(v,):Q(1)})
                for m,c in product(aa[1],{(w,):Q(1)}).items():add(p,m,c)
        elif g['operation'] in ('field_quotient_0','field_quotient_1'):
            w=g['pair'];assert abs(w-v)==1
            reason=g['domain_reason']
            assert reason in ('doubling slope','local parameter','nonzero logarithm','nonzero local parameter')
            paired=[h for h in d['gates'] if h['variable']==w]
            assert len(paired)==1 and paired[0]['pair']==v and paired[0]['arguments']==g['arguments'] and paired[0]['domain_reason']==reason
            assert all(i<min(v,w) for a in aa for m in a for i in m)
            if g['operation']=='field_quotient_0':
                assert v<w and paired[0]['operation']=='field_quotient_1'
                p=product(aa[2],{(v,):Q(1)})
                for m,c in product(aa[3],{(w,):Q(2)}).items():add(p,m,c)
                for m,c in aa[0].items():add(p,m,-c)
            else:
                assert w<v and paired[0]['operation']=='field_quotient_0'
                p=product(aa[2],{(v,):Q(1)})
                for m,c in product(aa[3],{(w,):Q(1)}).items():add(p,m,c)
                for m,c in aa[1].items():add(p,m,-c)
        else:raise AssertionError(g['operation'])
        assert p==decode(orig[g['row']]['terms']),('gate',v)
        assert orig[g['row']]['K_constant']==[0,1]
    active=d['initial_active_rows']
    rows={i:decode(orig[i]['terms']) for i in active}
    symbols={i:Q(*orig[i]['K_constant']) for i in active}
    counts=Counter()
    eliminated=[]
    for op in d['quadratic_operations']:
        counts[op['kind']]+=1
        if op['kind']=='row_add':
            i,j=op['target'],op['other'];assert i!=j
            q=Q(*op['factor'])
            for m,c in rows[j].items():add(rows[i],m,q*c)
            symbols[i]+=q*symbols[j]
        elif op['kind']=='eliminate':
            i,v=op['pivot'],op['variable']
            assert v in gate_variables and v not in eliminated and v!=0
            assert not symbols[i]
            pivot=rows[i];coef=pivot[(v,)]
            assert coef and all(v not in m for m in pivot if m!=(v,))
            replacement={m:-c/coef for m,c in pivot.items() if m!=(v,)}
            assert replacement==decode(op['replacement'])
            affected=sorted(j for j,r in rows.items() if j!=i and any(v in m for m in r))
            assert affected==op['affected']
            for j in affected:
                rows[j]=substitute(rows[j],v,replacement)
                assert all(len(m)<=2 for m in rows[j])
            del rows[i];del symbols[i];eliminated.append(v)
        else:raise AssertionError(op)
    rows={i:r for i,r in rows.items() if r or symbols[i]}
    used={0}|{v for r in rows.values() for m in r for v in m}
    mapping={v:i for i,v in enumerate(sorted(used))}
    assert mapping=={int(k):v for k,v in d['active_map'].items()}
    assert len(o['variables'])==len(used)
    assert all(v['index']==i and mapping[v['original_index']]==i for i,v in enumerate(o['variables']))
    actual={r['old_row']:r for r in o['residuals']}
    assert set(actual)==set(rows)
    for i,p in rows.items():
        denominator=lcm(*(c.denominator for c in list(p.values())+[symbols[i]]))
        content=0
        for c in list(p.values())+[symbols[i]]:content=gcd(content,abs(int(c*denominator)))
        content=max(1,content)
        rr=[[list(mapping[v] for v in m),0,int(c*denominator)//content] for m,c in sorted(p.items())]
        if symbols[i]:rr.append([[],1,int(symbols[i]*denominator)//content])
        assert rr==actual[i]['terms'],('residual',i)
        assert actual[i]['clearing_multiplier']==[denominator,content]
    # A separate convolution computes every coefficient, including all mixed
    # products. K is a coefficient symbol, never a coordinate.
    expansion=Counter()
    for row in o['residuals']:
        for m,k,c in row['terms']:
            assert len(m)<=2
            for n,l,e in row['terms']:
                expansion[(tuple(sorted(m+n)),k+l)]+=c*e
    expansion={key:c for key,c in expansion.items() if c}
    given={(tuple(m),k):c for m,k,c in o['expanded_polynomial']}
    assert len(given)==len(o['expanded_polynomial'])
    assert given==expansion,'complete expansion'
    degree=max(len(m) for m,k in given);assert degree==4
    assert all(v<len(used) for m,k in given for v in m)
    report=o['report']
    assert report['total_variables']==len(used)
    assert report['existential_witnesses']==len(used)-1
    assert report['quadratic_residuals']==len(rows)
    assert report['expanded_terms_in_Z_K']==len(given)
    assert report['quadratic_preserving_eliminations']==len(eliminated)
    assert report['categories']==dict(Counter(v['category'] for v in o['variables']))
    maxbits=max(abs(c).bit_length() for c in given.values())
    assert report['max_integer_coefficient_bits_in_Z_K']==maxbits
    polynomial_content=0
    for c in given.values():polynomial_content=gcd(polynomial_content,abs(c))
    # This is the exact height for the ordinary integer version. For the
    # symbolic version it is the height over Z[K], not after substitution.
    result={'status':'PASS','input':str(path),'total_variables':len(used),
            'existential_witnesses':len(used)-1,'degree':degree,
            'gates_checked':len(d['gates']),'row_operations':dict(counts),
            'residuals_checked':len(rows),'all_expanded_coefficients_checked':len(given),
            'coefficient_symbol_content':polynomial_content,
            'max_integer_coefficient_bits_in_Z_K':maxbits,
            'fixed_constants':o['fixed_constants'],
            'constant_coefficient_in_Z_K':{str(k):str(c) for (m,k),c in given.items() if not m},
            'uncompressed_sha256':hashlib.sha256(raw).hexdigest(),
            'scope':'Exact algebraic compiler and complete table checks. Source arithmetic assumptions and source-formula correspondence are separate proof/review obligations; this checker does not certify those number-theoretic theorems.'}
    (path.parent/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file',type=Path)
    verify(p.parse_args().file)
