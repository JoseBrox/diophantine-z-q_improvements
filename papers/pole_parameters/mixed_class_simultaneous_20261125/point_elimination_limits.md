# Point-elimination limits for the retained comparison geometry

The purpose of this note is to distinguish three precise failed
elimination mechanisms from an unrestricted lower bound. None of the
results below rules out new contact maps, a different witness order,
or extra arithmetic constraints.

## 1. Fixed-word merging of growth numerators, even without exact multiplication

Use the four fixed square-abscissa roots \(Q_1,Q_2,Q_3,Q_4\)
with integer labels \(n,a,t,b\) relative to P. At the growth
contacts of the [22-variable selective source](selective.md),
the reference H and all three growth numerator points \(U_2,U_3,U_4\)
are formal at a primary place; \(H-P\) and
\(U_i-Q_i\) are formal at the conjugate place.
The integer Lucas equation is
\[
 t^2-a(a-2)tb+(a-2)^2b^2=1,
 \qquad b\ne0,\quad c=|a-1|.
\]
Keep the source's integral-label growth conclusion
\(\log |t|>|a|-3\) for large \(|a|\).

Call a collection of prepared witnesses *cofinal for fixed roots*
if it supplies selected growth primes beyond every given bound,
with these same roots and the indicated two-slot formality.
This is the strength of the original ordered prime-selection
construction: first fix the roots and their scales, then take
arbitrarily large selected primes. It does not assert that
cofinality is logically necessary for every conceivable definition.

**Proposition.** A fixed nontrivial word relation
\[
 [r]U_2+[k]U_3+[\ell]U_4+[m]H=D_0
\]
where \(r,k,\ell,m\) are fixed integers,
\((r,k,\ell)\ne(0,0,0)\), and \(D_0\) is a point fixed once
the four roots have been fixed, cannot preserve such cofinal
completeness for arbitrarily large c. This also holds for a
fixed finite menu of words, even if D0 is an arbitrary
fixed-root-dependent point rather than a fixed linear word in
the roots.

Proof. The primary formality implies D0 is formal at every
selected primary place. A fixed nonidentity point of E(K) is
formal at only finitely many good places, by the denominators
of its abscissa; hence D0=O for a cofinal family. At the opposite
place, the same group-word relation, with each point replaced
by its formal difference, implies the fixed point
\[
 [r]Q_2+[k]Q_3+[\ell]Q_4+[m]P-D_0
\]
is formal. Therefore it is O. Since P is nontorsion,
\[
                       ra+kt+\ell b+m=0. \tag{1}
\]
This does not assume \(U_i=[h]Q_i\) globally. Only their reductions
at the two places were used.

If k is nonzero, substitute
\(kt=-ra-\ell b-m\) in the Lucas equation and multiply by k^2.
The leading coefficient in b is
\[
 \ell^2+k\ell a(a-2)+k^2(a-2)^2.
\]
It is a nonzero polynomial in a: its quadratic coefficient is
\(k(\ell+k)\), and if \(\ell=-k\) it is \(k^2(5-2a)\).
Exclude its finitely many integer roots. All coefficients of
the resulting polynomial in b are polynomials of bounded
degree in a with fixed integer coefficients. Its nonzero
leading coefficient has absolute value at least one, so
Cauchy's root bound gives \(|b|\le C(1+|a|)^d\) with
fixed C,d, and (1) gives the same kind of bound for t.
This contradicts the exponential Lucas growth for large |a|.
If k=0 and ell is nonzero, (1) bounds b linearly and the
monic Lucas quadratic in t bounds t polynomially.
If both are zero, r is nonzero and a is fixed.
For finitely many words, choose one common finite cutoff;
a cofinal family using a finite menu has one cofinal subfamily.
This proves the assertion.

In particular literal identification of two growth numerators
is not compatible with the unchanged cofinal growth preparation.
Separating the three comparisons across disjoint contact lists
would remove this obstruction, but would no longer give
\(M_{j,G}^3\mid\Delta c\) via the simultaneous polynomial
evaluation. A new joint residual transfer would be required.
The earlier input/Lucas sharing succeeds precisely because the
input relation and Lucas residual are two separate vanishing
problems. Unlike that operation, splitting the terms of the
Lucas polynomial is not a valid use of independent contact
families.

This strengthens the fixed-word obstruction of
[point_role_restrictions_20261117_v66.tex](../../../negative_results/papers/integer_labels/point_role_restrictions_20261117_v66.tex)
in its cofinal fixed-root setting by dropping the exact
global-multiplication hypothesis; it does not generalize that
paper's claims about all root-dependent witness families.

## 2. Bounded-degree point recovery in the ordinary and weak abc routes

The current [ordinary-abc](../../conditional_few_variables/six_test_sum_20261125/final.md)
and [weak-abc](../../conditional_few_variables/six_test_sum_20261125/weak.md)
eleven-variable systems have one input root A=[n]P and two
auxiliary points H,U. At the selected comparison prime H,U
are formal at the primary place and H-P,U-A at the opposite
place. The original height scalar uses the fixed input root A;
this permits cofinal prime selection after fixing A.

Here is a limitation on attempting to reconstruct U by finite
algebraic choices from H and the already fixed input and root A.
It allows arbitrary algebraic correspondences, not only fixed
group words.

