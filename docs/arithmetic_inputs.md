# Arithmetic inputs, theorem scope, and effectiveness

The construction theorems identify rational input projections with $\mathbb Z$ under explicitly stated arithmetic inputs. All variable counts include the input. A certified coefficient specification is distinguished from a certified sufficient choice of its fixed coefficient parameter.

| Construction | Variables | Degree | Number of monomials | Sufficient coefficient parameter |
|:--|--:|:--|:--|:--|
| [Few-variable family](../papers/few_variables25/few_variables25_merged_20261110_v19.pdf) | 25 | $\le20747108969426225455955968<2^{85}$ | Upper bound $<2^{1979}$ | Every sufficiently large odd $L$; ineffective threshold |
| [Fully specified polynomial](../papers/few_variables27/explicit27_20261110_v19.pdf) | 27 | $\le85829362869408651982929920<2^{87}$ | Upper bound $<2^{2192}$ | Every odd $L\ge20483$ |
| [Quartic family](../papers/quartic_existence/quartic226_20261110_v21.pdf) | 226 | Exactly 4 | Exactly 2,835 | Every sufficiently large $N$; ineffective threshold |
| [Fully specified quartic](../papers/quartic/quartic262_20261110_v21.pdf) | 262 | Exactly 4 | Exactly 3,494 | Every integer $N\ge9682$ |
| [Weak-abc family](../papers/conditional_few_variables/conditional13_20261109_v16.pdf) | 13 | $\le12339485119488<2^{44}$ | Upper bound $<2^{509}$ | Every sufficiently large odd $B$; ineffective threshold |
| [Ordinary-abc quartic](../papers/quartic_existence/quartic_abc87_20261110_v21.pdf) | 87 | Exactly 4 | Exactly 918 | Every sufficiently large odd $B$; ineffective threshold |

The first four constructions use the full normalized modular realization specified below and add no abc or Szpiro hypothesis. The thirteen-variable theorem assumes one weak abc inequality, or ordinary Szpiro through the proved implication. The eighty-seven-variable theorem assumes ordinary rational abc. All six retain the applicable elliptic, pole, and simultaneous prime-pattern inputs.

## The inherited arithmetic inputs

The [arithmetic-dependency paper](../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) gives the exact quantified statements derived from the pinned source and Sun's Theorem 4.1. It checks simultaneous congruences, fixed odd-prime avoidance, the special case of seven, real approximation, and the zero-preparation case of pole realization.

| Input | Mathematical content used | Role of finite verification |
|:--|:--|:--|
| Elliptic group and index height | For the specified curve over $K=\mathbb Q(\sqrt2)$ and point $P$, $2E(K)=\mathbb ZP$ and $h(x([n]P))\ge n^2-6$ for every nonzero integer $n$. | Point identities, local constants, and relevant finite-field counts are checked. These checks do not by themselves establish the full group or global height statement. |
| Normalized modular realization | The compatible representation, coefficient character, conductor, and restricted-trace properties specified in the [differential-evaluation paper](../papers/contact_heights/evaluation_of_differentials_20261109_v17.pdf) and [multiplicity theorem](../papers/contact_heights/multiplicity_and_contact_heights_20261110_v19.pdf). | Exact arithmetic certifies the constants in the resulting contact-height inequalities. The normalized arithmetic realization remains an explicit premise. |
| Pole obstruction and realization | The pole equations exclude negative odd valuations outside $2,3,17$ and admit witnesses for the stated positive inputs with square reduced denominator and the required local squareclasses and depths. | Coordinate identities and domains are checked. The restricted-converse and descent inputs give the nonzero witnesses used by the finite charts. |
| Simultaneous prime patterns | Prescribed prime values, Gaussian congruences, fixed avoidance and divisibility, conjugate reduction orders, and compatible real approximation are available together. | The dependency paper derives the required form from the pinned prime-pattern and reduction-order results. Finite computations check local congruences and order identities. |

The modular input is stronger information than a single numerical contact-height inequality. The leading twenty-five-, twenty-seven-, 226-, and 262-variable theorems use its full normalized form. Their sharper height bounds are proved consequences of that form. The thirteen- and eighty-seven-variable constructions instead use logarithmic bounds obtained from their stated additional height hypotheses.

The fixed prime and every finite exceptional set are chosen before applying the prime-pattern theorem. Enlarging a fixed coefficient changes only divisibility and avoidance conditions that are likewise fixed before the subsequent prime selection.

## Modular multiplicity and contact height

