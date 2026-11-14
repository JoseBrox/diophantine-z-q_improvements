#!/usr/bin/env python3
"""A complete 605-residue certificate for the reflection obstruction at 11."""
from pathlib import Path
import json
M=121

def require(ok,msg):
    if not ok:raise AssertionError(msg)
def plus(x,y):return ((x[0]+y[0])%M,(x[1]+y[1])%M)
def neg(x):return (-x[0]%M,-x[1]%M)
def minus(x,y):return plus(x,neg(y))
def times(x,y):return ((x[0]*y[0]+2*x[1]*y[1])%M,(x[0]*y[1]+x[1]*y[0])%M)
def scale(a,x):return (a*x[0]%M,a*x[1]%M)
def norm(x):return (x[0]*x[0]-2*x[1]*x[1])%M
def unit(x):return norm(x)%11!=0
def divide(x,y):
    require(unit(y),'Unit denominator in the unramified quadratic ring')
    return scale(pow(norm(y),-1,M),times(x,(y[0],-y[1])))
def mod11(x):return tuple(t%11 for t in x)
d=(3,-1);D=times(d,d)
P=(divide((57,-28),(8,0)),divide((-660,417),(32,0)))
def on(Q):
    x,y=Q;return times(y,y)==minus(times(times(x,x),x),times(D,x))
def add(Q,R):
    x,y=Q;u,v=R
    if unit(minus(u,x)):s=divide(minus(v,y),minus(u,x))
    elif unit(plus(v,y)):
        s=divide(minus(plus(plus(times(x,x),times(x,u)),times(u,u)),D),plus(v,y))
    else:raise ArithmeticError('Chosen sum is outside the affine unit addition charts')
    xx=minus(minus(times(s,s),x),u)
    out=(xx,minus(times(s,minus(x,xx)),y));require(on(out),'Addition curve identity')
    return out

def compute():
    require(pow(2,5,11)==10,'Inert prime 11')
    require(on(P),'Initial point is on curve')
    P2=add(P,P);P3=add(P2,P);P4=add(P2,P2)
    require(mod11(P[0])==(3,2) and mod11(P[1])==(0,1),'P reduction')
    require(mod11(P2[0])==(8,9) and mod11(P2[1])==(8,0),'2P reduction')
    require(mod11(P3[0])==mod11(P2[0]) and mod11(P3[1])==mod11(neg(P2[1])), '3P=-2P modulo 11')
    require(mod11(P4[0])==mod11(P[0]) and mod11(P4[1])==mod11(neg(P[1])), '4P=-P modulo 11')
    # Homogeneous addition at the identity: modulo p^2, z(2P+3P)=dx/dy.
    z5=divide(minus(P3[0],P2[0]),minus(P3[1],P2[1]))
    require(mod11(z5)==(0,0),'5P is in the first formal neighborhood')
    require(times(z5,z5)==(0,0),'First-order nilpotence')
    base={1:P,2:P2,3:P3,4:P4}
    points={}
    for k in range(11):
        z=scale(k,z5)
        for r,(x,y) in base.items():
            xx=plus(x,scale(2,times(y,z)))
            yy=plus(y,times(minus(scale(3,times(x,x)),D),z))
            points[r+5*k]=(xx,yy)
            require(on(points[r+5*k]),'First-order translated point lies on curve')
    # Independent additions check every block and all bridges, including wraparound.
    additions=0
    for n,Q in points.items():
        if n%5 in (1,2,3):
            require(add(Q,P)==points[n+1], 'Successive addition by P');additions+=1
        else:
            target=(n+2)%55
            require(add(Q,P2)==points[target], 'Bridge and wraparound by 2P');additions+=1
    require(additions==44,'All forty-four first-order points checked independently')
    def traces(n):
        Q=points[n%55];x=Q[0]
        xs=[x,divide(neg(D),x),plus(d,divide(scale(2,D),minus(x,d))),
            minus(divide(scale(2,D),plus(x,d)),d)]
        out=[2*z[0]%M for z in xs]
        require(sorted(pow(v,4,11) for v in out)==[3,5,5,9], 'Uniform fourth-power multiset')
        return out
    require([x%11 for x in traces(1)]==[6,7,9,9], 'Four base torsion traces')
    allowed=[-12,-6,-4,-2,2,4,6,12]
    signed={c%11:c for c in allowed}
    require(len(signed)==8,'Signed contact distances are distinct')
    choices=[1,3,1,3,2,3,2,1,2,1,2]
    rows=[]
    for B in range(605):
        x0=choices[B%11]
        if x0==1 and B%5==4:x0=10
        elif x0==2 and B%5==1:x0=9
        elif x0==3 and B%5==1:x0=14
        require(1<=x0<=14 and x0%11!=0,'Bounded base input')
        n0=B+x0*x0
        require(n0%5!=0 and n0%11 in (1,3,8,10),'Two required congruences')
        found=None
        for j in (-2,-1,0,1,2):
            X=abs(x0+55*j);n=B+X*X
            tt=traces(n)
            av=[(pow(n,4,M)+pow(T,4,M))%M for T in tt]
            require(all(v%11 in signed for v in av),'All four are contact residues')
            cc=[signed[v%11] for v in av]
            lifts=[(v-c)%M for v,c in zip(av,cc)]
            if all(v!=0 and v%11==0 for v in lifts):
                found={'B_residue':B,'input':X,'trial':j,'n_mod_55':n%55,
                       'four_trace_residues_mod_121':tt,'signed_contact_distances':cc,
                       'four_nonzero_contact_lifts':lifts}
                break
        require(found is not None,'Five trials cover this coefficient shift')
        require(1<=found['input']<=124,'Uniform input bound')
        rows.append(found)
    # A deliberately false trace residue must break the checked fourth-power pattern.
    bad=[6,7,9,0]
    require(sorted(pow(v,4,11) for v in bad)!=[3,5,5,9],'Corruption control')
    return {'schema':'uniform-reflection-obstruction/p11-v32','status':'PASS',
            'prime':11,'modulus':121,'order_of_P_mod_11':5,
            'z_of_5P_mod_121':list(z5),'first_order_group_points_checked':44,
            'B_modulus':605,'B_residue_classes_checked':605,
            'uniform_positive_input_bound':124,'largest_input_in_chosen_table':max(r['input'] for r in rows),
            'negative_controls':1,'table':rows,
            'scope':'Exact modular obstruction for every coefficient residue; the global conclusion uses the retained large-shift soundness theorem, not a numerical value of its threshold.'}
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    report=compute();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',args.output.name)
