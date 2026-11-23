#!/usr/bin/env python3
"""Check the scalar rechart, norm polynomial, detector trace and their composition."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'undecidability'


def run(name,*args):
    return subprocess.run([sys.executable,'-B',str(F/name),*args],cwd=ROOT,
        capture_output=True,text=True,check=True).stdout


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);args=ap.parse_args()
    for name in ['verify_scalar_rechart.py','verify_scalar_norm_compression.py','verify_detector_trace.py']:
        assert json.loads(run(name))['status']=='PASS'
    for base,prefix in [('scalar_norm','scalar_pell'),('detector_trace','detector_pell')]:
        out=run('verify_pell_core_reduction.py','--baseline-dir',str(F/f'coefficients/jones1980_{base}'),
            '--baseline-prefix',base,'--table-dir',str(F/f'coefficients/jones1980_{prefix}'),'--prefix',prefix)
        assert out.count('PASS')==2
    binomial=json.loads(run('verify_binomial_pell_certificate.py'))
    binomial_certificate=json.loads((F/'certificates/binomial_pell_certificate.json').read_text())
    assert binomial['normalized_examples']==binomial_certificate['ratio_examples']['normalized_pell_examples']
    assert binomial['ratio_examples']==binomial_certificate['ratio_examples']['ratio_examples']
    assert binomial['status']=='PASS' and binomial['source_universality_claim'] is False
    ledger=json.loads((F/'results.json').read_text());records={r['id']:r for r in ledger['records']}
    assert len(records)==len(ledger['records'])
    assert ledger['global_minimum_claimed'] is False
    assert ledger['inherited_arithmetic_premises_independently_proved'] is False
    cases={'scalar-rechart':[(163,1143,987),(179,1323,1143)],
        'scalar-norm':[(163,1122,966),(179,1302,1122)],
        'scalar-pell':[(163,1113,963),(179,1293,1119)],
        'detector-trace':[(163,1112,956),(179,1292,1112)],
        'detector-pell':[(163,1103,953),(179,1283,1109)]}
    checked={}
    for stage,items in cases.items():
        for m,n,q in items:
            key=f'{stage}-quartic-{m}';r=records[key];path=F/r['table']
            t=json.loads(path.read_bytes());c=json.loads((F/r['certificate']).read_text())
            assert r['variables']==t['variables']==c['variables']==n
            assert r['quadratic_rows']==len(t['residuals'])==q
            assert r['table_sha256']==c['table_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
            assert r['degree']==t['sum_of_squares_degree']==4
            assert r['source_universality_hypothesis']=='U_em'
            assert r['source_universality_independently_verified'] is False
            assert t['source_universality_verified'] is c['source_universality_verified'] is False
            assert t['unconditional_undecidability_claim'] is c['unconditional_undecidability_claim'] is False
            assert r['additional_height_hypothesis'] is None
            assert r['retains_project_arithmetic_premises'] is True
            assert r['integer_predicates_discarded']==0 and r['integer_certificates']==12
            assert r['pell_reduction_included']==stage.endswith('-pell')
            assert r['outer_coordinates']==t['outer_coordinates']==(242 if stage.endswith('-pell') else 251)
            assert (F/r['proof']).is_file() and (F/r['proof']).with_suffix('.pdf').is_file()
            checked[key]={'variables':n,'quadratic_rows':q}
    result={'schema':'zq-undecidability-verification/v92','status':'PASS','quartic_checkpoints':checked,
        'independent_binomial_certificate':binomial,'integer_certificates_retained':12,
        'no_global_minimum_claimed':True,'source_universality_claimed':False,
        'scope':'Exact equations, recovery identities, occurrence audits, literal guards, coefficient domains, counts and hashes. U_em and inherited arithmetic foundations remain qualified.'}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