For a reduced rational number $a=u/v$, with $v>0$, let $M_5(a)$ be the product of primes $p>76176$ having positive odd valuation in at least one of

$$
v,\quad u,\quad u-v,\quad u-2401v,\quad32u+343v.
$$

The rational number avoids the four finite contacts $0,1,2401,-343/32$. Put

$$
B_*=\prod_{p\le76176}p,\qquad C_0=210^{300},\qquad
\mathcal E(R)=\prod_{p\mid R}(1+1/p).
$$

The [multiplicity theorem, Theorem 4.1](../papers/contact_heights/multiplicity_and_contact_heights_20261110_v19.pdf) proves

$$
h(a)\le67C_0(B_*M_5(a))^2\mathcal E(B_*M_5(a))\log(B_*M_5(a)).
$$

In particular, with $C_2=67C_0B_*^2\mathcal E(B_*)\log B_*$,

$$
h(a)\le C_2M_5(a)^2(1+\log M_5(a))^2,
\qquad C_2<2^{221231},
$$

and

$$
h(a)<2^{221234}M_5(a)^{7/3}.
$$

For every $\eta>0$, an effective constant also gives exponent $2+\eta$. These bounds hold without a restriction on the two-primary parts of the contact primes minus one.

The proof uses the rational half-traces after restriction to the auxiliary field. All coefficient conjugates yield the same restricted factor, so the modular abelian variety is isogenous to a power of the fixed abelian surface. Its multiplicity is at least one quarter of the coefficient-character order. Dividing the modular Jacobian height among these factors and applying the fixed-dimensional isogeny estimate cancels that character-order contribution. The separate [scalar-character lemma](../papers/contact_heights/nebentypus_and_contact_heights_20261110_v18.pdf), including $(\varepsilon\chi)^2=1$ and the minimal-order character construction, supplies part of this argument.

Two disjoint five-contact blocks turn exponent $7/3$ into $7/6$: their odd contact radicals are coprime outside a fixed exceptional set, and multiplying their two height inequalities bounds the square of the argument height. All extra exceptional primes are explicitly included in the construction's constants.

## Prime selection and complete witnesses

