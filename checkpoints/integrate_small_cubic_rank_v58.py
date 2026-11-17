from pathlib import Path
import hashlib
import json
import re

BASE = Path('/workspace/scratch/9f1d98902abb')
ROOT = BASE/'research-repo'
author = BASE/'checkpoints/independent_route_v56'
auditor = BASE/'checkpoints/general_scalar_v56'
package = ROOT/'computation/pole_parameters/small_trace_classes_v58'

source = (author/'check_small_cubic_rank_v58.py').read_text()
source = source.replace('small_cubic_rank_v58_coefficients.json', 'rank_coefficients.json')
source = source.replace('small_cubic_rank_v58_certificate.json', 'rank_certificate.json')
source = source.replace('    args = parser.parse_args()', '    parser.add_argument("--output", type=Path, default=CERT)\n    args = parser.parse_args()')
source = source.replace('    CERT.write_text(', '    args.output.write_text(')
(package/'check_rank.py').write_text(source)
(package/'rank_coefficients.json').write_bytes((author/'small_cubic_rank_v58_coefficients.json').read_bytes())
source = (auditor/'check_small_cubic_rank_independent_v58.py').read_text()
source = source.replace("The independently generated roots are also compared with the other\nagent's evaluated division-polynomial coefficient arrays.", "The independently generated roots are also compared with the separately\nevaluated division-polynomial coefficient arrays.")
source = source.replace('import json\n', 'import argparse\nimport json\n')
source = source.replace('AUTHOR_DATA = (HERE.parent / "independent_route_v56" /\n               "small_cubic_rank_v58_coefficients.json")', 'AUTHOR_DATA = HERE / "rank_coefficients.json"')
source = source.replace('OUTPUT = HERE / "small_cubic_rank_independent_v58_certificate.json"', 'parser = argparse.ArgumentParser(description=__doc__)\nparser.add_argument("--output", type=Path, default=HERE / "independent_rank_certificate.json")\nOUTPUT = parser.parse_args().output')
(package/'independent_rank.py').write_text(source)

paper = ROOT/'papers/pole_parameters/small_trace_classes_20261117_v58.tex'
s = paper.read_text()
s = s.replace('whole-character guards, and give the associated curve models. The', 'whole-character guards, and give the associated curve models. The smallest\ncubic has a rational point of infinite order for every rational normalized\nweight $0<w\\le1/4$. The')
s = s.replace('The curve models and reference points do not prescribe the actual\ndetector trace. No Mordell--Weil rank or actual-source realization\nis inferred from them. Their displayed coordinates are changes of\nvariables for studying the square equation, not additional free\ncoordinates in its finite-algebra encoding.', 'The displayed coordinates are changes of variables for studying the\nsquare equations, not additional free coordinates in their finite-algebra\nencoding. They do not prescribe the actual detector trace. The next\nsection proves positive rank for the smallest cubic throughout the\nnormalized range.')
section = (author/'small_cubic_rank_section_v58.tex').read_text()
s = s.replace('\\section{Whole-character guards and the construction criteria}', section+'\n\\section{Whole-character guards and the construction criteria}')
bib = (author/'small_cubic_rank_bibliography_v58.tex').read_text()
s = s.replace('\\begin{thebibliography}{9}\\raggedright', '\\begin{thebibliography}{9}\\raggedright\n'+bib)
paper.write_text(s)

readme = ROOT/'README.md'
s = readme.read_text()
match = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', s)
assert match and hashlib.sha256(match.group().encode()).hexdigest() == 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'
needle = '\nThe [joint-pole theorem]'
assert s.count(needle) == 1
paragraph = '\nFor this smallest cubic, $x=V+2$ gives $E_w:y^2=x(x^2-(w+4)x+4(w+1))$. The [same paper](papers/pole_parameters/small_trace_classes_20261117_v58.tex) proves that **$(4,4)$ has infinite order for every rational $0<w\\le1/4$**. An exact division-polynomial certificate and an independent tangent/chord calculation prove the torsion exclusions. This supplies positive rank throughout the normalized weight range; prescribing $x=2+\\operatorname{Tr}(W^{-1})$ for both actual detectors remains unproved.\n'
s = s.replace(needle, paragraph+needle)
readme.write_text(s)

