# Exact polynomial data formats

## Quartic coefficient tables

The leading tables are in `computation/quartic/family228_v19`, `family265_v19`, and the additional-abc `family_abc91_v19`.

| Family | Total variables | Quadratic equations | Terms with parameter powers separate | Ordinary monomials |
|:--|--:|--:|--:|--:|
| 228 | 228 | 202 | 2830 | 2829 |
| 265 | 265 | 237 | 3486 | 3485 |
| 91, **additional abc** | 91 | 79 | 927 | 926 |

Each family has exact degree four and integer content one. The support counts hold for every positive coefficient parameter. The inherited-premise families use integers $N\ge1$; the additional-abc family uses odd shifts $B\ge3$. The 265-variable member at $N=14521$ has a certified defining theorem under the stated arithmetic inputs. The 228-variable family requires a sufficiently large $N$ with an ineffective threshold; its support and height computations do not certify a defining member.

The fixed coefficient is $A_N=149^{2N+1}$ in both inherited-premise families. In each family,

$$P_N=\sum_j Q_{N,j}^2,$$

where the complete quadratic-system file lists all residuals $Q_{N,j}$. The parameter is not an extra variable. The 228- and 91-variable quadratic tables use `integer-quadratic-family-reciprocal-factors-v19`; their expanded quartics use `integer-quartic-family-reciprocal-factors-v19`. The four-factor 265-variable tables use `integer-quadratic-family-four-factors-v19` and `integer-quartic-family-four-factors-v19`. They share these fields:

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

for both inherited-premise families. For the 265-variable family at $N=14521$, this is $149^{58086}+1$, which has exactly 419333 binary digits. The machine-readable reports retain the exact maximum constant coefficient and the largest linear coefficient multiplier as well.

## Exact source dependencies

The reciprocal-factor builder reads the pinned quadratic systems `family238_v18`, `family276_v19`, and `family_abc93_v18`. Its independent checker reconstructs the replacement factor equations, reciprocal-weight chains, and removed fourth-power definitions, then expands every quadratic square independently. The source and checker share no polynomial arithmetic implementation. These source systems, and the earlier systems needed to reconstruct them, are retained as exact dependencies rather than current leading results.

The 265-variable construction reads `family266_v19`, retains its scalar and point equations, and replaces each of its three comparison products by four factors. Eight shared rational coordinates store the four deep-comparison fourth powers; one fifth-power weight is added per comparison product. The builder and independent checker are `build_quartic265_v19.py` and `check_quartic265_v19.py`. The 266-variable tables remain a reconstruction dependency.

The three-detector source for the explicit quartic is reconstructed by `build_quartic276_v19.py` and independently checked by `check_quartic276_v19.py`. The final reciprocal equations leave the factor values unchanged where their weights are nonzero. The defining equations exclude zero weights in the inherited-premise families; in the abc family the two cleared factor equations and the point-pair chart exclude that stratum. These domain assertions are proved in the current papers and checked at the level of exact identities.

Original large source tables are distributed as deterministic gzip archives; their uncompressed lengths and hashes are recorded in the compressed-source metadata. The restoration script rejects conflicting existing files. `PROVENANCE.json` in `computation/quartic` binds the precise source commits, distributed computational files, current proof files, and exact source dependencies. Every final quartic coefficient is stored; reconstruction requires no search or unpublished intermediate polynomial.

## Few-variable specifications

The leading specifications are in `computation/few_variables/merged25_v19/active25` and `computation/few_variables/effective27_v19/active27`. Their guarded sources are in the corresponding `certificate` subdirectories. They have 24 and 26 retained rational coordinates, respectively, followed by one additional separating coordinate.

Nine independent monic quartic point generators define a finite algebra $B$ of rank $b=2^{18}$. Adding two or three monic quadratic pole generators gives $A$ of rank $2^{20}$ or $2^{21}$. The guard has the form $G=g\prod q_i$, where $g\in B$ and each $q_i$ is a pole generator; hence $G^2\in B$.

Write

$$\det(I-vM_{G^2})=\sum_{j=0}^{b}a_jv^j,\qquad a_0=1.$$

For each $r=1,\ldots,b$, the specification uses $a_r$ and the corresponding characteristic-polynomial relation to isolate the branches on which the guard is nonzero. The point discriminants, a sum of squared matrix entries, and $a_r$ give an explicit separation scale. A polynomial element $\beta_r$ separates the surviving characters. Every division used in the proof is cleared in its polynomial definition.

Put $H_r(U)=\det(I-UM_{\beta_r})$. The final polynomial is

$$H_b(U)\prod_{r=1}^{b-1}\left(H_r(U)^2+\sum_{j>r}a_j^2\right).$$

It has exactly 262,144 finite-product factors. Incorrect degree cases are rejected, and a rational zero in the correct case gives a rational source character. The construction covers disappearing branches and inactive nilpotents. The [finite-algebra proof](../papers/finite_algebra/active_finite_algebra_20261109_v15.pdf) gives the full formula. No rank-sized matrix or monomial expansion is materialized.

| Quantity | 25-variable family | Explicit 27-variable polynomial |
|:--|:--|:--|
| Degree upper bound | less than $2^{85}$ | less than $2^{87}$ |
| Exact degree majorant | 20747108969426225455955968 | 85829362869408651982929920 |
| Full finite-algebra rank | 1048576 | 2097152 |
| Number of finite-product factors | 262144 | 262144 |
| Fixed coefficient exponent | sufficiently large odd $L$; threshold ineffective | 125001, certified |
| Coefficient-height bound for a certified defining member | no effective bound supplied | less than $2^{2^{102}}$ |
| Uniform support upper bound | less than $2^{1979}$ | less than $2^{2192}$ |

