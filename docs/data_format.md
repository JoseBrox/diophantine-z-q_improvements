# Exact polynomial data formats

## Quartic coefficient tables

The leading tables are in `computation/quartic/family263`, `family322`, and the additional-abc `family_abc98`.

| Family | Total variables | Quadratic equations | Terms with parameter powers separate | Ordinary monomials |
|:--|--:|--:|--:|--:|
| 263 | 263 | 237 | 3313 | 3312 |
| 322 | 322 | 294 | 4993 | 4992 |
| 98, **additional abc** | 98 | 86 | 885 | 882 |

Each family has exact degree four and integer content one. The support counts hold for every positive coefficient parameter. The inherited-premise families use integers $N\ge1$; the additional-abc family uses odd shifts $B\ge3$. The 322-variable member at $N=27464$ has a certified defining theorem under the stated arithmetic inputs. The 263-variable family requires a sufficiently large $N$ with ineffective threshold; its support and height computations do not certify a defining member.

For these two inherited-premise families the fixed coefficient is $A_N=80989^{2N+1}$. In each family,

$$P_N=\sum_j Q_{N,j}^2,$$

where the complete quadratic-system file lists all residuals $Q_{N,j}$. The parameter is not an extra variable. The 322-variable tables use `integer-quadratic-family-v6` and `integer-quartic-family-v6`; the 263-variable tables use the corresponding `v11` labels. They share these fields:

| Field | Meaning |
|:--|:--|
| `variables` | Total coordinate count, including input |
| `inputCoordinate` | The distinguished rational input; value 1 |
| `coordinates` | Consecutive coordinate identifiers, names, and stable source identifiers |
| `fixedParameter` | The fixed integer coefficient and its expression in $N$ |
| `residuals` | Complete primitive integer quadratic equations |
| `terms` | Complete coefficient terms of an equation or expanded polynomial |
| `parameterPower` | Nonnegative power of $A_N$ in a coefficient term |
| `monomial` | Sorted coordinate identifiers, repeated according to exponent |
| `coefficient` | Signed integer, written as a decimal string |

A term with `parameterPower` equal to 1, `monomial` equal to `[2,2,5]`, and `coefficient` equal to `"-7"` means $-7A_NX_2^2X_5$. An empty monomial is a constant term. Grouping terms with the same coordinate monomial gives its ordinary integer coefficient after $A_N$ is fixed. Powers of $A_N$ contribute zero to total degree.

Stable source identifiers refer to the pinned source circuit, not the consecutive coordinate identifiers of the final polynomial. The constructor records deleted and new source coordinates, changed weight rows, and the affine scalar normalization. Coordinate 489 in source notation is replaced by the actual scalar contact product $r$. The change is invertible over the rational witnesses, has nonzero affine determinant $-45771136$, and preserves the input.

The independent checker expands each sum of squares separately, compares every coefficient, and verifies the affine change by reverse substitution. The coefficient of $r^2$ is $A_N^2+1$. Every other coefficient is constant or a pure multiple of $A_N$, which proves noncancellation for positive $A_N$. Exact comparisons with the largest constant and linear coefficients prove

$$H(P_N)=80989^{4N+2}+1\qquad(N\ge23).$$

At $N=27464$, this number has exactly 1,791,283 binary digits. The reports retain the coarser uniform bound $H(P_N)<2^{1520}A_N^2$ as well.

## Exact source dependencies

The even-valuation builder reads and hash-checks family342 to produce family322. The leading existence family follows the exact dependency chain family297 to family279 to family273 to family267 to family263. The checkers separately reconstruct the contact polynomial, the shared and separate degree-twenty evaluations, every changed quadratic row, all five local factors, and the full quartic. The producers and checkers share no polynomial arithmetic implementation. The source chain continues through the shared-weight and mixed-order families to the pinned baseline. Original large source tables are distributed as deterministic gzip archives; their uncompressed lengths and hashes are recorded in the compressed-source metadata. The restoration script rejects conflicting existing files.

`PROVENANCE.json` in `computation/quartic` binds precise source commits, distributed computational files, and mathematical proofs. Every final quartic coefficient is stored; reconstruction requires no search or unpublished intermediate polynomial.

## Few-variable specifications

The leading specifications under the inherited arithmetic premises are in computation/few_variables/active_elimination/active27 and active29. Their source algebras are supplied by trace27_nontorsion and effective29_nontorsion. They have 26 and 28 retained coordinates, respectively, and one additional rational coordinate.

Nine independent monic quartic point generators define a finite algebra B of rank b=2^18. Adding three or four monic quadratic pole generators gives A of rank 2^21 or 2^22. The guard has the form G=g times the product of the pole generators, with g in B; hence T=G^2 belongs to B.

Write

$$
\det(I-vM_T)=\sum_{j=0}^{b}a_jv^j,\qquad a_0=1.
$$

