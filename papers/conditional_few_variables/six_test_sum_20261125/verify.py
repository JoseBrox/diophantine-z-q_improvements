#!/usr/bin/env python3
"""Replay the weighted degree and pre-contact guard ledger of the new family."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha1,sha256
from math import prod
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
rec=json.loads((HERE/'degree.json').read_text())
def load(name,blob):
    data=(ROOT/rec['source']/name).read_bytes()
    assert sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
    return json.loads(data)
a=load('native.json',rec['source_native_blob'])
p=load('parent.json',rec['source_parent_blob'])
assert sha256((ROOT/rec['source']/'native.json').read_bytes()).hexdigest()==rec['source_native_sha256']
nodes=a['coefficient_dag']
weights=rec['point_weights']
d=[]
for op,*v in nodes:
    if op in ('int','parameter'):w=0
    elif op=='variable':w=weights[v[0]] if v[0]<len(weights) else 0
    elif op=='add':w=max(d[i] for i in v)
    elif op=='mul':w=sum(d[i] for i in v)
    elif op=='pow':w=d[v[0]]*v[1]
    elif op=='neg':w=d[v[0]]
    else:raise ValueError(op)
    d.append(w)
tests=next(e for e in a['events'] if e['operation']=='balanced_actual_detector')['original_tests']
assert tests==rec['raw_tests']
assert all(row[0]['denominator']==row[1]['denominator'] for row in tests)
nd=[max(d[t['numerator']] for t in row) for row in tests]
dd=[d[row[0]['denominator']] for row in tests]
assert nd==rec['raw_numerator_weights'] and dd==rec['raw_denominator_weights']
def atoms(i):
    op,*v=nodes[i]
    if op=='int':
        assert v[0]!=0
        return set()
    if op=='mul':return set().union(*(atoms(j) for j in v))
    if op=='pow':return atoms(v[0]) if v[1] else set()
    if op=='neg':return atoms(v[0])
    return {i}
height=next(e for e in a['events'] if e['operation']=='moving_contact_height')
before=[]
for node,label in a['guard_descriptions']:
    if node==height['H']['numerator']:break
    before.append(node)
guard=set().union(*(atoms(i) for i in before))
assert guard==set(rec['guard_atoms'])
for row in tests:
    for t in row:assert atoms(t['denominator'])<=guard
g0=sum(x['scalar_norm_degree_bound'] for x in p['subalgebra_norm_factors'] if x['node'] in guard)
assert g0==rec['guard_degree_before_contact']==288
assert d[height['beta']['numerator']]==d[height['trace']['numerator']]==2
assert d[height['beta']['denominator']]==d[height['trace']['denominator']]==0
M=8
P,Qc=16*M,20*M
D=sum(dd)
Ri=[D-b+a for a,b in zip(nd,dd)]
L=6*Qc+8*D
N=max(L,*(i*P+(6-i)*Qc+8*Ri[i-1] for i in range(1,7)))
J=2*max(N,L)
K=max(Qc+J,P+N+L)
pole_d=P+Qc
R=max(2*K,pole_d+2*J)+2*max(4,2*pole_d)
qweight=(R+1)//2
env=2*((R+3)//4)
pre=sum(x['envelope_degree'] for x in p['quadratic_tower'][:6])
g=g0+P+Qc
w=max(qweight,env)+pre
assert all(rec[k]==v for k,v in {
    'common_test_denominator_weight':D,'common_test_numerator_weights':Ri,
    'contact_numerator_degree':P,'contact_denominator_degree':Qc,
    'W_denominator_weight':L,'W_numerator_weight':N,
    'J_weight':J,'K_weight':K,'d_degree':pole_d,'radicand_weight':R,
    'pole_root_weight':qweight,'pole_envelope_degree':env,
    'point_envelopes_degree':pre,'guard_degree':g,'separator_degree':w}.items())
assert rec['rank']==128 and rec['degree_bound']==1+128*(1+g+w)==520065
assert Q(197,200)*Q(997,1001)-Q(1,2)==Q(96309,200200)>0
for nu in range(-99,100,2):
    assert len({i*nu%8 for i in range(7)})==7
print("Pre-contact guards, six raw-test weights, separator bound and degree 520065 verified.")
