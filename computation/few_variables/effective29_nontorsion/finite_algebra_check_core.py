"""Independent exact expression audit utilities; see provenance.json."""
from collections import Counter
from functools import lru_cache

def check(condition, message):
    if not condition:
        raise ValueError(message)


def children(node):
    op, *a = node
    if op in ("int", "variable", "parameter", "algebra_generator"):
        return []
    if op in ("pow", "neg"):
        return a[:1]
    if op in ("add", "mul"):
        return a
    raise ValueError("Unknown node operation")


def support_table(nodes, kind="variable"):
    answer = []
    for i, node in enumerate(nodes):
        kids = children(node)
        check(all(type(k) is int and 0 <= k < i for k in kids), "Non-topological DAG")
        mask = 1 << node[1] if node[0] == kind else 0
        for k in kids:
            mask |= answer[k]
        answer.append(mask)
    return answer


def plus(*polys):
    out = Counter()
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] += coefficient
    return {m: c for m, c in out.items() if c}


def times(*polys):
    out = {(): 1}
    for poly in polys:
        result = Counter()
        for m, c in out.items():
            for n, d in poly.items():
                result[tuple(sorted(m+n))] += c*d
        out = {m: c for m, c in result.items() if c}
    return out


def power(poly, exponent):
    out = {(): 1}
    while exponent:
        if exponent & 1:
            out = times(out, poly)
        exponent >>= 1
        if exponent:
            poly = times(poly, poly)
    return out


def expander(nodes, atoms=None, variables=None, parameters=None, generators=None):
    atoms, variables = atoms or {}, variables or {}
    parameters, generators = parameters or {}, generators or {}

    @lru_cache(None)
    def expand(index):
        if index in atoms:
            return {(atoms[index],): 1}
        op, *a = nodes[index]
        if op == "int":
            return {(): a[0]} if a[0] else {}
        if op == "variable":
            check(a[0] in variables, "Unexpected variable in a small formal identity")
            return {(variables[a[0]],): 1}
        if op == "parameter":
            check(a[0] in parameters, "Unexpected parameter in a small formal identity")
            return {(parameters[a[0]],): 1}
        if op == "algebra_generator":
            check(a[0] in generators, "Unexpected algebra generator in a small formal identity")
            return {(generators[a[0]],): 1}
        if op == "neg":
            return {m: -c for m, c in expand(a[0]).items()}
        if op == "add":
            return plus(*(expand(k) for k in a))
        if op == "mul":
            return times(*(expand(k) for k in a))
        if op == "pow":
            check(a[1] < 100, "Escaped the intended formal-identity frontier")
            return power(expand(a[0]), a[1])
        raise ValueError(op)
    return expand


class Interner:
    """Exact expression-tree equality, including only 0/1 normalizations."""
    def __init__(self):
        self.table, self.nodes = {}, []
        self.zero, self.one = self.raw("int", 0), self.raw("int", 1)

    def raw(self, op, *a):
        key = (op, *a)
        if key not in self.table:
            self.table[key] = len(self.nodes); self.nodes.append(key)
        return self.table[key]

    def add(self, *a):
        a = tuple(k for k in a if k != self.zero)
        return self.zero if not a else a[0] if len(a) == 1 else self.raw("add", *a)

    def mul(self, *a):
        if self.zero in a:
            return self.zero
        a = tuple(k for k in a if k != self.one)
        return self.one if not a else a[0] if len(a) == 1 else self.raw("mul", *a)

    def pow(self, a, n):
        return self.one if n == 0 else a if n == 1 else self.raw("pow", a, n)

    def neg(self, a):
        return self.zero if a == self.zero else self.raw("neg", a)

    def read(self, nodes):
        answer = []
        for op, *a in nodes:
            if op in ("int", "variable", "parameter", "algebra_generator"):
                value = self.raw(op, *a)
            elif op == "pow":
                value = self.raw(op, answer[a[0]], a[1])
            else:
                value = self.raw(op, *(answer[k] for k in a))
            answer.append(value)
        return answer

