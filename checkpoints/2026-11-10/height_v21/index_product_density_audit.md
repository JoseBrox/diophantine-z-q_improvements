# Independent audit: products of indices and finite correspondences

Audit target: `checkpoints/few_variables_v21/index_products_and_finite_correspondences.tex`.

**Result: PASS.** The density theorem, the affine-hyperplane criterion, the polynomial-index corollary, and the finite-correspondence consequence are correct with the hypotheses stated in the draft. They yield an obstruction to the specified reconstruction strategy, not a bound on the number of variables in arbitrary Diophantine definitions.

## Elementary elliptic proof

Let E be an elliptic curve and P a nontorsion point. Suppose a proper closed subset of E^3 contains (nP,hP,nhP) for infinitely many n and infinitely many h for each such n. Choose an ample line bundle L of degree d on E. A positive power of L boxproduct L boxproduct L has a nonzero section whose effective divisor D contains this closed subset.

Only finitely many fibers over the first E-factor are contained in D: each such fiber is itself an irreducible divisor and therefore an irreducible component of D. For every remaining n, the restriction D_n is an effective divisor on E^2 of numerical class N(L boxproduct L), for a fixed N. Infinitely many h imply that D_n contains the entire graph G_n of multiplication by n, since an infinite subset of the curve E is dense. With H=L boxproduct L, one has H^2=2d^2 and H.G_n=d(1+n^2). Effectivity of D_n-G_n gives 1+n^2 <= 2Nd, impossible for infinitely many integers n. The proof handles negative n and ignores only finitely many n; no Mordell--Lang input is needed here.

## General abelian proof

Let A have positive dimension and let Gamma=ZP be geometrically Zariski dense. Identify Gamma^r with Z^r. Mordell--Lang expresses V intersection Gamma^r, for any proper closed V, as a finite union of subgroup cosets. None of these subgroups can have rank r: a full-rank subgroup contains m Gamma^r for some nonzero m, whose closure is A^r because multiplication by m is surjective. Every remaining subgroup is annihilated by a nonzero integer linear form. Thus the associated indices lie in finitely many proper rational affine hyperplanes.

Conversely, a hyperplane sum a_i m_i=c gives the closed relation sum [a_i]Q_i=[c]P. This is proper since at least one a_i is nonzero and the homomorphism to A is surjective. A finite union remains proper since A^r is irreducible. This proves the exact criterion in the draft, including r=1.

For indices (n,h,nh), each hyperplane becomes (b+cn)h+an=d. Except at at most one value of n, it permits at most one h. A finite union cannot contain an infinite h-fiber for each of infinitely many n. The polynomial-index corollary follows by taking the product of finitely many nonzero polynomial pullbacks of affine linear forms; a nonzero polynomial cannot vanish on all of Z^s. For one variable it has only finitely many roots, which proves the arbitrary-infinite-subset assertion.

## Finite-correspondence scope and domains

A constructible relation in A^3 with finite geometric fibers over a nonempty open subset U of A^2 has proper closure. Each component dominating the base has dimension at most 2 dim A. Any nondominating component lies over a proper closed subset of the base, so its image closure is also proper regardless of exceptional fiber dimensions. There are finitely many components. A finite union of such relations still has proper closure.

If S is the dense set of product triples, then S intersect pr^{-1}(U) is dense in the nonempty open set pr^{-1}(U), and hence dense in A^3. Consequently no such relation can recover the product point on all the prescribed pairs within U. Rational output formulas are handled by restricting their source to their domains; finite algebraic auxiliary choices produce finite geometric output sets, so the same dimension argument applies. This does not assert recovery on branches on which the formulas are undefined.

The conclusion does not cover an extra independent free parameter, merely finite rational fibers when geometric fibers have positive dimension, a correspondence allowed to change with n, or a redesign whose completeness uses only specially chosen finitely many h for each n. The existing draft states the relevant limits correctly. In particular there is no new lower bound on Diophantine variable counts.

## Reference checks

The author manuscript of Ghioca--Hu--Scanlon--Zannier, https://math.berkeley.edu/~scanlon/papers/Ga_abelian.pdf, introduction lines 10--12 in the retrieved PDF explicitly states the required finitely generated Mordell--Lang theorem for abelian varieties over algebraically closed fields of characteristic zero. The primary Faltings chapter is *The general case of S. Lang's conjecture*, Barsotti Symposium in Algebraic Geometry, Perspectives in Mathematics 15 (1994), 175--182; publisher DOI https://doi.org/10.1016/B978-0-12-197270-7.50012-7.

The additive-group variants in the Ghioca--Hu--Scanlon--Zannier paper are not needed. Its Theorem 1.5 is unconditional for an extension of an elliptic curve by one additive group. Its Theorem 1.4 for an arbitrary higher-dimensional abelian variety assumes Bombieri--Lang. No use of the stronger conditional statement is implicit in this audit or the draft.

Checked by an independent mathematical proof; no numerical tests are used to certify these density assertions.
