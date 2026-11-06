"""Independent exact checker for a quartic projection-preserving certificate.

Only the Python standard library is required. No search/producer code is imported.
This checks algebraic equivalence to the pinned source residual system, not the
arithmetic theorem asserting that the source system defines the integers.
"""
import argparse,gzip,hashlib,itertools,json,math,time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

if not __debug__:raise RuntimeError('Do not disable the checks with python -O.')
SOURCE_ENTRIES = {'original64': {'source_sha256': '6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2', 'source_variables': 15672, 'source_rows': 15107}, 'reciprocal64-beta16-compressed-s1-b5e836d77643': {'source_id': 'reciprocal64-beta16-compressed-s1-b5e836d77643', 'source_sha256': 'ce9eeac7c4730aced8cfb70a1ab3b1b6a7fb2110c597afad1f56ddc92aeea73f', 'uncompressed_sha256': 'b5e836d7764363fcbfdafbacefe80a5f53e0979eba73af990827942b0fa9351d', 'source_variables': 12064, 'source_rows': 11499, 'source_header': {'witnesses': 12063, 'residuals': 11499, 'degree': 8, 'modules': {'q_anchor': [16, 6], 'q_primeparity': [7, 4], 'q_height_batch': [34, 31], 'q_batch41': [58, 55], 'q_compare4': [285, 272], 'Z_definition': [12038, 11474]}, 'stored_residuals': 615, 'stored_calls': 46, 'anchor_squarings': 24, 'chart': 10, 'prime_parity_witnesses': 7, 'unit_scale': True, 'base_gates': True, 'curve_droot': [3, -1], 'curve_d2': [11, -6], 'log_block': 2}, 'source_audit_sha256': '7c67ff1736e4a4f0e1f7e70e7f5e47c956dfb0c644fd5264acd0c224bbd60e01', 'source_audit_checker_sha256': '495ca32737687fca335704c6bdbabacf8f20a7698839aa680639e8e1b60a948f', 'construction_map_sha256': 'edad166ce99d33fe50271e2afdc1628bbec0361d812762212240cadd30f93cfe', 'inspected_files_sha256': {'PROPOSED_SOURCE.json': '93df4b4c2f8aba4dd74c93d64a95347e2494d804752dc3647907e14b91f1a9bb', 'compiler/archive_build.py': 'c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912', 'compiler/build_reciprocal_source.py': 'd9ec8f4788882f37f3a0b7746f8d19c28968f7bf3f09cc06addab92f787098f6', 'compiler/reciprocal_kernel.py': 'c4e94463cd59a2418a6502ac7cdcfd713edf9bc1134fe0b4d4bd84700983b304', 'counts.json': '71cf2c65bb51f837014e1803c19c9e5ed28faa86c8e3faffdff1992072d1933d', 'modules/Z_definition.json': '3481dc07810493980b94071aab3e728ead885710213d1fef337199e8d2f73885', 'modules/q_anchor.json': '961e0cdbaefef28d3fa718f4e5924b5b60e4c500fb4bf2ce33e0898a4650c270', 'modules/q_batch41.json': '2f9e8adfdabb3a224ddb0599c99c8e39877d27ac28516feec1a3df831aae96e2', 'modules/q_compare4.json': '0c529d02717b4300bb76525f3eb13524abfc99a6156a96c18b4ba5492cc31482', 'modules/q_height_batch.json': '15fc8a127c95a27b6104c9dfab5890c9f2ad801ee24203431248860f52b1ac42', 'modules/q_primeparity.json': 'df89176d00ab6cc61e86416c5d1209554fcf87f45f30a866177c76683c2a306a', 'polynomial.json': '2874f4d2b9eaf9752771007f393628fd2fffe2c283a4a5187a7ca1ad7da47269', 'residuals.jsonl': 'b5e836d7764363fcbfdafbacefe80a5f53e0979eba73af990827942b0fa9351d', 'shared.json': 'e8da6dac27a0aab65ab8a377a9a9c78bd8baccd40f4dff229fce17759b03cc28'}, 'high': 64, 'label': 16, 'compressed': True, 'uncompressed_chart_count': 6, 'arithmetic_status': 'REVIEWED PROPOSAL; arithmetic acceptance is outside this algebraic checker'}}

def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode('ascii')
def decode(terms):
    result={}
    for coefficient,variables in terms:
        assert type(coefficient) is int and coefficient!=0
        assert all(type(v) is int and v>=0 for v in variables)
        m=tuple(variables);assert m==tuple(sorted(m)) and m not in result
        result[m]=coefficient
    return result
def encode(row):return [[c,list(m)] for m,c in row.items()]
def add(*summands):
    result=defaultdict(Fraction)
    for scalar,poly in summands:
        for m,c in poly.items():result[m]+=scalar*c
    return {m:c for m,c in result.items() if c}
def mul(f,g):
    result=defaultdict(Fraction)
    for m,c in f.items():
        for n,d in g.items():result[tuple(sorted(m+n))]+=c*d
    return {m:c for m,c in result.items() if c}
