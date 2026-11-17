# Exploratory search for a 194-coordinate quartic

**Outcome: no new quartic was obtained. The established general count remains
195.** Z3 returned `unsat` on each of the three precisely specified support
models below. This package records negative computational evidence for those
models. It is not a lower bound for quartics, geometric charts, or arbitrary
coordinate changes.

The files contain the corrected real-part aggregate. Its terms are the matching
component products in `Re(h(h+s+t))`; imaginary cross terms are absent.

## Source and exact row change

`source195.json` is the published 175-row, 195-coordinate table at
`computation/quartic/affine_laurent195_v45/quadratic-family.json`, from commit
`7501669160c1662a742ddd54baed364a47c82ddc` of
`JoseBrox/diophantine-z-q_improvements`. Its SHA-256 is

```text
304f94843c1a4ac94fcd5f1295fee8b532e7f0424e638314d892c556e2fbfdf9
```

`reference-row-map.json` specifies an invertible constant change on the two
reference-square equations and six reference equations. It reverses the dense
primitive reference basis, with all individual row normalizations accounted
for. `reversed_reference_basis.json` is the resulting full table. The
standard-library checker verifies every source-row identity and the nonzero
determinant of this eight-dimensional change. All remaining source equations
are unchanged at this stage.

## The proposed point charts and nominal count

For each of roles 1, 3 and 4, the model replaces seven field coordinates by six
field coordinates `s,t,F,G,h,d`. Put `p=h+s+t` and use

```math
d=pF,\qquad d=hG,\qquad
D(F+G)=(s-t)h-t^2,\qquad
1=d(s-t)-DFG,\qquad D=11-6\sqrt2.
```

The comparison rows are `L s = k S` and `L0 t = k TH` for roles 1 and 3,
with the affine `L-1` and `L0-1` versions for role 4. The finite difference
abscissa is `h(h+s+t)` and is inserted into the real aggregate directly.
The functions `F,G` are the two reciprocal abscissas. Their conjugation in
the opposite-place tests changes coefficient signs, not supports.

Two chosen reciprocal squares remain as field helpers. The three helper
choices searched are

| Model | Retained square helpers |
|---|---|
| `A4_B4` | Primary and alternate reciprocal squares for role 4 |
| `A1_B3` | Primary square for role 1 and alternate square for role 3 |
| `A1_A3` | Primary squares for roles 1 and 3 |

Here `Ai=f(Ui)` and `Bi=conjugate(f(Vi))`. The stored helpers represent the
squares of the named functions. The count bookkeeping is

```math
195-42+36+4+1=194.
```

The final `+1` is an additional rational monomial-unit coordinate. This is
only the dimension of the proposed storage arrangement. No 194-coordinate
quadratic table, quartic expansion, or complete source-transfer theorem was
constructed.

## Physical units and the extra coordinate

The existing units have exponent vectors in `(u,v)`:

| Coordinate | Physical value | Exponent |
|---|---|---|
| 77 | `u=q0` | `(1,0)` |
| 78 | `u^-1` | `(-1,0)` |
| 90 | `v=q1/q0` | `(0,1)` |
| 91 | `v^-1` | `(0,-1)` |
| 92 | `u^-1*v^-2` | `(-1,-2)` |

In particular the second physical weight is **`q1=u*v`**. It is not `v`.
The existing guards are `x77*x78=1`, `x90*x91=1` and
`x77*x92=x91^2`.

Let `P0` be the five exponent vectors together with `(0,0)`, representing
the constant 1. The extra exponent ranges over all **32 distinct vectors**
in `(P0+P0-P0)\P0`. Such a vector `a+b-c` has a quadratic defining equation

```math
Y\,U_c=U_aU_b.
```

Each `U_e` is one of the existing unit coordinates or 1. The existing guards
make `U_c` nonzero, so this equation determines `Y` uniquely and does not
require another inverse coordinate. The possibilities include
`u*Y=x92^2` and `v*Y=x92^2`, giving exponents `(-3,-4)` and `(-2,-5)`.

## Literal detector model

The physical factor-output unit exponents are `(1,0)` in detector 0 and
`(1,2)` in detector 1. More precisely, the inherited outputs are

```math
\Phi_{jk}=C^{\alpha_k}u v^{2j}
  (x_{118+16j+2k}+\sqrt2\,x_{119+16j+2k}),\qquad
\alpha=(1,1,1,0,-1),
```

up to the fixed nonzero diagonal coefficient normalizations already present
in the source. Powers of the fixed nonzero coefficient parameter `C` do not
affect Laurent unit degree. The physical-to-stored mapping is the one
verified in `negative_results/computation/physical_detector_scaling_v67`.

