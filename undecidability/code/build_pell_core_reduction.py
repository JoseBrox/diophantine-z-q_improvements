#!/usr/bin/env python3
"""Apply the proved nine-coordinate Pell reduction to a complete table.

This is an existential arithmetic equivalence, not a pointwise substitution
for all Pell witnesses. Its proof is pell_index_optimization.tex. Universality
of U_em and the retained integrality interfaces remain separate hypotheses.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
REMOVED_NAMES={'d2'}|{f'positive_{s}_{i}' for s in ('I','phi','gamma') for i in (1,2,3)}
REMOVED_ROWS={'jones1980.d2.definition'}|{f'jones1980.positive.{s}' for s in ('I','phi','gamma')}
CHANGED_ROWS={'jones1980.d.norm','jones1980.G.definition'}
NEW_NAME='pell_d_positive_square'
NEW_ROW='jones1980.pell_positive_root'


def expression(row,names):
    return sp.expand(sum(sp.sympify(t['coefficient'])*
        sp.prod(sp.Symbol(names[i-1]) for i in t['monomial']) for t in row['terms']))


def build(baseline:Path):
    data=json.loads(baseline.read_bytes())
    assert data['source_universality_hypothesis']=='U_em'
    assert data['source_universality_verified'] is False
    assert data['unconditional_undecidability_claim'] is False
    oldnames=data['variable_names'];oldrows={r['name']:r for r in data['residuals']}
    assert len(oldrows)==len(data['residuals'])
    assert REMOVED_NAMES<=set(oldnames) and REMOVED_ROWS|CHANGED_ROWS<=set(oldrows)
    assert NEW_NAME not in oldnames and NEW_ROW not in oldrows
    occurrence={s:[] for s in sorted(REMOVED_NAMES)}
    for row in data['residuals']:
        used={oldnames[i-1] for t in row['terms'] for i in t['monomial']}
        for s in used&REMOVED_NAMES:occurrence[s].append(row['name'])
    assert set(occurrence['d2'])=={'jones1980.d2.definition','jones1980.d.norm','jones1980.G.definition'}
    for s in ('I','phi','gamma'):
        for j in (1,2,3):assert occurrence[f'positive_{s}_{j}']==[f'jones1980.positive.{s}']
    names=[s for s in oldnames if s not in REMOVED_NAMES]+[NEW_NAME]
    ids={s:i+1 for i,s in enumerate(names)}
    a,c,d,F2,G,zeta=map(sp.Symbol,['a','c','d','F2','G',NEW_NAME])
    norm=expression(oldrows['jones1980.d.norm'],oldnames).subs(sp.Symbol('d2'),d*d)
    bridge=G-a-F2*(c+1-a)
    branch=zeta*zeta-(a-1)*(d-1)
    replacements={'jones1980.d.norm':norm,'jones1980.G.definition':bridge,NEW_ROW:branch}
    def serialize(expr):
        expr=sp.expand(expr)
        active=sorted(expr.free_symbols&set(map(sp.Symbol,names)),key=lambda x:ids[str(x)])
        terms=[]
        for powers,coef in sp.Poly(expr,*active).terms():
            mon=sorted(ids[str(v)] for v,e in zip(active,powers) for _ in range(e))
            assert len(mon)<=2 and coef.free_symbols<=set(map(sp.Symbol,data['parameters']))
            terms.append({'coefficient':str(coef),'monomial':mon})
        return sorted(terms,key=lambda t:t['monomial'])
    rows=[]
    for row in data['residuals']:
        name=row['name']
        if name in REMOVED_ROWS:continue
        if name in replacements:
            rows.append({'name':name,'terms':serialize(replacements[name])})
        else:
            rows.append({'name':name,'terms':[{'coefficient':t['coefficient'],
                'monomial':sorted(ids[oldnames[i-1]] for i in t['monomial'])} for t in row['terms']]})
    rows.append({'name':NEW_ROW,'terms':serialize(branch)})
    assert len(names)==data['variables']-9
    assert len(rows)==len(data['residuals'])-3
    assert {i for r in rows for t in r['terms'] for i in t['monomial']}==set(range(1,len(names)+1))
    result=dict(data)
    result.update(variables=len(names),variable_names=names,residuals=rows,
        outer_coordinates=data['outer_coordinates']-9,
        outer_residuals=data['outer_residuals']-3,
        pell_core_predecessor_sha256=hashlib.sha256(baseline.read_bytes()).hexdigest(),
        pell_core_removed_coordinate_occurrences=occurrence,
        pell_core_savings={'coordinates':9,'quadratic_rows':3},
        pell_core_new_bridge='G=a+F2*(c+1-a)',
        pell_core_positive_root='pell_d_positive_square^2=(a-1)*(d-1)',
        pell_core_proof='undecidability/papers/pell_index_optimization.tex',
        pell_core_equivalence_scope='Existential equivalence with the positive emended source, retaining every integer predicate; Pell witnesses may be reconstructed.',
        pell_core_source_p_parameter='2*w*s^2*r^2*n^2; the n^6 alternative is not silently substituted',
        pell_core_source_discrepancy='The natural modern binomial identification produces n^6 instead of the printed n^2. U_em remains unresolved.')
    cert={k:v for k,v in result.items() if k not in ('variable_names','residuals','power_chain')}
    cert['quadratic_residuals']=len(rows)
    cert['verified']=['Complete occurrence audit for all ten deleted coordinates',
        'Exact first-norm substitution and new bridge and positive-root rows',
        'Every other row preserved literally up to coordinate numbering',
        'Quadratic degree, integral parameter-polynomial coefficients, full coordinate support',
        'Nine-coordinate and three-row saving in the complete materialized system']
    cert['not_verified']=['U_em: universality of the exact emended source',
        'Retained arithmetic interfaces', 'Global minimality of the variable count']
    return result,cert


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline-dir',type=Path,default=ROOT/'undecidability/coefficients/jones1980_global_gauge')
    ap.add_argument('--baseline-prefix',default='global_gauge')
    ap.add_argument('--out',type=Path,default=ROOT/'undecidability/coefficients/jones1980_pell_core')
    ap.add_argument('--prefix',default='pell_core')
    ap.add_argument('--include-abc',action='store_true',help='Also apply the same local theorem to the 846-variable shared-reference abc table.')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    for m in ((163,179,56) if args.include_abc else (163,179)):
        baseline=(ROOT/'undecidability/coefficients/jones1980_shared/shared_reference_m56_quadrics.json'
            if m==56 else args.baseline_dir/f'{args.baseline_prefix}_m{m}_quadrics.json')
        result,cert=build(baseline)
        target=args.out/f'{args.prefix}_m{m}_quadrics.json'
        target.write_text(json.dumps(result,separators=(',',':'),sort_keys=True)+'\n')
        cert['table_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        target.with_name(f'{args.prefix}_m{m}_certificate.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'m':m,'N':result['variables'],'quadrics':len(result['residuals']),'sha256':cert['table_sha256']}))


if __name__=='__main__':main()
