"""Exact integer interval certificate of analytic rank one for y²=x³−791²x."""
from fractions import Fraction as Q
from math import isqrt

D=791
K=12000
J=16
S=10**22
def ceil(a,b):return -((-a)//b)
def floorq(r):return r.numerator//r.denominator
def ceilq(r):return ceil(r.numerator,r.denominator)

# c=2pi/sqrt(32 D²)=pi/(2 sqrt(2) D). Use classical rational bounds.
rt=10**12
sq2=isqrt(2*rt**2)
lo=Q(314159,100000)*rt/(2*D*(sq2+1))
hi=Q(314160,100000)*rt/(2*D*sq2)
# 1-x <= exp(-x) <= 1-x+x²/2, all powers rounded outward at scale S.
qlo=floorq(S*(1-hi/J))
qhi=ceilq(S*(1-lo/J+(lo/J)**2/2))
assert 0<qlo<qhi<S
size=K*J
lower=[0]*(K+1);upper=[0]*(K+1)
pl=pu=S
terms=[]
for k in range(1,size+1):
    pl=(pl*qlo)//S;pu=ceil(pu*qhi,S)
    terms.append((pl//k,ceil(pu,k)))
# Above the final mesh endpoint sum q^k/k by a geometric majorant.
L=0; U=ceil(pu*S,size*(S-qhi))
for k in range(size,0,-1):
    a,b=terms[k-1]
    if k%J==0:lower[k//J]=L
    L+=a;U+=b
    if k%J==0:upper[k//J]=U

least=list(range(K+1))
for i in range(2,isqrt(K)+1):
    if least[i]==i:
        for j in range(i*i,K+1,i):
            if least[j]==j:least[j]=i
ap={}
for p in range(2,K+1):
    if least[p]!=p:continue
    if (2*D)%p==0 or p%4==3:ap[p]=0;continue
    squares={j*j%p for j in range(1,(p+1)//2)}
    # The cubic's three roots each contribute zero.
    cubic=[(x*(x*x-D*D))%p for x in range(p)]
    ap[p]=sum(0 if f==0 else -1 if f in squares else 1 for f in cubic)
coef=[0]*(K+1);coef[1]=1
for n in range(2,K+1):
    p=least[n];m=n//p
    coef[n]=ap[p]*coef[m]
    if m%p==0 and (2*D)%p:coef[n]-=p*coef[m//p]
anslo=anshi=0
for n in range(1,K+1):
    a=coef[n];l,u=lower[n],upper[n]
    if a<0:l,u=u,l
    anslo+=a*l//n;anshi+=ceil(a*u,n)
# |a_n| <= tau(n) sqrt(n) <= 2n. E1(cn)<=exp(-cn)/(cn).
# Use qhi^J as a geometric ratio for exp(-c).
rho=ceilq(S*Q(qhi,S)**J)
tail=ceilq(2*Q(pu,1)/(lo*K*(1-Q(rho,S))))
lo_scaled=2*(anslo-tail);hi_scaled=2*(anshi+tail)
assert lo_scaled>0
print(f"L'(E_791,1) in [{lo_scaled}/{S},{hi_scaled}/{S}]")
print(f"containing interval [{lo_scaled//(S//1000)/1000}, {ceil(hi_scaled,S//1000)/1000}]")
