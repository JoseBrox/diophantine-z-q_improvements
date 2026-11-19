"""Compile the square-scale ordinary abc variant from the balanced v75 source."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

here=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--repo",type=Path,default=here.parents[2]/"source")
ap.add_argument("--fewvars",type=Path,default=here.parents[2]/"fewvars")
ap.add_argument("--output",type=Path,default=here/"output")
args=ap.parse_args()
s=(args.fewvars/"positive.py").read_text()
target='        if args.balanced:\n            start=text.index("        if i < 2:")'
patch='''        assert text.count("M**(8 if self.contact_count == 7 else 4)")==1
        text=text.replace("M**(8 if self.contact_count == 7 else 4)","M**2")
'''
assert s.count(target)==1
with tempfile.TemporaryDirectory() as d:
    temporary=Path(d)/"square_scale.py"
    temporary.write_text(s.replace(target,patch+target))
    subprocess.run([sys.executable,"-B",str(temporary),"--repo",str(args.repo.resolve()),"--output",str(args.output.resolve()),
        "--termwise","--balanced","--route","abc11"],check=True)
