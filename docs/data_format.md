# Exact polynomial data formats

## Quartic coefficient tables

The leading tables are in `computation/quartic/family238_v18`, `family318_v18`, and the additional-abc `family_abc93_v18`.

| Family | Total variables | Quadratic equations | Terms with parameter powers separate | Ordinary monomials |
|:--|--:|--:|--:|--:|
| 238 | 238 | 212 | 2925 | 2924 |
| 318 | 318 | 290 | 5061 | 5060 |
| 93, **additional abc** | 93 | 81 | 921 | 920 |

Each family has exact degree four and integer content one. The support counts hold for every positive coefficient parameter. The inherited-premise families use integers $N\ge1$; the additional-abc family uses odd shifts $B\ge3$. The 318-variable member at $N=27464$ has a certified defining theorem under the stated arithmetic inputs. The 238-variable family requires a sufficiently large $N$ with ineffective threshold; its support and height computations do not certify a defining member.

The fixed coefficient is $A_N=149^{2N+1}$ in the 238-variable family and $A_N=80989^{2N+1}$ in the 318-variable family. In each family,

$$P_N=\sum_j Q_{N,j}^2,$$

where the complete quadratic-system file lists all residuals $Q_{N,j}$. The parameter is not an extra variable. The 318-variable tables use `integer-quadratic-family-fixed-difference-v18` and `integer-quartic-family-fixed-difference-v18`. The 238- and 93-variable quadratic tables retain their source schemas, `integer-quadratic-family-v13` and `integer-quadratic-family-abc-v1`; both expanded quartics use `integer-quartic-family-fixed-difference-v18`. They share these fields:

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

$$H(P_N)=149^{4N+2}+1\qquad(N\ge53)$$

for the 238-variable family, and $H(P_N)=80989^{4N+2}+1$ for $N\ge23$ in the 318-variable family.

For the 318-variable family at $N=27464$, this number has exactly 1,791,283 binary digits. The machine-readable results retain the coarser uniform bound $H(P_N)<2^{1520}A_N^2$ as well.

## Exact source dependencies

The explicit source chain passes from family342 through family322 to family318_v18. The final builder and independent checker replace the common point chart and normalize the numerator logarithms; they separately verify the exact coefficient expansion. The leading existence family follows the exact dependency chain family297 to family279 to family273 to family267 to family263 to family259_v17 to family249_v17 to family248_v17 to family238_v18. The 259 checker independently reconstructs from family267; the 249 checker independently reconstructs the ten-contact polynomial and all subsequent changes from the pinned 259 source. The 248 checker also reconstructs independently from family259, including the shorter scalar chain and the forced prime149. The checkers separately reconstruct the contact polynomial, the degree-ten evaluation and its degree-twenty source dependencies, every changed quadratic row, all five local factors, and the full quartic. The final four-coordinate common-point transformation also reads the pinned additional-abc source in family_abc97_v17. The independent final checker reconstructs the common-point equations and direct ratios, verifies the rational six-row change and its determinant, and independently expands the complete quartics. The producers and coefficient checkers share no polynomial arithmetic implementation. The source chain continues through the shared-weight and mixed-order families to the pinned baseline. Original large source tables are distributed as deterministic gzip archives; their uncompressed lengths and hashes are recorded in the compressed-source metadata. The restoration script rejects conflicting existing files.

`PROVENANCE.json` in `computation/quartic` binds precise source commits, distributed computational files, and mathematical proofs. Every final quartic coefficient is stored; reconstruction requires no search or unpublished intermediate polynomial.

## Few-variable specifications

The leading specifications are in `computation/few_variables/merged25/active25` and `computation/few_variables/active_elimination/active29`. Their guarded sources are in `merged25/certificate` and `effective29_nontorsion`. They have 24 and 28 retained rational coordinates, respectively, followed by one additional separating coordinate.

Nine independent monic quartic point generators define a finite algebra $B$ of rank $b=2^{18}$. Adding two or four monic quadratic pole generators gives $A$ of rank $2^{20}$ or $2^{22}$. The guard has the form $G=g\prod q_i$, where $g\in B$ and each $q_i$ is a pole generator; hence $G^2\in B$.

Write

$$\det(I-vM_{G^2})=\sum_{j=0}^{b}a_jv^j,\qquad a_0=1.$$

For each $r=1,\ldots,b$, the specification uses $a_r$ and the corresponding characteristic-polynomial relation to isolate the branches on which the guard is nonzero. The point discriminants, a sum of squared matrix entries, and $a_r$ give an explicit separation scale. A polynomial element $\beta_r$ separates the surviving characters. Every division used in the proof is cleared in its polynomial definition.

Put $H_r(U)=\det(I-UM_{\beta_r})$. The final polynomial is

$$H_b(U)\prod_{r=1}^{b-1}\left(H_r(U)^2+\sum_{j>r}a_j^2\right).$$

