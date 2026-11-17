#!/usr/bin/env python3
"""Exact constants and local support check for the scoped obstruction."""
from fractions import Fraction as F
from pathlib import Path
import json
import argparse
import hashlib

ROOT=Path(__file__).resolve().parent
REPO=Path(__file__).resolve().parents[3]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output",type=Path,default=ROOT/"certificate.json")
OUTPUT=parser.parse_args().output
alpha=F(997,1001)
gamma=F(997,200)
Q=F(1002,995)
C=F(401,100)
delta=gamma/Q-C
product=alpha*delta
assert delta==F(188411,200400)>0
assert product==F(187845767,200600400)>0
assert 3*product-1==F(362936901,200600400)>0
cases=0
for nu in range(1,52,2):
    for val_c in range(-50,1):
        val_d=max(2*val_c,-nu)
        val_w_factor=2*val_d-nu
        assert val_w_factor<=-nu
        # Other factors have nonpositive valuation and only decrease this bound.
        val_b_upper=nu+2*val_w_factor
        assert val_b_upper<0 and val_b_upper%2==1
        cases+=1
certificate={
    'status':'PASS',
    'manuscript_sha256':hashlib.sha256((REPO/'negative_results/papers/pole_parameters/denominator_support_height_obstruction_20261117_v60.tex').read_bytes()).hexdigest(),
    'alpha':str(alpha),'gamma':str(gamma),'Q':str(Q),'C':str(C),
    'delta':str(delta),'alpha_delta':str(product),
    'three_alpha_delta_minus_one':str(3*product-1),
    'local_support_valuation_cases':cases,
    'conclusion':'index ratio bounded for each fixed source',
    'scope':'positive odd weight support contained in denominator of H; height coordinate lower bound a(n^2-1)hhat(H)',
    'all_two_point_sources_excluded':False,
    'new_defining_variable_bound_claimed':False,
}
OUTPUT.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(certificate,indent=2))
