# Research directions

The established counts under the retained arithmetic premises are **25 total variables**, or **196 for a quartic**. The additional height hypotheses give **13 total variables**; ordinary rational abc gives a **78-variable quartic**. Every count includes the input. The priorities are variable count, degree, then coefficient height. The [main results table](../README.md) distinguishes the hypotheses and effective parameters; no global minimum or completed independent audit of all inherited arithmetic premises is asserted.

## The 25-coordinate budget

The [finite-algebra source](../papers/finite_algebra/unit_norm_20261114_v28.tex) has the following budget.

| Role | Rational coordinates |
|:--|--:|
| Input | 1 |
| Nine elliptic points over the quadratic field | 18 |
| Comparison slope | 1 |
| Two parameters for each of two pole predicates | 4 |
| One coordinate encoding all finite algebraic choices | 1 |
| **Total** | **25** |

The finite-algebra encoder already uses one extra coordinate. Smaller arithmetic circuits can lower the degree without changing this budget. A smaller total requires a complete source with fewer retained parameters, or a different encoding theorem that actually removes a retained coordinate.

The [terminal quadratic-root theorem](../papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) permits the last pole ordinate to vanish. It proves the degree bound

$$
\deg P_{25}\le 5\,059\,009\,872\,658\,432<2^{53}
$$

with the same variable count and inherited arithmetic premises. The two 13-variable constructions have degree below $2^{26}$. These are certified upper bounds from exact finite-operation specifications, not expanded polynomial degrees. Only the last quadratic step may lose its unit condition in this theorem: all preceding radicands remain nonzero. The character-descent proof handles nilpotents at that last step, so a simple-eigenvalue argument is unnecessary.

### A shared conic parameter: the precise route to 24

For a pole input written $b_i=d_i t_i^2$ with $d_i t_i\ne0$, the current rational chart is

$$
e_i=\frac{\tau_i^2-17d_i}{\tau_i^2+51d_i},
$$

$$
q_i^2=
17d_i\bigl(s_i^2-17e_i(17-b_i)\bigr)
       \bigl(s_i^2+51e_i(17-b_i)\bigr).
$$

The square factor $t_i^2$ is extracted from the fixed source circuit. The [rescaling theorem](../papers/finite_algebra/unit_norm_20261114_v28.tex), Section 4, gives the exact invertible change from the original pole equations and states its denominator guards.

Replacing $\tau_0,\tau_1$ by one freely varying rational $\tau$ would leave the three retained pole parameters $\tau,s_0,s_1$. If a complete source with this property were proved, the displayed budget would become **24**. The finite ordinates would still use the existing separating coordinate.

The missing result is a **simultaneous rational realization theorem**. For every integer input, one must choose the actual elliptic, prime-pattern and comparison data so that both displayed square equations have rational solutions at a common $\tau$, with all required nonzero guards. A theorem for every prepared pair of pole inputs would suffice, but completeness only needs the pairs actually supplied by a proved source construction. Individual solvability or separate Zariski-density statements for the two pole surfaces do not establish that their permitted $\tau$-values intersect.

This proposal shares the conic coordinate, not $e_i$ itself. Sharing $e$ requires matching input square classes; the [joint-pole theorem](../papers/pole_parameters/joint_pole_realization_20261114_v29.tex) proves that the existing fresh-prime witnesses violate that requirement. The [common-twist theorem](../papers/pole_parameters/common_twists_20261114_v30.tex) gives genuine savings on its explicitly compatible locus, but does not put the full integer construction on that locus. A common $\tau$ allows different $e_i$ and avoids that particular necessary square-class equality. It still needs its own arithmetic existence proof.

A fixed value of $\tau$ does not supply this missing result. The [fixed-parameter obstruction](../papers/pole_parameters/fixed_pole_parameters_20261109_v17.tex) gives prepared inputs excluding $\tau=\pm1$ and $\tau=\pm17$, including arbitrarily small prepared inputs in the latter case. The proposed shared parameter must remain variable unless a new restricted completeness theorem proves otherwise.

