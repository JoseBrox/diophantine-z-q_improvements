if not __debug__:
    raise RuntimeError('Run without -O; assertions are part of validation.')

#!/usr/bin/env python3
"""Tiny exact checks for the literal 15671-witness anchor; no expansion or builds."""
from fractions import Fraction as F
import argparse
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE.parents[1]
ZERO = (F(0), F(0))
ONE = (F(1), F(0))

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def sub(x,y): return add(x,neg(y))
def mul(x,y): return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def inv(x):
    n=x[0]*x[0]-2*x[1]*x[1]
    assert n
    return (x[0]/n,-x[1]/n)
def div(x,y): return mul(x,inv(y))
def scale(n,x): return (F(n)*x[0],F(n)*x[1])
def square(x): return mul(x,x)
def double(P,D):
    x,y=P
    slope=div(sub(scale(3,square(x)),D),scale(2,y))
    X=sub(square(slope),scale(2,x))
    Y=sub(mul(slope,sub(x,X)),y)
    return X,Y
def z(P): return neg(div(P[0],P[1]))
def vp(x,p):
    if x==0:return None
    num,den=x.numerator,x.denominator
    val=0
    while num%p==0:num//=p;val+=1
    while den%p==0:den//=p;val-=1
    return val
def serialize(x): return [[a.numerator,a.denominator] for a in x]
def normalize(row):
    out={}
    for coeff,monomial in row:
        key=tuple(sorted(monomial))
        out[key]=out.get(key,0)+coeff
    return {key:value for key,value in out.items() if value}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package',type=Path,default=DEFAULT)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    archive=args.package.resolve()
    module=json.loads((archive/'modules/q_anchor.json').read_text())
    shared=json.loads((archive/'shared.json').read_text())
    root=json.loads((archive/'modules/Z_definition.json').read_text())
    expected=[]
    for f,a,u,v in [(0,2,3,7),(1,10,11,15)]:
        expected += [
            [[1,[-25,a]],[-1,[f]]],
            [[-1,[]],[1,[u,u]],[-2,[u+1,u+1]],[-3,[u+2,u+2]],[6,[u+3,u+3]]],
            [[-4,[]],[1,[a,a]],[-4,[a,u]],[4,[u,u]],[-8,[v,v]],[-12,[v+1,v+1]],[24,[v+2,v+2]]]]
    assert module['free']==2 and module['locals']==16 and not module['calls']
    assert module['anchor_squarings']==24 and module['anchor_constant_global_index']==-25
    assert [normalize(row) for row in module['residuals']]==[normalize(row) for row in expected]
    expected_shared=[[[-3,[]],[1,[-1]]]]
    expected_shared += [[[1,[-i-2]],[-1,[-i-1,-i-1]]] for i in range(24)]
    assert shared['witnesses']==25
    assert [normalize(row) for row in shared['residuals']]==[normalize(row) for row in expected_shared]
    anchor_calls=[call for call in root['calls'] if call['module']=='q_anchor']
    assert anchor_calls==[{'module':'q_anchor','args':[26,27]}]
    assert root['point_coordinates']['S'][:2]==[30,31]
    root_rows=[normalize(row) for row in root['residuals']]
    assert normalize([[-1,[]],[1,[26,30]],[2,[27,31]]]) in root_rows
    assert normalize([[1,[26,31]],[1,[27,30]]]) in root_rows
    d0=(F(75),F(-53));D0=square(d0)
    d1=(F(3),F(-1));D1=square(d1)
    lam=(F(3),F(2))
    P0=((F(1641,8),F(-145)),(F(-15465,4),F(87483,32)))
    P1=((F(57,8),F(-7,2)),(F(-165,8),F(417,32)))
    assert mul(square(lam),d0)==d1
    assert mul(square(lam),P0[0])==P1[0]
    assert mul(mul(square(lam),lam),P0[1])==P1[1]
    for P,D in [(P0,D0),(P1,D1)]:
        assert square(P[1])==sub(mul(square(P[0]),P[0]),mul(D,P[0]))
    z0=z(double(P0,D0));z1=z(double(P1,D1))
    assert z0==(F(-6351748793760,3287811625151),F(-5612900635092,3287811625151))
    assert z0==mul(lam,z1)
    assert [vp(a,3) for a in z1]==[1,1]
    residue=lambda a,p:(a.numerator*pow(a.denominator,-1,p))%p
    reduction=[[residue(a,3) for a in xy] for xy in P1]
    assert reduction==[[0,1],[0,0]]
    p1z=z(P1)
    vals2=[vp(p1z[0],2),F(vp(p1z[1],2))+F(1,2)]
    assert min(vals2)==F(3,2)
    N=2**24;m=N//2
    left=3*(m-1);right=4*(5+4783227)
    assert left>right
    all_rows=module['residuals']+shared['residuals']
    assert all(math.gcd(*(abs(c) for c,_ in row))==1 for row in all_rows)
    l1_sos_bound=sum(sum(abs(c) for c,_ in row)**2 for row in all_rows)
    assert l1_sos_bound==6956 and l1_sos_bound<2**13
    assert max(len(mono) for row in all_rows for _,mono in row)==2
    files=['modules/q_anchor.json','modules/Z_definition.json','shared.json','counts.json',
           'source/article/short-polynomial-proof-sections.tex','source-inputs/focused_diophantine.tex',
           'arithmetic/anchor/anchor-proof.tex','source/module-specification.md']
    out={'status':'PASS','scope':'Literal anchor rows, constant-chain rows, exact scalar arithmetic and conditional numerical cutoff only.',
         'no_heavy_expansion_performed':True,
         'literal_counts':{'anchor_private_witnesses':16,'anchor_residuals':6,'shared_chain_witnesses':25,'shared_chain_residuals':25},
         'root_wiring':{'anchor_calls':anchor_calls,'S_abscissa_pair':[30,31],'reciprocal_pair':[26,27],
                        'both_coordinate_inverse_equations_verified':True},
         'P_new_mod_3':reduction,'z_2P_old':serialize(z0),'z_2P_new':serialize(z1),
         'z_2P_new_coefficient_3_adic_valuations':[vp(a,3) for a in z1],
         'z_P_new':serialize(p1z),'normalized_2_adic_parameter_valuation':'3/2',
         'anchor_constant_recipe':'C=3^(2^24); C digits not materialized',
         'anchor_index_subgroup_recipe':'2*3^(2^23-1) Z, excluding index zero when S is required nonzero',
         'height_bound_assumption':'log_2(H)<4783227, requiring separate H5 verification',
         'cutoff_integer_comparison':{'left':left,'right':right,'strictly_greater':True},
         'anchor_and_chain_sos_coefficient_L1_upper_bound':l1_sos_bound,
         'anchor_and_chain_sos_degree_upper_bound':4,
         'source_files':[{'path':name,'sha256':sha(archive/name)} for name in files]}
    if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