It has exactly 262,144 finite-product factors. Incorrect degree cases are rejected, and a rational zero in the correct case gives a rational source character. The construction covers disappearing branches and inactive nilpotents. The [finite-algebra proof](../papers/finite_algebra/active_finite_algebra_20261109_v15.pdf) gives the full formula. No rank-sized matrix or monomial expansion is materialized.

| Quantity | 25-variable family | Explicit 29-variable polynomial |
|:--|:--|:--|
| Degree upper bound | less than $2^{87}$ | less than $2^{89}$ |
| Exact degree majorant | 104263275909198787271196672 | 394212872202031272474705920 |
| Full finite-algebra rank | 1048576 | 4194304 |
| Number of finite-product factors | 262144 | 262144 |
| Fixed coefficient exponent | sufficiently large odd $L$; threshold ineffective | 137731, certified |
| Coefficient-height bound for a certified defining member | no effective bound supplied | at most $2^{2^{99}}$ |

The 25-variable source combines scalar and comparison conditions in two pole predicates. Its normalization and denominator exponents are both seven. Ten squared reciprocal-abscissa functions and six plain-parameter comparison functions give fourth-order extraction. Every normalization denominator and the nonzero slope are guarded. The independent source audit checks nine point quartics, two rational square clearings, and 152 atomic guard factors exactly; fifteen independent finite-field evaluations supplement the direct formula audit.

The $L=3$ fixture has binary logarithmic coefficient-norm bound 674973008955294037667741677, below $2^{90}$. This does not certify a defining polynomial at that value. The uniform degree calculation treats $76249^L$ and $76249^{(L+1)/2}$ as separate coefficient symbols of degree zero, and the independent checker sums all active cases literally. The point weights are six, the pole weights are 1181594 and 6716314, and the guard weight is 9642537.

For the explicit 29-variable construction,

$$\log_2\|F\|_1\le558578343639412157650224021485.$$

All these figures are bounds, not exact degrees or coefficient heights. SHA-256 digests bind the sources and output specifications. The older 27-variable construction remains a pinned arithmetic and computational dependency.

## Structural certificates and verification boundary

The number-field certificate checks the finite-difference identity for degrees 1 through 64, exact quadratic norm examples, and elliptic point computations by two independent finite-field counting methods. The input-normalization certificate checks all specified residue classes and lists witnesses for all 128 final cases. The uniform mathematical results are proved in their papers; finite cases do not substitute for the proofs.

Exact coefficient data and passing checks establish the algebraic specifications and the stated finite assertions. Projection theorems additionally use the arithmetic hypotheses identified in the papers. See the [reproducibility guide](reproducibility.md) for commands and the [arithmetic guide](arithmetic_inputs.md) for scope.

## Additional-hypothesis specifications

The weak-abc 13-variable family is stored in `computation/few_variables/weak_abc13`. Three monic quartic point generators and two monic quadratic pole generators give a finite algebra of rank 256 over 12 retained coordinates. The point algebra has rank 64, so the final polynomial has 64 factors and one additional rational coordinate. Its degree is at most 12339485119488, less than $2^{44}$, uniformly in the fixed odd shift $B$. The supplied $B=3$ fixture has binary logarithmic coefficient-norm bound 29454018907833, less than $2^{45}$; it is not certified to exceed the ineffective defining threshold. All assumptions and guard conventions are recorded in the module's source specification.

The 93-variable additional-abc quartic tables use a fixed odd input shift $B$ instead of $A_N$. Their 81 primitive quadratic rows give 921 parameter-separated terms and exactly 920 ordinary monomials. The coefficient height for $B\ge3$ is $\max(4153456,B^2+797687)$. The `parameterPower` field is a power of $B$ and contributes zero to polynomial degree. The affine input-coordinate change puts $B$ in only one quadratic row, while $\beta=L_0-I_0$ appears elsewhere. Every row and every quartic coefficient is stored. The sufficient defining shift is ineffective; support and height formulas for numerical fixtures are algebraic assertions only.

## Exact counts and support upper bounds

An ordinary monomial is a product of the polynomial coordinates after all fixed coefficient parameters have been substituted. Distinct powers of a fixed parameter attached to the same coordinate monomial count only once. Complete quartic expansions certify their exact ordinary support counts.

The 25-, 29-, and 13-variable determinant polynomials have not been expanded. Their exact support counts are explicitly unknown. Let $n$ be the total number of coordinates, $D$ the certified total-degree majorant, $b$ the rank of the point algebra, and $d$ the rank of the full algebra. Each determinant $H_r(U)$ has degree at most $d$ in $U$, globally including incorrect degree strata. The final product therefore has degree at most $E=(2b-1)d$ in that coordinate. The number of possible coordinate monomials is at most

$$
\binom{D+n}{n}-\binom{D-E+n-1}{n},
$$

with the second term omitted when $E\ge D$. The independent `merged25/check_merged_bounds.py` certificate computes the 25-variable bound, below $2^{2035}$. The retained `check_monomial_bounds.py` certificate computes the other two current bounds, below $2^{2417}$ and $2^{509}$. These are uniform support bounds, not exact monomial counts or assertions that all those monomials occur.
