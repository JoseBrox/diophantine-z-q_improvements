# Number-field research, version 13

## Scope and primary-source audit

No counterexample among finite number fields has been established. Large/ample-field undefinability theorems do not apply to number fields: a smooth genus at least two curve with a rational point has finitely many points over each number field by Faltings. Kwon, arXiv:2411.03212, Theorem 1.1, extends Fehm's theorem to finite unions of affine translates of proper subfields in perfect large fields. Mazur–Rubin–Shlapentokh, arXiv:2208.09963v3, Theorem 1.1 and section 14, is a theorem with integral witnesses; its approximate-logarithm construction is not an existential definition inside a number field.

## Elementary bounded-denominator bridge

Let K have degree n over Q. If a Diophantine S subset K satisfies Z subset S subset O_K, then O_K is Diophantine in K without any separate appeal to a definition of Z in O_K: for an integral basis omega_1,...,omega_n,

    O_K = omega_1 S + ... + omega_n S.

Both inclusions follow directly from the sandwich conditions. If S has a one-polynomial definition with N total coordinates and degree D, eliminating the last summand gives nN total coordinates, n equations, unchanged degree D.

More generally, suppose Z subset S and M S subset O_K for a positive rational integer M. Then T = union_{j=0}^{M-1}(j+M S) satisfies Z subset T subset O_K. If F(T,Y)=0 defines S with N total coordinates and degree D, the polynomial product over j of M^D F((T-j)/M,Y), with the same witness block Y, defines T. Thus T needs N total coordinates and degree at most MD; O_K needs nN total coordinates and n residuals of degree at most MD. The shared witness block is valid because a product over a field vanishes if and only if one factor vanishes; the other factors impose no requirement. This identifies uniformly bounded denominators as sufficient, but does not construct such an S.

## Ratios of differences of stable elliptic abscissas: next proved mechanism

Assume an elliptic curve E/Q has positive rank and rank E(K)=rank E(Q). Choose m annihilating E(K)/E(Q), a non-torsion R in E(Q), and c=x([m]R). For affine P,Q in E(K), put

    D = { (x([m]P)-c)/(x([m]Q)-c) : both images affine, denominator nonzero }.

Then D is Diophantine in K, is contained in Q, and has a six-total-coordinate definition (input, two affine elliptic points, one common inverse). Division polynomials give four residuals: two curve equations, the cleared ratio equation, and the common inverse equation. For m=1 these have degrees at most three; in general at most max(3,3m^2-1).

The density statement is proved simultaneously in any finite collection of completions of Q. A fixed non-torsion cyclic subgroup is dense in a product of suitable open p-adic subgroups and a real connected circle: reduce to congruences on the integer multiplier by CRT and apply irrational rotation for the real place. Near R, the function x([m]P)-c has nonzero derivative (since [m]R is not two-torsion). Its local image therefore contains a neighborhood of zero. Ratios of two such neighborhoods can approximate arbitrary local targets. Despite this density, Corvaja--Zannier's August 2026 Theorem 1.1 now proves that this rational-map image misses infinitely many rational integers. The precise proof and scope are in the polished paper.

## Explicit proper rational subset with four total coordinates

The general density proof is complete. More decisively, an explicit counterexample to global completeness of a locally dense elliptic ratio construction has been found.

Let E:y^2=x^3+9. Its quadratic twist by -1 is E^-:y^2=x^3-9, whose rational Mordell--Weil group is trivial. Therefore E(Q(i))=E(Q): for any P in E(Q(i)), P-conjugate(P) is anti-invariant, and a nonzero anti-invariant point gives an affine Q-point of E^-. The point (3,6) on E has infinite order, since its double is (-15/16,183/64), nonintegral.

Let X be the nonzero rational abscissas of E and D={0} union X/X. It is a proper subset of Q: if -1=x(P)/x(Q), the abscissas are a and -a with a nonzero. Their ordinate product gives (-a^2,y(P)y(Q)) on E':y^2=x^3+81. But E'(Q) consists exactly of O and (0,+/-9), forcing a=0.

The rank-zero calculations for E^- and E' were independently reproduced using cypari2 2.2.4 and PARI2.17.2. ellrank returns [0,0,0,[]] for both; ell2cover returns []; torsion orders are 1 and3 respectively. These are unconditional descent bounds, not BSD estimates. They agree with Cremona data records3888k1 and972b2. The verifier also independently counts reductions at5 and7 and expands the polynomial below.

