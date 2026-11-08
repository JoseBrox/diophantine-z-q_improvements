#!/usr/bin/env python3
"""Check the actual affine coordinate dictionary of all three height detectors.

This program uses only Fraction arithmetic and the emitted quadratic residuals.
It checks complete polynomial identities, not numerical samples or gate names.
"""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent

def c(n):return {} if not n else {():Fraction(n)}
def v(i):return {(i,):Fraction(1)}
def add(*terms):
    out=defaultdict(Fraction)
    for p in terms:
        for m,a in p.items():out[m]+=a
    return {m:a for m,a in out.items() if a}
def scale(p,n):return {m:a*n for m,a in p.items() if a*n}
def mul(p,q):
    out=defaultdict(Fraction)
    for m,a in p.items():
        for n,b in q.items():out[tuple(sorted(m+n))]+=a*b
    return {m:a for m,a in out.items() if a}
def power(p,n):
    out=c(1)
    for _ in range(n):out=mul(out,p)
    return out
def fieldmul(p,q):
    return (add(mul(p[0],q[0]),scale(mul(p[1],q[1]),2)),
            add(mul(p[0],q[1]),mul(p[1],q[0])))

def main():
    raw=(HERE/'final389/quadratic-system389.json').read_bytes()
    ir=json.loads(raw)
    sid={x['id']:x['sourceId'] for x in ir['coordinates']}
    rows={r['sourceId']:[(Fraction(t['coefficient']),tuple(sid[j] for j in t['monomial']))
                         for t in r['terms']] for r in ir['residuals']}
    def evaluate(row,env):
        out={}
        for a,m in rows[row]:
            term=c(a)
            for j in m:term=mul(term,env[j])
            out=add(out,term)
        return out
    def define(row,env):
        unknown={j for a,m in rows[row] for j in m if j not in env}
        assert len(unknown)==1,(row,unknown)
        j=unknown.pop();co=Fraction(0);rest={}
        for a,m in rows[row]:
            if j in m:
                assert m==(j,),(row,m)
                co+=a
            else:
                term=c(a)
                for k in m:term=mul(term,env[k])
                rest=add(rest,term)
        assert co
        env[j]=scale(rest,-1/co)
        assert evaluate(row,env)=={}
        return j

    # The field-product coordinates are scaled differently at different gates.
    env={82:v(0),83:v(1),84:v(2),85:v(3),86:v(4),87:v(5),88:v(6),89:v(7)}
    for row in range(289,298):define(row,env)
    roots=[(v(0),scale(v(1),2)),(v(2),scale(v(3),2)),
           (scale(v(4),2),scale(v(5),2)),(v(6),scale(v(7),2))]
    actual=(c(1),{})
    for root in roots:actual=fieldmul(actual,root)
    assert actual==(scale(env[341],2),scale(env[342],4))
    assert env[343]==power(env[341],2)
    assert env[344]==power(env[342],2)
    assert env[345]==power(env[342],4)

    lam,u,w,E,q,b,T=[v(i) for i in range(7)]
    base={37:lam,341:u,342:w,343:power(u,2),344:power(w,2),345:power(w,4)}
    theta=[Fraction(0),Fraction(-1,2),Fraction(-1),Fraction(1,2399),Fraction(-32,407)]
    definitions=[list(range(298,301)),list(range(345,352)),list(range(395,402))]
    e_slots=[350,398,446];q_slots=[352,400,448]
    b_slots=[385,433,481];T_slots=[383,431,479]
    results=[]
    for i in range(3):
        env=dict(base)
        for row in definitions[i]:define(row,env)
        env[e_slots[i]]=E;env[q_slots[i]]=q;env[b_slots[i]]=b;env[T_slots[i]]=T
        a=[c(1),scale(power(u,2),4),power(add(c(1),scale(power(w,2),16)),2)][i]
        t=mul(a,lam);delta=add(t,c(-1))
        represented=[env[37],scale(env.get(391,{}),4),add(env[37],scale(env.get(439,{}),32))][i]
        assert represented==t
        F=c(1)
        for root in theta:F=mul(F,add(t,c(-root)))
        e_equation=add(mul(F,E),scale(power(mul(a,delta),5),-1))
        e_factor=[Fraction(1952786),Fraction(976393,8),Fraction(1952786)][i]
        assert evaluate(302+50*i,env)==scale(e_equation,e_factor)
        q_equation=add(mul(power(delta,3),q),scale(E,-1))
        assert evaluate(304+50*i,env)==q_equation
        define(336+50*i,env)
        pole_input_equation=add(mul(mul(E,delta),b),scale(power(T,2),-1))
        actual_pole_row=evaluate(337+50*i,env)
        assert actual_pole_row in [pole_input_equation,scale(pole_input_equation,-1)]
        results.append({'detector':i,'semanticScale':['1','C0^2','(1+C1^2)^2'][i],
            'semanticInput':['lambda','4*t1Stored','lambda+32*t2Stored'][i],
            'weightRow':302+50*i,'weightResidualFactor':str(e_factor),
            'FeEqualsAdeltaPower5':True,'deltaCubedQ1EqualsE':True,
            'eDeltaBEqualsT2':True})
    # Laurent monomial identities for the six retained toric gates.
    # A pair denotes exponents of (e,delta).
    e=(1,0);q1=(1,-3)
    sub=lambda a,b:tuple(x-y for x,y in zip(a,b))
    times=lambda a,n:tuple(n*x for x in a)
    aa=sub(q1,e);bb=sub(times(aa,2),e);cc=sub(times(bb,2),q1)
    dd=sub(times(q1,5),cc);q10=sub(times(dd,2),cc);q40=sub(times(q10,4),cc)
    assert q10==(19,-3) and q40==(79,-3)
    result={'status':'passed','systemSHA256':hashlib.sha256(raw).hexdigest(),
        'actualProduct':'C=2*heightProduct.Z.0+4*heightProduct.Z.1*sqrt(2)',
        'actualRootTraceSum':'A.chart.x.0+S.chart.x.0+2*T.chart.x.0+Z.chart.x.0',
        'method':'Exact polynomial identities over Fraction; no samples.',
        'detectors':results,'toricWeightExponents':{'q1':q1,'q10':q10,'q40':q40}}
    (HERE/'final389/detector-normalization-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':main()
