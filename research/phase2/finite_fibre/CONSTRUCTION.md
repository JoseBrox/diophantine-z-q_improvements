# Explicit finite-algebra polynomial: design checkpoint

Status: **the exact 558-variable indexed-polynomial specification and the
43/44-variable finite-anchor and 45/46-variable semilocal specifications have
been generated and independently audited.** See `README.md` for the complete
comparison and `source_shared.tex` for the smaller-source conversion. This
includes the preferred 43/45-variable conic-parametrized packages, of ranks
at most `2^29`/`2^30` and smaller verified degree bounds. The previous source
variants are retained separately. This
design document details the general construction and its 558-variable
specialization. The complete coefficient DAG, all finite
ranges, and the determinant/coefficient/product recipe are in
`polynomial-558/polynomial-specification.json`. No matrix of dimension `2^508`
or expanded final monomial table is materialized. The small-algebra interpreter
executes the complete construction on eight adversarial examples and emits one
fully expanded example polynomial.

## Exact polynomial construction

Input consists of `b` external base coordinates, `m` formal algebra generators,
monic triangular equations defining a finite free algebra `A` of rank `n`, an
element `G` nonzero on the desired open subset, and elements `E_i` required to
vanish. Assume every geometric point where `G != 0` has local length one.
The formal algebra generators are eliminated by the following determinants;
they are **not** quantified coordinates of the output polynomial.

For each integer `ell` in `0..m*n*(n+1)/2`, set

```text
lambda_ell = 1 + sum_{i=1}^m ell^i z_i
M          = multiplication by G*lambda_ell in the monomial basis of A
H(V)       = det(I - V*M) = sum_{k=0}^n a_k V^k
R_i(V)     = Tr(M_{E_i} adj(I - V*M)).
```

The equality `a_0 = 1` holds identically. Zero-guard components, including
nilpotent components, contribute the constant factor one to `H`.

For every `d = 1..n`, define

```text
H_d(V) = sum_{k=0}^d a_k V^k
g      = a_d * Res_V(H_d, derivative_V H_d)
L      = a_d^2 * g
Psi(U) = 1 + sum_{j=1}^d a_{d-j} a_d^(2j-1) g^j U^j
Rtilde_i(U) = (L*U)^(n-1) R_i(1/(L*U))
Q_{ell,d} = Psi^2 + sum_{k=d+1}^n a_k^2 + sum_i Rtilde_i^2.
```

The notation for `Rtilde` means polynomial coefficient reversal, so it is
defined even at `L*U = 0`; no division is present in the resulting expression.
The resultant is the determinant of the specified Sylvester matrix with degree
bounds `d` and `d-1`. The polynomial for this finite-algebra branch is

```text
P(x,U) = product_{ell=0}^{m*n*(n+1)/2} product_{d=1}^n Q_{ell,d}(x,U).
```

All operations are finite integer polynomial operations. Thus this is an exact
indexed determinant/coefficient/product specification, even when expanding its
matrices, branch product, or monomials is infeasible. An interpreter can unroll
the specification in principle; the included small-dimension interpreter and
exact tests execute the complete construction on eight adversarial examples.

## Why it works

For fixed rational base coordinates, a matrix zero of `H(V)` with a nonzero
discriminant and `V != 0` gives a one-dimensional rational eigenspace of `M`.
Every multiplication matrix `M_{z_i}` commutes with `M`, so it acts on that
eigenspace by a rational scalar. These scalars satisfy all the algebra's
defining equations. The eigenvalue is `1/V`, which forces `G != 0`.

Writing `J = Tr(adj(I-V*M))`, the adjugate identity gives
`J = -V H'(V) != 0` at a simple root. Consequently
`R_i(V) = E_i(z) J`; the trace equations enforce precisely the desired closed
conditions, including all zero-radical branches.

Conversely, all guarded points are simple. For distinct guarded geometric
points `p,q`, the polynomial in `ell`

```text
G(p)*(1 + sum ell^i z_i(p)) - G(q)*(1 + sum ell^i z_i(q))
```

is nonzero and has degree at most `m`. The corresponding value at one guarded
point is also a nonzero polynomial in `ell`. Avoiding the at most
`m*n*(n+1)/2` bad integers makes all nonzero eigenvalues distinct and nonzero.
Then `H` is squarefree of some degree `d`, and the corresponding branch works.
The reciprocal `Psi` enforces the base-only leading-coefficient and resultant
guards without a second external witness. All exceptional degree drops are
explicitly covered by the finite degree cases; no unexecuted stratification
or generic-only primitive-element assertion is hidden in the construction.

## Implemented source specialization

Retain the same 557 base coordinates as in the phase-one finite-fiber proof:
422 point abscissa coordinates, 126 pole parameters, two anchor parameters,
and seven root parameters including the input.

There are 297 formal finite-algebra generators:

- 211 scaled point-chart roots `Y = 2C`, with monic quartics
  `Y^4 - 2K Y^2 + 2J^2`, where
  `K=(j^2+2)A+4jB`, `J=2jA+(j^2+2)B` and
  `a^3-Da=A+B sqrt(2)`.
- One completed Pell root `V=2*tau-a`, with `V^2-Delta=0`.
- 85 rescaled private quadratic roots: the anchor root and the 84 pole roots.

Every equation `L*y^2+M=0` for a private witness is covered by two fixed cases:

1. `z=0`, with the additional closed condition `M=0`;
2. `z^2+L*M=0`, with the guard `L*z != 0`, recovering `y=z/L`.

If `L=M=0`, the first case chooses the private witness zero and loses no
existential solutions. This includes the exceptional zero pole input.
The completed Pell equation has the same two cases with `L=1` and
`M=-Delta`, recovering `tau=(V+a)/2` in either case.

Thus there are 86 fixed zero/nonzero bits, with rank
`n = 4^211 * 2^popcount(mask) <= 2^508`. The old finite point chart has
212 choices and the height correction 256 choices. The guard is the original
guard product, times the point-quartic derivatives, times `L*z` in each
nonzero quadratic case. It forces the triangular algebra's Jacobian to be
nonzero. The point derivatives already follow from the source chart guards:
the discriminant of the quadratic in `Y^2` is
`4*(j^2-2)^2*(A^2-2B^2)`, and `Y != 0`.

Substitutions `C=Y/2` and `tau=(V+a)/2` are cleared using explicit powers of
two, producing integral coefficient DAGs. The final polynomial therefore
has exactly the 557 external base coordinates and one external witness `U`.

## Completed audit and bounds

The compact artifact includes the exact coefficient DAG, source hashes,
the base/generator map, extraction certificates for all private quadratics,
all finite parameter ranges, and the determinant/coefficient/product recipe.
Its independent checker validates the source conversion, monicity,
triangularity, all variable counts, simplicity guards, and exact uniform
degree/coefficient-norm bounds without attempting to expand gigantic matrices.
Small exact algebras test degree drops, nilpotents killed by the guard,
zero quadratic coefficients, bad separators, and trace reconstruction.

For bounds, use generator weights for a filtration respected by the monic
relations, and a submultiplicative column norm for multiplication matrices.
The resulting determinant and resultant bounds are explicit finite integers.
The convenient rounded bounds are degree at most `2^3122` and coefficient
height at most `2^(2^3127)`. They are upper bounds, not expansion statistics.
