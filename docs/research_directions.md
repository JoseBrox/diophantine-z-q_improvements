# Research directions

The established counts under the retained arithmetic premises are **25 total variables**, or **195 for a quartic**. The additional height hypotheses give **13 total variables**; ordinary rational abc gives a **74-variable quartic**. Every count includes the input. The priorities are variable count, degree, then coefficient height. The [main results table](../README.md) distinguishes the hypotheses and effective parameters; no global minimum or completed independent audit of all inherited arithmetic premises is asserted.

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

The missing result is a **simultaneous rational realization theorem**. For every integer input, one must choose the actual elliptic, prime-pattern and comparison data so that both displayed square equations have rational solutions with nonzero ordinates at a common $\tau$. The earlier point-stage guards are retained; the fixed-fiber theorem below supplies the remaining pole guards. A theorem for every prepared pair of pole inputs would suffice, but completeness only needs the pairs actually supplied by a proved source construction. Individual solvability or separate Zariski-density statements for the two pole surfaces do not establish that their permitted $\tau$-values intersect.

The [local-solubility theorem](../papers/pole_parameters/shared_parameter_local_solubility_20261115_v41.tex) proves that **every rational $\tau$** works over every completion for every prepared input, and a finite family can use that same parameter. The [fixed-fiber and scalar-input theorem](../papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex) strengthens the guard statement for actual native sources: the extracted $d_i$ are positive rational scalars independent of all auxiliary points and characters. Every rational $\tau$ avoids all conic denominator zeros. One nonzero rational pole witness in each fixed fiber gives infinitely many witnesses there and permits all remaining pole norms to be avoided. The problem is therefore simultaneous rational realization. In exact elliptic terms, for $D_i=17d_i$ and $C_i=17(17-b_i)$, one needs nonzero-ordinate points in the abscissa classes $D_i\mathbb Q^{\times2}$ on the correlated families

$$E_{N_i(\tau)}:\ y^2=x(x-N_i(\tau))(x+3N_i(\tau)),\qquad N_i(\tau)=D_iC_i(\tau^2-D_i)(\tau^2+3D_i).$$

Congruence sieves cannot exclude the shared parameter on this prepared locus. A global argument must establish the simultaneous rational square-class condition with nonzero ordinates. No separate pole-guard avoidance theorem remains necessary.

The same paper proves independent auxiliary-index freedom: after fixing one prepared guarded tuple, the five auxiliary points in the general source, or two in a conditional source, may vary independently in infinite cyclic return sets while preserving preparation and all earlier norms. The extracted $d_i$ remain fixed. This is a family of actual detector inputs, but it does not imply arbitrary rational values for the detector multipliers or preservation of rational pole solubility. The [proof guide](common_parameter_guard_reduction_20261116_v42.md) states the exact remaining assertion.

The [fixed-input geometry theorem](../negative_results/papers/pole_parameters/fixed_input_k3_surfaces_20261116_v42.tex) identifies each full one-pole surface, with $\tau$ still variable, as a K3 surface after resolving four $A_3$ singularities. The common-parameter product for fixed detector inputs dominates each K3 factor, so it has no rationally connected smooth projective model. This limits a geometric proof method for fixed inputs; it does not exclude rational witnesses or the independently varying actual detector families.

The [rational-section classification](../negative_results/papers/pole_parameters/rational_sections_20261116_v42.tex) makes one sufficient arithmetic locus explicit. For prepared fixed inputs, sections over $\mathbb Q(\tau)$ exist exactly when every $C_i=17(17-b_i)$ is a rational square. If $C_i=c_i^2$, then $s_i=c_i$ and $q_i=-4C_iD_i\tau/(\tau^2+3D_i)$ work simultaneously for every nonzero rational $\tau$. Realizing these square complements on actual guarded detector tuples is a stronger possible target. The theorem leaves open isolated rational common fibers and multisections when the complements are nonsquare.

The [early-scalar theorem](../papers/pole_parameters/square_complement_baseline_20261116_v43.tex) makes this square-complement route locally compatible with the actual general source. With the native $r$, $\ell=76249$ and fixed odd $L$, replace the early scalar by

$$\rho_* = \frac{102^2\ell^Lr}{(1+153\ell^Lr)^2}.$$

