#!/usr/bin/env python3
"""Exact norm identities and a physical balanced-detector counterexample.

The ramification and abelian-family assertions are proved in the companion
manuscript. Finite valuation cases here are supplementary checks only.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt,prod
from pathlib import Path
from hashlib import sha256
import json
import sympy as sp

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]

class K:
    def __init__(self,a=0,b=0):self.a,self.b=Q(a),Q(b)
    def __add__(self,o):
        if not isinstance(o,K):o=K(o)
        return K(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return K(-self.a,-self.b)
    def __sub__(self,o):return self+-o if isinstance(o,K)else self+K(-o)
    def __rsub__(self,o):return K(o)+-self
    def __mul__(self,o):
        if not isinstance(o,K):o=K(o)
        return K(self.a*o.a+2*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def conj(self):return K(self.a,-self.b)
    def norm(self):return self.a*self.a-2*self.b*self.b
    def inverse(self):
        n=self.norm();assert n
        return K(self.a/n,-self.b/n)
    def __truediv__(self,o):return self*(o if isinstance(o,K)else K(o)).inverse()
    def __rtruediv__(self,o):return K(o)*self.inverse()
    def __pow__(self,n):
        assert n>=0;r=K(1);x=self
        while n:
            if n&1:r=r*x
            n//=2;x=x*x
        return r
    def __eq__(self,o):
        if not isinstance(o,K):o=K(o)
        return self.a==o.a and self.b==o.b
    def sign(self):
        a,b=self.a,self.b
        if not b:return (a>0)-(a<0)
        if not a:return (b>0)-(b<0)
        if a>0 and b>0:return 1
        if a<0 and b<0:return -1
        diff=a*a-2*b*b;assert diff
        return ((diff>0)-(diff<0))*((a>0)-(a<0))
    def data(self):return [str(self.a),str(self.b)]

def point_add(P,Qp,D):
    if P==Qp:lam=(3*P[0]**2-D)/(2*P[1])
    else:lam=(Qp[1]-P[1])/(Qp[0]-P[0])
    x=lam*lam-P[0]-Qp[0];y=lam*(P[0]-x)-P[1]
    assert y*y==x*x*x-D*x
    return x,y

def valuation(x,p):
    x=Q(x);assert x
    def vp(n):
        n=abs(n);v=0
        while n%p==0:n//=p;v+=1
        return v
    return vp(x.numerator)-vp(x.denominator)

def residue(x,m):
    x=Q(x);return x.numerator*pow(x.denominator,-1,m)%m

def universal_identities():
    a,b,c,d,u=sp.symbols('a b c d u')
    W0=a*a+2*b*b+u*(c*c+2*d*d)
    W1=2*(a*b+u*c*d)
    C=a*a-2*b*b-u*(c*c-2*d*d)
    E=2*(a*c-2*b*d)
    N=W0*W0-2*W1*W1
    assert sp.expand(N-C*C-u*E*E)==0
    assert sp.expand(N-(a*a-2*b*b+u*(c*c-2*d*d))**2-8*u*(a*d-b*c)**2)==0
    assert sp.expand(W0*W0-C*C-u*E*E-2*W1*W1)==0
    # Symbolic rescaling of the general17 native conic, including its
    # first ordinate. This confirms the guarded chart uses the same input.
    dd,t,tau=sp.symbols('dd t tau',nonzero=True)
    bb=dd*t*t;den=tau*tau+51*dd;e=(tau*tau-17*dd)/den
    p0=-68*dd*t*tau/den
    assert sp.cancel(p0*p0-17*bb*(1-e)*(1+3*e))==0
    return {'two_cross_norm_identities':True,'rational_quadric_identity':True,'general17_first_conic_rescaling':True}

def parity_cases():
    count=0
    for nu in range(-39,0,2):
        for v in range(-30,31):
            r=min(nu,2*v)
            for s in range(-30,31):
                first=nu+2*r+4*s;second=3*nu+2*r
                assert first%2==second%2==1 and first!=second
                count+=1
    return count

def native_pre_pole_guards(P,R,hp,z):
    path=REPO/'computation/few_variables/seven_contact11_v74/specification/source.json'
    source=json.loads(path.read_text())
    labels={label:node for node,label in source['guard_descriptions']}
    end=labels['intrinsic.input']
    guards=[g for g in source['guard_numerators']if g<=end]
    q=1000000007;rt=pow(2,(q+1)//4,q);assert rt*rt%q==2
    def embed(x,root):return(residue(x.a,q)+residue(x.b,q)*root)%q
    names={v['name']:v['index']for v in source['variables']}
    fixed={'input.X':Q(1),'A.a0':hp.a,'A.a1':hp.b,
           'H.a0':R[0].a,'H.a1':R[0].b,'UA.a0':R[0].a,'UA.a1':R[0].b,
           'contact.z':z}
    ordinates={'A':P[1]/hp,'H':R[1],'UA':R[1]}
    count=0
    for signs in product((-1,1),repeat=6):
        variables=[0]*len(names)
        for name,val in fixed.items():variables[names[name]]=residue(val,q)
        for i,name in enumerate(['A','H','UA']):
            jp=signs[2*i]*embed(ordinates[name],rt)%q
            jm=signs[2*i+1]*embed(ordinates[name],-rt)%q
            variables[names[name+'.U']]=(jp+jm)%q
            variables[names[name+'.V']]=(jp-jm)*pow(rt,-1,q)%q
            variables[names[name+'.W']]=jp*jm%q
        values=[]
        for op,*args in source['coefficient_dag'][:end+1]:
            if op=='int':v=args[0]
            elif op=='parameter':v=args[1]
            elif op=='variable':v=variables[args[0]]
            elif op=='neg':v=-values[args[0]]
            elif op=='add':v=sum(values[i]for i in args)
            elif op=='mul':v=prod(values[i]for i in args)
            elif op=='pow':v=pow(values[args[0]],args[1],q)
            else:raise AssertionError(op)
            values.append(v%q)
        assert all(values[g]!=0 for g in guards)
        count+=len(guards)
    return {'source_path':str(path.relative_to(REPO)),'source_sha256':sha256(path.read_bytes()).hexdigest(),'reduction_prime':q,'sqrt2_mod_prime':rt,'pre_pole_guard_count':len(guards),'characters':64,'guard_nonzero_evaluations':count,'all_guard_values_nonzero':True,'scope':'Exact finite reduction of the actual algebraic point characters. Nonzero reductions prove the characteristic-zero native pre-pole guard values are nonzero; no pole variables are supplied.'}

def physical_example():
    p=100003
    assert all(p%d for d in range(2,isqrt(p)+1))
    D=K(11,-6);R=(K(1,1),K(0,2));P=point_add(R,R,D)
    expected=(K(Q(57,8),Q(-7,2)),K(Q(-165,8),Q(417,32)))
    assert P==expected
    R3=point_add(R,P,D)
    for point in [R,P,R3]:
        assert point[1]**2==point[0]**3-D*point[0]
        assert point[0].norm()and point[1].norm()
    assert (P[0]-R[0]).norm()
    hp=K(-1,Q(7,4));assert hp*hp==P[0]
    M=Q(4)**4+Q(57,4)**4
    assert M==Q(10621537,256)
    a=M**8;z=a+8+p;shifts=(-7,-6,-4,1,3,5,8)
    factors=[(a+c)**2-z*z for c in shifts]
    F=prod(factors)
    Fa=sum(2*(a+c)*prod(factors[j]for j in range(7)if j!=i)for i,c in enumerate(shifts))
    u=-14*F/Fa
    assert a>10 and z>a+10 and u>2*p
    assert valuation(F,p)==1 and valuation(Fa,p)==0 and valuation(u,p)==1
    w=u/(1+u)**2
    DD=u*u*(u*u+6*u+1)**2
    RR=DD+2*u**3+12*u*u+34*u+1
    W=(RR/DD)**2;V=2/W;b=w*W*W
    values={'F':valuation(F,p),'F_a':valuation(Fa,p),'u':valuation(u,p),'w':valuation(w,p),'D_poly':valuation(DD,p),'R_poly':valuation(RR,p),'W':valuation(W,p),'V':valuation(V,p),'b':valuation(b,p),'eta_7b':valuation(7*b,p)}
    assert values=={'F':1,'F_a':0,'u':1,'w':1,'D_poly':2,'R_poly':0,'W':-4,'V':4,'b':-7,'eta_7b':-7}
    c=1/R[0];assert c==K(-1,1)
    tests=[c,c,c.conj(),c.conj(),K(0),K(0)]
    actual=K(1);A,B=K(1),K(0)
    for ci in tests:
        di=ci*ci/(1+u*ci*ci)
        actual=actual*(1+di*di/u)
        A,B=A-B*di,B+A*(di/u)
    assert actual==W and A*A+u*B*B==actual
    assert A.b==B.b==0
    assert V==2/actual.a and b==4*w/V**2

    # Six independent ordinate signs across the three rank-four point blocks.
    # Every difference in either real slot is +/-R or +/-3R. All old point
    # guards reduce to the nonzero coordinates checked above. The following
    # exact computations additionally check every balanced denominator.
    checked=0;balanced_checks=0
    base=[P,R,R]
    for signs in product((-1,1),repeat=6):
        slots=[]
        for slot in range(2):
            pts=[]
            for i,point in enumerate(base):
                x,y=(tuple(q.conj()for q in point)if slot else point)
                pts.append((x,signs[2*i+slot]*y))
            As,Hs,Us=pts;Ds=D.conj()if slot else D
            fixed=(P[0].conj(),P[1].conj())if slot else P
            hm=point_add(Hs,(fixed[0],-fixed[1]),Ds)
            um=point_add(Us,(As[0],-As[1]),Ds)
            for point in [As,Hs,Us,hm,um]:assert point[0]!=0 and point[1]!=0
            rr=(-Us[0]/Us[1])/(-Hs[0]/Hs[1])
            rp=(-um[0]/um[1])/(-hm[0]/hm[1])
            slots.append((1/Hs[0],1/Us[0],1/hm[0],1/um[0],rr,rp))
        for slot in range(2):
            here,other=slots[slot],slots[1-slot]
            Cs=[here[0],here[1],other[2],other[3],here[4]-other[5],here[4]-1]
            for ci in Cs:
                denominator=1+u*ci*ci
                assert denominator.sign()>0
                balanced_checks+=1
        checked+=1
    assert checked==64 and balanced_checks==768
    native=native_pre_pole_guards(P,R,hp,z)
    return {'prime':p,'prime_verified_by_trial_division':True,'input_X':1,'fixture_B':3,'root_A':'P','auxiliary_H_U':'R=(1+sqrt(2),2*sqrt(2))=P/2','duplication_and_triple_checked':True,'P': [x.data()for x in P],'triple_R':[x.data()for x in R3],'M':str(M),'scale_a':str(a),'slope_z':str(z),'slope_rule':'z=a+8+100003','contact_shifts':list(shifts),'physical_u':str(u),'physical_u_greater_than_2p':True,'residues_mod_p_squared':{'a':residue(a,p*p),'z':residue(z,p*p),'F':residue(F,p*p),'F_a':residue(Fa,p*p)},'u_over_p_mod_p':residue(u/p,p),'valuations':values,'actual_balanced_product_and_norm_composition_checked':True,'pre_pole_real_point_characters_checked':checked,'balanced_denominators_checked_positive':balanced_checks,'native_pre_pole_guards':native,'all_pre_pole_whole_character_guards':True,'native_pole_witness_impossible':True,'scope':'Actual seven-contact physical slope and multiplication tuple for the original squared-balanced v74 source. All pre-pole point/contact/balanced/product/trace guards hold at every point character. No fixed-place or selected-prime preparation is claimed; the negative odd b valuation excludes every intrinsic native pole witness.'}

def main():
    report={'schema':'native-pole-ramification-finite-checks/v75','status':'PASS','universal_symbolic_identities':universal_identities(),'intrinsic_negative_odd_boundary_cases':parity_cases(),'physical_norm_counterexample':physical_example(),'fixed_point_contact_counts':[10,14,18],'minimum_genus_for_degree_two':[4,6,8],'scope':'Exact algebra and explicit physical counterexample. General valuation, ramification and abelian-family theorems are proved in the manuscript, not inferred from finite checks. No 21/9-variable realization or impossibility theorem is claimed.'}
    (HERE/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','prime':report['physical_norm_counterexample']['prime'],'valuations':report['physical_norm_counterexample']['valuations'],'pre_pole_characters':64,'balanced_denominators':768},indent=2))

if __name__=='__main__':main()
