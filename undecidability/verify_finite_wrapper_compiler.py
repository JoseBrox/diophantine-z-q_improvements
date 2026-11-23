#!/usr/bin/env python3
"""Independently replay the executable finite-wrapper coefficient recipe.

Exact checks: sparse P^2+(z-1)^2 coefficients, the coding constants,
every S-homogenization instruction, finite-stage dependencies, source hashes,
monic degrees, guards, ranks, and coordinate counts. Modular evaluations are
additional diagnostics of the bridge recipe and every original DAG node;
they are explicitly not used as proofs of polynomial identity.
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import itertools
import json
import math
import random
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/"undecidability"
sys.path.insert(0, str(BASE/"code"))
from build_finite_wrapper import (PolynomialDag, SOURCE_ROLES, ROUTES,
                                  build_document, geometric_sum, source_bridge)


def evaluate(nodes, variables, parameters, prime):
    values = []
    for op, *args in nodes:
        if op == "int":
            value = args[0]
        elif op == "variable":
            value = variables[args[0]]
        elif op == "parameter":
            value = parameters.get(args[0], args[1] if len(args) > 1 else None)
            assert value is not None, args[0]
        elif op == "add":
            value = sum(values[j] for j in args)
        elif op == "neg":
            value = -values[args[0]]
        elif op == "mul":
            value = math.prod(values[j] for j in args)
        elif op == "pow":
            value = pow(values[args[0]], args[1], prime)
        else:
            raise AssertionError(op)
        values.append(value % prime)
    return values


def independent_sparse(sparse):
    nu = sparse["unknowns"]
    variables = sp.symbols(f"z0:{nu+2}")
    polynomial = sum(term["coefficient"]*sp.prod(v**e for v, e in zip(variables, term["exponents"]))
                     for term in sparse["terms"])
    suitable = sp.Poly(polynomial**2+(variables[-1]-1)**2, *variables)
    terms = {tuple(e): int(c) for e, c in suitable.terms()}
    delta = suitable.total_degree()
    mass = sum(map(abs, terms.values()))
    v = nu+1
    threshold = 2*math.factorial(delta)*mass*(v+2)**delta
    beta = 4
    while beta <= threshold:
        beta *= 4
    assert beta > threshold and beta//4 <= threshold
    positions = [(delta+1)**j for j in range(v+2)]
    return terms, {"nu": nu, "v": v, "delta": delta,
                   "coefficient_mass": mass, "beta": beta,
                   "beta_threshold": threshold, "positions": positions,
                   "alpha": delta*positions[v]+1}


def reference_bridge(sparse, a, inputs, prime):
    """Literal modular evaluation of the three primary-source definitions."""
    terms, data = independent_sparse(sparse)
    v, delta, beta, positions, alpha = [data[key] for key in ("v", "delta", "beta", "positions", "alpha")]
    f, g, h, k, l, w, x, y = [inputs[name] % prime for name in SOURCE_ROLES[:-1]]
    power = lambda value, exponent: pow(value % prime, exponent, prime)
    reduce = lambda value: value % prime

    def series(value, count):
        value %= prime
        if value == 1:
            return count % prime
        return (power(value, count)-1)*pow(value-1, -1, prime) % prime

    b = reduce(1+3*(2*a+1)*f)
    B = reduce(beta*power(b, delta))
    gamma = power(beta, positions[v])
    mu = reduce(gamma*power(b, alpha))
    # The literal mask coefficients supply an independent check for the toy
    # case. For the 58-unknown stress case use the algebraic closed sum.
    if positions[v] < 10000:
        selected = set(positions[1:v+1])
        mask = sum((B-b if j in selected else B-1)*power(B, j)
                   for j in range(positions[v]+1)) % prime
    else:
        mask = reduce((B-1)*series(B, positions[v]+1)
                      -(b-1)*sum(power(B, e) for e in positions[1:v+1]))
    encoded = 0
    for exponents, coefficient in terms.items():
        multiplier = coefficient*math.factorial(delta-sum(exponents))*math.prod(math.factorial(e) for e in exponents)
        encoded += multiplier*power(B, positions[v+1]-sum(e*positions[j] for j, e in enumerate(exponents)))
    encoded %= prime
    c = reduce(1+a*B+g)
    K0 = reduce(power(c, delta)*encoded+(beta//2)*power(b, delta)*series(B, (2*delta+1)*positions[v]+1))
    N0 = power(B, positions[v]+1)
    N1 = reduce(4*power(B, (2*delta+1)*positions[v]+1))
    N = reduce(N0*N1)
    S0 = reduce(g+2*K0*N0)
    T0 = reduce(mask+(B-2)*power(B, positions[v+1])*N0)
    R0 = reduce((S0+T0+1)*N+T0+1)
    X, Y = reduce((N-1)*R0), power(N, 2)
    U, V = reduce(2*l*X*Y), reduce(4*g*w*Y)
    A, B1 = reduce(U*(V+1)), reduce(2*X+1)
    C = reduce(B1+(A-2)*h)
    D = reduce((A*A-4)*C*C+4)
    E = reduce(C*C*D*x)
    F = reduce(4*(A*A-4)*E*E+1)
    G = reduce(1+C*D*F-2*(A+2)*(A-2)**2*E*E)
    H = reduce(C+B1*F+(2*y-1)*C*F)
    I = reduce((G*G-1)*H*H+1)
    J = reduce(X+1+k*(U*U*V-2))
    A1, A2 = b, reduce(D*F*I)
    A3 = reduce((U**4*V*V-4)*J*J+4)
    S = reduce(2*A-5)
    T = reduce(3*b*w*C-2*(b*b*w*w-1))
    R = reduce(f*f*l*l*x*x*(8*mu**3*g*J*J-g*g*(32*(C-l*J*Y)**2*mu**3+g*g*J*J)))
    return {key: value for key, value in locals().copy().items()
            if key in ("a", "b", "B", "gamma", "mu", "mask", "encoded", "c", "K0", "N0", "N1", "N", "S0", "T0", "R0", "X", "Y", "U", "V", "A", "B1", "C", "D", "E", "F", "G", "H", "I", "J", "A1", "A2", "A3", "S", "T", "R")}, data, terms


def multiquadratic_norm(bridge, m, prime):
    """Eight-sign product in F_p[r1,r2,r3]/(ri^2-Ai), including nonsquares."""
    A = [bridge[name] for name in ("A1", "A2", "A3")]
    S, T, R = [bridge[name] for name in ("S", "T", "R")]
    Z = (1+sum(a*a for a in A)) % prime
    kappa = S*S*(2*R-1) % prime
    constant = (m+T*T-kappa*(T*T+pow(Z, 3, prime))) % prime

    def multiply(left, right):
        product = [0]*8
        for i, ai in enumerate(left):
            for j, bj in enumerate(right):
                coefficient = ai*bj
                for bit in range(3):
                    if (i & j) & (1 << bit):
                        coefficient *= A[bit]
                product[i ^ j] += coefficient
        return [coefficient % prime for coefficient in product]

    result = [1]+[0]*7
    for signs in itertools.product((-1, 1), repeat=3):
        factor = [constant]+[0]*7
        for j, sign in enumerate(signs):
            factor[1 << j] = sign*kappa*pow(Z, j, prime) % prime
        result = multiply(result, factor)
    assert result[1:] == [0]*7
    return result[0]


def exact_homogenization_replay(parent, doc):
    """Every step follows one of the displayed, formal ring identities."""
    nodes = doc["coefficient_dag"]
    index = {tuple(node): i for i, node in enumerate(nodes)}
    assert len(index) == len(nodes)
    mapping = doc["parent_coefficient_homogenization_map"]
    vmap = doc["parent_variable_map"]
    nvar = doc["parent_last_input_variable"]
    S, m = doc["wrapper"]["S_node"], doc["wrapper"]["m_node"]
    pole_exponents = {int(v): e for v, e in doc["parent_pole_S_exponents"].items()}

    def find(op, *args):
        return index[(op, *args)]

    def lift(node, exponent):
        return node if exponent == 0 else find("mul", node, find("pow", S, exponent))

    assert len(mapping) == len(parent["coefficient_dag"])
    for j, (op, *args) in enumerate(parent["coefficient_dag"]):
        if op == "variable":
            expected = (m, 2) if args[0] == nvar else (find("variable", vmap[args[0]]), pole_exponents.get(args[0], 0))
        elif op in ("int", "parameter"):
            expected = (find(op, *args), 0)
        elif op == "add":
            exponent = max(mapping[c][1] for c in args)
            expected = (find("add", *(lift(mapping[c][0], exponent-mapping[c][1]) for c in args)), exponent)
        elif op == "neg":
            expected = (find("neg", mapping[args[0]][0]), mapping[args[0]][1])
        elif op == "mul":
            expected = (find("mul", *(mapping[c][0] for c in args)), sum(mapping[c][1] for c in args))
        elif op == "pow":
            expected = (find("pow", mapping[args[0]][0], args[1]), mapping[args[0]][1]*args[1])
        else:
            raise AssertionError(op)
        assert tuple(mapping[j]) == expected, (j, op)
    assert set(doc["guard_numerators"]) == {S, *(mapping[j][0] for j in parent["guard_numerators"])}
    assert vmap[nvar] is None
    assert sum(v is None for v in vmap) == 1
    old_poles = [b for b in parent["finite_blocks"] if b["kind"] == "pole"]
    new_poles = [b for b in doc["finite_blocks"] if b["kind"] == "pole"]
    for old, new in zip(old_poles, new_poles):
        c = old["coefficient_nodes_ascending"][0]
        exponent = pole_exponents[old["variable"]]
        assert mapping[c] == [new["coefficient_nodes_ascending"][0], 2*exponent]
        assert nodes[new["coefficient_nodes_ascending"][1]] == ["int", 0]
        assert new["variable"] == vmap[old["variable"]]
        assert new["rescaling_S_exponent"] == exponent
    return len(mapping)


def exact_tower_dependencies(doc):
    dependencies = []
    nodes = doc["coefficient_dag"]
    for op, *args in nodes:
        if op == "variable":
            mask = 1 << args[0]
        elif op in ("int", "parameter"):
            mask = 0
        elif op in ("pow", "neg"):
            mask = dependencies[args[0]]
        else:
            mask = 0
            for j in args:
                mask |= dependencies[j]
        dependencies.append(mask)
    retained = doc["retained_base_count"]
    available = (1 << retained)-1
    rank = 1
    for block in doc["finite_blocks"]:
        rank *= block["degree"]
        if block["kind"] == "point_block":
            coefficients = [block[key][part] for key in ("A", "B") for part in ("numerator", "denominator")]
            for key in ("A", "B"):
                assert nodes[block[key]["denominator"]] == ["int", 1]
            generators = [nodes[j][1] for j in block["variable_nodes"]]
        else:
            assert block["monic"] is True
            coefficients = block["coefficient_nodes_ascending"]
            assert len(coefficients) == block["degree"]
            generators = [block["variable"]]
        assert all(dependencies[j] & ~available == 0 for j in coefficients)
        for i in generators:
            assert not (available & (1 << i))
            available |= 1 << i
    assert available == (1 << len(doc["variables"]))-1
    assert rank == int(doc["summary"]["finite_algebra_rank"])
    assert len(doc["separating_generator_nodes"])+1 == doc["summary"]["guarded_separator_count"]
    return {"rank": str(rank), "all_stages_monic_or_verified_point_blocks": True,
            "all_coefficients_depend_only_on_preceding_stages": True}


def bridge_diagnostics():
    toy = json.loads((BASE/"fixtures/natural_square_sparse.json").read_text())
    stress_exponents = [0]*59
    stress_exponents[1] = 4
    stress = {"unknowns": 58, "terms": [
        {"coefficient": 1, "exponents": stress_exponents},
        {"coefficient": -1, "exponents": [1]+[0]*58}]}
    fixtures = [toy, {"unknowns": 0, "terms": []},
                {"unknowns": 0, "terms": [{"coefficient": -3, "exponents": [0]}]}, stress]
    rng = random.Random(83010052)
    output = []
    for sparse in fixtures:
        dag = PolynomialDag()
        a = dag.node("variable", 0)
        inputs = {role: dag.node("variable", j+1) for j, role in enumerate(SOURCE_ROLES[:-1])}
        data = source_bridge(dag, sparse, a, inputs)
        terms, constants = independent_sparse(sparse)
        assert data["coding_constants"] == constants
        assert {tuple(t["exponents"]): t["coefficient"] for t in data["suitable_sparse_polynomial"]} == terms
        for trial, prime in enumerate((1000003, 1000000007, 1000000009)):
            values = [0]*9 if trial == 0 else [rng.randrange(prime) for _ in range(9)]
            evaluated = evaluate(dag.nodes, values, {}, prime)
            reference, _, _ = reference_bridge(sparse, values[0], dict(zip(SOURCE_ROLES[:-1], values[1:])), prime)
            for name, node in data["nodes"].items():
                assert evaluated[node] == reference[name] % prime, name
            m = rng.randrange(prime)
            coefficients = [evaluated[j] for j in data["monic_coefficients_ascending"]]
            assert coefficients[-1] == 1
            value = sum(c*pow(m, j, prime) for j, c in enumerate(coefficients)) % prime
            assert value == multiquadratic_norm(reference, m, prime)
        output.append({"input_unknowns": sparse["unknowns"], "coding_degree": constants["delta"],
                       "largest_coding_position": str(constants["positions"][-1]),
                       "coefficient_dag_nodes": len(dag.nodes),
                       "exact_sparse_and_coding_checks": "PASS", "independent_modular_bridge_trials": 3})
    # Check the binary-doubling geometric sum at exceptional base 1 as well.
    for count in (0, 1, 2, 3, 100, 10**20+7):
        dag = PolynomialDag()
        node = geometric_sum(dag, dag.node("variable", 0), count)
        for base in (0, 1, 2, 1000002):
            p = 1000003
            expected = (count % p if base == 1 else (pow(base, count, p)-1)*pow(base-1, -1, p) % p)
            assert evaluate(dag.nodes, [base], {}, p)[node] == expected
    return output


def verify():
    sparse = json.loads((BASE/"fixtures/natural_square_sparse.json").read_text())
    reports = {}
    rng = random.Random(82010052)
    for route in ROUTES:
        raw, receipt = build_document(ROOT, route, sparse)
        doc = json.loads(raw)
        parent_raw = gzip.decompress((ROOT/doc["parent_source"]).read_bytes())
        parent = json.loads(parent_raw)
        assert hashlib.sha256(parent_raw).hexdigest() == receipt["source_common_numerator_sha256"]
        exact_count = exact_homogenization_replay(parent, doc)
        tower = exact_tower_dependencies(doc)
        assert receipt["input_polynomial_claimed_universal"] is False
        for trial, prime in enumerate((1000003, 1000000007, 1000000009)):
            parameters = {"source_parameter_a": 7+trial}
            new_variables = [rng.randrange(prime) for _ in doc["variables"]]
            new_values = evaluate(doc["coefficient_dag"], new_variables, parameters, prime)
            S = new_values[doc["wrapper"]["S_node"]]
            assert S != 0  # These deterministic fixture specializations are safe.
            inverse = pow(S, -1, prime)
            old_variables = []
            for i, v in enumerate(doc["parent_variable_map"]):
                if v is None:
                    value = new_values[doc["wrapper"]["m_node"]]*inverse**2
                else:
                    exponent = doc["parent_pole_S_exponents"].get(str(i), 0)
                    value = new_variables[v]*pow(inverse, exponent, prime)
                old_variables.append(value % prime)
            old_values = evaluate(parent["coefficient_dag"], old_variables, parameters, prime)
            for i, (new_node, exponent) in enumerate(doc["parent_coefficient_homogenization_map"]):
                assert new_values[new_node] == old_values[i]*pow(S, exponent, prime) % prime, (route, i)
        stored_folder = BASE/"finite_wrapper_sources/natural_square"/route
        stored = stored_folder/"finite_wrapper_source.json.gz"
        if stored.exists():
            assert gzip.decompress(stored.read_bytes()) == raw
            assert json.loads((stored_folder/"certificate.json").read_text()) == receipt
        reports[route] = {**receipt, "exact_homogenization_nodes_replayed": exact_count,
                         "exact_tower_dependency_checks": tower,
                         "whole_DAG_modular_diagnostic_trials": 3}
    return {"status": "PASS", "bridge_fixtures": bridge_diagnostics(), "routes": reports,
            "scope": "Exact symbolic coefficient recipes and compositional homogenization replay; modular tests are supplementary diagnostics. The toy input is not universal. Source universality and arithmetic completeness remain the cited mathematical inputs."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = verify()
    output = json.dumps(result, indent=2)+"\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output)
    print(output, end="")
