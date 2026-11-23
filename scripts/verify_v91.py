#!/usr/bin/env python3
"""Verify the global-gauge and independently proved Pell reductions.

Finite algebra and exact bookkeeping only. The source U_em and retained
infinite arithmetic interfaces are not certified by this program.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'undecidability'


def run(name,*args):
    return subprocess.run([sys.executable,'-B',str(F/name),*args],cwd=ROOT,
        capture_output=True,text=True,check=True).stdout


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);args=ap.parse_args()
    global_output=run('verify_global_gauge.py')
    pell_output=run('verify_pell_core_reduction.py','--include-abc')
    assert global_output.count('PASS')==2 and pell_output.count('PASS')==3
    local=json.loads(run('verify_pell_index_optimization.py'))
    chart=json.loads(run('check_point_chart_lemmas.py'))
    assert local==json.loads((F/'certificates/pell_index_optimization.json').read_text())
    assert chart==json.loads((F/'certificates/point_chart_lemmas.json').read_text())
    assert local['status']==chart['status']=='PASS'
    assert local['symbolic_identities']['total_coordinate_saving']==9
    assert local['symbolic_identities']['total_equation_saving']==3
    assert local['negative_source_obstruction']['universal_negative_integer_witnesses']==[-7,-9]
    ledger=json.loads((F/'results.json').read_text())
    assert ledger['global_minimum_claimed'] is False
    assert ledger['inherited_arithmetic_premises_independently_proved'] is False
    records={r['id']:r for r in ledger['records']};assert len(records)==len(ledger['records'])
    receipt={}
    for prefix,m,n,q in [('global-gauge',163,1185,1095),('global-gauge',179,1355,1241),
        ('pell-core',163,1176,1092),('pell-core',179,1346,1238),('pell-core',56,837,725)]:
        key=f'{prefix}-quartic-{m}';r=records[key]
        tablepath=F/r['table'];table=json.loads(tablepath.read_bytes());cert=json.loads((F/r['certificate']).read_text())
        assert r['variables']==table['variables']==cert['variables']==n
        assert r['quadratic_rows']==len(table['residuals'])==q
        assert r['table_sha256']==cert['table_sha256']==hashlib.sha256(tablepath.read_bytes()).hexdigest()
        assert r['degree']==table['sum_of_squares_degree']==4
        assert r['source_universality_hypothesis']=='U_em'
        assert r['source_universality_independently_verified'] is False
        assert table['source_universality_verified'] is cert['source_universality_verified'] is False
        assert table['unconditional_undecidability_claim'] is cert['unconditional_undecidability_claim'] is False
        assert r['status']=='exact_algebraic_checkpoint_undecidability_conditional_on_U_em'
        assert r['retains_project_arithmetic_premises'] is True
        assert r['additional_height_hypothesis']==('ordinary_rational_abc' if m==56 else None)
        assert r['integer_certificates']==12==table['integer_blocks']
        assert (F/r['proof']).is_file() and (F/r['proof']).with_suffix('.pdf').is_file()
        if prefix=='pell-core':
            assert r['pell_core_savings']=={'coordinates':9,'quadratic_rows':3}
            assert r['integer_predicates_discarded']==0
            assert r['source_p_parameter']=='2*w*s^2*r^2*n^2'
        else:
            assert r['shared_source_coordinates']=={163:91,179:93}[m]
            assert r['duplicate_rows_removed']=={163:462,179:528}[m]
        receipt[key]={'variables':n,'quadratic_rows':q,'source_universality':'U_em remains unverified'}
    for proof in ['global_gauge_quartic_checkpoint','pell_index_optimization','point_chart_research','negative_mixed_witness']:
        assert (F/f'papers/{proof}.tex').is_file() and (F/f'papers/{proof}.pdf').is_file()
    result={'schema':'zq-undecidability-verification/v91','status':'PASS',
        'quartic_checkpoints':receipt,'independent_pell_identities':'PASS',
        'point_chart_identities_and_occurrences':'PASS','negative_mixed_input_obstruction':'PASS',
        'no_integer_predicate_discarded':True,'no_global_minimum_claimed':True,
        'scope':'Complete finite tables, occurrence audits, coefficient domains, hashes, and exact identities. General arithmetic equivalences are proved in the manuscripts under retained interfaces. U_em remains unresolved.'}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
