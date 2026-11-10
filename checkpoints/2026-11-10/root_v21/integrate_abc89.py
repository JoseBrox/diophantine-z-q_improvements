from pathlib import Path
import copy
import hashlib
import json
import re

ROOT=Path('/workspace/scratch/191d4e871efa/repo')
def read(path):return (ROOT/path).read_text()
def write(path,s):(ROOT/path).write_text(s)
def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def save(path,d):write(path,json.dumps(d,indent=2)+'\n')

for path in ['README.md','CITATION.cff','docs/arithmetic_inputs.md','docs/data_format.md',
             'docs/reproducibility.md','docs/research_directions.md','computation/quartic/README.md']:
    s=read(path).replace('quartic_abc91_20261110_v19','quartic_abc89_20261110_v21')
    s=re.sub(r'(?<![\w])91(?![\w])','89',s).replace('ninety-one','eighty-nine')
    s=s.replace('797683','797681')
    s=re.sub(r'(?<![0-9])926(?![0-9])','936',s)
    s=re.sub(r'(?<![0-9])927(?![0-9])','937',s)
    s=s.replace('**79**','**77**').replace('| 79 |','| 77 |')
    s=s.replace('79 primitive quadratic','77 primitive quadratic').replace('79 quadratic','77 quadratic')
    s=s.replace('family_abc91_v19','family_abc89_v21')
    write(path,s)

path='computation/quartic/README.md';s=read(path)
s=s.replace('python3 computation/quartic/check_inverse_contact_v21.py\n',
            'python3 computation/quartic/check_inverse_contact_v21.py\npython3 computation/quartic/build_abc_inverse_contact_v21.py\npython3 computation/quartic/check_abc_inverse_contact_v21.py\n')
start=s.index('The reciprocal coordinates satisfy\n',s.index('## The abc family'))
end=s.index('The sufficient odd input shift remains ineffective.',start)
s=s[:start]+r'''Write $r=(t-1)^2$ and $P_4(r)=(r-1)(r-4)(r-9)(r-16)$. Three shifted contact outputs $r_0,u_0,v_0$ and three weights satisfy

$$r_0=t^2-2t,\quad u_0=r_0^2+2r_0,\quad
(u_0-30r_0-v_0)s_2=(r_0+1)s_3,$$
$$u_0v_0+v_0+244u_0-820r_0=0,\qquad
s_4=s_2^2,\quad s_3^2=s_2s_4.$$

The pair chart excludes zero weights. Setting $s=s_3/s_2$ then gives $s_j=s^j$ and $P_4(r)=sr^3$, with $r=r_0+1\ne0$. No separate coordinate for $q=1/s$ is required. The stored factors are $A_i=sT_i$, and the stored product and trace are rescaled by $s^2/r$. Their equations are quadratic, and the identity $s_3b=\eta^2$ preserves exactly the original pole input $b$. The local proof uses the recovered unscaled factors and trace. All zero strata and both directions of the rational coordinate change are proved before the arithmetic arguments.

The affine contact shifts place the origin at the contact $P_4(1)=0$. All contact-equation constant terms vanish, giving the exact height $\max(4153456,B^2+797681)$. The full independent checker reconstructs all 77 quadratic rows and 936 ordinary monomials. For odd $B\ge1833$, the height is $B^2+797681$; this is a coefficient statement.

'''+s[end:]
s=s.replace('`family228_v19` and `family265_v19` are the pinned sources of the three-output contact constructions.', '`family228_v19`, `family265_v19`, and `family_abc91_v19` are the pinned sources of the three-output contact constructions.')
write(path,s)

path='docs/data_format.md';s=read(path)
s=s.replace('The 89-variable tables use `integer-quadratic-family-reciprocal-factors-v19` and `integer-quartic-family-reciprocal-factors-v19`.',
            'The 89-variable tables use `integer-quadratic-family-abc-inverse-contact-v21` and `integer-quartic-family-abc-inverse-contact-v21`.')
needle='## Few-variable specifications\n'
paragraph='The abc contact builder `build_abc_inverse_contact_v21.py` reads the pinned `family_abc91_v19` system. It removes the two explicit weight coordinates, translates the three contact outputs per detector, and rescales the two factors, their product, and their trace. The independent checker `check_abc_inverse_contact_v21.py` proves exact recovery of the old pole input, excludes the zero strata through the unchanged pair chart, and checks every coefficient of the expanded quartic.\n\n'
s=s.replace(needle,paragraph+needle)
write(path,s)

path='docs/reproducibility.md';s=read(path)
s=s.replace('python3 computation/quartic/check_inverse_contact_v21.py\n',
            'python3 computation/quartic/check_inverse_contact_v21.py\npython3 computation/quartic/build_abc_inverse_contact_v21.py\npython3 computation/quartic/check_abc_inverse_contact_v21.py\n')
write(path,s)
path='docs/research_directions.md';s=read(path)
s=s.replace('the abc factors use $q^{-2},q^{-3},q^{-4}$.', 'the abc construction uses three weights $s^2,s^3,s^4$ with $s=1/q$, without retaining $q$ itself.')
s=s.replace('The zero-weight components are excluded in the full proofs.', 'The zero-weight components are excluded in the full proofs. Three-output contact equations also use these weights. For the abc quartic, rescaling the factor product and trace preserves the original pole input exactly; affine contact shifts reduce the coefficient height.')
write(path,s)

