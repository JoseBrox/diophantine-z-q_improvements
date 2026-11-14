#!/usr/bin/env python3
"""Run pinned legacy scripts with Python 3.12 AST/gzip serialization on Python 3.13.

Python 3.13's ast.dump defaults to omitting empty fields. The frozen source
fingerprints include those fields. This restores only that serialization
choice. It does not change parsing, source bytes, arithmetic, or assertions.
The mtime-zero gzip path also uses the same zlib gzip header as Python 3.12.
Native Python 3.12 remains the preferred release/CI environment.

Example: ./scripts/python313_legacy_compat.py -B scripts/verify.py --full
"""
import ast
import gzip
import zlib
from pathlib import Path
import runpy
import sys

if sys.version_info[:2] != (3, 13):
    raise SystemExit('This compatibility runner is only for Python 3.13; use native Python 3.12 directly.')
_original_dump = ast.dump

def _python312_dump(node, annotate_fields=True, include_attributes=False, *, indent=None, show_empty=True):
    return _original_dump(node, annotate_fields=annotate_fields,
        include_attributes=include_attributes, indent=indent, show_empty=show_empty)

ast.dump = _python312_dump
_original_compress = gzip.compress

def _python312_compress(data, compresslevel=9, *, mtime=None):
    # CPython 3.12 delegates its mtime=0 case to zlib (OS header byte 3 here).
    if mtime == 0:
        return zlib.compress(data, level=compresslevel, wbits=31)
    return _original_compress(data, compresslevel=compresslevel, mtime=mtime)

gzip.compress = _python312_compress
sys.dont_write_bytecode = True
runner = str(Path(__file__).resolve())
args = sys.argv[1:]
if args and args[0] == '-B':
    args = args[1:]
if not args or args[0].startswith('-'):
    raise SystemExit('Usage: python313_legacy_compat.py [-B] script.py [script arguments]')
script = Path(args[0]).resolve()
sys.executable = runner  # Child legacy scripts use the same serialization mode.
sys.argv = [str(script), *args[1:]]
sys.path.insert(0, str(script.parent))
runpy.run_path(str(script), run_name='__main__')
