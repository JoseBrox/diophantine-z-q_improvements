#!/usr/bin/env python3
"""Independent exact row, recovery-identity and census checks for scalar sharing."""
from pathlib import Path
import hashlib
import json
import sys
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'undecidability/code'))
from build_scalar_rechart import build

theta = s.Symbol('theta')


def components(e):
    p = s.Poly(s.expand(e), theta)
    r = s.rem(p, s.Poly(theta**2-2, theta)).as_expr().expand()
    return r.coeff(theta, 0), r.coeff(theta, 1)


def identities():
    U,V,W,S,D,R,L,K,p,r,r2,Z = s.symbols('U V W S D R L K p r r2 Z')
    M = -2*S-W
    scalar = R*L-K
    zsquare = K-Z**2
    product = U*V-K*p
    rr = p*W-r
    total = r*(U+V-W-4*S)+D*K
    pair = U*V+W*(U+V)-M**2
    square = r2-r**2
    assertions = [
        (R*L-Z**2, scalar+zsquare),
        (U*V-L*(R*p), product-p*scalar),
        ((R*p)*W-R*r, R*rr),
        (r*(U+V-W-4*S)+D*R*L, total+D*scalar),
        ((R*r)*(U+V-W-4*S)+D*R**2*L, R*(total+D*scalar)),
        (L*R*p+W*(U+V)-M**2, pair-product+p*scalar),
        (R**2*r2-(R*r)**2, R**2*square),
    ]
    assert all(s.expand(a-b) == 0 for a,b in assertions)
    return len(assertions)


