#!/usr/bin/env python3
"""Compile the BDHMS mixed-integer equation into the joint finite algebra.

The input is a sparse polynomial P(a,z1,...,z_nu), with integer coefficients.
The output specifies a finite free algebra and a selected-character guard by
an exact polynomial DAG.  Applying joint_finite_algebra_encoder.tex gives one
integer polynomial, with 82, 100, or (under abc) 52 rational unknowns.

No universal polynomial is silently supplied.  For arbitrary P the result
represents its natural-number solution set, under the retained integer-
predicate source premises.  The included natural-square fixture is NOT a
universal polynomial and is not an undecidability certificate.

Input JSON: {"unknowns": nu, "terms": [
 {"coefficient": c, "exponents": [i_a,i_z1,...,i_znu]}, ...]}.
Exponents are nonnegative integers.  The external parameter a is not a
quantified unknown.  --instance specializes it to a nonnegative integer.
No third-party package is needed by this compiler.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import math
from pathlib import Path

from build_joint_few_variable import Dag


ROOT = Path(__file__).resolve().parents[2]
ROUTES = ("general25", "explicit27", "abc11")
SOURCE_ROLES = ("f", "g", "h", "k", "l", "w", "x", "y", "n")


class PolynomialDag(Dag):
    """Tiny exact integer-polynomial DAG, with only elementary simplification."""

    def __init__(self):
        super().__init__()
        self.zero = self.node("int", 0)
        self.one = self.node("int", 1)

    def integer(self, value):
        return self.node("int", int(value))

    def add(self, *items):
        out = self.zero
        for item in items:
            if item == self.zero:
                continue
            if out == self.zero:
                out = item
            elif self.nodes[out][0] == self.nodes[item][0] == "int":
                out = self.integer(self.nodes[out][1] + self.nodes[item][1])
            else:
                out = self.node("add", out, item)
        return out

    def neg(self, item):
        if self.nodes[item][0] == "int":
            return self.integer(-self.nodes[item][1])
        return self.node("neg", item)

    def sub(self, left, right):
        return self.add(left, self.neg(right))

    def mul(self, *items):
        out = self.one
        for item in items:
            if item == self.zero:
                return self.zero
            if item == self.one:
                continue
            if out == self.one:
                out = item
            elif self.nodes[out][0] == self.nodes[item][0] == "int":
                out = self.integer(self.nodes[out][1] * self.nodes[item][1])
            else:
                out = self.node("mul", out, item)
        return out

    def power(self, item, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        if exponent == 0:
            return self.one
        if exponent == 1 or item in (self.zero, self.one):
            return item
        # Do not materialize enormous constant powers such as beta^(9^59).
        return self.node("pow", item, exponent)

    def scale(self, value, item):
        return self.mul(self.integer(value), item)


def canonical_sparse(document):
    """Combine repeated terms and validate the public sparse-input format."""
    nu = document["unknowns"]
    assert isinstance(nu, int) and not isinstance(nu, bool) and nu >= 0
    terms = {}
    for term in document["terms"]:
        coefficient = term["coefficient"]
        exponents = tuple(term["exponents"])
        assert isinstance(coefficient, int) and not isinstance(coefficient, bool)
        assert len(exponents) == nu + 1
        assert all(isinstance(e, int) and not isinstance(e, bool) and e >= 0 for e in exponents)
        terms[exponents] = terms.get(exponents, 0) + coefficient
    terms = {e: c for e, c in terms.items() if c}
    return nu, terms


def suitable_polynomial(nu, terms):
    """Sparse exact coefficients of P^2+(z_(nu+1)-1)^2."""
    result = {}
    for exponents1, coefficient1 in terms.items():
        for exponents2, coefficient2 in terms.items():
            key = tuple(a+b for a, b in zip(exponents1, exponents2)) + (0,)
            result[key] = result.get(key, 0) + coefficient1*coefficient2
    zero = (0,)*(nu+1)
    for exponent, coefficient in ((2, 1), (1, -2), (0, 1)):
        key = zero+(exponent,)
        result[key] = result.get(key, 0) + coefficient
    result = {e: c for e, c in result.items() if c}
    assert result[(0,)*(nu+2)] > 0
    return result


def geometric_sum(dag, base, count):
    """Return sum(base^j, 0<=j<count) using O(log count) DAG nodes."""
    assert isinstance(count, int) and count >= 0

    def pair(length):
        if length == 0:
            return dag.one, dag.zero
        if length == 1:
            return base, dag.one
        power, total = pair(length//2)
        square = dag.power(power, 2)
        doubled = dag.mul(total, dag.add(dag.one, power))
        if length % 2:
            return dag.mul(square, base), dag.add(doubled, square)
        return square, doubled

    return pair(count)[1]


def polynomial_add(dag, left, right):
    length = max(len(left), len(right))
    result = [dag.add(left[j] if j < len(left) else dag.zero,
                      right[j] if j < len(right) else dag.zero)
              for j in range(length)]
    while len(result) > 1 and result[-1] == dag.zero:
        result.pop()
    return result


def polynomial_scale(dag, coefficients, scalar):
    return [dag.mul(scalar, coefficient) for coefficient in coefficients]


def polynomial_multiply(dag, left, right):
    result = [dag.zero]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i+j] = dag.add(result[i+j], dag.mul(a, b))
    while len(result) > 1 and result[-1] == dag.zero:
        result.pop()
    return result


def monic_norm_coefficients(dag, S, T, R, A1, A2, A3):
    """Nine coefficient nodes, in ascending powers of the formal variable m."""
    kappa = dag.mul(dag.power(S, 2), dag.sub(dag.scale(2, R), dag.one))
    Z = dag.add(dag.one, *(dag.power(a, 2) for a in (A1, A2, A3)))
    shift = dag.sub(dag.power(T, 2),
                    dag.mul(kappa, dag.add(dag.power(T, 2), dag.power(Z, 3))))
    a = dag.mul(dag.power(kappa, 2), A1)
    b = dag.mul(dag.power(kappa, 2), dag.power(Z, 2), A2)
    c = dag.mul(dag.power(kappa, 2), dag.power(Z, 4), A3)
    z = [shift, dag.one]
    z2 = polynomial_multiply(dag, z, z)
    w = polynomial_add(dag, z2, [dag.sub(dag.sub(c, a), b)])
    w2 = polynomial_multiply(dag, w, w)
    middle = polynomial_add(dag, w2, polynomial_scale(dag, z2, dag.scale(4, c)))
    middle = polynomial_add(dag, middle, [dag.scale(-4, dag.mul(a, b))])
    first = polynomial_multiply(dag, middle, middle)
    second = polynomial_scale(dag, polynomial_multiply(dag, z2, w2), dag.scale(-16, c))
    coefficients = polynomial_add(dag, first, second)
    assert len(coefficients) == 9 and coefficients[-1] == dag.one
    return coefficients, {"kappa": kappa, "Z0": Z, "shift": shift,
                          "radicand1": a, "radicand2": b, "radicand3": c}


def source_bridge(dag, sparse, a, inputs):
    """Definitions 2.1, 4.1 and 5.3 of BDHMS, without expanded large powers."""
    nu, terms = canonical_sparse(sparse)
    suitable = suitable_polynomial(nu, terms)
    v = nu+1
    delta = max(map(sum, suitable))
    mass = sum(map(abs, suitable.values()))
    beta = 1
    threshold = 2*math.factorial(delta)*mass*(v+2)**delta
    while beta <= threshold:
        beta *= 4
    assert beta % 4 == 0
    positions = [(delta+1)**j for j in range(v+2)]
    alpha = delta*positions[v]+1
    f, g, h, k, l, w, x, y = [inputs[name] for name in SOURCE_ROLES[:-1]]
    b = dag.add(dag.one, dag.scale(3, dag.mul(dag.add(dag.scale(2, a), dag.one), f)))
    B = dag.mul(dag.integer(beta), dag.power(b, delta))
    gamma = dag.power(dag.integer(beta), positions[v])
    mu = dag.mul(gamma, dag.power(b, alpha))
    mask = dag.sub(
        dag.mul(dag.sub(B, dag.one), geometric_sum(dag, B, positions[v]+1)),
        dag.mul(dag.sub(b, dag.one),
                dag.add(*(dag.power(B, positions[j]) for j in range(1, v+1)))))
    coefficient_terms = []
    for exponents, coefficient in sorted(suitable.items()):
        degree = sum(exponents)
        exponent = positions[v+1]-sum(e*positions[j] for j, e in enumerate(exponents))
        assert exponent >= 0
        multiplier = coefficient*math.factorial(delta-degree)
        for e in exponents:
            multiplier *= math.factorial(e)
        coefficient_terms.append(dag.scale(multiplier, dag.power(B, exponent)))
    encoded = dag.add(*coefficient_terms)
    c = dag.add(dag.one, dag.mul(a, B), g)
    half_B = dag.mul(dag.integer(beta//2), dag.power(b, delta))
    K0 = dag.add(dag.mul(dag.power(c, delta), encoded),
                 dag.mul(half_B, geometric_sum(dag, B, (2*delta+1)*positions[v]+1)))
    N0 = dag.power(B, positions[v]+1)
    N1 = dag.scale(4, dag.power(B, (2*delta+1)*positions[v]+1))
    N = dag.mul(N0, N1)
    S0 = dag.add(g, dag.scale(2, dag.mul(K0, N0)))
    T0 = dag.add(mask, dag.mul(dag.sub(B, dag.integer(2)), dag.power(B, positions[v+1]), N0))
    R0 = dag.add(dag.mul(dag.add(S0, T0, dag.one), N), T0, dag.one)
    X = dag.mul(dag.sub(N, dag.one), R0)
    Y = dag.power(N, 2)
    U = dag.scale(2, dag.mul(l, X, Y))
    V = dag.scale(4, dag.mul(g, w, Y))
    A = dag.mul(U, dag.add(V, dag.one))
    B1 = dag.add(dag.scale(2, X), dag.one)
    C = dag.add(B1, dag.mul(dag.sub(A, dag.integer(2)), h))
    D = dag.add(dag.mul(dag.sub(dag.power(A, 2), dag.integer(4)), dag.power(C, 2)), dag.integer(4))
    E = dag.mul(dag.power(C, 2), D, x)
    F = dag.add(dag.scale(4, dag.mul(dag.sub(dag.power(A, 2), dag.integer(4)), dag.power(E, 2))), dag.one)
    G = dag.sub(dag.add(dag.one, dag.mul(C, D, F)),
                dag.scale(2, dag.mul(dag.add(A, dag.integer(2)),
                                     dag.power(dag.sub(A, dag.integer(2)), 2), dag.power(E, 2))))
    H = dag.add(C, dag.mul(B1, F), dag.mul(dag.sub(dag.scale(2, y), dag.one), C, F))
    I = dag.add(dag.mul(dag.sub(dag.power(G, 2), dag.one), dag.power(H, 2)), dag.one)
    J = dag.add(X, dag.one, dag.mul(k, dag.sub(dag.mul(dag.power(U, 2), V), dag.integer(2))))
    A1 = b
    A2 = dag.mul(D, F, I)
    A3 = dag.add(dag.mul(dag.sub(dag.mul(dag.power(U, 4), dag.power(V, 2)), dag.integer(4)), dag.power(J, 2)), dag.integer(4))
    S = dag.sub(dag.scale(2, A), dag.integer(5))
    T = dag.sub(dag.scale(3, dag.mul(b, w, C)),
                dag.scale(2, dag.sub(dag.mul(dag.power(b, 2), dag.power(w, 2)), dag.one)))
    R = dag.mul(dag.power(f, 2), dag.power(l, 2), dag.power(x, 2),
                dag.sub(dag.scale(8, dag.mul(dag.power(mu, 3), g, dag.power(J, 2))),
                        dag.mul(dag.power(g, 2),
                                dag.add(dag.scale(32, dag.mul(dag.power(dag.sub(C, dag.mul(l, J, Y)), 2), dag.power(mu, 3))),
                                        dag.mul(dag.power(g, 2), dag.power(J, 2))))))
    coefficients, norm_data = monic_norm_coefficients(dag, S, T, R, A1, A2, A3)
    bridge = {name: value for name, value in locals().copy().items()
              if name in ("a", "b", "B", "gamma", "mu", "mask", "encoded", "c", "K0", "N0", "N1", "N", "S0", "T0", "R0", "X", "Y", "U", "V", "A", "B1", "C", "D", "E", "F", "G", "H", "I", "J", "A1", "A2", "A3", "S", "T", "R")}
    return {"nodes": bridge, "monic_coefficients_ascending": coefficients,
            "norm_nodes": norm_data, "coding_constants": {
                "nu": nu, "v": v, "delta": delta, "coefficient_mass": mass,
                "beta": beta, "beta_threshold": threshold, "positions": positions, "alpha": alpha},
            "suitable_sparse_polynomial": [
                {"exponents": list(e), "coefficient": c} for e, c in sorted(suitable.items())]}


def original_input_degrees(parent, input_variable):
    degrees = []
    for op, *args in parent["coefficient_dag"]:
        if op == "variable":
            degree = int(args[0] == input_variable)
        elif op in ("int", "parameter"):
            degree = 0
        elif op == "add":
            degree = max((degrees[j] for j in args), default=0)
        elif op == "neg":
            degree = degrees[args[0]]
        elif op == "mul":
            degree = sum(degrees[j] for j in args)
        elif op == "pow":
            degree = degrees[args[0]]*args[1]
        else:
            raise ValueError(op)
        degrees.append(degree)
    return degrees


def build_document(repo, route, sparse, instance=None):
    assert route in ROUTES
    if instance is not None:
        assert isinstance(instance, int) and instance >= 0
    folder = repo/"undecidability/common_numerator_sources"/route
    raw = gzip.decompress((folder/"common_source.json.gz").read_bytes())
    parent = json.loads(raw)
    source_hash = hashlib.sha256(raw).hexdigest()
    assert source_hash == json.loads((folder/"certificate.json").read_text())["joint_source_sha256"]
    inputs = sorted((v for v in parent["variables"] if v["category"] == "retained.input"),
                    key=lambda v: int(v["name"].split(".")[0][5:]))
    assert len(inputs) == 9
    last_input = inputs[-1]["index"]
    variables, vmap = [], [None]*len(parent["variables"])

    def variable(name, category):
        index = len(variables)
        variables.append({"index": index, "name": name, "category": category})
        return index

    for old in parent["variables"][:parent["retained_base_count"]]:
        if old["index"] != last_input:
            vmap[old["index"]] = variable(old["name"], old["category"])
    s_index = variable("wrapper.s", "retained.wrapper")
    t_index = variable("wrapper.t", "retained.wrapper")
    retained = len(variables)
    m_index = variable("wrapper.m", "finite.wrapper")
    xi_index = variable("wrapper.xi", "finite.wrapper")
    for old in parent["variables"][parent["retained_base_count"]:]:
        name = old["name"]+(".scaled_by_S" if old["category"] == "finite.pole" else "")
        vmap[old["index"]] = variable(name, old["category"])
    dag = PolynomialDag()
    input_nodes = {role: dag.node("variable", vmap[old["index"]])
                   for role, old in zip(SOURCE_ROLES[:-1], inputs[:-1])}
    parameter_a = (dag.node("parameter", "source_parameter_a") if instance is None else dag.integer(instance))
    bridge = source_bridge(dag, sparse, parameter_a, input_nodes)
    S = bridge["nodes"]["S"]
    m, xi = dag.node("variable", m_index), dag.node("variable", xi_index)
    s, t = dag.node("variable", s_index), dag.node("variable", t_index)
    xi_constant = dag.sub(dag.mul(dag.power(S, 2), dag.add(dag.power(s, 2), dag.power(t, 2))), m)
    finite = [
        {"name": "wrapper.m", "kind": "monic_extension", "degree": 8, "monic": True,
         "coefficient_nodes_ascending": bridge["monic_coefficients_ascending"][:-1],
         "variable": m_index, "generator_node": m},
        {"name": "wrapper.xi", "kind": "monic_extension", "degree": 2, "monic": True,
         "coefficient_nodes_ascending": [xi_constant, S],
         "variable": xi_index, "generator_node": xi}]
    n_degrees = original_input_degrees(parent, last_input)
    poles = [b for b in parent["finite_blocks"] if b["kind"] == "pole"]
    pole_degrees = {b["variable"]: n_degrees[b["coefficient_nodes_ascending"][0]] for b in poles}
    # (new numerator node, exponent e) means S^e times the old expression
    # after n=m/S^2 and q_old=q_new/S^(degree_n(c)).
    node_map = []

    def lift(node, exponent):
        if exponent == 0:
            return node
        return dag.node("mul", node, dag.node("pow", S, exponent))

    for op, *args in parent["coefficient_dag"]:
        if op == "variable":
            if args[0] == last_input:
                new, exponent = m, 2
            else:
                new = dag.node("variable", vmap[args[0]])
                exponent = pole_degrees.get(args[0], 0)
        elif op in ("int", "parameter"):
            new, exponent = dag.node(op, *args), 0
        elif op == "add":
            exponent = max(node_map[j][1] for j in args)
            new = dag.node("add", *(lift(node_map[j][0], exponent-node_map[j][1]) for j in args))
        elif op == "neg":
            new = dag.node("neg", node_map[args[0]][0])
            exponent = node_map[args[0]][1]
        elif op == "mul":
            new = dag.node("mul", *(node_map[j][0] for j in args))
            exponent = sum(node_map[j][1] for j in args)
        elif op == "pow":
            new = dag.node("pow", node_map[args[0]][0], args[1])
            exponent = node_map[args[0]][1]*args[1]
        else:
            raise ValueError(op)
        node_map.append((new, exponent))

    def rational(value):
        numerator, en = node_map[value["numerator"]]
        denominator, ed = node_map[value["denominator"]]
        return {"numerator": lift(numerator, max(0, ed-en)),
                "denominator": lift(denominator, max(0, en-ed))}

    for old in parent["finite_blocks"]:
        b = copy.deepcopy(old)
        if b["kind"] == "point_block":
            for key in ("A", "B"):
                assert node_map[b[key]["numerator"]][1] == node_map[b[key]["denominator"]][1] == 0
                b[key] = rational(old[key])
            assert all(node_map[j][1] == 0 for j in b["variable_nodes"])
            b["variable_nodes"] = [node_map[j][0] for j in b["variable_nodes"]]
        elif b["kind"] == "pole":
            c, linear = b["coefficient_nodes_ascending"]
            exponent = pole_degrees[b["variable"]]
            assert parent["coefficient_dag"][linear] == ["int", 0]
            assert node_map[c][1] == 2*exponent
            b["name"] += ".scaled_by_S"
            b["coefficient_nodes_ascending"] = [node_map[c][0], dag.zero]
            b["generator_node"] = node_map[b["generator_node"]][0]
            b["variable"] = vmap[b["variable"]]
            b["original_root"] = rational(old["original_root"])
            b["original_square_input"] = rational(old["original_square_input"])
            b["rescaling_S_exponent"] = exponent
        else:
            raise AssertionError(b["kind"])
        finite.append(b)
    guards = sorted({S, *(node_map[j][0] for j in parent["guard_numerators"])})
    separating = [xi]
    for block in finite[2:]:
        if block["kind"] == "point_block":
            separating.extend(block["variable_nodes"][:2])  # W=U^2/2-A.
        else:
            separating.append(block["generator_node"])
    nu, sparse_terms = canonical_sparse(sparse)
    source_description = {"unknowns": nu, "terms": [
        {"coefficient": c, "exponents": list(e)} for e, c in sorted(sparse_terms.items())]}
    for key in ("fixture_note", "description"):
        if key in sparse:
            source_description[key] = sparse[key]
    expected = {"general25": 82, "explicit27": 100, "abc11": 52}[route]
    assert retained+1 == expected
    old_rank_exp = parent["summary"]["finite_algebra_rank_exponent_base2"]
    summary = {
        "route": route, "rational_unknowns": retained+1,
        "ordinary_coordinates_before_encoder": retained,
        "integer_predicates_retained": 9,
        "finite_algebra_rank_exponent_base2": old_rank_exp+4,
        "finite_algebra_rank": str(1 << (old_rank_exp+4)),
        "guarded_separator_count": len(separating)+1,
        "coefficient_nodes": len(dag.nodes), "guard_nodes": len(guards),
        "source_common_numerator_sha256": source_hash,
        "ordinary_rational_abc_required": route == "abc11",
        "retained_source_arithmetic_premises": True,
        "source_family_parameter": parent["summary"]["source_family_parameter"],
        "input_polynomial_claimed_universal": False,
        "source_parameter_a": "formal external parameter" if instance is None else instance,
        "scope": "Exact coefficient recipe representing the supplied P over natural numbers under the retained source premises; universality of P is not asserted.",
    }
    document = {
        "schema": "finite-wrapper-source/v1", "summary": summary,
        "input_sparse_polynomial": source_description,
        "variables": variables, "retained_base_count": retained,
        "coefficient_dag": dag.nodes, "finite_blocks": finite,
        "guard_numerators": guards, "separating_generator_nodes": separating,
        "point_block_multiplication": parent["point_block_multiplication"],
        "encoder": "Apply joint_finite_algebra_encoder.tex using the displayed finite multiplication algebra, product guard, and separating generators; monic blocks have their companion multiplication tables.",
        "source_bridge": bridge, "source_input_role_nodes": input_nodes,
        "wrapper": {"S_node": S, "m_node": m, "xi_node": xi,
                    "s_node": s, "t_node": t,
                    "recovered_n": "m/S^2", "recovered_u": "xi/S",
                    "separating_generator_rule": "xi alone generates m because m=xi^2+S*xi+S^2*(s^2+t^2)."},
        "parent_variable_map": vmap,
        "parent_last_input_variable": last_input,
        "parent_coefficient_homogenization_map": [list(pair) for pair in node_map],
        "parent_pole_S_exponents": {str(i): e for i, e in pole_degrees.items()},
        "parent_source": str((folder/"common_source.json.gz").relative_to(repo)),
    }
    output = (json.dumps(document, separators=(",", ":"))+"\n").encode()
    certificate = copy.deepcopy(summary)
    certificate["finite_wrapper_source_sha256"] = hashlib.sha256(output).hexdigest()
    return output, certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--route", choices=ROUTES, default="explicit27")
    parser.add_argument("--instance", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw, certificate = build_document(args.repo, args.route, json.loads(args.input.read_text()), args.instance)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/"finite_wrapper_source.json.gz").write_bytes(gzip.compress(raw, mtime=0))
    (args.output/"certificate.json").write_text(json.dumps(certificate, indent=2)+"\n")
    print(json.dumps(certificate, indent=2))


if __name__ == "__main__":
    main()
