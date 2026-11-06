#!/usr/bin/env python3
"""Print concise, verifiable comparison from data/polynomial_benchmarks.json."""
from pathlib import Path
import json
p=Path(__file__).resolve().parents[1]/'data/polynomial_benchmarks.json'
rows=json.loads(p.read_text())['rows']
head=('id','variables','degree','size_metric','height')
widths={k:max(len(k),*(len(str(row[k])) for row in rows)) for k in head}
print(' | '.join(k.ljust(widths[k]) for k in head))
print('-+-'.join('-'*widths[k] for k in head))
for r in rows:print(' | '.join(str(r[k]).ljust(widths[k]) for k in head))