For each r=1,...,b, the specification uses a_r and the corresponding characteristic-polynomial relation to construct a multiple of the idempotent selecting precisely the branches on which the guard is nonzero. Point discriminants, a sum of squared matrix entries, and the product a_r supply an explicit separation scale. One polynomial element beta_r separates the surviving characters. All divisions used in the proof are cleared in its polynomial definition.

Put H_r(U)=det(I-U M_beta_r). The final polynomial is

$$
H_b(U)\prod_{r=1}^{b-1}
 \left(H_r(U)^2+\sum_{j>r}a_j^2\right).
$$

It has exactly b=262144 factors. Wrong degree cases are rejected, and a rational zero in the correct case gives a one-dimensional rational eigenspace; the commuting source multiplication matrices recover a rational source character. The construction covers disappearing branches and inactive nilpotents. The full proof and exact formula for beta_r are in the finite-algebra paper. No rank-sized matrix or monomial expansion of these enormous polynomials is materialized.

| Quantity | 27-variable family | Explicit 29-variable polynomial |
|:--|:--|:--|
| Degree upper bound | less than 2^87 | less than 2^89 |
| Exact degree majorant | 111295944630211471361441792 | 394212872202031272474705920 |
| Number of finite-product factors | 262144 | 262144 |
| Fixed coefficient exponent | sufficiently large odd L; threshold ineffective | 137731, certified |
| Coefficient-height bound for a certified defining member | no effective bound supplied | at most 2^(2^99) |

These are upper bounds, not exact degrees or heights. For the explicit construction,

$$
\log_2\|F\|_1\le558578343639412157650224021485.
$$

The 27-variable numerical fixture has log2 norm at most 217401420128398649581869203437, less than 2^98, at L=137731. This specific member is not certified to define the integers. The degree bound is uniform in L.

SHA-256 digests bind source and output specifications. The independent checker imports no producer code and verifies every source coefficient dependency, the guard's pole exponents, weighted companion norms, and the sum of bounds for all factors. Seven exact degeneration examples compare determinants computed by permutation expansion and Newton traces, and check the relevant characteristic-polynomial gcds.

## Structural certificates and verification boundary

The number-field certificate checks the finite-difference identity for degrees 1 through 64, exact quadratic norm examples, and elliptic point computations by two independent finite-field counting methods. The input-normalization certificate checks all specified residue classes and lists witnesses for all 128 final cases. The uniform mathematical results are proved in their papers; finite cases do not substitute for the proofs.

Exact coefficient data and passing checks establish the algebraic specifications and the stated finite assertions. Projection theorems additionally use the arithmetic hypotheses identified in the papers. See the [reproducibility guide](reproducibility.md) for commands and the [arithmetic guide](arithmetic_inputs.md) for scope.

## Additional-hypothesis specifications

The weak-abc 13-variable family is stored in `computation/few_variables/weak_abc13`. Three monic quartic point generators and two monic quadratic pole generators give a finite algebra of rank 256 over 12 retained coordinates. The point algebra has rank 64, so the final polynomial has 64 factors and one additional rational coordinate. Its degree is at most 12339485119488, less than $2^{44}$, uniformly in the fixed odd shift $B$. The supplied $B=3$ fixture has binary logarithmic coefficient-norm bound 29454018907833, less than $2^{45}$; it is not certified to exceed the ineffective defining threshold. All assumptions and guard conventions are recorded in the module's source specification.

The 98-variable additional-abc quartic tables use a fixed odd input shift $B$ instead of $A_N$. Its 86 primitive quadratic rows give 885 parameter-separated terms and exactly 882 ordinary monomials. Its coefficient height for $B\ge3$ is $\max(11600064,2B^4+169997)$. The `parameterPower` field is a power of $B$ and still contributes zero to polynomial degree. Every quadratic row and every quartic coefficient is stored. The sufficient defining shift is ineffective; support and height formulas for numerical fixtures are algebraic assertions only.

## Exact counts and support upper bounds

An ordinary monomial is a product of the polynomial coordinates after all fixed coefficient parameters have been substituted. Distinct powers of a fixed parameter attached to the same coordinate monomial count only once. Complete quartic expansions certify their exact ordinary support counts.

The 27-, 29-, and 13-variable determinant polynomials have not been expanded. Their exact support counts are explicitly unknown. Let $n$ be the total number of coordinates, $D$ the certified total-degree majorant, $b$ the rank of the point algebra, and $d$ the rank of the full algebra. Each determinant $H_r(U)$ has degree at most $d$ in $U$, globally including incorrect degree strata. The final product therefore has degree at most $E=(2b-1)d$ in that coordinate. The number of possible coordinate monomials is at most

$$
\binom{D+n}{n}-\binom{D-E+n-1}{n},
$$

with the second term omitted when $E\ge D$. The independent `check_monomial_bounds.py` certificate computes these integer bounds exactly and verifies strict upper bounds $2^{2202}$, $2^{2417}$, and $2^{509}$, respectively. These are uniform support bounds, not exact monomial counts or assertions that all those monomials occur.
