#!/usr/bin/env python3
"""Exact residue partitions and thresholds for revised physical detector factors.

The manuscript proves the unbounded valuation implication and stated
preparation limits. This file checks finite residue arithmetic and constants,
not quadratic compilation or a complete defining polynomial.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse, hashlib, json

HERE=Path(__file__).resolve().parent
residues=[]
for mu in (1,3,5,7):
    ordinary=[{0},{(-11*mu)%4},{(-2*mu)%4},{(-mu)%4}]
    special=[{0},{(-4*mu)%8},
             {(-mu+4*r)%8 for r in (0,1)},
             {(-2*mu+4*r)%8 for r in (0,1)},
             {(-3*mu+4*r)%8 for r in (0,1)}]
    paired_comparisons=[{0},{(-9*mu)%4},{(-11*mu)%4},{(-2*mu)%4}]
    paired_reciprocals=[{0},{(-mu)%4},{(-3*mu)%4},{(-2*mu)%4}]
    for name,sets,mod in [('ordinary',ordinary,4),('special',special,8),
                          ('alternating_comparisons',paired_comparisons,4),
                          ('alternating_reciprocals',paired_reciprocals,4)]:
        assert all(not a.intersection(b) for a,b in combinations(sets,2))
        assert set.union(*sets)==set(range(mod))
        residues.append({'mu_mod_8':mu,'pattern':name,'modulus':mod,
                         'term_residue_sets':[sorted(x) for x in sets]})

# v(q^e T^power)>-mu/2 is equivalent to
# v(T) > ((e-1/2)/power)*mu. At every mu>=1 the threshold is
# at least its value at one. Test valuations are integral, and reciprocal
# valuations are even, at every consumed place.
thresholds=[]
for label,e,power,step,expected,minimum in [
 ('C2,C3,C4,G',11,4,1,Q(21,8),3),
 ('C1',2,4,1,Q(3,8),1),
 ('I',4,8,1,Q(7,16),1),
 ('reciprocal at q',1,2,2,Q(1,4),2),
 ('reciprocal at q2',2,2,2,Q(3,4),2),
 ('reciprocal at q3',3,2,2,Q(5,4),2),
 ('alternating comparison at q9',9,4,1,Q(17,8),3)]:
    coefficient=(Q(e)-Q(1,2))/power
    assert coefficient==expected and coefficient>0
    exact_minimum=step*(coefficient//step+1)
    assert exact_minimum==minimum
    thresholds.append({'test':label,'q_power':e,'test_power':power,
                       'strict_depth_coefficient':str(coefficient),
                       'valuation_lattice_step':step,'uniform_minimum':minimum})

factors=[
 [('C2',11,4,4),('DH',2,2,2),('B1',1,2,2)],
 [('G',11,4,4),('A3',2,2,2),('B0',1,2,2)],
 [('I',4,8,4),('A2',1,2,2),('A4',2,2,2),('B3',3,2,2)],
 [('C3',11,4,4),('C1',2,4,4),('B4',1,2,2)],
 [('C4',11,4,4),('A1',2,2,2),('B2',1,2,2)],
]
selected=[]
for i,terms in enumerate(factors):
    bounds=[-e+power*depth for _,e,power,depth in terms]
    assert all(x>0 for x in bounds)
    assert all(power%2==0 and e>0 for _,e,power,_ in terms)
    selected.append({'factor':i,'tests':[t[0] for t in terms],
                     'selected_valuation_lower_bounds':bounds})
assert [row['selected_valuation_lower_bounds'] for row in selected]==[
 [5,2,3],[5,2,3],[28,3,2,1],[5,14,3],[5,2,3]]
assert -9+4*4==7

def vp(value,p):
    n,d=abs(value.numerator),value.denominator;v=0
    while n%p==0:n//=p;v+=1
    while d%p==0:d//=p;v-=1
    return v
baseline=Q(204,409)**2
assert 0<baseline<17
assert [vp(baseline,p) for p in (2,3,17)]==[4,2,2]
assert vp(Q(408,409),409)==-1

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=HERE/'certificate.json')
parser.add_argument('--source',type=Path)
args=parser.parse_args()
if args.source is None:
    filename='revised_detector_factors_20261117_v66.tex'
    candidates=[HERE/filename,HERE.parents[2]/'papers/quartic'/filename]
    args.source=next((p for p in candidates if p.exists()),None)
    if args.source is None:parser.error('Use --source to specify the manuscript.')

report={'status':'PASS',
 'scope':'Physical-factor arithmetic only; no quadratic-table feasibility, new variable count, or new audit of external arithmetic premises.',
 'residue_period_complete':8,'residue_partitions':residues,
 'strict_thresholds':thresholds,'selected_contact_bounds':selected,
 'pole_baseline':str(baseline),'baseline_valuations':{'2':4,'3':2,'17':2},
 'zero_test_terms_may_be_omitted':True,
 'alternating_pairing_arithmetic_passes':True,
 'new_polynomial_or_variable_count_proved':False,
 'source_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','complete_residue_partitions':len(residues),
                  'thresholds':len(thresholds),'selected_factors':len(selected),
                  'new_variable_count_proved':False},indent=2))
