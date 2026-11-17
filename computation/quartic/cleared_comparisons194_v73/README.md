# A quartic in 194 rational coordinates

This package specifies two quartic families with the same rational zero set. Each has **194 total coordinates, including the input**, and is the sum of **168 primitive integral quadratic squares**. The fixed coefficient parameter is `C = 149^N`, with `N >= 1`. Under the retained arithmetic premises and the cleared-comparison transfer theorem, every sufficiently large fixed `N` defines the integers in the rationals. A sufficient numerical value of `N` is not known.

## Exact polynomial data

| Presentation | Coordinate monomials | Parameter-separated terms | Exact coefficient height | Coefficient crossover |
|---|---:|---:|---|---:|
| Primitive reference basis | 2,765 | 2,772 | `max(K, 128*C^4)` | `N = 4` |
| Fewer-monomial reference basis | 2,621 | 2,628 | `max(L, 128*C^4)` | `N = 7` |

The constants are

```text
K = 126616122944180358034867798936
L = 484991541504995159662206970923766531374664106904986910720
```

Both polynomials have degree exactly four and integer content one. Every coordinate occurs. The coefficient of the fourth power of the input is one. The crossover values concern coefficient heights; they are not sufficient defining thresholds. The primitive reference basis has the smaller coefficient height for `1 <= N <= 6`. Both heights equal `128*C^4` for `N >= 7`.

The full equations and expanded quartics are in:

- `primitive/quadratic-family.json` and `primitive/polynomial-family.json`;
- `fewer_monomials/quadratic-family.json` and `fewer_monomials/polynomial-family.json`.

A polynomial term with fields `parameterPower`, `monomial`, and `coefficient` represents the integer coefficient times that power of `C` times the listed coordinate variables. Repeated coordinate indices denote powers. An empty coordinate list denotes a constant. The parameter is fixed, not existentially quantified.

## Construction

The field is `K = Q(sqrt(2))`, with `D = 11 - 6*sqrt(2)`, and the elliptic curve is `y^2 = x^3 - D*x`. The reference point chart and scalar inverse Vieta chart are retained. Three further numerator pairs use translated secants with six field coordinates each. Their reciprocal abscissas are stored directly, and their finite differences have quadratic abscissa outputs.

The comparison coordinates store cleared expressions. If `S = y(H)/x(H)` and `T_H = y(H-P_0)/x(H-P_0)`, the four cross comparisons are

```math
E_i=S\overline{t_i}-\overline{T_H}s_i.
```

The input coordinate stores `N = S - beta*s_1`, where `beta = 51*X^2 + 2504`. The scalar primary ratio `A = L_2` is retained. The homogeneous Lucas circuit uses

```math
\begin{aligned}
\mathcal C&=(A-1)(s_4+4S),\\
\mathcal P s_3&=2Ss_4,\\
\mathcal Q&=(A+1)\mathcal P,\\
\mathcal H&=\mathcal P^2+\mathcal C^2-\mathcal C\mathcal Q-s_4^2.
\end{aligned}
```

At a consumed contact prime, reciprocal positivity makes the relevant inverse ordinates nonzero. Consequently `L_1 = S/s_1`, `L_3 = P/s_4`, and `L_4 = 1 + 4*S/s_4` are recovered locally. The exact identity is

```math
\mathcal H=s_4^2G(A,\mathcal P/s_4,1+4S/s_4).
```

The arithmetic proof does not divide by these coordinates on arbitrary rational fibers. Zero-ordinate and finite two-torsion branches are handled through the absence of consumed contact primes and the retained height argument.

The detector factors use the stored squares of `E_2`, `E_3`, `E_4`, and `H` with contact exponents one or three. These exponents suffice because clearing the formal-parameter denominators increases the recovered comparison depth. The special input term is `q^4*N^8`. The exact ten-factor allocation is recorded in `laurent-certificate.json` and in the arithmetic theorem.

## Coordinate census

