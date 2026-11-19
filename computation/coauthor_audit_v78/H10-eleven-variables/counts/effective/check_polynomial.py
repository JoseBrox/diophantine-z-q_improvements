"""Independently replay the explicit 27-variable specialization at L=53."""
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parents[1] / "fewvars" / "check_positive.py"
spec = importlib.util.spec_from_file_location("positive_independent_audit", CHECKER)
module = importlib.util.module_from_spec(spec)
sys.argv = [str(CHECKER), "--output", str(HERE / "explicit53")]
spec.loader.exec_module(module)

# Same independent replay, with the pinned upstream arithmetic at L=53.
def baseline(route):
    assert route == "explicit27"
    return module.make_source(route, 53)

module.ancestor = baseline
if __name__ == "__main__":
    print("Independent detector/guard/separator verification:", module.audit("explicit27"))
