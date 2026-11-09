#!/usr/bin/env python3
"""Reproduce all distributed polynomial data and exact certificates offline."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from restore_data import restore

ROOT=Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(label, script, *args):
    start=time.monotonic()
    result=subprocess.run([sys.executable,str(script),*map(str,args)],
        cwd=script.parent,capture_output=True,text=True)
    if result.returncode:
        sys.stderr.write((result.stdout+'\n'+result.stderr)[-12000:])
        raise SystemExit(label+' failed')
    print(label+': PASS',flush=True)
    return {'stage':label,'status':'PASS','seconds':round(time.monotonic()-start,3)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true',help='run all supplied checks (also the default)')
    parser.add_argument('--receipt',type=Path)
    parser.add_argument('--with-pari',action='store_true',help='also reproduce the unconditional elliptic rank certificate; requires cypari2')
    args=parser.parse_args()
    assert sys.version_info>=(3,10)
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for entry in manifest['files']:
        path=ROOT/entry['path']
        assert path.is_file() and path.stat().st_size==entry['bytes'],entry['path']
        assert digest(path)==entry['sha256'],entry['path']
    print('Publication manifest: PASS ('+str(len(manifest['files']))+' files)',flush=True)
    quartic_root=ROOT/'computation/quartic'
    provenance=json.loads((quartic_root/'PROVENANCE.json').read_text())
    for name, entry in provenance['files'].items():
        path=quartic_root/name
        assert path.stat().st_size==entry['bytes'] and digest(path)==entry['sha256'],name
    for proof in provenance['proofs'].values():
        for extension in ('tex','pdf'):
            assert digest(quartic_root/proof[extension])==proof[extension+'_sha256'],proof[extension]
    documentation=provenance['documentation']
    assert digest(quartic_root/documentation['dataFormat'])==documentation['dataFormatSHA256']
    print('Quartic source and proof provenance: PASS',flush=True)
    stages=[]
    with tempfile.TemporaryDirectory(prefix='diophantine-verification-') as directory:
        work=Path(directory)
        shutil.copytree(ROOT/'computation',work/'computation',
            ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copytree(ROOT/'data',work/'data')
        restored=restore(work)
        quartic=work/'computation/quartic'
        originals={name:(quartic/'final392'/name).read_bytes() for name in
            ('quadratic-system392.json','polynomial392.json','construction-report392.json')}
        stages.append(run('392-variable quartic reconstruction',quartic/'build_quartic392.py'))
        for name,raw in originals.items():
            assert (quartic/'final392'/name).read_bytes()==raw,name
        stages.append(run('Independent full 394/392 coefficient and source checks',quartic/'verify_quartic392.py'))
        stages.append(run('Quadratic-extension specialization, two exact evaluations',quartic/'check_field_specialization392.py'))
        for count, folder, prefix in [(389,'final389',''),(370,'family370','family'),(329,'family329','family'),(317,'family317','family')]:
            names = ([f'quadratic-system{count}.json',f'polynomial{count}.json',f'construction-report{count}.json']
                     if not prefix else
                     [f'quadratic-family{count}.json',f'polynomial-family{count}.json',f'construction-report{count}.json'])
            fixed_tables = {name:(quartic/folder/name).read_bytes() for name in names}
            stages.append(run(f'{count}-coordinate exact quadratic construction',quartic/f'build_quartic{count}.py'))
            for name, raw in fixed_tables.items():
                assert (quartic/folder/name).read_bytes()==raw,name
            stages.append(run(f'{count}-coordinate independent full coefficient checks',quartic/f'check_quartic{count}.py'))
            if count==389:
                stages.append(run('All three detector affine normalizations',quartic/'verify_detector_normalizations.py'))
        packed_originals = {}
        for count in (301,351):
            for name in (f'quadratic-family{count}.json',f'polynomial-family{count}.json',f'construction-report{count}.json'):
                p=quartic/f'family{count}'/name
                packed_originals[p]=p.read_bytes()
        stages.append(run('301/351-variable exact quadratic constructions',quartic/'build_quartic_mixed.py'))
        for p,raw in packed_originals.items():
            assert p.read_bytes()==raw,str(p)
        stages.append(run('301/351-variable independent complete coefficient and valuation checks',quartic/'check_quartic_mixed.py'))
        shared_weight_originals = {}
        shared_weight_checks = {}
        for count in (297,342):
            for name in (f'quadratic-family{count}.json',f'polynomial-family{count}.json',f'construction-report{count}.json'):
                p=quartic/f'family{count}'/name
                shared_weight_originals[p]=p.read_bytes()
            p=quartic/f'family{count}'/f'independent-verification{count}.json'
            shared_weight_checks[p]=p.read_bytes()
        stages.append(run('297/342-variable exact shared-weight constructions and affine normalization',
            quartic/'build_quartic_shared_weights.py'))
        for p,raw in shared_weight_originals.items():
            assert p.read_bytes()==raw,str(p)
        stages.append(run('297/342-variable independent complete coefficient and exact-height checks',
            quartic/'check_quartic_shared_weights.py'))
        for p,raw in shared_weight_checks.items():
            assert p.read_bytes()==raw,str(p)
        even_originals = {}
        even_checks = {}
        for count in (322,):
            for name in (f'quadratic-family{count}.json',f'polynomial-family{count}.json',f'construction-report{count}.json'):
                p=quartic/f'family{count}'/name
                even_originals[p]=p.read_bytes()
            p=quartic/f'family{count}'/f'independent-verification{count}.json'
            even_checks[p]=p.read_bytes()
        stages.append(run('322-variable exact parity construction',quartic/'build_quartic_even.py'))
        for p,raw in even_originals.items():
            assert p.read_bytes()==raw,str(p)
        stages.append(run('322-variable independent complete coefficients and formal-valuation checks',quartic/'check_quartic_even.py'))
        for p,raw in even_checks.items():
            assert p.read_bytes()==raw,str(p)
        amplified = quartic/'family279'
        amplified_originals = {name:(amplified/name).read_bytes() for name in (
            'quadratic-family279.json','polynomial-family279.json',
            'construction-report279.json','independent-verification279.json')}
        stages.append(run('279-variable exact coefficient source reconstruction',quartic/'build_quartic279.py'))
        stages.append(run('279-variable independent source rows and complete coefficients',
            quartic/'check_quartic279.py'))
        for name,raw in amplified_originals.items():
            assert (amplified/name).read_bytes()==raw,name
        for count in (273,267):
            folder=quartic/f'family{count}'
            fixed_new={name:(folder/name).read_bytes() for name in (
                f'quadratic-family{count}.json',f'polynomial-family{count}.json',
                f'construction-report{count}.json',f'independent-verification{count}.json')}
            stages.append(run(f'{count}-variable exact contact evaluation construction',
                quartic/f'build_quartic{count}.py'))
            stages.append(run(f'{count}-variable independent rows, full coefficients, and height',
                quartic/f'check_quartic{count}.py'))
            for name,raw in fixed_new.items():
                assert (folder/name).read_bytes()==raw,name
        coordinate_budget=(quartic/'coordinate-budget279.json').read_bytes()
        stages.append(run('Disjoint coordinate accounting for the279-variable family',quartic/'check_coordinate_budget.py'))
        assert (quartic/'coordinate-budget279.json').read_bytes()==coordinate_budget
        few=work/'computation/few_variables'
        module=few/'forced_prime29'
        module_manifest=json.loads((module/'manifest.json').read_text())
        for entry in module_manifest['files']:
            assert digest(module/entry['path'])==entry['sha256'],entry['path']
        old_source=(module/'source.json.gz').read_bytes()
        old_spec=(module/'polynomial-specification.json').read_bytes()
        stages.append(run('29-variable source, finite algebra, and weighted coefficient bounds',module/'reproduce.py'))
        assert (module/'source.json.gz').read_bytes()==old_source
        assert (module/'polynomial-specification.json').read_bytes()==old_spec
        stages.append(run('Explicit 29-variable effective-height source and bounds',
            few/'effective29_nontorsion/reproduce.py'))
        stages.append(run('Complete optimal quadratic-field square predicates',
            work/'computation/square_predicates/check_square_predicates.py'))
        stages.append(run('Independent height-seven square-test coefficient certificate',
            work/'computation/square_predicates/check_height7_linear_multiplier.py'))
        stages.append(run('Effective elliptic abscissa-sum identities and constants',
            work/'computation/effective_sums/check_effective_elliptic_sums.py'))
        stages.append(run('27-variable cubic-chart family and uniform degree bound',
            few/'trace27_nontorsion/reproduce.py','--anchor-exponent','137731'))
        weighted=few/'weighted_elimination'
        for count,source in (
                (27,few/'trace27_nontorsion/example_L137731/polynomial-specification.json'),
                (29,few/'effective29_nontorsion/certificate/polynomial-specification.json')):
            destination=weighted/f'weighted{count}'
            fixed_weighted={name:(destination/name).read_bytes() for name in
                ('polynomial-specification.json','construction-certificate.json')}
            stages.append(run(f'{count}-variable weighted finite-algebra specification reconstruction',
                weighted/'build_weighted_specification.py',source,destination))
            for name,raw in fixed_weighted.items():
                assert (destination/name).read_bytes()==raw,str(destination/name)
        weighted_verification=(weighted/'verification.json').read_bytes()
        stages.append(run('Independent weighted degree bounds and guarded finite-algebra examples',
            weighted/'check_weighted_specification.py',weighted/'weighted27',weighted/'weighted29',
            '--output',weighted/'verification.json'))
        assert (weighted/'verification.json').read_bytes()==weighted_verification
        active=few/'active_elimination'
        for count,source in (
                (27,few/'trace27_nontorsion/example_L137731/polynomial-specification.json'),
                (29,few/'effective29_nontorsion/certificate/polynomial-specification.json')):
            destination=active/f'active{count}'
            fixed_active={name:(destination/name).read_bytes() for name in
                ('polynomial-specification.json','construction-certificate.json')}
            stages.append(run(f'{count}-variable exact separation on the nonzero guard locus',
                active/'build_active_specification.py',source,destination))
            for name,raw in fixed_active.items():
                assert (destination/name).read_bytes()==raw,str(destination/name)
        active_check=(active/'independent-verification.json').read_bytes()
        stages.append(run('Independent nonzero-guard separation degree and norm bounds',
            active/'check_active_specification.py',active/'active27',active/'active29',
            '--output',active/'independent-verification.json'))
        assert (active/'independent-verification.json').read_bytes()==active_check
        degenerations=(active/'degeneration-certificate.json').read_bytes()
        stages.append(run('Seven exact finite-algebra degeneration and determinant comparisons',
            active/'check_active_degenerations.py','--output',active/'degeneration-certificate.json'))
        assert (active/'degeneration-certificate.json').read_bytes()==degenerations
        conditional=few/'conditional13'
        conditional_files=[
            conditional/'certificate/source.json.gz',
            conditional/'certificate/source-polynomial-specification.json',
            conditional/'certificate/source-construction-certificate.json',
            conditional/'active13/polynomial-specification.json',
            conditional/'active13/construction-certificate.json',
            conditional/'independent-source-verification.json',
            conditional/'independent-bound-verification.json']
        conditional_originals={p:p.read_bytes() for p in conditional_files}
        stages.append(run('Additional-abc 13-variable exact guarded source construction',
            conditional/'build_conditional_source.py','--shift','3','--output',conditional/'certificate'))
        stages.append(run('Independent 13-variable source conversion, charts, and every guard',
            conditional/'check_conditional_source.py',conditional/'certificate',
            '--output',conditional/'independent-source-verification.json'))
        stages.append(run('13-variable exact finite-algebra specification',
            active/'build_active_specification.py',
            conditional/'certificate/source-polynomial-specification.json',conditional/'active13'))
        stages.append(run('Independent 13-variable uniform degree and fixture coefficient bounds',
            active/'check_active_specification.py',conditional/'active13',
            '--output',conditional/'independent-bound-verification.json'))
        for p,raw in conditional_originals.items():
            assert p.read_bytes()==raw,str(p)
        stages.append(run('Quadratic extension square chart: exact cubic identities',
            work/'computation/quadratic_squares/check_quadratic_square_chart.py'))
        stages.append(run('Scalar normalization: Bezout certificate and exhaustive residue check',
            work/'computation/scalar_normalization/check_scalar_normalization.py'))
        input_normalization=work/'computation/input_normalization'
        input_certificate=(input_normalization/'quadratic-input-obstruction-certificate.json').read_bytes()
        stages.append(run('Restricted quadratic input-map obstruction',
            input_normalization/'check_quadratic_input_obstruction.py','--output',
            input_normalization/'quadratic-input-obstruction-certificate.json'))
        assert (input_normalization/'quadratic-input-obstruction-certificate.json').read_bytes()==input_certificate
        stages.append(run('Independent fixed-prime numerical certificates',
            work/'computation/arithmetic/check_forced_prime_20261108_v8.py'))
        stages.append(run('Elliptic chart arithmetic',few/'verify_elliptic_chart.py'))
        stages.append(run('Quadratic elliptic-height identities and constants',few/'verify_quadratic_height.py'))
        constants=work/'computation/constants'
        fixed={name:(constants/'data'/name).read_bytes() for name in ('height19.bin','height19-primes.json')}
        stages.append(run('Two independent prime enumerations and exact height constant',constants/'check_height_constant.py'))
        for name,raw in fixed.items():
            assert (constants/'data'/name).read_bytes()==raw
        stages.append(run('Anisotropic forms and residue fields',
            work/'computation/field_extensions/verify_anisotropic_examples.py'))
        number_fields=work/'computation/number_fields'
        norm_verification=(number_fields/'norm-image-reduction-verification.json').read_bytes()
        stages.append(run('Number-field norm-image reduction and elliptic valuation obstruction',
            number_fields/'check_norm_image_reduction.py'))
        assert (number_fields/'norm-image-reduction-verification.json').read_bytes()==norm_verification
        exceptional=(number_fields/'exceptional-correspondence-certificate.json').read_bytes()
        stages.append(run('Exact exceptional surface, inverse maps, and four output lines',
            number_fields/'check_exceptional_correspondence.py'))
        assert (number_fields/'exceptional-correspondence-certificate.json').read_bytes()==exceptional
        rationality_filter=(number_fields/'rationality-filter-certificate.json').read_bytes()
        stages.append(run('Exact slope and ordinate polynomials and labelled bounded searches',
            number_fields/'check_rationality_filters.py'))
        assert (number_fields/'rationality-filter-certificate.json').read_bytes()==rationality_filter
        contacts=work/'computation/contact_heights'
        contact_certificate=(contacts/'contact-height-certificate.json').read_bytes()
        stages.append(run('Disjoint contact sets, exceptional primes, and exact exponent inequalities',
            contacts/'check_contact_height_amplification.py','--output',contacts/'contact-height-certificate.json'))
        assert (contacts/'contact-height-certificate.json').read_bytes()==contact_certificate
        scalar=work/'computation/scalar_normalization'
        scalar_certificate=(scalar/'uniform-scalar-normalization-certificate.json').read_bytes()
        stages.append(run('Uniform scalar normalization, two exact resultants, and exhaustive local residues',
            scalar/'check_uniform_scalar_normalization.py'))
        assert (scalar/'uniform-scalar-normalization-certificate.json').read_bytes()==scalar_certificate
        constraints=work/'computation/elliptic_constraints'
        parity_certificate=(constraints/'reduction-parity-certificate.json').read_bytes()
        stages.append(run('Exact conjugate reduction orders and parity counterexamples',
            constraints/'search_reduction_parities.py'))
        assert (constraints/'reduction-parity-certificate.json').read_bytes()==parity_certificate
        large_parity=(constraints/'large-split-order-certificate.json').read_bytes()
        stages.append(run('Independent large-prime point orders above the exceptional cutoff',
            constraints/'check_large_split_orders.py'))
        assert (constraints/'large-split-order-certificate.json').read_bytes()==large_parity
        if args.with_pari:
            original=json.loads((number_fields/'elliptic-ratio-certificate.json').read_text())
            stages.append(run('Unconditional elliptic ranks, exact quadratic-field stability, and local-global obstruction',
                number_fields/'check_elliptic_ratio_obstruction.py','--output',number_fields/'elliptic-ratio-recomputed.json'))
            recomputed=json.loads((number_fields/'elliptic-ratio-recomputed.json').read_text())
            # Rank bounds, torsion, and polynomial terms are canonical;
            # a PARI release may choose different point generators.
            for key in ('four_coordinate_polynomial','additional_quadratic_fields','positive_rank_witness','local_witness_checks'):
                assert original[key]==recomputed[key],key
            for a,b in zip(original['curves'],recomputed['curves']):
                for key in ('B','rank_lower','rank_upper','torsion_order','independent_finite_field_orders'):
                    assert a[key]==b[key],(a['B'],key)
            poles=work/'computation/pole_parameters'
            original_poles=json.loads((poles/'fixed-e-obstruction-certificate.json').read_text())
            stages.append(run('Prepared fixed-pole counterexamples, exact ranks, and squareclass descent',
                poles/'check_fixed_e_obstruction.py'))
            recomputed_poles=json.loads((poles/'fixed-e-obstruction-certificate.json').read_text())
            for key in ('prepared_inputs','maps','known_infinite_order_point_on_E9809',
                        'complete_x_squareclass_image_on_E9809','required_squareclass_absent',
                        'everywhere_local_witnesses','good_reduction_outside'):
                assert original_poles[key]==recomputed_poles[key],key
            for a,b in zip(original_poles['elliptic_curves'],recomputed_poles['elliptic_curves']):
                for key in ('parameter','coefficients','rank_lower','rank_upper',
                            'good_prime_counts','torsion_order_upper_bound',
                            'nonidentity_two_torsion','two_selmer_rank',
                            'pairing_rank_independently_checked_over_F2'):
                    assert a[key]==b[key],(a['parameter'],key)
    report={'status':'PASS','manifest_files_checked':len(manifest['files']),
        'compressed_tables_restored':restored,'pari_rank_checks_run':args.with_pari,'stages':stages,
        'scope':'Exact source identities, full quartic coefficients, finite-algebra specification, local constants and quantitative bounds. The global arithmetic projection premises are stated separately in the papers.'}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(report,indent=2)+'\n')
    print('All requested checks passed; published inputs were unchanged.')


if __name__=='__main__':
    main()
