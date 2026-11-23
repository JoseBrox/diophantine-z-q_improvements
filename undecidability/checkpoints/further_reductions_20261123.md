# Further reductions: proved limitations and current research obligations

Date: 23 November 2026.

The proved unrestricted-degree transfer bounds at this checkpoint are **99** variables for the general source, **117** for the specified source at $L=143$, and **69** under ordinary rational $abc$. They retain the non-pole arithmetic premises of the v88 sources. The general $L=143$ and ordinary-$abc$ $B=3$ stored members are algebraic fixtures, not certified sufficient specializations. This checkpoint claims no further numerical reduction.

## A squareclass obstruction in the current prepared witnesses

The v88 finite-support twist method can share pole parameters when the actual pole inputs have one common rational squareclass. The fresh-prime preparation in the current joint construction does not satisfy that condition.

Consider two different input blocks $i\ne\ell$. In the two- or three-detector general source the actual pole inputs are

$$
 e_{ij}=\frac{4\rho_iR_{ij}}{V_{ij}^2},
 \qquad V_{ij}=\operatorname{Tr}(W_{ij}^{-1}).
$$

The following hypotheses are part of the proved simultaneous preparation:

- The contact positions belonging to different input blocks are disjoint. They lie in the disjoint intervals obtained from $\lambda_i=\lambda+100i$.
- The selected primes avoid the numerators and denominators of every $\rho_i$, every scale, every fixed contact denominator, and every nonzero difference of contact positions. In particular the selected primes are odd and all the $\rho_i$ are units there.
- Each individual contact function is a rational square times the product of its selected primes. A prime selected for that contact occurs with valuation one in its contact numerator.
- At a selected prime of detector $(i,j)$, its normalization denominator and its actual reciprocal trace $V_{ij}$ are units. All pole inputs and all traces used as denominators are nonzero.

Choose a fresh prime $p$ of detector $(i,j)$. Then

$$
 v_p(\rho_i)=0,\qquad v_p(R_{ij})=1,\qquad v_p(V_{ij})=0,
 \qquad v_p(e_{ij})=1.
$$

For any detector $(\ell,q)$ of a different input block, $p$ belongs to none of its selected contact factors. Its scalar is a unit at $p$. The remaining factor in its contact function is a rational square, since its exponent is ten. Thus even a valuation of its normalization denominator contributes an even integer. Consequently

$$
 v_p(\rho_\ell R_{\ell q})\in2\mathbb Z,\qquad
 v_p(e_{\ell q})
   =v_p(\rho_\ell R_{\ell q})-2v_p(V_{\ell q})\in2\mathbb Z.
$$

It follows that $v_p(e_{ij}/e_{\ell q})$ is odd. A nonzero rational square has even valuation at every prime, so

$$
                 e_{ij}/e_{\ell q}\notin\mathbb Q^{\times2}.
$$

The actual pole inputs in different input blocks therefore have different rational squareclasses on these prepared witnesses. Replacing an extracted representative $d$ by $dM^2$, as in v88, cannot alter this conclusion.

This proof is stated for the two- and three-detector general sources. In the ordinary-$abc$ derivative source, odd valuations can also arise from its derivative denominator. Disjoint contact numerators alone would therefore not justify the same conclusion. An analogous statement would require a separate avoidance and noncollision check for those derivative denominators; it is not asserted here.

### Precise scope

This excludes applying the **common-squareclass** sharing theorem to the **current prepared general-source witnesses**. It does not prove that two arbitrary pole fibers have no common rational parameters. It does not exclude a different contact construction, a different arithmetic realization theorem, or a smaller-variable polynomial of another form.

The separate Bhargava--Burungale pole fibers have Zariski-dense rational projections to their parameter planes. Density of each projection alone does not prove that their intersections contain a rational point; dense subsets of a rational affine plane can be disjoint. A proposed identification of private pole parameters therefore needs an additional simultaneous-realization theorem, with its full local and guard conditions.

## Point-coordinate sharing

The seven shared point roles in the general construction and the one shared reference in the ordinary-$abc$ construction have complete simultaneous-witness proofs. The two retained base coordinates of a point chart represent its rational abscissa data; its finite algebra already removes the ordinate choices without retaining additional rational coordinates.

Directly identifying distinct private **root points** does not preserve the general tuple predicate. The prepared root labels are $n_i=X_i^2+1$ in the general route and $n_i=y_i=X_i^2+1$ after the ordinary-$abc$ input substitution. Since $P$ is nontorsion, equality $[n_i]P=[n_\ell]P$ implies $n_i=n_\ell$. For example inputs $0,1$ require the distinct roots $P,2P$. This rules out that literal identification while retaining the same root-label interpretation; it is not a lower bound for other charts or other reductions.

A different proposal may be more flexible: replace the private numerator points $U_{A_i}$ by one common $U=[j]P$, allowing $j$ to be independent of the reference index $h$. At a prime allocated to input $i$, one would ask $U$ to approximate $[n_i]H$ sufficiently closely. This would require compatible congruences of the form

$$
 j\equiv0\pmod{o_{i,p}^{\rm primary}},\qquad
 j\equiv n_i\pmod{o_{i,p}^{\rm opposite}},\qquad
 j-n_i h\equiv0\pmod{p^{r_{i,p}}},
$$

together with the old finite and real preparation and all denominator guards. Coprimality of the **selected primes** with the reduction orders does not, by itself, establish compatibility of the distinct **reduction orders with each other**. The latter property and the necessary formal-accuracy refinements must be proved from the exact retained prime supplier before a variable saving can be claimed.

If this proposal is established, the arithmetic would differ from the existing exact multiplication family $U_{A_i}=[hn_i]P$. It therefore requires a new completeness proof and a new source transformation. It is recorded here as a research obligation, with no additional numerical bound asserted.

## Current deliverables and remaining work

The clean results to use are the 99-, 117-, and 69-variable transfer manuscript, its complete native-source DAG transformations, and its exact degree and count ledgers. Further work should first settle the numerator-index congruence compatibility and the finite-place preparations for a common $U$. Pole-parameter identifications should not be inferred from density or from the number of finite roots eliminated by the encoder.
