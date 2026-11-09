#!/usr/bin/env python3
"""Apply the independent finite-algebra checker to the weak-abc source."""
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "active_elimination"))
import check_active_specification as checker

# The shared checker uses one source path per coordinate count.  This family
# also has thirteen coordinates, but a different verified rational source.
# Only that input path changes; every mathematical assertion is retained.
checker.SOURCES[13] = HERE / "certificate/source-polynomial-specification.json"

if __name__ == "__main__":
    checker.main()
