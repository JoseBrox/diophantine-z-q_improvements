#!/usr/bin/env python3
"""Independently compose inverse198 -> published195 and audit physical consumers.

Uses the published transformation data, but imports no producer/checker code.
No optimization or feasibility search is performed.
"""
import argparse
import hashlib
import json
from pathlib import Path

import sympy as s


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    hashes = {}
    def read(path):
        raw = (args.repo / path).read_bytes()
        hashes[path] = hashlib.sha256(raw).hexdigest()
        return json.loads(raw)
    parent_path = "sources/h10_quartic198/circuits/inverse198/quadratic.json"
    p38 = "computation/quartic/laurent_recovery_v38/"
    p40 = "computation/quartic/primitive_basis196_v40/"
    p45 = "computation/quartic/affine_laurent195_v45/"
    parent = read(parent_path)
    la38 = read(p38 + "family196/certificate.json")
    balance = read(p38 + "family196/balancing.json")
    balanced = read(p38 + "family196/balanced-quadratic.json")
    paired = read("computation/quartic/paired_redundancy196_v40/balanced-quadratic.json")
    primitive = read(p40 + "transform.json")
    primitive_table = read(p40 + "quadratic.json")
    tr = read(p45 + "transformation.json")
    final = read(p45 + "quadratic-family.json")
    assert hashes[parent_path] == la38["source_sha256"]
    assert hashes[primitive["source"]] == primitive["source_sha256"]
    assert hashes[tr["source"]] == tr["source_sha256"]
    assert balanced["coordinates"] == paired["coordinates"] == primitive_table["coordinates"]

    C, R, u, v, rho = s.symbols("C R u v rho", nonzero=True)
    xs = {i: s.Symbol("x" + str(i)) for i in range(1, 196)}
    # Only the retained unit identities are used here. R is the positive scalar
    # normalizer, whereas C is the fixed coefficient parameter.
    final_units = {77: u, 78: 1/u, 90: v, 91: 1/v,
                   92: 1/(u*v**2), 112: R**2*u/C, 113: R*u/C}
    final_value = {i: final_units.get(i, x) for i, x in xs.items()}
    la45 = tr["laurent"]
    final_parameter = tr["parameter_scaling"]["weights"]
    after45 = {}
    for item in primitive_table["coordinates"]:
        i = item["id"]
        if str(i) in la45["powers"]:
            after45[i] = u ** (-la45["powers"][str(i)][0])
        else:
            j = la45["old_to_new"][str(i)]
            after45[i] = (u ** (-la45["weights"].get(str(i), [0])[0])
                          * C ** final_parameter.get(str(j), 0) * final_value[j])
            after45[i] *= s.Rational(la45["constants"].get(str(i), "1"))

    pre_affine = {}
    for i in after45:
        terms = tr["affine_substitutions"].get(str(i))
        pre_affine[i] = after45[i] if terms is None else s.expand(sum(
            s.Rational(term["coefficient"]) * C ** term["parameterPower"]
            * s.prod(after45[j] for j in term["monomial"]) for term in terms))
    unbalanced = {
        i: C ** balance["weights"].get(str(i), 0)
        * s.Rational(primitive["coordinate_scaling"].get(str(i), "1")) * expr
        for i, expr in pre_affine.items()
    }
    # v38 unit basis is (R,w0,w1), with w0=u^-1 and w1=(uv)^-1.
    units38 = (R, 1/u, 1/(u*v))
    original = {}
    records = []
    for item in parent["coordinates"]:
        old = item["id"]
        constant = s.Rational(la38["constants"].get(str(old), "1"))
        if str(old) in la38["powers"]:
            expression = constant * s.prod(base ** exponent for base, exponent
                                           in zip(units38, la38["powers"][str(old)]))
            if str(old) in la38["old_to_new"]:
                i = la38["old_to_new"][str(old)]
                assert s.cancel(expression - constant * unbalanced[i]) == 0
        else:
            i = la38["old_to_new"][str(old)]
            expression = constant * unbalanced[i] * s.prod(base ** exponent for base, exponent
                         in zip(units38, la38["weights"].get(str(old), [0, 0, 0])))
        original[old] = s.factor(expression)
        records.append({"source198": old, "name": item["name"], "in_final_units": str(original[old])})
    assert original[77] == u and original[92] == u*v
    assert original[93] == 1/(u*v) and original[94] == 1/(u**2*v**2)

    def pair(index, imag_factor=1):
        return original[index] + rho * imag_factor * original[index + 1]
    physical_tests = {
        "D_H_squared": pair(64, 2), "B0_squared": pair(19, 2),
        "A2_squared": pair(54, 2), "B2_squared": pair(23, 2),
        "C2_squared": pair(66, 2), "C3_squared": pair(68, 2),
        "C4_squared": pair(70, 2),
        "G_squared": original[72] - 2*original[50] + 1 + 4*rho*(original[73] - original[51]),
        "C1_fourth": pair(117), "I_fourth": pair(119),
    }
    expected_tests = {
        "D_H_squared": (xs[64] + 2*rho*xs[65])/u,
        "B0_squared": (xs[19] + 2*rho*xs[20])/u,
        "A2_squared": C*(xs[54] + 2*rho*xs[55])/u,
        "B2_squared": (xs[23] + 2*rho*xs[24])/u,
        "C2_squared": C*(xs[66] + 2*rho*xs[67])/u**3,
        "C3_squared": C*(xs[68] + 2*rho*xs[69])/u**3,
        "C4_squared": (xs[70] + 2*rho*xs[71])/u**3,
        "G_squared": C*(xs[72] + 4*rho*xs[73])/u**3,
        "C1_fourth": C*(xs[114] + rho*xs[115])/u,
        "I_fourth": (xs[116] + C*rho*xs[117])/u**3,
    }
    assert all(s.cancel(physical_tests[name] - value) == 0 for name, value in expected_tests.items())

    field_maps = {}
    factor_parameter_powers = [1, 1, 1, 0, -1]
    product_parameter_powers = [3, 4, 3]
    for detector in range(2):
        factor_parent = 121 + 16*detector
        factor_final = 118 + 16*detector
        unit = u*v**(2*detector)
        for k in range(5):
            physical = pair(factor_parent + 2*k) / (R if detector else 1)
            expected = C**factor_parameter_powers[k]*unit*(xs[factor_final+2*k]+rho*xs[factor_final+2*k+1])
            assert s.cancel(physical-expected) == 0
            field_maps[f"Phi_{detector}_{k}"] = str(s.factor(expected))
        for k in range(3):
            physical = pair(131+16*detector+2*k)
            if detector and k >= 1:
                physical *= R
            out = 128+16*detector+2*k
            expected = C**product_parameter_powers[k]*unit*(xs[out]+rho*xs[out+1])
            assert s.cancel(physical-expected) == 0
            field_maps[f"partial_product_{detector}_{k+2}"] = str(s.factor(expected))
        actual_index, final_actual = (81,79) if detector == 0 else (96,93)
        expected = C*unit*(xs[final_actual]+rho*xs[final_actual+1])
        assert s.cancel(pair(actual_index)-expected) == 0
        field_maps[f"W_{detector}"] = str(expected)
        assert s.cancel(original[actual_index+2] - unit*xs[final_actual+2]) == 0
        assert s.cancel(original[actual_index+3] - unit*xs[final_actual+3]) == 0
        field_maps[f"inverse_trace_{detector}"] = str(unit*xs[final_actual+2])
        field_maps[f"pole_B_{detector}"] = str(unit*xs[final_actual+3])

    # Verify the complete literal source consumer equations after composition,
    # up to a nonzero rational Laurent monomial in C,R,u,v. This checks all
    # product/trace rows and the fixed C rescalings, not merely unit weights.
    def parse(row, values, parameter):
        return s.expand(sum(s.Rational(term["coefficient"])*parameter**term["parameterPower"]
                            *s.prod(values[i] for i in term["monomial"]) for term in row["terms"]))
    final_rows = {row["name"]: row for row in final["residuals"]}
    consumer_checks = []
    for row in parent["residuals"]:
        name = row["name"]
        selected = (name.startswith("amplified.det") or name.startswith("residue.det")
                    or name.startswith("detector0.") or name.startswith("detector1.")
                    or name.startswith("balanced.detector")
                    or name.startswith("testSquare.") or name.startswith("v27.testSquare.")
                    or name.startswith("amplified.C1.") or name.startswith("residue.I."))
        if not selected or name not in final_rows:
            continue
        # The primitive v40 basis swaps these two rows; use their actual names.
        target_name = name
        if name == "testSquare.40.0.0.definition": target_name = "testSquare.40.0.1.definition"
        if name == "testSquare.40.0.1.definition": target_name = "testSquare.40.0.0.definition"
        left = parse(row, original, 149*C**2)
        right = parse(final_rows[target_name], final_value, C)
        if left == 0 or right == 0:
            assert left == right == 0
            ratio = s.Integer(1)
        else:
            ratio = s.factor(s.cancel(left/right))
            assert ratio.free_symbols <= {C,R,u,v}, (name, ratio)
            coefficient, remainder = ratio.as_coeff_Mul()
            assert coefficient != 0
            assert remainder == 1 or all(base in {C,R,u,v} and exponent.is_Integer
                       for base, exponent in remainder.as_powers_dict().items()), (name, ratio)
            assert s.cancel(left-ratio*right) == 0
        consumer_checks.append({"source_row":name,"target_row":target_name,"unit_ratio":str(ratio)})

    report = {
        "status":"PASS", "input_sha256":hashes,
        "scope":"Exact source198-to-published195 coordinate composition and literal consumer-row audit; no feasibility search or variable-count claim",
        "unit_basis":{"u":"final x77 = first physical contact","v":"final x90 = second physical contact / first physical contact"},
        "physical_contacts":{"q0":"u","q1":"u*v"},
        "retained_unit_slots":{"77":"u","78":"u^-1","90":"v","91":"v^-1","92":"u^-1*v^-2"},
        "proposed_repurposing":{"new92":"u^-1*v^2","old92":"v^-4*new92","definition":"u*new92=v^2"},
        "physical_tests":{name:str(s.factor(expr)) for name,expr in expected_tests.items()},
        "factor_product_trace_maps":field_maps,
        "factor_parameter_powers":factor_parameter_powers,
        "partial_product_parameter_powers":product_parameter_powers,
        "source_coordinate_maps":records,
        "literal_consumer_rows_checked":len(consumer_checks),
        "consumer_checks":consumer_checks,
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({key:value for key,value in report.items() if key not in
                     ["input_sha256","source_coordinate_maps","consumer_checks"]},indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
