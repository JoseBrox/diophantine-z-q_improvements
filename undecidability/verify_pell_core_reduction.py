#!/usr/bin/env python3
"""Independently inspect complete tables after the proved Pell-core reduction."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'undecidability/code'))
from build_pell_core_reduction import build


def expression(row,names):
    return sp.expand(sum(sp.sympify(t['coefficient'])*
        sp.prod(sp.Symbol(names[i-1]) for i in t['monomial']) for t in row['terms']))


def verify(basepath,tablepath,certpath):
    old=json.loads(basepath.read_bytes());data=json.loads(tablepath.read_bytes());cert=json.loads(certpath.read_bytes())
    regenerated,generated_cert=build(basepath)
    assert tablepath.read_bytes()==(json.dumps(regenerated,separators=(',',':'),sort_keys=True)+'\n').encode()
    generated_cert['table_sha256']=hashlib.sha256(tablepath.read_bytes()).hexdigest()
    assert cert==generated_cert
    oldnames=old['variable_names'];names=data['variable_names']
    oldrows={r['name']:r for r in old['residuals']};rows={r['name']:r for r in data['residuals']}
    removed={'d2'}|{f'positive_{s}_{i}' for s in ('I','phi','gamma') for i in (1,2,3)}
    assert set(oldnames)-set(names)==removed
    assert set(names)-set(oldnames)=={'pell_d_positive_square'}
    dropped={'jones1980.d2.definition'}|{f'jones1980.positive.{s}' for s in ('I','phi','gamma')}
    assert set(oldrows)-set(rows)==dropped
    assert set(rows)-set(oldrows)=={'jones1980.pell_positive_root'}
    a,c,d,F2,G,z=map(sp.Symbol,['a','c','d','F2','G','pell_d_positive_square'])
    assert expression(rows['jones1980.d.norm'],names)==expression(oldrows['jones1980.d.norm'],oldnames).subs(sp.Symbol('d2'),d*d)
    assert expression(rows['jones1980.G.definition'],names)==sp.expand(G-a-F2*(c+1-a))
    assert expression(rows['jones1980.pell_positive_root'],names)==sp.expand(z*z-(a-1)*(d-1))
    for name,row in oldrows.items():
        if name in dropped|{'jones1980.d.norm','jones1980.G.definition'}:continue
        assert expression(row,oldnames)==expression(rows[name],names),name
    assert data['ordinary_integer_inputs']==old['ordinary_integer_inputs']
    assert data['reciprocal_integer_inputs']==old['reciprocal_integer_inputs']
    assert data['variables']==old['variables']-9==len(names)==len(set(names))
    assert len(rows)==len(oldrows)-3==len(data['residuals'])
    assert data['outer_coordinates']==old['outer_coordinates']-9
    assert data['outer_residuals']==old['outer_residuals']-3
    assert max(len(t['monomial']) for r in rows.values() for t in r['terms'])==2
    assert {i for r in rows.values() for t in r['terms'] for i in t['monomial']}==set(range(1,len(names)+1))
    parameters=list(map(sp.Symbol,data['parameters']))
    for row in rows.values():
        for term in row['terms']:
            coef=sp.sympify(term['coefficient'])
            assert coef.free_symbols<=set(parameters)
            assert sp.Poly(coef,*parameters).domain==sp.ZZ
    for doc in (data,cert):
        assert doc['source_universality_hypothesis']=='U_em'
        assert doc['source_universality_verified'] is False
        assert doc['unconditional_undecidability_claim'] is False
    return {'variables':len(names),'quadratic_rows':len(rows),'status':'PASS'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline-dir',type=Path,default=ROOT/'undecidability/coefficients/jones1980_global_gauge')
    ap.add_argument('--baseline-prefix',default='global_gauge')
    ap.add_argument('--table-dir',type=Path,default=ROOT/'undecidability/coefficients/jones1980_pell_core')
    ap.add_argument('--prefix',default='pell_core')
    ap.add_argument('--include-abc',action='store_true')
    args=ap.parse_args()
    for m in ((163,179,56) if args.include_abc else (163,179)):
        baseline=(ROOT/'undecidability/coefficients/jones1980_shared/shared_reference_m56_quadrics.json'
            if m==56 else args.baseline_dir/f'{args.baseline_prefix}_m{m}_quadrics.json')
        ans=verify(baseline,
            args.table_dir/f'{args.prefix}_m{m}_quadrics.json',args.table_dir/f'{args.prefix}_m{m}_certificate.json')
        print(f"m={m}: PASS, {ans['variables']} coordinates, {ans['quadratic_rows']} quadrics; all twelve integer predicates retained; U_em remains unverified")


if __name__=='__main__':main()
