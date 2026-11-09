# Exact polynomial data formats

## Quartic coefficient tables

The leading tables are in computation/quartic/family301 and family351.

| Family | Total variables | Quadratic equations | Terms with parameter powers separate | Ordinary monomials |
|:--|--:|--:|--:|--:|
| 301 | 301 | 275 | 4320 | 4305 |
| 351 | 351 | 323 | 5005 | 4990 |

The ordinary monomial counts hold for every integer N at least 27464. Each family has exact degree four and integer content one. The 351-variable member at N=27464 has a certified defining theorem under the stated arithmetic inputs. The 301-variable family requires a sufficiently large N with ineffective threshold; its support count does not certify a defining member.

The fixed coefficient is A_N=80989^(2N+1). In each family,

$$P_N=\sum_j Q_{N,j}^2,$$

where the complete quadratic-system file lists all Q rows. The parameter is not an extra variable.

The integer-quadratic-family-v4 and integer-quartic-family-v4 formats have these fields:

| Field | Meaning |
|:--|:--|
| variables | Total coordinate count, including input |
| inputCoordinate | The distinguished rational input; value 1 |
| coordinates | Consecutive coordinate identifiers, names, and stable source identifiers |
| fixedParameter | The fixed integer coefficient and its expression in N |
| residuals | Complete primitive integer quadratic equations |
| terms | Complete coefficient terms of an equation or expanded polynomial |
| parameterPower | Nonnegative power of A_N in a coefficient term |
| monomial | Sorted coordinate identifiers, repeated according to exponent |
| coefficient | Signed integer, written as a decimal string |

A term with parameterPower equal to 1, monomial [2,2,5], and coefficient "-7" means -7*A_N*X_2^2*X_5. An empty monomial is a constant term. Grouping all terms with the same coordinate monomial gives its ordinary integer coefficient after A_N is fixed. Powers of A_N contribute zero to total degree.

Stable source identifiers refer to the pinned source circuit; they are not the consecutive coordinate identifiers of the new polynomial. They permit every retained and changed row to be audited. The constructor records all deleted and new source coordinates and the complete grouping of the sixteen tests.

The independent checker expands each sum of squares separately and compares every coefficient. For each ordinary coefficient c_0+c_1*A_N+c_2*A_N^2, its absolute value is bounded by (|c_0|+|c_1|+|c_2|)*A_N^2. The largest such sum has 1520 binary digits. The same coefficient-sum bound proves that no ordinary coefficient vanishes for N at least 27464. The explicit 351-variable polynomial has a largest coefficient with 1,791,357 binary digits.

## Exact source dependencies

The new builders read the family317 and family370 quadratic systems directly and verify their SHA-256 digests. Those systems are reconstructed by the supplied earlier source constructors. The 392-coordinate baseline and the original source tables are distributed as deterministic gzip archives; their uncompressed lengths and hashes are recorded in data/compressed_sources.json. The restoration script rejects conflicting existing files.

PROVENANCE.json in computation/quartic binds the precise source commits, all distributed computational files, and the corresponding mathematical proofs. Every expanded new coefficient is stored; no search or unpublished intermediate polynomial is required for reconstruction.

## Few-variable specifications

The leading standalone modules are computation/few_variables/trace27_nontorsion and effective29_nontorsion. Their exact integer polynomials are described by coefficient graphs and finite-algebra operations. The 27-variable family has 26 retained coordinates and one additional rational coordinate. The explicit 29-variable construction has 28 retained coordinates and one additional rational coordinate.

Nine monic quartic point generators and three or four monic quadratic pole generators give finite-algebra ranks 2^21 and 2^22. Every pole generator is guarded nonzero. There is one conic-chart choice and one retained quadratic stratum. The finite selector range and coefficient-degree cases are explicitly bounded and are compiled into finite products. They are formal indices, not quantified variables.

The expression grammar consists of integer constants, coordinate variables, arithmetic operations, finite products, multiplication matrices, determinants, characteristic polynomials, traces, resultants, and reciprocal polynomials. The companion finite-algebra theorem proves that these expressions form an ordinary integer polynomial with the required projection. The independent verifier checks all coefficient conversions, guards, finite cases, and bound recurrences without expanding that enormous polynomial.

| Quantity | 27-variable family | Explicit 29-variable polynomial |
|:--|:--|:--|
| Degree upper bound | less than 2^154 | less than 2^161 |
| Exact degree majorant | 20373348814943897785292785017798269643599642624 | 2021432499262561030580590567538985948904131919872 |
| Number of finite-product factors | 55340258609409818624 | 479615460265661825024 |
| Fixed coefficient exponent | sufficiently large odd L; threshold ineffective | 137731, certified |
| Coefficient-height bound | no effective bound for a certified defining member | at most 2^(2^171) |

These are proved upper bounds, not asserted exact degrees or heights of the fully expanded polynomials. For the explicit29 specification, the exact upper bound for log_2 of the coefficient height is 1824327990117465218468581252398965551307997696753664. The 27-variable example at L=137731 has height at most 2^(2^165), but it is only an algebraic reproducibility fixture and is not certified to define the integers.

The source and specification each have a SHA-256 digest in their verification report. The default module reproduction command rebuilds both and compares their bytes to the distributed certificate. Proof scope and effectiveness are also machine-readable in data/results.json.

## Verification boundary

Exact coefficient data and passing finite checks establish the algebraic specifications and the stated finite assertions. The projection theorems additionally use the arithmetic hypotheses identified in the papers. The complete commands, expected behavior, and source-preservation conventions are given in the [reproducibility guide](reproducibility.md).
