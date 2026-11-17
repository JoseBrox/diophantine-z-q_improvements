#!/usr/bin/env python3
"""Exact contraction and complete finite minimal-degree certificates."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sympy as sp

rows=[
 (Q(101,100),0,4,6,Q(520251,893855)),
 (Q(25,24),0,4,6,Q(8125,8379)),
 (Q(16,15),0,4,6,Q(68,45)),
 (Q(121,100),0,6,8,Q(1039511,648906)),
 (Q(101,100),2,4,8,Q(520251,1825346)),
 (Q(25,24),2,6,6,Q(8125,27531)),
 (Q(16,15),2,4,10,Q(68,171)),
 (Q(121,100),2,6,14,Q(1039511,2727159)),
]

def calc(kappa,e,d,k):
    eps=Q(d)-kappa*(d//2+2)
    alpha=Q(e)/kappa-3
    gamma=Q(8)/kappa-6
    if min(eps,alpha,gamma)<=0:
        return {'positive':False,'epsilon':str(eps),'alpha':str(alpha),'gamma':str(gamma)}
    q=(2*kappa-1)/(eps*alpha*gamma)
    contraction=(Q(k)+Q(1,2))*q
    return {'positive':True,'epsilon':str(eps),'alpha':str(alpha),'gamma':str(gamma),
            'q':str(q),'contraction':str(contraction),'admissible':contraction<1}

certificate_rows=[]
for kappa,k,e,d,expected in rows:
    data=calc(kappa,e,d,k)
    assert data['admissible']
    assert Q(data['q'])==expected
    degree=2*e*d
    smaller=[]
    # e>=4 and d>=6 are necessary for any kappa>1. These are all
    # even pairs of smaller degree, rather than a heuristic box search.
    for ep in range(4,degree//12+1,2):
        for dp in range(6,(degree-1)//(2*ep)+1,2):
            assert 2*ep*dp<degree
            check=calc(kappa,ep,dp,k)
            assert not check.get('admissible',False)
            smaller.append({'e':ep,'d':dp,'degree':2*ep*dp,**check})
    certificate_rows.append({'kappa':str(kappa),'support_degree':k,'e':e,'d':d,
                             'argument_degree':degree,**data,
                             'all_smaller_even_pairs':smaller})

d,kappa,m=sp.symbols('d kappa m',positive=True)
eps=d-kappa*(d/2+2)
coef=(2*kappa-1)/eps
assert sp.simplify(sp.diff(coef,kappa)-(3*d/2-2)/eps**2)==0
epsdm=d*m-kappa*(d*m/2+2)
assert sp.simplify(epsdm-m*eps-2*kappa*(m-1))==0
e=sp.symbols('e',positive=True)
q=coef/((e/kappa-3)*(8/kappa-6))
assert sp.simplify(q.subs(kappa,1)-1/((d-4)*(e-3)))==0

# Exact polynomial degree in the retained rational coordinates.
X,h0,h1,z=sp.symbols('X h0 h1 z')
beta=X*X+3
T=2*(h0*h0+2*h1*h1)
for e0,d0 in sorted(set((r[2],r[3]) for r in rows)):
    # Total degrees of sums/powers can be checked from leading forms
    # without expanding the full high-degree polynomial.
    Hlead=(X*X)**e0+(2*(h0*h0+2*h1*h1))**e0
    assert sp.Poly(Hlead,X,h0,h1).total_degree()==2*e0
    assert Hlead.coeff(X,2*e0)==1
    assert 2*e0*d0>2

cert={'status':'PASS','rows':certificate_rows,
      'ordinary_abc_minimum_argument_degrees':{'k0':48,'k2':64},
      'degree_formula':'2*e*d; this is the scalar argument degree, not the defining determinant degree.',
      'scope':'Soundness/height criteria only; actual rational realization remains unproved, defining counts remain25/13.'}
Path(__file__).with_name('single_cover_height_criteria_v58_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({'status':'PASS','rows':[{k:v for k,v in r.items() if k!='all_smaller_even_pairs'} for r in certificate_rows],
                  'excluded_smaller_pairs':sum(len(r['all_smaller_even_pairs']) for r in certificate_rows)},indent=2))
