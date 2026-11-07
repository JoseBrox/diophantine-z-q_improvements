# Exact baseline certificates for the quartic construction

This directory supplies the arithmetic source expressions and the complete finite verification chain leading to the 474-coordinate baseline used by the 456-variable construction. These are verified dependencies of the final construction. The accompanying quartic paper proves the required rational nonzero domains, parity restriction, and completeness statements, and states the remaining arithmetic inputs explicitly.

## Verification

Requirements: Python 3.10 or later and Node.js 18 or later. No third-party packages, network access, or source manuscripts are needed.

```sh
python3 verify.py
```

The entrypoint first checks every supplied file against `MANIFEST.json`. It then performs the following checks in an isolated temporary copy:

1. Reconstruct the raw arithmetic system from the explicit source builder. Compare its complete output with the supplied raw system. Independently check every recognized arithmetic gate and replay every compiler elimination.
2. Verify the blocked product identities and reused fourth powers; replay the constant-pivot substitutions, merged anchor, and direct point-ratio equations; compare every coefficient of the 485-coordinate system.
3. Verify the primary parity restriction, all ten omitted inverse equations and their occurrence conditions, the exact coordinate rescalings, and every row and coefficient of the 475-coordinate system.
4. Verify the seven local-squareclass choices, the input substitution, and every row and coefficient of the 474-coordinate baseline.

The final baseline residual file is byte-identical to `../source/parent474-residuals.json`. Its SHA-256 is:

```text
9bd49b7542507f32e06cbc424cf223ec2b5226826b980876c7f0750edfa0e09c
```

The final 456-variable producer and checker are separate files in the parent directory. Together the two checks give a continuous finite audit from the explicit source arithmetic to the final coefficient table.

## Contents

- `source/builders/`: explicit arithmetic source program.
- `source/blocked/`: the blocked arithmetic program, raw equations, compiled equations, semantic values, and compiler certificates.
- `source/tools/checker.cjs`: an independent implementation of gate identities, coefficient arithmetic, and elimination checks.
- `data/system485/`, `data/system475/`, `data/system474/`: exact dependency systems, transformations, and coefficient tables.
- `check_source_system.py`, `check_primary_domain.py`, `check_local_correction.py`: independent exact certificate checks.
- `PROVENANCE.json`: pinned source references, original hashes, and the precise metadata-only curation.
- `verification.json`: the result of the most recent complete verification.

## Scope and provenance

The checks establish polynomial identities, coordinate correspondences on the stated domains, and exact coefficient data. They do not prove the elliptic-group, contact-height, prepared-pole, or prime-selection inputs. Those arithmetic premises and the local domain arguments belong to the accompanying mathematical proof.

The displayed source reference is recorded by a fixed commit and SHA-256. Its manuscript contents are not computational inputs: the source program previously read that file only to calculate its provenance hash. This read is replaced by the same pinned digest. An unused editorial `variant` object is removed from the raw and compiled data, and the corresponding compiler input hash is updated. No mathematical coefficient, coordinate, gate, semantic value, guard, or elimination operation is changed. The final three dependency systems remain byte-identical to their checked source files.

The arithmetic is carried out formally over the rational polynomial ring in the coefficient parameter `S`. Source declarations and baseline coefficient specializations are recorded separately. The final 456-variable construction uses the independently proved specialization `S = 3^52832906`.