path='data/results.json';D=json.loads(read(path))
entry=next(x for x in D['additional_hypothesis_constructions'] if x['total_variables']==91)
dependency=copy.deepcopy(entry)
dependency['role']='Pinned source for the inverse-weight abc contact construction.'
dependency.pop('proof',None);dependency.pop('local_test_proof',None)
D['reconstruction_dependencies'].append(dependency)
entry.update(id='quartic89_abc_family',total_variables=89,quadratic_residuals=77,
             ordinary_monomials=936,coefficient_parameter_terms=937)
folder='computation/quartic/family_abc89_v21'
entry['computation']=folder
entry['exact_height_data']=folder+'/independent-verification-abc89-v21.json'
for key in ('proof','local_test_proof'):
    entry[key]='papers/quartic_existence/quartic_abc89_20261110_v21.tex'
entry['polynomial_sha256']=digest(folder+'/polynomial-family-abc89-v21.json')
entry['residuals_sha256']=digest(folder+'/quadratic-family-abc89-v21.json')
entry['exact_coefficient_height']='max(4153456,B^2+797681)'
entry['eventual_coefficient_height']='B^2+797681'
entry['factor_clearing']='Store A_i=s*T_i, (r0+1)*Omega=A_1*A_2, and the scaled trace eta; s3*b=eta^2 preserves the original pole input.'
entry['contact_outputs_per_detector']=3
entry['contact_coordinates']=['r0=(t-1)^2-1','u0=(r0+1)^2-1','v0=xi+29']
entry['inverse_weights']=['s2=s^2','s3=s^3','s4=s^4; s=s3/s2=1/q']
entry['contact_projection_scope']='Exact on the entire rational solution set, preserving all unchanged point and pole coordinates and the pole input b.'
entry['stored_weight_q']=False
D['construction_scope']['effectiveness']=D['construction_scope']['effectiveness'].replace('91','89')
save(path,D)

path='computation/quartic/PROVENANCE.json';P=json.loads(read(path))
old=P['finalConstructions'].pop('familyABC91_v19')
dependency=copy.deepcopy(old);dependency['role']='Pinned source for the inverse-weight abc contact construction.'
P['reconstructionDependencies']['familyABC91_v19']=dependency
entry=copy.deepcopy(old)
entry.update(totalVariables=89,quadraticResiduals=77,symbolicTerms=937)
entry['ordinaryMonomials']['count']=936
entry['exactCoefficientHeight']['expression']='max(4153456,B^2+797681)'
for key in ('quadraticSystem','polynomial','constructionReport','independentVerification'):
    entry[key]=entry[key].replace('family_abc91_v19','family_abc89_v21').replace('abc91-v19','abc89-v21')
entry['quadraticSystemSHA256']=digest('computation/quartic/'+entry['quadraticSystem'])
entry['polynomialSHA256']=digest('computation/quartic/'+entry['polynomial'])
entry['localFactors']='Three inverse weights and rescaled factors, product and trace; the original pole input is preserved exactly.'
entry['contactOutputsPerDetector']=3
entry['affineContactCoordinates']=['r0=r-1','u0=r^2-1','v0=xi+29']
P['finalConstructions']['familyABC89_v21']=entry
proof=P['proofs'].pop('familyABC91_v19')
for ext in ('tex','pdf'):
    proof[ext]=proof[ext].replace('quartic_abc91_20261110_v19','quartic_abc89_20261110_v21')
    proof[ext+'_sha256']=digest('computation/quartic/'+proof[ext])
P['proofs']['familyABC89_v21']=proof
P['mathematicalSources']['localProofs']=['familyABC89_v21' if x=='familyABC91_v19' else x for x in P['mathematicalSources']['localProofs']]
P['constructionChain'].append({'from':'familyABC91_v19','to':'familyABC89_v21',
    'producer':'build_abc_inverse_contact_v21.py','checker':'check_abc_inverse_contact_v21.py',
    'change':'Three shifted contact outputs per detector and rescaled factors, product and trace preserve the original pole input and the whole rational projection.'})
P['reproduction']['quarticCommandsFromThisDirectory']+=['python3 build_abc_inverse_contact_v21.py','python3 check_abc_inverse_contact_v21.py']
save(path,P)

for ext in ('.tex','.pdf'):
    (ROOT/('papers/quartic_existence/quartic_abc91_20261110_v19'+ext)).unlink()

path='scripts/verify.py';s=read(path)
needle="        coordinate_budget=(quartic/'coordinate-budget279.json').read_bytes()\n"
addition="""        abc_inverse={path:path.read_bytes() for path in
            sorted((quartic/'family_abc89_v21').glob('*.json'))}
        stages.append(run('89-variable abc inverse-contact quadratic reconstruction',
            quartic/'build_abc_inverse_contact_v21.py'))
        stages.append(run('Independent abc contact, factor, trace and pole equivalence and full coefficients',
            quartic/'check_abc_inverse_contact_v21.py'))
        for path,raw in abc_inverse.items():
            assert path.read_bytes()==raw,str(path)
"""
assert needle in s;s=s.replace(needle,addition+needle);write(path,s)
print('Integrated the shifted abc89 quartic, exact height and verification stages.')
