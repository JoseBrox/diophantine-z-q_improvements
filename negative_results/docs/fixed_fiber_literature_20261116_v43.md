# Rational-point theorems for the fixed-input pole families

This audit concerns the direct common-parameter family

\[
q_i^2=D_i(s_i^2-C_i e_{D_i}(t))(s_i^2+3C_i e_{D_i}(t)),
\qquad e_D(t)=(t^2-D)/(t^2+3D),
\]

with distinct positive `D_i` and nonzero `C_i`. It does not exclude a
different fibration or an argument using the actual detector functions.
The statements below do not supply a common rational fiber from Schinzel
and finiteness of the Tate--Shafarevich groups alone.

## Relevant Jacobians

At a nonsingular rational fiber put `A=C_i e_(D_i)(t)` and `n=D_i A`,
so `n` is nonzero. The quartic is a two-isogeny homogeneous space with Jacobian

\[
J_n:Y^2=X^3-4nX^2+16n^2X.
\]

This has one nonzero rational two-torsion point, with two-division field
`Q(sqrt(-3))`. Its two-isogenous curve
`E_n:y^2=x(x-n)(x+3n)` has full rational two-torsion. Passing to `E_n`
does not lift points through the prescribed homogeneous space. The
input class `[D_i]` is locally soluble for prepared detector inputs and
then lies in the isogeny-Selmer group; its image in `Sha(J_n)[psi]` must
vanish. Finiteness of Sha alone does not make that element zero.

## Density on individual Kummer surfaces

Z. Huang, *Rational Points on Elliptic K3 Surfaces of Quadratic Twist
Type*, Quarterly Journal of Mathematics 72 (2021), 755--772,
doi:10.1093/qmath/haaa044. Primary preprint:
<https://arxiv.org/pdf/1806.07869>.

For squarefree cubic or quartic polynomials, Theorem 1.5 characterizes
Zariski density on the associated twisted Kummer surface by the
existence of one common quadratic twist on which both genus-one curves
have rational points and positive Jacobian rank. Rational points are
part of the hypothesis, including for quartic torsors. The theorem does
not obtain that common twist from local solubility. Corollary 3.5 gives
an unconditional result for cubic models with its stated restrictions
on the pair of j-invariants.

D. Gvirtz, *Mazur's conjecture and an unexpected rational curve on
Kummer surfaces and their superelliptic generalisations*, Acta
Arithmetica 187 (2019), 189--200, doi:10.4064/aa180201-1-10.
Primary accepted manuscript:
<https://eprints.gla.ac.uk/284302/1/284302.pdf>.

Theorem 1.1 uses the standard cubic Kummer model and its rational curve;
Theorem 5.1 assumes Zariski density to obtain the real-topology
conclusion. A rational origin on a quartic curve does not identify its
cover involution with standard negation. In our trivializing quartic
that involution has no rational fixed point for prepared `D`, whereas
negation fixes the origin. The extra torsor and involution data therefore
cannot be omitted when passing to cubic Jacobian models. Density on
individual surfaces would still not synchronize their parameter values.

## Skorobogatov--Swinnerton-Dyer (2005)

A. Skorobogatov and P. Swinnerton-Dyer, *2-Descent on elliptic curves and
rational points on certain Kummer surfaces*, Advances in Mathematics
198 (2005), 448--483.

Primary author PDF: <https://www.ma.imperial.ac.uk/~anskor/SSD_AM.pdf>.

The arithmetic theorem in Section 6 assumes full rational two-torsion on
the elliptic Jacobians. Our `J_n` fail that requirement. The preliminary
descent in Section 5 does not supply the missing arithmetic conclusion.
Also, the common-parameter threefold for two distinct `D_i` has Kodaira
dimension one by the accompanying proof, so it is not itself a Kummer
quotient of an abelian variety. Separate surface results do not
synchronize their parameter projections.


## Harpaz--Skorobogatov (2016)

Y. Harpaz and A. Skorobogatov, *Hasse principle for Kummer varieties*,
Algebra & Number Theory 10 (2016), 813--841.

