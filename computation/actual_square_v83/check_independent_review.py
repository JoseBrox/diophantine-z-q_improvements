#!/usr/bin/env python3
"""Run the frozen independent review with its source directory relocated."""
from pathlib import Path
import hashlib
import json

PACKAGE=Path(__file__).resolve().parent
FROZEN=PACKAGE/'independent_review'
review=json.loads((FROZEN/'manual_review.json').read_text())
assert review['status']=='PASS'
for name,digest in review['source_pins'].items():
    assert hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest()==digest,name
for name,digest in review['review_files'].items():
    assert hashlib.sha256((FROZEN/name).read_bytes()).hexdigest()==digest,name
source=(FROZEN/'check_review.py').read_text()
old="base=Path('/workspace/scratch/7ac4dd889cf6/v83_search25')"
assert source.count(old)==1
source=source.replace(old,'base=Path('+repr(str(PACKAGE))+')',1)
exec(compile(source,str(FROZEN/'check_review.py'),'exec'),
     {'__name__':'__main__','__file__':str(FROZEN/'check_review.py')})
