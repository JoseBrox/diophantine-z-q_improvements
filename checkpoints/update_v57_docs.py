from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]/'research-repo'
p=ROOT/'data/results_20261117_v57.json'
d=json.loads(p.read_text())
d['verification_script']='scripts/verify_v57.py'
d['execution_record']='data/audits/integration_20261117_v57.json'
d['proof_guide']='docs/results_20261117_v57.md'
d.pop('verification',None)
p.write_text(json.dumps(d,indent=2)+'\n')

p=ROOT/'README.md';s=p.read_text()
contrib=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',s).group()
assert hashlib.sha256(contrib.encode()).hexdigest()=='bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'
s=s.replace('data/results_20261117_v56.json','data/results_20261117_v57.json').replace('docs/results_20261117_v56.md','docs/results_20261117_v57.md')
needle='### A prepared pole block with coefficient height four\n'
addition=r'''### Variable square classes with controlled height

The [variable-class theorem](papers/pole_parameters/variable_squareclasses_20261117_v57.tex) allows each conditional native radicand to use a positive exceptional-unit multiple of any class in

```math
\{1,\ (X^2+B)^2+\operatorname{Tr}(x(A))^2,\ 1+X^4\}.
```

The varying classes may have prime support outside the exceptional set. Their height budget is absorbed by stronger source powers, with no new coordinate or guard. Under ordinary abc, the two-cover choice has exponent **6** and contraction $135/136$; the single-cover argument has degree **224** and contraction $103006635/103133368$. These optimize the stated even-power height criteria, not the complete defining degree. The nine-coordinate census remains conditional on actual rational realization for every integer input. **That realization is unproved**, and no unrestricted 21-variable transfer of these varying classes is asserted.

'''
assert needle in s;s=s.replace(needle,addition+needle)
old='It retains two free coordinates per pole; a complete replacement in a defining source still requires that source\'s preparation audit.'
new='It retains two free coordinates per pole. The complete [general source transfer](papers/pole_parameters/general_intrinsic_transfer_20261117_v57.tex) and [conditional source transfer](papers/pole_parameters/conditional_intrinsic_transfer_20261117_v57.tex) verify that preparation and every character guard, retaining **25 and 13 variables**. The general transfer changes only the early scalar; the conditional transfer keeps the fast detector and uses $d=7b$. No new complete determinant-degree or coefficient bound is assigned to these source variants.'
assert old in s;s=s.replace(old,new)
needle='## Negative results\n\n'
addition=r'''The [prepared-cover obstruction](negative_results/papers/pole_parameters/prepared_sha_obstruction_20261117_v57.tex) gives $d=112/225$ for which $y^2=d((1-d)^2-s^4)$ is soluble over every completion of $\mathbb Q$ and has no rational point. An exact Cassels pairing on $E_{791}$ proves the obstruction, with two independent arithmetic certificates. This excludes the specified one-coordinate pole specialization on all prepared inputs; it does not assert that this input is an actual detector value.

The [intrinsic-specialization theorem](negative_results/papers/pole_parameters/intrinsic_specializations_20261117_v57.tex) excludes every finite rational-function menu for $s(d)$ and identifies the positive abscissa classes of the relevant rank-one congruent curves. Relations coupling both pole coordinates and higher-rank constructions remain outside its scope.

'''
assert needle in s;s=s.replace(needle,needle+addition)
s=s.replace('    python -B scripts/verify_v56.py','    python -B scripts/verify_v57.py\n    python -B scripts/verify_v56.py',1)
assert re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',s).group()==contrib
assert r'\(' not in s and r'\[' not in s
p.write_text(s)

