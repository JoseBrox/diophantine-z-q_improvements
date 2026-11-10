from pathlib import Path
import copy
import hashlib
import json
import re

ROOT = Path('/workspace/scratch/191d4e871efa/repo')

def read(path):
    return (ROOT/path).read_text()

def write(path, value):
    (ROOT/path).write_text(value)

def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def savejson(path, data):
    write(path, json.dumps(data, indent=2)+'\n')

paper_replacements = {
    'quartic228_20261110_v19': 'quartic226_20261110_v21',
    'quartic265_20261110_v19': 'quartic262_20261110_v21',
}
current_docs = ['README.md', 'CITATION.cff', 'docs/arithmetic_inputs.md',
                'docs/research_directions.md', 'docs/reproducibility.md',
                'docs/data_format.md', 'computation/quartic/README.md']
for path in current_docs:
    s = read(path)
    for old, new in paper_replacements.items():
        s = s.replace(old, new)
    # Current prose and tables; executable dependency names stay unchanged.
    s = re.sub(r'(?<![\w])228(?![\w])', '226', s)
    s = re.sub(r'(?<![\w])265(?![\w])', '262', s)
    for old,new in [('2,829','2,835'),('3,485','3,494'),('2829','2835'),('2830','2836'),
                    ('3485','3494'),('3486','3495')]:
        s = s.replace(old,new)
    s = s.replace('**202**', '**200**').replace('**237**', '**234**')
    s = s.replace('| 202 |', '| 200 |').replace('| 237 |', '| 234 |')
    s = s.replace('237 primitive quadratic', '234 primitive quadratic')
    s = s.replace('237 quadratic rows', '234 quadratic rows')
    write(path,s)

s=read('README.md')
needle='### Fully specified parameters\n'
addition=r'''The contact equations use the inverse weight already present in each detector. Write

$$P_5(r)=r^5-e_1r^4+e_2r^3-e_3r^2+e_4r-e_5.$$

With $qs_1=1$, the three outputs $r,u,v$ satisfy

$$u=r^2,\qquad v=ru-e_1(1+s_1)u+e_2(1+s_1)r,$$
$$uv=(1+s_1)(e_3u-e_4r+e_5).$$

These quadratic equations are equivalent to $(1+q)P_5(r)=r^5$ on the entire rational zero set, including $r=0$. No coordinate storing $P_5(r)$ is needed. The full independent reconstruction checks all changed rows, every retained row, and all quartic coefficients.

'''
assert needle in s
s=s.replace(needle,addition+needle)
needle='## Current papers\n'
addition=r'''The [quadratic-cover theorem](papers/pole_parameters/quadratic_contact_covers_20261110_v21.pdf) treats algebraic parity conditions. For every rational $a>4$, the curve $z^2=dR(\lambda)R(a\lambda)$ has genus four. Hence only finitely many rational slopes at a fixed scale have equal odd contact sets outside a fixed finite set of primes. The negative-square condition gives the soundness implication needed by a proposed one-pole construction, but completeness remains unproved. The explicit negative-square section fails the elliptic comparison conditions for infinitely many odd input shifts; an exact inert-prime certificate proves that assertion. These are obstructions to specified simplifications, with no new defining variable count.

'''
s=s.replace(needle,addition+needle)
s=s.replace('[rational contact parity](papers/pole_parameters/rational_combinations_of_contacts_20261110_v20.pdf),', '[rational contact parity](papers/pole_parameters/rational_combinations_of_contacts_20261110_v20.pdf), [quadratic contact covers](papers/pole_parameters/quadratic_contact_covers_20261110_v21.pdf),')
s=s.replace('The polynomial-release receipts are [standard-library verification](data/verification-standard-v19.json) and [verification including PARI](data/verification-v19.json).', 'The current release receipt is [standard-library verification](data/verification-standard-v21.json). The unchanged elliptic rank, descent, and function-field dependencies also have a [verification receipt including PARI](data/verification-v19.json).')
write('README.md',s)