In the projective chart X!=0 on E, put u=Y/X,w=Z/X. Then u^2*w-9*w^3-1=0, forcing w!=0. Eliminating the second chart coordinate w2=t*w gives

    F=u^2*w-9*w^3-1,
    G=v^2*t*w-9*t^3*w^3-1,
    P=t*(F^2-2*G^2).

Because2 is nonsquare in Q(i), P existentially defines exactly D there. It has FOUR total coordinates (t,w,u,v), degree13, height162, and11 monomials. This is a rationality-restricting set, NOT a definition of Z, Q, or Z[i].

D is dense simultaneously in every finite product of Q-completions. This follows by translating a non-torsion cyclic subgroup toward the rational torsion point (0,3), using CRT and irrational rotation, and applying the local inverse theorem to x near this point. Moreover P(t,...) is soluble for EVERY input t in EVERY completion of Q(i): choose a sufficiently small nonzero local s so both9+s^3 and9+t^3*s^3 are squares. Thus even all local solubility tests together cannot detect its excluded global value-1.

For any fixed rational t other than0,1 the associated biquadratic curve y^2=s^3+9,z^2=t^3*s^3+9 has genus4 (seven branch points, each inertia2). Hence its rational witnesses are finite by Faltings. No rational-function section can supply witnesses as functions of a variable t, since every point of an elliptic curve over k(t) is constant.

Complete polished proof: elliptic_ratios_and_integrality_20261109_v13.tex, successfully compiled twice to an eleven-page PDF using the shared tex_environment helper. Exact reproducible code and PASS result: check_elliptic_ratio_obstruction.py and elliptic-ratio-certificate.json. A local cypari2 wheel and dependency directory were used only for execution and should NOT be committed as research artifacts.

The paper and certificate now also include the identical polynomial over the eight quadratic fields Q(sqrt(d)), d in {-15,-13,-11,-10,-1,3,5,7}. For all eight, unconditional PARI bounds show that y^2=x^3+9d^3 has rank zero and torsion order one. The anti-invariant-point argument gives exact equality E(Q(sqrt(d)))=E(Q). Since none of these fields contains sqrt(2), the same polynomial defines precisely the same proper rational subset D. Real and imaginary quadratic fields therefore both admit this small rationality restriction; neither case resolves completeness or the ring-of-integers question.

## Final rational-map obstruction and degree-eleven consequence

Primary source independently retrieved and checked:
P. Corvaja and U. Zannier, with appendix by D. Masser,
*Rational and integral values of rational functions at rational points*,
arXiv:2608.28255v1, 28 August 2026,
https://arxiv.org/html/2608.28255v1, Theorem 1.1.
For finitely many semiabelian varieties, rational maps, and finitely
generated point subgroups, the union of the value sets misses infinitely
many rational integers. The abelian specialization is unconditional;
its proof uses Mordell--Lang, not the separate Vojta-conjectural height
claims in Section 3.

The polished paper now includes the precise cited theorem and complete
proof of our consequence: every fixed finite rational combination of
finitely many points on fixed abelian varieties is contained in a
rational-map image on their product. Mordell--Weil makes the product's
rational points finitely generated. Finite unions and added finite
sets still miss infinitely many rational integers. Additional point
restrictions cannot enlarge these images. This rules out making a set
containing every integer by finite sums/products/ratios of the stable
elliptic coordinate sets.

The four-coordinate degree-eleven slope condition is now proved to
fail integer completeness. For every nonzero input, its chart forces
two rational points with nonzero abscissas and nonzero second ordinate,
so the input is a defined rational slope ratio on E×E. The leading
factor adds only input zero. Both the main abscissa construction and
this slope construction are therefore covered, including their
degenerate strata. The exact expansion and bounded search are in
check_rationality_filters.py and rationality-filter-certificate.json.
The particular missing status of slope inputs 2 and 3 is still not
proved by the bounded search and is not claimed.

The obstruction does not cover arbitrary algebraic correspondences or
unrestricted affine witnesses whose outputs are not fixed rational
functions of the abelian points. It is not a counterexample to general
Diophantine definability of a ring of integers in a number field.
Three precise next questions and source scopes are recorded in
next_priorities.md (under 700 words).
