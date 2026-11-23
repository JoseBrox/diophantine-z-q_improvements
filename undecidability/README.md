# Variable bounds for undecidability over the rationals

Here `N` counts existential rational unknowns in a decision problem. The
integer input specifying an instance occurs in its coefficients and is not
counted. This is a separate objective from minimizing the total coordinates
of a polynomial defining the integers. All recorded numbers are upper bounds;
no global least value is claimed.

## Current unrestricted-degree results

The [common-numerator proof](papers/common_numerator_transfers.tex) and
[finite-wrapper proof](papers/finite_wrapper_transfer.tex)
([PDF](papers/finite_wrapper_transfer.pdf)) give:

| Source route | Additional height hypothesis | Rational unknowns | Degree strictly below |
|:--|:--|--:|--:|
| General two-detector source | No additional abc hypothesis | **82** | `2^650` |
| Specified three-detector source, `L=143` | No additional abc hypothesis | **100** | `2^714` |
| Ordinary-abc source | Ordinary rational abc | **52** | `2^500` |

These are proved transfer theorems **under the source's retained arithmetic
premises**. Those premises have not all been independently proved here.
The current v88 Bhargava–Burungale product poles are used; the former native
pole converse premise is not reintroduced. The general and abc sufficient
fixed parameters remain ineffective. The stored general `L=143` and abc
`B=3` sources are algebraic fixtures, not certified defining members.
The 100-variable source uses its specified sufficient parameter.

### Method and intermediate improvements

Sun's mixed-domain representation uses eight arbitrary integer unknowns
and one nonnegative integer unknown. The substitution

```math
L(s,t,u)=s^2+t^2+u^2+u
```

represents every nonnegative integer and is at least `-1/4` over the
rationals. Requiring its value to be an integer therefore forces it to be
nonnegative. It replaces one input with three coordinates, a net cost of two.

The initial [independent-block theorem](papers/transfer_general_degree.tex)
([PDF](papers/transfer_general_degree.pdf)) gives `9m+2`, hence
**227 / 245 / 101**. Its common degree bound `2*eta(58,4)` is much smaller
than the new joint bounds, so it remains a useful tradeoff.

The [guarded finite-algebra encoder](papers/joint_finite_algebra_encoder.tex)
([PDF](papers/joint_finite_algebra_encoder.pdf)) combines any finite set of
root-existence conditions with one rational encoding coordinate. Its proof
allows nilpotents, repeated roots and denominators vanishing on excluded
characters. Merging only the nine encoders gives `9m-6`, hence
**219 / 237 / 93**, without sharing any ordinary witnesses.

The further reduction proves simultaneous witness construction. Seven
point roles and one translated contact parameter can be common in the
general sources. This gives joint certificates for `Z^k` in **`9k+16`**
or **`11k+16`** total coordinates. The ordinary-abc variant shares its
reference point and a scaled contact parameter, first lifting each input
to `X_i^2+1`; its count is **`7k+4`**. Set `k=9` and add the wrapper's two
coordinates to obtain the earlier 99/117/69 bounds.

The [complete compressed source circuits](joint_sources) specify every
coefficient node, finite block, coordinate map and guard. The final
polynomials are given by finite determinant formulas and have not been
fully expanded. The [exact certificate](certificates/shared_integer_transfers.json)
records all counts, hashes and matrix-entry degree bounds.

The [common-numerator theorem](papers/common_numerator_transfers.tex)
([PDF](papers/common_numerator_transfers.pdf)) replaces every private
numerator point by one common point. Its index is chosen independently of
the reference index. The all-sign coprimality clause of the retained prime
supplier allows different target residues at the disjoint input contact
families. Prime-power refinements preserve the formal depths, and the
existing contact weights suppress bounded comparisons at fixed places.
The new tuple counts are **`7k+18` / `9k+18` / `5k+6`**, giving
**83 / 101 / 53**, with degree ceilings `2^413 / 2^477 / 2^263`.
The [new complete circuits](common_numerator_sources) and
[exact certificate](certificates/common_numerator_transfers.json) are supplied.

The [finite-wrapper theorem](papers/finite_wrapper_transfer.tex) then
absorbs the mixed universal equation and one positivity witness into a
rank-sixteen finite algebra. Its generators recover the ninth input and
the omitted witness; all **nine integer predicates remain**. Two monic
relations and a single additional guard suffice. The old encoder handles
the new finite generators, so no new ordinary variable is introduced.
This gives the headline **82 / 100 / 52** bounds, at a higher degree.
The manuscript gives the full source coefficient recipe, both directions,
denominator rescalings, a general equation-absorption principle and the
[certified degree ledger](certificates/finite_wrapper_transfer.json).
The [executable compiler and format guide](finite_wrapper_sources/README.md)
turn any supplied sparse source polynomial into the whole coefficient DAG;
the stored demonstration is explicitly nonuniversal.

