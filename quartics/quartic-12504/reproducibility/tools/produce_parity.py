# Generated locator adapter; --repo names the isolated adapter directory.
"""Untrusted producer. Run on norm-base or another unsimplified initial lift."""
import argparse
from collections import defaultdict
import gzip
import json
from pathlib import Path
import sys


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--parent',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--diagnostic-only',action='store_true')
    a=p.parse_args()
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from export_artifact import export,enc
    import polynomial_ops as poly
    records=[json.loads(line) for line in gzip.decompress((a.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    initial=records[0]
    allocated=records[-1]['allocated_variables']
    records=[r for r in records if r['kind'] not in ('weights','final')]
    rows=[{tuple(m):c for c,m in r} for r in json.loads(gzip.decompress((a.parent/'candidate-rows.json.gz').read_bytes()))]
    initial_rows=[{tuple(m):c for c,m in r} for r in initial['rows']]
    gates={g['variable']:(initial['source_rows']+i,tuple(g['product'])) for i,g in enumerate(initial['gates'])}
    incidence=defaultdict(set)
    for i,row in enumerate(rows):
        for v in poly.vars_in(row):incidence[v].add(i)
    instances=json.loads((a.repo/'construction-map.json').read_text())['instantiations']
    report=[]
    for inst in instances:
        if inst['module']!='q_primeparity':continue
        b=inst['arguments'][0]
        old=list(range(inst['first_local'],inst['first_local']+7))
        ids=list(range(inst['first_residual'],inst['first_residual']+4))
        closure=set()
        def visit(v):
            if v in gates and v not in closure:
                closure.add(v)
                for w in gates[v][1]:visit(w)
        for i in ids:
            for v in poly.vars_in(initial_rows[i]):visit(v)
        defs=[[gates[v][0],v] for v in sorted(closure)]
        selected=set(ids)|{i for i,v in defs}
        unchanged=all(rows[i]==initial_rows[i] for i in selected)
        outside={v:sorted(incidence[v]-selected) for v in set(old)|closure if incidence[v]-selected}
        summary={'path':inst['path'],'source_witnesses':7,'lift_gates':len(closure),
                 'old_private_variables':7+len(closure),'new_private_variables':12,
                 'raw_saving':7+len(closure)-12,'unchanged':unchanged,'outside':outside,
                 'rows':sorted(selected)}
        report.append(summary)
        if a.diagnostic_only:continue
        assert unchanged and not outside,summary
        new=list(range(allocated,allocated+12));allocated+=12
        u,v,x,z,e,pv,c,w,s,q,j,k=new
        def r(*terms):
            row={}
            for coeff,*mon in terms:
                key=tuple(sorted(mon));row[key]=row.get(key,0)+coeff
            return dict(poly.primitive({m:coeff for m,coeff in row.items() if coeff}))
        replacements=[r((1,z),(-1,u,u)),r((1,x),(-1,b,v)),
            r((1,z),(1,v,x),(-1,b,b)),r((1,c),(-1,b,e)),
            r((1,pv,pv),(-17,b),(-34,c),(51,e,c)),
            r((1,w),(-17,b,c),(1,c,z)),r((1,j),(-1,s,s)),
            r((1,k),(-1,b,q)),r((1,j,j),(34,j,w),(-867,w,w),(-17,q,k))]
        assert len(selected)>=len(replacements)
        patches={i:{} for i in selected}
        for i,row in zip(sorted(selected),replacements):patches[i]=row
        for i,row in patches.items():
            for v0 in poly.vars_in(rows[i]):incidence[v0].remove(i)
            rows[i]=row
            for v0 in poly.vars_in(row):incidence[v0].add(i)
        records.append({'kind':'parity_conic','data':{'input':b,'old_witnesses':old,
            'residual_rows':ids,'definitions':defs,'new_variables':new},
            'patches':[[i,enc(row)] for i,row in sorted(patches.items())]})
    summary={'instances':len(report),'raw_total_saving':sum(r['raw_saving'] for r in report),
             'all_unchanged':all(r['unchanged'] for r in report),'all_private':all(not r['outside'] for r in report),
             'details':report}
    if a.diagnostic_only:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(summary,indent=2)+'\n')
    else:
        result=export(a.output,a.parent/'source-residuals.jsonl.gz',rows,records,allocated,
            {'parity_replacements':len(report),'parity_raw_saving':summary['raw_total_saving']})
        (a.output/'parity-diagnostic.json').write_text(json.dumps(summary,indent=2)+'\n')
        summary['export']=result
    print(json.dumps({k:v for k,v in summary.items() if k!='details'},indent=2),flush=True)


if __name__=='__main__':main()
