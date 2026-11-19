"""Independently verify the square scale and all compact determinant majorants."""
import argparse
import importlib.util
from pathlib import Path
import sys

here=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--repo",type=Path,default=here.parents[2]/"source")
ap.add_argument("--fewvars",type=Path,default=here.parents[2]/"fewvars")
ap.add_argument("--output",type=Path,default=here/"output")
args=ap.parse_args()
sys.argv=[sys.argv[0],"--repo",str(args.repo),"--output",str(args.output),"--balanced"]
loc=importlib.util.spec_from_file_location("finite_audit",args.fewvars/"check_positive.py")
checker=importlib.util.module_from_spec(loc);loc.loader.exec_module(checker)
old=checker.ancestor("abc11")
m=next(q for q in old["events"] if q["operation"]=="moving_contact_height")
n=m["A"]["numerator"]
assert m["A"]["denominator"]==m["M"]["denominator"]==1
assert old["coefficient_dag"][n]==["pow",m["M"]["numerator"],4]
powers=[row for row in old["coefficient_dag"] if row[:2]==["pow",m["M"]["numerator"]]]
assert sorted(row[2] for row in powers)==[4,8]
for row in powers:row[2]//=2
checker.ancestor=lambda route: old
print(checker.audit("abc11"))
