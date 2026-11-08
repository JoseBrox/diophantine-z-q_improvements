"""Exact independent certificates for finite-field scalar normalization.

No huge fixed coefficients are expanded. All modular certificates have
degree at most twenty; direct residue enumeration is a separate check.
"""
from pathlib import Path
from math import isqrt
import json

p = 76249
assert all(p % d for d in range(2, isqrt(p)+1))

def trim(a):
    a = [c % p for c in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    return trim(c)

def neg(a): return trim([-x for x in a])
def sub(a,b): return add(a,neg(b))

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)

def divmod_poly(a,b):
    a,b=trim(a),trim(b)
    assert b != [0]
    q=[0]*max(1,len(a)-len(b)+1)
    inv=pow(b[-1],-1,p)
    while a != [0] and len(a)>=len(b):
        k=len(a)-len(b); c=a[-1]*inv%p
        q[k]=c
        for j,v in enumerate(b): a[k+j]=(a[k+j]-c*v)%p
        a=trim(a)
    return trim(q),a

def modpow(a,n,f):
    out=[1]
    while n:
        if n&1: out=divmod_poly(mul(out,a),f)[1]
        a=divmod_poly(mul(a,a),f)[1]
        n//=2
    return out

def egcd(a,b):
    r0,r1=a,b; s0,s1=[1],[0]; t0,t1=[0],[1]
    while r1 != [0]:
        q,r2=divmod_poly(r0,r1)
        r0,r1=r1,r2
        s0,s1=s1,sub(s0,mul(q,s1))
        t0,t1=t1,sub(t0,mul(q,t1))
    inv=pow(r0[-1],-1,p)
    return (mul(r0,[inv]),mul(s0,[inv]),mul(t0,[inv]))

beta=[450459,0,0,0,216]
polyr=[1]
for factor in [beta,sub(beta,[1]),sub(beta,[2401]),
               add(mul([32],beta),[343]),sub(mul([2],beta),[1])]:
    polyr=mul(polyr,factor)
f=add([1],mul([17],polyr))
remainder=sub(modpow([0,1],p,f),[0,1])
gcd,bezout_f,bezout_remainder=egcd(f,remainder)
assert gcd==[1]
assert add(mul(bezout_f,f),mul(bezout_remainder,remainder))==[1]
f0=f[0::4]
g0=remainder[1::4]
a0=bezout_f[0::4]
b0=bezout_remainder[3::4]
assert sub(modpow([0,1],(p-1)//4,f0),[1])==g0
assert add(mul(a0,f0),mul([0,1],mul(b0,g0)))==[1]

def eval_r(x):
    b=(216*pow(x,4,p)+450459)%p
    return b*(b-1)*(b-2401)*(32*b+343)*(2*b-1)%p

image={eval_r(x) for x in range(p)}
assert 0 not in image and (-pow(17,-1,p))%p not in image
fourths={pow(x,4,p) for x in range(p)}
assert len(fourths)==19063 and len(image)==16859
thetas=[0,1,2401,(-343*pow(32,-1,p))%p,pow(2,-1,p)]
quartic_residues=[((t-450459)*pow(216,-1,p))%p for t in thetas]
quartic_tests=[pow(t,(p-1)//4,p) for t in quartic_residues]
assert quartic_residues==[32862,32509,24048,904,70810]
assert quartic_tests==[76248,76248,76248,76248,40177]

b0=450459
r0=b0*(b0-1)*(b0-2401)*(32*b0+343)*(2*b0-1)
assert r0==1180712527837405404989927078052
assert 36*p**7<676**2*r0
assert 36*p**7>=675**2*r0
assert p%8==1 and p%3==1 and p%17==4

report={
    'status':'PASS',
    'prime':p,
    'prime_test':'Trial division by all integers 2 through floor(sqrt(p))',
    'numerator_prime_exponent':137731,
    'denominator_coefficient_expression':'17*(676*76249^68862+1)',
    'numerator_degree':20,
    'denominator_degree':40,
    'minimum_scalar_valuation':137731,
    'valuation_formula_integral_input':137731,
    'valuation_formula_negative_input':'137731 - 20*v_ell(X)',
    'r0':r0,
    'real_bound_lhs':36*p**7,
    'real_bound_rhs':676**2*r0,
    'fourth_power_image_size':len(fourths),
    'contact_image_size':len(image),
    'forbidden_residue':(-pow(17,-1,p))%p,
    'contact_no_root_quartic_residues':quartic_residues,
    'contact_no_root_quartic_tests':quartic_tests,
    'modular_certificate':{
        'coefficient_order':'ascending powers of X; coefficients in F_p',
        'F_equals_1_plus_17r':f,
        'G_equals_remainder_of_Xp_minus_X_mod_F':remainder,
        'A':bezout_f,
        'B':bezout_remainder,
        'identity':'A*F + B*G = 1 in F_p[X]',
        'independent_check':'Exhaustive enumeration of all 76249 residues',
        'compact_certificate':{
            'variable':'U=X^4',
            'F0':f0,'G0':g0,'A0':a0,'B0':b0,
            'power_remainder':'U^19062-1 = G0 mod F0',
            'identity':'A0*F0+U*B0*G0=1 in F_p[U]',
        },
    },
    'scope':'Scalar replacement is proved. The existing rational-source arithmetic premises remain unchanged. No variable reduction is claimed.'
}
target=Path(__file__).with_name('scalar-normalization-certificate.json')
target.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='modular_certificate'},indent=2))
