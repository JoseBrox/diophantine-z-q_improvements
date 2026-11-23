# Bhargava–Burungale v2: exact source package

The five complete coefficient DAGs, finite algebras and final determinant
certificates implement the transfers proved in
[the v88 manuscript](../../papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex).
Every variable count includes the input.

| Route | Directory | Final certificate | Variables | Degree upper bound |
|:--|:--|:--|--:|--:|
| General | bb_general/general25 | projective.json | 25 | 48,318,382,080 |
| Explicit general | bb_general/explicit27 | reduced.json | 27 | 183,368,679,424 |
| Ordinary abc | bb_twelve/abc11 | strengthened.json | 11 | 3,261,569 |
| Weak abc, 121/100 | bb_weak/weak_flip_first | strengthened.json | 11 | 16,460,929 |
| Weak abc, 16/15 | bb_weak/strong_flip_first | strengthened.json | 11 | 9,808,001 |

Each native.json contains the complete ordered coefficient DAG, free/finite
variables, point relations, terminal pole, denominator occurrences, guards,
events and parameter data. Its parent.json (polynomial.json in the weak
routes) records the finite multiplication algebra and subalgebra norm bounds.
The final certificate selects the proved positive/projective encoder and
ordered guard removals. The source-level terminal ordinate guards are removed
by this final encoder: terminal zero roots are permitted. Using only the
legacy guarded-source interpretation would describe a different predicate.

The explicit general member has L=143 and coefficient height below
2^(2^45). General L=143 and conditional B=3 are algebraic fixtures only.
The family degrees are uniform; their sufficient defining parameters remain
ineffective except in the explicit route. All non-pole arithmetic premises
listed in the proofs are retained.

## Reproduction

From the repository root, with Python and SymPy 1.14.0:

~~~sh
python -B scripts/verify_v88.py --report /tmp/v88-verification.json
~~~

To obtain the original pinned source interfaces and a directly runnable
complete new working tree:

~~~sh
python -B scripts/verify_v88.py --materialize /tmp/zq-v88-offline
~~~

The destination must not already contain a materialized archive.
No network access is needed. The gate copies 590 distinct pinned historical
files, rebuilds all 23 specification/certificate files, and compares their
bytes with this package. It also checks the proof/PDF review and the scoped
negative certificates.

The new producers are derived from the v78 sources and Gabe Conant's notes
with Astra 6.2; see the root attribution file. They run against temporary
byte-pinned archives. Historical code and polynomial tables are unchanged.
Two exact historical name-spelling restorations occur only in those
temporary archives and are bound by both current and historical SHA-256.

## Independent checks and their scope

- check_degrees.py reconstructs all changed general and ordinary-abc
  circuits, compares unchanged point/test prefixes, verifies each input
  squareclass identity and pole, and independently replays all operator
  majorants, denominators, norm guards and final degree/height/support bounds.
- check_semantic_normalization.py verifies the manuscript's ordered contact
  factor identities and the selected balanced representative directly.
- check_weak_bb_full.py and check_weak_bb.py independently reconstruct both
  weak-abc sources, every denominator and the nine staged guard removals.
  Concrete corruption controls must be rejected.
- check_scalar_arithmetic.py uses exact integers and fractions for the
  67 residue classes, local preparations, exceptional sets and L=143 ledger.
- finite_twists_check.py checks the finite descent/genus computations,
  independent class-number comparisons and exact pole/sharing identities.
- check_height_improvements.py checks the seed, Shimura/formal-log identities,
  quadratic predicate inventory and multiplication estimates.

No independent checker imports a new construction producer. Pinned
historical circuit interfaces and independent majorant routines are reused.
The certificates prove their finite assertions; the infinite arithmetic
implications use the written proofs and cited external theorems.

The normalization-menu JSON files record bounded discovery searches:
nine ordinary-abc factor choices, 48 weak-abc choices, and the general
scalar/contact factor menus. They establish no global optimum. The selected
five complete sources are rebuilt and independently verified by the release
gate; menu exploration is not substituted for that verification.
