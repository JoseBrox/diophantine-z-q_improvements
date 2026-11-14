#!/usr/bin/env python3
"""Exact diagonal balancing of the corrected 200-variable quadratic family."""
from __future__ import annotations
import argparse,copy,json
from pathlib import Path
from collections import defaultdict
from build import parse,serialize,primitive,add,square,need
HERE=Path(__file__).resolve().parent

def make(source:Path,output:Path):
    system=json.loads(source.read_text());rows=[]
    for row in system['residuals']:
        raw=parse(row);q=defaultdict(int)
        least=min(2*a+sum(i in (117,118) for i in m) for a,m in raw)
        for (a,m),c in raw.items():
            q[2*a+sum(i in (117,118) for i in m)-least,m]+=c*149**a
        q=primitive(q)
        need(max(a for a,m in q)<=1,'Unexpected parameter degree')
        need(max(len(m) for a,m in q)<=2,'Not quadratic')
        rows.append(dict(id=row['id'],name=row['name'],terms=serialize(q)))
    system=copy.deepcopy(system);system['residuals']=rows
    system['format']='integer-quadratic-family-balanced200-v33'
    system['fixedParameter']={'symbol':'C','value':'149^N','quantified':False,'domain':'N integer >=1','definingThreshold':'ineffective'}
    system.pop('parameter',None)
    full={}
    for row in rows:full=add(full,square(parse(row)))
    polynomial={k:v for k,v in system.items() if k!='residuals'}
    polynomial.update(format='integer-quartic-family-balanced200-v33',degree=4,terms=serialize(full))
    output.mkdir(parents=True,exist_ok=True)
    for name,obj in [('balanced-quadratic.json',system),('balanced-polynomial.json',polynomial)]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=HERE/'quadratic-family.json');ap.add_argument('--output',type=Path,default=HERE)
    args=ap.parse_args();make(args.source,args.output)
