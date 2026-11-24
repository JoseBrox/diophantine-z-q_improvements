# Scope of the nine-coefficient contact construction

This is a restricted obstruction, not a lower bound for quartic witnesses or for nonlinear recharting.

The shared denominator construction keeps the square/fourth-power progression unchanged and requires each contact denominator to be an affine linear expression, with rational constant coefficients, in common helper functions and the retained progression functions. Within this class, **nine new helper functions are necessary** once nine distinct contact indices are used.

To see this, restrict the general progression to the exact parametrization

```math
u(j)=(s+j d)^2,\qquad f(j)=(s+j d)^4.
```

Every retained progression function has polynomial degree at most four in `(s,d)`. For fixed constants with `C!=0`, the new denominator is

```math
P_j=C(s+jd)^8+B(s+jd)^6+E(s+jd)^4+D(s+jd)^2+F.
```

Take any nine distinct rational indices `j_1,...,j_9`. If a rational constant linear combination of their denominators has degree at most four, its homogeneous degree-eight component gives

```math
\sum_{i=1}^9 c_i(s+j_i d)^8=0.
```

Equating the coefficients of `s^(8-h)d^h`, for `0<=h<=8`, gives a Vandermonde system with entries `binom(8,h)*j_i^h`. Its determinant is the nonzero product of the binomial coefficients and the pairwise index differences. Hence all `c_i` vanish. The nine denominators are linearly independent modulo the vector space of polynomials of degree at most four.

If all nine were affine combinations of only `r` additional common functions plus retained functions, their images in that quotient would span dimension at most `r`. Therefore `r>=9`. This argument even permits arbitrary rational common helper functions; it only restricts how their values enter the denominators. The specified chart contains the specialization `kappa=1` of the same abstract progression, so its local progression algebra has the same obstruction.

This does **not** exclude exploiting additional equations of the full source, a denominator-dependent change of inverse weights, recharting the progression, parameter-dependent coefficient combinations, changing the contact rational function, or a new arithmetic witness construction. In particular, a normalization using the nonzero physical spacing would require a separate proof of nonvanishing from the full point chart and an occurrence audit of every affected gate and inverse row. The local progression equations alone allow zero spacing, so it cannot be divided out in an exact local equivalence without further justification.
