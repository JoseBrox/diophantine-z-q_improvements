"""Independent mathematical/source checker for reciprocal-log proposals.

This file imports neither the archive builder nor the proposal compiler.
No acceptance of the changed arithmetic theorem follows from a PASS here.
"""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
import gzip
import hashlib
import json
from math import comb, gcd, isfinite
from pathlib import Path
import time

ORIGINAL_BUILDER = 'c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912'
ORIGINAL_MODULES = {
    'q_anchor': 'e4d8f1c9395d254fef83bddefdf304c520af8fee0575926be3aa7189376965cb',
    'q_batch41': '8963245225447a7065b67de902ad27b8820dbeba5562d13756fdf1f71902ae6a',
    'q_compare4': '639574951f42451345b3286a57ca922273567f20a548ee2426939c7a30a07212',
    'q_height_batch': '6682b1069de2edb5fe5ef5ffd5d53ac74652699d8166c509bccad63bf741860a',
    'q_primeparity': 'de1bd279f6ca85b6f4d972c36a4ad079cc9678c47a8672904c168eedbab17478',
    'Z_definition': '75fe909cbd7992c77ec99a2fe18495745362054d20083e4e6a3ff705bb17035e',
}
DEADLINE = float('inf')
MAX_TERMS = 50_000
MAX_DEGREE = 256
MAX_COEFFICIENT_BITS = 32_768
MAX_COORDINATES = 4096


class CheckerResourceError(RuntimeError):
    """An inconclusive resource failure, never a semantic rejection."""


def resource(condition, message):
    if not condition:
        raise CheckerResourceError(message)


def tick():
    resource(time.monotonic() < DEADLINE, 'Checker elapsed-time bound reached')


def load(path):
    tick()
    resource(path.stat().st_size < 20_000_000, 'JSON file size bound reached')
    return json.loads(path.read_bytes())


def file_sha256(path, maximum=50_000_000):
    tick()
    resource(path.stat().st_size <= maximum, 'Hashed file size bound reached')
    digest = hashlib.sha256(); total = 0
    with path.open('rb') as stream:
        while True:
            tick()
            chunk = stream.read(65536)
            if not chunk:
                break
            total += len(chunk)
            resource(total <= maximum, 'Hashed stream size bound reached')
            digest.update(chunk)
    return digest.hexdigest()


def construction_map_bytes(visits):
    return (json.dumps({'instantiations': visits}, sort_keys=True,
                       separators=(',', ':'), ensure_ascii=True)+'\n').encode('ascii')


def v(i):
    return {(i,): Q(1)}


def const(c):
    return {(): bounded_coefficient(c)} if c else {}


def bounded_coefficient(c):
    a = Q(c)
    resource(max(abs(a.numerator).bit_length(), a.denominator.bit_length()) <= MAX_COEFFICIENT_BITS,
             'Expanded coefficient bit bound reached')
    return a


def check_polynomial(p):
    tick()
    resource(len(p) <= MAX_TERMS, 'Polynomial term bound reached')
    for mon, coefficient in p.items():
        resource(len(mon) <= MAX_DEGREE, 'Expanded monomial degree bound reached')
        bounded_coefficient(coefficient)


def coefficient_product(a, b):
    a = bounded_coefficient(a); b = bounded_coefficient(b)
    # Cancellation may make the actual product smaller. This conservative
    # preflight prevents building an oversized numerator or denominator.
    resource(abs(a.numerator).bit_length()+abs(b.numerator).bit_length() <= MAX_COEFFICIENT_BITS+1,
             'Coefficient product numerator bound reached')
    resource(a.denominator.bit_length()+b.denominator.bit_length() <= MAX_COEFFICIENT_BITS+1,
             'Coefficient product denominator bound reached')
    return bounded_coefficient(a*b)


def coefficient_sum(a, b):
    a = bounded_coefficient(a); b = bounded_coefficient(b)
    common = gcd(a.denominator, b.denominator)
    left_factor = b.denominator//common
    right_factor = a.denominator//common
    resource(a.denominator.bit_length()+left_factor.bit_length() <= MAX_COEFFICIENT_BITS+1,
             'Coefficient sum denominator bound reached')
    resource(max(abs(a.numerator).bit_length()+left_factor.bit_length(),
                 abs(b.numerator).bit_length()+right_factor.bit_length()) <= MAX_COEFFICIENT_BITS+1,
             'Coefficient sum numerator bound reached')
    return bounded_coefficient(a+b)