The [prime-selection paper](../papers/prime_selection/prime_selection_20261109_v12.pdf) derives the separation and denominator conditions from [Sun, arXiv:2610.20691v2](https://arxiv.org/abs/2610.20691v2), Propositions 5.1 and 6.2 and Section 6.1. For fixed coefficients, the patterns have the form $p_j=u+c_jw^2$, with $X/2\le u\le X$ and $1\le w\le\tau(X)\sqrt X$.

The cited weighted estimates retain a positive proportion after the reduction-order obstructions are removed. Excluding $w<X^\alpha$, for fixed $1/4<\alpha<1/2$, costs negligible weight and makes distinct prime values farther apart than the Hasse-sized order errors. The permitted slow choice of $\tau$ simultaneously keeps the selected primes in a narrow relative interval. The denominator dilation and all finite congruence conditions are fixed before selection.

The raw-comparison, linear-scalar normalization in the twenty-five- and twenty-seven-variable papers additionally requires the common elliptic index $h$ to be divisible by each selected comparison prime. The clustered-prime and Hasse argument proves that those primes divide none of the prescribed opposite reduction orders. These extra congruences are therefore compatible with the existing index progression. The fixed real component is preserved under compatible refinements. This is a consequence of the retained prime-pattern input, not a new conjecture.

The [nonzero-witness paper](../papers/pole_parameters/pole_witness_density_20261109_v14.pdf) records the restricted-converse and descent assumptions that supply witnesses outside two-torsion. Bare pole solvability would not imply their nonzero ordinates. The nonzero witnesses justify the single-conic charts in the few-variable constructions and the normalized pole coordinates in the additional-abc quartic.

## Twenty-five variables with raw comparison functions

The [twenty-five-variable theorem](../papers/few_variables25/few_variables25_merged_20261110_v19.pdf) uses two pole predicates that impose both scalar divisibility and elliptic comparisons. Its ten reciprocal-abscissa functions and its two input comparisons enter directly at order one. The three Lucas-label comparisons and the Lucas residual enter at order three. The first four scalar components need only positive valuation, while the two logarithm-ratio components retain the deeper bound. The scalar functions use the linear rational normalization

$$
\Phi_R(D)=\frac{RD}{1+RD},
$$

with all denominator guards retained. Formal precision four requires only the plain local parameter $z=-x/y$. The additional divisibility of $h$ just described supplies the deeper primary neighborhood needed for these linear scalar denominators at the newly selected primes.

Every scalar/comparison parity case is included. The two comparison radicals satisfy $M_j^3\mid\Delta c$ for a nonzero Lucas residual, and $M_j\mid(u-nv)c$ for a nonzero input residual, where $c=|a-1|$ is the scalar index. The scalar height is $h(\beta)=O(c^{7/9})$, and the forced prime gives

$$
c\ge76249^{2L+1}.
$$

For the Lucas residual, the contact bound gives a term $|\Delta c|^{7/18}$ and growth exponent $35/18<2$ in the maximum elliptic index. For the input residual it gives $|(u-nv)c|^{7/6}$. Keeping $c$ separate in $|(u-nv)c|\le2e^{h(\beta)}Bc$ yields a bound for $\log B$ by a constant multiple of $h(\beta)+\log c+1$. Lucas growth contradicts this bound because $c^{7/9}=o(c)$. Primes shared by the scalar and comparison supports are included throughout.

There are 24 retained rational coordinates: the input, eighteen coordinates for nine elliptic points, one nonzero comparison slope, and four pole parameters. Nine finite quartic roots and two finite quadratic roots are removed by guarded finite-algebra elimination using one additional rational coordinate. The exact degree bound is $20747108969426225455955968<2^{85}$; the support bound is $<2^{1979}$. The [source and bound certificates](../computation/few_variables/merged25_v19/README.md) are uniform in the fixed odd coefficient exponent. The supplied $L=3$ fixture is not certified to define $\mathbb Z$.

## Effective and ineffective height comparisons

The [aggregate trace-height theorem](../papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) proves a uniform comparison between the sum of canonical heights of finitely many nonzero multiples of the specified point and the height of their rational trace. Its geometric argument excludes positive-dimensional abelian translates, including those defined over the algebraic closure, from a constant trace fiber. It then applies [von Buhren, Theorem 1.1](https://www.numdam.org/item/10.5802/jtnb.981.pdf) to a fixed graph and finite-rank subgroup.

The additive constant in this proved theorem is ineffective here. This is why the twenty-five- and 226-variable families have no numerical sufficient coefficient parameter. The one-point version is also used in the thirteen- and eighty-seven-variable theorems. Their additional abc constants are ineffective as well. None of these fixed coefficients becomes a quantified variable.

For four positive elliptic abscissas, the [effective sum-height theorem](../papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf) instead gives

$$
B^2\le2h(\mathcal S)+80
 \le2h(S_0)+2h(S_0+S_1)+82,
\qquad \mathcal S=S_0+S_1\sqrt2,
$$

using the retained index-height lower bound. For the second inequality write $\mathcal S=(1-\sqrt2)S_0+\sqrt2(S_0+S_1)$; the product of the two archimedean coefficient sums is seven. Thus the extra height cost is at most $\log7<2$.

The [fully specified twenty-seven-variable construction](../papers/few_variables27/explicit27_20261110_v19.pdf) uses three comparison scales

$$
1,\quad(1+\rho S_0^2)^2,\quad(1+\rho(S_0+S_1)^2)^2
$$

and three common scalar/comparison pole predicates. Here $\rho$ is its rational scalar normalizer, rather than the notation for $\sqrt2$ used in some other papers. Its complete exceptional set, effective common height constant, and threshold inequalities are checked in the [constant certificate](../computation/few_variables/effective27_v19/effective27-constants-certificate.json). Every odd $L\ge20483$ suffices. The selected member has degree at most $85829362869408651982929920<2^{87}$, support $<2^{2192}$, and coefficient height $<2^{2^{99}}$, as certified by the [independent bound check](../computation/few_variables/effective27_v19/independent-bound-verification.json). The finite specification is not expanded, so these degree and support statements are upper bounds.

## The quartics in 226 and 262 variables

The [226-variable family](../papers/quartic_existence/quartic226_20261110_v21.pdf) uses two reflected five-contact blocks, whose only extra exceptional prime above $76176$ is $2029147$. With $H_2=2^{221284}$, its ten-contact height bound is

$$
h(t)\le H_2M_{10}(t)^{7/6}.
$$

The balanced contact function is $R=F_{10}(t)/(t-1)^{10}$ and $q=R^{-1}-1$. Five factors encode sixteen tests. Fifth-power weights give comparison order three, while even reciprocal-abscissa valuations keep every negative term in a distinct valuation class. In the factor with two odd-valued terms, the exponents five and three give the distinct residues $-\nu$ and $\nu$ modulo four. Integrality of the full ratios is proved before the formal-logarithm errors are used as congruences.

Each factor equation is multiplied by $q^{-4}$. Three scalar coordinates, specified by $qs_1=1$, $s_2=s_1^2$, and $s_4=s_2^2$, store the necessary inverse weights. Every numerator fourth power then occurs directly as the square of an already stored field square. This removes five field outputs, or ten rational coordinates. The equations exclude $q=0$; complete witnesses already have a selected contact prime with $v_p(q)=-1$. The remaining $t=1$ stratum has contact radical one and requires no interpretation of $R$.

The scalar normalization gives

$$
149^{L_N}M_5(\beta)^3\mid c,
\qquad L_N=\left\lfloor\frac{19(2N-1)}8\right\rfloor+1,
\qquad\beta=51X^2+2504.
$$

Consequently $h(\beta)\le2^{221234}(c/149^{L_N})^{7/9}$. The nonzero Lucas residual would give growth exponent $14/9<2$; the input residual then contradicts Lucas growth. The aggregate trace constant makes the sufficient $N$ ineffective. The quartic is the sum of 200 primitive quadratic squares and has 2,835 monomials. Its coefficient height is exactly $149^{4N+2}+1$ for $N\ge53$; this coefficient-height threshold is distinct from a sufficient defining threshold.

The [262-variable quartic](../papers/quartic/quartic262_20261110_v21.pdf) uses four factors and the three effective scales $1,S_0^2,(S_0+S_1)^2$. Four shared fourth powers of the deep comparison tests and one additional scalar fifth-power weight per detector permit four factors to encode all sixteen tests. Their valuation classes are $-\nu,\nu,2$ modulo four and four modulo eight. Deep comparisons still have order three, and both input comparisons need order one. Its height transfer is

$$
B^2\le5K_2|J|^{1/k}\left(22+\frac{\log|J|}{2k}\right)^2,
\qquad K_2=2^{221274}.
$$

when each comparison radical divides the nonzero integer $J$ to order $k$. For the order-three Lucas residual, the exact integer inequality in the logarithmic threshold certificate gives $B<2^{331969}$ unless the residual vanishes. Exact integer comparison proves that $N\ge9682$ excludes that case and then excludes a nonintegral input. At $N=9682$, the fixed coefficient is $A=149^{19365}$ and the coefficient height is exactly $149^{38730}+1$, with 279,599 binary digits. There are 234 primitive quadratic rows and 3,494 quartic monomials. The theorem uses no ineffective aggregate constant. [Exact tables and independent reconstruction](../computation/quartic/family262_v21/independent-verification262-v21.json) certify the stated finite assertions.

## Point charts, input maps, and exceptional strata

The [square-abscissa theorem](../papers/square_abscissa/square_abscissa_charts_20261108_v9.pdf) proves that $x=h^2$, $j^2=h^4-(3-\sqrt2)^2$, $y=hj$ describes the nonzero multiples of $P$, under the stated group input. The [quadratic square-root chart](../papers/quadratic_squares/quadratic_square_chart_20261108_v9.pdf) gives one finite quartic root for $j$; its completeness and nonvanishing are elementary and do not require a rank computation.

The [fixed-difference chart](../papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf) is an unconditional algebraic theorem. For $E:y^2=x^3-Dx$ and $P=(a,b)$ satisfying $abD(D^2+6a^2D-3a^4)\ne0$, three quadrics in four field coordinates describe exactly the allowed pairs $H,H-P$. A polynomial elimination identity covers vanishing leading coefficients. The rational component row change has nonzero determinant $-1/362963666515968$ and preserves the zero set. This chart is shared by the three leading quartics.

The 25- and 27-variable families use $\beta=216X^4+450459$: integrality for a reduced $X=u/v$ forces $v^4\mid216=2^3 3^3$, hence $v=1$. The 226- and 262-variable quartics use $51X^2+2504$, giving $v^2\mid51$. The thirteen- and eighty-seven-variable constructions use $2X^2+B$, giving $v^2\mid2$. In each case the arithmetic comparison recovers integrality of the original input exactly.

## The thirteen-variable theorem from weak abc

The [thirteen-variable family](../papers/conditional_few_variables/conditional13_20261109_v16.pdf) assumes only one weak rational abc inequality with exponent $\kappa=121/100$, together with the specified elliptic group, pole obstruction and nonzero realization, and simultaneous prime patterns. Applying this inequality to

$$
\varphi(z)=\frac{z(z+2)^3}{(2z+1)^3},\qquad
\varphi(z)-1=\frac{(z-1)^3(z+1)}{(2z+1)^3}
$$

and changing coordinates by $z=2+1/t$ gives six finite rational contacts and

$$
h(t)\le\frac{121}{74}\log M(t)+C_0.
$$

The primitive common-denominator calculation gives the projective estimate

$$
h(1:u:v)\le\frac{121}{437}h(u^8+v^8)+C_1.
$$

The scales are $1$ and $\beta^8+T^8$, where $T$ is the trace of the abscissa of one elliptic multiple. No square condition on the latter scale is needed: its sixth-power prefactor in the contact product is a square. All six local tests have order one. If $\beta\ne n$, their odd contact radicals divide the positive numerator $N$ of $\beta-n$, and

$$
h(1:\beta:T)\le\frac{14641}{16169}\log N+C.
$$

This coefficient is less than one. Since $\log N\le h(\beta)+\log(1+|n|)$, the inequality and the one-point trace-height theorem bound $n$ and the input height independently of $B$. Every sufficiently large fixed odd shift excludes this case. There are three point pairs, two independent pole pairs, one slope and the input; finite-root elimination adds one coordinate, giving thirteen in total.

The exact source and bound certificates in [the weak-abc module](../computation/few_variables/weak_abc13/README.md) give uniform degree at most 12,339,485,119,488, strictly below $2^{44}$. Its 64-factor polynomial specification has not been expanded. The shift-three coefficient-height check does not determine a sufficient defining shift.

More generally, every one weak exponent $1<\kappa<4/3$ suffices after choosing an even $d$ with $(8/\kappa-6)(d/\kappa-3)>2$ and using $\beta^d+T^d$. The same thirteen-coordinate count holds. The supplied numerical degree certificate concerns only $\kappa=121/100,d=8$.

## The additional-abc quartic

The [eighty-seven-variable family](../papers/quartic_existence/quartic_abc87_20261110_v21.pdf) uses ordinary rational abc and the eight contacts $\{-5,-2,-1,0,2,3,4,7\}$. Granville's squarefree binary-form estimate gives $h(t)\le\frac13\log M(t)+C_0$. A second abc consequence gives $h(1:u:v)\le\frac43h(u^4+v^4)+C_1$. The scales $1$ and $\beta^4+T^4$ therefore give strict absorption coefficient $8/9$.

The exact point chart includes identity numerator points. A height argument excludes the exceptional torsion translates of the common reference point before interpreting any removed denominator. The local tests establish integrality before applying formal-logarithm congruences. Completeness permits arbitrary positive rational scales because the eighth-power scale prefactor is a square.

The squared contact distances from the center are $1,4,9,36$. With $r=(t-1)^2$ and $z=r+36/r$, the identity

$$\frac{(r-1)(r-4)(r-9)(r-36)}{r^2}=z^2-50z+481$$

gives two contact outputs per detector. In the affine coordinates $R=r-1$ and $Z=z-37$, their equations are

$$R=t^2-2t,\qquad RZ+Z-R^2+35R=0,$$
$$ (R+1)s=Z^2+24Z,\qquad s_2=s^2,\qquad s_3=ss_2.$$

The first contact identity excludes $r=0$. If $s=0$, the factor equations force both numerator reciprocal squares to vanish; the unchanged point-pair equations then give a contradiction. Thus all inverse weights have their intended values. The scaled factors $A_i=sT_i$, product $\Omega$, and trace $\eta$ satisfy $(R+1)\Omega=A_1A_2$ and $s_3b=\eta^2$. The local proof uses the recovered unscaled product and trace. The changed degree-eight contact set preserves the required local valuation classes, square-denominator identity, fixed-place preparation, and simultaneous prime construction. Only the ineffective height constant and sufficient defining shift can change.

The source has 87 total coordinates and 75 primitive quadratic equations. Their sum of squares has exact degree four, content one, and 918 monomials. The input-comparison coordinate makes $B$ occur in one row only. For every integer $B\ge3$,

$$
H(P_B)=\max(4153456,B^2+797681).
$$

No numerical sufficient odd defining shift is certified. The [complete tables and independent check](../computation/quartic/family_abc87_v21/independent-verification-abc87-v21.json) reconstruct every reciprocal factor, retained row, and quartic coefficient. Ordinary rational abc is the stated hypothesis; the weak-abc/Szpiro premise of the separate thirteen-variable theorem is not asserted sufficient here.

## Other conjectures and proved obstructions

The [arithmetic-hypotheses paper](../papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf) proves that ordinary discriminant--conductor Szpiro implies weak abc with every exponent $6/5+\epsilon$; $\epsilon=1/100$ supplies the thirteen-variable theorem. Modified Szpiro and the stated truncated Vojta conjecture imply ordinary abc. None of these implications removes the retained elliptic or pole-realization premises. No coordinate reduction is derived from RH, GRH, or Grimm's conjecture. Mazur's connected-component conjecture would exclude an existential integer projection and cannot be combined consistently with premises that already yield one.

The [restricted-abc paper](../papers/restricted_abc/restricted_abc_inputs_20261109_v17.pdf) checks the small-$j$-denominator and asymmetric-size hypotheses on the actual scalar families. Those hypotheses fail along the exhibited unbounded families, so the cited unconditional results do not currently give the required logarithmic contact estimate. The statements concern those applications, rather than all possible uses of the results.

The [fixed-pole-parameter theorem](../papers/pole_parameters/fixed_pole_parameters_20261109_v17.pdf) and [combined-pole obstruction](../papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf) rule out their specified constant-parameter and product constructions. The [six-contact product-height theorem](../papers/pole_parameters/product_height_obstructions_20261110_v19.pdf) gives exact involutions and an elliptic family for which the product odd radical stays bounded while the multiplicative scale has unbounded height, including positive-domain variants. These are counterexamples to the proposed height inequalities. They do not assert that every auxiliary elliptic or pole equation in a defining construction is satisfied, and they do not give a lower bound for every possible pole certificate.

## Number fields and independent algebraic results

The [number-field reductions](../papers/number_fields/number_field_definability_20261109_v12.pdf) use Alpöge--Bhargava--Ho--Shnidman, Corollary 1.2, that $\mathbb Z$ is Diophantine in the ring of integers of every number field. Integral witnesses in that theorem are not replaced by unrestricted field witnesses. Equivalence with defining the rational subfield additionally assumes a definition of $\mathbb Z$ in $\mathbb Q$. The other elementary reduction and descent statements have their stated separate hypotheses.

The [elliptic-ratio examples](../papers/number_fields/elliptic_ratios_and_integrality_20261109_v13.pdf) give proper subsets over eight quadratic fields using unconditional upper and lower Mordell--Weil rank bounds and exact torsion calculations. Their optional PARI check uses neither analytic rank nor BSD. The local witnesses and the global exclusion of $-1$ concern that particular polynomial. The [finite-correspondence and denominator results](../papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf) and the restricted quadratic-input obstruction also concern their specified constructions. None supplies a counterexample to existential definability of an entire ring of integers in its fraction field.

The equation-combination theorem, guarded finite-algebra elimination, degree and coordinate lower bounds, point-chart identities, formal-logarithm estimates, square predicates, and the stated field-extension obstructions are independent results with the hypotheses of their own papers. The number-field trace-height corollary requires its explicit independence assumptions and does not itself define a ring of integers.

## Provenance and the meaning of a certificate

The foundational coefficient source is Version 9 at commit `14e8f601fe0d9173d4a5f084aedc3e07066a7688`; the arithmetic interpretation incorporates the Version 11 Kato index-set and retained-class correction at commit `650b298a2a18fa956f8859f3ca80e9d7c8cedd82`. The baseline quartic source is Version 13 at commit `5bbd74f6a479776a332cbe036809d5dddae63720`. Sun's prime-pattern reference is arXiv:2610.20691v2, Theorem 4.1. The dependency paper gives exact statement identifiers and bibliography. [Quartic provenance](../computation/quartic/PROVENANCE.json) and the individual source certificates record all subsequent pinned tables and hashes.

The twenty-five-, twenty-seven-, and thirteen-variable finite determinant specifications are not expanded. Their certified support bounds are respectively $<2^{1979}$, $<2^{2192}$, and $<2^{509}$. The three leading quartics are fully expanded, with exact monomial counts 2,835, 3,494, and 918. Parameter powers are fixed coefficients, not quantified coordinates.

Exact identities, coefficient reconstructions, support bounds, finite valuation residues, and numerical integer inequalities are unconditional statements about the supplied expressions. A rational projection equals $\mathbb Z$ by the corresponding construction theorem under its explicit arithmetic premises. A passing computation certifies its listed finite assertions; it neither proves an arithmetic conjecture nor supplies a missing effective threshold.
