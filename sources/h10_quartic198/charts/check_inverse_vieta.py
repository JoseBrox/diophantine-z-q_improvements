#!/usr/bin/env python3
"""Exact polynomial identities; complements the written geometric proof."""
import sympy as s,json
from pathlib import Path
U,V,W,M,r,P,R,D=s.symbols('U V W M r P R D')
rows=[U*V-R**2*P,P*W-r,r*(U+V+W+2*M)+D*R**2,R**2*P+W*(U+V)-M**2]
G=s.groebner(rows,U,V,W,M,r,P,R,D)
tests={
'sum_roots':V*W+U*W+P*R**2-M**2,
'pair_products':U*V*W*(U+V+W)+D*R**4+2*M*r*R**2,
'product_roots':U*V*P*W**2-R**2*r**2,
'curve_U':(M+U)**2*V*W-(V*W)**2+D*R**4,
'curve_V':(M+V)**2*U*W-(U*W)**2+D*R**4,
'curve_Q':(M+W)**2*P-P**2*R**2+D*R**2,
'reciprocal_U':r*R**2-U*V*W,
}
res={name:str(G.reduce(expr)[1]) for name,expr in tests.items()}
print(res)
assert set(res.values())=={'0'}
Path(__file__).with_name('inverse_vieta_identity_check.json').write_text(json.dumps(res,indent=2)+'\n')
