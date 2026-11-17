#!/usr/bin/env python3
"""Independent exact audit of the 194-variable Laurent construction.

Uses SymPy only for field expression identities. Integer dictionaries audit
all normalized rows and independently re-expand the sum of squares.
No construction module or solver is imported.
"""
from pathlib import Path
from hashlib import sha256
from collections import defaultdict
from fractions import Fraction
from math import gcd,comb
import itertools,json,argparse,sys
sys.dont_write_bytecode=True
import sympy as sp
HERE=Path(__file__).resolve().parent
C,u,v=sp.symbols('C u v');x={i:sp.Symbol('x'+str(i))for i in range(1,1000)}
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[0],-a[1])
def sub(a,b):return add(a,neg(b))
def scale(a,q):return(a[0]*q,a[1]*q)
def mul(a,b):return(a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return(a[0],-a[1])
def pair(i,c=1):return(x[i],c*x[i+1])
def power(a,n):
    z=(sp.Integer(1),sp.Integer(0))
    for k in range(n):z=mul(z,a)
    return z

def audit(folder,model_path,result_path,source_path,primitive=False):
    D=json.loads(model_path.read_text());R=json.loads(result_path.read_text());T=json.loads((folder/'transformation.json').read_text())
    Q=json.loads((folder/'quadratic-family.json').read_text());P=json.loads((folder/'polynomial-family.json').read_text());L=json.loads((folder/'laurent-source.json').read_text())
    src=json.loads(source_path.read_text());base={int(i):tuple(e)for i,e in D['base_units'].items()};active=set(D['active'])
    assert T['base_units']==D['base_units'] and T['weights']==R['weights'] and T['row_weights']==R['row_weights'] and T['factor_assignments']==R['assignments']
    assert R['model_sha256']==sha256(model_path.read_bytes()).hexdigest()
    def monomial(ids):
        z=sp.Integer(1)
        for i in ids:z*=u**base[i][0]*v**base[i][1]if i in base else x[i]
        return z
    original={r['name']:sum(sp.Rational(t['coefficient'])*C**t['parameterPower']*monomial(t['monomial'])for t in r['terms'])for r in src['residuals']}
    reference_audit=None
    if primitive:
        original_path=source_path.parent/'source195.json'
        assert sha256(original_path.read_bytes()).hexdigest()=='304f94843c1a4ac94fcd5f1295fee8b532e7f0424e638314d892c556e2fbfdf9'
        olddata=json.loads(original_path.read_text())
        oldexpr={r['name']:sum(sp.Rational(t['coefficient'])*C**t['parameterPower']*monomial(t['monomial'])for t in r['terms'])for r in olddata['residuals']}
        change=json.loads((source_path.parent/'reference-row-map.json').read_text())
        names=change['names'];M=sp.Matrix([[sp.Rational(c)for c in row]for row in change['matrix']])
        determinant=M.det();assert determinant and determinant==sp.Rational(change['determinant'])
        assert len(names)==8 and {tuple(R['row_weights'][n])for n in names}=={(2,2)}
        for j,n in enumerate(names):assert sp.expand(original[n]-sum(M[j,k]*oldexpr[nn]for k,nn in enumerate(names)))==0,n
        for n in names:original[n]=oldexpr[n]
        reference_audit={'rows':8,'determinant':str(determinant),'common_row_weight':[2,2],'basis':'original v45 primitive reference rows','source_sha256':sha256(original_path.read_bytes()).hexdigest()}
    expected={}
    def group(name,z):
        expected[name]=[sp.expand(z[0]),sp.expand(z[1])]
    root=(sp.Integer(11),sp.Integer(-6));one=(sp.Integer(1),sp.Integer(0))
    pairs={1:(201,203,205,207,209,211),3:(213,215,217,219,221,223),4:(225,227,229,231,233,235)}
    raw={}
    S=scale(pair(17),1/u);TH=scale(pair(150),1/u)
    for role,indices in pairs.items():
        s,t,F,G,h,d=[pair(i)for i in indices];p=add(add(h,s),t)
        group(f'new{role}.d_piF',sub(d,mul(p,F)))
        group(f'new{role}.d_Gh',sub(d,mul(h,G)))
        group(f'new{role}.sum',add(sub(mul(root,add(F,G)),mul(sub(s,t),h)),power(t,2)))
        group(f'new{role}.unit',add(sub(one,mul(d,sub(s,t))),mul(root,mul(F,G))))
        raw['A'+str(role)]=F;raw['B'+str(role)]=conj(G)
        E={1:31,3:39,4:43}[role]
        physical=sub(mul(S,conj(t)),mul(conj(TH),s))
        group(f'cleared.E{role}',scale(sub(scale(pair(E),1/u),physical),u))
    # s2=(U+M)/R, t2=-(V+M)/R. Clear by nonzero R.
    s2=scale(add(pair(182),pair(188)),1/x[113]);t2=scale(add(pair(184),pair(188)),-1/x[113])
    E2=sub(mul(S,conj(t2)),mul(conj(TH),s2))
    group('cleared.E2',scale(sub(scale(pair(35),1/u),E2),u*x[113]))
    for role,E,J in [(1,31,60),(2,35,66),(3,39,68),(4,43,70)]:
        group(f'cleared.E{role}.square',scale(sub(scale(pair(J,2),C/u),power(scale(pair(E),1/u),2)),u*u))
    group('new.square.237',sub(pair(237),power(raw['A4'],2)))
    group('new.square.239',sub(pair(239),power(pair(231),2)))
    beta=51*x[45]/u+2504
    N=sub(S,scale(pair(201),beta))
    group('input.cleared',scale(sub(scale(pair(29),1/u),N),u))
    group('input.cleared.square',scale(sub(scale(pair(62,2),1/u),power(scale(pair(29),1/u),2)),u*u))
    group('input.cleared.fourth',scale(sub(scale(pair(116),1/u),power(scale(pair(62,2),1/u),2)),u*u))
    A=scale(pair(33),C/u);w=pair(225);calC=scale(pair(46),1/u);calP=scale(pair(41),1/u);calQ=scale(pair(48),1/u);H=scale(pair(50,2),1/u)
    group('homogeneous.C',scale(sub(calC,mul(sub(A,one),add(w,scale(S,4)))),u))
    group('homogeneous.Q',scale(sub(calQ,mul(add(A,one),calP)),u*u))
    hvalue=sub(sub(add(power(calP,2),power(calC,2)),mul(calC,calQ)),power(w,2))
    group('homogeneous.H',scale(sub(H,hvalue),u*u))
    group('homogeneous.H.square',scale(sub(scale(pair(72,4),1/u),power(H,2)),u*u))
    group('homogeneous.P.ratio',scale(sub(mul(calP,pair(213)),scale(mul(S,w),2)),u))
    aggregate=2*x[2]-2*x[86]+14*u+x[192]
    for indices in pairs.values():
        s,t,F,G,h,d=[pair(i)for i in indices]
        aggregate+=u*mul(h,add(add(h,s),t))[0]
    expected['new.aggregate']=[sp.expand(aggregate)]
    quadratic={'C2':scale(pair(66,2),C/u),'C3':scale(pair(68,2),C/u),'C4':scale(pair(70,2),C/u),'GL':scale(pair(72,4),1/u),**{k:raw[k]for k in ['A1','B1','A3','B3']}}
    linear={'DH':scale(pair(64,2),1/u),'B0':scale(conj(pair(19,2)),1/u),'A2':scale(pair(54,2),C/u),'B2':scale(conj(pair(23,2)),1/u),'A4':pair(237),'B4':conj(pair(239)),'C1':scale(pair(114),C/u)}
    for det in(0,1):
        q=u*v**det;assign=R['assignments'][str(det)]
        for k in range(5):
            output=scale(pair(118+16*det+2*k),C**[1,1,1,0,-1][k]*u*v**(2*det))
            residual=sub(one,output)
            if k==4:residual=add(residual,scale(power(scale(pair(116),1/u),2),q**4))
            for lab,slot in assign['quadratic'].items():
                if slot//2==k:residual=add(residual,scale(power(quadratic[lab],2),q**(1+2*(slot%2))))
            for lab,slot in assign['linear'].items():
                if(slot if slot<4 else 4)==k:residual=add(residual,scale(linear[lab],q**(2 if slot<4 else slot-3)))
            group(f'new.det{det}.factor{k}',residual)
    grouped=defaultdict(list)
    for row in L['rows']:grouped[row['group']].append(row)
    assert set(grouped)=={r['name']for r in D['rows']}
    explicit=retained=0
    for name,rows in grouped.items():
        if name in expected:exprs=expected[name];explicit+=len(rows)
        else:exprs=[original[name]];retained+=1
        assert len(exprs)==len(rows),(name,len(exprs),len(rows))
        for row,expr in zip(rows,exprs):
            observed=sum(sp.Rational(t['coefficient'])*C**t['parameterPower']*u**t['unitPower'][0]*v**t['unitPower'][1]*monomial(t['monomial'])for t in row['terms'])
            assert sp.expand(expr-observed)==0,name
    # Independently recover every Laurent source from the final normalized row.
    weight={int(i):tuple(e)for i,e in T['weights'].items()};ren={int(i):j for i,j in T['old_to_new'].items()};inv={j:i for i,j in ren.items()}
    assert set(ren)==active|set(base) and set(ren.values())==set(range(1,195)) and ren[1]==1
    for entry in Q['coordinates']:assert inv[entry['id']]==entry['source_id']
    normalization={r['name']:r for r in T['normalizations']};laurent={r['name']:r for r in L['rows']};compiled={r['name']:r for r in Q['residuals']}
    assert len(compiled)==len(Q['residuals'])==168
    assert set(compiled)==set(laurent)|set(T['literal_guards'])
    def sparse_terms(row):
        z=defaultdict(Fraction)
        for t in row['terms']:
            m=[];e=[0,0]
            for j in t['monomial']:
                i=inv[j]
                if i in base:
                    for k in(0,1):e[k]+=base[i][k]
                else:
                    m.append(i)
                    for k in(0,1):e[k]-=weight[i][k]
            z[t['parameterPower'],tuple(sorted(m)),tuple(e)]+=Fraction(t['coefficient'])
        return {k:c for k,c in z.items()if c}
    for name,row in compiled.items():
        assert all(len(t['monomial'])<=2 for t in row['terms'])
        back=sparse_terms(row)
        if name in laurent:
            original_row=laurent[name];norm=normalization[name];rw=original_row['rowUnitDivision'];want=defaultdict(Fraction)
            for t in original_row['terms']:
                key=(t['parameterPower']+norm['C_shift'],tuple(t['monomial']),tuple(t['unitPower'][k]-rw[k]for k in(0,1)))
                want[key]+=Fraction(t['coefficient'])*Fraction(norm['rational_multiplier'])
            assert back=={k:c for k,c in want.items()if c},name
        else:assert not back,name
    # Different multiplication ordering from the producer: i<=j with doubled
    # off-diagonal products, accumulated solely with Python integers.
    expansion=defaultdict(int)
    for row in Q['residuals']:
        terms=row['terms']
        for i,t in enumerate(terms):
            for j in range(i,len(terms)):
                s=terms[j];key=t['parameterPower']+s['parameterPower'],tuple(sorted(t['monomial']+s['monomial']))
                expansion[key]+=(1 if i==j else 2)*int(t['coefficient'])*int(s['coefficient'])
    expansion={k:c for k,c in expansion.items()if c}
    observed={}
    for t in P['terms']:
        key=t['parameterPower'],tuple(t['monomial']);assert key not in observed;observed[key]=int(t['coefficient'])
    assert expansion==observed
    assert expansion[(0,(1,1,1,1))]==1
    assert all(not(a>0 and m==(1,1,1,1))for a,m in expansion)
    assert set(i for a,m in expansion for i in m)==set(range(1,195))
    assert max(len(m)for a,m in expansion)==4
    coefficients=defaultdict(dict)
    for(a,m),c in expansion.items():coefficients[m][a]=c
    mixed=[]
    for m,cs in coefficients.items():
        if len({1 if c>0 else-1 for c in cs.values()})>1:
            f=sum(c*C**a for a,c in cs.items());mixed.append({'monomial':m,'factorization':str(sp.factor(f)),'rational_roots':[str(z)for z in sp.polys.polytools.ground_roots(f,C)],'nonzero_C_ge_149':all(not(z.is_real and z>=149)for z in sp.solve(f,C))})
    assert all(z['nonzero_C_ge_149']for z in mixed)
    constant_rows=[(m,cs[0])for m,cs in coefficients.items()if set(cs)=={0}]
    H0=max(abs(c)for m,c in constant_rows)
    assert H0==(126616122944180358034867798936 if primitive else 484991541504995159662206970923766531374664106904986910720)
    assert any(cs=={4:128}for cs in coefficients.values())
    crossover=1
    while 128*149**(4*crossover)<H0:crossover+=1
    assert crossover==(4 if primitive else 7)
    finite=[]
    for N in range(1,crossover):
        cval=149**N;actual=max(abs(sum(c*cval**a for a,c in cs.items()))for cs in coefficients.values());assert actual==H0
        finite.append({'N':N,'height':actual})
    cmin=149**crossover;margins=[None]*5
    for m,cs in coefficients.items():
        for sign in(-1,1):
            # Exact binomial expansion at C=cmin+z, using integers only.
            for k in range(5):
                a=128*comb(4,k)*cmin**(4-k)+sign*sum(c*comb(j,k)*cmin**(j-k)for j,c in cs.items()if j>=k)
                assert a>=0,(m,sign,k,a)
                margins[k]=a if margins[k]is None else min(margins[k],a)
    assert 128*149**(4*(crossover-1))<H0<128*149**(4*crossover)
    height_audit={'formula':f'max({H0},128*149^(4N))','valid_for':'every integer N>=1','constant_to_quartic_crossover_N':crossover,'exact_below_crossover':finite,'all_N_ge_crossover_certificate':f'Every coefficient of 128*(149^{crossover}+z)^4 ± f(149^{crossover}+z) is nonnegative for every coefficient polynomial f. Thus the bound holds for z>=0, and the pure coefficient 128*C^4 attains it.','coefficientwise_nonnegative_comparisons':2*len(coefficients),'minimum_comparison_coefficient_by_degree':margins}
    return {'schema':'independent-quartic194-exact-audit/v71','status':'PASS','variables':194,'explicit_physical_component_rows':explicit,'retained_source_rows':retained,'literal_unit_guards':6,'normalized_quadratic_rows':168,'all_row_pullbacks_exact':True,'independent_sum_of_squares_expansion':True,'parameter_separated_terms':len(expansion),'coordinate_monomials_at_C_149_power_N':len(coefficients),'degree':4,'content_for_each_positive_integral_C':1,'every_coordinate_occurs':True,'mixed_coefficient_audit':mixed,'source_sha256':sha256(source_path.read_bytes()).hexdigest(),'quadratic_table_sha256':sha256((folder/'quadratic-family.json').read_bytes()).hexdigest(),'quartic_table_sha256':sha256((folder/'polynomial-family.json').read_bytes()).hexdigest(),'reference_basis_audit':reference_audit,'coefficient_height_audit':height_audit,'scope':'Exact algebra, coordinate map, degree and expansion. Arithmetic transfer and retained global premises are checked separately.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--folder',type=Path,default=HERE/'fewer_monomials')
    ap.add_argument('--model',type=Path,default=HERE/'coordinate-model.json')
    ap.add_argument('--result',type=Path,default=HERE/'laurent-certificate.json')
    ap.add_argument('--source',type=Path,default=HERE/'source/reversed_reference_basis.json')
    ap.add_argument('--primitive-reference',action='store_true')
    ap.add_argument('--output',type=Path,default=HERE/'quartic194_exact_certificate.json')
    a=ap.parse_args();r=audit(a.folder,a.model,a.result,a.source,a.primitive_reference);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