## Quartic checkpoints: source universality remains unresolved

The [direct quadratic compilation](papers/jones1980_quartic_transfer.tex)
([PDF](papers/jones1980_quartic_transfer.pdf)) proves an exact equivalence
with a precisely displayed emended 28-variable positive-integer system.
It uses twelve integrality inputs, a 169-step signed power chain,
geometric-quotient integrality, automatic positivity on a cofinite instance
tail and Pell powers restoring positive witnesses.

The source audit found that Jones's 1980 announcement prints **Greek alpha**
in a coefficient where the builder uses **Latin a**. Matiyasevich's
1999 author-written chapter supports Latin a, but has a separate impossible
Pell row. The full universality proof for this precise emended system has
not been verified. We state that missing assertion explicitly as **`U_em`**.
It is separate from abc and from the integer predicate's arithmetic premises.

The [shared-reference construction](papers/shared_quartic_checkpoint.tex)
first gave 2086/2278/846. A [reciprocal-input rechart](papers/reciprocal_reference_checkpoint.tex)
then removes one coordinate and one row in each general system.
The [common-point theorem](papers/common_points_quartic_checkpoint.tex)
([PDF](papers/common_points_quartic_checkpoint.pdf)) identifies 54/50
actual common physical coordinates, including the newly shared input
numerator point:

| Integer interface | Independent combined system | Current checkpoint | Quadratic residuals | Additional height hypothesis |
|:--|--:|--:|--:|:--|
| General, 163 coordinates | 2,195 | **1,601** | 1,599 | No additional abc |
| Specified, 179 coordinates | 2,387 | **1,837** | 1,811 | No additional abc |
| Ordinary-abc, 56 coordinates | 911 | **846** | 728 | Ordinary rational abc |

The physical function dictionary, all normalization weights, and the
stronger common-index precision are proved before the registers are
identified. The private contact gauges remain separate. Every residual is
supplied in the [independent tables](coefficients/jones1980),
[shared-reference tables](coefficients/jones1980_shared),
[reciprocal tables](coefficients/jones1980_shared_reciprocal) and
[current common-point tables](coefficients/jones1980_common_points).
Their sums of squares have degree exactly four. The complete tables are
reconstructed row by row, including every removed duplicate.
**Their undecidability interpretation remains conditional on `U_em`** and
all selected interface premises. A quartic bound near 263 has not been
established.

The [literal Mishchenko–Treier audit](papers/mt_source_audit.tex)
([PDF](papers/mt_source_audit.pdf)) proves a reversible **62/50 to 57/45**
reduction. Its universality is unresolved because of discrepancies in its
Pell and product equations. This does not independently reprove the alleged
universal **57-positive-integer-variable / 47-quadratic** theorem.

The earlier **2,539 / 2,779 / 934** candidates were registered first in the
[baseline checkpoint](checkpoints/baseline_20261123.md). Their historical
status is preserved in the registry.

## Limitations and further work

The [polynomial integrality obstruction](papers/polynomial_integrality_obstruction.tex)
([PDF](papers/polynomial_integrality_obstruction.pdf)) proves that fewer than
`r` rational-coefficient polynomial integer-value tests cannot recognize all
of `Z^r` inside `Q^r`. Counterexamples exist at infinitely many denominator
primes, with unbounded denominator exponents. The theorem does not exclude
shared existential witnesses or extra equations of a particular source.

The [further-reduction checkpoint](checkpoints/further_reductions_20261123.md)
records the obstruction to applying common-squareclass pole sharing in the
current fresh-prime construction. Next steps are to audit the complete
Jones 1982 proof, seek a new simultaneous point/pole realization theorem,
remove private translated-point registers while preserving degree two,
and compile any resulting improvement with exact source maps.

## Reproduction and recordkeeping

```sh
python -B undecidability/verify_transfer_general_degree.py
python -B undecidability/verify_joint_sources.py
python -B undecidability/verify_jones1980.py
python -B undecidability/verify_shared_reference.py
python -B undecidability/verify_common_numerator.py
python -B undecidability/verify_finite_wrapper.py
python -B undecidability/verify_finite_wrapper_compiler.py
python -B undecidability/verify_reciprocal_reference.py
python -B undecidability/verify_common_points.py
python -B scripts/verify_v90.py
python -B scripts/verify_v89.py
```

The gate rebuilds the complete specifications and checks the recorded source
qualifications. A `PASS` verifies the stated finite identities and counts;
it does not discharge arithmetic foundations or `U_em`. Proofs, source
citations and the verification scope are in the manuscripts. The
[machine-readable registry](results.json) separates proved transfers from
source-audit checkpoints; the [project report](../docs/results_20261123_v90.md)
summarizes the mathematical changes and their limits.