**Proposition.** Suppose that, for each fixed canonical integer
input X and its fixed A=[n]P, the permissible pairs (H,U)
lie on a finite union of curves in \(E_K\times E_K\).
Assume a uniform integer upper bound D on the degrees of the
two projections on every geometrically irreducible curve
component on which the projection is nonconstant. Then for
\(|n|>D\) there is no cofinal family of rational witnesses
with the original two-slot formality just described.
The curves may depend on the fixed input and A, and the
points H,U need not be exact multiplication witnesses.

Proof. A cofinal family would give infinitely many H because
each fixed nonidentity H is formal at only finitely many
places. One curve component admits such a cofinal subfamily.
Components not geometrically irreducible over K contribute
only finitely many K-points outside the common geometrically
irreducible components defined over K: conjugate distinct
components meet in a finite set. Discard those finite sets
and singular points, which cannot contribute cofinally.
Normalize the selected component to a smooth projective curve
C over K. Its projection f to E in the first coordinate is
nonconstant. Thus the genus is at least one by Riemann--Hurwitz.
If it is at least two, Faltings' theorem gives finitely many
K-points, a contradiction. Therefore C has genus one and,
since it has a K-point, may be made an elliptic curve over K.

After choosing an origin on C the projections are
\(H=f_0(Q)+H_0,\ U=g_0(Q)+U_0\), with \(f_0\) an isogeny,
\(g_0\) a homomorphism (possibly zero), and fixed
translations H0,U0. Let \(d=\deg f_0\ge1\), and let
\(f_0^\vee:E\to C\) be the dual isogeny. The composition
\(g_0 f_0^\vee\) is a K-endomorphism of E.
Since E has j-invariant 1728 and K is real, its K-endomorphism
ring is Z (the nonreal CM endomorphisms are not defined over
K). Thus this composition is multiplication by some integer k.
Composing with f0 and using \(f_0^\vee f_0=[d]\) yields
\[
                   [d]U=[k]H+C_0,\qquad
 C_0=[d]U_0-[k]H_0 .
\]
If g0 is nonzero, \(k^2=d\deg g_0\le D^2\); if it is zero,
k=0. Thus |k|<=D in either case. Cofinal primary formality
gives \(C_0=O\). Cofinal opposite formality then gives
\([d]A=[k]P\), since
\([d](U-A)-[k](H-P)=[k]P-[d]A\).
It follows that \(dn=k\), impossible if \(|n|>D\).
This proves the proposition.

The degree hypothesis holds for reconstruction from a fixed
bounded-degree algebraic relation in H and U with no other
moving ordinary coordinate, whenever its fixed-input fibers
are curves with bounded projection degrees. A rational map
from H is a special case. A rational formula in H and a free
slope which is identically E-valued on a product is also
independent of the free slope: a rational map from the generic
projective line to E is constant. But the result does **not**
cover equations with the slope that define only a proper
joint locus, rather than an identically E-valued reconstruction.
It also does not prohibit a completely different witness
construction where only finitely many selected primes are
available for each fixed root.

## 3. A distinct two-point mechanism and its missing global bound

There is a way to dispense with the input root in the *local*
integer-recognition stage, using two exact divisibilities and
a difference of ratios instead of the old equality of ratios.
This is a useful alternative target rather than a defining
polynomial.

For integer labels \(h,j\) with \(h(h-1)\ne0\), impose
\[
                         h\mid j,\qquad h-1\mid j-1 .
\]
They imply
\(h(h-1)\mid j-h\), because the two positive absolute
divisors are coprime. Therefore the integer
\[
 m=\frac{j-h}{h(h-1)}=
          \frac{j-1}{h-1}-\frac{j}{h}
\]
is defined. Conversely \(j=h+m h(h-1)\) satisfies both
divisibilities for every integer m.

Take \(H=[h]P,\ U=[j]P\), using the two fixed translated
points \(H-P,U-P\) rather than \(U-A\). At a selected prime
where H,U are formal in one slot and H-P,U-P in its conjugate,
the corresponding exact formal logarithm ratios are \(j/h\)
and \((j-1)/(h-1)\). Their difference is m. The same
formal-parameter approximations as in the parent sources
can compare it to X with arbitrarily prescribed finite
precision if the relevant formal depths are available.
The identity \(j=h+m h(h-1)\) also respects all the
annihilator congruences for these formality conditions:
\(h\equiv0\bmod u_p\) implies \(j\equiv0\bmod u_p\),
and \(h\equiv1\bmod v_p\) implies \(j\equiv1\bmod v_p\).
No input-root translation is needed. This contrasts with
trying to use a point identity for a variable multiplication
on a fixed elliptic curve.

However the exact divisibilities are not enough for global
soundness. Even granting them as exact integer relations,
fix a nonintegral rational X and any finite collection of
primes p at which X is integral, with finite precisions
\(k_p>0\). By the Chinese remainder theorem there are
arbitrarily large integers m with
\[
                     m\equiv X\bmod p^{k_p}
\]
at every such prime. Every one gives \(j=h+m h(h-1)\),
with both divisibilities and the desired local comparisons.
Thus **even exact double divisibility plus any finite
collection of local difference-of-ratio tests cannot alone
recognize rational integrality**. This is a counterexample
at the integer-index comparison level, not a claim about
rational solutions of an unspecified full pole polynomial.

In a possible new construction the simultaneous divisibility
tests would have to be realized by the existing pole
machinery with its full prime preparation. In addition
a global bound on \(\log(1+|m|)\), strong enough relative
to the comparison radical, or another nonlocal condition
is required. Bounding this index quotient through a
rational or algebraic reconstruction of U risks the
cofinal correspondence obstruction above. We have not
proved a two-point defining polynomial under ordinary or
weak abc. The eleven-variable records remain unchanged.
