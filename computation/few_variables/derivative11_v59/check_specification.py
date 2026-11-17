#!/usr/bin/env python3
"""Rebuild the complete circuit and independently check its determinant bounds."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
from build_source import make_source, specification, canonical

loader = importlib.util.spec_from_file_location('independent_v28_bound_audit',
                                               HERE.parent/'unit_norm_v28'/'check.py')
audit = importlib.util.module_from_spec(loader)
loader.loader.exec_module(audit)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'specification_certificate.json')
    args = parser.parse_args()
    source = make_source(3)
    spec = specification(source)
    assert canonical(source) == (HERE/'specification/source.json').read_bytes()
    assert canonical(spec) == canonical(json.loads((HERE/'specification/polynomial.json').read_text()))
    assert source['retained_base_count'] == 10
    assert len([x for x in source['variables'] if x['category']=='retained.point']) == 6
    assert [r['degree'] for r in source['finite_blocks']] == [4,4,4,2]
    assert spec['bounds']['full_rank'] == 128 and spec['bounds']['total_variables'] == 11
    rows = []
    for B in (3,5,81,101):
        member = make_source(B)
        record = audit.structural_check(member,specification(member))
        record['B'] = B
        rows.append(record)
    assert all(row['degree_bound']==5444199553 for row in rows)
    assert spec['bounds']['integer_content']==1
    assert spec['bounds']['support_strict_power_of_two']==309
    report = dict(status='PASS',scope='Exact circuit regeneration and independent iterative support, denominator, square-extraction and degree audit; no infinite arithmetic assertion is inferred from computation.',
                  source_sha256=hashlib.sha256(canonical(source)).hexdigest(),
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  native_nodes=len(source['coefficient_dag']),
                  total_variables=11,full_rank=128,degree_upper_bound=5444199553,
                  degree_strict_power_of_two=33,monomials_strict_power_of_two=309,
                  integer_content=1,uniformity_reason='The fixed parameter B has degree zero and changes no nonconstant exponent in the circuit.',
                  fixtures=rows)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','native_nodes','total_variables','degree_upper_bound')},indent=2))


if __name__=='__main__':
    main()
