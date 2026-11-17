# Full elliptic-curve auxiliary points

This package specifies an eleven-variable integer polynomial family for the derivative detector, under ordinary rational abc and the arithmetic premises retained by its source. Counts include the input variable. The root point remains in `2E(K)`. The two auxiliary points range over the guarded affine points of `E(K)` through cubic point radicands.

The degree bound is **232,094,337**, the encoder degree is at most 128, the support bound is strictly below `2^264`, and integer content is one. The native circuit contains 1,990 integer arithmetic nodes, 32 recorded guards, and 38 retained subalgebra norm factors. No expanded production polynomial is stored.

The same auxiliary enlargement preserves soundness of the nine-variable actual-trace source. Global rational realization for that source remains unproved. This package does not claim nine- or twenty-one-variable completeness.

## Family parameter and coefficient bounds

`B` is a fixed odd integer at least three. The accompanying theorem proves that every sufficiently large fixed `B` defines the integers. The sufficient threshold is not numerically specified. In particular, the stored **B = 3 member is an algebraic fixture**, with no assertion that it is a defining member.

The degree and support bounds are uniform in `B`. The coefficient bound is reconstructed for each supplied `B`: the parameter node uses `ceil(log2(B))`, and the exact integer circuit propagates coefficient norm bounds through every arithmetic operation and norm determinant. The bound concerns the coefficient L1 norm, so also bounds every coefficient in absolute value.

| Fixed parameter | Coefficient L1 norm bound | Degree bound |
| --- | --- | --- |
| B = 3 | `2^487256960` | 232,094,337 |
| B = 5 | `2^599950720` | 232,094,337 |

## Reconstruct and verify

Run from the repository root:

```sh
python computation/few_variables/full_auxiliary11_v71/build_source.py --B 3
python computation/few_variables/full_auxiliary11_v71/check.py
```

The scripts discover the repository from their location. A separate output directory and an explicit repository path are supported:

```sh
python computation/few_variables/full_auxiliary11_v71/build_source.py --repo . --B 5 --output verification_full_auxiliary_B5
python computation/few_variables/full_auxiliary11_v71/check.py --repo . --specification verification_full_auxiliary_B5
```

The dependency manifest pins the reused source compilers, independent checkers and exact elliptic arithmetic by SHA-256. Every dependency is read without modification. The finite list of in-memory changes to the inherited degree and coefficient majorants is included in `construction.json`. Parent-specification pins are relative to the directory containing the specification files.

## Independent verification

`check.py` verifies the universal rank-four multiplication table, all three generator commutators, the primitive characteristic quartic, its factored discriminant, and the cubic coordinate identity by exact polynomial arithmetic. It checks the new weighted basis and coefficient norm estimates directly.

A separate iterative traversal checks all guard factors, subalgebra supports, quadratic-stage bounds, root envelopes and denominator retention. It rejects deliberate mutations of a degree bound and a guard factor. The final quadratic root is allowed to vanish; every preceding radicand remains a unit.

Native circuit evaluation is compared with ordinary chord-and-tangent calculations for all 64 point characters at each of three actual point tuples and two split primes. The auxiliary indices `1/2`, `3/2` and `5/2` include points outside `2E(K)`. The certificate records 384 character evaluations. These finite checks verify the circuit and its bounds. They do not prove the retained external arithmetic inputs or certify a sufficient numerical value of `B`.

## Files

| File | Purpose |
| --- | --- |
| `build_source.py` | Family builder with `--B`, `--repo` and `--output` |
| `check.py` | Independent exact algebra, circuit, guard and degree verification |
| `dependencies.json` | SHA-256 pins for reused project code |
| `specification/source.json` | Complete native integer arithmetic circuit for B = 3 |
| `specification/subalgebra_parent.json` | Parent norm and separator specification |
| `specification/polynomial.json` | Final terminal-root polynomial specification |
| `specification/construction.json` | Construction bounds and compiler adjustments |
| `specification/independent_certificate.json` | Exact verification certificate |

The proof is in `papers/conditional_few_variables/full_auxiliary11_20261117_v71.tex`.
