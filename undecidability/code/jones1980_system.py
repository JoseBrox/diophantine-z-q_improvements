#!/usr/bin/env python3
"""Exact quadratization of an emended Jones-type system.

SOURCE-STATUS CORRECTION: the literal Jones1980 scan prints 4*alpha*gamma
in the d equation, whereas this builder uses 4*a*gamma. Matiyasevich1999
p.191 supports Latin a, but its Pell row has a separate =1 versus +1 typo.
Thus universality of this precise emended system remains hypothesis U_em;
the coefficient identities and both-direction algebraic reduction are exact.
See source_reconciliation.tex for the source comparison and remaining task.

No Mishchenko--Treier equation is used. The integrality interface is external.
"""
from __future__ import annotations
import argparse
import json
import hashlib
from pathlib import Path
import sympy as sp

EXPONENT = 5**60


def power_chain(exponent: int, width: int):
    """An addition chain containing 5, from a fixed sliding-window algorithm."""
    have={1}
    steps=[]
    def add(a,b):
        e=a+b
        if e not in have:
            assert a in have and b in have
            steps.append((e,a,b));have.add(e)
        return e
    add(1,1);add(2,2);add(4,1)
    add(2,1)
    for odd in range(5,1<<width,2):add(odd-2,2)
    bits=bin(exponent)[2:]
    pos=0;current=0
    while pos<len(bits):
        if bits[pos]=='0':
            current=add(current,current);pos+=1
        else:
            end=min(len(bits),pos+width)
            while bits[end-1]=='0':end-=1
            odd=int(bits[pos:end],2)
            if current==0:current=odd
            else:
                for _ in range(end-pos):current=add(current,current)
                current=add(current,odd)
            pos=end
    assert current==exponent
    return steps


def signed_power_chain(exponent: int, width: int):
    """An exact addition/subtraction chain; subtraction uses a quadratic row."""
    have={1};steps=[]
    def add(a,b):
        assert a in have and abs(b) in have
        e=a+b
        assert e>0
        if e not in have:
            steps.append((e,a,b));have.add(e)
        return e
    add(1,1)
    for e in range(3,1<<(width-1),2):add(e-2,2)
    digits=[];cur=exponent
    while cur:
        digit=0
        if cur&1:
            digit=cur%(1<<width)
            if digit>=1<<(width-1):digit-=1<<width
            cur-=digit
        digits.append(digit);cur//=2
    cur=0
    for digit in reversed(digits):
        if not cur:
            cur=digit
            assert cur>0
            continue
        cur=add(cur,cur)
        if digit:cur=add(cur,digit)
    assert cur==exponent and 5 in have
    needed={exponent,5}
    for e,a,b in reversed(steps):
        if e in needed:needed|={a,abs(b)}
    return [q for q in steps if q[0] in needed]


def best_power_chain():
    candidates=[]
    for w in range(2,8):
        chain=power_chain(EXPONENT,w)
        candidates.append((len(chain),w,chain))
        chain=signed_power_chain(EXPONENT,w)
        candidates.append((len(chain),-w,chain))
    return min(candidates,key=lambda v:(v[0],sum(t[2]<0 for t in v[2]),abs(v[1])))


