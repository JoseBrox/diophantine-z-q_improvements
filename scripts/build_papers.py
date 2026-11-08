#!/usr/bin/env python3
"""Build the nine standalone papers with a standard pdflatex installation."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    engine = shutil.which('pdflatex')
    if not engine:
        raise SystemExit('pdflatex is required; see docs/reproducibility.md')
    sources = sorted((ROOT/'papers').glob('*/*.tex'))
    assert len(sources) == 9
    environment = dict(os.environ)
    environment.setdefault('SOURCE_DATE_EPOCH','1794096000')
    environment.setdefault('FORCE_SOURCE_DATE','1')
    with tempfile.TemporaryDirectory(prefix='diophantine-papers-') as directory:
        for source in sources:
            work = Path(directory)/source.stem
            work.mkdir()
            shutil.copyfile(source, work/source.name)
            for _ in range(3):
                result = subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error',source.name],
                                        cwd=work,env=environment,capture_output=True,text=True)
                if result.returncode:
                    raise SystemExit(result.stdout[-5000:])
            log = (work/(source.stem+'.log')).read_text(errors='replace')
            if re.search(r'undefined|multiply defined|Overfull|Rerun to get cross-references right',log):
                raise SystemExit(source.name+': unresolved reference or layout issue\n'+log[-5000:])
            shutil.copyfile(work/(source.stem+'.pdf'),source.with_suffix('.pdf'))
            print(source.stem+': PASS')


if __name__ == '__main__':
    main()