### Integral labels from one finite Pell choice

The [integral Lucas-label theorem](../papers/integer_labels/pell_labels_20261115_v40.tex) supplies a different arithmetic compression. Let $a,n$ be integers with

$$
|a|\ge3,\qquad c=|a-2|\ge3,\qquad n\ne0,\qquad t=(a-2)n+1.
$$

If a rational $w$ satisfies

$$
t^2-atw+w^2=1,
$$

then monicity forces $w$ to be an integer. With $U_0(A)=0$, $U_1(A)=1$ and $U_{j+1}(A)=AU_j(A)-U_{j-1}(A)$, the sharp lower bound is

$$
|t|\ge U_{c-1}(|a|)\ge(|a|-1)^{c-2}.
$$

Thus a third separately integral label can be replaced by a finite quadratic choice when the first two labels are already exact integers. The equivalent square condition is

$$
z^2=(a^2-4)\bigl((a-2)n+1\bigr)^2+4,
$$

of total degree six and coefficient height sixteen. The same paper gives sharp witnesses and arbitrarily large solutions preserving prescribed finite congruence data of a given witness.

The present source carries labels through local approximations by elliptic formal-parameter ratios. Those rational ratios are not known to be the exact integral labels, so monicity at the ratios does not prove the needed integrality. This distinction has a concrete counterexample: $a=5,n=1$ gives discriminant $340$, which is not a rational square, but for every $r\ge1$ there are rational norm-one solutions with $0<n_r<1$ and $n_r\equiv1\pmod{19^r}$. The paper proves this by an explicit rational parametrization. A useful application must therefore recover an exact integer carrier, or prove a new global implication from the complete source equations. Arbitrarily precise local approximation alone does not close the gap.

### Dependencies among point roles

A replacement for the nine points need not realize every independent tuple of labels. That freedom is where a genuine reduction can occur. It must nevertheless give witnesses for every integer input and prove soundness on every rational solution of the new source.

Two established obstructions delimit direct substitutions:

- The [dimension and label-graph theorems](../papers/elliptic_charts/structural_constraints_20261109_v13.tex) show that a finite algebraic presentation recovering arbitrary tuples of nine points needs at least eighteen rational parameters. The integer-index graph itself is Zariski dense in the product of the additive group and the relevant abelian variety.
- The [index-product theorem](../papers/elliptic_charts/index_products_and_finite_correspondences_20261110_v21.tex) shows that a fixed correspondence with finite geometric fibers cannot recover $[nh]P$ from $[n]P,[h]P$ uniformly for infinitely many $n$ and infinitely many permitted $h$ for each $n$. Restricting each index to congruence classes does not remove this obstruction.

These statements concern generic recovery and the specified finite correspondences. They do not exclude a smaller arithmetic source whose witnesses satisfy additional dependencies, or one using a different integer-growth relation.

## Propagating the three-coordinate chart through a quartic

The [three-coordinate reference chart](../papers/elliptic_charts/three_coordinate_reference_20261115_v40.tex) gives a complete algebraic improvement. For $P=(a,b)$ on $y^2=x^3-Dx$, put $c=b/a$ and $\delta=D/a$, with $abD\ne0$. The two quadratic equations

$$
v(v+T-S)=-\delta,\qquad
ST+c(T-S)+2cv+2\delta=0
$$

recover the reference pair $H,H-P$ from just three field coordinates $S,T,v$. They describe exactly the open set on which both points are finite with nonzero abscissas, including the allowed tangent and torsion cases. Define

$$
u=\frac{v-S-c}{a},\qquad
w=\frac{v+T-c}{a}.
$$

Then $auw=1$, $v\ne0$, and