Both sources combine scalar and comparison conditions in common pole predicates. The ten raw reciprocal-abscissa functions and the two input comparisons use denominator order one. The three Lucas-label comparisons and the Lucas residual use order three. Only the six rational scalar components are normalized, by $\Phi_R(D)=RD/(1+RD)$. The four reciprocal-abscissa components use numerator factor $R$ and denominator order one; the two scalar-ratio components use numerator factor $R^3$ and denominator order three. Formal-logarithm precision four uses the plain local parameter. Every scalar normalization denominator and the nonzero slope are guarded. Completeness chooses the common elliptic index divisible by the selected comparison primes, with compatibility proved by the clustered-prime and Hasse bounds.

The 25-variable source uses two detector scales, $1$ and $(1+\rho T^2)^2$, where $T$ is the rational trace of the sum of four root abscissas. The effective 27-variable source uses three scales: $1$, $(1+\rho S_0^2)^2$, and $(1+\rho(S_0+S_1)^2)^2$, where the sum of the four root abscissas is $S_0+S_1\sqrt2$. Here $\rho$ is the rational scalar contact coefficient defined in the papers. The effective sum-height estimate supplies the certified fixed exponent for this second source.

| Exact source census | 25 variables | 27 variables |
|:--|--:|--:|
| Rational coefficient nodes | 5864 | 6898 |
| Integer coefficient nodes | 2240 | 2588 |
| Point quartics | 9 | 9 |
| Pole-square clearings | 2 | 3 |
| Atomic guard factors | 136 | 164 |

The independent source audits prove the affine source-to-integer conversion, point quartics, square clearings, and guard coverage exactly. Fifteen independent finite-field reconstructions for each source supply bounded supplementary evidence for the new rational formulas; those samples are not universal identity proofs or arithmetic projection proofs.

The $L=3$ fixture of the 25-variable family has binary logarithmic coefficient-norm bound 132562563423570884606820333, below $2^{87}$. This does not certify a defining polynomial at that value. For the certified 27-variable member at $L=125001$,

$$\log_2\|F\|_1\le3593722961921650418383728672749<2^{102}.$$

The uniform degree calculations treat $76249^L$ and $76249^{(L+1)/2}$ as separate coefficient symbols of degree zero. The independent checkers sum all active cases literally. The point weights are six. The 25-variable pole weights are 266506 and 1316106, with guard weight 1930897. The 27-variable pole weights are 266506, 1316106, and 1316106, with guard weight 3534038.

All degree, support, and coefficient-norm figures for these determinant polynomials are upper bounds. SHA-256 digests bind the guarded sources and output specifications. Earlier few-variable sources remain pinned arithmetic or computational dependencies; they are not the current leading specifications.

## Structural certificates and verification boundary

The number-field certificate checks the finite-difference identity for degrees 1 through 64, exact quadratic norm examples, and elliptic point computations by two independent finite-field counting methods. The input-normalization certificate checks all specified residue classes and lists witnesses for all 128 final cases. The uniform mathematical results are proved in their papers; finite cases do not substitute for the proofs.

Exact coefficient data and passing checks establish the algebraic specifications and the stated finite assertions. Projection theorems additionally use the arithmetic hypotheses identified in the papers. See the [reproducibility guide](reproducibility.md) for commands and the [arithmetic guide](arithmetic_inputs.md) for scope.

## Additional-hypothesis specifications

The weak-abc 13-variable family is stored in `computation/few_variables/weak_abc13`. Three monic quartic point generators and two monic quadratic pole generators give a finite algebra of rank 256 over 12 retained coordinates. The point algebra has rank 64, so the final polynomial has 64 factors and one additional rational coordinate. Its degree is at most 12339485119488, less than $2^{44}$, uniformly in the fixed odd shift $B$. The supplied $B=3$ fixture has binary logarithmic coefficient-norm bound 29454018907833, less than $2^{45}$; it is not certified to exceed the ineffective defining threshold. All assumptions and guard conventions are recorded in the module's source specification.

The 91-variable additional-abc quartic tables use a fixed odd input shift $B$ instead of $A_N$. Their 79 primitive quadratic rows give 927 parameter-separated terms and exactly 926 ordinary monomials. The coefficient height for $B\ge3$ is $\max(4153456,B^2+797683)$. The `parameterPower` field is a power of $B$ and contributes zero to polynomial degree. The affine input-coordinate change puts $B$ in only one quadratic row, while $\beta=L_0-I_0$ appears elsewhere. Every row and every quartic coefficient is stored. The sufficient defining shift is ineffective; support and height formulas for numerical fixtures are algebraic assertions only.

## Exact counts and support upper bounds

An ordinary monomial is a product of the polynomial coordinates after all fixed coefficient parameters have been substituted. Distinct powers of a fixed parameter attached to the same coordinate monomial count only once. Complete quartic expansions certify their exact ordinary support counts.

The 25-, 27-, and 13-variable determinant polynomials have not been expanded. Their exact support counts are explicitly unknown. Let $n$ be the total number of coordinates, $D$ the certified total-degree majorant, $b$ the rank of the point algebra, and $d$ the rank of the full algebra. Each determinant $H_r(U)$ has degree at most $d$ in $U$, globally including incorrect degree strata. The final product therefore has degree at most $E=(2b-1)d$ in that coordinate. The number of possible coordinate monomials is at most

$$
\binom{D+n}{n}-\binom{D-E+n-1}{n},
$$

with the second term omitted when $E\ge D$. The independent `merged25_v19/check_merged_bounds.py` and `effective27_v19/check_effective_bounds.py` certificates compute bounds below $2^{1979}$ and $2^{2192}$, respectively. The retained `check_monomial_bounds.py` certificate computes the 13-variable bound below $2^{509}$. These are uniform support bounds, not exact monomial counts or assertions that every possible monomial occurs.
