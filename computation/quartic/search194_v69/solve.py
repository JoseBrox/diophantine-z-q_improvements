#!/usr/bin/env python3
"""Reproduce three explicitly scoped194-coordinate support searches.

Requires z3-solver==5.4.1.0. This is a search ledger, not a polynomial
producer or a general lower-bound proof.
"""
from pathlib import Path
from hashlib import sha256
import argparse,itertools,json,time
import z3

ROOT=Path(__file__).resolve().parent


def solve(path,timeout):
    raw=path.read_bytes();data=json.loads(raw)
    active=data['active'];rows=data['rows']
    quad=data['quadratic_tests'];linear=data['linear_tests']
    factors={tuple(map(int,k.split(','))):v for k,v in data['factor_rows'].items()}
    ev=(z3.Int('extra_u'),z3.Int('extra_v'))
    P=[(0,0)]+[tuple(e)for e in data['base_units'].values()]+[ev]
    options={k:[tuple(sum(a[d]for a in seq)for d in range(2))for seq in itertools.product(P,repeat=k)]for k in range(3)}
    w={i:[z3.Int(f'w{i}_{d}')for d in range(2)]for i in active}
    r={j:[z3.Int(f'r{j}_{d}')for d in range(2)]for j in range(len(rows))}
    s=z3.Solver();s.set(timeout=timeout)
    s.add(z3.Or(*[z3.And(ev[0]==e[0],ev[1]==e[1])for e in data['extra_unit_candidates']]))
    s.add(*[v==0 for v in w[1]])
    def term(j,m,e):
        v=[e[d]+sum(w[i][d]for i in m)-r[j][d]for d in range(2)]
        return z3.Or(*[z3.And(*[v[d]==o[d]for d in range(2)])for o in options[2-len(m)]])
    for j,row in enumerate(rows):s.assert_and_track(z3.And(*[term(j,m,e)for m,e in row['terms']]),f'row{j}')
    positions={}
    for det in (0,1):
        qp={label:z3.Int(f'qpos{det}_{label}')for label in quad}
        lp={label:z3.Int(f'lpos{det}_{label}')for label in linear}
        positions[det]=(qp,lp)
        s.add(z3.Distinct(*qp.values()),*[z3.And(v>=0,v<8)for v in qp.values()])
        s.add(z3.Distinct(*lp.values()),*[z3.And(v>=0,v<7)for v in lp.values()])
        # Retain the stated ordering normalization: C2 in factor0, either parity.
        s.add(qp['C2']<2)
        for label,(variable,e,basepower)in quad.items():
            cs=[]
            for slot in range(8):
                j=factors[det,slot//2];power=basepower+2*(slot%2)
                ee=(e[0]+power,e[1]+det*power)
                ms=[tuple(variable+c for c in cc)for cc in itertools.combinations_with_replacement(range(2),2)]
                cs.append(z3.Implies(qp[label]==slot,z3.And(*[term(j,m,ee)for m in ms])))
            s.assert_and_track(z3.And(*cs),f'qplace{det}_{label}')
        for label,(variable,e)in linear.items():
            cs=[]
            for slot in range(7):
                j=factors[det,slot if slot<4 else 4];power=2 if slot<4 else slot-3
                ee=(e[0]+power,e[1]+det*power)
                cs.append(z3.Implies(lp[label]==slot,z3.And(*[term(j,(variable+c,),ee)for c in range(2)])))
            s.assert_and_track(z3.And(*cs),f'lplace{det}_{label}')
    start=time.monotonic();status=s.check();elapsed=time.monotonic()-start
    report=dict(schema='exploratory-support194-result/v69',model=path.name,model_sha256=sha256(raw).hexdigest(),status=str(status),seconds=elapsed,solver=z3.get_version_string(),timeout_ms=timeout,integer_weights_unbounded=True,nominal_coordinates=len(active)+len(data['base_units'])+1,extra_unit_candidates=len(data['extra_unit_candidates']),scope='Only the literal support model, fixed common field-row multipliers and enumerated choices in the named JSON file. No general quartic lower bound.')
    if status==z3.unsat:
        report['unsat_core']=[rows[int(str(c)[3:])]['name']if str(c).startswith('row')else str(c)for c in s.unsat_core()]
    elif status==z3.sat:
        model=s.model()
        report['extra_unit']=[model.eval(v).as_long()for v in ev]
        report['weights']={str(i):[model.eval(v,model_completion=True).as_long()for v in ww]for i,ww in w.items()}
        report['row_weights']={row['name']:[model.eval(v,model_completion=True).as_long()for v in r[j]]for j,row in enumerate(rows)}
        report['assignments']={str(det):dict(quadratic={label:model.eval(v).as_long()for label,v in qp.items()},linear={label:model.eval(v).as_long()for label,v in lp.items()})for det,(qp,lp)in positions.items()}
    else:report['reason_unknown']=s.reason_unknown()
    return report


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model',choices=['A4_B4','A1_B3','A1_A3'])
    ap.add_argument('--timeout-ms',type=int,default=60000)
    ap.add_argument('--output',type=Path,default=ROOT/'rerun.json')
    args=ap.parse_args()
    reports=[]
    for name in([args.model]if args.model else['A4_B4','A1_B3','A1_A3']):
        result=solve(ROOT/'models'/(name+'.json'),args.timeout_ms);reports.append(result)
        print(json.dumps({k:v for k,v in result.items()if k not in('unsat_core','weights','row_weights','assignments')}),flush=True)
    args.output.write_text(json.dumps(dict(schema='exploratory-support194-rerun/v69',results=reports),indent=2)+'\n')


if __name__=='__main__':main()
