#!/usr/bin/env python3
"""Literal 204-to-200 quadratic transformation, with exact coefficient expansion.

The arithmetic parameter is retained verbatim from the pinned source. It is a
coefficient, not a quantified coordinate. No defining numerical threshold is
claimed by this generator.
"""
from __future__ import annotations
import argparse, copy, hashlib, json
from collections import defaultdict
from fractions import Fraction as Q
from math import gcd, lcm
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)
def const(a):return {(0,()):Q(a)} if a else {}
def variable(i):return {(0,(i,)):Q(1)}
def add(*args):
    out=defaultdict(Q)
    for arg in args:
        for key,value in arg.items():out[key]+=value
    return {key:value for key,value in out.items() if value}
def scale(a,k):return {key:value*Q(k) for key,value in a.items() if value*Q(k)}
def subtract(a,b):return add(a,scale(b,-1))
def multiply(a,b):
    out=defaultdict(Q)
    for (i,m),x in a.items():
        for (j,n),y in b.items():out[(i+j,tuple(sorted(m+n)))]+=x*y
    return {key:value for key,value in out.items() if value}
def square(a):return multiply(a,a)
def primitive(a):
    need(bool(a),'Zero residual')
    den=lcm(*(v.denominator for v in a.values()))
    content=gcd(*(int(v*den) for v in a.values()))
    if a[min(a)]<0:content=-content
    return scale(a,Q(den,content))
def parse(row):
    out=defaultdict(Q)
    for t in row['terms']:out[(int(t['parameterPower']),tuple(map(int,t['monomial'])))]+=Q(t['coefficient'])
    return {key:value for key,value in out.items() if value}
def serialize(a):return [dict(parameterPower=i,monomial=list(m),coefficient=str(c)) for (i,m),c in sorted(a.items())]
def substitute(a,replacements):
    ans={}
    for (i,m),c in a.items():
        term={(i,()):c}
        for j in m:term=multiply(term,replacements.get(j,variable(j)))
        ans=add(ans,term)
    return ans

def field(i):return (variable(i),variable(i+1))
def kconst(a,b=0):return (const(a),const(b))
def kadd(*xs):return (add(*(x[0] for x in xs)),add(*(x[1] for x in xs)))
def kscale(x,c):return (scale(x[0],c),scale(x[1],c))
def ksub(x,y):return kadd(x,kscale(y,-1))
def kmul(x,y):return (add(multiply(x[0],y[0]),scale(multiply(x[1],y[1]),2)),add(multiply(x[0],y[1]),multiply(x[1],y[0])))
def ksq(x):return kmul(x,x)