def normal(row):
    if not row:return ()
    common=math.lcm(*(Fraction(c).denominator for c in row.values()))
    terms={m:int(c*common) for m,c in row.items() if c}
    divisor=math.gcd(*terms.values())
    if terms[min(terms)]<0:divisor=-divisor
    return tuple(sorted((m,c//divisor) for m,c in terms.items()))
def substitute(row,v,replacement):
    result={}
    for m,c in row.items():
        value={():Fraction(c)}
        for variable in m:value=mul(value,replacement if variable==v else {(variable,):1})
        result=add((1,result),(1,value))
    return result
def variables(row):return {v for m in row for v in m}

def expand_definitions(row,definitions):
    result={}
    for monomial,coefficient in row.items():
        term={():Fraction(coefficient)}
        for v in monomial:term=mul(term,definitions.get(v,{(v,):1}))
        result=add((1,result),(1,term))
    return result

def decode_affine(obj):
    denominator=obj['denominator']
    assert type(denominator) is int and denominator>0
    row=decode(obj['terms'])
    assert all(len(mon)<=1 for mon in row)
    return {m:Fraction(c,denominator) for m,c in row.items()}

def unit_scale_expected(rows,d,nextvar):
    """Use the rational nonsquareness proof in UNIT_SCALING.md, not a field axiom."""
    E,theta,proof=d['unit'],d['root'],d['root_row']
    assert all(type(v) is int and 0<v<nextvar for v in (E,theta)) and E!=theta
    assert type(proof) is int and 0<=proof<len(rows)
    assert normal(rows[proof])==normal({(E,):1,(theta,theta):-1,():2})
    pairs=d['weights'];weights={v:k for v,k in pairs}
    assert len(weights)==len(pairs) and weights
    assert all(type(v) is int and 0<v<nextvar and v not in (E,theta)
               and type(k) is int and 1<=k<=8 for v,k in pairs)
    replacements=defaultdict(dict);bridges=[];aliased=set()
    for v,a,consumers in d['aliases']:
        assert type(v) is int and weights.get(v)==1 and v not in aliased
        aliased.add(v)
        assert type(a) is int and a==nextvar;nextvar+=1
        assert consumers and len(consumers)==len(set(consumers))
        for j in consumers:
            assert type(j) is int and 0<=j<len(rows) and j!=proof
            assert v in variables(rows[j])
            replacements[j][v]=a
        bridges.append({(v,):1,tuple(sorted((E,a))):-1})
    expected={}
    for j,row in enumerate(rows):
        if not variables(row)&weights.keys():continue
        laurent=defaultdict(Fraction);aliases=replacements[j]
        for mon,c in row.items():
            exponent=0;other=[]
            for v in mon:
                if v==E:exponent+=1
                elif v in aliases:other.append(aliases[v])
                else:other.append(v);exponent-=weights.get(v,0)
            laurent[(tuple(sorted(other)),exponent)]+=c
        laurent={m:c for m,c in laurent.items() if c}
        least=min((power for (_,power) in laurent),default=0)
        transformed={tuple(sorted(mon+(E,)*(power-least))):c
                     for (mon,power),c in laurent.items()}
        assert all(len(mon)<=2 for mon in transformed),'Unit scaling exceeds quadratic degree'
        expected[j]=transformed
    assert proof not in expected
    for k,row in enumerate(bridges):expected[len(rows)+k]=row
    return expected,nextvar

def redundant_inverse_expected(rows,d,nextvar,incidence):
    """Discard a private inverse using R*H=E^2 and E=theta^2-2 != 0."""
    i,u=d['row'],d['inverse'];nz=d['nonzero']
    assert type(i) is int and 0<=i<len(rows)
    assert type(u) is int and 0<u<nextvar and incidence[u]=={i}
    assert nz['kind']=='root_error'
    j,k=nz['root_row'],nz['relation_row']
    assert all(type(n) is int and 0<=n<len(rows) for n in (j,k))
    assert len({i,j,k})==3
    R,theta,E,H=[decode_affine(obj) for obj in
                 (d['factor'],nz['root'],nz['error'],nz['cofactor'])]
    for form in (R,theta,E,H):
        assert all(v<nextvar and v!=u for v in variables(form))
    assert normal(rows[i])==normal(add((1,mul({(u,):1},R)),(-1,{():1})))
    assert normal(rows[j])==normal(add((1,E),(-1,mul(theta,theta)),(2,{():1})))
    assert normal(rows[k])==normal(add((1,mul(R,H)),(-1,mul(E,E))))
    return {i:{}}


_rules_chart={'__name__':'embedded_chart'}
exec(compile('"""Independent verifier for the seven-field-coordinate sparse 2E chart.\n\nThis file imports no producer code. See PROOF.md for the solution maps.\n"""\nfrom collections import defaultdict\nfrom fractions import Fraction\nfrom functools import reduce\nfrom math import gcd, lcm\n\n\ndef add(*terms):\n    answer = defaultdict(Fraction)\n    for scalar, polynomial in terms:\n        for monomial, coefficient in polynomial.items():\n            answer[monomial] += scalar * coefficient\n    return {m: c for m, c in answer.items() if c}\n\n\ndef multiply(left, right):\n    answer = defaultdict(Fraction)\n    for m, c in left.items():\n        for n, d in right.items():\n            answer[tuple(sorted(m + n))] += c * d\n    return {m: c for m, c in answer.items() if c}\n\n\ndef normalize(polynomial):\n    if not polynomial:\n        return ()\n    denominator = lcm(*(Fraction(c).denominator for c in polynomial.values()))\n    integer = {m: int(c * denominator) for m, c in polynomial.items()}\n    common = reduce(gcd, integer.values())\n    if integer[min(integer)] < 0:\n        common = -common\n    return tuple(sorted((m, c // common) for m, c in integer.items()))\n\n\ndef variables(polynomial):\n    return {v for m in polynomial for v in m}\n\n\ndef fadd(left, right, scalar=1):\n    return tuple(add((1, a), (scalar, b)) for a, b in zip(left, right))\n\n\ndef fmul(left, right):\n    a, b = left\n    c, d = right\n    return add((1, multiply(a, c)), (2, multiply(b, d))), add((1, multiply(a, d)), (1, multiply(b, c)))\n\n\ndef chart_expected(rows, data, nextvar, incidence):\n    """Return exact replacement rows and next unused variable, or reject."""\n    names = (\'u\', \'v\', \'w\', \'z\', \'f\', \'h\', \'x\', \'y\')\n    blocks = (\'f=u^2\', \'v2+df=1\', \'w2+v2=2\', \'h=vw\', \'zh+u=0\', \'xf=1\', \'yz+x=0\')\n    assert set(data) == {\'coordinates\', \'rows\', \'new_variables\', \'droot\'}\n    assert data[\'droot\'] == [3, -1], \'Unexpected pinned curve parameter\'\n    coordinates = data[\'coordinates\']\n    assert set(coordinates) == set(names)\n    old_variables = []\n    for name in names:\n        pair = coordinates[name]\n        assert type(pair) is list and len(pair) == 2\n        assert all(type(v) is int and 0 < v < nextvar for v in pair)\n        old_variables.extend(pair)\n    assert len(set(old_variables)) == 16, \'Aliased chart coordinates\'\n    row_ids = data[\'rows\']\n    assert set(row_ids) == set(blocks)\n    selected = []\n    for block in blocks:\n        pair = row_ids[block]\n        assert type(pair) is list and len(pair) == 2\n        assert all(type(i) is int and 0 <= i < len(rows) for i in pair)\n        selected.extend(pair)\n    assert len(set(selected)) == 14, \'Duplicate proof row\'\n    u, v, w, z, f, h, x, y = [tuple({(i,): 1} for i in coordinates[name]) for name in names]\n    one, two = ({(): 1}, {}), ({(): 2}, {})\n    droot, dsquare = ({(): 3}, {(): -1}), ({(): 11}, {(): -6})\n    old = (\n        fadd(f, fmul(u, u), -1),\n        fadd(fadd(fmul(v, v), fmul(droot, f)), one, -1),\n        fadd(fadd(fmul(w, w), fmul(v, v)), two, -1),\n        fadd(h, fmul(v, w), -1),\n        fadd(fmul(z, h), u),\n        fadd(fmul(x, f), one, -1),\n        fadd(fmul(y, z), x),\n    )\n    for block, pair in zip(blocks, old):\n        for index, expected in zip(row_ids[block], pair):\n            assert normalize(rows[index]) == normalize(expected), (\'Chart proof row differs\', block, index)\n    changed = set(row_ids[\'w2+v2=2\'] + row_ids[\'h=vw\'] + row_ids[\'zh+u=0\'])\n    removed = set(coordinates[\'w\'] + coordinates[\'h\'])\n    for v in removed:\n        assert incidence.get(v, set()) <= changed, (\'Removed chart coordinate used outside\', v)\n    fresh = data[\'new_variables\']\n    assert type(fresh) is list and len(fresh) == 2\n    assert all(type(v) is int for v in fresh)\n    assert fresh == [nextvar, nextvar + 1], \'Nonfresh p coordinate\'\n    p = tuple({(i,): 1} for i in fresh)\n    new = (fadd(p, fmul(y, f), -1), fadd(fadd(fmul(p, p), x, -1), fmul(dsquare, f)))\n    patches = {i: {} for i in changed}\n    for block, pair in zip((\'w2+v2=2\', \'h=vw\'), new):\n        for index, expected in zip(row_ids[block], pair):\n            assert all(len(m) <= 2 for m in expected)\n            assert not variables(expected) & removed\n            patches[index] = expected\n    return patches, nextvar + 2\n\n\ndef ordinate_expected(rows, data, nextvar, incidence):\n    """Eliminate y=x*p, using xf=1 to preserve the two chart relations."""\n    assert set(data) == {\'coordinates\', \'rows\'}\n    coordinates, row_ids = data[\'coordinates\'], data[\'rows\']\n    names = (\'x\', \'y\', \'z\', \'f\', \'p\')\n    blocks = (\'xf=1\', \'p=yf\', \'yz+x=0\')\n    assert set(coordinates) == set(names) and set(row_ids) == set(blocks)\n    flat = []\n    for name in names:\n        pair = coordinates[name]\n        assert type(pair) is list and len(pair) == 2\n        assert all(type(v) is int and 0 < v < nextvar for v in pair)\n        flat.extend(pair)\n    assert len(set(flat)) == 10, \'Aliased ordinate proof coordinates\'\n    indices = []\n    for block in blocks:\n        pair = row_ids[block]\n        assert type(pair) is list and len(pair) == 2\n        assert all(type(i) is int and 0 <= i < len(rows) for i in pair)\n        indices.extend(pair)\n    assert len(set(indices)) == 6, \'Duplicate ordinate proof row\'\n    x, y, z, f, p = [tuple({(i,): 1} for i in coordinates[name]) for name in names]\n    one = ({(): 1}, {})\n    old = (fadd(fmul(x, f), one, -1), fadd(p, fmul(y, f), -1), fadd(fmul(y, z), x))\n    for block, pair in zip(blocks, old):\n        for i, expected in zip(row_ids[block], pair):\n            assert normalize(rows[i]) == normalize(expected), (\'Ordinate proof row differs\', block, i)\n    removed = set(coordinates[\'y\'])\n    replacements = dict(zip(coordinates[\'y\'], fmul(x, p)))\n    affected = set().union(*(incidence.get(v, set()) for v in removed))\n    assert set(row_ids[\'p=yf\'] + row_ids[\'yz+x=0\']) <= affected\n    patches = {}\n    for i in affected:\n        if i in row_ids[\'p=yf\']:\n            patches[i] = {}\n            continue\n        if i in row_ids[\'yz+x=0\']:\n            k = row_ids[\'yz+x=0\'].index(i)\n            patches[i] = fadd(fmul(p, z), one)[k]\n            continue\n        replacement = {}\n        for monomial, coefficient in rows[i].items():\n            term = {(): coefficient}\n            for v in monomial:\n                term = multiply(term, replacements.get(v, {(v,): 1}))\n            replacement = add((1, replacement), (1, term))\n        assert all(len(m) <= 2 for m in replacement), \'Ordinate substitution exceeds quadratic degree\'\n        assert not variables(replacement) & removed\n        patches[i] = replacement\n    return patches, nextvar\n','<embedded-chart>','exec'),_rules_chart)
_rules_parity={'__name__':'embedded_parity'}
exec(compile('"""Independent checker for the exact q_primeparity conic replacement.\n\nNo producer or repository modules are imported. See PROOF.md for rational\nsolution maps, including both zero and exceptional-chart cases.\n"""\nfrom collections import defaultdict\nfrom fractions import Fraction as F\nfrom math import gcd, lcm\n\n\ndef add(*terms):\n    out = defaultdict(F)\n    for k, row in terms:\n        for mon, c in row.items():\n            out[mon] += k*c\n    return {m: c for m, c in out.items() if c}\n\n\ndef mul(left, right):\n    out = defaultdict(F)\n    for m, c in left.items():\n        for n, d in right.items():\n            out[tuple(sorted(m+n))] += c*d\n    return {m: c for m, c in out.items() if c}\n\n\ndef var(v):\n    return {(v,): F(1)}\n\n\ndef norm(row):\n    if not row:\n        return ()\n    den = lcm(*(F(c).denominator for c in row.values()))\n    ints = {m: int(c*den) for m, c in row.items() if c}\n    divisor = gcd(*ints.values())\n    if ints[min(ints)] < 0:\n        divisor = -divisor\n    return tuple(sorted((m, c//divisor) for m, c in ints.items()))\n\n\ndef variables(row):\n    return {v for m in row for v in m}\n\n\ndef expand(row, definitions):\n    result = {}\n    for mon, c in row.items():\n        term = {(): c}\n        for v in mon:\n            term = mul(term, definitions.get(v, var(v)))\n        result = add((1, result), (1, term))\n    return result\n\n\ndef source_rows(b, witnesses):\n    b = var(b)\n    t, u, e, p, q, s, h = map(var, witnesses)\n    tt, uu, ss = mul(t,t), mul(u,u), mul(s,s)\n    return [\n        add((1,u),(-1,b),(1,mul(mul(b,b),tt)),(1,mul(mul(b,u),tt))),\n        add((1,mul(p,p)),(-17,b),(-34,mul(b,e)),(51,mul(b,mul(e,e)))),\n        add((1,h),(-17,mul(b,e)),(1,mul(e,uu))),\n        add((17,mul(b,mul(q,q))),(-1,mul(ss,ss)),\n            (-34,mul(mul(b,h),ss)),(867,mul(mul(b,b),mul(h,h))))]\n\n\ndef replacement_rows(b, fresh):\n    b = var(b)\n    u,v,a,z,e,p,c,w,s,q,j,k = map(var, fresh)\n    return [\n        add((1,z),(-1,mul(u,u))),\n        add((1,a),(-1,mul(b,v))),\n        add((1,z),(1,mul(v,a)),(-1,mul(b,b))),\n        add((1,c),(-1,mul(b,e))),\n        add((1,mul(p,p)),(-17,b),(-34,c),(51,mul(e,c))),\n        add((1,w),(-17,mul(b,c)),(1,mul(c,z))),\n        add((1,j),(-1,mul(s,s))),\n        add((1,k),(-1,mul(b,q))),\n        add((1,mul(j,j)),(34,mul(j,w)),(-867,mul(w,w)),(-17,mul(q,k)))]\n\n\ndef check_rule(rows, incidence, data, nextvar):\n    """Return expected patches and new allocation count; fail closed."""\n    b = data[\'input\']\n    old = data[\'old_witnesses\']\n    ids = data[\'residual_rows\']\n    defs = data[\'definitions\']\n    new = data[\'new_variables\']\n    assert type(b) is int and 0 <= b < nextvar\n    assert len(old) == len(set(old)) == 7\n    assert all(type(v) is int and 0 < v < nextvar and v != b for v in old)\n    assert len(ids) == len(set(ids)) == 4\n    assert all(type(i) is int and 0 <= i < len(rows) for i in ids)\n    assert len(new) == 12 and new == list(range(nextvar, nextvar+12))\n    assert all(isinstance(d, list) and len(d) == 2 for d in defs)\n    di = [i for i,v in defs]\n    dv = [v for i,v in defs]\n    assert len(di) == len(set(di)) and len(dv) == len(set(dv))\n    assert not set(di)&set(ids)\n    assert all(type(i) is int and 0 <= i < len(rows) for i in di)\n    assert all(type(v) is int and 0 < v < nextvar for v in dv)\n    assert not set(dv)&(set(old)|{b})\n    selected = set(ids)|set(di)\n    removed = set(old)|set(dv)\n    assert len(selected) >= 9\n    for v in removed:\n        assert incidence.get(v,set()) <= selected, \'Outside use of removed parity coordinate\'\n    expanded = {}\n    for i,v in defs:\n        row = rows[i]\n        coefficient = row.get((v,),0)\n        assert coefficient\n        rhs = add((-1/F(coefficient),row),(1,var(v)))\n        assert v not in variables(rhs)\n        assert variables(rhs) <= set(old)|{b}|set(expanded), \'Non-acyclic or external definition\'\n        expanded[v] = expand(rhs,expanded)\n    expected_source = source_rows(b,old)\n    for i,source in zip(ids,expected_source):\n        assert norm(expand(rows[i],expanded)) == norm(source), \'Wrong source parity residual\'\n    expected = {i:{} for i in selected}\n    for i,row in zip(sorted(selected),replacement_rows(b,new)):\n        assert all(len(m)<=2 for m in row)\n        expected[i] = dict(norm(row))\n    return expected,nextvar+12\n\n\ndef check_patches(expected, supplied):\n    assert len(supplied) == len({i for i,row in supplied})\n    actual = {i:{tuple(m):c for c,m in row} for i,row in supplied}\n    assert actual.keys() == expected.keys()\n    for i,row in actual.items():\n        assert all(type(c) is int and c and len(m)<=2 for m,c in row.items())\n        assert norm(row) == norm(expected[i]), \'Incorrect supplied replacement\'\n\n\ndef old_to_new(b, old):\n    t,u,e,p,q,s,h = map(F,old)\n    b = F(b)\n    denominator = 1+b*t*t\n    assert denominator != 0\n    v = 2*b*t/denominator\n    return [u,v,b*v,u*u,e,p,b*e,b*h,s,q,s*s,b*q]\n\n\ndef new_to_old(b, new):\n    b = F(b)\n    u,v,a,z,e,p,c,w,s,q,j,k = map(F,new)\n    if not b:\n        assert u == 0\n        t = F(0)\n    elif u+b:\n        t = v/(u+b)\n    else:\n        assert u == -b and v == 0\n        u = b\n        t = F(0)\n    return [t,u,e,p,q,s,e*(17*b-z)]\n','<embedded-parity>','exec'),_rules_parity)
_rules_batch={'__name__':'embedded_batch'}
exec(compile('"""Independent checker for root-error absorption in a quadratic norm batch.\n\nIntegration: import batch_absorb_expected; dispatch the event kind\n``batch_absorb`` to expected,nextvar=batch_absorb_expected(rows,d,nextvar,incidence).\nThe caller must check every supplied patch against ``expected`` up to a nonzero\nrational scalar and retain the usual final expansion checks.\n"""\nfrom collections import defaultdict\nfrom fractions import Fraction\nfrom math import gcd, lcm\n\n\ndef dec(terms):\n    p = {}\n    for c, m in terms:\n        assert type(c) is int and c != 0\n        assert type(m) is list and all(type(v) is int and v >= 0 for v in m)\n        t = tuple(m)\n        assert t == tuple(sorted(t)) and t not in p\n        p[t] = Fraction(c)\n    return p\n\n\ndef vs(p):\n    return {v for m in p for v in m}\n\n\ndef add(*parts):\n    out = defaultdict(Fraction)\n    for c, p in parts:\n        for m, a in p.items():\n            out[m] += c*a\n    return {m: a for m, a in out.items() if a}\n\n\ndef mul(p, q):\n    out = defaultdict(Fraction)\n    for m, a in p.items():\n        for n, b in q.items():\n            out[tuple(sorted(m+n))] += a*b\n    return {m: a for m, a in out.items() if a}\n\n\ndef v(i):\n    return {(i,): Fraction(1)}\n\n\ndef canon(p):\n    if not p:\n        return ()\n    den = lcm(*(Fraction(c).denominator for c in p.values()))\n    q = {m: int(c*den) for m, c in p.items()}\n    g = gcd(*q.values())\n    if q[min(q)] < 0:\n        g = -g\n    return tuple(sorted((m, c//g) for m, c in q.items()))\n\n\ndef expand(p, defs):\n    out = {}\n    for m, a in p.items():\n        term = {(): a}\n        for i in m:\n            term = mul(term, defs.get(i, v(i)))\n        out = add((1, out), (1, term))\n    return out\n\n\ndef batch_absorb_expected(rows, d, nextvar, incidence):\n    old_limit = nextvar\n    def old(i):\n        assert type(i) is int and 0 < i < old_limit\n        return v(i)\n    def row(i):\n        assert type(i) is int and 0 <= i < len(rows)\n        return rows[i]\n    def eq(i, p):\n        assert p and canon(row(i)) == canon(p)\n    E, T = old(d[\'error\']), old(d[\'root\'])\n    assert d[\'error\'] != d[\'root\']\n    root_row = d[\'root_row\']\n    eq(root_row, add((1, E), (-1, mul(T, T)), (2, {(): 1})))\n    # Over Q the retained root row implies E != 0: sqrt(2) is irrational.\n    # Every retained first-leaf row then proves its R != 0.\n    proofs = {}\n    proof_rows = {root_row}\n    for r, f, i in d[\'first_leaves\']:\n        R, F = old(r), old(f)\n        assert r not in proofs and i not in proof_rows\n        eq(i, add((1, mul(R, F)), (-1, R), (-1, mul(E, E))))\n        proofs[r] = f\n        proof_rows.add(i)\n    assert proofs\n\n    items = d[\'definitions\']\n    targets = [t for _, t in items]\n    indices = [i for i, _ in items]\n    assert len(targets) == len(set(targets))\n    assert len(indices) == len(set(indices))\n    assert not set(indices) & proof_rows\n    target_set = set(targets)\n    expanded = {}\n    for i, t in items:\n        old(t)\n        rr = row(i)\n        c = rr.get((t,), 0)\n        assert c\n        rhs = add((-Fraction(1, c), rr), (1, v(t)))\n        assert t not in vs(rhs)\n        assert vs(rhs) & target_set <= expanded.keys()\n        expanded[t] = expand(rhs, expanded)\n\n    removed_list = d[\'removed\']\n    removed = set(removed_list)\n    assert len(removed) == len(removed_list) and removed <= target_set\n    pair_rows = [p[\'row\'] for p in d[\'pairs\']]\n    assert pair_rows and len(pair_rows) == len(set(pair_rows))\n    assert not set(pair_rows) & (set(indices) | proof_rows)\n    changed = set(pair_rows) | {i for i, t in items if t in removed}\n    for t in removed:\n        assert incidence.get(t, set()) <= changed\n    expected = {i: {} for i in changed}\n\n    # Every new coordinate is explicitly defined. Odd powers use the proved\n    # unit R; squares use a polynomial definition. No square root is chosen.\n    new_rows = []\n    odds = {}\n    squares = {}\n    def fresh(t):\n        nonlocal nextvar\n        assert type(t) is int and t == nextvar\n        nextvar += 1\n    for spec in d[\'new_variables\']:\n        kind = spec[\'kind\']; t = spec[\'variable\']; fresh(t)\n        if kind == \'odd_power\':\n            r, p = spec[\'factor\'], spec[\'even\']\n            R, P = old(r), old(p)\n            assert r in proofs and (r, p) not in odds\n            assert not {r, p} & removed\n            odds[r, p] = t\n            new_rows.append(add((1, mul(R, v(t))), (-1, P)))\n        else:\n            assert kind == \'square\'\n            B = dec(spec[\'base\'])\n            assert B and all(len(m) <= 1 for m in B)\n            assert all(i < old_limit for i in vs(B)) and not vs(B) & removed\n            squares[t] = B\n            new_rows.append(add((1, v(t)), (-1, mul(B, B))))\n    low = {}\n    for r, p, i in d[\'low_powers\']:\n        R, P = old(r), old(p)\n        assert r in proofs and (r, p) not in low and (r, p) not in odds\n        assert i not in changed and not {r, p} & removed\n        eq(i, add((1, P), (-1, mul(R, R))))\n        low[r, p] = r\n    used_odds = set(); used_squares = set(); used_proofs = set(); used_low = set()\n    for pair in d[\'pairs\']:\n        i, r, f, p, o, n, t, q = (pair[k] for k in\n            (\'row\', \'factor\', \'first\', \'even\', \'odd\', \'norm\', \'test\', \'square\'))\n        R, F, P, N, U = (old(j) for j in (r, f, p, n, t))\n        assert proofs.get(r) == f\n        assert o == (odds | low).get((r, p))\n        B = dec(pair[\'base\'])\n        assert B and all(len(m) <= 1 for m in B)\n        assert all(j < old_limit for j in vs(B))\n        assert q in squares and mul(B, B) == mul(squares[q], squares[q])\n        assert not (vs(B) | {r, f, p, n, t}) & (removed | target_set)\n        want = add((1, mul(P, N)), (-1, mul(mul(E, E), mul(B, B))),\n                   (-1, mul(R, mul(U, U))))\n        assert canon(expand(row(i), expanded)) == canon(want)\n        expected[i] = add((1, mul(v(o), N)), (-1, mul(F, v(q))),\n                          (1, v(q)), (-1, mul(U, U)))\n        used_proofs.add(r); used_squares.add(q)\n        (used_odds if (r, p) in odds else used_low).add((r, p))\n    assert used_proofs == proofs.keys()\n    assert used_odds == odds.keys() and used_low == low.keys()\n    assert used_squares == squares.keys()\n    for k, rr in enumerate(new_rows):\n        expected[len(rows)+k] = rr\n    assert not set(expected) & proof_rows\n    assert all(not vs(rr) & removed and all(len(m) <= 2 for m in rr)\n               for rr in expected.values())\n    return expected, nextvar\n\n\nif __name__ == \'__main__\':\n    import argparse\n    import gzip\n    import json\n    from pathlib import Path\n    parser = argparse.ArgumentParser(description=\'Check one batch-absorb event against its parent rows.\')\n    parser.add_argument(\'--parent\', type=Path, required=True)\n    parser.add_argument(\'--event\', type=Path, required=True)\n    args = parser.parse_args()\n    rr = [dec(x) for x in json.loads(gzip.decompress((args.parent/\'candidate-rows.json.gz\').read_bytes()))]\n    records = [json.loads(line) for line in gzip.decompress((args.parent/\'certificate.jsonl.gz\').read_bytes()).splitlines()]\n    limit = records[-1][\'allocated_variables\']\n    incidence = defaultdict(set)\n    for i, poly in enumerate(rr):\n        for t in vs(poly):\n            incidence[t].add(i)\n    event = json.loads(args.event.read_bytes())\n    assert event[\'kind\'] == \'batch_absorb\'\n    want, limit = batch_absorb_expected(rr, event[\'data\'], limit, incidence)\n    patches = {i: dec(poly) for i, poly in event[\'patches\']}\n    assert len(patches) == len(event[\'patches\']) and patches.keys() == want.keys()\n    assert all(canon(patches[i]) == canon(poly) for i, poly in want.items())\n    print(json.dumps({\'status\': \'PASS\', \'scope\': \'one exact event; parent certificate and final expansion not checked here\',\n                      \'pairs\': len(event[\'data\'][\'pairs\']), \'patches\': len(patches), \'allocated_variables\': limit}))\n','<embedded-batch>','exec'),_rules_batch)

def verify(root,write_report=True):
    start=time.monotonic();source_bytes=(root/'source-residuals.jsonl.gz').read_bytes()
    with gzip.open(root/'certificate.jsonl.gz','rt',encoding='ascii') as seed:
        first=json.loads(next(seed))
    source_id=first.get('source_id','original64')
    assert source_id in SOURCE_ENTRIES
    entry=SOURCE_ENTRIES[source_id]
    SOURCE_SHA=entry['source_sha256'];SOURCE_VARIABLES=entry['source_variables'];SOURCE_ROWS=entry['source_rows']
    if source_id!='original64':
        assert first['source_entry_sha256']==hashlib.sha256(canonical(entry)+b'\n').hexdigest()
        assert json.loads(gzip.decompress(source_bytes).splitlines()[0])==entry['source_header']
        assert hashlib.sha256(gzip.decompress(source_bytes)).hexdigest()==entry['uncompressed_sha256']
    assert hashlib.sha256(source_bytes).hexdigest()==SOURCE_SHA
    source=[decode(json.loads(line)) for line in gzip.decompress(source_bytes).splitlines()[1:]]
    assert len(source)==SOURCE_ROWS and set.union(*(variables(r) for r in source))==set(range(SOURCE_VARIABLES))
    counts=defaultdict(int)
    with gzip.open(root/'certificate.jsonl.gz','rt',encoding='ascii') as stream:
        initial=json.loads(next(stream));assert initial['kind']=='initial'
        assert initial['source_sha256']==SOURCE_SHA and initial['source_variables']==SOURCE_VARIABLES and initial['source_rows']==SOURCE_ROWS
        rows=[decode(r) for r in initial['rows']]
        rules={};anchors=set()
        for rule in initial['reuse']:
            pair=tuple(rule['product']);v=rule['variable'];scale=Fraction(*rule['scale']);index=rule['anchor']
            assert len(pair)==2 and pair==tuple(sorted(pair)) and pair not in rules and v not in pair and scale
            assert 0<=index<len(source) and 0<=v<SOURCE_VARIABLES
            assert normal(source[index])==normal({pair:1,(v,):-scale})
            rules[pair]=(v,scale);anchors.add(index)
        def reduce_anchor_terms(row):
            result={}
            for monomial,coefficient in row.items():
                current=list(monomial);coefficient=Fraction(coefficient)
                while True:
                    choices=sorted(set(itertools.combinations(current,2))&rules.keys())
                    if not choices:break
                    pair=choices[0];v,scale=rules[pair]
                    for w in pair:current.remove(w)
                    current.append(v);current.sort();coefficient*=scale
                key=tuple(current);result[key]=result.get(key,0)+coefficient
            return {m:c for m,c in result.items() if c}
        expanded_vars={v:(v,) for v in range(SOURCE_VARIABLES)};nextvar=SOURCE_VARIABLES
        gates=initial['gates'];assert len(rows)==SOURCE_ROWS+len(gates)
        for position,gate in enumerate(gates):
            v=gate['variable'];pair=tuple(gate['product'])
            assert v==nextvar and len(pair)==2 and all(w in expanded_vars for w in pair)
            expanded_vars[v]=tuple(sorted(expanded_vars[pair[0]]+expanded_vars[pair[1]]));nextvar+=1
            assert rows[SOURCE_ROWS+position]=={pair:-1,(v,):1}
        for i,original in enumerate(source):
            expanded=defaultdict(int)
            for monomial,coefficient in rows[i].items():
                assert all(v in expanded_vars for v in monomial)
                key=tuple(sorted(v for w in monomial for v in expanded_vars[w]));expanded[key]+=coefficient
            expanded={m:c for m,c in expanded.items() if c}
            if i in anchors:assert normal(expanded)==normal(original),('anchor',i)
            else:assert normal(reduce_anchor_terms(expanded))==normal(reduce_anchor_terms(original)),('source',i)
        assert all(len(m)<=2 for r in rows for m in r)
        incidence=defaultdict(set)
        for i,r in enumerate(rows):
            for v in variables(r):incidence[v].add(i)
        def fresh(v):
            nonlocal nextvar
            assert type(v) is int and v==nextvar;nextvar+=1
        def patch(data,expected):
            supplied={i:decode(r) for i,r in data}
            assert len(supplied)==len(data) and supplied.keys()==expected.keys()
            for i,r in supplied.items():
                assert normal(r)==normal(expected[i]),('incorrect row',i)
                assert all(len(m)<=2 for m in r) and all(v<nextvar for v in variables(r))
                assert 0<=i<=len(rows)
                if i==len(rows):rows.append({})
                for v in variables(rows[i]):incidence[v].remove(i)
                rows[i]=r
                for v in variables(r):incidence[v].add(i)
        final=None;weights=None;circuit_cache=set()
        for line in stream:
            event=json.loads(line);kind=event['kind']
            if kind=='final':
                assert final is None;final=event
                assert not stream.read().strip(),'Data after final record'
                break
            if kind=='weights':
                assert weights is None
                weights=event['values'];assert len(weights)==len(rows) and all(type(w) is int and w>0 for w in weights)
                continue
            assert weights is None,'Transformations after final weights are not supported'
            assert final is None
            d=event['data'];expected={};counts[kind]+=1
            if kind=='cse':
                v=d['variable'];fresh(v);definition=decode(d['definition']);assert v not in variables(definition)
                for i,factor in d['rows']:
                    assert 0<=i<len(rows) and i not in expected and type(factor) is int
                    expected[i]=add((1,rows[i]),(-factor,definition),(factor,{(v,):1}))
                expected[len(rows)]=add((1,definition),(-1,{(v,):1}))
            elif kind=='split':
                v=d['variable'];fresh(v);i=d['row'];assert 0<=i<len(rows)
                left=decode(d['left']);assert v not in variables(left)
                right=add((1,rows[i]),(-1,left))
                expected={i:add((1,left),(-1,{(v,):1})),len(rows):add((1,right),(1,{(v,):1}))}
            elif kind=='eliminate':
                i=d['row'];v=d['variable'];assert v!=0 and 0<=i<len(rows)
                replacement=decode(d['replacement']);assert v not in variables(replacement)
                denominator=d.get('denominator',1)
                assert type(denominator) is int and denominator>0
                replacement={m:Fraction(c,denominator) for m,c in replacement.items()}
                assert normal(rows[i])==normal(add((1,{(v,):1}),(-1,replacement)))
                affected=d['affected'];assert len(set(affected))==len(affected) and set(affected)==incidence[v]-{i}
                expected={j:substitute(rows[j],v,replacement) for j in affected};expected[i]={}
            elif kind=='linear':
                i,j=d['target'],d['other'];a,b=d['a'],d['b']
                assert 0<=i<len(rows) and 0<=j<len(rows) and i!=j and type(a) is int and a!=0 and type(b) is int
                expected={i:add((a,rows[i]),(b,rows[j]))}
            elif kind=='unit_scale':
                expected,nextvar=unit_scale_expected(rows,d,nextvar)
            elif kind=='redundant_inverse':
                expected=redundant_inverse_expected(rows,d,nextvar,incidence)
            elif kind=='gpoint_chart':
                expected,nextvar=_rules_chart['chart_expected'](rows,d,nextvar,incidence)
            elif kind=='field_ordinate':
                expected,nextvar=_rules_chart['ordinate_expected'](rows,d,nextvar,incidence)
            elif kind=='parity_conic':
                expected,nextvar=_rules_parity['check_rule'](rows,incidence,d,nextvar)
            elif kind=='batch_absorb':
                expected,nextvar=_rules_batch['batch_absorb_expected'](rows,d,nextvar,incidence)
            elif kind=='norm_inverse':
                i=d['row'];u=d['inverse'];definitions=d['definitions']
                assert type(i) is int and 0<=i<len(rows)
                assert type(u) is int and 0<u<nextvar
                indices=[pair[0] for pair in definitions];targets=[pair[1] for pair in definitions]
                assert definitions and len(indices)==len(set(indices)) and len(targets)==len(set(targets))
                assert i not in indices and u not in targets
                assert all(type(j) is int and 0<=j<len(rows) for j in indices)
                assert all(type(v) is int and 0<v<nextvar for v in targets)
                target_set=set(targets);expanded={}
                for j,v in definitions:
                    coefficient=rows[j].get((v,),0);assert coefficient
                    rhs=add((Fraction(-1,coefficient),rows[j]),(1,{(v,):1}))
                    assert v not in variables(rhs)
                    assert variables(rhs)&target_set<=expanded.keys(),'Non-acyclic norm-guard definitions'
                    expanded[v]=expand_definitions(rhs,expanded)
                removed={u}|{v for v in targets if u in variables(expanded[v])}
                assert len(d['removed'])==len(set(d['removed'])) and set(d['removed'])==removed
                changed={i}|{j for j,v in definitions if v in removed}
                assert len(changed)>=2
                for v in removed:assert incidence[v]<=changed,'Removed norm coordinate has outside uses'
                for j,v in definitions:
                    if v not in removed:assert not variables(rows[j])&removed
                components=d['components'];assert len(components)==2
                A,B=map(decode,components)
                for component in (A,B):
                    assert all(len(m)<=1 for m in component)
                    assert all(v<nextvar for v in variables(component))
                    assert not variables(component)&(target_set|{u})
                N=add((1,mul(A,A)),(-2,mul(B,B)))
                assert normal(expand_definitions(rows[i],expanded))==normal(add((1,mul({(u,):1},N)),(-1,{():1})))
                new=d['new_variables'];assert len(new)==2
                s,t=new;fresh(s);fresh(t)
                S,T={(s,):1},{(t,):1}
                real=add((1,mul(A,S)),(2,mul(B,T)))
                imag=add((1,mul(A,T)),(1,mul(B,S)))
                # Exact norm multiplicativity supplies the reverse solution map.
                assert mul(N,add((1,mul(S,S)),(-2,mul(T,T))))==add((1,mul(real,real)),(-2,mul(imag,imag)))
                second=min(changed-{i})
                expected={j:{} for j in changed}
                expected[i]=add((1,real),(-1,{():1}));expected[second]=imag
            elif kind=='circuit':
                old_ids=d['old_rows'];old_targets=d['old_targets'];outputs=d['outputs'];new_targets=d['new_targets']
                assert len(old_ids)==len(set(old_ids))==len(old_targets)==len(set(old_targets))
                assert all(type(i) is int and 0<=i<len(rows) for i in old_ids)
                assert all(type(v) is int and 0<v<nextvar for v in old_targets)
                assert outputs and len(outputs)==len(set(outputs)) and set(outputs)<=set(old_targets)
                assert all(type(v) is int for v in outputs+new_targets)
                assert 0<len(new_targets)<=len(old_ids) and len(new_targets)==len(set(new_targets))
                assert set(outputs)<=set(new_targets) and set(new_targets)&set(old_targets)==set(outputs)
                for v in set(old_targets)-set(outputs):
                    assert incidence[v]<=set(old_ids),'Removed circuit variable used outside selected rows'
                for v in new_targets:
                    if v not in outputs:fresh(v)
                supplied={i:decode(r) for i,r in event['patches']}
                assert len(supplied)==len(event['patches']) and set(supplied)==set(old_ids)
                assert all(not supplied[i] for i in old_ids[len(new_targets):])
                old_defs=[rows[i] for i in old_ids]
                new_defs=[supplied[i] for i in old_ids[:len(new_targets)]]
                external=set().union(*(variables(r) for r in old_defs))-set(old_targets)
                assert (set().union(*(variables(r) for r in new_defs))-set(new_targets))<=external
                ext=sorted(external)
                def normalized_circuit(defs,targets):
                    mapping={v:i for i,v in enumerate(ext+targets)}
                    assert len(mapping)==len(ext)+len(targets)
                    seen=set(ext);normalized=[]
                    for target,row in zip(targets,defs):
                        assert row.get((target,),0)!=0
                        assert all(target not in mon for mon in row if mon!=(target,))
                        assert variables(row)-{target}<=seen,'Circuit is cyclic or has a forward reference'
                        assert all(len(mon)<=2 for mon in row)
                        renamed={tuple(sorted(mapping[v] for v in mon)):c for mon,c in row.items()}
                        normalized.append((mapping[target],normal(renamed)))
                        seen.add(target)
                    return normalized,[mapping[v] for v in outputs]
                old_norm,old_outputs=normalized_circuit(old_defs,old_targets)
                new_norm,new_outputs=normalized_circuit(new_defs,new_targets)
                # The cache key is the complete normalized data, not a digest.
                cache_key=canonical([len(ext),old_norm,old_outputs,new_norm,new_outputs])
                if cache_key not in circuit_cache:
                    def evaluate(defs):
                        env={i:{(i,):Fraction(1)} for i in range(len(ext))}
                        for target,terms in defs:
                            row=dict(terms);leading=row[(target,)];value={}
                            for mon,c in terms:
                                if mon==(target,):continue
                                term={():Fraction(-c,leading)}
                                for v in mon:term=mul(term,env[v])
                                value=add((1,value),(1,term))
                            env[target]=value
                        return env
                    old_values=evaluate(old_norm);new_values=evaluate(new_norm)
                    assert all(old_values[a]==new_values[b] for a,b in zip(old_outputs,new_outputs)),'Circuit outputs differ'
                    circuit_cache.add(cache_key)
                expected=supplied
            elif kind in ('translate','shear'):
                v=d['variable'];assert 0<v<nextvar
                affected=d['affected'];assert len(set(affected))==len(affected) and set(affected)==incidence[v]
                if kind=='translate':replacement={(v,):1,():Fraction(*d['shift'])}
                else:
                    w=d['other'];assert 0<=w<nextvar and w!=v
                    replacement={(v,):1,(w,):Fraction(*d['scalar'])}
                expected={i:substitute(rows[i],v,replacement) for i in affected}
            else:raise AssertionError(('unknown operation',kind))
            patch(event['patches'],expected)
        assert final is not None and final['allocated_variables']==nextvar
        if weights is None:weights=[1]*len(rows)
        assert hashlib.sha256(canonical([encode(r) for r in rows])).hexdigest()==final['rows_sha256']
    saved=[decode(r) for r in json.loads(gzip.decompress((root/'candidate-rows.json.gz').read_bytes()))];assert saved==rows
    active=json.loads((root/'variable-map.json').read_bytes())
    assert active[0]==0 and len(active)==len(set(active))
    assert set(active)=={v for v,indices in incidence.items() if indices}
    mapping={v:i for i,v in enumerate(active)}
    compact=[{tuple(sorted(mapping[v] for v in m)):coefficient for m,coefficient in r.items()} for r in rows if r]
    assert compact==[decode(r) for r in json.loads(gzip.decompress((root/'residuals.json.gz').read_bytes()))]
    compact_weights=[w for r,w in zip(rows,weights) if r]
    if (root/'weights.json').exists():assert json.loads((root/'weights.json').read_bytes())==compact_weights
    else:assert all(w==1 for w in compact_weights)
    # All ordered products, independent of the producer's triangular expansion.
    polynomial=defaultdict(int)
    for row,weight in zip(compact,compact_weights):
        for m,coefficient in row.items():
            for n,other in row.items():polynomial[tuple(sorted(m+n))]+=weight*coefficient*other
    polynomial={m:c for m,c in polynomial.items() if c}
    expanded_bytes=(root/'polynomial.expanded.txt').read_bytes()
    assert gzip.decompress((root/'polynomial.expanded.txt.gz').read_bytes())==expanded_bytes
    supplied={}
    for line in expanded_bytes.decode('ascii').splitlines():
        if line.startswith('#'):continue
        coefficient,*m=map(int,line.split());m=tuple(m)
        assert coefficient and m not in supplied and m==tuple(sorted(m));supplied[m]=coefficient
    assert polynomial==supplied
    degree=max(map(len,polynomial));maximum=max(map(abs,polynomial.values()))
    assert degree==4 and set.union(*(set(m) for m in polynomial))==set(range(len(active)))
    assert maximum<2**80,'Expanded coefficient reaches the strict 2^80 bound'
    stats={'witnesses':len(active)-1,'variables':len(active),'rows':len(compact),'monomials':len(polynomial),'degree':degree,'max_abs_coefficient':maximum}
    for key in ('variables','witnesses','rows','monomials','degree','max_abs_coefficient'):assert stats[key]==final['report'][key],key
    report={'status':'PASS','scope':'Exact projection-preserving algebraic equivalence to the pinned source system; exact full integer expansion. The source arithmetic theorem is not checked here.',
            **stats,'source_id':source_id,'source_sha256':SOURCE_SHA,'operations':dict(counts),'total_operations':sum(counts.values()),'weights_greater_than_one':sum(w>1 for w in compact_weights),
            'expanded_bytes':len(expanded_bytes),'compressed_bytes':(root/'polynomial.expanded.txt.gz').stat().st_size,
            'expanded_sha256':hashlib.sha256(expanded_bytes).hexdigest(),
            'certificate_sha256':hashlib.sha256((root/'certificate.jsonl.gz').read_bytes()).hexdigest(),
            'distinct_circuit_identities_checked':len(circuit_cache),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':round(time.monotonic()-start,3)}
    if write_report:(root/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path);arguments=parser.parse_args()
    print(json.dumps(verify(arguments.directory),indent=2))