def add(*parts):
    tick()
    out = defaultdict(Q)
    for c, p in parts:
        check_polynomial(p)
        for mon, a in p.items():
            out[mon] = coefficient_sum(out[mon], coefficient_product(c, a))
            resource(len(out) <= MAX_TERMS, 'Polynomial addition term bound reached')
    return {mon: a for mon, a in out.items() if a}


def mul(p, q):
    tick()
    check_polynomial(p); check_polynomial(q)
    resource(len(p)*len(q) <= 500_000, 'Polynomial product operation bound reached')
    out = defaultdict(Q)
    for mon, a in p.items():
        tick()
        for other, b in q.items():
            resource(len(mon)+len(other) <= MAX_DEGREE, 'Polynomial product degree bound reached')
            key = tuple(sorted(mon+other))
            out[key] = coefficient_sum(out[key], coefficient_product(a, b))
            resource(len(out) <= MAX_TERMS, 'Polynomial product term bound reached')
    out = {mon: a for mon, a in out.items() if a}
    return out


def power(p, n):
    out = const(1)
    for _ in range(n):
        out = mul(out, p)
    return out


def variables(p):
    return {x for mon in p for x in mon}


def decode(raw, limit, shared=0):
    assert isinstance(raw, list) and len(raw) > 0
    resource(len(raw) <= 256, 'Source row term bound reached')
    out = {}
    for coefficient, mon in raw:
        assert type(coefficient) is int and coefficient
        resource(abs(coefficient).bit_length() <= 4096, 'Source coefficient bit bound reached')
        assert isinstance(mon, list) and len(mon) <= 4
        assert all(type(x) is int and -shared <= x < limit for x in mon)
        key = tuple(mon)
        assert key == tuple(sorted(key)) and key not in out
        out[key] = Q(coefficient)
    return out


