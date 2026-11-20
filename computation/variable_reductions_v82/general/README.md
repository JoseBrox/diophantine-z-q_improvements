# Quartics in 163 and 179 total variables

This package is based on notes of **Gabe Conant with Astra 6.2**. It
contains the complete coefficient tables for the scalar-point reduction
proved in
`papers/quartic/scalar_point163_179_20261120_v82.tex`.

The defining assertions are conditional on the retained arithmetic
interfaces stated in that manuscript and in the v78 shared-product
audit. They are not consequences of a finite coefficient calculation
alone. In particular, the native pole realization and the quantified
prime-pattern/approximation inputs remain hypotheses of the transfer.

| Construction | Total variables | Quadratic rows | Monomials | Degree | Content |
|---|---:|---:|---:|---:|---:|
| General family | 163 | 137 | 2789 | 4 | 1 |
| Fully specified member | 179 | 151 | 3036 | 4 | 1 |

Coordinate one is the rational input. Each polynomial is the sum of
the squares of its listed residuals. The family uses $C=149^N$ and
defines the integers for every sufficiently large fixed $N$; the
sufficient threshold remains ineffective. Its exact coefficient height,
for every $N\ge1$, is

```math
\max\{126616122944180358034867798936,149^{4N+2}\}.
```

The fixed member uses $R=A_{\rm a}r/(1+25r)$, where

```math
A_0=645904574641049503754777843805872291231896003979.
```

The additional factor and normalizer are

```math
B_{\rm a}=263\cdot2161\cdot2437\cdot2837\cdot3793
         =14904184670611231,\qquad A_{\rm a}=A_0B_{\rm a}^4.
```

Its height is exactly $A_{\rm a}^2$, of 748 bits. This is a variable-count
improvement with a larger coefficient height than the preceding
180-variable member.

## What changes

For $K=\mathbb Q(\sqrt2)$ and the retained reference reciprocal
$f=1/x(H)$, the new scalar relations are

```math
J=\frac{Z^2}{R^5}+\frac{f^2}{R^4},\qquad
\tau\operatorname{Tr}(Z^2/R^5)=N(J),\qquad
b_s=R(R+9792)\tau^2.
```

They force $Z\ne0$ and a nonzero trace, and retain the common-slot
inequalities $v(Z)>9\mu/4$ and $v(f)>7\mu/4$ at every consumed
odd scalar contact. Scaling the scalar inverse-Vieta chart by $Z$
then gives the identity $M=-2S-W$, so its two rational $M$ components
can be removed. The general family weights only the scalar root by
$R$ in its aggregate, so its contribution is the stored $P^*=R x(Q_2)$
and no inverse of $R$ is needed. The fixed member adds one inverse
of $R$ and retains the effective unweighted aggregate. The square
register $R^2$ remains in both.

The general soundness proof uses the already proved positive weighted
trace theorem with fixed weights $(1,r,1,1)$ at $r=R$. Its constants
are uniform in $N$ and the input. The additional term satisfies

```math
h(R)\le4h(\beta)+(2N+1)\log149+\log1801500.
```

The scalar lower bound absorbs this term uniformly before $N$ is
chosen large. The weighted theorem has an ineffective additive
constant, so it is not used to claim a fixed 178-variable member.

The changed comparison is

```math
E_2^*=A\overline{(V+M)}+2\overline{T_H}\,\overline Z
      =-\overline{Zt_2}\,C_2.
```

Its factor uses the pair $c^5E_3^4-c^{11}(E_2^*)^4$. The local
conclusion is $M_j^3\mid a\Delta$. Since $|a\Delta|\le14B^5$,
the retained general height bound has exponent $35/18<2$ and still
proves soundness. The manuscript proves the complete ordered converse,
including every scalar denominator, the native zero-coordinate branches,
the original synchronized depth $d\ge1$, and the explicit endpoint
$|a|\ge2^{960}$.

## Files and exact maps

`source163.json` and `source179.json` are the complete physical Laurent
row definitions. A term lists its powers of $C,c,R$, its ordinary
source-labelled coordinate monomial, and its rational coefficient.
Source label 112 stores $R^2$. The fixed source has no parameter.

Each construction directory contains:

- `quadrics.json`: all ordinary quadratic residuals;
- `polynomial.json`: the complete expanded integer coefficient table;
- `maps.json`: the integer Laurent weights, row weights, coordinate
  permutation, and definitions of the six unit coordinates;
- `certificate.json`: the exact census and conditional theorem statement.

For an ordinary coordinate the map is
$x_i^{\rm source}=C^{k_i}c^{e_i}R^{r_i}x_i^{\rm stored}$, with
$C$ omitted in the fixed member. The guards are
$c c^{-1}=1$, $c^{-2}=(c^{-1})^2$, and $R_2=R^2$; the fixed member
also has $R R^{-1}=1$. In the general family the ordinary input
rows themselves force $R>0$ before any inverse map is used:
the rescaled register $\rho$ satisfies $\rho=r(X)>0$ and
$R(1+149^2\rho)=149C^2\rho$. Every map is invertible on every
rational solution. No point chart
is restricted to a generic fiber.

## Independent verification

From the repository root, run:

```sh
python -B computation/variable_reductions_v82/general/check.py
```

The checker uses Python 3 and SymPy. Its default invocation is read-only.
It imports no construction producer. It independently reconstructs every
retained physical row from the published enhanced v78 quadratic and
weight tables, directly reconstructs the new field equations, reverses
all compiled maps, and expands both sums of squares with SymPy. It also
checks the universal point/native/comparison identities, all 26,778
anchor residues, and the exact endpoint inequalities. The immutable
`independent.json` records the result and binds the source, tables,
manuscript, and checker hashes. `arithmetic.json` records the precise
arithmetic deductions; the manuscript supplies their proofs.

To reproduce the tables into a separate directory, run:

```sh
python -B computation/variable_reductions_v82/general/build.py --output /tmp/v82-general-reproduction
```

The producer uses only the Python standard library and the supplied
physical rows and weight maps. It needs no integer solver and does not
modify the source files. Its output matches the published tables exactly.
The historical dependencies used by the independent check are pinned
in the receipt and remain unmodified.