s=read('computation/quartic/README.md')
s=s.replace('| family228_v19 |', '| family226_v21 |').replace('| family265_v19 |', '| family262_v21 |')
s=s.replace('python3 computation/quartic/check_quartic265_v19.py\n', 'python3 computation/quartic/check_quartic265_v19.py\npython3 computation/quartic/build_inverse_contact_v21.py\npython3 computation/quartic/check_inverse_contact_v21.py\n')
s=s.replace('In the 226-variable construction this eliminates five field coordinates.', 'In the 226-variable construction this expresses five field fourth powers through existing squares.')
needle='## The abc family\n'
addition=r'''## Quadratic contact equations

Let $P_5(r)=r^5-e_1r^4+e_2r^3-e_3r^2+e_4r-e_5$, where its five roots are the squared distances of the contact pairs from one. The inverse weight $s_1=q^{-1}$ already occurs in the local factors. Three outputs suffice:

$$r=(t-1)^2,\qquad u=r^2,$$
$$v=ru-e_1(1+s_1)u+e_2(1+s_1)r,\qquad
uv=(1+s_1)(e_3u-e_4r+e_5).$$

Together with $qs_1=1$, these equations are equivalent to $(1+q)P_5(r)=r^5$. They exclude $P_5(r)=0$ and preserve the boundary $r=0$, where $q=s_1=-1$. The removed polynomial output has no use elsewhere in the source. The 226- and 262-variable systems have respectively 200 and 234 quadratic rows. The independent checker reconstructs the contact coefficients from elementary symmetric sums and verifies the general projection identity before expanding every coefficient.

'''
s=s.replace(needle,addition+needle)
s=s.replace('In particular, `family266_v19` is the pinned source of `family265_v19`,', 'In particular, `family228_v19` and `family265_v19` are the pinned sources of the three-output contact constructions. The table `family266_v19` is the pinned source of `family265_v19`,')
write('computation/quartic/README.md',s)

s=read('docs/data_format.md')
s=s.replace('The leading tables are in `computation/quartic/family228_v19`, `family265_v19`,', 'The leading tables are in `computation/quartic/family226_v21`, `family262_v21`,')
old='The 226- and 91-variable quadratic tables use `integer-quadratic-family-reciprocal-factors-v19`; their expanded quartics use `integer-quartic-family-reciprocal-factors-v19`. The four-factor 262-variable tables use `integer-quadratic-family-four-factors-v19` and `integer-quartic-family-four-factors-v19`.'
new='The 226- and 262-variable quadratic tables use `integer-quadratic-family-inverse-contact-v21`; their expanded quartics use `integer-quartic-family-inverse-contact-v21`. The 91-variable tables use `integer-quadratic-family-reciprocal-factors-v19` and `integer-quartic-family-reciprocal-factors-v19`.'
assert old in s;s=s.replace(old,new)
s=s.replace('The 262-variable construction reads `family266_v19`,', 'The four-factor source `family265_v19` reads `family266_v19`,')
needle='## Few-variable specifications\n'
s=s.replace(needle,'The final contact builder `build_inverse_contact_v21.py` reads the pinned systems `family228_v19` and `family265_v19`. It replaces four stored contact outputs by three using the existing inverse weight. The independent checker `check_inverse_contact_v21.py` proves the projection identity, treats the zero boundary, checks that removed outputs have no other uses, compares all retained rows, and reconstructs every expanded coefficient.\n\n'+needle)
write('docs/data_format.md',s)