def build(source:Path,output:Path):
    parent=json.loads(source.read_text())
    need(parent['variables']==204 and len(parent['residuals'])==186,'Parent is not the pinned 204-variable, 186-row format')
    need([int(v['id']) for v in parent['coordinates']]==list(range(1,205)),'Parent coordinate order')
    need([int(v['id']) for v in parent['residuals']]==list(range(1,187)),'Parent row order')
    deleted=set(range(169,183))
    coordinates=copy.deepcopy(parent['coordinates'])
    for start,name in [(205,'pair4.f'),(207,'pair4.h'),(209,'pair4.g'),(211,'pair4.k'),(213,'pair4.slope')]:
        for j in (0,1):coordinates.append({'id':start+j,'name':name+'.'+str(j)})
    coordinates=[c for c in coordinates if int(c['id']) not in deleted]
    remap={int(c['id']):i+1 for i,c in enumerate(coordinates)}
    for c in coordinates:c['id']=remap[int(c['id'])]
    f,h,g,k,s=map(field,(205,207,209,211,213))
    FF=(variable(60),scale(variable(61),2));GG=(variable(29),scale(variable(30),2))
    S=field(19);TH=field(183);DD=kconst(11,-6);one=kconst(1)
    L=ksub(field(43),kconst(Q(1,2)));L0=ksub(field(45),kconst(Q(1,2)))
    x4=kadd(ksq(s),kmul(DD,kadd(f,g)))
    new_equations=[
        ('pair4.fSquare',ksub(FF,ksq(f))),
        ('pair4.gSquare',ksub(GG,ksq(g))),
        ('pair4.curve',kadd(ksq(h),kscale(f,-1),kmul(DD,kmul(f,FF)))),
        ('pair4.secant',ksub(kmul(s,ksub(f,g)),kadd(h,k))),
        ('pair4.tangent',kadd(kmul(s,ksub(h,k)),kscale(one,-1),kmul(DD,kadd(FF,kmul(f,g),GG)))),
        ('pair4.primary.raw',kadd(kmul(h,L),kscale(kmul(f,S),2))),
        ('pair4.primary.regular',kadd(kmul(ksub(one,kmul(DD,FF)),L),kscale(kmul(h,S),2))),
        ('pair4.alternate.raw',kadd(kmul(k,L0),kscale(kmul(g,TH),2))),
        ('pair4.alternate.regular',kadd(kmul(ksub(one,kmul(DD,GG)),L0),kscale(kmul(k,TH),2)))]
    oldroot=add(square(subtract(variable(173),variable(175))),scale(square(subtract(variable(174),variable(176))),2))
    affine={35:add(scale(variable(35),Q(1,2)),scale(variable(118),-1)),36:scale(variable(36),Q(1,2)),
            37:add(scale(variable(37),Q(1,2)),scale(variable(118),-1)),38:scale(variable(38),Q(1,2))}
    rows=[];incidences=[];changed=[]
    def append(name,a):
        need(all(not deleted.intersection(m) for _,m in a),'Deleted coordinate survived: '+name)
        a={(p,tuple(sorted(remap[i] for i in m))):c for (p,m),c in a.items()}
        a=primitive(a)
        need(max(len(m) for _,m in a)<=2,'Nonquadratic row: '+name)
        rows.append({'id':len(rows)+1,'name':name,'terms':serialize(a)})
    for row in parent['residuals']:
        rid=int(row['id']);a=parse(row)
        if any(deleted.intersection(m) for _,m in a):incidences.append(rid)
        if 122<=rid<=139:continue
        if 104<=rid<=121:
            a=substitute(a,affine);changed.append(rid)
        if rid==144:
            coefficient=a.get((0,(173,173)))
            need(coefficient is not None and coefficient!=0,'Aggregate coefficient missing')
            actual={key:c for key,c in a.items() if deleted.intersection(key[1])}
            need(actual==scale(oldroot,coefficient),'Aggregate differs from its specified old point contribution')
            a=add(a,scale(oldroot,-coefficient),scale(x4[0],4*coefficient));changed.append(rid)
        append(row.get('name','retained.row'+str(rid)),a)
    need(incidences==list(range(122,140))+[144],'Unexpected external use of the removed point block')
    need(len(rows)==168,'Retained row count')
    for name,equation in new_equations:
        append(name+'.0',equation[0]);append(name+'.1',equation[1])
    need(len(coordinates)==200 and len(rows)==186,'New counts')
    full={}
    for row in rows:full=add(full,square(parse(row)))
    need(max(len(m) for _,m in full)==4,'Exact quartic degree')
    need(full.get((0,(191,191,191,191)))==1,'Unit fourth-power coefficient')
    need(all(c.denominator==1 for c in full.values()),'Integer coefficients')
    need({i for _,m in full for i in m}==set(range(1,201)),'A declared coordinate is unused')
    metadata={key:copy.deepcopy(value) for key,value in parent.items() if key not in ('coordinates','residuals','variables','format','terms','degree')}
    quadratic=dict(metadata,format='integer-quadratic-family-shifted200-v33',variables=200,coordinates=coordinates,residuals=rows)
    quartic=dict(metadata,format='integer-quartic-family-shifted200-v33',variables=200,degree=4,coordinates=coordinates,terms=serialize(full))
    report=dict(schema='shifted200-construction/v33',variables=200,quadratic_rows=186,degree=4,integer_content=1,
                parameter_separated_terms=len(full),coordinate_monomials=len({m for _,m in full}),
                source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                removed_coordinate_ids=list(range(169,183)),removed_row_ids=list(range(122,140)),
                affine_changed_parent_rows=list(range(104,122)),aggregate_parent_row=144,
                new_row_count=18,old_to_new_coordinate_map={str(k):v for k,v in remap.items()},
                defining_threshold='Ineffective, sufficiently large fixed coefficient exponent; no numerical defining member asserted',
                inherited_arithmetic_verified_by_computation=False,
                scope='Complete finite coefficient specification; the mathematical arithmetic argument is a separate TeX proof.')
    output.mkdir(parents=True,exist_ok=True)
    for name,obj in [('quadratic-family.json',quadratic),('polynomial-family.json',quartic),('construction-report.json',report)]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'computation/quartic/reciprocal204_v27/unbalanced-quadratic.json')
    p.add_argument('--output',type=Path,default=HERE)
    a=p.parse_args();build(a.source,a.output)
