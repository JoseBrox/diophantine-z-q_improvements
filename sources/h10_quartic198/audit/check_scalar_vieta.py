from pathlib import Path
import json
import sympy as s
u,v,w,m,k,p,D=s.symbols('u v w m k p D')
r=[p-u*v,k*k-p*w,u+v+w+2*m+D*k*k,p+w*(u+v)-m*m]
g=s.groebner(r,p,m,u,v,w,k,D,order='grevlex')
checks={}
for name,a in [('u',u),('v',v),('w',w)]:
 expr=s.expand(a*(m+a)**2+D*k*k*a*a-k*k)
 checks[name+'_curve_identity']=s.expand(g.reduce(expr)[1])==0
checks['nonzero_product']=s.expand(g.reduce(u*v*w-k*k)[1])==0
assert all(checks.values())
out={'status':'PASS','checks':checks,'scope':'Polynomial ideal identities only; nonzero guard, point-group law, height and completeness arguments are separate.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