p=ROOT/'docs/research_directions.md';s=p.read_text()
needle='## A single-cover route and finite square-class choices\n\n'
addition=r'''The [height-controlled class theorem](../papers/pole_parameters/variable_squareclasses_20261117_v57.tex) broadens the conditional target to the menu $\{1,(X^2+B)^2+\operatorname{Tr}(x(A))^2,1+X^4\}$, with fixed positive exceptional-unit multipliers. The class support may vary with the input and root point. The contact primes lost to it have a proved height budget, so suitable larger powers retain soundness and the nine-coordinate census. The missing step remains simultaneous **rational realization on actual detector tuples**, with the prescribed root index and all source guards. Local filters do not prove it.

The [prepared-cover obstruction](../negative_results/papers/pole_parameters/prepared_sha_obstruction_20261117_v57.tex) rules out the proposed specialization $q_0=0$ uniformly: $d=112/225$ yields an everywhere locally soluble genus-one curve without a rational point. The [finite-menu obstruction](../negative_results/papers/pole_parameters/intrinsic_specializations_20261117_v57.tex) also excludes prescribing $s$ from finitely many rational functions of $d$. A viable coordinate relation must use a more restricted actual-input locus or couple the two pole coordinates in a way that evades these precise obstructions. Positive rank alone does not supply the required abscissa class.

'''
assert needle in s;s=s.replace(needle,needle+addition)
s=s.replace('Its use in a full source requires the complete preparation audit.','The complete [general](../papers/pole_parameters/general_intrinsic_transfer_20261117_v57.tex) and [conditional](../papers/pole_parameters/conditional_intrinsic_transfer_20261117_v57.tex) transfers supply those preparation and all-character audits, with unchanged counts.')
s=s.replace('[current proof guide](results_20261116_v53.md)','[current proof guide](results_20261117_v57.md)')
p.write_text(s)

p=ROOT/'negative_results/README.md';s=p.read_text()
needle='| Manuscript | Result and scope |\n|:--|:--|\n'
addition='| [A prepared covering obstruction](papers/pole_parameters/prepared_sha_obstruction_20261117_v57.tex) | The prepared input $112/225$ gives an everywhere locally soluble one-coordinate pole curve without a rational point; an exact Cassels pairing excludes the required abscissa class. No actual detector tuple is asserted. |\n| [Intrinsic specializations](papers/pole_parameters/intrinsic_specializations_20261117_v57.tex) | No finite rational-function menu for the second coordinate works on all prepared inputs. The rank-one class theorem restricts the specified congruent curves; adaptive relations and higher rank remain possible. |\n'
assert needle in s;s=s.replace(needle,needle+addition,1);p.write_text(s)
p=ROOT/'negative_results/data/results.json';data=json.loads(p.read_text());data['schema']='diophantine-negative-results/v57'
for t in d['new_negative_results']:
 data['theorems'].append(dict(t,proved=True))
p.write_text(json.dumps(data,indent=2)+'\n')

p=ROOT/'CITATION.cff';s=p.read_text().replace('2026.11.17-v56','2026.11.17-v57')
s=s.replace('square-class menus and a degree-nine prepared pole block of coefficient\n  height four.', 'square-class menus, height-controlled variable classes and complete\n  source transfers of a degree-nine pole block of coefficient height four.\n  Separate obstructions include a prepared genus-one cover certified by\n  an exact Cassels pairing.')
p.write_text(s)
p=ROOT/'THIRD_PARTY.md';s=p.read_text()
s+='''\n## Intrinsic source transfers and prepared descent obstructions\n\nThe complete intrinsic source transfers use A. Burungale, *A Diophantine definition of Z in Q*, arXiv:2611.16130v1, Theorem B, in the exact prepared-input form stated in the repository intrinsic-pole paper. The other source arithmetic premises remain explicit. The new source variants have no separately certified numerical full determinant bound.\n\nThe prepared covering obstruction uses the full 2-descent, Monsky-matrix and Cassels-pairing conventions in Z. Wang, *Congruent Elliptic Curves with Non-trivial Shafarevich-Tate Groups*, arXiv:1511.03810v2, Sections 2.1–2.2 ([primary paper](https://arxiv.org/pdf/1511.03810)), and S. Zhang, *On non-congruent numbers as multiples of non-congruent numbers*, 28 August 2025, Sections 2.1–2.2 ([author manuscript](https://zhangshenxing.github.io/publications/Zhang2025.pdf)). Its specific conics, tangent identities, all-prime local factors and Mordell–Weil point are proved and exactly checked in this repository. The proof does not infer rank from a numerical L-value or assume finiteness of the Tate–Shafarevich group.\n'''
p.write_text(s)
p=ROOT/'.github/workflows/verify.yml';s=p.read_text()
needle='      - name: Verify single-cover criteria, intrinsic poles, precision transfer and inert obstruction\n'
assert needle in s
s=s.replace(needle,'      - name: Verify intrinsic transfers, variable classes and exact prepared descent obstruction\n        run: python -B scripts/verify_v57.py --report /tmp/v57-verification.json\n'+needle)
p.write_text(s)
print('Updated current guides, preserved contribution text, and registered verification')
