#!/usr/bin/env python3
"""Replace private quadratic-field detector products by rational traces.

The default predecessor includes the scalar-point and scalar-norm changes.
The transformation also accepts any complete predecessor with the same
literal detector interface, so independent outer-core changes commute.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'undecidability/code'))
from quadratic_utils import sparse_rows


def build(m,root=ROOT,source_path=None):
    source=Path(source_path)if source_path else root/f'undecidability/coefficients/jones1980_scalar_norm/scalar_norm_m{m}_quadrics.json'
    raw=source.read_bytes()
    old=json.loads(raw)
    maps=json.loads((root/f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
    labels={int(j):v for j,v in maps['source_labels'].items()}
    oldnames=old['variable_names']
    blocks=old['ordinary_integer_inputs']+['i_reciprocal']
    def z(b,j):
        n=f'int_{b}_{labels[j]}'
        return s.Symbol(n if n in oldnames else f'int_b_{labels[j]}')
    def expr(row):
        return s.expand(sum(s.sympify(t['coefficient'])*s.prod(s.Symbol(oldnames[j-1])for j in t['monomial'])for t in row['terms']))
    u=z('b',402)
    k=u if m==163 else z('b',401)
    B0,B1=z('b',130),z('b',131)
    v0,v1=s.symbols('common_detector_inverse_real common_detector_inverse_imag')
    common=[v0,v1]
    private={b:s.Symbol(f'int_{b}_detector_product_trace')for b in blocks}
    gone={str(z(b,j))for b in blocks for j in[302,303]}
    removed=[]
    replaced=[]
    rows=[]
    for row in old['residuals']:
        n=row['name'];e=expr(row)
        if n.startswith('global.') and '.factor_product3.' in n:
            removed.append(n)
            continue
        if n.startswith('integer.') and n.endswith('.shared.norm_error'):
            label=n.split('.')[1];b='i_reciprocal'if label=='i'else label
            a0,a1=z(b,118),z(b,119)
            D=z(b,305)
            e=(D+k)*private[b]-a0**2+2*a1**2-v0**2+2*v1**2
            replaced.append(n)
        assert not(set(map(str,e.free_symbols))&gone),(n,e)
        rows.append((n,e))
    for b in blocks:
        a0,a1=z(b,118),z(b,119)
        rows.append((f'detector_trace.{b}.definition',k*private[b]-2*v0*a0-4*v1*a1))
    rows.extend([
        ('detector_trace.common.inverse.0',B0*v0-2*B1*v1-k*u),
        ('detector_trace.common.inverse.1',B0*v1-B1*v0),
    ])
    names=[n for n in oldnames if n not in gone]+list(map(str,private.values()))+list(map(str,common))
    residuals=sparse_rows(rows,list(map(s.Symbol,names)),list(map(s.Symbol,old['parameters'])))
    saving=len(blocks)-len(common)
    assert len(names)==old['variables']-saving
    assert len(residuals)==len(old['residuals'])-saving
    assert len(removed)==2*len(blocks) and len(replaced)==len(blocks)
    new=dict(old)
    new.update({
        'variables':len(names),'variable_names':names,'residuals':residuals,
        'detector_trace_predecessor_sha256':hashlib.sha256(raw).hexdigest(),
        'detector_trace_coordinate_saving':saving,
        'detector_trace_removed_coordinates':sorted(gone),
        'detector_trace_added_private_coordinates':list(map(str,private.values())),
        'detector_trace_added_common_coordinates':list(map(str,common)),
        'detector_trace_removed_rows':removed,'detector_trace_replaced_rows':replaced,
        'detector_trace_recovery':'W_i=a_i B/u; v conjugate(B)=k*u; k*trace_i=Tr(v a_i)',
        'detector_trace_status':'exact rational equivalence; retained arithmetic interfaces and U_em remain hypotheses',
    })
    return new


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline-dir',type=Path,default=ROOT/'undecidability/coefficients/jones1980_scalar_norm')
    ap.add_argument('--baseline-prefix',default='scalar_norm')
    ap.add_argument('--output-dir',type=Path,default=ROOT/'undecidability/coefficients/jones1980_detector_trace')
    ap.add_argument('--output-prefix',default='detector_trace')
    args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for m in[163,179]:
        source=args.baseline_dir/f'{args.baseline_prefix}_m{m}_quadrics.json'
        d=build(m,source_path=source)
        path=args.output_dir/f'{args.output_prefix}_m{m}_quadrics.json'
        path.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
        cert={
            'interface_coordinates':m,'variables':d['variables'],'quadratic_rows':len(d['residuals']),
            'degree':4,'coordinate_saving':d['detector_trace_coordinate_saving'],
            'table_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'predecessor_sha256':d['detector_trace_predecessor_sha256'],
            'source_universality_hypothesis':'U_em','source_universality_verified':False,
            'unconditional_undecidability_claim':False,'retained_arithmetic_interfaces':True,
            'new_abc_assumption':False,'pell_core_reduction_already_included':bool(d.get('pell_core_reduction',False)),
            'proof':'undecidability/papers/detector_trace_compression.tex',
            'independent_verifier':'undecidability/verify_detector_trace.py',
        }
        (args.output_dir/f'{args.output_prefix}_m{m}_certificate.json').write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n')
        print({'m':m,'N':d['variables'],'rows':len(d['residuals']),'saving':cert['coordinate_saving'],'sha256':cert['table_sha256']})


if __name__=='__main__':main()
