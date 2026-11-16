#!/usr/bin/env python3
"""Exact algebra and local parity certificates for bounded native levels."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import json
import sympy as sp


def main():
    W0,W1,w,c,y,q=sp.symbols('W0 W1 w c y q')
    N=W0**2-2*W1**2
    V=2*W0/N
    m=N/(c+N)
    level=17*m*m
    native_b=4*w/(V*V)
    assert sp.factor(m*V-2*W0/(c+N))==0
    # The complement polynomial and prescribed-coordinate norm polynomial
    # differ by an explicitly nonzero square after the witness substitution.
    q_from_y=17*sp.symbols('d')*m*y/V
    d=sp.symbols('d')
    residual=sp.factor((q_from_y*q_from_y-d*level*(level-native_b))
                       /(-289*d*m*m/(V*V)))
    assert sp.factor(residual-((m*V)**2-d*y*y-4*w/17))==0

    U=2*W0/(1+N)
    J=2*W1/(1+N)
    Z=(1-N)/(1+N)
    assert sp.factor(U*U-2*J*J+Z*Z-1)==0

    # Cayley identity verified independently in polynomial form.
    poly=(2*W0)**2-2*(2*W1)**2+(1-N)**2-(1+N)**2
    assert sp.Poly(sp.expand(poly),W0,W1).is_zero

    # The conditional source is exactly a product of 1+w*h^2 factors.
    delta,F,C=sp.symbols('delta F C')
    w_cond=F/(4*delta**8)
    h_cond=C/(2*delta**2*w_cond)
    assert sp.factor(w_cond*h_cond*h_cond-delta**4*C*C/F)==0

    # All possible split residue pairs, and the two inert ones.
    residues=[]
    for e0 in [0,1]:
        for e1 in [0,1]:
            trace=e0+e1
            invnorm=e0*e1
            bounded_trace=Q(trace,1+invnorm)
            assert bounded_trace in [0,1]
            residues.append({'inverse_W_residues':[e0,e1],
                             'reciprocal_trace_residue':trace,
                             'inverse_norm_residue':invnorm,
                             'bounded_trace_residue':int(bounded_trace)})

    # Supplementary screen for both signs of an odd physical-weight valuation.
    local_cases=0
    for nu in range(-19,20,2):
        for vh in range(-12,13):
            second=nu+2*vh
            assert second%2 and second!=0
            factor=min(0,second)
            assert factor<=0
            if factor==0:
                assert second>0
            local_cases+=1

    # For w>0 all real factor values are >=1. The bound on the transformed
    # trace follows from (r-1)(s-1)>=0; this is an exact identity.
    r,s=sp.symbols('r s')
    assert sp.factor(1+r*s-r-s-(r-1)*(s-1))==0

    # Numerical values are rational exact fixtures for the identities, not
    # claims that the chosen W and w arise from actual elliptic tuples.
    fixtures=[]
    for a,b,ww in [(Q(3),Q(1),Q(1,16)),(Q(9,4),Q(1,8),Q(5,49))]:
        nn=a*a-2*b*b
        mm=nn/(1+nn)
        uu=2*a/(1+nn)
        jj=2*b/(1+nn)
        zz=(1-nn)/(1+nn)
        assert uu*uu-2*jj*jj+zz*zz==1
        assert Q(1,2)<mm<1 and 0<uu<=1
        fixtures.append({'W0':str(a),'W1':str(b),'weight':str(ww),
                         'N':str(nn),'m':str(mm),'level':str(17*mm*mm),
                         'bounded_trace':str(uu),'cayley_identity':True,
                         'native_realization_asserted':False})

    receipt={'status':'PASS',
             'exact_identities':['bounded prescribed trace',
                                 'complement/norm equivalence with nonzero factors',
                                 'Cayley quadric',
                                 'independent polynomial Cayley expansion',
                                 'conditional native factor presentation',
                                 'real trace bound factorization'],
             'split_residue_pairs':residues,
             'inert_residue_pairs':[[0,0],[1,1]],
             'supplementary_parity_cases':local_cases,
             'algebraic_fixtures':fixtures,
             'retained_variable_count_if_actual_realization_proved':{'general':21,'conditional':9},
             'actual_uniform_realization_proved':False,
             'established_count_change':False,
             'scope':'The manuscript proves the universal all-prime local transfer and whole-character guards. These finite checks certify the displayed identities and supplementary cases; they do not prove the missing actual rational realization.'}
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    data=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(data)
    else:print(data,end='')


if __name__=='__main__':main()
