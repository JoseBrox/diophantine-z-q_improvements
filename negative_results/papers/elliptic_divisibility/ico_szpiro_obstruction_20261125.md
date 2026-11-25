# A generalized-Szpiro obstruction to all boundary-controlled ico lifts

## Statement

The earlier [multiplication-boundary obstruction](ico_multiplication_boundary_20261125.md) treats rational-function choices of the lift. This note gives a substantially different obstruction, applying to **arbitrary arithmetic choices of the ico point**, even with just one reference per integer.

Let \(q=\widehat h(P)>0\) and \(H=[h]P,\ U=[mh]P\) in the existing rational cyclic chart, with \(h,m\ne0\). Let \(Z=Z(g_U,t)\) be a guarded ico lift, where \(g_U^2=x(U)\), and let \(B(Z)\) be the product of primes of coordinate-point reduction.

The following implication holds:

> If for unbounded integer multipliers \(m\) there is even one reference
> and one guarded lift satisfying
> \[
>                 \log B(Z)\le C_0 qh^2+C_1                 \tag{1}
> \]
> with fixed constants \(C_0,C_1\), then the uniform generalized
> Szpiro conjecture for abelian surfaces over number fields of bounded
> degree is false.

This does not assume a formula for \(t\), a bound on \(t\)'s rational-function degree, an infinite set of references at any one input, or preparation of a BB pole. It therefore applies to the completeness target before any of those further requirements are imposed.

The implication uses an additional conjecture for a **conditional impossibility** conclusion. Ordinary rational abc is not known to imply the generalized Szpiro bound used here. We do not prove an unconditional impossibility result for the ico lift.

We also prove, under ordinary rational abc alone and the cited moduli identifications, a necessary large-prime-mass condition on the *decomposable good reductions* of the lifted surface (Section 3). These are not the same as its bad abelian reduction primes.

## 1. Bounded-degree arithmetic realization of the actual ico point

