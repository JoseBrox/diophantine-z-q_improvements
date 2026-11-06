#!/usr/bin/env python3
"""Fresh degree-72 norm specifications for the final quartic transforms.

The previous four specifications and receipts are never overwritten.
The source arguments are pinned by their uncompressed hashes in each
new output.  The determinant convention is the verified v1 convention.
"""
from pathlib import Path
from hashlib import sha256
from math import factorial
import argparse
import gzip
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
_module_spec = importlib.util.spec_from_file_location(
    'previous_norm_constructor', HERE/'build_division_norm_specs_20261106_v1.py')
previous = importlib.util.module_from_spec(_module_spec)
_module_spec.loader.exec_module(previous)


def compile_one(path, translated):
    raw = gzip.decompress(path.read_bytes())
    source = json.loads(raw)
    rows = source['residuals']
    if translated:
        expected_n, expected_r = 1315,1272
    else:
        expected_n=len(source['variables'])
        assert expected_n in (1338,1335)
        expected_r={1338:1295,1335:1292}[expected_n]
    assert len(source['variables']) == expected_n and len(rows) == expected_r
    assert all(len(m) <= 2 for row in rows for m,k,c in row['terms'])
    assert [(i,m,k,c) for i,row in enumerate(rows) for m,k,c in row['terms'] if 0 in m] == [(0,[0,0],0,1)]
    norm = previous.norm_data(36,37,2)
    nbound = factorial(36)*72**36
    assert nbound == norm['norm_coefficient_l1_bound'] and nbound < 2**361
    if translated:
        assert source['fixed_constants'] == {'S':'3^(2^27)'}, source['fixed_constants']
        symbolic = [(i,m,k,c) for i,row in enumerate(rows) for m,k,c in row['terms'] if k]
        assert symbolic == [(46,[55],1,8)], symbolic
        m0 = max(sum(abs(c) for m,k,c in row['terms'] if k == 0) for row in rows)
        assert m0 < 2**511
        # S>2^511, so every residual has coefficient norm <9S.
        # 9S=3^(2^27+2), and 3^5<2^8.
        assert 3**5 < 2**8 and 2**27 > 511
        numerator = 8*(2**27+2)
        assert numerator % 5 == 0
        residual_log_bound = numerator//5
        height_bits = 361+36*residual_log_bound
        coefficient_certificate = {
            'constant_part_maximum_l1_norm':m0,
            'symbolic_terms':symbolic,
            'residual_coefficient_l1_bound':'strictly less than 9*S = 3^(2^27+2)',
            'residual_coefficient_log2_bound':residual_log_bound,
            'full_coefficient_norm_bound':{'integer_factor':nbound,
                                           'power_base':3,
                                           'power_exponent':36*(2**27+2)},
            'derivation':'The only symbolic coefficient is 8*S. Every constant part has l1 norm <2^511<S. Thus all residual norms are <9*S. Use 3^5<2^8 and the exact determinant coefficient norm bound.'}
        filename='norm_repair_1315_translated_degree72_20261106_v2.json.gz'
    else:
        assert source['fixed_constants'] == {}
        assert all(k == 0 for row in rows for m,k,c in row['terms'])
        m0=max(sum(abs(c) for m,k,c in row['terms']) for row in rows)
        height_bits=previous.clog(nbound)+36*previous.clog(m0)
        coefficient_certificate={'residual_coefficient_l1_bound':m0,
                                 'residual_coefficient_log2_bound':previous.clog(m0),
                                 'determinant_coefficient_l1_bound':nbound}
        filename=f'norm_repair_{expected_n}_degree72_20261106_v2.json.gz'
    spec={
        'format':'integer-polynomial-cyclic-norm/v2',
        'source_json_sha256':sha256(raw).hexdigest(),
        'source_file':str(path.relative_to(ROOT)),
        'variables':source['variables'],
        'fixed_constants':source['fixed_constants'],
        'quadratic_residuals':rows,
        'norm_construction':norm,
        'total_variables':expected_n,'existential_witnesses':expected_n-1,
        'exact_degree':72,'leading_input_coefficient':1,
        'coefficient_height_bound_power_of_two_exponent':height_bits,
        'coefficient_certificate':coefficient_certificate,
        'equivalence':'Over fields where the specified cyclic algebra remains division, the polynomial vanishes exactly when every recorded quadratic residual vanishes.',
        'arithmetic_scope':'No assertion that the base-changed quadratic system defines the ring of integers of K is made.',
        'representation':'Complete 36 by 36 indexed determinant with cyclotomic coefficient extraction and the complete quadratic residual tables. The degree-72 coefficient table is not expanded. No cyclotomic symbol is quantified.',
        'transformation_scope':('Invertible rational affine witness-coordinate change preserves the literal polynomial projection over every characteristic-zero field.' if translated else ('Eliminating the private squaring coordinate preserves the conjunction over every field. This alone does not preserve every sum-of-squares cancellation over a nonreal field.' if expected_n==1338 else 'Eliminating the private squaring coordinate and three fixed constant graph coordinates preserves the conjunction over every field. This alone does not preserve every sum-of-squares cancellation over a nonreal field.'))}
    encoded=(json.dumps(spec,separators=(',',':'))+'\n').encode()
    output=HERE/filename
    if output.exists():
        assert gzip.decompress(output.read_bytes())==encoded, 'A frozen specification would change'
    else:
        output.write_bytes(gzip.compress(encoded,mtime=0))
    return {'file':filename,'source_file':spec['source_file'],
            'uncompressed_sha256':sha256(encoded).hexdigest(),
            'source_json_sha256':spec['source_json_sha256'],
            'total_variables':expected_n,'residual_count':expected_r,
            'exact_degree':72,'leading_input_coefficient':1,
            'coefficient_height_bound_power_of_two_exponent':height_bits}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--translated',type=Path,required=True)
    parser.add_argument('--eliminated',type=Path,required=True)
    parser.add_argument('--folded',type=Path)
    args=parser.parse_args()
    rows=[compile_one(args.translated.resolve(),True),compile_one(args.eliminated.resolve(),False)]
    if args.folded:rows.append(compile_one(args.folded.resolve(),False))
    receipt={'status':'PASS','producer_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
             'reused_norm_constructor_sha256':sha256((HERE/'build_division_norm_specs_20261106_v1.py').read_bytes()).hexdigest(),
             'repairs':rows,'prior_artifacts':'The four v1 specifications and their certificates are unchanged.'}
    (HERE/'division-norm-construction_20261106_v2.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
