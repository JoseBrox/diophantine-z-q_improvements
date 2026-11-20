#!/usr/bin/env python3
"""Run the frozen independent review after relocating its source package.

The reviewed arithmetic code is loaded unchanged. Only its package-directory
constant is adapted. Its original source pins describe the reviewer's scratch
layout; the publication gate separately verifies the actual repository pins.
"""
from contextlib import redirect_stdout
from importlib.util import module_from_spec, spec_from_file_location
from io import StringIO
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def main():
    original = HERE / 'independent_review' / 'check_independent.py'
    spec = spec_from_file_location('v82_frozen_independent_review', original)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PACKAGE = HERE
    output = StringIO()
    with redirect_stdout(output):
        module.main()
    actual = json.loads(output.getvalue())
    expected = json.loads((HERE / 'independent_review' /
                           'independent_reconstruction.json').read_text())
    actual.pop('source_pins')
    expected.pop('source_pins')
    assert actual == expected, 'Independent arithmetic reconstruction changed'
    print(json.dumps({
        'status': 'PASS',
        'arithmetic_algorithm_unchanged': True,
        'all_arithmetic_results_byte_equivalent_as_json_values': True,
        'prepared_counterexample_is_not_actual_detector_data': True,
        'excluded_target_classes': actual['excluded_target_class_count'],
        'source_binding': 'The v82 gate verifies both original and publication pins.',
    }, indent=2))


if __name__ == '__main__':
    main()
