#!/usr/bin/env python3
"""Independent exact verification of the 392-variable forced-prime construction.

No producer or other checker is imported. A complete 394-variable SOS is first
reconstructed and compared with the pinned upstream public table. The new
coordinate incidence, every residual, the complete new SOS, its specialization,
and elementary local numerical certificates are then checked independently.
This program does not certify the inherited arithmetic theorems.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd, isqrt, lcm
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
DIR=ROOT/'final392'
SOURCE=ROOT/'upstream'/'candidate394-ir.json'
PIN='7eb02f9913b55d60a790a287616f1bb80d9f93523e9f11e12481c9ab955746a5'


def prune(p):return {m:c for m,c in p.items() if c}

def add(*polys):
    a=defaultdict(Fraction)
    for p in polys:
        for m,c in p.items():a[m]+=c
    return prune(a)

def times(p,q):
    a=defaultdict(Fraction)
    for (m,k),c in p.items():
        for (n,l),d in q.items():a[tuple(sorted(m+n)),k+l]+=c*d
    return prune(a)

def atom(coefficient=1,variables=(),power=0):
    return {(tuple(sorted(variables)),power):Fraction(coefficient)}

def rescale(p,c):return prune({m:c*v for m,v in p.items()})

def parse(row,power_name='sPower'):
    ans=defaultdict(Fraction)
    for t in row['terms']:ans[tuple(t['monomial']),t[power_name]]+=Fraction(t['coefficient'])
    return prune(ans)

def prim(poly):
    d=lcm(*(v.denominator for v in poly.values()))
    g=gcd(*(int(v*d) for v in poly.values()))
    return {m:int(v*d)//g for m,v in poly.items()}

def sum_squares(rows):
    result={}
    for row in rows:result=add(result,times(row,row))
    return result

# Univariate operations use a separate, coefficient-list implementation.
def uadd(a,b):
    c=[Fraction(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    while len(c)>1 and c[-1]==0:c.pop()
    return c

def umul(a,b):
    c=[Fraction(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    while len(c)>1 and c[-1]==0:c.pop()
    return c

def ueval(row,values):
    result=[Fraction(0)]
    for (variables,power),coefficient in row.items():
        assert power==0
        p=[coefficient]
        for v in variables:p=umul(p,values[v])
        result=uadd(result,p)
    return result


def main():
    raw=SOURCE.read_bytes();assert sha256(raw).hexdigest()==PIN
    source=json.loads(raw);source_rows={r['id']:parse(r) for r in source['residuals']}
    assert len(source_rows)==364 and len(source['coordinates'])==394
    # Bind the complete source coefficients to its independently supplied public table.
    public=json.loads((ROOT/'upstream'/'polynomial394.json').read_text())
    cmap={c['id']:c['sourceId'] for c in public['coordinates']}
    target={}
    for (mon,power),coefficient in parse(public).items():
        target[tuple(cmap[v] for v in mon),power]=coefficient
    old_sos=sum_squares([prim(r) for r in source_rows.values()])
    assert old_sos==target
    assert len(old_sos)==6338
    # Derive the raw scalar contact from the literal old root row.
    oldroot=source_rows[512]
    raw_contact={}
    for (mon,power),c in oldroot.items():
        if 541 in mon:
            mon=list(mon);mon.remove(541)
            raw_contact[tuple(mon),power]=-c
    assert all(power==0 and len(mon)<=1 for mon,power in raw_contact)
    assert source_rows[560]==add(atom(1,(600,)),rescale(times(raw_contact,raw_contact),-1))
    assert source_rows[566]==add(atom(1,(540,604)),atom(-1,(508,508)),rescale(times(raw_contact,atom(1,(539,))),-1))
    assert source_rows[512]==add(atom(1,(542,604)),atom(-1,(540,540)),rescale(times(raw_contact,atom(1,(541,))),-1))
    assert source_rows[492]==add(atom(1,(525,600)),rescale(times(raw_contact,atom(1,(525,))),4896),atom(82479248,(526,)))
    # Sequentially solve the raw polynomial circuit, without producer formulas.
    uv={0:[Fraction(0),Fraction(1)],248:[Fraction(0),Fraction(0),Fraction(1)]}
    assert ueval(source_rows[200],uv)==[0]
    for gate,row_id in [(487,453),(488,454),(489,455)]:
        p=source_rows[row_id]; pivot=p[((gate,),0)]
        assert all(gate not in m or m==(gate,) for m,e in p)
        remainder={key:c for key,c in p.items() if key!=((gate,),0)}
        uv[gate]=[x/(-pivot) for x in ueval(remainder,uv)]
        assert ueval(p,uv)==[0]
    actual_raw=ueval(raw_contact,uv)
    beta=[Fraction(2555),Fraction(204),Fraction(204)]
    expected=[Fraction(1)]
    for a,b in [(1,0),(1,-1),(1,-2401),(32,343),(2,-1)]:
        expected=umul(expected,uadd([a*x for x in beta],[Fraction(b)]))
    assert actual_raw==expected and len(actual_raw)==11
    # Check exactly which objects were changed and which coordinates disappeared.
    new=json.loads((DIR/'quadratic-system392.json').read_text())
    coords=new['coordinates'];back={c['id']:c['sourceId'] for c in coords}
    forward={v:k for k,v in back.items()}
    assert sorted(back)==list(range(1,393)) and back[1]==0
    deleted={55,56,57}; fresh=702
    old_ids={c['id'] for c in source['coordinates']}
    assert set(back.values())==(old_ids-deleted)|{fresh}
    names={c['id']:c['name'] for c in source['coordinates']}
    assert all(c['name']==names[c['sourceId']] for c in coords if c['sourceId']!=fresh)
    incidence={v:[i for i,p in source_rows.items() if any(v in m for m,e in p)] for v in deleted}
    assert incidence=={55:[504],56:[504],57:[504]}
    assert [i for i,p in source_rows.items() if any(e for m,e in p)]==[504]
    ell=80989;n=27464;exponent=54929
    assert exponent==2*n+1
    assert new['fixedParameter']=={'name':'A','base':ell,'exponent':exponent,'coordinate':False}
    rr=atom(1,(fresh,));aa=atom(1,power=1)
    replacement={
        492:add(atom(1,(525,600)),atom(4896,(525,fresh)),atom(82479248,(526,))),
        512:add(atom(1,(542,604)),atom(-1,(540,540)),atom(-1,(541,fresh))),
        560:add(atom(1,(600,)),atom(-1,(fresh,fresh))),
        566:add(atom(1,(540,604)),atom(-1,(508,508)),atom(-1,(539,fresh))),
        733:add(rr,rescale(times(raw_contact,rr),ell**2),rescale(times(raw_contact,aa),-1))}
    actual={}
    for row in new['residuals']:
        assert row['sourceId'] not in actual
        poly=parse(row,'parameterPower')
        actual[row['sourceId']]={(tuple(back[v] for v in m),e):c for (m,e),c in poly.items()}
    assert set(actual)==(set(source_rows)-{504})|{733}
    for i,poly in actual.items():assert poly==prim(replacement[i] if i in replacement else source_rows[i])
    assert len(actual)==364 and max(len(m) for row in actual.values() for m,e in row)==2
    # The retained physical scalar normalization and nonzero guard are literal.
    assert actual[732]==prim(source_rows[732])
    assert source_rows[732]==add(atom(-1),atom(1,(543,549)))
    wrow=source_rows[491];J=wrow[((525,),0)]
    assert J>0 and wrow==add(atom(J,(525,)),atom(-1,(542,542)))
    physical_pole_scale=int(82479248*J)
    # Independent full new expansion: ordered pairs, then collapse parameter powers.
    full_source=sum_squares(list(actual.values()))
    table=json.loads((DIR/'polynomial392.json').read_text())
    assert table['fixedParameter']==new['fixedParameter'] and table['coordinates']==coords
    table_source={(tuple(back[v] for v in m),e):c for (m,e),c in parse(table,'parameterPower').items()}
    assert full_source==table_source
    assert max(len(m) for m,e in full_source)==4
    ordinary=defaultdict(dict)
    for (m,e),c in full_source.items():ordinary[m][e]=int(c)
    av=pow(ell,exponent); powers=[1,av,av*av]
    instantiated={m:sum(c*powers[e] for e,c in poly.items()) for m,poly in ordinary.items()}
    assert all(instantiated.values())
    assert set(v for m in ordinary for v in m)==set(back.values())
    assert len(ordinary)==6204 and len(full_source)==6225
    units=[m for m,c in instantiated.items() if c==1]
    assert units and gcd(*(int(c) for c in full_source.values()))==1
    height_monomial=max(instantiated,key=lambda m:abs(instantiated[m]))
    assert height_monomial==()
    assert instantiated[()].bit_length()==1791357
    # Exact starting residue for the retained nonzero scalar-coordinate guard.
    def ka(x,y):return (x[0]+y[0],x[1]+y[1])
    def km(x,y):return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    def ks(x,c):return (c*x[0],c*x[1])
    def kd(x,y):
        norm=y[0]*y[0]-2*y[1]*y[1]
        return ks(km(x,(y[0],-y[1])),1/norm)
    xp=(Fraction(57,8),Fraction(-7,2));yp=(Fraction(-165,8),Fraction(417,32))
    dd=(Fraction(11),Fraction(-6))
    slope=kd(ka(ks(km(xp,xp),3),ks(dd,-1)),ks(yp,2))
    x2=ka(km(slope,slope),ks(xp,-2))
    y2=ka(km(slope,ka(xp,ks(x2,-1))),ks(yp,-1))
    z2=ks(kd(x2,y2),Fraction(-1,3))
    residues=[c.numerator*pow(c.denominator,-1,3)%3 for c in z2]
    assert residues==[2,1]
    # Independently certify the common explicit contact-height constant.
    sieve=bytearray(b'\1')*76177;sieve[:2]=b'\0\0'
    for pp in range(2,isqrt(76176)+1):
        if sieve[pp]:sieve[pp*pp:76177:pp]=b'\0'*(((76176-pp*pp)//pp)+1)
    primes=[pp for pp in range(2,76177) if sieve[pp]]
    primorial=1
    for pp in primes:primorial*=pp
    common_height=(1<<110)*210**1800*primorial**19+128
    assert len(primes)==7499 and primes[-1]==76163
    assert common_height.bit_length()==2093448
    # Prime, nonresidue and exact numerical margin certificates.
    assert ell>76176 and ell%17==1 and all(ell%d for d in range(2,isqrt(ell)+1))
    roots=[Fraction(0),Fraction(1),Fraction(2401),Fraction(-343,32),Fraction(1,2)]
    legendre=[]
    for theta in roots:
        x=(theta-2504)/51
        residue=x.numerator*pow(x.denominator,-1,ell)%ell
        value=pow(residue,(ell-1)//2,ell)
        assert value==ell-1
        legendre.append({'root':str(theta),'residue':residue,'eulerPower':value})
    nu=2*n-1; depth=187*nu//8+1
    assert depth==1283919 and nu==54927
    assert pow(ell,4096)>1<<66787
    margin=66787*depth-4096*20934550
    assert margin==1181453 and margin>0
    # Local square ratios for integer input: exact unit residue checks.
    assert ell%2 and ell%3 and ell%17==1
    assert (1+ell*ell*15)%17!=0
    # Exact residue classes certify the integer-input valuations of the raw contact.
    def raw_at_tau(t):
        b=51*t*t+2504
        return b*(b-1)*(b-2401)*(32*b+343)*(2*b-1)
    assert all(raw_at_tau(t)%8==4 for t in range(1,8,2))
    assert all(raw_at_tau(t)%3==0 and raw_at_tau(t)%9!=0 for t in range(9))
    assert all(raw_at_tau(t)%17==15 for t in range(17))
    # M/R has depths3,1,1, giving c/R a square over Q2,Q3,Q17.
    def valuation(a,p):
        v=0
        while a%p==0:a//=p;v+=1
        return v
    assert [valuation(4896,p)-a for p,a in [(2,2),(3,1),(17,0)]]==[3,1,1]
    # Check the leading valuation formulas in a general rational valuation ring.
    assert 4*(Fraction(63,4))==63 and 4*(Fraction(61,4))==61
    assert (Fraction(63,4)+32)/2==Fraction(191,8)
    assert (Fraction(63,4)+32-1)/2==Fraction(187,8)
    report={'status':'passed','variables':392,'residuals':364,'degree':4,'ordinaryMonomials':6204,
        'symbolicTerms':6225,'content':1,'heightBitLength':1791357,
        'heightPolynomial':{str(e):str(c) for e,c in sorted(ordinary[()].items())},
        'source394SOSReconstructed':True,'sourceContactIdentityDegree':len(actual_raw)-1,
        'unchangedResiduals':359,'modifiedResiduals':4,'addedResiduals':1,'removedResiduals':1,
        'fixedPrime':ell,'normalizerExponent':exponent,'legendreCertificate':legendre,
        'commonHeightBitLength':common_height.bit_length(),'commonHeightPrimeCount':len(primes),
        'z2PDividedBy3Residues':residues,
        'minimumForcedValuation':nu,'minimumIndexDepth':depth,
        'binaryLogLowerBound':20934550,'integerMarginCertificate':margin,
        'physicalPoleScale':str(physical_pole_scale),
        'unitCoefficientSourceMonomial':list(units[0]),
        'scope':'The exact algebraic construction and elementary numerical certificates pass. The inherited arithmetic input contract and its applications require the accompanying proofs.',
        'hashes':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in [SOURCE,ROOT/'upstream'/'polynomial394.json',DIR/'quadratic-system392.json',DIR/'polynomial392.json']}}
    (DIR/'independent-verification392.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','variables','residuals','degree','ordinaryMonomials','content','heightBitLength','fixedPrime','normalizerExponent','minimumIndexDepth']},indent=2))

if __name__=='__main__':main()