s=read('docs/arithmetic_inputs.md')
s=s.replace('family265_v19/independent-verification265-v19.json','family262_v21/independent-verification262-v21.json')
write('docs/arithmetic_inputs.md',s)
s=read('docs/reproducibility.md')
s=s.replace('python3 computation/quartic/check_quartic265_v19.py\n','python3 computation/quartic/check_quartic265_v19.py\npython3 computation/quartic/build_inverse_contact_v21.py\npython3 computation/quartic/check_inverse_contact_v21.py\n')
s+='\n## Quadratic contact covers\n\nThe exact section identities, the ten branch points, and the inert-prime obstruction are verified by:\n\n~~~sh\npython3 computation/pole_parameters/check_quadratic_contact_covers.py\n~~~\n\nThe checker reconstructs the trace at index three in two ways, verifies the finite-field annihilator and congruence modulo the inert prime squared, and checks the two odd contact valuations. The paper proves the infinite progression and the genus and finiteness theorems separately. No computation asserts the completeness of a one-pole definition.\n'
write('docs/reproducibility.md',s)
s=read('docs/research_directions.md')
needle='No construction below thirteen total variables under abc is established.\n'
addition=r'''The [quadratic-cover theorem](../papers/pole_parameters/quadratic_contact_covers_20261110_v21.pdf) makes the distinction precise. Adding $z^2=-R(\lambda)R(a\lambda)$ does force equality of the odd contact radicals and proves soundness with one pole under the same weak abc premise. For each fixed $a>4$, however, its curve has genus four; equality of odd contact sets outside any fixed finite prime set permits only finitely many rational slopes. The usual prime-selection argument therefore cannot supply an unbounded slope family on this cover. Its explicit rational section also fails the comparison tests for infinitely many odd shifts, by an inert-prime obstruction. A successful route must prove an arithmetic existence statement for other cover points, change the contact geometry, or avoid requiring equality of the two entire parity sets.

'''
assert needle in s;s=s.replace(needle,addition+needle)
write('docs/research_directions.md',s)

# Promote the new constructions, retaining exact computational dependencies.
path='data/results.json';D=json.loads(read(path))
for old,new,rows,monomials in [(228,226,200,2835),(265,262,234,3494)]:
    entry=next(d for d in D['constructions'] if d['total_variables']==old)
    dependency=copy.deepcopy(entry)
    dependency['role']='Pinned source for the inverse-weight contact equations.'
    dependency.pop('proof',None);dependency.pop('local_test_proof',None)
    D['reconstruction_dependencies'].append(dependency)
    entry['id']=entry['id'].replace(str(old),str(new))
    entry.update(total_variables=new,quadratic_residuals=rows,ordinary_monomials=monomials,
                 coefficient_parameter_terms=monomials+1)
    folder=f'computation/quartic/family{new}_v21'
    entry['computation']=folder
    entry['exact_height_data']=f'{folder}/independent-verification{new}-v21.json'
    for key in ('proof','local_test_proof'):
        entry[key]=entry[key].replace(f'quartic{old}_20261110_v19',f'quartic{new}_20261110_v21')
    entry['polynomial_sha256']=digest(f'{folder}/polynomial-family{new}-v21.json')
    entry['residuals_sha256']=digest(f'{folder}/quadratic-family{new}-v21.json')
    entry['contact_outputs_per_detector']=3
    entry['contact_equations']='r=(t-1)^2; u=r^2; v=r*u-e1*(1+s1)*u+e2*(1+s1)*r; u*v=(1+s1)*(e3*u-e4*r+e5)'
    entry['contact_projection_scope']='Exact on the whole rational zero set with q*s1=1, including r=0.'
D['unconditional_theorems'].append({
    'id':'quadratic_contact_cover_obstructions',
    'proof':'papers/pole_parameters/quadratic_contact_covers_20261110_v21.tex',
    'pdf':'papers/pole_parameters/quadratic_contact_covers_20261110_v21.pdf',
    'certificate':'computation/pole_parameters/quadratic-contact-covers-certificate.json',
    'product_cover_genus':4,'scale_domain':'Every rational a>4',
    'single_contact_cover_genus':2,
    'finiteness':'At each fixed scale and finite prime set, only finitely many admissible rational slopes have equal odd contact sets.',
    'section_obstruction_prime':315467,
    'section_obstruction_shifts':'B=3+k*62790389880761304, k>=0, at integer input X=0',
    'scope':'Genus, finiteness and the inert-prime comparison obstruction are unconditional. The separately stated one-pole soundness implication retains weak abc and the original arithmetic premises; its converse is open. No new defining variable count.'
})
savejson(path,D)