def check(m, N, rowcount):
    folder = ROOT/'undecidability/coefficients/jones1980_scalar_rechart'
    path = folder/f'scalar_rechart_m{m}_quadrics.json'
    raw = path.read_bytes()
    new = json.loads(raw)
    cert = json.loads((folder/f'scalar_rechart_m{m}_certificate.json').read_text())
    predecessor = ROOT/f'undecidability/coefficients/jones1980_global_gauge/global_gauge_m{m}_quadrics.json'
    oldraw = predecessor.read_bytes()
    old = json.loads(oldraw)
    assert cert['table_sha256'] == hashlib.sha256(raw).hexdigest()
    assert cert['predecessor_sha256'] == new['scalar_rechart_predecessor_sha256'] == hashlib.sha256(oldraw).hexdigest()
    assert raw == (json.dumps(build(m), sort_keys=True, separators=(',',':'))+'\n').encode()
    assert new['variables'] == cert['variables'] == N
    assert len(new['residuals']) == cert['quadratic_rows'] == rowcount
    for d in (new,cert):
        assert d['source_universality_hypothesis'] == 'U_em'
        assert d['source_universality_verified'] is False
        assert d['unconditional_undecidability_claim'] is False
    assert cert['pell_core_reduction_already_included'] is False
    assert new['scalar_rechart_pell_core_applied'] is False
    assert cert['new_abc_assumption'] is False
    names = new['variable_names']
    oldnames = old['variable_names']
    assert len(names) == len(set(names)) == N
    parameters = set(map(s.Symbol, new['parameters']))
    support = set()
    for row in new['residuals']:
        for t in row['terms']:
            assert len(t['monomial']) <= 2
            support.update(t['monomial'])
            a = s.sympify(t['coefficient'])
            assert a.free_symbols <= parameters
            assert s.Poly(a, *parameters).domain.is_ZZ
    assert support == set(range(1,N+1))

    maps = json.loads((ROOT/f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
    labels = {int(k):v for k,v in maps['source_labels'].items()}
    blocks = old['ordinary_integer_inputs']+['i_reciprocal']
    def z(b,j):
        n=f'int_{b}_{labels[j]}'
        return s.Symbol(n if n in oldnames else f'int_b_{labels[j]}')
    def field(b,j):
        return z(b,j)+theta*z(b,j+1)
    def expr(row,ns):
        return s.expand(sum(s.sympify(t['coefficient'])*s.prod(s.Symbol(ns[j-1])for j in t['monomial'])for t in row['terms']))
    oldrows = {r['name']:expr(r,oldnames)for r in old['residuals']}
    newrows = {r['name']:expr(r,names)for r in new['residuals']}
    assert len(oldrows)==len(old['residuals']) and len(newrows)==rowcount
    p = s.Symbol('common_scalar_x_real')+theta*s.Symbol('common_scalar_x_imag')
    K = s.Symbol('common_scalar_Z_square_real')+theta*s.Symbol('common_scalar_Z_square_imag')
    r = (s.Symbol('common_scalar_r_real')+theta*s.Symbol('common_scalar_r_imag')
         if m==163 else field('b',190))
    U,V,W,Z,S=(field('b',j)for j in(182,184,186,102,17))
    M=-2*S-W
    D=11-6*theta
    f2=z('b',64)+2*theta*z('b',65)
    r2=field('b',194)*(z('b',400)if m==179 else 1)
    common={
        'Z_square':K-Z**2, 'product':U*V-K*p, 'r':p*W-r,
        'sum':r*(U+V-W-4*S)+D*K,
        'pair':U*V+W*(U+V)-M**2, 'r_square':r2-r**2,
    }
    expected=dict(oldrows)
    deleted_rows=set()
    changed_rows=set()
    for b in blocks:
        tag='i' if b=='i_reciprocal'else b
        prefix=f'integer.{tag}.'
        R=z(b,113)
        assert s.expand(oldrows[prefix+'unit.R_square']-(z(b,112)-R**2))==0
        L=field(b,109)-f2
        P=field(b,192)
        rr=field(b,190)
        old_eqs={
            'product':U*V-L*P,
            'r':P*W-(rr if m==163 else R*rr),
            'sum':rr*(U+V-W-4*S)+D*(z(b,112) if m==163 else R)*L,
            'pair':L*P+W*(U+V)-M**2,
            'r2':z(b,112)*r2-rr**2 if m==163 else r2-rr**2,
        }
        for stem,e in old_eqs.items():
            for j,c in enumerate(components(e)):
                n=prefix+f'v82.point.{stem}.{j}'
                if n not in oldrows:
                    assert m==179 and stem=='r2' and b!='b'
                    continue
                assert s.expand(oldrows[n]-c)==0,(m,n)
                del expected[n]
                deleted_rows.add(n)
        for j,c in enumerate(components(R*L-K)):
            n=prefix+f'v82.scalar.field.{j}'
            assert s.expand(oldrows[n]-components(R*L-Z**2)[j])==0
            expected[n]=c
            changed_rows.add(n)
        for stem,component in [('new.aggregate',0)]+([('new.aggregate_shift',1)]if m==179 else[]):
            n=prefix+stem
            oldterm=z(b,192+component)*(z(b,114)if m==179 else 1)
            newterm=components(p)[component]*(R if m==163 else 1)
            expected[n]=s.expand(oldrows[n]-oldterm+newterm)
            changed_rows.add(n)
        if m==179:
            inverse=prefix+'unit.R_inverse'
            assert s.expand(oldrows[inverse]-(R*z(b,114)-1))==0
            del expected[inverse]
            deleted_rows.add(inverse)
            pole_ids=[11,12,13,14,104,105,106,107,108]
            back={z(b,j):z(b,j)/R for j in pole_ids}
            back[z(b,114)]=1/R
            native_stems=('inverse','input','p2','q2','first','middle','second')
            for stem in native_stems:
                n=prefix+'v82.scalar.'+stem
                if stem=='inverse':
                    expected[n]=z(b,111)*z(b,104)-z(b,112)**2
                elif stem=='input':
                    expected[n]=z(b,104)*z(b,105)-z(b,112)-9792*R
                # These are exact homogeneous coordinate substitutions after
                # the retained guard R2=R^2, never division by a pole witness.
                factor=R if stem=='inverse'else R**2
                diff=(factor*oldrows[n].subs(back,simultaneous=True)-expected[n]).subs(z(b,112),R**2)
                assert s.cancel(diff)==0,(m,n)
                changed_rows.add(n)
            assert new['scalar_rechart_native_pole_sources_reweighted']==pole_ids
            native=set(map(str,[z(b,j)for j in pole_ids]))
            for n,e in oldrows.items():
                if native & set(map(str,e.free_symbols)):
                    assert n in {prefix+'v82.scalar.'+stem for stem in native_stems}
    for n,e in common.items():
        for j,c in enumerate(components(e)):
            expected[f'scalar_common.{n}.{j}']=c
    assert set(expected)==set(newrows)
    assert all(s.expand(e-newrows[n])==0 for n,e in expected.items())
    assert deleted_rows==set(new['scalar_rechart_removed_rows'])
    assert changed_rows==set(new['scalar_rechart_modified_rows'])
    gone={str(z(b,j))for b in blocks for j in([190,191,192,193]if m==163 else[192,193,114])}
    assert gone==set(new['scalar_rechart_removed_coordinates'])
    assert set(oldnames)-set(names)==gone
    assert set(names)-set(oldnames)==set(new['scalar_rechart_added_coordinates'])
    assert len(gone)==cert['coordinates_removed']==(48 if m==163 else 36)
    assert len(new['scalar_rechart_added_coordinates'])==cert['coordinates_added']==(6 if m==163 else 4)
    return {'interface':m,'variables':N,'quadratic_rows':rowcount,
            'every_row_reconstructed':True,'table_sha256':cert['table_sha256'],
            'universality_verified':False}


if __name__=='__main__':
    print(json.dumps({'status':'PASS','polynomial_recovery_identities':identities(),
                      'systems':[check(163,1143,987),check(179,1323,1143)]},indent=2))