Its complement is a nonzero rational square, and the actual detector complements can be squares at any finite set of primes prescribed before preparation. The revised denominator case has $v_\ell(\rho_*)=|L-20m|$ for $m=-v_\ell(X)>0$; the paper supplies the necessary corrected height estimate. The source census is unchanged, with a sufficiently large ineffective fixed odd exponent. No new degree or coefficient record is assigned to the modified family. The remaining condition is a global rational square on actual detector tuples, not arbitrarily accurate local approximation.

Two separate obstructions delimit that condition. The [actual-neighborhood theorem](../negative_results/papers/pole_parameters/actual_square_complement_neighborhoods_20261116_v43.tex) produces original-source independent return families with nonsquare complements throughout a fixed 23-adic neighborhood. The [normalization counterexample](../negative_results/papers/pole_parameters/square_complement_normalization_20261116_v43.tex) shows why applying a square-complement normalization directly to the final detector inputs destroys the pole test. The early scalar is changed before the detector is formed and has its own soundness proof.

The [fixed-class synchronization theorem](../negative_results/papers/pole_parameters/fixed_class_synchronization_20261116_v43.tex) gives genus $1+2^r(r-1)$ for the common propagation curve when $r$ distinct positive pole scales and their twist classes are fixed. For two poles the genus is five, with an explicit $1+1+1+2$ Jacobian decomposition. Every fixed class tuple therefore gives only finitely many rational parameters. Infinitely many varying class tuples remain available. The full common-parameter variety has Kodaira dimension one when $r\ge2$, so direct Kummer-quotient theorems do not apply to it. The [literature audit](../negative_results/docs/fixed_fiber_literature_20261116_v43.md) also checks the relevant two-torsion, semistability and cohomological hypotheses; no theorem from Schinzel and finite Sha alone is claimed.

The [abelian-parameter obstruction](../negative_results/papers/rational_fibers/abelian_parameter_obstruction_20261116_v44.tex) excludes a uniform rational identity on an abelian parameter space when the detector argument varies nontrivially, even if every twist class may vary. It applies both to rational square complements and to the original normalized pole equations. The argument forces an odd contact divisor and a negative odd pole valuation. It does not cover an actual detector family at a fixed comparison slope, a ramified cover, or individually chosen rational points. Local return sets still supply the required preparation and guards, but cannot establish the rational incidence themselves.

At a fixed allowed slope with positive detector weight, the [fixed-argument ramification theorem](../negative_results/papers/rational_fibers/fixed_argument_complement_ramification_20261116_v44.tex) proves that the complement cover of the full independent auxiliary product is geometrically ramified. Therefore a surjective abelian coupling, including an isogeny or independent half-point doubling, cannot furnish a uniform square-complement section. The next targets are a proper coupled subvariety with a separate rational realization proof, or rational points directly on the ramified incidence cover. A common rational pole fiber without square complements remains a separate possible route. None of these obstructions proves nonexistence of the required individual actual detector tuples.

The [varying-input quadric theorem](../papers/pole_parameters/varying_input_quadric_20261116_v44.tex) gives a rational parameter space for compatible coefficient inputs at any fixed nonexceptional common conic parameter. For a pole scale \(D>0\) and \(e=(\tau^2-D)/(\tau^2+3D)\), the surface with input \(b=D/(17V^2)\) is birational to

$$x^2-Dy^2=e(\sigma^2+3D),\qquad V=\frac{\sigma x-Dy}{17(x-\sigma y)}.$$

The quadric has the explicit rational point \((\tau,1,\tau)\). The arithmetic target is to match this V with the native reciprocal trace while preserving the earlier source guards. This gives an exact incidence problem on which to try proper couplings or descent. The parametrization neither changes a final detector input by normalization nor proves that arbitrary actual tuples lift. Its explicit small-positive-input curve has square complement; its full two-parameter surface is the relevant broader family.

The [native doubled-source norm map](../papers/pole_parameters/doubled_source_congruent_twists_20261116_v43.tex) supplies a different arithmetic handle: it constructs a nonzero-ordinate rational point on a congruent-number twist with abscissa square class $[\operatorname{Tr}(x\bar d)/2]$. Its class has not been identified with a required detector class. A useful next step is either an exact class identity or a descent argument trivializing the prescribed isogeny-Selmer elements, not only proving positive rank on an unrelated twist.

