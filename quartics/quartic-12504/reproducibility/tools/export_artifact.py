"""Serialize an untrusted algebraic candidate for the separate checker."""
from collections import Counter
from pathlib import Path
import gzip,hashlib,json,shutil
import polynomial_ops as p

def enc(row):return [[c,list(m)] for m,c in row.items()]
def raw(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode('ascii')

def export(out,source,rows,records,allocated,extra=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    poly={}
    for row in rows:p.poly_add(poly,p.square(row))
    freq=Counter(v for m in poly for v in m)
    active=[0]+sorted(set(freq)-{0},key=lambda v:(-freq[v],v))
    assert set(active)==set().union(*(p.vars_in(row) for row in rows))
    mapping={v:i for i,v in enumerate(active)}
    compact=[{tuple(sorted(mapping[v] for v in m)):c for m,c in row.items()} for row in rows if row]
    final={}
    for row in compact:p.poly_add(final,p.square(row))
    report={'witnesses':len(active)-1,'variables':len(active),'rows':len(compact),
            'degree':max(map(len,final)),'monomials':len(final),
            'max_abs_coefficient':max(map(abs,final.values())),
            'status':'CANDIDATE: independent verification pending',**(extra or {})}
    assert report['degree']==4 and report['max_abs_coefficient']<2**80
    records=records+[{'kind':'weights','values':[1]*len(rows)},
        {'kind':'final','allocated_variables':allocated,'report':report,
         'rows_sha256':hashlib.sha256(raw([enc(row) for row in rows])).hexdigest()}]
    shutil.copyfile(source,out/'source-residuals.jsonl.gz')
    for name,value in [('candidate-rows.json.gz',raw([enc(row) for row in rows])),
                       ('residuals.json.gz',raw([enc(row) for row in compact])),
                       ('certificate.jsonl.gz',b''.join(raw(record)+b'\n' for record in records))]:
        (out/name).write_bytes(gzip.compress(value,compresslevel=1,mtime=0))
    (out/'variable-map.json').write_bytes(raw(active)+b'\n')
    (out/'weights.json').write_bytes(raw([1]*len(compact))+b'\n')
    expanded=b'# coefficient followed by repeated variable indices; input is variable 0\n'+b''.join(
        (' '.join(map(str,(c,*m)))+'\n').encode('ascii') for m,c in sorted(final.items()))
    (out/'polynomial.expanded.txt').write_bytes(expanded)
    (out/'polynomial.expanded.txt.gz').write_bytes(gzip.compress(expanded,compresslevel=1,mtime=0))
    (out/'producer-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
