from math import gcd

def ordinate(n,a):
    x,y=0,1
    for _ in range(n): x,y=y,2*a*y-x
    return x

def data(b,q,s,L):
    A=b//2+(b*b-1)*q*s
    m=2*b*A-b*b-1
    V=1+2*(b+1)*q*s
    Cq=2*b*b*s*(q*q-1)
    C0=Cq-m*V*V*(L-Cq)
    assert (b-1)*V==2*A-1
    assert gcd(m,A-1)==1
    assert (C0-L)%(A-1)==0 and (C0-Cq)%m==0
    return A,m,V,Cq,C0

checks=0
for b in [2,4,8,16]:
    for q in [-17,-3,1,2,7,19]:
        for s in [-9,-1,1,3]:
            for L in [5,25,125]:
                A,m,V,Cq,C0=data(b,q,s,L)
                y=ordinate(L,A)
                K=b**L
                assert ((b*b-1)*y*K-b*(K*K-1))%m==0
                if (y-Cq)%m==0:
                    assert ((q-K)*(q*K+1))%m==0
                checks+=1
for b in [2,4,8,16]:
    for L in [5,25,125]:
        q=b**L
        for s in [1,3,7]:
            A,m,V,Cq,C0=data(b,q,s,L)
            y=ordinate(L,A)
            assert (y-C0)%(m*(A-1))==0
            assert (q-1)%(b**5-1)==0
            G=(q-1)//(b**5-1)
            assert G*(q**3+q**2+q+1)*(b**5-1)==q**4-1
            checks+=1
print(checks,'exact signed/canonical fixtures passed')
