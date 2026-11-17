#!/usr/bin/env python3
"""Exact general25 family with ten unsquared reciprocal-abscissa tests."""
from pathlib import Path
import argparse, hashlib, importlib.util, inspect, json, sys, textwrap
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def discover_repo():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--repo', type=Path)
    args, _ = parser.parse_known_args()
    candidates = ([args.repo.resolve()] if args.repo else
                  [q for p in (HERE, *HERE.parents) for q in (p, p/'repo')])
    marker = Path('computation/few_variables/full_auxiliary25_v72/build_source.py')
    for candidate in candidates:
        if (candidate/marker).is_file():
            return candidate
    raise FileNotFoundError('Cannot find project checkout; pass --repo PATH')


REPO = discover_repo()


def check_dependencies():
    pins = json.loads((HERE/'dependencies.json').read_text())
    for relative, expected in pins['sha256'].items():
        actual = hashlib.sha256((REPO/relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('Pinned dependency changed: '+relative)
    return pins


check_dependencies()
_path = REPO/'computation/few_variables/full_auxiliary25_v72/build_source.py'
_spec = importlib.util.spec_from_file_location('full_auxiliary25_parent_v75', _path)
_parent = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _parent
_spec.loader.exec_module(_parent)
helper, FULL11 = _parent.helper, _parent.FULL11


def revised_build_method():
    """Apply exactly the two recorded edits to the pinned native constructor."""
    source = textwrap.dedent(inspect.getsource(_parent.General25.build))
    replacements = [
        ('for C,order in zip(tests,comparison_orders):',
         'for test_index,(C,order) in enumerate(zip(tests,comparison_orders)):'),
        ('self.scale(self.square(C),weight)',
         'self.scale(C if test_index<10 else self.square(C),weight)'),
    ]
    for old, new in replacements:
        if source.count(old) != 1:
            raise ValueError('Expected one exact constructor edit: '+old)
        source = source.replace(old, new)
    namespace = dict(_parent.General25.build.__globals__)
    exec(compile(source, __file__+'::revised_native_build', 'exec'), namespace)
    return namespace['build']


_native_build = revised_build_method()


class FullAuxiliary25(_parent.FullAuxiliary25):
    def build(self):
        source = _native_build(self)
        source['format'] = 'point-block-guarded-source/v75'
        source['auxiliary_chart'] = (
            'H,U_A,U_S,U_T,U_Z use x=h,y=j,j^2=h^3-Dh; '
            'four root points retain x=h^2')
        source['proof'] = 'papers/few_variables25/even_valuation25_20261117_v75.tex'
        source['arithmetic_status'] = (
            'Ten reciprocal-abscissa factors use C instead of C^2. '
            'Even valuations preserve extraction, and the original prepared '
            '2E(K) subfamily gives completeness under the retained premises. '
            'No general21 realization is claimed.')
        for event in source['events']:
            if event['operation'] in ('comparison_and_scalar_tests', 'combined_detector'):
                event['comparison_powers'] = [1]*10+[2]*6
        return source


def patch():
    return _parent.patch()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=REPO)
    parser.add_argument('--L', '--parameter', dest='L', type=int, default=3)
    parser.add_argument('--name', choices=['general25'], default='general25')
    parser.add_argument('--output', type=Path, default=HERE/'specification')
    args = parser.parse_args()
    changes = patch()
    source = FullAuxiliary25(args.L).build()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    parent = helper.old._subalgebra.compile_specification(source)
    parent['native_source_generator'] = 'computation/few_variables/even_valuation25_v75/build_source.py'
    parent['parent_pin_base'] = 'containing specification directory'
    parent_path = output/'subalgebra_parent.json'
    parent_path.write_text(json.dumps(parent, indent=2)+'\n')
    helper.old._terminal.ROOT = output
    final = helper.old._terminal.compile_specification(source, parent, parent_path)
    (output/'source.json').write_bytes(helper.old.canonical(source))
    (output/'polynomial.json').write_text(json.dumps(final, indent=2)+'\n')
    report = {
        'status': 'PASS',
        'scope': 'Exact integer circuit construction; independent checks are in check.py',
        'source_sha256': hashlib.sha256(helper.old.canonical(source)).hexdigest(),
        'nodes': len(source['coefficient_dag']),
        'guards': len(source['guard_numerators']),
        'bounds': final['bounds'],
        'compiler_adjustments': changes,
        'native_change': 'First ten comparison factor numerators use C instead of C^2; all remaining operations retained.',
        'family_parameter': source['family_parameter'],
        'coefficient_scope': 'The coefficient bound is for the specified fixed L; no numerical L is certified to exceed the sufficient defining threshold.',
        'general21_realization_claimed': False,
    }
    (output/'construction.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
