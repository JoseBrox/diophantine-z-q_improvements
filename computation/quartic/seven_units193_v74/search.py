#!/usr/bin/env python3
"""Optional unbounded integral-weight search for the seven-unit chart.

Requires z3-solver. No solver is needed to check the stored exact certificate.
The factors are fixed to the independently audited v73 assignments.
"""
from pathlib import Path
from hashlib import sha256
import argparse,itertools,json,time
import z3
HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--timeout-ms',type=int,default=60000)
    ap.add_argument('--output',type=Path,default=HERE/'search-result.json')
    args=ap.parse_args();raw=(HERE/'coordinate-model.json').read_bytes();D=json.loads(raw);previous=json.loads((HERE/'laurent-certificate.json').read_text())
    units=[(0,0)]+[tuple(e)for e in D['base_units'].values()]
    options={k:set(tuple(sum(q[j]for q in seq)for j in(0,1))for seq in itertools.product(units,repeat=k))for k in range(3)}
    weights={i:[z3.Int(f'w{i}_{j}')for j in(0,1)]for i in D['active']}
    rowweights={row['name']:[z3.Int(f'r{k}_{j}')for j in(0,1)]for k,row in enumerate(D['rows'])}
    solver=z3.Solver();solver.set(timeout=args.timeout_ms);solver.add(*[weights[1][j]==0 for j in(0,1)])
    def term(name,monomial,exponent):
        v=[exponent[j]+sum(weights[i][j]for i in monomial)-rowweights[name][j]for j in(0,1)]
        return z3.Or(*[z3.And(*[v[j]==e[j]for j in(0,1)])for e in options[2-len(monomial)]])
    for row in D['rows']:solver.add(*[term(row['name'],m,e)for m,e in row['terms']])
    for det in(0,1):
        assignment=previous['assignments'][str(det)]
        for label,(i,e,b)in D['quadratic_tests'].items():
            slot=assignment['quadratic'][label];power=b+2*(slot%2);name=D['rows'][D['factor_rows'][f'{det},{slot//2}']]['name'];exponent=(e[0]+power,e[1]+det*power)
            solver.add(*[term(name,(i+a,i+b),exponent)for a,b in[(0,0),(0,1),(1,1)]])
        for label,(i,e)in D['linear_tests'].items():
            slot=assignment['linear'][label];power=2 if slot<4 else slot-3;name=D['rows'][D['factor_rows'][f'{det},{slot if slot<4 else 4}']]['name'];exponent=(e[0]+power,e[1]+det*power)
            solver.add(*[term(name,(i+a,),exponent)for a in(0,1)])
    names=json.loads((HERE/'source/reference-row-map.json').read_text())['names']
    for name in names:solver.add(rowweights[name][0]==2,rowweights[name][1]==2)
    start=time.monotonic();status=solver.check();report={'schema':'seven-unit193-search/v74','model_sha256':sha256(raw).hexdigest(),'status':str(status),'seconds':time.monotonic()-start,'integer_weights_unbounded':True,'coordinates':193,'solver':z3.get_version_string(),'assignments':previous['assignments']}
    if status==z3.sat:
        model=solver.model();report['weights']={str(i):[model.eval(v,model_completion=True).as_long()for v in pair]for i,pair in weights.items()};report['row_weights']={name:[model.eval(v,model_completion=True).as_long()for v in pair]for name,pair in rowweights.items()}
    elif status==z3.unknown:report['reason_unknown']=solver.reason_unknown()
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in['weights','row_weights','assignments']},indent=2))
if __name__=='__main__':main()