Each detector has four regular factors. Each regular factor has a constant
term, two odd-power test slots and one square-weight linear-test slot. Eight
quadratic tests are assigned bijectively to the eight odd-power slots:
the fourth powers of `C2,C3,C4,G`, and the four reciprocal squares whose
helpers were not retained. A comparison fourth power uses exponent 9 in
the first slot or 11 in the second; a raw reciprocal square uses exponent
1 or 3, respectively. The even slot is `q_j^2 L`.

The special factor is

```math
1+q_j^4 I^8+q_j L_4+q_j^2 L_5+q_j^3 L_6.
```

The seven linear tests are `DH^2`, `B0^2`, `A2^2`, `B2^2`, `C1^4`, and the
two retained reciprocal-square helpers. They are assigned bijectively to
the four ordinary even slots and three special-factor slots. The two
detectors have independent assignments. The local valuation hypotheses
for these exponent choices are those of
`papers/quartic/revised_detector_factors_20261117_v66.tex`. The complete
literal formulas above specify the searched factor model.

The stored quadratic test profiles use unit exponent `(-6,0)` for the
squares of the comparison-square outputs and for `I^8`, and `(0,0)` for
the squares of the newly introduced raw reciprocal coordinates. Existing
linear square outputs use `(-1,0)`; the new square helpers use `(0,0)`.
Every profile and coordinate number is recorded in each JSON model.

## Exact constraints and scope

For each nonunit coordinate there is an **unbounded integer** weight vector
`w_i` in two dimensions, with input weight `w_1=(0,0)`. Each row group has
an unbounded integer divisor vector `r_j`. A term with active-variable
monomial `m` and existing unit exponent `e` is admissible exactly when

```math
e+\sum_{i\in m}w_i-r_j\in P^{(2-|m|)},
```

where `P=P0\cup{extra exponent}`, and `P^(k)` means sums of exactly `k`
elements of `P`; inclusion of zero permits lower degree. Repeated indices
in `m` are counted with multiplicity. The right side describes ordinary
degree at most two after rewriting unit monomials through available
coordinates.

The model imposes a **common multiplier for the two components of each new
field equation**. Retained source equations are separate literal rational
rows, with independent multipliers. The scalar aggregate is a single real
row, with only its actual real-part support. The quadratic-test position
normalization places `C2` in regular factor 0 in each detector, in either
odd-power slot. The retained product-chain supports and all other retained
source rows are included.

These are deliberate model restrictions. The search does not cover all
field-component scalings, all rational equation bases, all geometric
charts, arbitrary affine coordinate changes, other detector exponents,
other helper roles, nonmonomial helpers, or all possible quartics. It does
not establish that 194 variables are impossible. No numerical infeasibility
from a bounded floating-point search is used in this ledger.

## Results and reproduction

With Z3 5.4.1, the corrected models returned:

| Model | Result | Initial corrected run |
|---|---|---:|
| `A4_B4` | `unsat` | 4.19 seconds |
| `A1_B3` | `unsat` | 1.80 seconds |
| `A1_A3` | `unsat` | 2.05 seconds |

The exact timings are descriptive and depend on environment and solver
state. `results/` contains these original corrected outputs. `rerun.json`
contains the standalone reproducer's output. The `.smt2` files contain
the complete asserted formulas and `check-sat-assuming` commands activating
all tracked constraints. They can also be passed directly to a compatible
Z3 executable. No general lower-bound theorem is inferred from these runs.

```sh
python -B check_model.py --output model_certificate.json
python -m pip install -r requirements.txt
python -B solve.py --output rerun.json
```

`check_model.py` uses only the standard library. It authenticates the source,
checks the invertible reference row change, reconstructs every retained
support, expands each new field expression by exact arithmetic in
`Q[sqrt2]`, checks the corrected real aggregate, and verifies all test
profiles, factor-output directions and 32 quadratic unit extensions.
It makes no solver or arithmetic-definability assertion.

`solve.py` requires only the stated Z3 package beyond the standard library.
It reads the portable JSON models directly and imports no search producer
or external repository module. The complete current 195-variable record
is unchanged by this investigation.

## Independent two-factor certificate

The independent standard-library checker `check_projection.py` finds the
obstruction already in the constant terms and the shared squared comparison
coordinate of one regular factor in each detector. If its two powers are
`p0,p1` in `{9,11}`, let `E0,E1` be the exponent vectors of the constant
terms after row normalization. Quadraticity of the comparison-square terms
forces

```math
E_1-E_0=(p_0-p_1,-p_1),\qquad E_0,E_1\in P+P.
```

For each of the 32 available extra units, none of these four differences
occurs between two members of `P+P`. The checker enumerates all 128 cases
using exact integer pairs and imports no solver or search producer. The
obstruction already holds for real scaling weights, before the additional
integer parity conditions. It still concerns only the stated unit basis
and the displayed factor forms. Changing the original unit basis remains
a separate possibility.

```sh
python -B check_projection.py --output projection_certificate.json
```
