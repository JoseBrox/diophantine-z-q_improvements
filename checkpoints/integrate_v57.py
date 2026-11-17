from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'research-repo'

papers = {
 'checkpoints/general_scalar_v56/burungale_scalar_transfer_20261117_v56.tex':
 'papers/pole_parameters/general_intrinsic_transfer_20261117_v57.tex',
 'checkpoints/single_cover_realization_v56/conditional_burungale_transfer.tex':
 'papers/pole_parameters/conditional_intrinsic_transfer_20261117_v57.tex',
 'checkpoints/variable_classes_v57/variable_squareclasses.tex':
 'papers/pole_parameters/variable_squareclasses_20261117_v57.tex',
 'checkpoints/independent_route_v56/negative_results/intrinsic_specialization_obstructions.tex':
 'negative_results/papers/pole_parameters/intrinsic_specializations_20261117_v57.tex',
 'checkpoints/independent_route_v56/negative_results/prepared_q0_sha_counterexample.tex':
 'negative_results/papers/pole_parameters/prepared_sha_obstruction_20261117_v57.tex',
}
for source, destination in papers.items():
    text = (BASE/source).read_text()
    text = text.replace(r'\nolinkurl{precision_transfer_20261117_v56.tex}',
                        r'\nolinkurl{papers/pole_parameters/precision_transfer_20261117_v56.tex}')
    text = text.replace(r'\nolinkurl{intrinsic_burungale_pole.tex}',
                        r'\nolinkurl{papers/pole_parameters/intrinsic_pole_20261117_v56.tex}')
    text = text.replace('The physical weights still have positive odd valuations everywhere\noutside the fixed exceptional set.',
                        'Every odd valuation of a physical weight outside the fixed\nexceptional set is still positive.')
    if destination.startswith('negative_results/'):
        old = r'\documentclass[11pt]{article}'+'\n'+r'\usepackage{amsmath,amssymb,amsthm,hyperref}'
        new = r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb,amsthm,microtype}
\usepackage[margin=27mm]{geometry}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}
\setlength{\emergencystretch}{2em}'''
        assert old in text
        text = text.replace(old, new)
    p = ROOT/destination
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

def adapt(source, destination, old_filename, certificate_variable, independent=False):
    text = (BASE/source).read_text()
    text = text.replace('import json\n', 'import json\nimport argparse\n', 1)
    declaration = "parser = argparse.ArgumentParser(description=__doc__)\nparser.add_argument('--output', type=Path)\nargs = parser.parse_args()\n"
    marker = "Path(__file__).with_name('" + old_filename + "')"
    if independent:
        assert 'out = '+marker in text
        text = text.replace('out = '+marker, declaration+"out = args.output or Path(__file__).with_name('independent_certificate.json')\nout.parent.mkdir(parents=True, exist_ok=True)")
    else:
        assert marker in text
        text = text.replace(marker, "out")
        pos = text.index('out.write_text(')
        text = text[:pos]+declaration+"out = args.output or Path(__file__).with_name('certificate.json')\nout.parent.mkdir(parents=True, exist_ok=True)\n"+text[pos:]
    p = ROOT/destination
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

adapt('checkpoints/general_scalar_v56/check_scalar_seven_transfer.py',
      'computation/pole_parameters/intrinsic_source_transfers_v57/check.py',
      'scalar_seven_transfer_certificate.json', 'result')
adapt('checkpoints/independent_route_v56/negative_results/check_intrinsic_specialization_obstructions.py',
      'negative_results/computation/intrinsic_specializations_v57/check.py',
      'intrinsic_specialization_obstructions_certificate.json', 'certificate')
adapt('checkpoints/independent_route_v56/negative_results/check_prepared_q0_sha_counterexample.py',
      'negative_results/computation/prepared_sha_v57/check.py',
      'prepared_q0_sha_counterexample_certificate.json', 'certificate')
adapt('checkpoints/general_scalar_v56/check_prepared_q0_independent.py',
      'negative_results/computation/prepared_sha_v57/independent_check.py',
      'prepared_q0_independent_certificate.json', 'cert', independent=True)
p = ROOT/'computation/pole_parameters/variable_squareclasses_v57/check.py'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text((BASE/'checkpoints/variable_classes_v57/check.py').read_text())

packages = [
 'computation/pole_parameters/intrinsic_source_transfers_v57',
 'computation/pole_parameters/variable_squareclasses_v57',
 'negative_results/computation/intrinsic_specializations_v57',
 'negative_results/computation/prepared_sha_v57',
]
for relative in packages:
    p = ROOT/relative
    r = subprocess.run([sys.executable, '-B', str(p/'check.py'), '--output', str(p/'certificate.json')],
                       cwd=ROOT, text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stdout+r.stderr)
    print('Checked', relative)
p = ROOT/packages[-1]
r = subprocess.run([sys.executable, '-B', str(p/'independent_check.py'), '--output', str(p/'independent_certificate.json')],
                   cwd=ROOT, text=True, capture_output=True)
if r.returncode:
    raise RuntimeError(r.stdout+r.stderr)
print('Checked independent prepared-cover certificate')

data = json.loads((ROOT/'data/results_20261117_v56.json').read_text())
data['schema'] = 'diophantine-current-results/v57'
data['new_auxiliary_theorems'] = [
 {'id':'general_intrinsic_transfer', 'proved':True, 'variables':25,
  'new_variable_bound':False, 'proof':papers[next(iter(papers))],
  'scope':'Complete scalar-only transfer under the retained source premises and Burungale Theorem B; no new complete determinant degree bound.'},
 {'id':'conditional_intrinsic_transfer', 'proved':True, 'variables':13,
  'new_variable_bound':False, 'proof':list(papers.values())[1],
  'scope':'Complete d=7b transfer for both retained weak-abc exponents; every source and character guard included.'},
 {'id':'variable_squareclasses', 'proved':True, 'conditional_target':9,
  'new_variable_bound':False, 'proof':list(papers.values())[2],
  'scope':'Conditional soundness and finite-algebra census with height-controlled classes; uniform rational realization remains unproved.'},
]
data['variable_squareclass_realization'] = {
 'proved':False, 'menus':['1','(X^2+B)^2+Trace(x(A))^2','1+X^4'],
 'conditional_target':9, 'unrestricted_21_transfer_proved':False,
 'ordinary_abc_two_cover_exponent':6,
 'ordinary_abc_single_cover_argument_degree':224,
 'new_complete_defining_degree_bound':False,
}
data['new_negative_results'] = [
 {'id':'intrinsic_specializations', 'proof':list(papers.values())[3],
  'scope':'Finite rational-function menus for s(d), and positive abscissa classes on rank-one congruent curves; adaptive relations and higher rank remain outside the result.'},
 {'id':'prepared_sha_obstruction', 'proof':list(papers.values())[4],
  'prepared_input':'112/225', 'everywhere_locally_soluble':True,
  'has_rational_point':False,
  'scope':'The q0=0 one-coordinate specialization on prepared inputs; no assertion that the input is an actual detector tuple.'},
]
data['verification'] = 'scripts/verify_v57.py'
(ROOT/'data/results_20261117_v57.json').write_text(json.dumps(data, indent=2)+'\n')
print('Installed five manuscripts and four exact packages')
