# Reconstructed checkpoint: rational Pell solutions with an integral shifted trace

**Status: newly reconstructed and proved, not recovered from the previous
conversation. No integer predicate is removed, and no undecidability
variable count is changed.** The available git history contains the v102
denominator obstruction, but the original later classification checkpoint
has not been located.

Let `a` be an integer, `Delta=a^2-1`, `D=4a-5`, and suppose

```math
d^2-\Delta c^2=1,\qquad T=d-(a-2)c\in\mathbb Z,
\qquad c,d\in\mathbb Q.
```

The complete proof is in [pell_classification.pdf](pell_classification.pdf)
and its [TeX source](pell_classification.tex).

## Positive parameters: exactly two orbits

For `a>=2`, put

```math
\epsilon=a+\sqrt\Delta,\qquad
\rho=\frac{2a^2-4a+3+2(a-2)\sqrt\Delta}{4a-5}.
```

Every solution is exactly of the form

```math
d+c\sqrt\Delta=\pm\epsilon^n
\quad\hbox{or}\quad
d+c\sqrt\Delta=\pm\rho\epsilon^n,
\qquad n\in\mathbb Z.
```

At `a=2`, `rho=1` and the two descriptions coincide. For `a>=3`
the first orbit is integral and the second has the exact reduced
denominator

```math
\operatorname{den}(c)=\frac{4a-5}{\gcd(4a-5,3)}.
```

This strengthens the v102 statement that the denominator merely divides
`4a-5`. Multiplication by either `epsilon` or its inverse preserves the
integrality of `T` and the exact denominator of `c`.

## Negative parameters: a different finite seed classification

For `a=-A<=-2`, put `K=4A+5` and `epsilon=A+sqrt(A^2-1)`.
All solutions are signed integer powers of `epsilon` times the following
finite, distinct seeds. For every integer `t` between `1` and `2A+1`
for which `v^2=(A^2-1)t^2+K` is an integer square, take its positive root
`v` and put

```math
c_0=\frac{(A+2)t-v}{K},\qquad
d_0=\frac{(A+2)v-(A^2-1)t}{K}.
```

Each seed has `0<=c_0<1`, and its exact denominator persists along its
orbit. There can be more than two orbits: `a=-5` has the three seeds
`(c_0,d_0)=(0,1),(3/25,29/25),(2/5,11/5)`.
The signed current source therefore cannot be treated using only the
positive-parameter two-orbit theorem.

## The precise obstruction and the zero edge case

The rational reflection

```math
c^\#=\frac{2(a-2)T}{D}-c,\qquad
d^\#=\frac{2\Delta T}{D}-d
```

preserves both the norm and the **same value of `T`**. For `a>=3` it
interchanges the integral and nonintegral orbits. Consequently the first
linear source equation `T=bw+D*gamma` cannot distinguish those branches.
The v102 counterfamily already shows that the subsequent norm subsystem
also permits nonintegral examples; it does not satisfy the full source.

One preliminary circularity can nevertheless be removed. At `a=0`, the
norm and integral shifted trace force
`c` to lie in `{0,+/-1,+/-3/5,+/-4/5}`. Hence the small-Pell margin
`|c|<1/2` forces `c=0` even without a c-integrality predicate. This
repairs that step of the existing `s!=0` argument, but does not exclude
the nonintegral orbits at `|a|>=2`.

The remaining problem is to combine the full small-Pell equation,
closeness inequality, large source parameters, and the third norm to
exclude every nonintegral orbit. No such exclusion is claimed here.

## Exact verification

Run from the repository root:

```sh
python -B undecidability/pell_classification_reconstructed_v105/verify_classification.py
```

The independent script enumerates the rational fundamental-interval
solutions for a finite range of both parameter signs, checks them against
the seed formulas, tests forward and inverse orbit recovery and exact
denominator invariance, checks the reflection identities, and verifies
the zero-parameter edge case. The quantified theorem is proved in the
manuscript. `--write-certificate` explicitly refreshes the deterministic
receipt.
