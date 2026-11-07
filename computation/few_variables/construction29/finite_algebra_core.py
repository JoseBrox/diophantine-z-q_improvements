"""Integer expression DAG and exact pruning; inherited implementation.
See provenance.json for the source identity.
"""

def children(node):
    op, *a = node
    if op in ("int", "variable", "parameter", "algebra_generator"):
        return []
    if op in ("neg", "pow"):
        return a[:1]
    if op in ("add", "mul"):
        return a
    raise ValueError(op)


class DAG:
    def __init__(self, nodes=()):
        self.nodes = [list(node) for node in nodes]
        self.cache = {tuple(node): i for i, node in enumerate(self.nodes)}
        self.zero, self.one = self.node("int", 0), self.node("int", 1)

    def node(self, op, *a):
        key = (op, *a)
        if key not in self.cache:
            self.cache[key] = len(self.nodes)
            self.nodes.append(list(key))
        return self.cache[key]

    def add(self, *terms):
        terms = [t for t in terms if t != self.zero]
        return self.zero if not terms else terms[0] if len(terms) == 1 else self.node("add", *terms)

    def mul(self, *terms):
        if self.zero in terms:
            return self.zero
        terms = [t for t in terms if t != self.one]
        return self.one if not terms else terms[0] if len(terms) == 1 else self.node("mul", *terms)

    def pow(self, a, exponent):
        return self.one if exponent == 0 else a if exponent == 1 else self.node("pow", a, exponent)

    def neg(self, a):
        return self.zero if a == self.zero else self.node("neg", a)

    def integer(self, n):
        return self.node("int", n)


def supports(nodes):
    masks = []
    for node in nodes:
        mask = 1 << node[1] if node[0] == "variable" else 0
        for child in children(node):
            mask |= masks[child]
        masks.append(mask)
    return masks


def extract_quadratic(dag, root, variable, source_support):
    cache = {}

    def plus(a, b):
        result = dict(a)
        for degree, coefficient in b.items():
            result[degree] = dag.add(result.get(degree, dag.zero), coefficient)
        return result

    def times(a, b):
        result = {}
        for i, aa in a.items():
            for j, bb in b.items():
                result = plus(result, {i+j: dag.mul(aa, bb)})
        return result

    def expand(index):
        if index in cache:
            return cache[index]
        if not (source_support[index] >> variable & 1):
            result = {0: index}
        else:
            op, *a = dag.nodes[index]
            if op == "variable":
                assert a == [variable]
                result = {1: dag.one}
            elif op == "add":
                result = {}
                for child in a:
                    result = plus(result, expand(child))
            elif op == "mul":
                result = {0: dag.one}
                for child in a:
                    result = times(result, expand(child))
            elif op == "neg":
                result = {k: dag.neg(v) for k, v in expand(a[0]).items()}
            elif op == "pow":
                result = {0: dag.one}
                for _ in range(a[1]):
                    result = times(result, expand(a[0]))
            else:
                raise ValueError(op)
        cache[index] = result
        return result

    coefficients = expand(root)
    assert set(coefficients) == {0, 2}
    return coefficients[2], coefficients[0]


def prune(nodes, roots):
    reached, todo = set(), list(roots)
    while todo:
        index = todo.pop()
        if index in reached:
            continue
        reached.add(index); todo.extend(children(nodes[index]))
    mapping = {old: new for new, old in enumerate(sorted(reached))}
    result = []
    for index in sorted(reached):
        op, *a = nodes[index]
        if op in ("int", "variable", "parameter", "algebra_generator"):
            result.append(nodes[index])
        elif op == "pow":
            result.append([op, mapping[a[0]], a[1]])
        else:
            result.append([op, *(mapping[k] for k in a)])
    return result, mapping

