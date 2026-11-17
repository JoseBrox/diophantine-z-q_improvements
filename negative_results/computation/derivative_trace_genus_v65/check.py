#!/usr/bin/env python3
"""Exact contact and first-order identities for the derivative trace cover.

Genus, normalization, and rational-curve conclusions are mathematical proofs
in the manuscript. No global trace-square witness is inferred from this check.
"""
from pathlib import Path
import argparse, hashlib, json
import sympy as s

HERE=Path(__file__).resolve().parent
SHIFTS=(-10,-8,-5,1,2,3,4,6,7)
a,z=s.symbols('a z')
u,q,J=s.symbols('u q J')
assert len(SHIFTS)==len(set(SHIFTS))==9
assert min(SHIFTS)==-10 and max(SHIFTS)==7
assert sum(SHIFTS)==0
# If a>10, a+c>0, and 2a+c+d>0 for all c,d in this fixed set.
assert min(20+c+d for c in SHIFTS for d in SHIFTS)>=0
assert min(20+c+d for c in SHIFTS for d in SHIFTS if c!=d)>0

F=s.Poly(s.prod((a+c)**2-z*z for c in SHIFTS),a,z).as_expr()
Fa=s.diff(F,a)
Fz=s.diff(F,z)
Faz=s.diff(Fa,z)
assert s.Poly(F,z).degree()==18
assert s.Poly(Fa,z).degree()==16
assert s.Poly(Fa,z).LC()==18*a
contacts=[]
for c in SHIFTS:
    Pc=s.prod((a+d)**2-(a+c)**2 for d in SHIFTS if d!=c)
    factored=s.prod((d-c)*(2*a+c+d) for d in SHIFTS if d!=c)
    assert s.expand(Pc-factored)==0
    assert all(d-c for d in SHIFTS if d!=c)
    for epsilon in (-1,1):
        contact=epsilon*(a+c)
        fc=s.expand(F.subs(z,contact))
        fac=s.expand(Fa.subs(z,contact))
        fzc=s.expand(Fz.subs(z,contact))
        assert fc==0
        assert s.expand(fac-2*(a+c)*factored)==0
        assert s.expand(fzc+2*epsilon*(a+c)*factored)==0
        # The full quotient-rule numerator specializes with F=0.
        derivative=s.cancel(-18*(fzc*fac-fc*Faz.subs(z,contact))/fac**2)
        assert derivative==18*epsilon
        contacts.append({'shift':c,'sign':epsilon,'slope':str(contact),
                         'weight_derivative':int(derivative),
                         'trace_radicand_derivative':int(2*derivative)})
assert len(contacts)==18

# A nonzero test q has a simple-zero reciprocal factor; q=0 gives factor1.
Di=q*q/(1+u*q*q)
reciprocal=s.cancel(1/(1+Di*Di/u))
num=u*(1+u*q*q)**2
den=u*(1+u*q*q)**2+q**4
assert s.cancel(reciprocal-num/den)==0
assert num.subs(u,0)==0 and s.diff(num,u).subs(u,0)==1
assert den.subs(u,0)==q**4
assert s.cancel(reciprocal.subs(q,0)-1)==0
# Four nonzero factors in each slot imply V=u^4*J(u) with regular J.
# J may have any constant/higher coefficients; none affects this 1-jet.
V=u**4*J
C=V*V+u/(1+u)**2*(2-V)
assert s.cancel(C.subs(u,0))==0
assert s.cancel(s.diff(C,u).subs(u,0))==2
assert s.cancel((C-2*u)/u**2).subs(u,0)==-4

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source',type=Path)
parser.add_argument('--output',type=Path,default=HERE/'certificate.json')
args=parser.parse_args()
if args.source is None:
    name='derivative_trace_genus_20261117_v65.tex'
    candidates=[HERE/name,HERE.parents[2]/'negative_results/papers/pole_parameters'/name]
    args.source=next((p for p in candidates if p.exists()),None)
    if args.source is None:parser.error('Use --source to specify the manuscript.')
report={
 'status':'PASS',
 'scope':'Exact polynomial contact identities and reciprocal/trace first-order identities; geometry is proved in the manuscript, not inferred from samples.',
 'source_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'pinned_derivative_source':'f70057ffce6b8318a79a7e3648779067fd98c2e3',
 'pinned_trace_criterion':'aa7013ce6129af0db621b89d5e44deaa07590b35',
 'shifts':SHIFTS,
 'hypothesis':'a>10; each slot has at least four nonzero finite tests',
 'contacts_checked':contacts,
 'reciprocal_nonzero_test_order_at_u_zero':1,
 'minimum_trace_order_at_u_zero':4,
 'trace_radicand_first_jet':'2*u',
 'minimum_simple_branch_points':18,
 'riemann_hurwitz_genus_lower_bound':8,
 'global_actual_trace_realization_proved':False,
 'actual_trace_criterion_disproved':False,
}
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','contacts_checked':len(contacts),
                  'derivatives_u':[-18,18],'derivatives_radicand':[-36,36]},indent=2))
