"""Generate a proposed source package, never authorize or modify its source pin."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
from reciprocal_kernel import install

sys.dont_write_bytecode = True

ORIGINAL_BUILDER_SHA256 = 'c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912'
ORIGINAL_COMPARISON_SHA256 = '639574951f42451345b3286a57ca922273567f20a548ee2426939c7a30a07212'


def check_original_comparison(b):
    """Reproduce the complete pinned comparison JSON before any changes."""
    b.CURVE_DROOT = (3, -1)
    b.CURVE_D2 = (11, -6)
    b.CHART = 10
    b.LOG_BLOCK = 2
    captured = {}
    original_save = b.M.save
    def save(m, **metadata):
        captured.update(name=m.name, free=m.free, locals=m.count-m.free,
                        residuals=m.rows, calls=m.calls, construction_log=m.operations, **metadata)
    b.M.save = save
    try:
        b.make_multi_comparison()
    finally:
        b.M.save = original_save
    encoded = json.dumps(captured, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')+b'\n'
    if hashlib.sha256(encoded).hexdigest() != ORIGINAL_COMPARISON_SHA256:
        raise ValueError('Complete original comparison module did not regenerate exactly')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--builder', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--high', type=int, choices=(52, 64), default=64)
    p.add_argument('--label', type=int, choices=(13, 16, 64), default=64)
    p.add_argument('--compressed-primary-charts', action='store_true')
    p.add_argument('--hscale', type=int, choices=(1, 2, 3, 4), default=1)
    args = p.parse_args()
    if (args.high, args.label) not in ((64, 64), (64, 16), (52, 13), (52, 16)):
        raise ValueError('Unsupported precision pair')
    if hashlib.sha256(args.builder.read_bytes()).hexdigest() != ORIGINAL_BUILDER_SHA256:
        raise ValueError('Original builder does not have the reviewed pinned digest')
    spec = importlib.util.spec_from_file_location('isolated_original_source', args.builder)
    b = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b)
    check_original_comparison(b)
    args.out.mkdir(parents=True, exist_ok=False)
    install(b, high=args.high, label=args.label, compressed=args.compressed_primary_charts, hscale=args.hscale)
    sys.argv = [str(args.builder), '--out', str(args.out.resolve()), '--chart', '10', '--parity', '7',
                '--base-gates', '--unit-scale', '--log-block', '2']
    b.main()
    compiler = args.out/'compiler'
    compiler.mkdir()
    files = [args.builder.resolve(), Path(__file__).resolve(), Path(__file__).with_name('reciprocal_kernel.py').resolve()]
    hashes = {}
    for path in files:
        target = compiler/path.name
        shutil.copyfile(path, target)
        hashes[target.name] = hashlib.sha256(target.read_bytes()).hexdigest()
    contract = {'status': 'PROPOSED SOURCE; INDEPENDENT MATHEMATICAL REVIEW REQUIRED',
                'source_pin_authorized': False, 'compiler_sha256': hashes,
                'original_builder_digest_matched': ORIGINAL_BUILDER_SHA256,
                'complete_original_comparison_regenerated': ORIGINAL_COMPARISON_SHA256,
                'high_precision': args.high, 'label_precision': args.label,
                'anchor_squarings': b.ANCHOR_SQUARINGS,
                'scalar_orders': [1,1,1,1,48,48],
                'logarithm': 'z * G(D*f^2), f=1/x, coefficients in RECIPROCAL_PROOF.md',
                'compressed_primary_charts': args.compressed_primary_charts,
                'hscale': args.hscale,
                'degree_of_generated_source': 'at most8, before a fresh quadratic lift',
                'not_claimed': ['accepted equivalence to original source', 'final quartic variable count',
                                'full coefficient bound', 'independent module/circuit audit']}
    (args.out/'PROPOSED_SOURCE.json').write_text(json.dumps(contract, indent=2)+'\n')
    print(json.dumps(contract, indent=2))


if __name__ == '__main__':
    main()