$$
v^{-1}=-\frac{v+T-S}{\delta},\qquad
x(H)^{-1}=\frac{u}{v},\qquad
x(H-P)^{-1}=\frac{w}{v}.
$$

Replacing a five-field-coordinate reference block by this chart would remove four rational coordinates **within that block**. A complete quartic saving does not yet follow. The reciprocal abscissas are now quadratic expressions, so their squares are generally quartic. The surrounding comparison factors consume these square coordinates and must remain quadratic before taking the final sum of squares.

The [uniform rescaling theorem](../papers/elliptic_charts/paired_ratio_redundancy_20261115_v40.tex), Section 2, addresses part of this propagation problem. Multiplying all seven point-pair coordinates $f,h,g,j,s,F,G$ by the same retained unit $v$ preserves quadratic equations. The rescaled square satisfies $vF_*=f_*^2$, not $F_*=f_*^2$. Both complete ratio equations stay quadratic. Recovering the old slope for the difference-abscissa trace can be done quadratically by retaining a further field coordinate $r$ with $s_*=vr$; that recovery costs two rational coordinates. Every such cost must be included in a full comparison.

The next mathematical target is a simultaneous choice of coordinate weights for the reference chart, reciprocal point pairs, height trace and detector factors. A valid saving requires an input-preserving equivalence of the whole system, a nonvanishing proof for every rescaling unit from retained equations, and degree at most two in every final row. A count on a generic chart alone is insufficient.

The complete ratio equations also imply the paired curve equations whenever the two reference ratios do not vanish together. The fixed translating point is not two-torsion, which supplies that nonvanishing on the entire reference chart. This gives [176 quadratic rows in 196 variables](../papers/quartic/quartic196_redundancy_20261115_v40.tex) and [68 rows in the 78-variable abc system](../papers/elliptic_charts/paired_ratio_redundancy_20261115_v40.tex), with the same full rational zero sets as the respective unreduced systems. The [primitive quadratic bases](../papers/quartic/primitive_quadratic_bases_20261115_v40.tex) then lower the coefficient heights by exact invertible rational row changes and specified constant coordinate scalings. Their quartics have 2994 and 1254 monomials, respectively. The variable counts, degree and sufficient defining thresholds are preserved. These identities can be used in further eliminations, but deleting rows or changing their basis alone does not lower the number of variables.

## Arithmetic and coefficient obligations

A shared pole parameter preserves two separate parity tests. Replacing them by a single rational test is a different proposal and encounters stronger restrictions. The [product-height counterfamilies](../papers/pole_parameters/product_height_obstructions_20261110_v19.tex) show that the product of two contact functions can have trivial odd radical while the scale is large. The [local rational-combination theorem](../papers/pole_parameters/rational_combinations_of_contacts_20261110_v20.tex) excludes every fixed rational parity combination for its specified source family. These are obstructions to the stated implications, not to all single-pole constructions.

Forcing equality of the two contact square classes can prove soundness, but rational completeness becomes a separate problem. At a fixed comparison scale, the [quadratic contact cover](../papers/pole_parameters/quadratic_contact_covers_20261110_v21.tex) has genus four. Allowing both ordered contact arguments to vary gives the [ordered square-class surface](../papers/pole_parameters/ordered_squareclass_surface_20261115_v33.tex), which is of general type. It has neither a dominant rational parametrization nor a fibration with rational or genus-one general fiber. These facts leave open special arithmetic families of witnesses; they exclude the corresponding unrestricted parametrization strategies.

For effective coefficients in the few-variable construction, the unresolved analytic issue is a uniform effective trace-height estimate on the relevant integer-index tuples. The [explicit construction](../papers/few_variables27/explicit27_20261110_v19.tex) uses both rational components and a third pole predicate to avoid that issue. Positivity on selected completeness witnesses cannot replace a height bound needed for every soundness tuple.