This proposal shares the conic coordinate, not $e_i$ itself. Sharing $e$ requires matching input square classes; the separate [fresh-prime obstruction](../negative_results/papers/pole_parameters/fresh_prime_squareclass_obstruction_20261116_v42.tex) proves that the existing fresh-prime witnesses violate that requirement. The [common-twist theorem](../papers/pole_parameters/common_twists_20261114_v30.tex) gives genuine savings on its explicitly compatible locus, but does not put the full integer construction on that locus. A common $\tau$ allows different $e_i$ and avoids that particular necessary square-class equality. It still needs its own arithmetic existence proof.

A fixed value of $\tau$ does not supply this missing result. The [fixed-parameter obstruction](../negative_results/papers/pole_parameters/fixed_pole_parameters_20261109_v17.tex) gives prepared inputs excluding $\tau=\pm1$ and $\tau=\pm17$, including arbitrarily small prepared inputs in the latter case. The proposed shared parameter must remain variable unless a new restricted completeness theorem proves otherwise.

Those fixed-parameter counterexamples are global: their pole quartics are everywhere locally soluble by the preceding theorem. Their rank and square-class certificates do not constitute local obstructions.

### The stronger rational-complement target

The [native complement theorem](../papers/pole_parameters/guarded_complement_reduction_20261116_v45.tex) sharpens the payoff of the square-complement route. At an actual point-stage tuple every character lies in \(K=\mathbb Q(\sqrt2)\). Prepared inputs have the form \(b_i=w_iS_i^2\), with even \(v_{17}(w_i)\). Vanishing of a complement at any character would make \(w_i/17\) a square in \(K\), contradicting its odd valuation at 17. Thus the complement norm guards are automatic.

If actual simultaneous rational complements exist for every integer input, they themselves exclude the negative odd valuations needed by soundness. Both retained pole pairs can then be removed, giving the conditional counts **21 and 9**, with the existing one-coordinate encoder. This implication is proved; the native realization assertion is not. The **24-variable** common-fiber route remains a weaker sufficient target and does not require square complements. A global coupling with varying twist classes must prove one of these arithmetic incidence statements on the unmodified detector values.

The same theorem constructs infinitely many prepared free inputs at a fixed common pole parameter, including square reduced denominators and all preparation depths. The missing step remains equality with the actual reciprocal traces. Neither a rational parametrization of the free-input quadric nor finite local preparation proves that equality.

The [finite-class complement theorem](../papers/pole_parameters/finite_complement_classes_20261116_v46.tex) gives a weaker sufficient realization condition. Fix finite sets of levels 17m² and positive square classes supported on the source's original exceptional primes. For each actual input it suffices to make one allowed multiple of the corresponding complement a rational square. The complement norms are still units at every point-algebra character. Separate finite-algebra encodings followed by their product give the same 21/9 conditional census without a retained class-selection coordinate, even if branch radicands coincide.

At the single level 17, allowing all exceptional square classes means that both actual complements need only have even valuations outside the original exceptional set. No consumed prime may be moved into that set. Its actual uniform rational realization is still missing. The explicit nonsquare-class coefficient family in the paper does not establish native trace matching.

The [admissible-level theorem](../papers/pole_parameters/admissible_levels_native_traces_20261116_v47.tex) also permits finitely many fixed rational levels with nonnegative even valuations outside the exceptional set, provided every whole-algebra complement guard is proved. An exact native fixture at X=±1 and B=3 satisfies both prescribed-trace equations after fixed positive exceptional-unit rescalings, with all 128 guards checked. Its levels and rescalings are fixed constants; no completeness theorem for other inputs or sufficiently large defining B follows. The [polynomial-level local theorem](../papers/pole_parameters/polynomial_levels_local_20261116_v47.tex) supplies compensating test powers for levels cM(X)². Global realization and the corresponding height/completeness transfer are separate obligations.

