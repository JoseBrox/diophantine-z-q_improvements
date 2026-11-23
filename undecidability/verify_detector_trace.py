#!/usr/bin/env python3
"""Exact independent verification of the detector-product trace compression."""
from pathlib import Path
import hashlib
import json
import sys
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'undecidability/code'))
from build_detector_trace import build


def rational_identity():
    a0,a1,b0,b1,u,k,D=s.symbols('a0 a1 b0 b1 u k D')
    nb=b0**2-2*b1**2
    w0=(a0*b0+2*a1*b1)/u
    w1=(a0*b1+a1*b0)/u
    v0=k*u*b0/nb
    v1=k*u*b1/nb
    t=(2*v0*a0+4*v1*a1)/k
    old=-w0**2+2*w1**2+2*w0*(D+k)-k**2
    new=(D+k)*t-a0**2+2*a1**2-v0**2+2*v1**2
    assert s.cancel(new-u**2*old/nb)==0
    assert s.cancel(b0*v0-2*b1*v1-k*u)==0
    assert s.cancel(b0*v1-b1*v0)==0


def check(m,N,rowcount):
    folder=ROOT/'undecidability/coefficients/jones1980_detector_trace'
    raw=(folder/f'detector_trace_m{m}_quadrics.json').read_bytes()
    new=json.loads(raw)
    cert=json.loads((folder/f'detector_trace_m{m}_certificate.json').read_text())
    oldpath=ROOT/f'undecidability/coefficients/jones1980_scalar_norm/scalar_norm_m{m}_quadrics.json'
    oldraw=oldpath.read_bytes();old=json.loads(oldraw)
    assert new['variables']==cert['variables']==N
    assert len(new['residuals'])==cert['quadratic_rows']==rowcount
    assert cert['coordinate_saving']==new['detector_trace_coordinate_saving']==10
    assert cert['table_sha256']==hashlib.sha256(raw).hexdigest()
    assert cert['predecessor_sha256']==new['detector_trace_predecessor_sha256']==hashlib.sha256(oldraw).hexdigest()
    assert raw==(json.dumps(build(m),sort_keys=True,separators=(',',':'))+'\n').encode()
    for d in[cert,new]:
        assert d['source_universality_hypothesis']=='U_em'
        assert d['source_universality_verified']is False
        assert d['unconditional_undecidability_claim']is False
    assert cert['new_abc_assumption']is False
    assert cert['pell_core_reduction_already_included']is False
    ns=new['variable_names'];ons=old['variable_names']
    assert len(ns)==len(set(ns))==N
    support=set()
    parameters=set(map(s.Symbol,new['parameters']))
    for r in new['residuals']:
        for term in r['terms']:
            assert len(term['monomial'])<=2
            support.update(term['monomial'])
            coeff=s.sympify(term['coefficient'])
            assert coeff.free_symbols<=parameters
            assert s.Poly(coeff,*parameters).domain.is_ZZ
    assert support==set(range(1,N+1))
    def expression(row,names):
        return s.expand(sum(s.sympify(t['coefficient'])*s.prod(s.Symbol(names[j-1])for j in t['monomial'])for t in row['terms']))
    oldrows={r['name']:expression(r,ons)for r in old['residuals']}
    newrows={r['name']:expression(r,ns)for r in new['residuals']}
    assert len(newrows)==rowcount
    maps=json.loads((ROOT/f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
    labels={int(j):v for j,v in maps['source_labels'].items()}
    blocks=old['ordinary_integer_inputs']+['i_reciprocal']
    assert len(blocks)==12
    def z(b,j):
        n=f'int_{b}_{labels[j]}'
        return s.Symbol(n if n in ons else f'int_b_{labels[j]}')
    c,ci,u=(z('b',j)for j in[400,401,402])
    k=u if m==163 else ci
    assert s.expand(oldrows['integer.b.unit.c_inverse']-(c*ci-1))==0
    assert s.expand(oldrows['integer.b.unit.c_inverse_square']-(u-ci**2))==0
    b0,b1=z('b',130),z('b',131)
    v0,v1=s.symbols('common_detector_inverse_real common_detector_inverse_imag')
    expected=dict(oldrows)
    gone=set();private=set();removed=set();replaced=set()
    for b in blocks:
        label='i'if b=='i_reciprocal'else b
        a0,a1=z(b,118),z(b,119)
        w0,w1=z(b,302),z(b,303)
        D=z(b,305)
        t=s.Symbol(f'int_{b}_detector_product_trace')
        private.add(str(t));gone.update(map(str,[w0,w1]))
        n0=f'global.{b}.factor_product3.0'
        n1=f'global.{b}.factor_product3.1'
        nn=f'integer.{label}.shared.norm_error'
        assert s.expand(oldrows[n0]-(a0*b0+2*a1*b1-u*w0))==0
        assert s.expand(oldrows[n1]-(a0*b1+a1*b0-u*w1))==0
        constant=u**2 if m==163 else u
        assert s.expand(oldrows[nn]-(-w0**2+2*w1**2+2*w0*(D+k)-constant))==0
        assert s.expand((constant-k**2).subs(u,ci**2))==0
        for n,e in oldrows.items():
            if e.free_symbols&{w0,w1}:
                assert n in{n0,n1,nn},(m,b,n)
        del expected[n0];del expected[n1]
        removed.update([n0,n1]);replaced.add(nn)
        expected[nn]=s.expand((D+k)*t-a0**2+2*a1**2-v0**2+2*v1**2)
        expected[f'detector_trace.{b}.definition']=k*t-2*v0*a0-4*v1*a1
    expected['detector_trace.common.inverse.0']=b0*v0-2*b1*v1-k*u
    expected['detector_trace.common.inverse.1']=b0*v1-b1*v0
    assert set(expected)==set(newrows)
    assert all(s.expand(e-newrows[n])==0 for n,e in expected.items())
    assert gone==set(new['detector_trace_removed_coordinates'])==set(ons)-set(ns)
    assert private==set(new['detector_trace_added_private_coordinates'])
    assert set(new['detector_trace_added_common_coordinates'])==set(map(str,[v0,v1]))
    assert set(ns)-set(ons)==private|set(map(str,[v0,v1]))
    assert removed==set(new['detector_trace_removed_rows'])
    assert replaced==set(new['detector_trace_replaced_rows'])
    return {'interface':m,'variables':N,'quadratic_rows':rowcount,
            'every_row_reconstructed':True,'complete_deleted_coordinate_audit':True,
            'table_sha256':cert['table_sha256'],'universality_verified':False}


if __name__=='__main__':
    rational_identity()
    print(json.dumps({'status':'PASS','norm_trace_identity':'exact rational function identity',
                     'systems':[check(163,1112,956),check(179,1292,1112)]},indent=2))