def build_system(include_positivity=True):
    """Return symbolic quadratic rational core and interfaces.

    Ordinary integer inputs: b,g,t,m,w,s,h,phi,gamma,o,j (11).
    Reciprocal integer input: i_inverse, whose reciprocal must be in Z.
    The row i_inverse*E=C2 forces i_inverse!=0 once C>0.
    The core contains eleven three-triangular positivity wrappers.
    Soundness is proved for the cofinite instance range x>2*z; r>0 is then automatic.
    """
    sym={}
    variables=[]
    rows={}
    def var(name):
        assert name not in sym,name
        v=sp.Symbol(name);sym[name]=v;variables.append(v);return v
    x,z,u,y=sp.symbols('x z u y')
    parameters=(x,z,u,y)
    def row(name,expr):
        assert name not in rows,name
        rows[name]=sp.expand(expr)
    def define(name,expr):
        v=var(name);row(name+'.definition',v-expr);return v
    names='b g t m w s h phi gamma o j i_inverse'.split()
    b,g,t,m,w,s,h,phi,gamma,o,j,i_inverse=[var(v) for v in names]
    lam=var('lam');F=var('F');tau=var('tau')
    chain_len,width,chain=best_power_chain()
    powers={1:b}
    for index,(e,a0,b0) in enumerate(chain):
        name={2:'b2',4:'b4',5:'B5',EXPONENT:'q'}.get(e,f'power_{index:03}')
        if b0>0:
            powers[e]=define(name,powers[a0]*powers[b0])
        else:
            powers[e]=var(name)
            row(name+'.quotient',powers[e]*powers[-b0]-powers[a0])
    B5=powers[5];q=powers[EXPONENT]
    q2=define('q2',q*q);q3=define('q3',q*q2);q4=define('q4',q2*q2)
    q5=define('q5',q*q4);q8=define('q8',q4*q4)
    n=define('n',q8*q8);n2=define('n2',n*n)
    theta=B5-2*z
    row('lambda.geometric',lam*(B5-1)-q4+1)
    ell=define('ell',u+t*theta);evar=define('e',y+m*theta)
    c0=1+x*B5+g
    c02=define('c02',c0*c0);c04=define('c04',c02*c02)
    V=define('V',c04*q4)
    S=define('S',g+evar*q3+ell*q5+2*(evar-z*lam)*V+(lam+q4-1)*(q4+q8))
    T=define('T',(1-b)*ell+(q4+(1-2*z)*lam)*q3+(B5-2)*q5)
    r=define('r',S*(n2-n)+T*(n2-1))
    el=define('el',evar*ell);g2=define('g2',g*g)
    alpha=(b-x*y)*q2-el*g2
    sr=define('sr',s*r);sr2=define('sr2',sr*sr)
    U=define('U',w*n2)
    p=define('p',2*U*sr2)
    Y=define('Y',s*n2);M=define('M',r*Y)
    a=define('a',(U+1)*M)
    k=define('k',r+1+h*(p-1))
    pk=define('pk',p*k)
    row('tau.norm',tau*tau-pk*pk+k*k-1)
    c=2*r+1+phi
    YK=define('YK',Y*k)
    eta=k*k-4*(c-YK)**2
    d=define('d',b*w+c*a-2*c+4*a*gamma-5*gamma)
    ac=define('ac',a*c);C2=define('C2',c*c)
    d2=define('d2',d*d)
    row('d.norm',d2-ac*ac+C2-1)
    E=var('E');row('E.reciprocal',i_inverse*E-C2)
    AE=define('AE',a*E);F2=define('F2',F*F)
    row('F.norm',F2-AE*AE+E*E-1)
    G=define('G',a+F2*(d2-a))
    H=define('H',2*r+1+j*c)
    I=define('I',d+o*F)
    GH=define('GH',G*H)
    row('I.norm',I*I-GH*GH+H*H-1)
    guards={name:sym[name] for name in 'g t m w s phi gamma'.split()}
    guards.update({'I':I,'theta':theta,'alpha':alpha,'eta':eta})
    assert len(guards)==11
    if include_positivity:
        for name,expr in guards.items():
            v=[var(f'positive_{name}_{l}') for l in range(1,4)]
            row('positive.'+name,2*expr-2-sum(qv*(qv+1) for qv in v))
    return {
      'variables':tuple(variables),'parameters':parameters,'rows':rows,'symbols':sym,
      'ordinary_integrality_inputs':tuple(sym[v] for v in 'b g t m w s h phi gamma o j'.split()),
      'reciprocal_integrality_inputs':(i_inverse,),
      'positive_guards':guards,
      'source_aliases':{'theta':theta,'alpha':alpha,'eta':eta,'c':c,'i':1/i_inverse},
      'power_chain':chain,'power_expressions':powers,'power_window':width,
      'source':'Emended Jones1980/Matijasevich1999 system; precise universality hypothesis U_em remains unverified',
      'source_status':'algebraically verified; undecidability transfer conditional on U_em',
    }


def source_system():
    d=build_system()
    return d['variables'],d['parameters'],d['rows'],d['symbols']


