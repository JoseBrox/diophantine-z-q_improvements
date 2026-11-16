#!/usr/bin/env python3
"""Exact certificates for native normalization and the X=4 inert obstruction.

Uses only Python's standard library. The proof of the infinite/input-uniform
statements is in the accompanying manuscript; finite checks have their stated
scope and do not establish rational realization on elliptic tuples.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import hashlib
import json


def valuation(q, p):
    q=Q(q)
    if not q:
        raise ValueError('zero valuation is not finite')
    n,d=abs(q.numerator),q.denominator
    v=0
    while n%p==0:
        n//=p; v+=1
    while d%p==0:
        d//=p; v-=1
    return v


def residue(q,p):
    q=Q(q)
    return q.numerator*pow(q.denominator,-1,p)%p


def prime_trial(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))


def contact_sets(p):
    theta=[Q(0),Q(-1,2),Q(-1),Q(1,2399),Q(-32,407)]
    sets=[]
    for j in (0,1):
        entries=[Q(4*j+2)+t for t in theta]+[Q(4*j+4)+t for t in theta]+[Q(-j-1)]
        rs=[residue(q,p) for q in entries]
        assert 0 not in rs and len(set(rs))==11
        assert all(q.denominator%p for q in entries)
        sets.append(rs)
    assert set(sets[0]).isdisjoint(sets[1])
    return sets


def pairadd(a,b): return (a[0]+b[0],a[1]+b[1])
def pairmul(a,b): return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def pairscale(a,c): return (a[0]*c,a[1]*c)
def pairnorm(a): return a[0]*a[0]-2*a[1]*a[1]
def pairinv(a): return (a[0]/pairnorm(a),-a[1]/pairnorm(a))


def product(omega,hs):
    out=(Q(1),Q(0))
    for h in hs:
        out=pairmul(out,pairadd((Q(1),Q(0)),pairscale(pairmul(h,h),omega)))
    return out


def normalization_checks():
    count=0
    for omega in [Q(1,3),Q(7,16),Q(3),Q(29,5)]:
        hs=[(Q(2,3),Q(-1,5)),(Q(-4,7),Q(3,11))]
        W=product(omega,hs)
        Wi=pairinv(W); V=2*Wi[0]; J=pairnorm(Wi)
        for c in [Q(0),Q(1),Q(-3,5),Q(7,11)]:
            G=1+omega*c*c; op=omega/G**2
            hsp=[(c*G,Q(0))]+[pairscale(h,G) for h in hs]
            Wp=product(op,hsp); Wpi=pairinv(Wp)
            assert Wp==pairscale(W,G)
            assert 2*Wpi[0]==V/G and pairnorm(Wpi)==J/G**2
            assert 4*op/(2*Wpi[0])**2==4*omega/V**2
            count+=1
    parity=0
    for n in range(1,100,2):
        for r in range(-100,101):
            np=n-2*min(0,n+2*r)
            assert np>0 and np%2==1
            parity+=1
    return {'exact_native_transformations':count,'integer_valuation_cases':parity,
            'universal_proof':'algebraic factor substitution and odd valuation minimum in manuscript'}


def scalar_prepared_examples():
    rows=[]
    ss=[('fixed',Q(100,1001))]+[(f'M={m}',Q(102**m,10*102**m+1)) for m in range(2,10)]
    for tag,s in ss:
        w=s*s; r=1/(10*s)
        W=1+2*w*r*r
        assert W==Q(51,50)
        b=w*W*W
        assert b==(s*W)**2 and 0<b<17
        wp=w/(1+w)**2; Vp=2/(W*(1+w))
        assert valuation(Vp,3)==-1
        assert all(valuation(b,p)>0 for p in (2,3,17))
        assert valuation(wp,17)%2==0
        rows.append({'label':tag,'s':str(s),'w':str(w),'W':str(W),'b':str(b),
                     'w_star':str(wp),'V_star':str(Vp),
                     'b_valuations':{str(p):valuation(b,p) for p in (2,3,17)},
                     'V_star_valuation_at_3':valuation(Vp,3)})
    return rows


def main(output=None):
    p=252877; x=4; ell=76249
    beta=216*x**4+450459
    assert beta==505755 and beta-1==2*p
    assert prime_trial(p) and p%8==5
    assert p>76176 and p not in (1875611,3828397,3982747,ell)
    contacts=[beta,beta-1,beta-2401,32*beta+343,2*beta-1]
    vs=[valuation(c,p) for c in contacts]
    assert vs==[0,1,0,0,0]
    rr=1
    for c in contacts: rr*=c
    assert valuation(rr,p)==1 and valuation(Q(102*ell),p)==0
    residues=contact_sets(p)
    modular_samples=[]
    for L in (3,5,21,101,20483):
        C=17*(pow(ell,(L+1)//2,p*p)+1)
        den=(1+C*rr)%(p*p)
        num=(102**2*pow(ell,L,p*p)*rr)%(p*p)
        assert den%p==1 and num%p==0 and num%(p*p)!=0
        modular_samples.append({'L':L,'numerator_mod_p2':num,'denominator_base_mod_p2':den})
    certificate={
        'schema':'zq.native-normalization-inert-obstruction.v51',
        'scope':{'actual_integer_input_obstruction':True,
                 'all_odd_L':'proved symbolically by p-unit denominator and exact one contact valuation',
                 'all_auxiliary_tuples_and_slopes':'proved by the disjoint-contact unit-weight alternative',
                 'all_finite_native_normalizations':'proved by positive odd valuation preservation',
                 'rules_out':'simultaneous final reciprocal trace one in original general scalar source',
                 'does_not_rule_out':['other prescribed-trace norm equations','the 21/9 target itself','modified scalar sources'],
                 'scalar_prepared_product_examples_are_actual_elliptic_tuples':False},
        'input':x,'beta':beta,'prime':p,'prime_square':p*p,
        'primality':{'method':'trial division by every integer from 2 to floor(sqrt(p))','bound':isqrt(p)},
        'prime_mod_8':p%8,'scalar_contacts':contacts,'scalar_contact_valuations':vs,
        'scalar_contacts_mod_p':[c%p for c in contacts],
        'r_over_p_mod_p':(rr//p)%p,
        'contact_and_pole_residue_sets':residues,
        'scalar_modular_samples':modular_samples,
        'input_progression':f'X = 4 mod {p*p}',
        'normalization_checks':normalization_checks(),
        'scalar_prepared_norm_orbit_examples':scalar_prepared_examples(),
    }
    out=output or Path(__file__).with_name('certificate.json')
    out.parent.mkdir(parents=True,exist_ok=True)
    blob=(json.dumps(certificate,indent=2,sort_keys=True)+'\n').encode()
    out.write_bytes(blob)
    print(json.dumps({'status':'pass','certificate':str(out),'sha256':hashlib.sha256(blob).hexdigest(),
                      'prime':p,'progression_modulus':p*p},sort_keys=True))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    main(parser.parse_args().output)
