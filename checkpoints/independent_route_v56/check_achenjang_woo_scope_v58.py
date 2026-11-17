"""Exact formulas in a source-scope checkpoint; no rank-table assumptions."""
import json
from itertools import permutations
from pathlib import Path
import sympy as S

v, x = S.symbols("v x")
G = -(v*v+4)*(v*v-1)*(v*v-16)/S.Integer(125)
points = [
    (G*(1-v*v)/5, G*G),
    (G*(v*v-16)/(5*v*v), -8*G*G/v**3),
]
for xx, yy in points:
    assert S.cancel(yy**2 - xx*(xx-G)*(xx+3*G)) == 0
classes = [(v*v+4)*(v*v-16), -(v*v+4)*(v*v-1)]
squares = [(v*v-1)/25, (v*v-16)/(25*v)]
for (xx, _), cc, ss in zip(points, classes, squares):
    assert S.cancel(xx-cc*ss**2) == 0
ratios = sorted({S.Rational(c-a,b-a) for a,b,c in permutations([0,1,-3])})
assert set(ratios) == {S.Rational(-3),S.Rational(-1,3),S.Rational(4),S.Rational(1,4),S.Rational(3,4),S.Rational(4,3)}
assert S.factorint(2*2-1) == {3:1}
assert S.factorint(2) == {2:1}
congruent_ratios = sorted({S.Rational(c-a,b-a) for a,b,c in permutations([0,1,-1])})
assert set(congruent_ratios) == {S.Rational(-1),S.Rational(2),S.Rational(1,2)}
certificate = {
    "status":"PASS",
    "original_pole_root_ratios":list(map(str, ratios)),
    "congruent_number_root_ratios":list(map(str, congruent_ratios)),
    "m":2,
    "m_squared_minus_one_prime_factors":{3:1},
    "admissibility_failures":["A3: no prime greater than14 divides m²−1", "A4: no odd prime divides m"],
    "point_equations_verified":2,
    "squareclass_identities_verified":2,
    "scope":"The cited exact-rank theorem does not apply; no nonexistence assertion for the desired rational witnesses.",
}
out = Path(__file__).with_name("achenjang_woo_scope_v58_certificate.json")
out.write_text(json.dumps(certificate, indent=2)+"\n")
print(json.dumps(certificate, indent=2))
