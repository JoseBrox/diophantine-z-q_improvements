"""Run the algebraic verifications and the modular descent using the bundled sources."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parent
def run(script, *args):
    subprocess.run([sys.executable, "-B", str(root / script), *map(str, args)], check=True, cwd=root)
run("eight_cusps.py")
run("counts/selector/eight_contacts.py")
run("counts/poles/check_weak11.py")
run("counts/poles/ordinary_scale/check.py")
run("counts/points/check_single_pole.py")
run("counts/realization/check.py")
run("counts/realization/hasse-failure.py")
run("counts/abc/verify.py")
run("counts/abc/quartics/verify.py", "--parent", root / "abc/shared/record62/quadrics.json")
run("counts/effective/check_L53.py")
run("counts/effective/check_polynomial.py")
run("counts/effective/check_compact.py")
print("All listed verification procedures passed.")
