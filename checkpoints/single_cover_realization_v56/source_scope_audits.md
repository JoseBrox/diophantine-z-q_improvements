# Additional primary-source audits

## Harpaz–Skorobogatov and the affine Pheidas block

Primary source: Yonatan Harpaz and Alexei N. Skorobogatov, *Hasse principle
for Kummer varieties*, Algebra & Number Theory 10 (2016), 813–841,
https://msp.org/ant/2016/10-4/ant-v10-n4-p05-p.pdf.

Theorem 2.3 and conditions (a)–(g) were checked directly in the published
text against `checkpoints/independent_route_v56/affine_pheidas_theorem.tex`.
The proof correctly uses the general theorem, not the more restrictive
discriminant-valuation-one corollary. Its selected primes only need to be
distinct and odd. Multiplicative reduction with odd geometric component
group order is sufficient, so any positive odd discriminant valuation at
a prime with unit c4 works.

The original draft's conclusion `p_i>7` was false under its stated lemma
hypotheses. For `c=114/13`,

`2048 c^2-27 = 5 (2307/13)^2`,

so the second discriminant factor has no odd valuation at any prime
above seven. The proof gives primes outside `{2,3,7}`, and allowing five
repairs the theorem: all Jacobian scaling constants involve only two
and three, and the two discriminant factors differ by `D_2-8D_1=189`.
At a selected prime the quartic's unique double root is `r_i=-4i/3`;
its other two roots are simple and lift over the maximal unramified
extension. These repairs were communicated to the authoring agent and
incorporated into its latest manuscript and exact certificate.

The local-solubility proof also works when `v_2(c)>0`, rather than
only when it equals one: solve `c^2 x^4+x+1=c/2` over Z_2, whose
derivative is one modulo two. The affine Galois lemma still uses
`v_2(c)=1` for its Newton polygon. The integer-only corollary supplies
a separate irreducible-resolvent argument when the valuation is higher.

After these corrections, the local-solubility cases, S4/S3 group
conditions, linear disjointness, unramified nonzero torsor classes,
geometric component groups, and the fixed-input all-sign guard argument
pass this independent audit. The additional finiteness of 2-primary
Tate–Shafarevich groups remains an explicit hypothesis. This source
does not prove a one-parameter specialization.

## Achenjang–Woo: prime patterns, conic bundles, rank-two twists

Primary work: Niven Achenjang and Katharine Woo, *Prime values of linear
forms and a quadratic form: one proof and two arithmetic applications*,
arXiv:2611.16062v1, 11 November 2026.

Official record: https://arxiv.org/abs/2611.16062.
The official PDF retrieval failed in this session; the same primary
paper was read at https://arxiv.cnoctave.top/pdf/2611.16062.

Theorem A treats finitely many independent linear forms and one
imaginary-quadratic norm form. It does not supply simultaneous prime
values of the six different quadratic contact forms forced by the
single-cover substitution `t=c+z^2`.

Theorem 9.2 is a fibration theorem over P1 with specified degeneration
fields and Hasse/weak-approximation assumptions on its rational fibers.
It does not automatically apply to an actual detector incidence after
writing some of its equations as norms: the additional square
constraints give K3 or higher-genus covers rather than conic fibers.

Theorem 10.1 concerns rank exactly two twists of curves
`E_(mu,lambda): y^2=x(x-mu)(x-lambda)` satisfying all of Definition
10.4. In particular `lambda=mu*m^2`, `m=2 mod 8`, and several extra
prime-factor conditions are required. Neither the congruent-number
curve nor the original m=2 pole curve meets those hypotheses.

Proposition 10.2 gives two independent sections in a Rubin–Silverberg
family. Their abscissa ratio is `alpha^2/u^2`, a rational square.
Thus their independence does not provide arbitrary two prescribed
abscissa square classes. The result does not by itself synchronize the
actual detector inputs.