guide = ROOT/'docs/results_20261117_v58.md'
s = guide.read_text()
s = s.replace('The curve models have rational reference points, but the theorem does not infer rank or actual trace matching from those points.', 'The smallest cubic also has **positive rank for every rational $0<w\\le1/4$**. Under $x=V+2$, its point $P=(4,4)$ has infinite order on\n\n$$\ny^2=x\\bigl(x^2-(w+4)x+4(w+1)\\bigr).\n$$\n\nThe proof combines Mazur\'s torsion classification with exact primitive division-polynomial data: the $8$-, $10$- and $12$-division polynomials at $P$ have leading coefficients $1$, $5$ and $3$. The rational-root theorem leaves only $w=1/5$, which is excluded modulo three. A separate tangent/chord calculation recovers exactly the same polynomial roots from the reduced denominators of $x([8]P)$, $x([10]P)$ and $x([12]P)$. The [rank certificates](../computation/pole_parameters/small_trace_classes_v58) reproduce both computations. Positive rank supplies rational points for each fixed weight; it does not prescribe the required abscissa $x=2+\\operatorname{Tr}(W^{-1})$.')
guide.write_text(s)

arithmetic = ROOT/'docs/arithmetic_inputs.md'
s = arithmetic.read_text()
s += '\nFor the smallest trace cubic, the point $(4,4)$ has infinite order for every rational $0<w\\le1/4$. This uses the same Mazur torsion theorem cited for the earlier cubic, together with exact division-polynomial and independent group-law computations. It supplies no actual prescribed-trace realization hypothesis.\n'
arithmetic.write_text(s)

strategy = ROOT/'docs/research_directions.md'
s = strategy.read_text()
s = s.replace('## The 25-coordinate budget', 'The [smallest trace cubic](../papers/pole_parameters/small_trace_classes_20261117_v58.tex) now has a proved infinite-order section $(4,4)$ for every rational normalized weight. Its equation has four radicand monomials and coefficient height four. The required construction must couple its abscissa to the actual detector trace; a free point on this positive-rank curve does not meet that obligation.\n\n## The 25-coordinate budget')
strategy.write_text(s)

third = ROOT/'THIRD_PARTY.md'
s = third.read_text()
s = s.replace('The cubic trace rank theorem uses **B. Mazur', 'The cubic trace rank theorems, including the four-term trace cubic, use **B. Mazur')
third.write_text(s)

results_path = ROOT/'data/results_20261117_v58.json'
data = json.loads(results_path.read_text())
data['trace_conic_realization']['smallest_cubic_rank'] = {
    'curve':'y^2=x*(x^2-(w+4)*x+4*(w+1))',
    'reference_point':[4,4],
    'reference_point_infinite_order_for_all_rational_0_lt_w_le_1_over_4':True,
    'positive_rank_proved':True,
    'actual_trace_matching_proved':False,
    'proof':'papers/pole_parameters/small_trace_classes_20261117_v58.tex',
    'certificate':'computation/pole_parameters/small_trace_classes_v58/rank_certificate.json',
    'independent_certificate':'computation/pole_parameters/small_trace_classes_v58/independent_rank_certificate.json'}
results_path.write_text(json.dumps(data,indent=2)+'\n')

(package/'README.md').write_text('''# Small trace classes and the cubic rank theorem

The manuscript `papers/pole_parameters/small_trace_classes_20261117_v58.tex`
proves the local, whole-character and finite-algebra claims. Its smallest
radicand is `V^3+(2-w)*V^2+4*w`. The change `x=V+2` gives
`y^2=x*(x^2-(w+4)*x+4*(w+1))`.

For every rational `0<w<=1/4`, the point `(4,4)` has infinite order.
The torsion proof uses Mazur's classification and exact rational-root
exclusions for the evaluated division polynomials of orders 8, 10 and 12.

- `check.py` verifies the class and local polynomial identities.
- `check_rank.py` uses only standard-library exact polynomial arithmetic
  to recompute every saved coefficient in `rank_coefficients.json`, the
  primitive contents and the modulo-three exclusion at `w=1/5`.
- `independent_rank.py` uses exact tangent/chord arithmetic in `Q(w)`,
  without division-polynomial recurrences, to recover the same primitive
  polynomials from reduced multiple-coordinate denominators. It requires
  SymPy 1.14.0.

Run both rank scripts with `--output PATH` to reproduce their certificates.
The integration command is `python -B scripts/verify_v58.py`.

These checks and the proved positive rank do not prescribe the abscissa
`x=2+Trace(W^-1)` of an actual detector. Simultaneous actual-trace
realization and the proposed 21/9 defining-variable bounds remain unproved.
''')
print('Integrated rank paper, exact checkers and current documentation.')
