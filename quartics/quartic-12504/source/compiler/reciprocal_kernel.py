"""Producer for reciprocal-coordinate logarithms. Not an independent checker."""
from fractions import Fraction


def coefficients(count):
    a = [Fraction(1)]
    if count > 1:
        a.append(Fraction(-2, 5))
    for j in range(2, count):
        a.append(a[-1] * Fraction(4*j-5, 4*j+1))
    return a


def emit_g(b, field, fcoords, precision, *, bind_output=True, hscale=1):
    """Return G(D*f^2), retaining only explicitly bound quadratic targets.

    The bound long output is normalized by a6. The returned expression
    restores that constant factor. Direct mode returns a quadratic output
    expression for fusion with a following equation.
    """
    if precision not in (13, 16, 52, 64):
        raise ValueError('Reviewed probe precisions are 13, 16, 52 and 64')
    if hscale not in (1, 2, 3, 4):
        raise ValueError('Unsupported nonzero constant scaling')
    m = field.m
    a = coefficients((precision + 3) // 4)
    zero = (b.P(), b.P())
    one = (b.P(1), b.P())
    def bind(pair):
        return tuple(m.value(x) for x in pair)
    w = bind(b.raw_fmul(field.D, b.raw_fmul(fcoords, fcoords)))
    w2 = field.mul(w, w)
    if len(a) == 4:
        expr = b.fa(b.fa(one, b.scale(w, a[1])),
                    b.fa(b.scale(w2, a[2]), b.scale(b.raw_fmul(w2, w), a[3])))
        return bind(expr) if bind_output else expr
    w3 = field.mul(w2, w)
    basis = [one, w, w2, w3]
    def low(cs):
        result = zero
        for j, c in enumerate(cs):
            if c:
                result = b.fa(result, b.scale(b.raw_fmul(basis[min(j, 3)], basis[max(j-3, 0)]), c))
        return result
    a += [Fraction(0)] * (16-len(a))
    h = bind(b.scale(b.raw_fmul(w3, w3), hscale))
    upper = low([a[j]/a[12] for j in range(12, 16)])
    tail = [Fraction(0)]*4 + [a[10]/a[12], a[11]/a[12]]
    t = bind(b.fa(b.scale(b.raw_fmul(h, upper), Fraction(1, hscale)), low(tail)))
    mid = low([a[j]/a[6] for j in range(6, 10)])
    body = b.fa(b.scale(b.raw_fmul(h, b.fa(b.scale(t, a[12]/a[6]), mid)), Fraction(1, hscale)),
                low([a[j]/a[6] for j in range(6)]))
    if bind_output:
        body = bind(body)
    return b.scale(body, a[6])


def comparison_point(b, field, label):
    """Chart without z; the surrounding G-ratio equations force p nonzero."""
    m = field.m
    u, v, f, x, p = [b.fvar(m, label+'.'+s) for s in ('u', 'v', 'f', 'x', 'p')]
    d = tuple(b.P(q) for q in b.CURVE_DROOT)
    b.feq(m, b.fs(f, b.raw_fmul(u, u)), label+'.f=u2')
    b.feq(m, b.fs(b.fa(b.raw_fmul(v, v), b.raw_fmul(d, f)), (b.P(1), b.P())), label+'.v2+df=1')
    b.feq(m, b.fs(b.raw_fmul(p, p), b.fs(x, b.raw_fmul(field.D, f))), label+'.p2=x-Df')
    b.feq(m, b.fs(b.raw_fmul(x, f), (b.P(1), b.P())), label+'.xf=1')
    return {'x': x, 'y': b.raw_fmul(x, p), 'f': f, 'p': p}


def install(b, *, high=64, label=64, compressed=False, hscale=1):
    """Install the proposed compiler in an isolated imported builder module."""
    if (high, label) not in ((64, 64), (64, 16), (52, 13), (52, 16)):
        raise ValueError('Unsupported proposed source parameters')
    if high == 52:
        # This is a comparison experiment, not the primary 64/24 proposal.
        b.ANCHOR_SQUARINGS = 26
    else:
        b.ANCHOR_SQUARINGS = 24
    b.PELL_PRECISION = high
    old_batch = b.make_batch
    orders = [1]*23 + [label]*2 + [high]*8 + [label]*2 + [high]*6
    def new_batch(name, source_orders, parity):
        return old_batch(name, orders if name == 'q_batch41' else source_orders, parity)
    b.make_batch = new_batch
    def new_log(field, point, precision=64):
        key = 'reciprocal_log'+str(precision)
        if key not in point:
            g = emit_g(b, field, field.f(point), precision, hscale=hscale)
            point[key] = field.mul(field.z(point), g)
        return point[key]
    b.Field.logarithm = new_log

    def new_comparison():
        n = 4
        free = n+4+4*n+4+3
        m = b.M('q_compare4', free)
        field = b.Field(m)
        at = n
        proxies = tuple(b.P.v(i) for i in range(n))
        def read_point():
            nonlocal at
            result = {'x': (b.P.v(at), b.P.v(at+1)), 'y': (b.P.v(at+2), b.P.v(at+3))}
            at += 4
            return result
        p4 = read_point()
        q4 = [read_point() for _ in range(n)]
        fj = (b.P.v(at), b.P.v(at+1)); at += 2
        zji = (b.P.v(at), b.P.v(at+1)); at += 2
        root, error, r = b.P.v(at), b.P.v(at+1), at+2
        assert r == free-1
        if compressed:
            points = [comparison_point(b, field, s) for s in ('H', 'X0', 'X1', 'X2', 'X3')]
        else:
            points = [field.gpoint(s) for s in ('H', 'X0', 'X1', 'X2', 'X3')]
        differences = [field.difference(p, q) for p, q in zip(points, [p4]+q4)]
        formal = [field.f(p) for p in points] + [fj] + [field.conj(field.f(p)) for p in differences]
        primary = []
        if compressed:
            # H=G(f_H)/p_H=-L_H. All ratios retain the old sign.
            h = b.fvar(m, 'common negative logarithm')
            gh = emit_g(b, field, points[0]['f'], high, bind_output=False, hscale=hscale)
            b.feq(m, b.fs(b.raw_fmul(h, points[0]['p']), gh), 'H pH=GH')
            for i, (point, proxy) in enumerate(zip(points[1:], proxies)):
                c = b.fvar(m, 'retained logarithm ratio')
                a = b.fvar(m, 'ratio times p')
                b.feq(m, b.fs(a, b.raw_fmul(c, point['p'])), 'A=C p')
                gi = emit_g(b, field, point['f'], label if i == 0 else high,
                            bind_output=False, hscale=hscale)
                b.feq(m, b.fs(b.raw_fmul(a, h), gi), 'A H=G')
                primary.append(b.fs(c, (proxy, b.P())))
        else:
            inverse = field.inv(field.logarithm(points[0], high))
            for i, (point, proxy) in enumerate(zip(points[1:], proxies)):
                value = field.mul(field.logarithm(point, label if i == 0 else high), inverse)
                primary.append(b.fs(value, (proxy, b.P())))
        alternate = [field.mul(field.conj(field.z(p)), zji) for p in differences]
        tests = b.field_tests(m, root, error, formal+primary+alternate)
        assert len(tests) == 41
        m.call('q_batch41', [r]+tests)
        m.save(precision=high, label_precision=label, modeled_points=4,
               field_inequality_orders=[1]*11+[label]+[high]*3+[high,label,high,high,high],
               logarithm_coordinate='reciprocal f=1/x', compressed_primary_charts=compressed,
               input_layout='beta,s,t,z;4P;4A;4S;4T;4Z;conj_fJ;inv_conj_zJ;root;root_error;r')
    b.make_multi_comparison = new_comparison
