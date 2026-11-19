"""Finite congruence descent for the locally soluble diagonal fiber d=112/289."""


def classes():
    candidates = [1, -1]
    for prime in (2, 3, 7, 17, 59):
        candidates += [prime*k for k in candidates]
    return [(k, 7*k if k % 7 else k//7) for k in candidates]


def allowed_at(candidates, prime, exponent):
    modulus = prime**exponent
    squares = {x*x % modulus for x in range(modulus)}
    values = set()
    for denominator_chart in (False, True):
        step = prime if denominator_chart else 1
        for t in range(0, modulus, step):
            a, b = (1, t) if denominator_chart else (t, 1)
            r, s = a*a, b*b
            u = 289*r*(112*s+289*r)
            v = 177*s*(112*s-289*r)
            values.add(((u+v) % modulus, (u-v) % modulus))
    return [(k,j) for k,j in candidates
            if any((k*u) % modulus in squares and (j*v) % modulus in squares
                   for u,v in values)]


if __name__ == '__main__':
    remaining = classes()
    assert len(remaining) == 64
    for p, e, expected in [(2,8,32), (3,3,16), (7,2,4), (41,1,0)]:
        remaining = allowed_at(remaining, p, e)
        assert len(remaining) == expected
        if p == 7:
            assert set(remaining) == {(7,1), (14,2), (-413,-59), (-826,-118)}
        print(f'mod {p**e}: {len(remaining)} candidate classes survive')
