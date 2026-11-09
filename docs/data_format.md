# Exact polynomial data formats

## Quartic coefficient tables

The leading tables are in `computation/quartic/family297` and `family342`.

| Family | Total variables | Quadratic equations | Terms with parameter powers separate | Ordinary monomials |
|:--|--:|--:|--:|--:|
| 297 | 297 | 271 | 4269 | 4268 |
| 342 | 342 | 314 | 4939 | 4938 |

Each family has exact degree four and integer content one. The support counts hold for every positive coefficient parameter, hence for every integer $N\ge1$. The 342-variable member at $N=27464$ has a certified defining theorem under the stated arithmetic inputs. The 297-variable family requires a sufficiently large $N$ with ineffective threshold; its support and height computations do not certify a defining member.

The fixed coefficient is $A_N=80989^{2N+1}$. In each family,

$$P_N=\sum_j Q_{N,j}^2,$$

where the complete quadratic-system file lists all residuals $Q_{N,j}$. The parameter is not an extra variable. The `integer-quadratic-family-v5` and `integer-quartic-family-v5` formats have these fields:

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

The shared-weight builder reads the family301 and family351 quadratic systems and verifies their SHA-256 digests. Those systems are reconstructed from family317 and family370, respectively. The source chain is complete in the supplied constructors. The 392-coordinate baseline and original source tables are distributed as deterministic gzip archives; their uncompressed lengths and hashes are recorded in `data/compressed_sources.json`. The restoration script rejects conflicting existing files.

`PROVENANCE.json` in `computation/quartic` binds precise source commits, distributed computational files, and mathematical proofs. Every final quartic coefficient is stored; reconstruction requires no search or unpublished intermediate polynomial.

## Few-variable specifications

The leading specifications are in `computation/few_variables/weighted_elimination/weighted27` and `weighted29`. Their source algebras are supplied by `trace27_nontorsion` and `effective29_nontorsion`, respectively. The 27-variable family has 26 retained coordinates and one additional rational coordinate; the explicit 29-variable construction has 28 retained coordinates and one additional rational coordinate.

Nine monic quartic point generators and three or four monic quadratic pole generators give ranks $2^{21}$ and $2^{22}$. Every pole generator is guarded nonzero. There is one conic chart and one retained quadratic stratum. Matrix entries, algebra generators, selector indices, and finite degree cases are formal polynomial operations, not quantified coordinates.

For a guarded multiplication element $u$, the compiler forms $\det(I-VM_u)=\sum a_kV^k$. In degree case $d$, put $H_d(V)=\sum_{k=0}^d a_kV^k$ and $g_d=\operatorname{Res}(H_d,H_d')$, using the fixed Sylvester degrees $d,d-1$. For $d<n$, use the factor

$$H_d(g_dU)^2+\sum_{k>d}a_k^2.$$

For $d=n$, use the unsquared factor $H_n(g_nU)$. The finite product over the explicitly specified selector range and all degree cases is an ordinary integer polynomial. The constant coefficient $a_0=1$ rejects zero resultants and zero $U$ automatically. The theorem proves that a rational zero yields a rational algebra character with nonzero guard; the converse uses a separating selector. The leading algebras have no additional closed residuals.

Weighted principal minors give $\deg a_k\le kw$. With $S=1+mn(n+1)/2$ and

$$C(n)=2\sum_{d=1}^{n-1}\max(d^3+d,n)+(n^3+n),$$

the total degree is at most $S(wC(n)+n^2)$. The complete norm calculation is recorded in each construction certificate and independently recomputed.

| Quantity | 27-variable family | Explicit 29-variable polynomial |
|:--|:--|:--|
| Degree upper bound | less than $2^{151}$ | less than $2^{157}$ |
| Exact degree majorant | 1622838857795564438964780120527413199713157888 | 154383598645603405051555717167316362269845989152 |
| Number of finite-product factors | 55340258609409818624 | 479615460265661825024 |
| Fixed coefficient exponent | sufficiently large odd $L$; threshold ineffective | 137731, certified |
| Coefficient-height bound for a certified defining member | no effective bound supplied | at most $2^{2^{168}}$ |

These are upper bounds, not exact degrees or heights of the unexpanded polynomials. The explicit construction has

$$\log_2\|F\|_1\le228040944767112830511621792043639838233373391751570.$$

The numerical 27-variable fixture has $H(F)\le2^{2^{162}}$ at $L=137731$; this specific member is not certified to define the integers. SHA-256 digests bind input specifications and output specifications. The independent checker compares exact recurrences and nine small finite-algebra examples, including degree drops, repeated eigenvalues, complex factors, inactive nilpotents, and a zero guard.

## Structural certificates and verification boundary

The number-field certificate checks the finite-difference identity for degrees 1 through 64, exact quadratic norm examples, and elliptic point computations by two independent finite-field counting methods. The input-normalization certificate checks all specified residue classes and lists witnesses for all 128 final cases. The uniform mathematical results are proved in their papers; finite cases do not substitute for the proofs.

Exact coefficient data and passing checks establish the algebraic specifications and the stated finite assertions. Projection theorems additionally use the arithmetic hypotheses identified in the papers. See the [reproducibility guide](reproducibility.md) for commands and the [arithmetic guide](arithmetic_inputs.md) for scope.