The [norm-compatible scalar theorem](../papers/pole_parameters/norm_compatible_scalar_20261116_v47.tex) removes the bare norm-conic obstruction in a complete prepared family. Its degree-eight input map reflects integrality and makes all four finite height-contact factors norms from Q(√10657). The new general scalar preserves the forced odd valuation at 76249, local preparation, height contacts and 25-coordinate census. The conditional sources already have uniformly soluble bare norm conics under compatible prime preparation. The concrete remaining target in either setting is

$$ (m_j\operatorname{Tr}(\mathcal W_j^{-1}))^2-10657Y_j^2=4w_j/17,$$

with m_j from fixed finite admissible levels, the actual coupled detector data, and all guards. The free first coordinate of a conic point must not be substituted for the prescribed trace.

For the unchanged general scalar, the [signed finite-class theorem](../negative_results/papers/pole_parameters/finite_nonsquare_class_obstruction_20261116_v47.tex) excludes uniform realization using any finite collection consisting entirely of nontrivial square classes. Its three quartic contact fields and Chebotarev argument apply to every guarded rational auxiliary tuple, not only the prime-prepared family. Including the rational-square class or using the new norm-compatible scalar avoids this specific obstruction.

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

The present source carries labels through local approximations by elliptic formal-parameter ratios. Those rational ratios are not known to be the exact integral labels, so monicity at the ratios does not prove the needed integrality. This distinction has a concrete counterexample: $a=5,n=1$ gives discriminant $340$, which is not a rational square, but for every $r\ge1$ there are rational norm-one solutions with $0<n_r<1$ and $n_r\equiv1\pmod{19^r}$. The separate [rational Pell approximation obstruction](../negative_results/papers/integer_labels/rational_pell_approximation_obstruction_20261116_v42.tex) proves this by an explicit rational parametrization. A useful application must therefore recover an exact integer carrier, or prove a new global implication from the complete source equations. Arbitrarily precise local approximation alone does not close the gap.

### Dependencies among point roles

A replacement for the nine points need not realize every independent tuple of labels. That freedom is where a genuine reduction can occur. It must nevertheless give witnesses for every integer input and prove soundness on every rational solution of the new source.

Two established obstructions delimit direct substitutions:

- The [dimension and label-graph theorems](../negative_results/papers/elliptic_charts/structural_constraints_20261109_v13.tex) show that a finite algebraic presentation recovering arbitrary tuples of nine points needs at least eighteen rational parameters. The integer-index graph itself is Zariski dense in the product of the additive group and the relevant abelian variety.
- The [index-product theorem](../negative_results/papers/elliptic_charts/index_products_and_finite_correspondences_20261110_v21.tex) shows that a fixed correspondence with finite geometric fibers cannot recover $[nh]P$ from $[n]P,[h]P$ uniformly for infinitely many $n$ and infinitely many permitted $h$ for each $n$. Restricting each index to congruence classes does not remove this obstruction.

These statements concern generic recovery and the specified finite correspondences. They do not exclude a smaller arithmetic source whose witnesses satisfy additional dependencies, or one using a different integer-growth relation.

## The 74-variable detector and further quartic reductions

The [ordinary-abc construction](../papers/quartic_existence/quartic_abc74_20261116_v46.tex) uses **74 variables and 64 quadratic rows**. Put β=X/2, rescale the paired reciprocal coordinates by powers of β, and use the height scale B+β⁸+T². The complete five-field reference chart is retained. A normalized factor now has the form

$$1+C^2/w+(\beta^2 f(H)f(U))^2/w^2.$$

At a consumed prime, the three terms have distinct valuation classes. The complete ratio equations show that a positive product valuation with v(β)≤0 forces both reference and numerator into the formal group at the identity. This controls all torsion branches and gives the residual β(n−β), with strict height absorption **602/679**. Each factor is converted quadratically using the existing reciprocal squares; no stored w² coordinate is needed. The original trace is recovered exactly.

The physical pole input is b=w(N(W)/Tr(W))². The retained simultaneous-twist premise supplies rational pole witnesses for the actual prepared b>1 inputs. The source Gaussian congruences already make the order quotients annihilate the half-generator, giving completeness for odd and negative X. Zero weight is excluded automatically for X≠0; X=0 has an explicit degenerate scaled-point witness. Every square, height and nonzero constraint is included in the 74-coordinate total.