Use the ico surface and boundary of the preceding [interpolation paper](../../../papers/elliptic_divisibility/ico_boundary_interpolation_20261125/README.md). If \(Z\) is a nonboundary rational point, a primitive integral vector representing it defines an integral point of the open moduli model over
\[
                        R=\mathbb Z[1/(30B(Z))].
\]
Indeed, outside \(30B(Z)\) its reduction misses all five coordinate points. This is exactly the integral model of von Kanel--Kret, *Integral points on coarse Hilbert moduli schemes*, [arXiv:2307.06944v1](https://arxiv.org/pdf/2307.06944), Proposition 11.5, Theorem 11.3 and its proof. It parametrizes abelian surfaces with real multiplication by the integers of \(\mathbb Q(\sqrt5)\), the prescribed polarization datum and principal level-two structure. Its coarse branch locus is empty over the specified base.

For the argument it suffices to choose a fixed finite etale level cover of this open moduli scheme, after inverting a further fixed finite set of primes if necessary, on which the universal abelian scheme exists. The construction is precisely the finite-etale-cover step in the proof of Fan--von Kanel, *Rational points and rational moduli spaces*, [arXiv:2501.17155v2](https://arxiv.org/html/2501.17155v2), Proposition 5.2. Pulling back this fixed cover along the actual integral point \(Z\) gives a nonempty finite etale algebra over \(R\) with the further fixed primes inverted. Any connected factor is the integral closure of that ring in its fraction field \(L\). Consequently there are a fixed degree bound \(d_*\) and a fixed positive integer \(M_*\) such that the actual abelian surface \(A_Z/L\) satisfies:

* \([L:\mathbb Q]\le d_*\);
* \(L/\mathbb Q\) is unramified outside \(M_*B(Z)\);
* \(A_Z\) has good reduction outside the primes above \(M_*B(Z)\).

For example the principal level-three cover in the cited proof gives the bounded-degree fields used there (their bound \(3^{4g}\) with \(g=2\)); the argument here does not require a numerical degree bound. We use a **single bounded-degree field factor for each point**, not the degree of the compositum of all such fields.

Let \(h_F\) denote stable logarithmic Faltings height. Von Kanel--Kret Proposition 11.13 and (11.30) give, for this very moduli point,
\[
           h_{\rm W}(Z)\le 2h_F(A_Z)+8^8\log(h_F(A_Z)+8).
\]
Changing the normalization of Faltings height by a dimension-dependent constant does not affect the argument. Its fixed lower bound and this inequality imply
\[
                     h_{\rm W}(Z)\le C_2(1+\max(0,h_F(A_Z)))     \tag{2}
\]
with a constant independent of \(Z\) and \(L\). Both the cover and this height comparison are for the same actual ico point.

We record the elementary consequence of bounded field degree:
\[
                 \log|\Delta_L|+\log\mathrm N\mathfrak f_{A_Z/L}
                    \le C_3(1+\log B(Z)).                       \tag{3}
\]
To check uniformity, for \(p>d_*\) every local extension of degree at most \(d_*\) is tame. Thus the field discriminant exponent at such a prime is at most \(d_*\); at the finitely many primes \(p\le d_*\) it is uniformly bounded by the finiteness of local extensions of bounded degree. For the conductor exponents use Brumer--Kramer, *The conductor of an abelian variety*, Compositio Math. 92 (1994), 227--248, [Theorem 6.2](https://www.numdam.org/item/CM_1994__92_2_227_0.pdf). In their notation with \(g=2\), \(e_v\le d_*\), and \(d_p=\lfloor4/(p-1)\rfloor\), the local bound is
\[
     f_v\le4+e_v\{p d_p+(p-1)\lambda_p(d_p)\},
 \qquad
 \lambda_p(n)=\sum_i i r_i p^i\quad(n=\sum_i r_i p^i).
\]
It is uniform, and equals the bound 4 when \(p>5\). Multiplying by local residue degrees and summing above \(p\) costs at most a further fixed degree factor. Both discriminant and conductor are supported on \(M_*B(Z)\), proving (3). No uniform bound on the *actual* ramified prime set is assumed.

## 2. Consequence for generalized Szpiro

State the required additional conjecture explicitly: for fixed dimension 2 and fixed degree bound \(d_*\), there exist constants \(C_4,C_5\), independent of the field \(L\) and surface \(A\), such that
\[
 h_F(A)\le
 C_4\frac{\log\mathrm N\mathfrak f_{A/L}+\log|\Delta_L|}{[L:\mathbb Q]}
     +C_5.                                                     \tag{GS}
\]
This is the bounded-degree case of the generalized Szpiro conjecture, for example Conjecture 1.1 in the introduction of Wustholz--Fuchs (eds.), *Arithmetic and Geometry*, Annals of Mathematics Studies 202 (Princeton, 2019), p. 4, [preview](https://api.pageplace.de/preview/DT0400.9780691197548_A37122790/preview-9780691197548_A37122790.pdf). Only uniformity over fields of bounded degree and fixed dimension is used; the much sharper proposed coefficient in the conjecture is irrelevant.

Under (GS), (2) and (3) give
\[
                    h_{\rm W}(Z)\ll1+\log B(Z).                \tag{4}
\]
This is a **linear** height budget rather than the currently proved exponential one. The inverse plane chart gives \(h_{\rm W}(g_U)\le8h_{\rm W}(Z)+\log6\). Canonical-height comparison therefore yields
\[
                  qm^2h^2 \ll 1+\log B(Z).
\]
If (1) held with fixed constants, dividing by \(qh^2\ge q>0\) would bound \(|m|\). This proves the conditional impossibility conclusion, including one-reference-per-input strategies.

Equivalently, without assuming (GS), the existence of the requested sequence would produce actual bounded-degree abelian surfaces for which
\[
 \frac{h_F(A_Z)}{1+\log\mathrm N\mathfrak f_{A_Z/L}+\log|\Delta_L|}
\]
is unbounded, at least a constant times \(m^2\) asymptotically. Indeed (2) and the inverse chart bound give a lower bound of order \(qm^2h^2\) for \(h_F\), while (3) and (1) give an upper bound of order \(1+qh^2\) for the denominator. This is a necessary consequence of the hypothetical complete lift, not a claimed construction of counterexamples to (GS).

The identical argument applies to arbitrary off-diagonal forms with controlled diagonal prime support, because the optimal interpolation theorem gives \(\operatorname{rad}(d_{\rm diag})\ge B(Z)\) in the divisibility sense for every such form. It also applies, under the retained ordinary abc charge lower bound, to the charge-based version: the charge height is at least \(qj^2-qh^2-o(j^2)-O(1)\). A linear bound in the reference height again contradicts unbounded true multipliers.

## 3. A necessary compact-type mass under ordinary rational abc

This argument uses the special full level-two structure and does not assume (GS). It applies when the associated principally polarized abelian surface is geometrically indecomposable in characteristic zero. This is sufficient for testing lifts in the open Torelli locus; we do not need to identify the entire guarded chart with that locus.

The Hilbert moduli description in Section 11.2 and (11.6) of von Kanel--Kret supplies the principal polarization and full level-two structure over the base. For clarity, for the different of \(\mathbb Q(\sqrt5)\) choose the totally positive generator \(\epsilon/\sqrt5\) of the inverse different, where \(\epsilon=(1+\sqrt5)/2\). Evaluating the prescribed polarization datum at this generator gives the principal polarization. Taking the underlying rank-four \(\mathbb F_2\)-space of \((\mathcal O/2)^2\), with the alternating trace pairing given by this datum, and choosing a fixed symplectic basis gives the forgetful map to principally polarized abelian surfaces with symplectic level two. The datum is defined over the rational base; this operation does not require adjoining \(\sqrt5\) as a scalar to the base field. It is the forgetful morphism used in Lemma 11.14. We may enlarge \(M_*\) by fixed primes for the integral moduli maps below.

Over an algebraically closed field of characteristic zero an indecomposable principally polarized abelian surface is a genus-two Jacobian. Torelli and the identification \({\rm Sp}_4(\mathbb F_2)\simeq S_6\) identify the level-two Torelli locus with the moduli of six ordered distinct points of the projective line. Equivalently the normalized branch configuration is \((0,1,\infty,\lambda_1,\lambda_2,\lambda_3)\). See Gruenewald, *Computing Humbert surfaces and applications*, [Section 2](https://www.maths.usyd.edu.au/u/davidg/humbertrosfinal.pdf). Since the level labels and coarse moduli point are rational, the normalized coordinates \(\lambda_i\) are rational: a Galois automorphism must preserve the labelled configuration up to projective equivalence, and the transformation normalizing the first three points is unique. This argument does not require a preassigned rational genus-two curve model or descent of a theta constant itself.

Write \(D_{\rm sep}(Z)\) for the product of primes outside \(M_*B(Z)\) at which the associated principally polarized abelian moduli point reduces to a geometrically decomposable one. This condition is intrinsic to the moduli point (equivalently after lifting to the fixed finite etale cover). At every other prime the reduction lies in the open Torelli locus. The three normalized branch functions and their inverses, as well as \(1-\lambda_i\) and their inverses, are regular there. One may use spreading out of these regular functions and the open Torelli moduli isomorphism, excluding a fixed finite number of primes, to see that each \(\lambda_i,1-\lambda_i\) is a unit there. Thus the rational abc radical of each \(\lambda_i\) is supported on \(M_*B(Z)D_{\rm sep}(Z)\).

For each fixed \(\kappa>1\), ordinary rational abc gives
\[
 h_{\rm W}(\lambda_i)\le
   \kappa(\log B(Z)+\log D_{\rm sep}(Z))+O_\kappa(1).
\]
The constant is uniform; none of the branch coordinates is zero, one or infinity in characteristic zero.

We now bound the theta height explicitly. Thomae's formula expresses the ten even theta fourth powers projectively by products of pair determinants, one product for each partition of the six branch points into two triples (up to fixed signs). See Dolgachev--Ortland, *Point sets in projective spaces and theta functions*, Asterisque 165 (1988), Section III.5, [Theorem 2](https://www.numdam.org/item/AST_1988__165__1_0.pdf). Choose primitive integral pairs \((a_i,b_i)\) for the six normalized points; their maximum absolute coordinate is \(H_i=\exp h_{\rm W}(a_i:b_i)\), with \(H_i=1\) for the first three. Each determinant has size at most \(2H_iH_j\); in a partition product of the six determinants each point appears exactly twice. Therefore the projective theta height of the lifted moduli point satisfies
\[
       h_\theta(Z)\le 2\sum_{i=1}^3 h_{\rm W}(\lambda_i)+6\log2 .
\]
The formula is homogeneous in the branch representatives, with the same multidegree for every partition, so it is valid with a point at infinity. A common scalar of the theta vector has no effect on projective height.

Lemma 11.14 of von Kanel--Kret gives \(h_{\rm W}(Z)\le h_\theta(Z)\). The inverse-chart degree bound now yields
\[
 h_{\rm W}(g_U)\le48\kappa(\log B(Z)+\log D_{\rm sep}(Z))+O_\kappa(1).
                                                                    \tag{5}
\]
In particular any true lift satisfying (1) in the indecomposable characteristic-zero locus must have
\[
           \log D_{\rm sep}(Z)\ge
               \left(\frac{m^2}{48\kappa}-C_0\right)qh^2-O_\kappa(1).
                                                                    \tag{6}
\]
This holds uniformly, including at individually chosen single references.

The separating/compact-type degeneration primes in (6) cannot simply be added to the allowed small prime set by the good-reduction criterion for \(A_Z\). The Jacobian of a stable curve of compact type can have good abelian reduction even when the curve itself is singular with two elliptic components. The five coordinate points of the ico compactification do not include the decomposable interior divisor. This distinction prevents the usual rational-abc bound for a six-branch-point configuration from establishing (4) directly. We have not proved any upper bound for \(\log D_{\rm sep}(Z)\) in terms of \(\log B(Z)\) under ordinary rational abc. Equation (6) is a necessary large interior-prime mass, not an unconditional contradiction. It is consistent with the generalized-Szpiro obstruction and makes the obstruction quantitatively visible in the Torelli locus.

## Conclusion

A uniform boundary-controlled ico lift for every integer multiplier would violate a standard conjecture about heights of abelian surfaces, even with arbitrarily flexible arithmetic lifts and just one reference per integer. This is a stronger limitation than any fixed-rational-map argument. The proposed eight-coordinate coefficient budget in the [companion note](../../../papers/elliptic_divisibility/ico_coefficient_anchor_20261125/README.md) satisfies precisely this uniform budget on all actual solutions; consequently one should not expect to obtain its completeness if (GS) is true. The ordinary rational abc assumptions in the project do not settle (GS). No new lower bound on arbitrary Diophantine definitions of the integers, no unconditional counterexample to the desired completeness, and no new complete defining polynomial are claimed.
