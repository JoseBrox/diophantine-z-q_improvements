#!/usr/bin/env python3
"""Rebuild and independently verify the complete fixed-prime specification.

Run with Python 3.10 or newer. Only the Python standard library is required.
All paths are relative to this script; no network or earlier release is used.
"""
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
steps=[
    ['build_forced_prime_source.py','--output','source.json.gz'],
    ['check_forced_prime_source.py'],
    ['verify_explicit_height_constant.py'],
    ['compile_source.py','source.json.gz','--output','.'],
    ['verify_specification.py','source.json.gz','polynomial-specification.json'],
    ['verify_bound_equality.py'],
]
for step in steps:
    subprocess.run([sys.executable,*step],cwd=HERE,check=True)
print('All fixed-prime source, exact height-constant and polynomial checks passed.')