def normal(p):
    if not p:
        return ()
    check_polynomial(p)
    den = 1
    for a in p.values():
        tick()
        a = bounded_coefficient(a)
        factor = a.denominator//gcd(den, a.denominator)
        resource(den.bit_length()+factor.bit_length() <= MAX_COEFFICIENT_BITS+1,
                 'Normalization denominator bound reached')
        den *= factor
        resource(den.bit_length() <= MAX_COEFFICIENT_BITS, 'Normalization denominator bound reached')
    integers = {}
    for mon, a in p.items():
        a = Q(a); factor = den//a.denominator
        resource(abs(a.numerator).bit_length()+factor.bit_length() <= MAX_COEFFICIENT_BITS+1,
                 'Normalization integer bound reached')
        integers[mon] = a.numerator*factor
        resource(abs(integers[mon]).bit_length() <= MAX_COEFFICIENT_BITS, 'Normalization integer bound reached')
    common = gcd(*integers.values())
    if integers[min(integers)] < 0:
        common = -common
    return tuple(sorted((mon, a//common) for mon, a in integers.items()))


def subst(p, env):
    out = {}
    for mon, c in p.items():
        term = const(c)
        for x in mon:
            assert x in env, ('Undeclared or forward dependency', x)
            term = mul(term, env[x])
        out = add((1, out), (1, term))
    return out


def fa(a, b):
    return tuple(add((1, x), (1, y)) for x, y in zip(a, b))


def fs(a, b):
    return tuple(add((1, x), (-1, y)) for x, y in zip(a, b))


def fm(a, b):
    return (add((1, mul(a[0], b[0])), (2, mul(a[1], b[1]))),
            add((1, mul(a[0], b[1])), (1, mul(a[1], b[0]))))


def fc(a, c):
    return tuple(add((c, x)) for x in a)


def conj(a):
    return a[0], add((-1, a[1]))


ONE = (const(1), {})
ZERO = ({}, {})
D = (const(11), const(-6))
SMALL_D = (const(3), const(-1))


def coefficients(n):
    # sqrt(1-w) times sum binom(2k,k)w^k/(4^k(4k+1)).
    # This does not use the producer's first-order recurrence for a_j.
    root = [Q(1)]
    for j in range(1, n):
        root.append(root[-1]*(Q(j-1)-Q(1, 2))/j)
    integral = [Q(comb(2*j, j), 4**j*(4*j+1)) for j in range(n)]
    return [sum(root[j]*integral[k-j] for j in range(k+1)) for k in range(n)]


def expected_g(f, precision):
    cs = coefficients((precision+3)//4)
    w = fm(D, fm(f, f)); term = ONE; result = ZERO
    for c in cs:
        result = fa(result, fc(term, c))
        term = fm(term, w)
    return result


class Module:
    """Validate allocation logs, then expose only explicit definitions."""
    def __init__(self, obj, shared=0, arithmetic_labels=('arithmetic',)):
        self.obj = obj
        self.free = obj['free']
        assert type(self.free) is int and self.free > 0
        assert type(obj['locals']) is int and obj['locals'] >= 0
        resource(self.free <= MAX_COORDINATES and obj['locals'] <= 2000,
                 'Module allocation bound reached')
        self.total = self.free+obj['locals']
        resource(self.total <= MAX_COORDINATES, 'Module coordinate bound reached')
        resource(type(shared) is int and 0 <= shared <= MAX_COORDINATES, 'Shared allocation bound reached')
        resource(len(obj['residuals']) <= 3000, 'Module row bound reached')
        resource(len(obj['construction_log']) <= 10_000, 'Module log bound reached')
        resource(len(obj['calls']) <= 100, 'Module call bound reached')
        self.rows = [decode(row, self.total, shared) for row in obj['residuals']]
        self.labels = defaultdict(list); self.equations = defaultdict(list)
        self.arithmetic = set(); self.core = set(); self.row_labels = {}
        self.env = {x: v(x) for x in range(self.free)}
        self.env.update({-x: v(-x) for x in range(1, shared+1)})
        expanded_terms = len(self.env); expanded_bits = 2*len(self.env)
        self.definitions = {}; allocated = []; seen_rows = []; pending = None
        for op in obj['construction_log']:
            tick()
            assert len(op) == 3 and op[0] in ('variable', 'equation')
            kind, index, label = op
            assert type(index) is int and isinstance(label, str)
            if kind == 'variable':
                assert index == self.free+len(allocated)
                allocated.append(index); self.labels[label].append(index)
                if label in arithmetic_labels:
                    assert pending is None
                    pending = index
                else:
                    assert pending is None
                    self.env[index] = v(index)
            else:
                assert index == len(seen_rows)
                seen_rows.append(index); self.equations[label].append(index)
                self.row_labels[index] = label
                row = self.rows[index]
                assert variables(row) <= set(self.env) | ({pending} if pending is not None else set())
                if label in arithmetic_labels:
                    assert pending is not None
                    c = row.get((pending,), 0); assert c
                    rhs = add((-1/c, row), (1, v(pending)))
                    assert pending not in variables(rhs)
                    assert all(len(mon) <= 2 for mon in row)
                    self.env[pending] = subst(rhs, self.env)
                    expanded_terms += len(self.env[pending])
                    expanded_bits += sum(abs(a.numerator).bit_length()+a.denominator.bit_length()
                                         for a in self.env[pending].values())
                    resource(expanded_terms <= 250_000 and expanded_bits <= 250_000_000,
                             'Module aggregate expansion bound reached')
                    self.definitions[pending] = index
                    self.arithmetic.add(index); pending = None
                else:
                    assert pending is None
        assert pending is None and len(allocated) == obj['locals']
        assert seen_rows == list(range(len(self.rows)))
        for call in obj['calls']:
            assert isinstance(call['module'], str)
            assert all(type(x) is int and -shared <= x < self.total for x in call['args'])

    def scalar(self, label, number=0, count=1):
        assert len(self.labels[label]) == count, ('Variable label multiplicity', label)
        x = self.labels[label][number]; self.core.add(x)
        return v(x)

    def pair(self, label, number=0, count=1):
        return tuple(self.scalar(label+'.'+str(j), number, count) for j in (0, 1))


def check_compare(obj, high, label, compressed):
    m = Module(obj)
    assert m.free == 31 and obj['name'] == 'q_compare4'
    assert obj['precision'] == high and obj['label_precision'] == label
    assert obj['modeled_points'] == 4 and obj['compressed_primary_charts'] is compressed
    assert obj['logarithm_coordinate'] == 'reciprocal f=1/x'
    assert obj['input_layout'] == 'beta,s,t,z;4P;4A;4S;4T;4Z;conj_fJ;inv_conj_zJ;root;root_error;r'
    orders = [1]*11+[label]+[high]*3+[high, label, high, high, high]
    assert obj['field_inequality_orders'] == orders
    expected = defaultdict(list)
    def eq(tag, p):
        assert p
        expected[tag].append(p)
    def feq(tag, pair):
        for k, poly in enumerate(pair):
            eq(tag+'.'+str(k), poly)
    points = []
    for name in ('H', 'X0', 'X1', 'X2', 'X3'):
        u, vv, f, x = (m.pair(name+'.'+s) for s in ('u', 'v', 'f', 'x'))
        if compressed:
            p = m.pair(name+'.p')
            feq(name+'.f=u2', fs(f, fm(u, u)))
            feq(name+'.v2+df=1', fs(fa(fm(vv, vv), fm(SMALL_D, f)), ONE))
            feq(name+'.p2=x-Df', fs(fm(p, p), fs(x, fm(D, f))))
            feq(name+'.xf=1', fs(fm(x, f), ONE))
            points.append(dict(x=x, y=fm(x, p), f=f, p=p))
        else:
            w, z, h, y = (m.pair(name+'.'+s) for s in ('w', 'z', 'h', 'y'))
            feq(name+'.f=u^2', fs(f, fm(u, u)))
            feq(name+'.v2+df=1', fs(fa(fm(vv, vv), fm(SMALL_D, f)), ONE))
            feq(name+'.w2+v2=2', fs(fa(fm(w, w), fm(vv, vv)), fc(ONE, 2)))
            feq(name+'.h=vw', fs(h, fm(vv, w)))
            feq(name+'.zh+u=0', fa(fm(z, h), u))
            feq(name+'.xf=1', fs(fm(x, f), ONE))
            feq(name+'.yz+x=0', fa(fm(y, z), x))
            points.append(dict(x=x, y=y, f=f, z=z))
    differences = []
    for j, point in enumerate(points):
        target = dict(x=(v(4+4*j), v(5+4*j)), y=(v(6+4*j), v(7+4*j)))
        lam, nu, x, y, f, z = (m.pair('difference.'+s, j, 5)
                                for s in ('lambda', 'nu', 'x', 'y', 'f', 'z'))
        feq('difference line at first point', fs(fs(fm(lam, point['x']), point['y']), nu))
        feq('difference line at negated second point', fs(fa(fm(lam, target['x']), target['y']), nu))
        feq('difference abscissa', fa(fs(x, fm(lam, lam)), fa(point['x'], target['x'])))
        feq('difference line at output', fs(fa(fm(lam, x), y), nu))
        feq('difference reciprocal abscissa', fs(fm(f, x), ONE))
        feq('difference formal parameter', fa(fm(z, y), x))
        guard = m.scalar('distinct abscissae guard', j, 5)
        delta = fs(point['x'], target['x'])
        norm = add((1, mul(delta[0], delta[0])), (-2, mul(delta[1], delta[1])))
        eq('distinct abscissae guard', add((1, mul(guard, norm)), (-1, const(1))))
        differences.append(dict(x=x, y=y, f=f, z=z))
    gs = [expected_g(point['f'], high if j != 1 else label) for j, point in enumerate(points)]
    primary = []
    if compressed:
        lam = m.pair('common negative logarithm')
        feq('H pH=GH', fs(fm(lam, points[0]['p']), gs[0]))
        for j in range(4):
            ratio = m.pair('retained logarithm ratio', j, 4)
            aux = m.pair('ratio times p', j, 4)
            feq('A=C p', fs(aux, fm(ratio, points[j+1]['p'])))
            feq('A H=G', fs(fm(aux, lam), gs[j+1]))
            primary.append(fs(ratio, (v(j), {})))
    else:
        inverse = tuple(m.scalar('field inverse', j, 2) for j in range(2))
        logs = [fm(point['z'], g) for point, g in zip(points, gs)]
        inverse_product = fs(fm(logs[0], inverse), ONE)
        eq('field inverse real', inverse_product[0]); eq('field inverse sqrt2', inverse_product[1])
        primary = [fs(fm(logs[j+1], inverse), (v(j), {})) for j in range(4)]
    formal = [point['f'] for point in points]+[(v(24), v(25))]+[conj(point['f']) for point in differences]
    alternate = [fm(conj(point['z']), (v(26), v(27))) for point in differences]
    tests = [v(29)]
    for real, imag in formal+primary+alternate:
        tests.extend([mul(v(29), imag), add((1, real), (1, mul(v(28), imag)))])
    assert len(tests) == 41
    actual_tags = set(m.equations)-{'arithmetic'}
    assert actual_tags == expected.keys(), ('Missing or unexpected equation groups', actual_tags ^ expected.keys())
    for tag, polys in expected.items():
        ids = m.equations[tag]
        assert len(ids) == len(polys), ('Equation multiplicity', tag)
        for i, polynomial in zip(ids, polys):
            assert normal(subst(m.rows[i], m.env)) == normal(polynomial), ('Wrong core equation', tag, i)
    assert len(obj['calls']) == 1
    call = obj['calls'][0]
    assert call['module'] == 'q_batch41' and len(call['args']) == 42
    expected_args = [v(30)]+tests
    for index, (x, wanted) in enumerate(zip(call['args'], expected_args)):
        assert m.env[x] == wanted, ('Wrong ordered batch argument', index)
    # No extra unconstrained core witness, hidden chart, or missing inverse.
    assert m.core | set(m.definitions) == set(range(m.free, m.total))
    assert not m.core & set(m.definitions)
    # Full incidence accounting. Arithmetic witnesses are total polynomial
    # definitions; every consumer is checked above after exact expansion.
    incidence = defaultdict(list)
    for i, row in enumerate(m.rows):
        for x in variables(row):
            incidence[x].append(i)
    assert all(incidence[x] for x in range(m.free, m.total))
    if compressed:
        assert not any(name+'.z.' in tag for tag in m.labels for name in ('H','X0','X1','X2','X3'))
    return dict(status='PASS', compressed=compressed, high=high, label=label,
                free=m.free, local_coordinates=obj['locals'], arithmetic_definitions=len(m.definitions),
                checked_core_equations=sum(map(len, expected.values())),
                checked_ordered_batch_arguments=42, retained_difference_parameters=10)


def expected_plan(orders):
    groups = defaultdict(list)
    for i, order in enumerate(orders[1:], 2):
        groups[order].append(i)
    plan = [{'type': 'constant_pair', 'test': 1}]
    for order, indices in sorted(groups.items()):
        for start in range(0, len(indices), 2):
            pair = indices[start:start+2]
            plan.append({'type': 'pair', 'tests': pair, 'order': order} if len(pair) == 2
                        else {'type': 'single', 'test': pair[0], 'order': order})
    return plan


def check_batch(obj, orders):
    m = Module(obj, arithmetic_labels=('shared contact power',))
    assert obj['name'] == 'q_batch41' and m.free == 42
    assert obj['orders'] == orders and orders[0] == 1
    plan = expected_plan(orders); assert obj['norm_tree'] == plan
    assert obj['parity_module'] == 'q_primeparity' and obj['squareclass_correction'] is False
    consumed = set(m.arithmetic)
    def check(tag, polys):
        ids = m.equations[tag]
        assert len(ids) == len(polys), ('Batch equation multiplicity', tag)
        for i, p in zip(ids, polys):
            assert normal(subst(m.rows[i], m.env)) == normal(p), ('Wrong batch equation', tag, i)
            consumed.add(i)
    R = v(0)
    inv = m.scalar('nonzero contact factor')
    first = m.scalar('constant leaf norm')
    check('nonzero contact factor', [add((1, mul(R, inv)), (-1, const(1)))])
    check('fused constant leaf norm', [add((1, mul(R, first)), (-1, R), (-1, mul(v(1), v(1))))])
    nodes = [first]; pair_rows = []; single_rows = []
    for j, entry in enumerate(plan[1:]):
        out = m.scalar('normalized bottom norm', j, len(plan)-1)
        nodes.append(out); order = entry['order']
        if entry['type'] == 'pair':
            a, b = map(v, entry['tests'])
            pair_rows.append(add((1, mul(power(R, 2*order), out)), (-1, mul(a, a)), (-1, mul(R, mul(b, b)))))
        else:
            single_rows.append(add((1, mul(power(R, order), out)), (-1, v(entry['test']))))
    check('fused normalized pair', pair_rows)
    if single_rows:
        check('single normalized leaf', single_rows)
    upper = []; levels = []; number = 0
    count_upper = len(nodes)-1
    while len(nodes) > 1:
        levels.append(len(nodes)); next_nodes = []
        for start in range(0, len(nodes), 2):
            if start+1 == len(nodes):
                next_nodes.append(nodes[start]); continue
            a, b = nodes[start:start+2]
            out = m.scalar('cubic norm node', number, count_upper); number += 1
            upper.append(add((1, out), (-1, mul(a, a)), (-1, mul(R, mul(b, b)))))
            next_nodes.append(out)
        nodes = next_nodes
    assert obj['norm_level_sizes'] == levels
    check('cubic norm node', upper)
    square = m.scalar('batched square'); argument = m.scalar('parity argument')
    check('batched square', [add((1, square), (-1, mul(nodes[0], nodes[0])))])
    check('parity argument', [add((1, argument), (-1, mul(R, square)))])
    assert consumed == set(range(len(m.rows)))
    assert m.core | set(m.definitions) == set(range(m.free, m.total))
    assert obj['calls'] == [{'module': 'q_primeparity', 'args': [next(iter(argument))[0]]}]
    # Pure power definitions cannot constrain free inputs and cannot disguise
    # another witness relation or a change of norm leaves.
    assert all(len(value) == 1 and next(iter(value.values())) == 1
               and set(next(iter(value))) <= {0} for x, value in m.env.items() if x in m.definitions)
    return dict(status='PASS', ordered_tests=len(orders), bottom_nodes=len(plan), upper_nodes=len(upper))


def unchanged_modules(proposed, original, high):
    for name in ('q_height_batch', 'q_primeparity'):
        assert proposed[name] == original[name], ('Changed frozen module', name)
    root = deepcopy(original['Z_definition'])
    root['precision'] = high; root['anchor_squarings'] = 24 if high == 64 else 26
    assert proposed['Z_definition'] == root, 'Changed root constraints, contacts, or fixed generator'
    anchor = deepcopy(original['q_anchor'])
    if high == 52:
        anchor['anchor_squarings'] = 26; anchor['anchor_constant_global_index'] = -27
        for row in anchor['residuals']:
            for _, mon in row:
                mon[:] = [-27 if x == -25 else x for x in mon]
    assert proposed['q_anchor'] == anchor, 'Changed anchor constraints'


def flatten_and_check(directory, modules, high):
    squarings = 24 if high == 64 else 26
    shared_count = squarings+1
    shared = [[[-3, []], [1, [-1]]]]
    shared += [[[1, [-i-1]], [-1, [-i, -i]]] for i in range(1, squarings+1)]
    assert load(directory/'shared.json') == {'witnesses': shared_count, 'residuals': shared}
    rows = [[[c, sorted(-x for x in mon)] for c, mon in row] for row in shared]
    nextvar = shared_count+1; visits = []; active_stack = set()
    def visit(name, args, path):
        nonlocal nextvar
        tick()
        assert name in modules and name not in active_stack
        obj = modules[name]; assert len(args) == obj['free']
        start = nextvar; nextvar += obj['locals']; first_row = len(rows)
        resource(nextvar <= 40_000 and len(rows) <= 30_000, 'Flattened source size bound reached')
        def mapvar(x):
            if x < 0:
                assert -x <= shared_count
                return -x
            assert x < obj['free']+obj['locals']
            return args[x] if x < obj['free'] else start+x-obj['free']
        for row in obj['residuals']:
            rows.append([[c, sorted(mapvar(x) for x in mon)] for c, mon in row])
        visits.append(dict(module=name, path=path, arguments=args, first_local=start,
                           local_count=obj['locals'], first_residual=first_row, residual_count=len(obj['residuals'])))
        active_stack.add(name)
        for j, call in enumerate(obj['calls']):
            visit(call['module'], [mapvar(x) for x in call['args']], path+'/'+str(j))
        active_stack.remove(name)
    visit('Z_definition', [0], 'Z_definition')
    totals = {}; stack = set()
    def count(name):
        if name in totals:
            return totals[name]
        assert name not in stack; stack.add(name)
        obj = modules[name]; w, r = obj['locals'], len(obj['residuals'])
        for call in obj['calls']:
            cw, cr = count(call['module']); w += cw; r += cr
        stack.remove(name); totals[name] = [w, r]
        return totals[name]
    count('Z_definition')
    counts = dict(witnesses=nextvar-1, residuals=len(rows),
                  degree=2*max(len(mon) for row in rows for _, mon in row), modules=totals,
                  stored_residuals=sum(len(obj['residuals']) for obj in modules.values())+shared_count,
                  stored_calls=sum(len(obj['calls']) for obj in modules.values()),
                  anchor_squarings=squarings, chart=10, prime_parity_witnesses=7,
                  unit_scale=True, base_gates=True, curve_droot=[3,-1], curve_d2=[11,-6], log_block=2)
    assert load(directory/'counts.json') == counts
    polynomial = load(directory/'polynomial.json')
    assert polynomial == dict(semantics='Sum the square of every instantiated residual. Variable 0 is free X; all remaining variables range over Q.',
                              root='Z_definition', modules={name:'modules/'+name+'.json' for name in modules},
                              shared='shared.json', counts=counts)
    raw = directory/'residuals.jsonl'
    if raw.exists():
        stream = raw.open('rt')
    else:
        stream = gzip.open(directory/'residuals.jsonl.gz', 'rt')
    with stream:
        consumed_bytes = 0
        def line():
            nonlocal consumed_bytes
            tick()
            value = stream.readline(2_000_001)
            consumed_bytes += len(value)
            resource(len(value) <= 2_000_000 and consumed_bytes <= 50_000_000,
                     'Flattened residual stream bound reached')
            return value
        assert json.loads(line()) == counts
        for index, expected in enumerate(rows):
            tick()
            text = line(); assert text, ('Missing flattened row', index)
            assert json.loads(text) == expected, ('Wrong flattened row', index)
        tail = stream.read(2_000_001)
        resource(len(tail) <= 2_000_000, 'Flattened trailing-data bound reached')
        assert not tail.strip(), 'Extra flattened residuals'
    # If both encodings are supplied, neither may silently disagree with
    # the selected and report-bound residual stream.
    compressed = directory/'residuals.jsonl.gz'
    if raw.exists() and compressed.exists():
        total = 0
        with raw.open('rb') as left, gzip.open(compressed, 'rb') as right:
            while True:
                tick()
                a, b = left.read(65536), right.read(65536)
                total += max(len(a), len(b))
                resource(total <= 50_000_000, 'Residual encoding comparison bound reached')
                assert a == b, 'Raw and compressed residual streams disagree'
                if not a:
                    break
    visits_by_module = Counter(x['module'] for x in visits)
    assert visits_by_module == {'Z_definition':1, 'q_anchor':1, 'q_height_batch':1,
                               'q_compare4':41, 'q_batch41':41, 'q_primeparity':42}
    return counts, visits


def check(directory, original_directory):
    proposal = load(directory/'PROPOSED_SOURCE.json')
    high, label, compressed = (proposal[k] for k in ('high_precision','label_precision','compressed_primary_charts'))
    assert (high, label) in ((64,64),(64,16),(52,13),(52,16))
    assert type(compressed) is bool
    assert proposal['source_pin_authorized'] is False
    assert proposal['anchor_squarings'] == (24 if high == 64 else 26)
    assert proposal['scalar_orders'] == [1,1,1,1,48,48]
    assert proposal['hscale'] in (1,2,3,4)
    assert proposal['original_builder_digest_matched'] == ORIGINAL_BUILDER
    assert proposal['complete_original_comparison_regenerated'] == ORIGINAL_MODULES['q_compare4']
    assert set(proposal['compiler_sha256']) == {'archive_build.py','build_reciprocal_source.py','reciprocal_kernel.py'}
    for name, digest in proposal['compiler_sha256'].items():
        assert file_sha256(directory/'compiler'/name) == digest
    assert proposal['compiler_sha256']['archive_build.py'] == ORIGINAL_BUILDER
    original = {}
    for name, digest in ORIGINAL_MODULES.items():
        path = original_directory/'modules'/f'{name}.json'
        assert file_sha256(path) == digest, ('Unpinned original module', name)
        original[name] = load(path)
    assert {p.stem for p in (directory/'modules').glob('*.json')} == ORIGINAL_MODULES.keys()
    modules = {name: load(directory/'modules'/f'{name}.json') for name in ORIGINAL_MODULES}
    unchanged_modules(modules, original, high)
    # Syntax/log completeness for frozen modules too; their exact identity
    # above pins all numerical generator and contact choices.
    for name in ('Z_definition','q_anchor','q_height_batch','q_primeparity'):
        Module(modules[name], 25 if high == 64 else 27, arithmetic_labels=())
    compare_report = check_compare(modules['q_compare4'], high, label, compressed)
    orders = [1]*23+[label]*2+[high]*8+[label]*2+[high]*6
    batch_report = check_batch(modules['q_batch41'], orders)
    counts, visits = flatten_and_check(directory, modules, high)
    residual_name = 'residuals.jsonl' if (directory/'residuals.jsonl').exists() else 'residuals.jsonl.gz'
    inspected_names = ['PROPOSED_SOURCE.json', 'counts.json', 'polynomial.json', 'shared.json', residual_name]
    if (directory/'residuals.jsonl').exists() and (directory/'residuals.jsonl.gz').exists():
        inspected_names.append('residuals.jsonl.gz')
    inspected_names += ['modules/'+name+'.json' for name in ORIGINAL_MODULES]
    inspected_names += ['compiler/'+name for name in proposal['compiler_sha256']]
    inspected_hashes = {name: file_sha256(directory/name)
                        for name in sorted(inspected_names)}
    return dict(status='PASS: SOURCE CONSTRUCTION ONLY', high=high, label=label, compressed=compressed,
                source_pin_authorized=False, inspected_files_sha256=inspected_hashes,
                source_residual_file=residual_name,
                construction_map_sha256=hashlib.sha256(construction_map_bytes(visits)).hexdigest(),
                comparison=compare_report, batch=batch_report, counts=counts,
                original_modules_pinned=ORIGINAL_MODULES, original_builder=ORIGINAL_BUILDER,
                missing_constraint_checks='all core rows, all arithmetic definitions, all module calls, complete flattening',
                not_established=['arithmetic equivalence of the changed finite logarithms',
                                 'all-prime analytic estimates or global nonvanishing theorem',
                                 'acceptance of compressed-chart mathematical proof',
                                 'fresh quadratic lift or quartic coefficient bound',
                                 'partial mixed compressed/uncompressed source variants']), visits


def main():
    global DEADLINE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--write-map', type=Path)
    args = parser.parse_args()
    assert isfinite(args.seconds) and 0 < args.seconds <= 600
    started = time.monotonic(); DEADLINE = started+args.seconds
    report, visits = check(args.source, args.original)
    report['seconds'] = round(time.monotonic()-started, 3)
    report['checker_sha256'] = file_sha256(Path(__file__))
    tick()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    if args.write_map:
        args.write_map.parent.mkdir(parents=True, exist_ok=True)
        args.write_map.write_bytes(construction_map_bytes(visits))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
