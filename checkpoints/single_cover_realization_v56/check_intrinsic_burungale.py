#!/usr/bin/env python3
"""Exact algebra and expansion for the intrinsic prepared pole theorem."""
from pathlib import Path
import json
import sympy as S

d,v,s,b,u = S.symbols("d v s b u")
P = d*(d+v**2)**2*s**4-d*(d-v**2)**2*(1-d)**2
e=(d-v**2)/(d+v**2)
p=2*d*v/(d+v**2)
assert S.cancel(p**2-d*(1-e**2)) == 0
assert S.cancel(P-(d+v**2)**2*d*(s**4-e**2*(1-d)**2)) == 0
old=343*b*(7*b+u**2)**2*s**4-7*b*(7*b-u**2)**2*(b-7)**2
assert S.expand(old.subs({b:7*d,u:7*v})-7**8*P) == 0
poly=S.Poly(P,d,v,s)
assert poly.total_degree()==9
assert len(poly.terms())==12
assert max(abs(c) for c in poly.coeffs())==4
fixture={d:S.Rational(112,841),v:S.Rational(4,29),s:S.Rational(27,29)}
fixture_Y=S.Rational(653184,20511149)
assert S.factor(fixture_Y**2-P.subs(fixture))==0
assert S.factor((d*s*(d-v**2)*(1-d)*(d+v**2)).subs(fixture))!=0
assert 28**3-21**2*28==98**2
certificate={
    "total_degree":9,"monomials":12,"coefficient_height":4,
    "terms":[{"exponents":list(m),"coefficient":int(c)}
             for m,c in poly.terms()],
    "checks":["conic parametrization","cleared second curve",
              "scaled radicand factor 7^8","root scaling 2401",
              "prepared rational fixture","point (28,98) on E_21"],
    "prepared_fixture":{"d":"112/841","v":"4/29","s":"27/29",
                        "Y":"653184/20511149","underlying_curve_parameter":21,
                        "underlying_point":[28,98]},
    "scope":"Exact algebra; arithmetic completeness retains Burungale Theorem B."
}
target=Path(__file__).with_name("intrinsic_burungale_certificate.json")
target.write_text(json.dumps(certificate,indent=2)+"\n")
print(json.dumps({"checks":"passed","certificate":str(target),
                  "degree":9,"monomials":12,"height":4}))
