"""Check the complete quartic against direct physical field and scalar equations."""
import json
from itertools import product
from collections import defaultdict
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
DIREC=Path(__file__).resolve().parent
# Keys are (power of B, Laurent power of c, sparse coordinate monomial).
def atom(i=None,value=1,b=0,c=0):
 return {(b,c,(i,) if i else ()):Q(value)} if value else {}
def add(*pp):
 d=defaultdict(Q)
 for p in pp:
  for k,v in p.items():d[k]+=v
 return {k:v for k,v in d.items() if v}
def times(*pp):
 z=atom()
 for p in pp:
  d=defaultdict(Q)
  for (b,c,m),v in z.items():
   for (j,e,n),w in p.items():d[b+j,c+e,tuple(sorted(m+n))]+=v*w
  z={k:v for k,v in d.items() if v}
 return z
def minus(p):return {k:-v for k,v in p.items()}
def sub(p,q):return add(p,minus(q))
def sq(p):return times(p,p)
def ff(i):return (atom(i),atom(i+1))
def fc(a,b=0):return (atom(value=a),atom(value=b))
def fk(p):return (p,{})
def fadd(*v):return tuple(add(*a) for a in zip(*v))
def fsub(x,y):return sub(x[0],y[0]),sub(x[1],y[1])
def fmul(x,y):return add(times(x[0],y[0]),times(atom(value=2),x[1],y[1])),add(times(x[0],y[1]),times(x[1],y[0]))
def fscale(x,p):return times(x[0],p),times(x[1],p)
def fbar(x):return x[0],minus(x[1])
def fsq(x):return fmul(x,x)
def direct():
 c=atom(c=1);cinv=atom(c=-1);one=atom();half=atom(value=Q(1,2));two=atom(value=2)
 S,T,v=ff(3),ff(5),ff(7);k=fc(4,-2);di=fc(-23,17);ai=fc(-1,1);dcurve=fc(11,-6)
 u=fmul(ai,fsub(fsub(v,k),S));wref=fmul(ai,fsub(fadd(v,T),k));fieldrows={}
 ref1=fadd(fmul(v,fsub(fadd(v,T),S)),di);ref2=fadd(fmul(S,T),fmul(k,fsub(fadd(T,fscale(v,two)),S)),fscale(di,two))
 rows={f'reference.primitive.{i+1}':z for i,z in enumerate(ref1+ref2)}
 s,t,F,G,h,d=[ff(i) for i in [10,12,14,16,18,20]];pi=fadd(h,s,t);sd=fsub(s,t)
 rows['pair.differenceReal']=sub(atom(9),fmul(h,pi)[0])
 fieldrows.update({'pair.firstProduct':fsub(d,fmul(pi,F)),'pair.secondProduct':fsub(d,fmul(h,G)),
 'pair.secant':fadd(fsub(fmul(dcurve,fadd(F,G)),fmul(sd,h)),fsq(t)),
 'pair.scale':fadd(fsub(fk(atom(31)),fmul(d,sd)),fmul(dcurve,fmul(F,G)))})
 # P,Q = C² ± c bar(I)²; U,V = J ± c bar(K).
 P,Q_,U,V=ff(26),ff(28),ff(22),ff(24)
 J=fscale(fadd(U,V),half);K=fbar(fscale(fsub(U,V),times(half,cinv)))
 fieldrows['product.first']=fsub(fmul(v,J),fmul(u,F));fieldrows['product.second']=fsub(fmul(v,K),fmul(wref,G))
 for n,z in fieldrows.items():
  for j in range(2):rows[n+'.'+str(j)]=z[j]
 rels={'C':fsub(fscale(fadd(P,Q_),half),fsq(fsub(s,S))),
       'I':fsub(fbar(fscale(fsub(P,Q_),times(half,cinv))),fsq(fsub(t,T)))}
 W=ff(40);rels['product']=fsub(W,fadd(fc(1),fscale(fmul(P,Q_),c),fscale(fmul(U,V),sq(c))))
 for n,z in rels.items():
  for j in range(2):rows[n+str(j)]=z[j]
 rows['height.betaSquare']=sub(atom(30),sq(atom(1)));rows['height.betaFourth']=sub(atom(31),sq(atom(30)))
 rows['detector1.argument']=sub(sub(atom(32),atom(2)),add(atom(b=1),sq(atom(31)),times(atom(value=4),sq(atom(9)))))
 DD=atom(71);wm=fsub(W,fc(1));rows['sharedD']=sub(times(two,W[0],DD),fmul(wm,fbar(wm))[0])
 polefirsts=[]
 for n,(ti,off) in enumerate([(2,0),(32,18)]):
  det='detector'+str(n)+'.';r,z,w,eta,b,e,u,p,vv,qq,p2,q2=[atom(i+off) for i in (33,34,35,42,43,44,45,46,47,48,49,50)]
  t=atom(ti);qj=atom(73) if n==0 else sub(c,atom(73))
  rows[det+'contactSquare']=sub(r,sub(sq(t),times(two,t)))
  rows[det+'contactSum']=sub(times(add(r,one),z),sub(sq(r),times(atom(value=35),r)))
  rows[det+'inverseContact']=sub(times(add(r,one),w),add(sq(z),times(atom(value=24),z)))
  rows[det+'pole.pSquare']=sub(p2,sq(p));rows[det+'pole.qSquare']=sub(q2,sq(qq))
  polefirsts.append(sub(add(sq(e),times(b,p2)),one))
  rows[det+'pole.first']=polefirsts[-1] if n==0 else sub(polefirsts[-1],polefirsts[0])
  rows[det+'pole.factor']=sub(times(u,vv),times(e,sub(one,b)))
  rows[det+'pole.second']=sub(sub(sq(u),sq(vv)),times(b,q2))
  rows['weight'+str(n)]=sub(times(w,qj),one)
  rows['gate'+str(n)]=sub(times(two,w,eta),add(w,times(sq(c),w),minus(times(two,c)),qj,sq(DD)))
  rows['pole'+str(n)]=sub(times(qj,b),sq(eta))
 return rows
