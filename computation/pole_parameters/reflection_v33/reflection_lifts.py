#!/usr/bin/env python3
"""Independent first-order elliptic computation over (Z/361)[sqrt(2)]."""
import json
from pathlib import Path
MOD=361

def a(x,y): return ((x[0]+y[0])%MOD,(x[1]+y[1])%MOD)
def neg(x): return (-x[0]%MOD,-x[1]%MOD)
def sub(x,y): return a(x,neg(y))
def mul(x,y): return ((x[0]*y[0]+2*x[1]*y[1])%MOD,(x[0]*y[1]+x[1]*y[0])%MOD)
def sc(k,x): return (k*x[0]%MOD,k*x[1]%MOD)
def unit(x): return (x[0]*x[0]-2*x[1]*x[1])%19!=0
def div(x,y):
    if not unit(y): raise ArithmeticError('Nonunit denominator')
    return sc(pow((y[0]*y[0]-2*y[1]*y[1])%MOD,-1,MOD),mul(x,(y[0],-y[1])))
d=(3,-1);D=mul(d,d)
P=(div((57,-28),(8,0)),div((-660,417),(32,0)))
def on(Q):
    x,y=Q
    return mul(y,y)==sub(mul(mul(x,x),x),mul(D,x))
def add(Q,R):
    x,y=Q;u,v=R
    if unit(sub(u,x)):
        s=div(sub(v,y),sub(u,x))
    elif unit(a(v,y)):
        s=div(sub(a(a(mul(x,x),mul(x,u)),mul(u,u)),D),a(y,v))
    else:
        raise ArithmeticError('This chosen addition chain leaves the affine unit chart')
    xx=sub(sub(mul(s,s),x),u)
    out=(xx,sub(mul(s,sub(x,xx)),y))
    if not on(out): raise ArithmeticError('Curve equation fails after addition')
    return out

def compute():
    if not on(P):raise ArithmeticError('Initial point')
    powers={1:P}
    for i in (2,4,8,16,32,64,128):powers[i]=add(powers[i//2],powers[i//2])
    Q=add(add(add(add(powers[64],powers[32]),powers[16]),P),powers[8])
    Q2=add(add(powers[128],P),(powers[8][0],neg(powers[8][1])))
    if Q!=Q2:raise ArithmeticError('Independent chains for 121P disagree')
    x=Q[0]
    coords=[x,div(neg(D),x),a(d,div(sc(2,D),sub(x,d))),sub(div(sc(2,D),a(x,d)),d)]
    traces=[2*z[0]%MOD for z in coords]
    if [z%19 for z in traces]!=[0,2,2,3]:raise ArithmeticError('Trace residues')
    cs=[-12,4,4,12]
    avals=[(121**4+T**4)%MOD for T in traces]
    ds=[((av-c)%MOD)//19 for av,c in zip(avals,cs)]
    if any((av-c)%19 for av,c in zip(avals,cs)):raise ArithmeticError('Expected contact divisibility')
    forbidden=sorted({(-z*pow(2,-1,19))%19 for z in ds})
    good=[t for t in range(19) if t not in forbidden]
    for t in good:
        for T,c in zip(traces,cs):
            residue=((121+190*t)**4+T**4-c)%MOD
            if residue==0 or residue%19:raise ArithmeticError('Odd valuation witness')
    if len(good)<15 or not set(good).intersection(range(5)):
        raise ArithmeticError('Pigeonhole bound')
    result={'status':'PASS','modulus':MOD,'point121':[list(z) for z in Q],
            'two_independent_addition_chains_agree':True,'four_trace_residues':traces,
            'four_contact_lifts':ds,'exceptional_trial_residues':forbidden,
            'excluded_shift_residues_mod_3610':[(117+190*t)%3610 for t in good],
            'number_of_excluded_progressions':len(good),
            'first_of_five_explicit_excluded_shifts':117+190*min(set(good).intersection(range(5))),
            'scope':'First-order modular arithmetic, conditional source soundness used separately for the global obstruction'}
    return result
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    report=compute();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',args.output.name)
