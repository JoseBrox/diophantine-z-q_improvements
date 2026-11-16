# Literature references

These primary sources are relevant to the current research directions. A comparison reference is not an additional premise of a polynomial specification. The construction manuscripts and [arithmetic-dependency guide](arithmetic_inputs.md) identify the precise versions and theorem statements actually used.

## Definitions over the rationals

1. **Ashay Burungale**, *A Diophantine definition of Z in Q*, arXiv:2611.16130v1, 12 November 2026. [Versioned abstract](https://arxiv.org/abs/2611.16130v1); [HTML](https://arxiv.org/html/2611.16130v1). This preprint describes a quartic definition through congruent-number twists and a Shimura-curve height argument. The abstract gives an existential variable count rather than an explicit numerical record. Its pole preparation and square-class conditions must be compared explicitly before replacing another source theorem. No arithmetic premise of the present specifications is replaced by this citation.

2. **Zhi-Wei Sun**, *Z is Diophantine over Q with 28 unknowns*, arXiv:2611.14605v1, 10 November 2026. [Versioned abstract](https://arxiv.org/abs/2611.14605v1); [HTML](https://arxiv.org/html/2611.14605v1). The displayed formulation has one input x and 28 existential witnesses, hence **29 total variables** in this repository's convention. Its stated count is not below the current 25-variable source. This reference is distinct from Sun's earlier prime-pattern theorem cited in the arithmetic dependencies.

3. **Manvir Jaswal**, *A proof that Z is Diophantine in Q through congruent-number twists*, Hexagon 2611.00331v2, 12 November 2026, Theorem 1.2. [Versioned paper](https://hexagonmath.org/pdf/2611.00331v2). The prepared two-twist application is proved in the repository's [congruent-twist pole paper](../papers/pole_parameters/congruent_twist_poles_20261114_v27.tex). The separately supplied [finite-family audit](../sources/hexagon/jaswal_row5a_audit_and_simultaneous_twists_20261113.tex) is used for the compatible-pole theorem only. These two inputs are not interchangeable without their hypotheses.

The versioned bibliographic entries for the first two comparison papers are also available in [BibTeX](../data/literature_20261115.bib). No assertion of a complete literature survey or non-author verification is made.

### Pole-parameter comparison

In Burungale's Definition 3.1 and the following remark, the displayed witnesses are t,e,v,w,Y,Z, with two square equations. Treating Y,Z as finite algebraic choices leaves four retained parameters. Our exact homogeneity normalization, valid because v is nonzero, replaces e,w,Y,Z by e/v²,w/v,Y/v²,Z/v² and sets v=1. This leaves three retained parameters, compared with two in the current pole chart. This calculation concerns that presentation, not a lower bound. Proposition 3.14 chooses the additional preparation parameter t separately for each input; it does not state the shared-conic-parameter realization needed in the current [24-variable strategy](research_directions.md#a-shared-conic-parameter-the-precise-route-to-24).

## Local curves and noncongruence certificates

- **J. S. Milne**, *Elliptic Curves*, second edition, World Scientific, 2021. [Author's PDF](https://jmilne.org/math/Books/EC2.pdf). Chapter IV, Corollary 9.3 gives a rational point on every smooth projective genus-one curve over a finite field; Theorem 9.4 gives the elliptic Hasse bound. These precise statements support the good-reduction case of the shared-parameter local theorem.
- **J. B. Tunnell**, *A classical Diophantine problem and modular forms of weight 3/2*, Inventiones Mathematicae **72** (1983), 323–334. [DOI](https://doi.org/10.1007/BF01389327); [original paper scan hosted at Rutgers](https://sites.math.rutgers.edu/~zeilberg/EM22/JT1983.pdf). The introduction's Theorem (a), on page 323, says that a nonzero coefficient of \(q\prod_{m\ge1}(1-q^{8m})(1-q^{16m})\sum_{z\in\mathbb Z}q^{2z^2}\) proves that its positive integer index is not a congruent number. Only this unconditional necessary direction is used. Page 324 gives the rational-triangle correspondence. The automatic-conic checker computes coefficients \(-4\) and \(-256\) at 17 and 15,499,155, respectively, and checks them independently using ternary counts. No conditional converse, analytic rank, or BSD hypothesis is used.

## Rational torsion in the fixed pole fibers

- **B. Mazur**, *Modular curves and the Eisenstein ideal*, Publications Mathématiques de l’IHÉS **47** (1977), 33–186. [DOI](https://doi.org/10.1007/BF02684339); [primary Numdam scan](https://archive.numdam.org/item/10.1007/BF02684339.pdf). Introduction, Theorem (8), page 35 gives the rational torsion classification. The [fixed-fiber paper](../papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex) applies the full-two-torsion case and supplies explicit order-three and order-four exclusions for every nonsquare twist used here. The odd valuation at 17 checks the nonsquare hypothesis at every rational conic parameter.

## Geometry of the fixed-input pole surfaces

- **G. Angermüller and W. Barth**, *Elliptic fibres on Enriques surfaces*, Compositio Mathematica **47** (1982), no. 3, 317–332. [Primary scan](https://www.numdam.org/item/CM_1982__47_3_317_0.pdf), Section 3, page 319: a double cover of the quadric branched along a reduced curve of bidegree (4,4) with the stated simple singularities resolves to a K3 surface.
- **O. Debarre**, *On rationality problems*, author notes dated 15 April 2024. [Author’s PDF](https://perso.imj-prg.fr/olivier-debarre/wp-content/uploads/sites/34/2024/04/On-rationality-problems.pdf), Proposition 2.5(b): smooth projective rationally connected varieties have no nonzero regular differential forms in positive degree. The [fixed-input pole theorem](../negative_results/papers/pole_parameters/fixed_input_k3_surfaces_20261116_v42.tex) gives the explicit branch equations, all four local singularity calculations and the dominance argument needed to apply these results.

## Rational sections and quadratic twists

- **A. V. Sutherland**, *The Hilbert class polynomial*, MIT 18.783, Spring 2017, Lecture 21, 1 May 2017. [Author’s notes](https://math.mit.edu/classes/18.783/2017/LectureNotes21.pdf), Corollary 21.13, page 6 proves that a CM elliptic j-invariant is an algebraic integer. The explicit Jacobian in the [rational-section classification](../negative_results/papers/pole_parameters/rational_sections_20261116_v42.tex) has j=2048/3, so its geometric endomorphism ring is Z.
- **J. S. Milne**, *Elliptic Curves*, second edition, Chapter II, Section 1, Proposition 1.5. [Author’s PDF](https://jmilne.org/math/Books/EC2.pdf). A nonconstant morphism of elliptic curves carrying origin to origin is a group homomorphism. The section proof first obtains a rational origin on the target from the image of a rational source point, so it does not assume the genus-one target has a rational point in advance.

## Common rational fibers and fixed twist classes

The [fixed-fiber literature audit](../negative_results/docs/fixed_fiber_literature_20261116_v43.md) supplies theorem-by-theorem hypotheses and primary links for Huang (2021), Gvirtz (2019), Skorobogatov–Swinnerton-Dyer (2005), Harpaz–Skorobogatov (2016), Wittenberg (2007), Colliot-Thélène (2001), and Harpaz–Wittenberg (2016). Their direct application to the current common-parameter family fails at explicitly identified torsor, two-torsion, semistability, or cohomological conditions. No implication from local solubility, Schinzel's hypothesis and finite Sha to the required common rational point is asserted.

Faltings, *Endlichkeitssätze für abelsche Varietäten über Zahlkörpern*, Inventiones Mathematicae **73** (1983), 349–366, with correction **75** (1984), 381, supplies rational-point finiteness for the fixed-class synchronization curves of genus at least two. [Primary scan](https://math.uchicago.edu/~drinfeld/Deligne%27s_conjecture_Manin_conf/Faltings_argument/Faltings.pdf). The [synchronization paper](../negative_results/papers/pole_parameters/fixed_class_synchronization_20261116_v43.tex) proves the exact genus and quotient formulas before applying this theorem. Finiteness of each fixed class tuple does not imply finiteness of their infinite union.

All eight additional bibliographic entries appear in the shared [BibTeX file](../data/literature_20261115.bib).

## Number-field questions and limitations

The precise external sources for the number-field reductions are retained in [Number-field definability](../papers/number_fields/number_field_definability_20261109_v12.tex), [Finite correspondences and denominators](../negative_results/papers/number_fields/finite_correspondences_and_denominators_20261109_v14.tex), and [Complex multiplication and trace cancellation](../negative_results/papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.tex). They distinguish definitions inside rings of integers from definitions inside their fraction fields.

Undefinability results for infinite algebraic extensions do not supply counterexamples for number fields. Likewise, rank stability or an infinite Diophantine set of rational abscissas does not by itself define the entire rational subfield. The current [strategy guide](research_directions.md#rings-of-integers-of-number-fields) states the required additional denominator and completeness arguments.
