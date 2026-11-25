#!/usr/bin/env python3
"""Verify the final degree improvement against the independently replayed source."""
from pathlib import Path
import json,runpy
HERE=Path(__file__).resolve().parent
runpy.run_path(str(HERE/'verify.py'))
a=json.loads((HERE/'degree.json').read_text())
m=[1,1,1,1,2,2]
P,Q=121,128
nd,dd=a['raw_numerator_weights'],a['raw_denominator_weights']
L=6*Q+sum(k*d for k,d in zip(m,dd))
N=sum(max(Q+k*d,P+k*n) for k,d,n in zip(m,dd,nd))
J=2*max(L,N)
K=max(Q+J,P+L+N)
first=max(2*K,P+Q+2*J)
other=max(2*Q+4,2*P)
rad=first+2*other
q=(rad+1)//2
env=2*((rad+3)//4)
w=max(q,env)+a['point_envelopes_degree']
g=a['guard_degree_before_contact']+P+Q
assert (L,N,J,K,first,other,rad,q,env,w,g)==(
    850,850,1700,1828,3656,260,4176,2088,2088,2118,537)
assert 1+128*(1+g+w)==339969
assert max(8*(8-k)+k for k in range(1,9,2))==57
print('Final degree bound 339969 verified.')

for e,k,expected in [(6,6,3810177),(4,5,2282369)]:
    P=(2*k+5)*16*e
    Q=(2*k+6)*16*e
    L=6*Q+sum(j*d for j,d in zip(m,dd))
    N=sum(max(Q+j*d,P+j*n) for j,d,n in zip(m,dd,nd))
    J=2*max(L,N)
    K=max(Q+J,P+L+N)
    rad=max(2*K,P+Q+2*J)+2*max(2*Q+4,2*P)
    g=a['guard_degree_before_contact']+P+Q
    w=max((rad+1)//2,2*((rad+3)//4))+a['point_envelopes_degree']
    assert rad==30*Q+336
    assert 1+128*(1+g+w)==expected
print('Both weak-abc degree bounds verified.')