For quartic coefficient optimization, invertible rational combinations of quadratic rows preserve the rational zero set, and invertible coordinate rescalings give a bijection of zero sets. Each proposed change must be followed by primitive integer normalization and exact collection of the squared rows. A height claim for a parameter family needs a bound for every allowed parameter, together with a coefficient that attains it; one small test member does not establish that claim. The current [primitive-basis coefficient theorem](../papers/quartic/primitive_quadratic_bases_20261115_v40.tex) gives

$$
H(P_N)=\max\{126616122944180358034867798936,\;32561227748626372080\cdot149^{2N}\}
$$

for the 196-variable family, and

$$
H(Q_B)=\max\{20828275368498373068800,\;B^2+275933278576697172\}
$$

for the 78-variable family. These algebraic improvements are independent of any remaining audit of the arithmetic premises; their parameter terms and ineffective sufficient defining thresholds remain.

The [lower-bound results](../papers/lower_bounds/lower_bounds_20261109_v15.tex) require degree at least four for a single defining equation and at least five total coordinates for a globally nonnegative quartic or a quadratic system. They supply no lower bound near the current counts.

## Rings of integers of number fields

No counterexample to $\mathcal O_K$ being Diophantine in its fraction field $K$ has been established. The [number-field reductions](../papers/number_fields/number_field_definability_20261109_v12.tex) give three useful formulations:

1. $\mathcal O_K$ is Diophantine in $K$ if and only if $\mathbb Z$ is Diophantine in $K$, using the cited theorem defining $\mathbb Z$ inside $\mathcal O_K$.
2. Assuming a definition of $\mathbb Z$ in $\mathbb Q$, these are equivalent to the rational subfield $\mathbb Q$ being Diophantine in $K$.
3. A counterexample persists through every finite extension. Hence one could pass to a totally imaginary Galois extension when searching for a counterexample.

A failure after extending the witnesses of a particular polynomial is a failure of that polynomial. It does not establish the third assertion's counterexample hypothesis. The same reduction paper proves that no fixed finite collection of formulas can work unchanged throughout all finite extensions; field-dependent constructions remain possible.

The specified $j=1728$ elliptic curve cannot be transferred unchanged across adjoining $i$. The [complex-multiplication theorem](../papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.tex) proves exact rank doubling and constructs an infinite cyclic subgroup with zero abscissa trace and unbounded heights. It also supplies distinct doubled points with zero abscissa sum. A number-field construction must use another curve or prove a height statement that controls these cancellation directions.

Rank stability is useful but does not itself define the rational subfield: it supplies an infinite Diophantine subset of rational abscissas, which can remain arithmetically sparse. Likewise, writing a norm or trace in base-field coordinates does not force unrestricted extension-field variables to lie in the base field. The [norm-and-trace equivalences](../papers/number_fields/number_field_definability_20261109_v12.tex), Section 4, identify that missing restriction explicitly.

One sufficient positive target is a Diophantine set $T\subset K$ containing every rational integer and having uniformly bounded integral denominators. Indeed, for an integral basis $\omega_1,\ldots,\omega_n$, the set $S=\sum_i\omega_iT$ contains $\mathcal O_K$ and satisfies $MS\subseteq\mathcal O_K$ for some positive integer $M$. A finite union of translates of $MS$ by representatives of $\mathcal O_K/M\mathcal O_K$ then equals $\mathcal O_K$. The [finite-correspondence and denominator theorems](../papers/number_fields/finite_correspondences_and_denominators_20261109_v14.tex) exclude several routes to such a set, including quasi-finite covers of abelian varieties and their stated low-genus extensions. A successful construction must avoid those hypotheses or use exceptional positive-dimensional fibers with a proved arithmetic completeness argument.

The decisive goals are therefore a complete shared-parameter pole realization, a globally quadratic propagation of the three-coordinate chart, an exact integral carrier for the Pell compression, or a new number-field denominator mechanism. Each would change an actual arithmetic dependency rather than only the presentation of an existing formula.