The [reference-cover theorem](../papers/elliptic_charts/reference_covers_20261116_v47.tex) gives an exact three-coordinate square-root cover and a polynomially isomorphic four-coordinate presentation. The latter makes both reciprocal abscissas linear; its input scaling, numerator product rows and ratio rows remain quadratic. Under the retained group premise the covered points are exactly 2E(K), so using that point restriction for every integer input requires an integral index relative to P, rather than silently retaining the half-generator convention. Its separate Jacobi chart recovers the original difference trace and identifies the complete zero-scale fiber.

The next concrete quartic target is the asymmetric pairing between the two differently scaled numerator points. It must encode their actual difference trace within the saved reference budget and account for every zero-reference, zero-ratio and zero-contact stratum. The reference and numerator blocks alone do not give a smaller complete source; the current complete bound remains 74.

The deeper comparison precision needed by the 195-variable construction is not supplied by this detector. A transfer there requires a new valuation argument or a different use of the integer-growth relation. Its variable reduction must be justified separately from the input-preserving affine–Laurent elimination used in the 195-variable family.

### Further elimination from the 195- and 257-variable systems

The [current quartic](../papers/quartic/quartic195_20261116_v45.tex) centers the Lucas expression before rescaling by a guarded unit. The affine change removes constant and cross terms that previously required an inverse-weight square coordinate. Its complete certificate includes every source row, the retained inverse guard and the fixed input. A further reduction must provide the same full-system equivalence or a new soundness and completeness proof. Joint use of the detector units and scalar-normalizer unit is a precise algebraic direction; a favorable count for an isolated block is insufficient.

The [257-variable explicit construction](../papers/quartic/quartic257_20261116_v45.tex) applies an affine centering using an existing inverse coordinate. Its complete rational zero-set equivalence preserves the sufficient parameter N=9682 and gives exact height $149^{19366}$. A further algebraic saving from either family must retain its inverse guards or prove soundness on every additional boundary.

### Propagating the three-coordinate chart


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

The [quadratic reference and height theorem](../papers/elliptic_charts/scaled_reference_height_20261116_v43.tex) propagates the chart through the paired points and the original trace. Set $\lambda=v^{-1}$, $J=\lambda^2$, $\alpha=\lambda S$ and retain $\kappa=J^2$. The reference reciprocal abscissas are linear, and weighted rescaling makes the point, difference and ratio equations quadratic. One additional rational coordinate recovers the original trace of the fixed difference; it does not replace that trace by a reference-dependent height.

The reference, pair, ratio and trace blocks decrease from 33 to 32 rational coordinates on $\lambda\ne0$. The exact quadratic guard $\kappa_0\zeta=1$ costs one rational coordinate and restores the total to **33**. The zero-scale boundary admits degenerate scaled solutions, so its exclusion needs proof or this counted guard. Conversion of every physical detector factor still needs a complete quadratic construction. The [current guide](common_fibers_and_reference_charts_20261116_v43.md) gives the full block table.

The separate [mixed-reference-sign theorem](../negative_results/papers/elliptic_charts/mixed_reference_signs_20261116_v42.tex) shows that the reference chart and membership in $2E(K)$ alone do not force the two torsion-translation signs to agree. The [shared-reference test theorem](../negative_results/papers/elliptic_charts/shared_reference_test_obstructions_20261116_v43.tex) also gives exact local cancellations for the proposed squared test and its whole-factor odd-cube repairs. In the latter case the comparison slope can have positive valuation while its error from the target remains a unit. These are obstructions to the stated local test implications, not false solutions of a complete source.

The [duplication sign obstruction](../negative_results/papers/elliptic_charts/duplicated_reference_signs_20261116_v44.tex) shows that replacing the local parameter by its doubled-point version does not remove every sign branch. At the valid contact prime 76537, an allowed half-integral reference progression simultaneously enters a formal neighborhood at one embedding and an order-four neighborhood at the other. Duplication sends the latter to a two-torsion branch and reverses the formal-parameter sign. The quartic permits the full source group, so restricting this check to integral multiples of the doubled generator would omit allowed soundness tuples.

The weighted-product test now handles every torsion branch with the complete reference chart. Propagating it through the three-coordinate chart remains a separate task. Its integration must include detector powers, the original height trace, all auxiliary squares, and every nonzero condition. A further quartic saving requires soundness on every rational solution, including any added chart boundary.

