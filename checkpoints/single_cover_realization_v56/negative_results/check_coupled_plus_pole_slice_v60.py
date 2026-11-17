"""Exact identities and transfer to the previously certified E791 obstruction.

This does not infer nonexistence from bounded rational searches. The rank and
abscissa-image assertion is the explicit Monsky/Cassels certificate in the
repository's prepared_sha_v57 package, which this script reruns.
"""
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
import json
import subprocess
import sys
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPO = ROOT / "research-repo"
d, v, s, y, t, zz = S.symbols("d v s y t zz")
e = (d-v*v)/(d+v*v)
P = d*(d+v*v)**2*s**4-d*(d-v*v)**2*(1-d)**2
assert S.factor(P.subs(s**4, ((1+d)*e)**2)-(2*d*(d-v*v))**2) == 0
v2 = d*(1+d-s*s)/(1+d+s*s)
assert S.factor(v2*(1+d+s*s)**2-d*((1+d)**2-s**4)) == 0
assert S.factor((d-v2)/(d+v2)-s*s/(1+d)) == 0
poly = S.Poly(y*y-d*((1+d)**2-s**4), d, s, y)
assert poly.total_degree() == 5
assert max(abs(c) for c in poly.coeffs()) == 2

d0 = Fraction(448,13225)
assert 0 < d0 < 1 and d0 == 7*Fraction(8,115)**2
assert d0.denominator == 115**2 and d0.numerator % 64 == 0
assert d0.numerator % 128 != 0
assert 1+d0 == 113*Fraction(11,115)**2
scale = S.Rational(8*11**2,115**3)
q = (y*y-d*((1+d)**2-s**4)).subs({d:S.Rational(d0.numerator,d0.denominator),
      s:S.Rational(11,115)*t, y:scale*zz})
assert S.expand(q-scale**2*(zz*zz-7*(113**2-t**4))) == 0

valuation_cases = 0
for nu in range(-29,0,2):
    for vs in range(-30,31):
        a, b = 3*nu, nu+4*vs
        assert a%2 and b%2 and a != b and min(a,b)%2
        valuation_cases += 1

base = REPO/"negative_results/computation/prepared_sha_v57/check.py"
out = HERE/"coupled_plus_underlying_cassels_certificate.json"
run = subprocess.run([sys.executable,str(base),"--output",str(out)],
                     check=True,capture_output=True,text=True)
underlying = json.loads(out.read_text())
assert underlying["rank"] == 1
assert underlying["abscissa_image"] == [-791,-1,1,791]
assert underlying["excluded_abscissa_class"] == -7
cert = {
  "status":"PASS",
  "coupling":"s^2=(1+d)(d-v^2)/(d+v^2)",
  "slice":"y^2=d((1+d)^2-s^4)",
  "degree":5,"coefficient_height":2,
  "negative_odd_valuation_cases":valuation_cases,
  "valuation_proof":"Both radicand terms have distinct odd valuations for every negative odd v_p(d), including p=2.",
  "prepared_counterexample":str(d0),
  "two_adic_depth":6,
  "change_of_variables":{"s":"11t/115","y":"968z/1520875"},
  "target":"z^2=7(113^2-t^4)",
  "underlying_checker":str(base.relative_to(ROOT)),
  "underlying_checker_sha256":sha256(base.read_bytes()).hexdigest(),
  "underlying_certificate":out.name,
  "scope":"One specific coupled slice; no assertion that d0 is an actual detector value, and no exclusion of other coupled slices."
}
(HERE/"coupled_plus_pole_slice_v60_certificate.json").write_text(json.dumps(cert,indent=2)+"\n")
print(json.dumps(cert,indent=2))