def norm(p):
 d=p[min(p)]
 return {k:v/d for k,v in p.items()}
def main():
 s=json.loads((DIREC/'quadrics.json').read_text());cert=json.loads((DIREC/'weights.json').read_text());pp=json.loads((DIREC/'polynomial.json').read_text())
 exp=direct();ids=s['sourceIds'];ws={int(i):v for i,v in cert['weights'].items()};div=cert['divs'];assert ids==sorted([*ws,100,101]) and len(ids)==62 and ws[1]==0 and set(div)==set(exp)
 total=defaultdict(int)
 for r in s['residuals']:
  n=r['name'];q={(z['parameterPower'],tuple(z['monomial'])):int(z['coefficient']) for z in r['terms']}
  assert max(len(m) for b,m in q)<=2
  for ((b,m),v),((bb,nn),w) in product(q.items(),repeat=2):total[b+bb,tuple(sorted(m+nn))]+=v*w
  if n=='shared.unit':
   assert q=={(0,()):-1,(0,(ids.index(100)+1,ids.index(101)+1)):1}
   continue
  decoded=defaultdict(Q)
  for (b,mo),coef in q.items():
   m=tuple(ids[i-1] for i in mo);native=tuple(i for i in m if i<100);powc=div[n]+m.count(100)-m.count(101)-sum(ws[i] for i in native)
   decoded[b,powc,native]+=coef
  decoded={k:v for k,v in decoded.items() if v}
  assert norm(exp.pop(n))==norm(decoded),n
 assert not exp and len(s['residuals'])==50
 total={k:v for k,v in total.items() if v};g=gcd(*total.values());total={k:v//g for k,v in total.items()}
 assert total=={(z['parameterPower'],tuple(z['monomial'])):int(z['coefficient']) for z in pp['terms']}
 profiles=defaultdict(dict)
 for (b,m),v in total.items():profiles[m][b]=v
 assert len(profiles)==830 and len(total)==833 and max(map(len,profiles))==4
 assert set(i for m in profiles for i in m)==set(range(1,63))
 fixed=[p[0] for p in profiles.values() if set(p)=={0}]
 assert max(map(abs,fixed))==1548 and gcd(*fixed)==1
 assert sorted((p.get(0,0),p.get(1,0),p.get(2,0)) for p in profiles.values() if max(p)>0)==sorted([(1,2,0),(0,2,0),(1,8,0),(0,-2,0),(4091,0,1)])
 balanced=json.loads((DIREC/'parameter-scaling.json').read_text())
 ws=balanced['variable_powers'];divs=balanced['row_powers'];assert ws[0]==0 and len(ws)==62 and len(divs)==50
 alt=defaultdict(int);rr=[]
 for j,r in enumerate(s['residuals']):
  tr=[(4*t['parameterPower']+sum(ws[i-1] for i in t['monomial'])-divs[j],tuple(t['monomial']),int(t['coefficient'])) for t in r['terms']]
  rr.append({(e,m):v for e,m,v in tr})
  assert all(0<=e<=2 for e,m,v in tr)
  for (e,m,v),(f,n,w) in product(tr,repeat=2):alt[e+f,tuple(sorted(m+n))]+=v*w
 alt={k:v for k,v in alt.items() if v}
 test=json.loads((DIREC/'polynomial-n.json').read_text())
 assert alt=={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in test['terms']}
 ap=defaultdict(dict)
 for (e,m),v in alt.items():ap[m][e]=v
 assert len(ap)==830 and len(alt)==831 and gcd(*(p[0] for p in ap.values() if set(p)=={0}))==1
 assert [max([abs(v) for (e,m),v in alt.items() if e==i],default=0) for i in range(5)]==[4091,16,44,4,1]
 assert sorted(sorted(p.items()) for p in ap.values() if len(p)>1)==[[(0,4091),(4,1)]]
 sparse=json.loads((DIREC/'sparsity.json').read_text())
 for i,j,n,d in sparse['ops']:
  assert i!=j and d
  pp={k:d*rr[i].get(k,0)+n*rr[j].get(k,0) for k in set(rr[i])|set(rr[j])};pp={k:v for k,v in pp.items() if v}
  gg=gcd(*pp.values())*(1 if pp[min(pp)]>0 else -1);rr[i]={k:v//gg for k,v in pp.items()}
 sparse_poly=defaultdict(Q)
 for r,wgt in zip(rr,sparse['weights'],strict=True):
  wgt=Q(wgt);assert wgt>0
  for ((e,m),v),((f,n),w) in product(r.items(),repeat=2):sparse_poly[e+f,tuple(sorted(m+n))]+=v*w*wgt
 zz={k:v for k,v in sparse_poly.items() if v};gg=gcd(*(int(v) for v in zz.values()));assert all(v.denominator==1 for v in zz.values());zz={k:v//gg for k,v in zz.items()}
 sp=json.loads((DIREC/'sparse-n.json').read_text())
 assert zz=={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in sp['terms']}
 zzp=defaultdict(dict)
 for (e,m),v in zz.items():zzp[m][e]=v
 assert len(zzp)==757 and len(zz)==758 and gcd(*(int(p[0]) for p in zzp.values() if set(p)=={0}))==1
 assert [max([abs(v) for (e,m),v in zz.items() if e==i],default=0) for i in range(5)]==[758541,16,44,4,1]
 assert [p for p in zzp.values() if len(p)>1]==[{0:758541,4:1}]
 print('Equivalent sparsified family for odd n>=3: 757 monomials, content one, height B+758541.')
 print('On B=n^4 for every odd n>=3: 830 monomials, content 1, exact height B+4091.')
 print('62 variables, 50 quadratic squares, 830 monomials, primitive, height B^2+4091 for every integer B>=81. Physical equations and expansion verified.')
if __name__=='__main__':main()