The complete ratio equations also imply the paired curve equations whenever the two reference ratios do not vanish together. The fixed translating point is not two-torsion, which supplies that nonvanishing on the entire reference chart. This redundancy is used in the [176-row, 196-variable construction](../papers/quartic/quartic196_redundancy_20261115_v40.tex) and the current 64-row, 74-variable abc construction. The [primitive quadratic bases](../papers/quartic/primitive_quadratic_bases_20261115_v40.tex) lower coefficient heights by exact invertible rational row changes and specified constant coordinate scalings. Deleting redundant rows or changing their basis alone does not lower the number of variables; the present 74-variable count also uses the weighted-product detector, input rescaling and pole realization above.

### Height budgets for further reference compression

The [mixed-power height theorem](../papers/elliptic_heights/mixed_power_height_20261116_v45.tex) applies to several possible target choices. For the current β=X/2 target and scale a=B+β⁸+T² it gives

$$h(\beta)\le\frac{301}{388}h(a)+O(1),\qquad h(T)\le\frac{301}{97}h(a)+O(1).$$

The quadratic residual β(n−β) then has strict absorption **602/679** under the ordinary-abc eight-contact estimate. This is sufficient with two input-power coordinates. A modified detector that leaves a higher-degree residual must recalculate this budget and include any extra power coordinates in its count. Height absorption alone never supplies a missing rational completeness theorem or a quadratic conversion.

## Arithmetic and coefficient obligations

Smaller pole equations need a complete realization theorem. The [conic-chain classification](../negative_results/papers/pole_parameters/conic_chain_obstruction_20261115_v41.tex) proves that the quadratic family

$$P=p^2,\qquad e^2+bP=1,\qquad D=1+(cb-1)P,\qquad z^2=bD$$

fails on arbitrarily small prepared inputs for **every fixed rational coefficient $c$**. Its four-auxiliary specialization at $c=0$ and five-auxiliary member at $c=1$ already have explicit local obstructions at 29 and 5. This is not a lower bound for other pole models.

Making the first conic automatic also leaves a substantive global problem. The identity $b=(1-e^2)r^2$, $p=1/r$ gives $e^2+bp^2=1$. The [automatic-conic obstruction](../negative_results/papers/pole_parameters/automatic_conic_obstruction_20261115_v41.tex) proves failure of the remaining congruent-pole equations on dense prepared families, even for the fully split six-contact formula at $e=20/343$. Its noncongruence certificate uses Tunnell's unconditional necessary direction. A viable version of this approach must control the multiplier values actually produced by the detector and prove the remaining rational realization on that restricted set.

A shared pole parameter preserves two separate parity tests. Replacing them by a single rational test is a different proposal and encounters stronger restrictions. The [product-height counterfamilies](../negative_results/papers/pole_parameters/product_height_obstructions_20261110_v19.tex) show that the product of two contact functions can have trivial odd radical while the scale is large. The [local rational-combination theorem](../negative_results/papers/pole_parameters/rational_combinations_of_contacts_20261110_v20.tex) excludes every fixed rational parity combination for its specified source family. These are obstructions to the stated implications, not to all single-pole constructions.

Forcing equality of the two contact square classes can prove soundness, but rational completeness becomes a separate problem. At a fixed comparison scale, the [quadratic contact cover](../negative_results/papers/pole_parameters/quadratic_contact_covers_20261110_v21.tex) has genus four. Allowing both ordered contact arguments to vary gives the [ordered square-class surface](../negative_results/papers/pole_parameters/ordered_squareclass_surface_20261115_v33.tex), which is of general type. It has neither a dominant rational parametrization nor a fibration with rational or genus-one general fiber. These facts leave open special arithmetic families of witnesses; they exclude the corresponding unrestricted parametrization strategies.

For effective coefficients in the few-variable construction, the unresolved analytic issue is a uniform effective trace-height estimate on the relevant integer-index tuples. The [explicit construction](../papers/few_variables27/explicit27_20261110_v19.tex) uses both rational components and a third pole predicate to avoid that issue. Positivity on selected completeness witnesses cannot replace a height bound needed for every soundness tuple.