def audit():
    d=build_system()
    vs=d['variables'];ps=d['parameters'];rs=d['rows'];s=d['symbols']
    assert all(sp.Poly(row,*vs).total_degree()<=2 for row in rs.values())
    used=set.union(*(row.free_symbols for row in rs.values()))-set(ps)
    assert used==set(vs)
    assert len(vs)==len(set(vs))
    # Verify all large powers through exact integer exponents, never expand them.
    have={1}
    for e,a,b in d['power_chain']:
        assert e==a+b and a in have and abs(b) in have and e not in have and e>0
        have.add(e)
    assert EXPONENT in have and 5 in have
    # Verify the two regroupings used in the r-polynomial modulo lambda row.
    B,q,la,e,l,g,b,z,x=sp.symbols('B q la e l g b z x')
    C04=sp.symbols('C04')
    S0=g+e*q**3+l*q**5+(2*(e-z*la)*C04+la*B+la*B*q**4)*q**4
    S1=g+e*q**3+l*q**5+2*(e-z*la)*C04*q**4+(la+q**4-1)*(q**4+q**8)
    T0=q**3-b*l+l+(B-2*z)*la*q**3+(B-2)*q**5
    T1=(1-b)*l+(q**4+(1-2*z)*la)*q**3+(B-2)*q**5
    lamres=la*(B-1)-q**4+1
    assert sp.expand(S0-S1-(q**4+q**8)*lamres)==0
    assert sp.expand(T0-T1-q**3*lamres)==0
    # Independent checks of every nonlinear source product whose exponent matters.
    sr,U,n,w,r,ss=sp.symbols('sr U n w r ss')
    assert sp.expand((2*U*sr**2).subs({U:w*n**2,sr:ss*r})-2*w*ss**2*r**2*n**2)==0
    aa,F,dd,H,I=sp.symbols('aa F dd H I')
    GG=aa+F**2*(dd**2-aa)
    assert sp.expand(I**2-(GG*H)**2+H**2-1-(I**2-(GG**2-1)*H**2-1))==0
    checks={
      'source':d['source'],
      'source_status':d['source_status'],
      'quadratic_core_variables':len(vs),
      'quadratic_core_rows':len(rs),
      'core_before_positivity_variables':len(vs)-33,
      'ordinary_integrality_inputs':list(map(str,d['ordinary_integrality_inputs'])),
      'reciprocal_integrality_inputs':list(map(str,d['reciprocal_integrality_inputs'])),
      'positivity_guards':list(d['positive_guards']),
      'positivity_triples':11,
      'instance_restriction':'x > 2*z (cofinite tail preserves undecidability)' ,
      'power_exponent':str(EXPONENT),'power_window':d['power_window'],
      'power_multiplications':len(d['power_chain']),
      'power_candidates':{str(w):len(power_chain(EXPONENT,w)) for w in range(2,8)},
      'signed_power_candidates':{str(w):len(signed_power_chain(EXPONENT,w)) for w in range(2,8)},
      'power_subtractions':sum(q[2]<0 for q in d['power_chain']),
      'power_chain_precondition':'b nonzero, forced by b**5-2*z>0; every intermediate is exactly b**e for positive e',
      'source_P_exponent_n':2,'source_last_norm_G_exponent':2,
      'source_F_norm_E':'i*c**2 (without +1)',
      'transfer_variable_formula':f'12*(m-1)+{len(vs)}',
      'm163_variables':12*162+len(vs),
      'm179_variables':12*178+len(vs),
      'm56_variables':12*55+len(vs),
      'm163_residuals':12*137+len(rs),
      'm179_residuals':12*151+len(rs),
      'm56_residuals':12*46+len(rs),
      'core_sha256':hashlib.sha256('\n'.join(k+':'+sp.srepr(v) for k,v in rs.items()).encode()).hexdigest(),
      'verification_scope':'exact algebraic reconstruction of the displayed emended system and finite counts; universality hypothesis U_em and chosen integrality interface are separate premises',
    }
    return checks

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);args=ap.parse_args()
    data=audit();out=json.dumps(data,indent=2,sort_keys=True)+'\n'
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(out)
    print(out,end='')
