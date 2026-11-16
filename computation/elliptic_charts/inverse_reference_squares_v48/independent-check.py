#!/usr/bin/env python3
"""Exhaust every complete reference graph fiber over small finite fields.

Standard-library implementation; imports no producer or symbolic algebra.
The all-characteristic-zero theorem is proved in the accompanying paper.
"""
import argparse,json
from pathlib import Path

def run(p):
    parameters=points=exception_A=exception_B=candidates=0
    for a in range(1,p):
        for c in range(1,p):
            d=(a-c*c)%p
            Delta=((a+d)**2-4*a*c*c)%p
            if not d or not Delta:continue
            parameters+=1
            for u in range(1,p):
                w=pow(a*u,-1,p)
                for h in range(1,p):
                    if (d*h*h+a*h*(u+w)+2*c*h-1)%p:continue
                    points+=1
                    v=(a*(u+w)+2*c+d*h)%p
                    assert v*h%p==1
                    LA=(v+d*w)%p;LB=(v+d*u)%p
                    assert LA or LB
                    At=u*u*h*h%p;Bt=w*w*h*h%p
                    ca=(2*c*h*u+h-u)%p;cb=(2*c*h*w+h-w)%p
                    acand=[-ca*pow(a*LA,-1,p)%p] if LA else range(p)
                    bcand=[-cb*pow(a*LB,-1,p)%p] if LB else range(p)
                    hits=[]
                    for A in acand:
                        for B in bcand:
                            candidates+=1
                            if (a*A*LA+ca)%p or (a*B*LB+cb)%p:continue
                            if (a*a*(d*d*A*B-(1+4*c*w)*A-(1+4*c*u)*B)+1-2*(2*a+c*c)*h*h)%p:continue
                            hits.append((A,B))
                    assert hits==[(At,Bt)]
                    S=(v-c-a*u)%p;T=(a*w-v+c)%p
                    assert (v*(v+T-S)+d)%p==0
                    assert (S*T+c*(T-S)+2*c*v+2*d)%p==0
                    assert (S*T+c*(S-T)+2*d)*pow(2*c*d,-1,p)%p==h
                    if not LA:
                        exception_A+=1
                        assert Bt==pow(d*d,-1,p)
                        assert (-4*a*a*c*w)%p
                    if not LB:
                        exception_B+=1
                        assert At==pow(d*d,-1,p)
                        assert (-4*a*a*c*u)%p
    return {'prime':p,'admissible_constant_pairs':parameters,'reference_points':points,
            'candidate_square_pairs_tested':candidates,'exceptional_A_fibers':exception_A,
            'exceptional_B_fibers':exception_B,'all_fibers_unique_correct_graph':True}

parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('independent-verification.json'))
args=parser.parse_args()
records=[run(p) for p in [5,7,11,13,17,19]]
report={'status':'PASS','implementation':'Python standard library; no producer import',
        'scope':'Exhaustive finite-field supplement to the all-field graph theorem, not a substitute for its proof.',
        'fields':records,'total_reference_points':sum(x['reference_points'] for x in records)}
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','fields':len(records),'points':report['total_reference_points'],'output':str(args.output)}))