path='computation/quartic/PROVENANCE.json';P=json.loads(read(path))
for old,new,oldkey,newkey,rows,monomials in [(228,226,'family228_v19','family226_v21',200,2835),(265,262,'specified265_v19','specified262_v21',234,3494)]:
    oldentry=P['finalConstructions'].pop(oldkey)
    dependency=copy.deepcopy(oldentry);dependency['role']='Pinned source for the inverse-weight contact construction.'
    P['reconstructionDependencies'][oldkey]=dependency
    entry=copy.deepcopy(oldentry)
    entry.update(totalVariables=new,quadraticResiduals=rows,symbolicTerms=monomials+1)
    entry['ordinaryMonomials']['count']=monomials
    for key in ('quadraticSystem','polynomial','constructionReport','independentVerification'):
        entry[key]=entry[key].replace(f'family{old}_v19',f'family{new}_v21').replace(f'{old}-v19',f'{new}-v21')
    entry['quadraticSystemSHA256']=digest('computation/quartic/'+entry['quadraticSystem'])
    entry['polynomialSHA256']=digest('computation/quartic/'+entry['polynomial'])
    entry['contactOutputsPerDetector']=3
    entry['contactProjection']='Exact with the retained inverse weight, including r=0; no polynomial-value coordinate.'
    P['finalConstructions'][newkey]=entry
    proof=P['proofs'].pop(oldkey)
    for ext in ('tex','pdf'):
        proof[ext]=proof[ext].replace(f'quartic{old}_20261110_v19',f'quartic{new}_20261110_v21')
        proof[ext+'_sha256']=digest('computation/quartic/'+proof[ext])
    P['proofs'][newkey]=proof
    P['mathematicalSources']['localProofs']=[newkey if k==oldkey else k for k in P['mathematicalSources']['localProofs']]
P['constructionChain'].append({'from':['family228_v19','specified265_v19'],
    'to':['family226_v21','specified262_v21'],
    'producer':'build_inverse_contact_v21.py','checker':'check_inverse_contact_v21.py',
    'change':'The existing inverse weight permits three contact outputs per detector. The rational projection is preserved on every stratum.'})
P['reproduction']['quarticCommandsFromThisDirectory']+=['python3 build_inverse_contact_v21.py','python3 check_inverse_contact_v21.py']
savejson(path,P)

# Only the current complete theorem papers are retained for these families.
for path in ('papers/quartic_existence/quartic228_20261110_v19','papers/quartic/quartic265_20261110_v19'):
    for ext in ('.tex','.pdf'):
        (ROOT/(path+ext)).unlink()

path='scripts/verify.py';s=read(path)
needle="        coordinate_budget=(quartic/'coordinate-budget279.json').read_bytes()\n"
addition="""        inverse_contact={path:path.read_bytes()
            for folder in ('family226_v21','family262_v21')
            for path in sorted((quartic/folder).glob('*.json'))}
        stages.append(run('226/262-variable inverse-weight contact reconstruction',
            quartic/'build_inverse_contact_v21.py'))
        stages.append(run('Independent contact projection, full rows, coefficients, and effective threshold',
            quartic/'check_inverse_contact_v21.py'))
        for path,raw in inverse_contact.items():
            assert path.read_bytes()==raw,str(path)
"""
assert needle in s;s=s.replace(needle,addition+needle)
needle="        small_tau_algebra=(poles/'small-fixed-tau17-algebra-verification.json').read_bytes()\n"
addition="""        contact_covers=(poles/'quadratic-contact-covers-certificate.json').read_bytes()
        stages.append(run('Quadratic contact covers: exact section, branch points, and inert-prime obstruction',
            poles/'check_quadratic_contact_covers.py'))
        assert (poles/'quadratic-contact-covers-certificate.json').read_bytes()==contact_covers
"""
assert needle in s;s=s.replace(needle,addition+needle)
write(path,s)
print('Integrated 226/262 quartics, coefficient thresholds, contact-cover theorem and verification stages.')