For quartic coefficient optimization, invertible rational combinations of quadratic rows preserve the rational zero set, and invertible coordinate rescalings give a bijection of zero sets. Each proposed change must be followed by primitive integer normalization and exact collection of the squared rows. A height claim for a parameter family needs a bound for every allowed parameter, together with a coefficient that attains it; one small test member does not establish that claim. The current [affine–Laurent coefficient theorem](../papers/quartic/quartic195_20261116_v45.tex) gives

$$
H(P_N)=\max\{126616122944180358034867798936,\;149^{2N+2}\}
$$

for the 195-variable family, and

$$
H(Q_B)=\max\{20828275368498373068800,\;B^2+275933278576697091\}
$$

for the [74-variable ordinary-abc family](../papers/quartic_existence/quartic_abc74_20261116_v46.tex). Exact expansion proves these height formulas for the stated parameter ranges. A sufficient defining parameter in each ineffective family still depends on the explicitly retained arithmetic premises.

The [lower-bound results](../negative_results/papers/lower_bounds/lower_bounds_20261109_v15.tex) require degree at least four for a single defining equation and at least five total coordinates for a globally nonnegative quartic or a quadratic system. They supply no lower bound near the current counts.

## Rings of integers of number fields

No counterexample to $\mathcal O_K$ being Diophantine in its fraction field $K$ has been established. The [number-field reductions](../papers/number_fields/number_field_definability_20261109_v12.tex) give three useful formulations:

1. $\mathcal O_K$ is Diophantine in $K$ if and only if $\mathbb Z$ is Diophantine in $K$, using the cited theorem defining $\mathbb Z$ inside $\mathcal O_K$.
2. Assuming a definition of $\mathbb Z$ in $\mathbb Q$, these are equivalent to the rational subfield $\mathbb Q$ being Diophantine in $K$.
3. A counterexample persists through every finite extension. Hence one could pass to a totally imaginary Galois extension when searching for a counterexample.

A failure after extending the witnesses of a particular polynomial is a failure of that polynomial. It does not establish the third assertion's counterexample hypothesis. The separate [unchanged-formula obstruction](../negative_results/papers/number_fields/unchanged_formula_obstruction_20261116_v42.tex) proves that no fixed finite collection of formulas can work unchanged throughout all finite extensions; field-dependent constructions remain possible.

The specified $j=1728$ elliptic curve cannot be transferred unchanged across adjoining $i$. The [complex-multiplication theorem](../negative_results/papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.tex) proves exact rank doubling and constructs an infinite cyclic subgroup with zero abscissa trace and unbounded heights. It also supplies distinct doubled points with zero abscissa sum. A number-field construction must use another curve or prove a height statement that controls these cancellation directions.

Rank stability is useful but does not itself define the rational subfield: it supplies an infinite Diophantine subset of rational abscissas, which can remain arithmetically sparse. Likewise, writing a norm or trace in base-field coordinates does not force unrestricted extension-field variables to lie in the base field. The [norm-and-trace equivalences](../papers/number_fields/number_field_definability_20261109_v12.tex), Section 4, identify that missing restriction explicitly.

One sufficient positive target is a Diophantine set $T\subset K$ containing every rational integer and having uniformly bounded integral denominators. Indeed, for an integral basis $\omega_1,\ldots,\omega_n$, the set $S=\sum_i\omega_iT$ contains $\mathcal O_K$ and satisfies $MS\subseteq\mathcal O_K$ for some positive integer $M$. A finite union of translates of $MS$ by representatives of $\mathcal O_K/M\mathcal O_K$ then equals $\mathcal O_K$. The [finite-correspondence and denominator theorems](../negative_results/papers/number_fields/finite_correspondences_and_denominators_20261109_v14.tex) exclude several routes to such a set, including quasi-finite covers of abelian varieties and their stated low-genus extensions. A successful construction must avoid those hypotheses or use exceptional positive-dimensional fibers with a proved arithmetic completeness argument.

The decisive goals are therefore a complete shared-parameter pole realization, a globally quadratic propagation of the three-coordinate chart, an exact integral carrier for the Pell compression, or a new number-field denominator mechanism. Each would change an actual arithmetic dependency rather than only the presentation of an existing formula.
