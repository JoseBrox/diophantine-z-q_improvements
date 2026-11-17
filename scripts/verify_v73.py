#!/usr/bin/env python3
"""Reproduce the complete 194-coordinate quartic and its exact certificates."""
import argparse,hashlib,json,platform,re,shutil,subprocess,sys,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PACKAGE='computation/quartic/cleared_comparisons194_v73'
PAPER='papers/quartic/quartic194_20261117_v73.tex'
CONTRIBUTORS_HASH='bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(folder,*args):
    r=subprocess.run([sys.executable,'-B',*map(str,args)],cwd=folder,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)

def main(output):
    package=ROOT/PACKAGE
    manifest=json.loads((package/'manifest.json').read_text())
    for name,value in manifest.items():assert digest(package/name)==value,name
    with tempfile.TemporaryDirectory(prefix='diophantine-v73-')as d:
        copied=Path(d)/'package';shutil.copytree(package,copied)
        run(copied,'build.py');run(copied,'verify_height.py')
        run(copied,'check_support.py','--output','support-certificate.json')
        run(copied,'check_arithmetic.py')
        for folder,extra in [('primitive',['--primitive-reference']),('fewer_monomials',[])]:
            run(copied,'check.py','--folder',folder,*extra,'--output',folder+'/independent-verification.json')
            for name in ['quadratic-family.json','polynomial-family.json','laurent-source.json',
                         'transformation.json','construction-report.json','mixed-coefficients.json',
                         'independent-verification.json']:
                assert (copied/folder/name).read_bytes()==(package/folder/name).read_bytes(),(folder,name)
        for name in ['support-certificate.json','arithmetic-certificate.json']:
            assert (copied/name).read_bytes()==(package/name).read_bytes(),name
    variants=[]
    for folder,monomials,terms,crossover in [('primitive',2765,2772,4),('fewer_monomials',2621,2628,7)]:
        q=json.loads((package/folder/'independent-verification.json').read_text())
        assert q['status']=='PASS' and q['variables']==194
        assert q['normalized_quadratic_rows']==168 and q['literal_unit_guards']==6
        assert q['explicit_physical_component_rows']==q['retained_source_rows']==81
        assert q['coordinate_monomials_at_C_149_power_N']==monomials
        assert q['parameter_separated_terms']==terms and q['degree']==4
        assert q['content_for_each_positive_integral_C']==1 and q['every_coordinate_occurs']
        assert q['all_row_pullbacks_exact'] and q['independent_sum_of_squares_expansion']
        assert q['coefficient_height_audit']['constant_to_quartic_crossover_N']==crossover
        variants.append({'basis':folder,'monomials':monomials,'parameter_terms':terms,
                         'height':q['coefficient_height_audit']['formula'],
                         'quartic_sha256':digest(package/folder/'polynomial-family.json')})
    arithmetic=json.loads((package/'arithmetic-certificate.json').read_text())
    assert arithmetic['status']=='PASS' and len(arithmetic['factor_table'])==10
    assert arithmetic['input_error_minimum_depth']==2
    assert arithmetic['height_argument_uses_input_depth']==1
    assert arithmetic['completeness_contact_depth']==1
    assert arithmetic['homogeneous_lucas_identity']
    records=json.loads((ROOT/'data/results_20261117_v73.json').read_text())
    current={r['id']:r for r in records['current_constructions']}
    old={r['id']:r for r in json.loads((ROOT/'data/results_20261117_v72.json').read_text())['current_constructions']}
    prior=old.pop('quartic195');new=current.pop('quartic194')
    assert old==current and prior['variables']==195 and new['variables']==194
    assert new['degree']==4 and new['quadratic_rows']==168 and new['monomials']==2765
    assert new['proof']==PAPER and new['data']==PACKAGE and not new['parameter_effective']
    assert new['alternative_reference_basis']['monomials']==2621
    assert records['new_variable_reduction']
    for key in ['targets_21_and_9_proved','all_number_fields_definition_established',
                'number_field_counterexample_established','arithmetic_foundations_complete_independent_audit']:
        assert records[key]is False,key
    review=json.loads((package/'independent_review.json').read_text())
    for key,path in [('manuscript_sha256',ROOT/PAPER),('review_sha256',package/'independent_review.md'),
                     ('producer_sha256',package/'build.py'),('checker_sha256',package/'check.py'),
                     ('arithmetic_checker_sha256',package/'check_arithmetic.py')]:
        assert review[key]==digest(path),key
    assert review['status']=='PASS' and not review['global_21_or_9_realization_proved']
    for item in review['retained_sources']:
        assert digest(ROOT/item['path'])==item['sha256'],item['path']
    build=json.loads((ROOT/'data/audits/tex_build_20261117_v73.json').read_text())['papers']
    assert len(build)==1
    b=build[0]
    assert b['paper']==PAPER and b['source_sha256']==digest(ROOT/PAPER)
    assert b['returncode']==0 and b['warnings']==[] and b['pages']>0
    assert b['all_rendered_pages_reviewed']
    readme=(ROOT/'README.md').read_text()
    section=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest()==CONTRIBUTORS_HASH
    for name in ['README.md','negative_results/README.md',PACKAGE+'/README.md','docs/results_20261117_v73.md']:
        text=(ROOT/name).read_text()
        assert '$'not in text and r'\operatorname'not in text,name
    assert '**194**'in readme and '2,765'in readme and '2,621'in readme
    link=re.search(r'\[results JSON\]\((data/results_[^)]*\.json)\)',readme)
    assert link
    latest=json.loads((ROOT/link.group(1)).read_text())
    latest194=next(r for r in latest['current_constructions']if r['id']=='quartic194')
    assert latest194==new
    assert 'docs/results_20261117_v73.md'in readme
    report={'schema':'diophantine-exact-verification/v73','status':'PASS','python':platform.python_version(),
            'total_variables':194,'quadratic_rows':168,'degree':4,'integer_content':1,'variants':variants,
            'manuscript_sha256':digest(ROOT/PAPER),'complete_integer_family_under_retained_premises':True,
            'sufficient_defining_parameter_effective':False,'global_21_or_9_realization_proved':False,
            'arithmetic_foundations_complete_independent_audit':False}
    if output:Path(output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report');main(ap.parse_args().report)
