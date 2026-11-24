"""Exact algebraic checks for the ico cap and bounded-reference estimates.
No assertion about the retained arithmetic theorems or general completeness.
"""
from fractions import Fraction as Q
from itertools import combinations
import sympy as sp


def elementary(a, k):
    return sum(sp.prod(c) for c in combinations(a, k))


def chart(w, t):
    a = [(t-1)*(w*t+w-1), w+t-w*w*t-1,
         w*(1-t*t-w), t-w+w*w-t*t]
    A = sum(a)
    Z = [-A*sp.prod(a[l] for l in range(4) if l != i)
         for i in range(4)] + [sp.prod(a)]
    return a, A, Z


def inverse(Z):
    R = [sp.prod(Z[l] for l in range(5) if l != i) for i in range(5)]
    return [-(R[1]+R[3])*(R[0]+R[1]+R[2]),
            R[0]*sum(R[:4]), R[0]*(R[0]+R[2])]


def alpha0(v):
    return -4*(v*v+1)**4/(v*(v-2)*(v-1)*(v+1)*(v+3)*(2*v+1)*(3*v-1))


def alpha1(g):
    return -(5*g*g-2*g+1)**4/(g*(g-1)*(g+1)*(3*g-1)*(5*g-3)*(5*g-1)*(5*g+1))


w, t, a, u, z, g = sp.symbols('w t a u z g')
parts, A, Z = chart(w,t)
a0,a1,a2,a3=parts
assert sp.expand(A*elementary(parts,2)-elementary(parts,3)) == 0
assert sp.expand(-(a1+a3)*(a0+a1+a2)-w*a0*(a0+a2)) == 0
assert sp.expand(a0*A-t*a0*(a0+a2)) == 0
parts2 = [sp.factor(x.subs(t,2)) for x in parts]
assert sp.cancel(A.subs(t,2)*sum(1/x for x in parts2)-alpha0(w)) == 0
assert sp.cancel(alpha0(2*g/(g-1))-alpha1(g)) == 0
# Homogeneous radical degree: degree-two factor and eight linear factors.
n,d=sp.symbols('n d')
for fn,quad,lin in [(alpha0,n*n+d*d,[d,n,n-2*d,n-d,n+d,n+3*d,2*n+d,3*n-d]),
                   (alpha1,5*n*n-2*n*d+d*d,[d,n,n-d,n+d,3*n-d,5*n-3*d,5*n-d,5*n+d])]:
    denom=sp.prod(lin)
    const=4 if fn is alpha0 else 1
    assert sp.cancel(fn(n/d)+const*quad**4/denom)==0
    assert sp.Poly(quad*denom,n,d).total_degree()==10
F=z**4+a*z**3+a*z**2-u*(z+1)
C=27*u**3+(-4*a**3+12*a*a-48*a+256)*u*u+(8*a**4-60*a**3+128*a*a)*u-4*a**5+16*a**4
assert sp.expand(sp.discriminant(F,z)+u*C)==0
assert sp.expand(sp.discriminant(C,u)+16*a**5*(a+4)**2*(8*a*a-61*a+128)**3)==0
for av,expected in [(1,Q(11939,20449)),(2,Q(43753,69312))]:
    co=sp.Poly((u*C).subs(a,av),u).monic().all_coeffs()
    p={0:sp.Integer(4)}
    for k in range(1,5):
        p[k]=-sum(co[i]*p[k-i] for i in range(1,k))-k*co[k]
    mean=p[1]/4
    moment=lambda k: sum(sp.binomial(k,i)*(-mean)**(k-i)*p[i] for i in range(k+1))
    assert moment(4)/moment(2)**2==expected
assert 24*(-2+4*Q(1,2)+Q(2,3))==16
assert Q(133*289,299)-Q(1,1196)==Q(153747,1196)>120


def add(P,R):
    if P is None:return R
    if R is None:return P
    x,y=P; a,b=R
    if x==a:
        if y==-b:return None
        l=(3*x*x-2)/(2*y)
    else:l=(b-y)/(a-x)
    X=l*l-x-a
    return X,l*(x-X)-y


def check(w0, alpha):
    aa, A, Z=chart(w0,Q(2))
    assert A*sp.prod(aa)*aa[0]*(aa[0]+aa[2])!=0
    assert elementary(Z,2)==0 and elementary(Z,4)==0
    assert sum(Z[:4])+alpha*Z[4]==0
    R=inverse(Z)
    assert R[2]!=0 and R[0]==w0*R[2] and R[1]==2*R[2]
    assert alpha!=0


R0=(Q(2),Q(2));P=None;count=0
for h in range(1,17):
    P=add(P,R0); x,y=P
    g=abs((x*x+2)/(2*y))
    H=add(P,P)
    assert g*g==H[0] and g>1
    if g not in (1,2):
        check(g,alpha0(g));count+=1
    s=2*g/(g-1);r=(g+1)/(g-1)
    assert r*r==1+s*s/g
    check(s,alpha1(g));count+=1
for N in range(1,1001):
    d=4*N+20
    assert 20*(2*(d-N)-5)>=2*d+2
assert 20*404+20==8100 and 2*(8100+1)==16202
print(f'PASS: symbolic surface, inverse, radical-degree, discriminant, branch invariant, and precision identities; {count} actual rational elliptic chart fixtures; 1000 Taylor exponent checks.')
