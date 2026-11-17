#!/usr/bin/env python3
"""Rebuild the halfpoint and physical-curve certificates without producer imports."""
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from math import gcd,lcm
from pathlib import Path
import argparse,json
import sympy as s

HERE=Path(__file__).resolve().parent

def unpack(v,x,p=None):
    return s.Poly.from_list([int(a) for a in reversed(v)],x,modulus=p) if p else s.Poly.from_list([int(a) for a in reversed(v)],x,domain=s.ZZ)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--contacts',type=int,choices=[7,9],default=7)
    args=ap.parse_args();contacts=args.contacts
    certificate=HERE/('certificate.json' if contacts==7 else 'nine_contact_certificate.json')
    data=json.loads(certificate.read_text());u,t,r=s.symbols('u t r')
    assert data['contact_count']==contacts
    # An independent quadratic-field reduction through Q[r]/(r^2-2).
    def field(expr):
        expr=s.cancel(expr)
        a,b=s.fraction(expr)
        aa=s.rem(s.Poly(a,r,domain=s.QQ),s.Poly(r*r-2,r,domain=s.QQ))
        bb=s.rem(s.Poly(b,r,domain=s.QQ),s.Poly(r*r-2,r,domain=s.QQ))
        return s.rem(aa*s.invert(bb,s.Poly(r*r-2,r)),s.Poly(r*r-2,r)).as_expr()
    d=11-6*r;x=1+r;y=2*r
    assert field(y*y-x*x*x+d*x)==0
    slope=field((3*x*x-d)/(2*y));xx=field(slope*slope-2*x);yy=field(slope*(x-xx)-y)
    assert xx==s.Rational(57,8)-s.Rational(7,2)*r
    assert yy==-s.Rational(165,8)+s.Rational(417,32)*r
    assert field(1/x)==r-1
    alpha=r-1
    L=u*(1+u*alpha)**2+alpha**2
    Lbar=L.subs(r,-r)
    normL=s.rem(s.Poly(s.expand(L*Lbar),r),s.Poly(r*r-2,r)).as_expr()
    denominator=s.expand(u*u*(1-2*u-u*u)**2)
    R=s.Poly(normL,u);D=s.Poly(denominator,u)
    Pi=4*D**4*s.Poly((1+u)**2,u)+2*s.Poly(u,u)*R**2*(R**2-D**2)
    stored=data['ascending_integer_coefficients']
    assert R==unpack(stored['R'],u) and D==unpack(stored['D'],u) and Pi==unpack(stored['Pi'],u)
    assert R.degree()==D.degree()==6 and Pi.degree()==26
    assert s.gcd(R,D).degree()==0 and s.gcd(Pi,Pi.diff()).degree()==0
    scale=(s.Rational(4)**4+s.Rational(57,4)**4)**(8 if contacts==7 else 4)
    assert str(scale)==data['scale']
    # Differentiate before specializing scale, unlike the producer's factor loop.
    a=s.symbols('a')
    shifts=([-7,-6,-4,1,3,5,8] if contacts==7 else [-10,-8,-5,1,2,3,4,6,7])
    unspecialized=s.prod((a+c)**2-t for c in shifts)
    polA=s.Poly((-2*contacts*unspecialized).subs(a,scale),t)
    polB=s.Poly(s.diff(unspecialized,a).subs(a,scale),t)
    common=lcm(*(int(c.q) for pp in [polA,polB] for c in pp.all_coeffs()))
    polA=s.Poly(polA.as_expr()*common,t,domain=s.ZZ);polB=s.Poly(polB.as_expr()*common,t,domain=s.ZZ)
    content=reduce(gcd,[abs(int(c)) for pp in [polA,polB] for c in pp.all_coeffs()])
    polA=polA.exquo_ground(content);polB=polB.exquo_ground(content)
    assert polA==unpack(stored['physical_A'],t) and polB==unpack(stored['physical_B'],t)
    assert (polA.degree(),polB.degree())==(contacts,contacts-1)
    verified=[]
    for record in data['finite_field_certificates']:
        p=record['prime'];x=u if record['name']=='weight' else t
        f=unpack(record['coefficients'],x,p)
        e=unpack(record['bezout_polynomial'],x,p);g=unpack(record['bezout_derivative'],x,p)
        assert e*f+g*f.diff()==s.Poly(1,x,modulus=p)
        if record['name']=='weight':
            assert f==s.Poly(Pi.as_expr(),u,modulus=p)
        else:
            am=s.Poly(polA.as_expr(),t,modulus=p);bm=s.Poly(polB.as_expr(),t,modulus=p)
            assert am.degree()==contacts and bm.degree()==contacts-1 and s.gcd(am,bm).degree()==0
            result=s.Poly(0,t,modulus=p);bp=s.Poly(1,t,modulus=p)
            for j,c in enumerate(Pi.all_coeffs()):
                result=result*am+int(c)*bp
                bp*=bm
            assert result==f and f.degree()==26*contacts and f.eval(0)!=0
        assert f.degree()==record['degree']
        verified.append(dict(name=record['name'],prime=p,degree=f.degree()))
    report=dict(status='PASS',producer_certificate_sha256=sha256(certificate.read_bytes()).hexdigest(),
        reconstructed_coefficients=['D','R','Pi','physical_A','physical_B'],
        independent_quadratic_field_point_check=True,finite_field_bezout_checks=verified,
        genera={'weight':12,'squared_slope':13*contacts-1,'twisted_squared_slope':13*contacts,'slope':26*contacts-1},
        rational_witness_proved=False)
    (HERE/('independent_certificate.json' if contacts==7 else 'nine_contact_independent_certificate.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