Each field coordinate contributes two rational coordinates.

| Part | Rational coordinates |
|---|---:|
| Input, rational normalizers, contact arguments and pole coordinates | 44 |
| Contact units | 8 |
| Reference chart and reference outputs | 10 |
| Three translated numerator pairs | 36 |
| Scalar inverse Vieta point coordinates | 14 |
| Nonreference reciprocal-square outputs | 8 |
| Scalar primary ratio and scalar quotient | 4 |
| Four cleared cross comparisons and their squares | 16 |
| Fourth power of the first cleared cross comparison | 2 |
| Cleared input and its square and fourth power | 6 |
| Homogeneous Lucas circuit and its square | 10 |
| Factor evaluations and partial products | 36 |
| **Total** | **194** |

`coordinate-names.json` identifies every final coordinate and its storage slot before the monomial change. `transformation.json` in each presentation gives the complete renumbering and all coordinate and equation multipliers.

## Units and rational equivalence

Write `u` for the first physical contact weight and `v` for the ratio of the second physical weight to the first. Thus the physical weights are `u` and `u*v`. The eight stored units are

```math
u,\ u^{-1},\ v,\ v^{-1},\ u^{-1}v^{-2},\ v^{-3},\ uv^{-1},\ u^{-1}v^{-1}.
```

Six literal quadratic equations force their values and their nonvanishing. In the source numbering they are

```text
x77*x78 = 1
x90*x91 = 1
x77*x92 = x91^2
x90*x901 = x91^2
x902 = x77*x91
x903 = x78*x91
```

The input is unchanged. Every other storage coordinate is multiplied by a specified integer power of `u` and `v`; every equation is divided by a specified unit monomial. These operations are invertible on every rational zero of the compiled system because the six unit equations are retained literally. No new boundary component is admitted by clearing a Laurent denominator.

The two reference presentations are related by an invertible constant change of eight equations. Their common Laurent equation multiplier is `u^2*v^2`. They therefore define the same rational zero set after compilation as well as before it.

## Verification

The construction and support and height checks require only the Python standard library. The independent full equation checker uses SymPy 1.14.0. No SMT solver is needed to verify the stored certificate.

The [complete arithmetic and algebraic proof](../../../papers/quartic/quartic194_20261117_v73.tex) states the retained premises and the defining theorem.

Run from this directory:

```sh
python build.py
python verify_height.py
python check_arithmetic.py
python check_support.py --output support-certificate.json
python check.py --folder primitive --primitive-reference --output primitive/independent-verification.json
python check.py --folder fewer_monomials --output fewer_monomials/independent-verification.json
```

The independent checker reconstructs all 81 new physical component equations and all 81 retained source equations, checks every monomial pullback and primitive normalization, verifies the six unit guards, and expands the 168 squares independently. It also checks that all 194 coordinates occur and that every stated coefficient profile is nonzero for every `C = 149^N`, `N >= 1`.

The only coefficient polynomial with coefficients of different signs is `289*(C^2 - 2)`. The height checks evaluate the finitely many values below the stated crossover and prove the remaining inequalities by exact binomial expansion at the crossover value. These finite certificates establish the algebraic assertions. The defining property additionally uses the arithmetic transfer theorem and its explicitly retained global premises.

## Source bindings

The pinned 195-coordinate source is `source/source195.json`, with SHA-256

```text
304f94843c1a4ac94fcd5f1295fee8b532e7f0424e638314d892c556e2fbfdf9
```

The primitive 194-coordinate quadratic table has SHA-256

```text
2e7c015103156772fbeccbed38aa1f5ec0ab9b9751b18ba0c7a81dca1bb9fdde
```

Its expanded quartic table has SHA-256

```text
3556a4c71694bdc574a1eb6793d8a2a8ab8f5bd333ede9e9328eb143bde5b69b
```

`manifest.json` records the package file hashes. The retained source files and exact constant reference-row map are included for reproducibility.
