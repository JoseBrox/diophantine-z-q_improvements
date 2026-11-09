#!/usr/bin/env python3
"""Exact residue checks for the quadratic-input obstruction; no dependencies."""
from pathlib import Path
import argparse
import json


def r(t):return t*(t-1)*(t-2401)*(32*t+343)*(2*t-1)


def valuation2(n):
    assert n
    return (abs(n)&-abs(n)).bit_length()-1


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    classes=[]
    for modulus,residue,v,u in [(8,5,4,3),(8,7,2,5),(16,9,6,3)]:
        tested=[]
        for t in range(residue,512,modulus):
            q=r(t);actual_v=valuation2(q);actual_u=(q//2**actual_v)%8
            assert (actual_v,actual_u)==(v,u)
            tested.append(t)
        classes.append({'input_congruence':f't={residue} mod {modulus}',
                        'valuation2':v,'odd_unit_mod8':u,'representatives_checked_mod512':len(tested)})
    odd_k_images={}
    for k in (1,3,5,7):
        image=sorted({x*(x+k)%8 for x in range(8)})
        assert image==[0,2,4,6]
        odd_k_images[str(k)]=image
    normalized=[]
    for A in range(6,128,8):
        for c in range(3,128,8):
            if (A+c)%16!=1:continue
            candidates=[x for x in range(32) if (A*x*x+c-1)%128==64]
            assert candidates
            x=candidates[0];t=A*x*x+c
            assert valuation2(t-1)==6
            assert valuation2(t-2401)==5
            assert valuation2(r(t))==11
            normalized.append({'A_mod128':A,'c_mod128':c,'x_mod32':x,
                               'contact_valuation':6,'r_valuation':11})
    square_class=[]
    for t in range(3,512,8):
        q=r(t);v=valuation2(q);u=(q//2**v)%8
        assert (v,u)==(2,1)
        square_class.append(t)
    quartic_examples=[]
    for c in (3,2403):
        assert c%8==3
        # A reduced denominator v would satisfy v^4 | 8; the only
        # positive integer possibility is v=1, because 3<4.
        assert valuation2(8)==3<4
        for x in range(-32,33):
            t=8*x**4+c
            assert t>=c>0 and t%8==3
            value=r(t);v=valuation2(value)
            assert v==2 and (value//4)%8==1
        quartic_examples.append({'leading_coefficient':8,'constant':c,
                                 'degree':4,'minimum_on_integers':c,
                                 'integrality_denominator_condition':'v^4 divides 8, hence v=1',
                                 'sample_integer_inputs_checked':65})
    result={'status':'PASS','local_nonsquare_classes':classes,
            'positive_quartic_sharpness':{'minimum_degree':4,
                'square_class':'t=3 mod 8 implies v2(r(t))=2 and r(t)/4=1 mod 8',
                'square_class_representatives_checked_mod512':len(square_class),
                'examples':quartic_examples},
            'odd_k_quadratic_images_mod8':odd_k_images,
            'normalized_root_cases_checked':len(normalized),
            'normalized_root_witnesses':normalized,
            'scope':'Finite residue checks supporting the proved obstruction for integer polynomials of degree at most two that reflect rational integrality, are odd on all integers, and would make r(q(x)) a Q2-square for all integers. This is not an obstruction to arbitrary defining polynomials or to scalar correction methods.'}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='normalized_root_witnesses'},indent=2))

if __name__=='__main__':main()
