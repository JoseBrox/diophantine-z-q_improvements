#!/usr/bin/env python3
"""Independent universal algebra audit of the four-coordinate cover."""
from pathlib import Path
import json
import argparse
import sympy as p


def main():
    e,c=p.symbols("e c",nonzero=True)
    a=e**2
    D=a*(a-c**2)
    r,u,z=p.symbols("r u z")
    R,Q,s,t=p.symbols("R Q s t")
    field=p.QQ.frac_field(e,c)
    src=[z-r*u,a*(r*r+u*u)+2*c*e*z+D*z*z-1]
    dst=[s*s+D*R*R-1,t*t+D*Q*Q-1,
         c*e*s*t+a-D*(R+Q)-a*D*R*Q]
    forward={R:r*r,Q:u*u,
             s:e*u+c*r+(D/e)*r*z,
             t:-e*r-c*u-(D/e)*u*z}
    reverse={r:-(t/e+e*R*t+c*Q*s)/2,
             u:(s/e+c*R*t+e*Q*s)/2,
             z:(1-a*(R+Q)-D*R*Q)/(2*c*e)}
    gs=p.groebner(src,z,u,r,order="grlex",domain=field)
    gd=p.groebner(dst,R,Q,s,t,order="grlex",domain=field)
    denominators=set()
    checks=[]

    def denominator_check(expression,variables):
        poly=p.Poly(expression,*variables,domain=field)
        for coefficient in poly.coeffs():
            den=p.factor(p.denom(p.cancel(coefficient)))
            if den!=1:denominators.add(str(den))

    def certify_basis(original,basis,variables):
        # Track ideal membership throughout a separate Buchberger run.
        # Merely inspecting the final basis coefficients would not prove
        # that no hidden parameter denominator occurred in its derivation.
        polys=[]
        provenance=[]
        def leading(expression):
            pp=p.Poly(expression,*variables,domain=field)
            mon=pp.monoms(order="grlex")[0]
            return mon,pp.coeff_monomial(mon)
        def mono(exponents):
            return p.prod(v**a for v,a in zip(variables,exponents))
        for index,expression in enumerate(original):
            _,lc=leading(expression)
            polys.append(p.expand(expression/lc))
            provenance.append([1/lc if j==index else p.Integer(0)
                               for j in range(len(original))])
        pending=[(i,j) for i in range(len(polys)) for j in range(i)]
        while pending:
            i,j=pending.pop(0)
            mi,li=leading(polys[i]);mj,lj=leading(polys[j])
            lcm=tuple(max(a,b) for a,b in zip(mi,mj))
            ui=mono(tuple(a-b for a,b in zip(lcm,mi)))/li
            uj=mono(tuple(a-b for a,b in zip(lcm,mj)))/lj
            ss=p.expand(ui*polys[i]-uj*polys[j])
            quotients,rem=p.reduced(ss,polys,*variables,
                                   order="grlex",domain=field)
            if rem==0:continue
            _,lc=leading(rem)
            vector=[]
            for index in range(len(original)):
                raw=ui*provenance[i][index]-uj*provenance[j][index]
                raw-=sum(q*v[index] for q,v in zip(quotients,provenance))
                vector.append(p.cancel(raw/lc))
            new=p.expand(rem/lc)
            assert p.cancel(new-sum(v*f for v,f in zip(vector,original)))==0
            new_index=len(polys)
            polys.append(new);provenance.append(vector)
            pending.extend((new_index,j) for j in range(new_index))
        for polynomial in basis.polys:
            quotients,rem=p.reduced(polynomial.as_expr(),polys,*variables,
                                   order="grlex",domain=field)
            assert rem==0
            vector=[p.cancel(sum(q*v[i] for q,v in zip(quotients,provenance)))
                    for i in range(len(original))]
            assert p.cancel(polynomial.as_expr()
                            -sum(v*f for v,f in zip(vector,original)))==0
            for coefficient in vector:
                denominator_check(coefficient,variables)
        return len(polys)

    def reduce(label,expression,basis,variables):
        quotients,remainder=basis.reduce(p.expand(expression))
        assert remainder==0,label
        for quotient in quotients:denominator_check(quotient,variables)
        checks.append(label)

    for i,equation in enumerate(dst):
        reduce("forward equation "+str(i),equation.xreplace(forward),gs,(z,u,r))
    for i,equation in enumerate(src):
        reduce("inverse equation "+str(i),equation.xreplace(reverse),gd,(R,Q,s,t))
    for variable in (R,Q,s,t):
        reduce("forward inverse "+str(variable),
               forward[variable].xreplace(reverse)-variable,gd,(R,Q,s,t))
    for variable in (r,u,z):
        reduce("inverse forward "+str(variable),
               reverse[variable].xreplace(forward)-variable,gs,(z,u,r))
    for g in gs.polys:denominator_check(g.as_expr(),(z,u,r))
    for g in gd.polys:denominator_check(g.as_expr(),(R,Q,s,t))
    source_provenance_size=certify_basis(src,gs,(z,u,r))
    target_provenance_size=certify_basis(dst,gd,(R,Q,s,t))
    checks.append("original-ideal provenance with controlled denominators")

    # At R=0, square the third equation and use the two conic equations.
    # The resulting scalar identity is D*(a*Q-1)^2=0. The squared
    # conclusion is sufficient over fields; no reduced scheme claim is made.
    first=s*s-1
    second=t*t+D*Q*Q-1
    third=c*e*s*t+a-D*Q
    identity=(
        (a-D*Q)**2-c*c*e*e*(1-D*Q*Q)
        -D*(a*Q-1)**2)
    assert p.expand(identity)==0
    checks.append("R-zero boundary square identity")
    boundary=[
        {R:0,Q:1/a,s:1,t:-c/e},
        {R:0,Q:1/a,s:-1,t:c/e},
        {R:1/a,Q:0,s:c/e,t:-1},
        {R:1/a,Q:0,s:-c/e,t:1},
    ]
    for point in boundary:
        assert all(p.cancel(q.xreplace(point))==0 for q in dst)
    checks.append("four exact boundary points")

    # Every denominator factor must be excluded by the stated ecD!=0.
    exceptional=p.Poly(e*c*(e-c)*(e+c),e,c)
    extra=[]
    for denominator in denominators:
        den=p.sympify(denominator)
        for factor,exponent in p.factor_list(den,e,c)[1]:
            ff=p.Poly(factor,e,c)
            if exceptional.rem(ff)!=0:extra.append(str(factor))
    assert not extra,extra
    report={
        "status":"PASS_UNIVERSAL_COVER_IDENTITIES",
        "checks":checks,
        "sourceGroebnerBasisSize":len(gs.polys),
        "targetGroebnerBasisSize":len(gd.polys),
        "sourceTrackedBuchbergerBasisSize":source_provenance_size,
        "targetTrackedBuchbergerBasisSize":target_provenance_size,
        "certificateDenominators":sorted(denominators),
        "additionalParameterExceptions":[],
        "parameterScope":"Characteristic zero, e*c*D !=0, with a=e²,D=a(a-c²).",
        "scope":"Exact cover isomorphism, constant-denominator inverse and field-valued boundary points. No paired-point/height conversion or smaller full quartic count.",
    }
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    encoded=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(encoded)
    print(encoded,end="")


if __name__=="__main__":
    main()
