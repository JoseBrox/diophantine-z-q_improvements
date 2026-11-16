#!/usr/bin/env python3
"""Independent literal-equation and complete coefficient audit of abc74.

No producer code is imported. The eight reference quadrics are bound to the
pinned abc76 source. All other rows are reconstructed from field arithmetic
and the displayed 74-coordinate equations. The checker also verifies the
nonzero-beta coordinate rescaling and the algebra used at both boundaries.
Arithmetic existence and the global height argument remain mathematical
theorems of the companion paper; finite coefficient checks do not prove them.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "computation/quartic/abc76_v44/quadratic-family.json"
SOURCE_HASH = "5f03efc8629210d3da25f7b2fad6428ea4f8f288d806bd32f26a87954bc012e8"
FIXED_HEIGHT = 20828275368498373068800
CONSTANT_TERM = 275933278576697091


def add(*values):
    return tuple(sum(value[i] for value in values) for i in (0, 1))


def neg(value):
    return -value[0], -value[1]


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    return (left[0]*right[0] + 2*left[1]*right[1],
            left[0]*right[1] + left[1]*right[0])


def scale(scalar, value):
    return scalar*value[0], scalar*value[1]


def scalar(value):
    return sp.sympify(value), sp.Integer(0)


def square(value):
    return mul(value, value)


def conjugate(value):
    return value[0], -value[1]


def norm(value):
    return value[0]**2 - 2*value[1]**2


def inverse(value):
    nn = norm(value)
    assert nn != 0
    return tuple(sp.cancel(x/nn) for x in conjugate(value))


def divide(left, right):
    return tuple(sp.cancel(x) for x in mul(left, inverse(right)))


def equal_field(left, right, label):
    assert all(sp.cancel(a-b) == 0 for a, b in zip(left, right)), label


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE/"independent-verification.json")
    args = parser.parse_args()
    files = {name: (HERE/name).read_bytes() for name in
             ("quadratic-family.json", "polynomial-family.json",
              "construction-report.json")}
    original = SOURCE.read_bytes()
    assert sha256(original).hexdigest() == SOURCE_HASH
    parent = json.loads(original)
    qtable = json.loads(files["quadratic-family.json"])
    ptable = json.loads(files["polynomial-family.json"])
    report = json.loads(files["construction-report.json"])
    assert qtable["parentQuadraticSha256"] == SOURCE_HASH
    assert report["parentQuadraticSha256"] == SOURCE_HASH
    assert qtable["variables"] == ptable["variables"] == 74
    assert qtable["inputCoordinate"] == ptable["inputCoordinate"] == 1
    assert qtable["coordinates"] == ptable["coordinates"]
    assert qtable["fixedParameter"] == ptable["fixedParameter"]
    assert qtable["fixedParameter"]["quantified"] is False
    assert [c["id"] for c in qtable["coordinates"]] == list(range(1, 75))
    assert [r["id"] for r in qtable["residuals"]] == list(range(1, 65))

    variables = sp.symbols("x1:75")
    parameter = sp.Symbol("B")
    names = {c["name"]: variables[c["id"]-1]
             for c in qtable["coordinates"]}
    assert len(names) == 74
    parent_names = {c["id"]: c["name"] for c in parent["coordinates"]}
    coordinate_renaming = {
        "height.inputSquare": "height.betaSquare",
        **{f"detector{i}.poleScaledInput": f"detector{i}.poleInput"
           for i in range(2)},
    }
    row_renaming = dict(coordinate_renaming)
    removed = {
        "height.inputFourth",
        "detector0.inverseWeightSquare",
        "detector1.inverseWeightSquare",
    }
    expected_names = [coordinate_renaming.get(c["name"], c["name"])
                      for c in parent["coordinates"]
                      if c["name"] not in removed] + ["height.betaFourth"]
    assert [c["name"] for c in qtable["coordinates"]] == expected_names
    assert set(qtable["deletedCoordinates"]) == removed

    def value(name):
        return names[name]

    def field(name):
        return value(name+".0"), value(name+".1")

    def parse(row, source_ids=False):
        terms = []
        seen = set()
        for term in row["terms"]:
            power = term["parameterPower"]
            monomial = tuple(term["monomial"])
            assert isinstance(power, int) and power >= 0
            assert tuple(sorted(monomial)) == monomial
            assert (power, monomial) not in seen
            seen.add((power, monomial))
            coefficient = sp.Rational(term["coefficient"])
            assert coefficient.q == 1 and coefficient != 0
            item = coefficient * parameter**power
            for index in monomial:
                if source_ids:
                    name = parent_names[index]
                    assert name not in removed
                    item *= value(coordinate_renaming.get(name, name))
                else:
                    assert 1 <= index <= 74
                    item *= variables[index-1]
            terms.append(item)
        assert terms
        return sp.Add(*terms)

    parent_rows = {r["name"]: r for r in parent["residuals"]}
    target = {r["name"]: parse(r) for r in qtable["residuals"]}
    assert len(target) == 64
    desired = {}

    def field_row(name, expression):
        for component in (0, 1):
            desired[f"{name}.{component}"] = sp.expand(expression[component])

    # The only inherited formulas not reconstructed below are the exact
    # primitive reference basis, fixed by the pinned parent source.
    for index in range(1, 9):
        name = f"common.primitive.{index}"
        desired[name] = parse(parent_rows[name], source_ids=True)

    f, h, g, k, slope = (field(name) for name in
                         ("pair.f", "pair.h", "pair.g", "pair.k",
                          "pair.slope"))
    F, G = field("square.pair.f"), field("square.pair.g")
    FH, GH = field("square.common.f"), field("square.common.g")
    S, T0 = field("common.S"), field("common.T")
    L, M = field("ratio.primary"), field("ratio.alternate")
    C2, I2 = field("square.comparison"), field("square.input")
    trace = value("height.trace")
    beta2, beta4 = value("height.betaSquare"), value("height.betaFourth")
    D = (sp.Integer(11), sp.Integer(-6))
    field_row("pair.secant", sub(mul(slope, sub(f, g)), add(h, k)))
    field_row("pair.tangent",
              add(mul(slope, sub(h, k)), scalar(-beta4),
                  mul(D, add(F, mul(f, g), G))))
    field_row("square.pair.f", sub(F, square(f)))
    field_row("square.pair.g", sub(G, square(g)))
    field_row("ratio.primary.raw", add(mul(h, L), mul(f, S)))
    field_row("ratio.alternate.raw", add(mul(k, M), mul(g, T0)))
    field_row("ratio.primary.regular",
              add(mul(sub(scalar(beta4), mul(D, F)), L), mul(h, S)))
    field_row("ratio.alternate.regular",
              add(mul(sub(scalar(beta4), mul(D, G)), M), mul(k, T0)))
    field_row("square.comparison", sub(C2, square(sub(L, conjugate(M)))))
    field_row("square.input", sub(I2, square(sub(L, scalar(1)))))
    desired["height.trace"] = (
        beta2*trace - 2*add(square(slope), mul(D, add(f, g)))[0])
    desired["height.betaSquare"] = 4*beta2-value("input")**2
    desired["height.betaFourth"] = beta4-beta2**2
    desired["detector1.argument"] = (
        value("detector1.argument") - value("slope") - parameter
        - beta4**2 - trace**2)

    for index in range(2):
        prefix = f"detector{index}."
        t = value("slope") if index == 0 else value(prefix+"argument")
        R = value(prefix+"contactSquareShift")
        Z = value(prefix+"contactSumShift")
        w = value(prefix+"inverseWeight")
        eta, b = value(prefix+"trace"), value(prefix+"poleInput")
        A1, A2, Om = (field(prefix+name) for name in
                      ("factor1", "factor2", "product"))
        e, u, p, v, q, p2, q2 = (
            value(prefix+"pole."+name)
            for name in ("e", "u", "p", "v", "q", "pSquare", "qSquare"))
        desired[prefix+"contactSquare"] = R-t**2+2*t
        desired[prefix+"contactSum"] = R*Z+Z-R**2+35*R
        desired[prefix+"inverseContact"] = (R+1)*w-Z**2-24*Z
        field_row(prefix+"factor1",
                  sub(scale(w, A1), add(scalar(w*w), scale(w, C2),
                                       mul(FH, F))))
        field_row(prefix+"factor2",
                  sub(scale(w, A2), add(scalar(w*w), scale(w, I2),
                                       mul(conjugate(GH), conjugate(G)))))
        field_row(prefix+"product", sub(scale(w, Om), mul(A1, A2)))
        desired[prefix+"trace"] = Om[0]**2-2*Om[0]*eta-2*Om[1]**2
        desired[prefix+"poleInput"] = w*b-eta**2
        desired[prefix+"pole.pSquare"] = p2-p**2
        desired[prefix+"pole.first"] = e**2+b*p2-1
        desired[prefix+"pole.factor"] = u*v-e*(1-b)
        desired[prefix+"pole.qSquare"] = q2-q**2
        desired[prefix+"pole.second"] = u**2-v**2-b*q2

    assert set(desired) == set(target) and len(desired) == 64
    signs, primitiveness = {}, {}
    for name, expression in desired.items():
        raw = sp.Poly(sp.expand(expression), parameter, *variables,
                      domain=sp.QQ)
        denominator, cleared = raw.clear_denoms(convert=True)
        content, primitive = cleared.primitive()
        assert denominator != 0 and content != 0
        normalized = primitive.as_expr()
        actual = target[name]
        if sp.expand(actual-normalized) == 0:
            signs[name] = 1
        else:
            assert sp.expand(actual+normalized) == 0, name
            signs[name] = -1
        polynomial = sp.Poly(actual, *variables)
        assert polynomial.total_degree() <= 2
        coefficients = polynomial.coeffs()
        if all(c.is_Integer for c in coefficients):
            assert reduce(gcd, (abs(int(c)) for c in coefficients)) == 1
            primitiveness[name] = "constant gcd 1"
        else:
            assert any(c in (1, -1) for c in coefficients)
            primitiveness[name] = "unit ordinary coefficient"

    retained, changed = [], []
    for name, row in parent_rows.items():
        if name in removed:
            continue
        new_name = row_renaming.get(name, name)
        if new_name in target:
            # Source rows using a removed coordinate are necessarily changed.
            uses_removed = any(parent_names[i] in removed
                               for t in row["terms"] for i in t["monomial"])
            # Both components of the changed tangent field identity
            # are classified together, even though its irrational
            # component happens to retain the same literal coefficients.
            if (not uses_removed and name not in row_renaming
                    and name != "pair.tangent.1"):
                old_expression = parse(row, source_ids=True)
                if sp.expand(old_expression-target[new_name]) == 0:
                    retained.append(name)
                    continue
            changed.append(name)
    assert len(retained) == 36 and len(changed) == 27, {
        "retained": len(retained), "changed": len(changed),
        "extraRetained": sorted(set(retained)-set(report["retainedRows"])),
        "missingRetained": sorted(set(report["retainedRows"])-set(retained)),
    }
    assert set(retained) == set(report["retainedRows"])
    assert set(changed) == set(report["changedRows"])
    assert set(report["removedRows"]) == removed
    assert report["addedRows"] == ["height.betaFourth"]

    # Independent full expansion in a dense symbolic polynomial ring,
    # then comparison of every sparse coefficient with the stored JSON.
    expansion = sp.Poly(sp.expand(sum(q*q for q in target.values())),
                        parameter, *variables)
    expanded = {}
    for powers, coefficient in expansion.terms():
        monomial = tuple(i+1 for i, degree in enumerate(powers[1:])
                         for _ in range(degree))
        expanded[(powers[0], monomial)] = int(coefficient)
    stored = {}
    for term in ptable["terms"]:
        key = term["parameterPower"], tuple(term["monomial"])
        assert key not in stored
        assert tuple(sorted(key[1])) == key[1]
        coefficient = sp.Rational(term["coefficient"])
        assert coefficient.q == 1 and coefficient != 0
        stored[key] = int(coefficient)
    assert expanded == stored
    assert max(len(m) for _, m in stored) == ptable["degree"] == 4
    assert stored[(0, (1, 1, 1, 1))] == 1
    assert {i for _, m in stored for i in m} == set(range(1, 75))
    assert reduce(gcd, stored.values()) == 1

    profiles = defaultdict(dict)
    for (degree, monomial), coefficient in stored.items():
        profiles[monomial][degree] = coefficient
    assert len(profiles) == 1190 and len(stored) == 1192
    assert profiles[()] == {0: CONSTANT_TERM, 2: 1}
    constant_height = max(abs(p[0]) for p in profiles.values()
                          if set(p) == {0})
    assert constant_height == FIXED_HEIGHT
    varying = {m: p for m, p in profiles.items() if any(p)}
    assert len(varying) == 5
    for monomial, profile in profiles.items():
        if set(profile) == {0}:
            assert profile[0] != 0
        elif monomial:
            assert set(profile) <= {0, 1}
            linear, constant = profile[1], profile.get(0, 0)
            assert linear*constant >= 0 and 0 < abs(linear) <= 2
            assert CONSTANT_TERM-abs(constant) >= 1
            # For every B>=1, 2B <= B^2+1; hence this profile is
            # bounded by B^2+CONSTANT_TERM and cannot vanish.
    assert report["variables"] == 74 and report["quadraticRows"] == 64
    assert report["ordinaryMonomialsForEveryPositiveB"] == 1190
    assert report["parameterSeparatedTerms"] == 1192
    assert int(report["constantCoefficient"]) == CONSTANT_TERM
    assert int(report["largestFixedCoefficient"]) == FIXED_HEIGHT

    # Nonzero-beta rescaling: formal field identities, with beta an
    # independent nonzero indeterminate. This does not assert a full
    # equivalence with the old detector or with its old input label.
    bb = sp.Symbol("beta", nonzero=True)
    ff, hh, gg, kk, ss, LL, MM, SS, TT = (
        tuple(sp.symbols(name+"0 "+name+"1"))
        for name in ("f", "h", "g", "k", "s", "L", "M", "S", "T"))
    FF, GG = square(ff), square(gg)
    fp, gp = scale(bb**2, ff), scale(bb**2, gg)
    hp, kp, spoint = scale(bb**3, hh), scale(bb**3, kk), scale(bb, ss)
    Fp, Gp = scale(bb**4, FF), scale(bb**4, GG)
    Lp, Mp = scale(1/bb, LL), scale(1/bb, MM)
    rescalings = []

    def scaling_identity(label, left, right):
        equal_field(left, right, label)
        rescalings.append(label)

    scaling_identity("f square", square(fp), Fp)
    scaling_identity("g square", square(gp), Gp)
    scaling_identity("secant",
        sub(mul(spoint, sub(fp, gp)), add(hp, kp)),
        scale(bb**3, sub(mul(ss, sub(ff, gg)), add(hh, kk))))
    scaling_identity("tangent",
        add(mul(spoint, sub(hp, kp)), scalar(-bb**4),
            mul(D, add(Fp, mul(fp, gp), Gp))),
        scale(bb**4, add(mul(ss, sub(hh, kk)), scalar(-1),
                        mul(D, add(FF, mul(ff, gg), GG)))))
    for label, point_h, point_f, point_F, ratio, reference, old_h, old_f, old_F, old_ratio in (
        ("primary", hp, fp, Fp, Lp, SS, hh, ff, FF, LL),
        ("alternate", kp, gp, Gp, Mp, TT, kk, gg, GG, MM),
    ):
        scaling_identity(label+" raw",
            add(mul(point_h, ratio), mul(point_f, reference)),
            scale(bb**2, add(mul(old_h, old_ratio), mul(old_f, reference))))
        scaling_identity(label+" regular",
            add(mul(sub(scalar(bb**4), mul(D, point_F)), ratio),
                mul(point_h, reference)),
            scale(bb**3, add(mul(sub(scalar(1), mul(D, old_F)), old_ratio),
                            mul(old_h, reference))))
    scaling_identity("comparison square", square(sub(Lp, conjugate(Mp))),
                     scale(bb**-2, square(sub(LL, conjugate(MM)))))
    scaling_identity("input square", square(sub(Lp, scalar(1))),
                     scale(bb**-2, square(sub(LL, scalar(bb)))))
    scaling_identity("trace recovery",
                     add(square(spoint), mul(D, add(fp, gp))),
                     scale(bb**2, add(square(ss), mul(D, add(ff, gg)))))

    # Physical pole formula, including the factor two in the field trace.
    ww, w0, w1 = sp.symbols("w w0 w1", nonzero=True)
    tau = (w0*w0-2*w1*w1)/(2*w0)
    om0, om1, eta = ww*w0, ww*w1, ww*tau
    assert sp.cancel(om0**2-2*om0*eta-2*om1**2) == 0
    assert sp.cancel(ww*(ww*tau**2)-eta**2) == 0

    # At w=0 and beta!=0, the factor and square rows give f=g=F=G=0.
    # These exact ideal identities then force betaFourth^2*S and
    # betaFourth^2*T to vanish. The complete reference chart excludes
    # S=T=0, so w=0 is impossible on that stratum.
    hh0, kk0, ss0, ll0, mm0, sr, tr, c4 = sp.symbols(
        "hh kk ss ll mm sr tr c4")
    secant = hh0+kk0
    tangent = ss0*(hh0-kk0)-c4
    primary_raw = hh0*ll0
    primary_regular = c4*ll0+hh0*sr
    alternate_raw = kk0*mm0
    alternate_regular = c4*mm0+kk0*tr
    certificate_s = (
        4*ss0**2*(hh0*primary_regular-c4*primary_raw)
        - sr*(tangent+ss0*secant)*(2*ss0*hh0+c4))
    certificate_t = (
        4*ss0**2*(kk0*alternate_regular-c4*alternate_raw)
        - tr*(-tangent+ss0*secant)*(2*ss0*kk0-c4))
    assert sp.expand(certificate_s-c4**2*sr) == 0
    assert sp.expand(certificate_t-c4**2*tr) == 0

    # Exact reference H=2P and the X=0 degeneration. All 54 non-pole
    # rows vanish for symbolic B and lambda; the two remaining native
    # pole blocks are filled by the companion above-one pole theorem.
    def point_double(point):
        px, py = point
        tangent_slope = divide(sub(scale(3, square(px)), D), scale(2, py))
        nx = sub(square(tangent_slope), scale(2, px))
        ny = sub(mul(tangent_slope, sub(px, nx)), py)
        return tuple(tuple(sp.cancel(v) for v in z) for z in (nx, ny))

    R0 = ((sp.Integer(1), sp.Integer(1)), (sp.Integer(0), sp.Integer(2)))
    P = ((sp.Rational(57, 8), -sp.Rational(7, 2)),
         (-sp.Rational(165, 8), sp.Rational(417, 32)))
    doubled_R0 = point_double(R0)
    equal_field(doubled_R0[0], P[0], "2R0=P abscissa")
    equal_field(doubled_R0[1], P[1], "2R0=P ordinate")
    H = point_double(P)
    reference_values = {
        "common.S": divide(H[1], H[0]),
        "common.T": divide(P[1], P[0]),
        "common.f": inverse(H[0]),
        "square.common.f": square(inverse(H[0])),
        "square.common.g": square(inverse(P[0])),
    }
    zero_map = {
        value("input"): 0, beta2: 0, beta4: 0, trace: 0,
        value("detector1.argument"): value("slope")+parameter,
    }
    for name, component_values in reference_values.items():
        for component, component_value in enumerate(component_values):
            zero_map[value(name+f".{component}")] = component_value
    for name in ("pair.f", "pair.h", "pair.g", "pair.k", "pair.slope",
                 "square.pair.f", "square.pair.g", "square.comparison",
                 "square.input"):
        for component in (0, 1):
            zero_map[value(name+f".{component}")] = 0
    for name in ("ratio.primary", "ratio.alternate"):
        zero_map[value(name+".0")] = 1
        zero_map[value(name+".1")] = 0
    for index in range(2):
        prefix = f"detector{index}."
        t = value("slope")+index*parameter
        rr = t*t-2*t
        zz = (rr*rr-35*rr)/(rr+1)
        weight = (zz*zz+24*zz)/(rr+1)
        zero_map[value(prefix+"contactSquareShift")] = rr
        zero_map[value(prefix+"contactSumShift")] = zz
        zero_map[value(prefix+"inverseWeight")] = weight
        for label in ("factor1", "factor2", "product"):
            zero_map[value(prefix+label+".0")] = weight
            zero_map[value(prefix+label+".1")] = 0
        zero_map[value(prefix+"trace")] = weight/2
        zero_map[value(prefix+"poleInput")] = weight/4
    boundary_rows = []
    for name, expression in target.items():
        if ".pole." not in name:
            assert sp.cancel(expression.xreplace(zero_map)) == 0, name
            boundary_rows.append(name)
    assert len(boundary_rows) == 54

    # Exact contact identity and congruence-class separation certificate.
    t = sp.Symbol("t")
    rr = t*t-2*t
    zz = (rr*rr-35*rr)/(rr+1)
    weight = (zz*zz+24*zz)/(rr+1)
    contact_set = (-5, -2, -1, 0, 2, 3, 4, 7)
    assert sp.cancel((t-1)**6*weight-sp.prod(t-a for a in contact_set)) == 0
    assert all(len({0, (2*c-nu)%4, (-2*nu)%4}) == 3
               for nu in (1, 3) for c in range(4))
    assert Fraction(301, 388)*Fraction(4, 7)*2 == Fraction(602, 679) < 1

    # Input files must remain frozen throughout the independent audit.
    assert original == SOURCE.read_bytes()
    for name, data in files.items():
        assert data == (HERE/name).read_bytes()
    receipt = {
        "status": "PASS_EXACT_ALGEBRA",
        "method": "Independent SymPy field equations, pinned literal reference rows, complete sum-of-squares expansion; no producer import.",
        "arithmeticScope": "The companion paper supplies the retained hypotheses, all-branch extraction, height argument, above-one pole theorem, and half-generator completeness. Finite checks do not prove these arithmetic existence assertions.",
        "sha256": {
            "parentQuadratic": SOURCE_HASH,
            **{name: sha256(data).hexdigest() for name, data in files.items()},
        },
        "variables": 74,
        "quadraticRows": 64,
        "independentlyReconstructedRows": 56,
        "pinnedReferenceRows": 8,
        "retainedSourceRows": len(retained),
        "changedSourceRows": len(changed),
        "removedSourceRows": sorted(removed),
        "addedRows": ["height.betaFourth"],
        "maximumQuadraticDegree": 2,
        "degree": 4,
        "inputFourthPowerCoefficient": 1,
        "integerContentForEveryIntegerB": 1,
        "allRowsPrimitiveForEveryIntegerB": True,
        "ordinaryMonomialsForEveryPositiveB": len(profiles),
        "parameterSeparatedTerms": len(stored),
        "exactHeightForEveryPositiveB":
            f"max({FIXED_HEIGHT}, B^2 + {CONSTANT_TERM})",
        "betaRescalingFieldIdentities": rescalings,
        "zeroInputNonPoleRowsVerified": len(boundary_rows),
        "zeroWeightIdealCertificates": ["betaFourth^2*S", "betaFourth^2*T"],
        "physicalPoleIdentity": "b=w*(Norm(W)/Trace(W))^2",
        "contactPolynomialIdentity": True,
        "valuationClassSeparation": True,
        "heightAbsorption": "602/679 < 1",
        "variableCoefficientProfiles": [
            {"monomial": list(m), "coefficients": p}
            for m, p in sorted(varying.items())],
        "rowSignsRelativeToLiteralEquations": signs,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "status": receipt["status"], "variables": 74, "quadraticRows": 64,
        "ordinaryMonomials": len(profiles), "parameterTerms": len(stored),
        "exactHeight": receipt["exactHeightForEveryPositiveB"],
        "receipt": str(args.output.resolve()),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
