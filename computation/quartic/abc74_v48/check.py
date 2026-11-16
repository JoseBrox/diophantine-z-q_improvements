#!/usr/bin/env python3
"""Independent exact audit of the 74-coordinate coefficient specification.

Uses sparse polynomials with rational-pair coefficients for Q(sqrt(2)).
Imports no producer code and does not rerun lattice reduction. The displayed
literal equations, the stored invertible matrices and their inverses are
checked, then the quartic is expanded by unordered term pairs.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from collections import defaultdict
from math import gcd,lcm
from hashlib import sha256
import argparse,json

@dataclass(frozen=True)
class K:
    re:Q=Q(0)
    im:Q=Q(0)
    def __post_init__(self):
        object.__setattr__(self,'re',Q(self.re));object.__setattr__(self,'im',Q(self.im))
    @staticmethod
    def co(x):
        if isinstance(x,K):return x
        if isinstance(x,(int,Q)):return K(x)
        return None
    def __add__(self,x):
        x=K.co(x)
        if x is None:return NotImplemented
        return K(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self):return K(-self.re,-self.im)
    def __sub__(self,x):return self+-x
    def __rsub__(self,x):return -self+x
    def __mul__(self,x):
        x=K.co(x)
        if x is None:return NotImplemented
        return K(self.re*x.re+2*self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def inv(self):
        n=self.re*self.re-2*self.im*self.im;assert n
        return K(self.re/n,-self.im/n)
    def __truediv__(self,x):return self*K.co(x).inv()
    def __rtruediv__(self,x):return K.co(x)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        ans=K(1);x=self
        while n:
            if n&1:ans=ans*x
            x=x*x;n//=2
        return ans
    def norm(self):return self.re*self.re-2*self.im*self.im

class P:
    def __init__(self,x=0):
        if isinstance(x,P):self.d=dict(x.d)
        elif isinstance(x,dict):self.d={m:K.co(c) for m,c in x.items() if K.co(c)!=K(0)}
        else:self.d={} if K.co(x)==K(0) else {():K.co(x)}
    def __add__(self,x):
        x=P(x);out=self.d.copy()
        for m,c in x.d.items():out[m]=out.get(m,K(0))+c
        return P(out)
    __radd__=__add__
    def __neg__(self):return P({m:-c for m,c in self.d.items()})
    def __sub__(self,x):return self+-P(x)
    def __rsub__(self,x):return P(x)+-self
    def __mul__(self,x):
        x=P(x);out={}
        for m,c in self.d.items():
            for n,d in x.d.items():
                mn=tuple(sorted(m+n));out[mn]=out.get(mn,K(0))+c*d
        return P(out)
    __rmul__=__mul__
    def __pow__(self,n):
        assert n>=0;ans=P(1)
        for _ in range(n):ans=ans*self
        return ans
    def components(self):
        return [{m:getattr(c,part) for m,c in self.d.items() if getattr(c,part)} for part in ['re','im']]

def variable(i):return P({(i,):K(1)})
def clean(d):return {m:c for m,c in d.items() if c}
def primitive(d):
    d=clean(d);assert d
    den=lcm(*(Q(c).denominator for c in d.values()))
    ints={m:int(Q(c)*den) for m,c in d.items()}
    content=gcd(*ints.values());sign=1 if ints[min(ints)]>0 else -1
    return {m:sign*c//content for m,c in ints.items()},Q(sign*content,den)
def combine(rows,coeffs):
    out=defaultdict(Q)
    for row,c in zip(rows,coeffs):
        for m,d in row.items():out[m]+=c*d
    return clean(out)
def decode(row):
    ans={(int(t['parameterPower']),tuple(t['monomial'])):int(t['coefficient']) for t in row['terms']}
    assert len(ans)==len(row['terms']) and all(ans.values())
    return ans

def inverse(matrix):
    n=len(matrix);a=[[Q(x) for x in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(matrix)];det=Q(1)
    for j in range(n):
        i=next(i for i in range(j,n) if a[i][j])
        if i!=j:a[i],a[j]=a[j],a[i];det=-det
        piv=a[j][j];det*=piv;a[j]=[x/piv for x in a[j]]
        for i in range(n):
            if i!=j:
                c=a[i][j];a[i]=[x-c*y for x,y in zip(a[i],a[j])]
    return det,[row[n:] for row in a]

HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--tables',type=Path,default=HERE)
parser.add_argument('--source',type=Path,default=REPO/'computation/quartic/abc74_v46/quadratic-family.json')
parser.add_argument('--output',type=Path)
args=parser.parse_args();tables=args.tables
source_bytes=args.source.read_bytes();source_sha=sha256(source_bytes).hexdigest()
assert source_sha=='44499a87b0188f64d7e6d2c01046883a19326c40fa9956dcf31a1eb6e7a142dc'
source=json.loads(source_bytes)
basis=json.loads((tables/'basis-transformation.json').read_text())
quad=json.loads((tables/'quadratic-family.json').read_text())
expanded=json.loads((tables/'polynomial-family.json').read_text())
report=json.loads((tables/'construction-report.json').read_text())
assert quad['variables']==74 and quad['inputCoordinate']==1
assert report['parentQuadraticSha256']==source_sha
assert quad['parentQuadraticSha256']==source_sha

rho=K(0,1);a=1+rho;c=4-2*rho;delta=a-c*c;D=11-6*rho
Delta=(a+delta)**2-4*a*c*c
assert a*delta==D
assert [z.norm() for z in [a,c,delta,Delta]]==[Q(-1),Q(8),Q(-49),Q(-3056)]
u=variable(3)+rho*variable(4);w=variable(5)+rho*variable(6)
h=variable(7)+rho*variable(8);AH=variable(23)+rho*variable(24);BH=variable(25)+rho*variable(26)
v=a*(u+w)+2*c+delta*h
S=a*w+c+delta*h;T=-a*u-c-delta*h
literal=[a*u*w-1,delta*h*h+a*h*(u+w)+2*c*h-1,
         a*AH*(v+delta*w)+2*c*h*u+h-u,
         a*BH*(v+delta*u)+2*c*h*w+h-w,
         a*a*(delta*delta*AH*BH-(1+4*c*w)*AH-(1+4*c*u)*BH)+1-2*(2*a+c*c)*h*h]
raw=[]
for row in literal:
    for component in row.components():raw.append(primitive(component)[0])
assert len(raw)==10 and all(max(map(len,row))<=2 for row in raw)
U=[[int(x) for x in row] for row in basis['referenceMatrix']]
assert len(U)==10 and all(len(row)==10 for row in U)
det,Uinv=inverse(U);assert det in [Q(1),Q(-1)]
assert all(x.denominator==1 for row in Uinv for x in row)
reference=[];ref_scales=[]
for vector in U:
    row,scale=primitive(combine(raw,vector));reference.append(row);ref_scales.append(scale)
for i,row in enumerate(raw):
    recovered=combine(reference,[Uinv[i][j]*ref_scales[j] for j in range(10)])
    assert recovered==row
pre=[{(0,m):z for m,z in row.items()} for row in reference]
names=[f'common.unitGraph.{i}' for i in range(1,11)]
replacements=dict(zip([3,4,5,6],S.components()+T.components()))
source_rows=[row for row in source['residuals'] if not row['name'].startswith('common.primitive.')]
assert len(source_rows)==56
power_changes=0
for src in source_rows:
    row=decode(src)
    if src['name']=='height.betaSquare':
        assert row=={(0,(1,1)):1,(0,(36,)):-4}
        row={(0,(1,1)):1,(0,(36,)):-1};power_changes+=1
    assert not any(7 in m or 8 in m for j,m in row),src['name']
    out=defaultdict(Q)
    for (power,mon),coeff in row.items():
        terms={():Q(coeff)}
        for i in mon:
            sub=replacements.get(i,{(i,):Q(1)});next_terms=defaultdict(Q)
            for m,z in terms.items():
                for n,y in sub.items():next_terms[tuple(sorted(m+n))]+=z*y
            terms=clean(next_terms)
        for m,z in terms.items():out[(power,m)]+=z
    out,scale=primitive(out);pre.append(out);names.append(src['name'])
assert power_changes==1 and len(pre)==66

# Independent complete round trip for the constant-elimination basis.
pivot=int(basis['constantPivotRow'])-1;assert pivot==0
pivot_row=pre[pivot];pivot_const=pivot_row[(0,())];assert pivot_const==1
transform=basis['constantTransformation'];assert len(transform)==66
final=[];expected_transform=[]
for i,row in enumerate(pre):
    mult=0 if i==pivot else row.get((0,()),0)
    result=row.copy()
    if i!=pivot:
        for mon,z in pivot_row.items():result[mon]=result.get(mon,0)-mult*z
    result,scale=primitive(result)
    content=scale.numerator if scale>0 else -scale.numerator
    assert scale.denominator==1
    sign=1 if scale>0 else -1
    expected_transform.append({'row':i+1,'pivotMultiple':mult,'primitiveDivisor':content,'sign':sign})
    final.append(result)
    recovered={mon:z*scale for mon,z in result.items()}
    if i!=pivot:
        for mon,z in pivot_row.items():recovered[mon]=recovered.get(mon,0)+mult*z
    assert clean(recovered)==row
assert transform==expected_transform
assert len(quad['residuals'])==66
for i,(row,name,actual) in enumerate(zip(final,names,quad['residuals'])):
    assert actual['id']==i+1 and actual['name']==name
    assert decode(actual)==row,name
    assert gcd(*row.values())==1
    assert all(0<=j<=1 and len(m)<=2 and all(1<=k<=74 for k in m) for j,m in row)
assert sum(bool(row.get((0,()),0)) for row in final)==1
power_index=names.index('height.betaSquare')
assert final[power_index]=={(0,(1,1)):1,(0,(36,)):-1}

expected_coords=json.loads(json.dumps(source['coordinates']))
for coord in expected_coords:
    name=coord['name']
    if name.startswith('common.S.'):coord['name']=name.replace('common.S.','common.u.')
    if name.startswith('common.T.'):coord['name']=name.replace('common.T.','common.w.')
    if name.startswith('common.f.'):coord['name']=name.replace('common.f.','common.inverseChord.')
assert quad['coordinates']==expected_coords
assert [x['id'] for x in expected_coords]==list(range(1,75))

# Full expansion by unordered term pairs, independent of the producer loop.
poly=defaultdict(int)
for row in final:
    terms=sorted(row.items())
    for i,((j,m),z) in enumerate(terms):
        for k in range(i,len(terms)):
            (jj,mm),zz=terms[k]
            poly[(j+jj,tuple(sorted(m+mm)))]+=z*zz*(1 if k==i else 2)
poly=clean(poly)
assert poly==decode(expanded)
assert expanded['variables']==74 and expanded['degree']==4
assert poly[(0,(1,1,1,1))]==1 and max(len(m) for j,m in poly)==4
assert gcd(*poly.values())==1
profiles=defaultdict(dict)
for (j,m),z in poly.items():profiles[m][j]=z
assert len(profiles)==1695 and len(poly)==1697
assert profiles[()]=={0:1,2:1}
fixed=[(m,abs(v[0])) for m,v in profiles.items() if set(v)=={0}]
fixedmax=max(z for m,z in fixed);assert fixedmax==30568
fixed_at=[list(m) for m,z in fixed if z==fixedmax]
linear=[]
for mon,profile in profiles.items():
    if 1 in profile:
        c1=profile[1];c0=profile.get(0,0)
        assert abs(c1)==2 and abs(c0)<=2 and c1*c0>=0 and set(profile)<= {0,1}
        linear.append({'monomial':list(mon),'coefficientOfB':c1,'fixedCoefficient':c0})
assert len(linear)==4
# Every moving nonconstant coefficient is at most2B+2 in absolute value.
# For B>=3 this is at most B^2+1; for B=1,2 it is below fixedmax30568.
# All fixed and moving coefficients are nonzero for B>=1, and X^4 is1.
assert 2*2+2<fixedmax

# Literal common-source zero-input witness at H=2R0, before row transforms.
vv=(c*c-2*a)/(2*c);uu=1/vv;ww=vv/a;hh=1/vv
point_values={3:uu.re,4:uu.im,5:ww.re,6:ww.im,7:hh.re,8:hh.im,
              23:(vv**-4).re,24:(vv**-4).im,25:(a**-2).re,26:(a**-2).im,
              19:Q(1),21:Q(1)}
def evaluate_row(row):
    out=Q(0)
    for (j,mon),coef in row.items():
        assert j==0
        z=Q(coef)
        for i in mon:z*=point_values.get(i,Q(0))
        out+=z
    return out
common_names=set(names[:10]+[name for name in names if name.startswith(('pair.','ratio.','square.','height.'))])
for row,name in zip(pre,names):
    if name in common_names:assert evaluate_row(row)==0,name

receipt={'status':'PASS','implementation':'Independent standard-library rational-pair sparse arithmetic; no producer imports or LLL rerun',
 'parentQuadraticSha256':source_sha,'variables':74,'quadraticRows':66,'referenceRows':10,'nonreferenceRows':56,
 'referenceMatrixDeterminant':str(det),'referenceInverseIntegral':True,
 'referenceRowNormalizationScales':[str(x) for x in ref_scales],
 'constantBasisRoundTrips':66,'constantPivotRow':1,
 'literalInputEquation':'X^2-b2=0','inputReplacementCount':power_changes,
 'affineReferenceOutputs':'S=a*w+c+delta*h; T=-a*u-c-delta*h',
 'zeroInputCommonWitness':'H=2R0, all seven scaled pair coordinates zero, L=L0=1',
 'degree':4,'contentForEveryIntegerB':1,'ordinaryMonomialsForEveryBAtLeast1':1695,
 'parameterSeparatedTerms':1697,'constantCoefficient':'B^2+1','largestFixedCoefficient':30568,
 'largestFixedCoefficientMonomials':fixed_at,'parameterLinearCoefficients':linear,
 'exactHeightForEveryIntegerBAtLeast1':'max(30568,B^2+1)',
 'fixedConstantNorms':{'a':'-1','c':'8','delta':'-49','Delta':'-3056'},
 'arithmeticTransfer':'Proved separately under the retained premises; this finite certificate checks only equations, changes of basis, expansion and counts.',
 'noNewVariableRecord':True,'noExternalFoundationAudit':True}
blob=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
if args.output:
    args.output.write_text(blob);print(json.dumps({'status':'PASS','output':str(args.output),'height':receipt['exactHeightForEveryIntegerBAtLeast1']}))
else:print(blob,end='')