Primary author PDF: <https://www.ma.imperial.ac.uk/~anskor/hsk.pdf>.

Theorem A assumes, among other conditions, that both quartic branch
polynomials are irreducible with Galois group `S4`, together with
independent discriminant primes. Our biquadratic branch polynomials
have Galois group contained in `V4`, and their relevant two-division
fields coincide. These are decisive failures of Theorem A. The
common-parameter threefold has the additional geometric mismatch above.


## One-rational-two-torsion pencil theorems

O. Wittenberg, *Intersections de deux quadriques et pinceaux de courbes de
genre 1*, Lecture Notes in Mathematics 1901, Springer, 2007.

Primary author preprint: <https://arxiv.org/pdf/1502.04462>.

Chapter 2, Section 2.2 (printed page 75), requires a semistable Jacobian
at every closed base point. The chapter introduction (printed page 74)
specifies that the earlier one-rational-two-torsion pencil results
covered types `I1` or `I2`, whereas this chapter allows arbitrary
semistable reduction. The earlier paper identified there is
J.-L. Colliot-Thélène, *Hasse principle for pencils of curves of genus
one whose Jacobians have a rational 2-division point*, Progress in
Mathematics 199 (2001), 117--161. These semistability hypotheses are
stated and compared in Wittenberg's Chapter 2.

Our exact invariant calculation gives

\[
c_4=-512n^2,\quad c_6=-14336n^3,\quad
\Delta=-196608n^6,\quad j=2048/3.
\]

At each `t^2=D_i,-3D_i`, a minimal integral model has
`v(c4)=2`, `v(Delta)=6`, hence additive `I0*` in residue characteristic
zero. It is not semistable. A rational base change cannot remove all
four odd twist branches: over an algebraic closure it would give a
nonconstant map from `P1` to their genus-one double cover. Removing two
distinct branch sets simultaneously gives the genus-five cover.


## Harpaz--Wittenberg (2016)

Y. Harpaz and O. Wittenberg, *On the fibration method for zero-cycles and
rational points*, Annals of Mathematics 183 (2016), 229--295,
doi:10.4007/annals.2016.183.1.5.

Primary publisher PDF:
<https://annals.math.princeton.edu/wp-content/uploads/annals-v183-n1-p05-p.pdf>.

Theorem 9.17 concerns a smooth proper variety over a number field with
a map to the projective line, geometrically irreducible generic fiber,
and a multiplicity-one irreducible component in every fiber. For a finite
subgroup `B` of the Brauer group over a suitable open subset, and under
the stated cases of its polynomial-value Conjecture 9.1 or 9.2, it
approximates appropriate adelic points by adelic points on rational
fibers orthogonal to `B`. Its conclusion is not a rational point.

Corollary 9.23 additionally requires
`H^1(X_geometric_generic,Q/Z)=0` and
`H^2(X_geometric_generic,O)=0`, and assumes that fibers over rational
points of a Hilbert subset satisfy the indicated Brauer--Manin weak
approximation property. In its proof these vanishings permit one finite
Brauer subgroup to control the full fiber Brauer groups on a Hilbert
subset. Corollary 9.25 assumes rationally connected geometric generic
fiber. These statements occur on printed pages 283--285.

Here the geometric generic fiber is a product of `r` genus-one curves.
Its first group is `(Q/Z)^(2r)`, and its second group has dimension
`r(r-1)/2`; for two poles both required vanishings fail. Even if finite
Sha supplies a Brauer--Manin criterion on each individual genus-one
fiber, Theorem 9.17 has not produced the required full orthogonality.
Taking its finite Brauer subgroup to be zero would merely return local
solubility, already known for every rational parameter in this problem.


## Remaining arithmetic target

A successful external conditional reduction needs control of the
simultaneously varying prescribed isogeny-Selmer classes, or a different
fibration whose full hypotheses can be checked. Independent positive
ranks, local points, and finite Sha are individually insufficient. The
actual detector functions and their independent-index families provide
extra structure which these general theorems have not used.
