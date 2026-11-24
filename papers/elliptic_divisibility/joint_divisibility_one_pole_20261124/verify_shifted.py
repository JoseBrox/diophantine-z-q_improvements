# Run alongside verify.py (also reruns the base fixtures).
from verify import Q,P,mul,v,isqrt

def shifted(h,shifts,js):
    Ls={a:mul(h+a,P)[1] for a in set(shifts)}
    L=sum(Ls.values(),Q(0)); assert L
    C=sum((Ls[a]**2/(1+L**2))*(1-1/(1+L**2/mul(j,P)[0]**4))
          for a,j in zip(shifts,js))
    return 1+L*C*C

def prime_support(n):
    n=abs(n); p=2; out=set()
    while p*p<=n:
        while n%p==0:out.add(p);n//=p
        p+=1
    if n>1:out.add(n)
    return out

checks=reject=0
for shifts in ((0,1),(0,2,3),(0,0,2)):
    S={2,7}|set(range(2,len(shifts)+1))
    for a in set(shifts):
        for d in set(shifts):
            if a!=d:S|=prime_support(mul(a-d,P)[0].denominator)
    for h in range(4,8):
        for ms in (tuple(1+i for i in range(len(shifts))),tuple(-2 for i in shifts)):
            b=shifted(h,shifts,[m*(h+a) for a,m in zip(shifts,ms)])
            den=b.denominator
            for p in S:
                while den%p==0:den//=p
            assert isqrt(den)**2==den
            checks+=1
    for p in (3,5,11,13,17,19,23,31,37,41,43,47,53):
        if p in S:continue
        for h in range(4,15):
            for a in set(shifts):
                n=h+a
                if v(mul(n,P)[0],p)!=-2:continue
                if any(v(mul(j,P)[0],p)<0 for j in range(1,n)):continue
                js=[2*(h+b) for b in shifts];js[shifts.index(a)]=1
                assert v(shifted(h,shifts,js),p)==-3
                reject+=1
                break
            else:continue
            break
assert reject>0
print(f'PASS: {checks} shifted true-multiple fixtures outside finite exclusions, {reject} shifted primitive-prime rejections')
