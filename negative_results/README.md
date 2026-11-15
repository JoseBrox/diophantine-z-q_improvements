# Obstructions and lower bounds

This directory contains proved negative results, separated from the constructive results in [papers](../papers). Each obstruction concerns the precise equations, arithmetic family, or geometric presentation stated in its manuscript. Failure of a replacement on all prepared inputs does not exclude a construction whose actual witnesses lie in a smaller, separately proved locus.

The [current construction table](../README.md#current-constructions--15-november-2026) gives the positive bounds. No result in this directory establishes a number field whose ring of integers is not Diophantine in its fraction field.

## Pole predicates and contact functions

| Manuscript | Result and scope |
|:--|:--|
| [Conic-chain predicates](papers/pole_parameters/conic_chain_obstruction_20261115_v41.tex) | Every fixed rational coefficient in the specified five-auxiliary family has arbitrarily small prepared local counterexamples. |
| [Automatic first conics](papers/pole_parameters/automatic_conic_obstruction_20261115_v41.tex) | Dense prepared counterfamilies obstruct the remaining pole equations, including on the completely split six-contact map. The argument uses only Tunnell's unconditional necessary criterion. |
| [Fixed pole parameters](papers/pole_parameters/fixed_pole_parameters_20261109_v17.tex) | Constant first-conic values and the specified fixed conic parameters fail on prepared inputs. The fixed-parameter genus-one examples are global obstructions, consistent with everywhere local solubility. |
| [A quartic pole predicate](papers/pole_parameters/quartic_pole_obstruction_20261109_v17.tex) | The stated quartic predicate and finite menus of its fixed coefficients fail on explicit prepared local counterfamilies. |
| [Combining pole certificates](papers/pole_parameters/combining_pole_certificates_20261109_v16.tex) | Sharing the first-conic value requires matching input square classes; the paper also gives reflection and product-height limitations. This is distinct from sharing the normalized parameter \(\tau\). |
| [Products of contact functions](papers/pole_parameters/product_height_obstructions_20261110_v19.tex) | Exact square-product and fixed-square-class families have bounded odd radical while the comparison scale grows. |
| [Rational parity combinations](papers/pole_parameters/rational_combinations_of_contacts_20261110_v20.tex) | No fixed rational parity combination has the stated detection property on the specified independent-contact family. |
| [Quadratic contact covers](papers/pole_parameters/quadratic_contact_covers_20261110_v21.tex) | Square-class matching produces genus-four covers; the proposed negative-product section has an inert-prime obstruction. |
| [The ordered square-class surface](papers/pole_parameters/ordered_squareclass_surface_20261115_v33.tex) | General type excludes the stated rational parametrizations and rational or genus-one general-fiber fibrations. Special arithmetic witness families remain a separate question. |
| [Reflection matching](papers/pole_parameters/reflection_obstruction_20261115_v33.tex) | The exact reflection restriction omits a true integer for every sufficiently large odd shift under the retained source premises. |
| [Fresh-prime square classes](papers/pole_parameters/fresh_prime_squareclass_obstruction_20261116_v42.tex) | The specified fresh-prime witnesses cannot have matching first-pole square classes; fixed comparison scales also give the stated higher-genus covers. |
| [Fixed-input K3 surfaces](papers/pole_parameters/fixed_input_k3_surfaces_20261116_v42.tex) | The full one-pole surface is a K3 after resolving four A3 points. The common-parameter product for fixed inputs has no rationally connected smooth projective model. Rational witnesses and varying-input constructions are not excluded. |
| [Rational sections](papers/pole_parameters/rational_sections_20261116_v42.tex) | For prepared fixed inputs, a rational-function section exists exactly when 17(17−b) is a rational square. The general affine and projective criteria include every boundary case. Individual rational fibers, shared rational parameters and multisections are not excluded. |

The [pole-compression guide](docs/pole_compression_obstructions_20261115_v41.md) gives the recent explicit counterfamilies. Their exact checkers remain in [conic_chain_v41](../computation/pole_parameters/conic_chain_v41) and [automatic_conic_v41](../computation/pole_parameters/automatic_conic_v41). The positive [shared-parameter local theorem](../papers/pole_parameters/shared_parameter_local_solubility_20261115_v41.tex) remains with the constructive results.

## Elliptic points and integer labels

| Manuscript | Result and scope |
|:--|:--|
| [One-parameter elliptic presentations](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.tex) | One retained rational parameter cannot give the specified finite algebraic presentation of infinitely many elliptic points. |
| [Structural constraints](papers/elliptic_charts/structural_constraints_20261109_v13.tex) | Dimension, label-graph, common-index and square-class obstructions for the stated elliptic witness models. |
| [Products of elliptic indices](papers/elliptic_charts/index_products_and_finite_correspondences_20261110_v21.tex) | The index-product graph is Zariski dense, obstructing a fixed finite correspondence on the stated infinite label sets. |
| [Label-dependent progressions](papers/elliptic_charts/progression_density_20261114_v29.tex) | Allowing infinite progressions depending on the label does not provide the proposed algebraic elimination of the reference point. |
| [Mixed reference signs](papers/elliptic_charts/mixed_reference_signs_20261116_v42.tex) | An explicit progression of doubled points lies in opposite torsion neighborhoods at the two primes above 76537. The reference chart alone cannot force agreement of the corresponding formal-parameter signs. |
| [Rational Pell approximations](papers/integer_labels/rational_pell_approximation_obstruction_20261116_v42.tex) | Arbitrarily accurate rational approximation at 19, even with the exact norm equation, does not replace the integral-label hypothesis. |

## Heights, inputs and general lower bounds

| Manuscript | Result and scope |
|:--|:--|
| [Quadratic input maps](papers/input_normalization/quadratic_input_obstruction_20261109_v12.tex) | The required universal local square condition is incompatible with the specified quadratic input normalization. |
| [Scalar measurements of degree at most three](papers/scalar_heights/cubic_scalar_height_obstruction_20261109_v11.tex) | Infinite rational fibers obstruct the proposed uniform scalar-height control on ambient rational pairs; special arithmetic subsets are not covered. |
| [Restricted abc inputs](papers/restricted_abc/restricted_abc_inputs_20261109_v17.tex) | The required scalar families fail the bounded-denominator or asymmetric-size hypotheses of the specified restricted estimates. |
| [Degree and coordinate lower bounds](papers/lower_bounds/lower_bounds_20261109_v15.tex) | Lower bounds for the classes of defining equations, quadratic systems, and nonnegative polynomials distinguished in the paper. |
| [Four-contact radicals](papers/contact_heights/four_contact_radical_obstruction_20261116_v42.tex) | The displayed four-contact family has bounded odd radical and unbounded height, including points in a fixed positive real interval. |
| [Limits of auxiliary hypotheses](papers/arithmetic_hypotheses/limitations_of_auxiliary_hypotheses_20261116_v42.tex) | Prime assignments do not control valuation parity; polynomial injections do not supply finite algebraic recovery. The separate implication from Mazur's connected-component conjecture is explicitly conditional. |

## Number-field constructions

| Manuscript | Result and scope |
|:--|:--|
| [Elliptic ratios and integrality](papers/number_fields/elliptic_ratios_and_integrality_20261109_v13.tex) | Local solubility and simultaneous approximation do not make the stated ratio construction surjective; finite rational combinations still omit infinitely many integers. |
| [Finite correspondences and denominators](papers/number_fields/finite_correspondences_and_denominators_20261109_v14.tex) | Finite-output algebraic constructions omit the specified progression terms; bounded-denominator hypotheses obstruct the stated rational or genus-one constructions. |
| [Complex multiplication and trace cancellation](papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.tex) | Adjoining \(i\) changes the rank and permits unbounded points with cancelling traces, obstructing direct transfer of this rank-and-height argument. |
| [Norm and trace graphs](papers/number_fields/norm_trace_graph_obstruction_20261116_v42.tex) | Graphs on one ambient extension-field input are Zariski dense and have no quantifier-free ring-language definition. Existential definitions are not excluded. |
| [Unchanged formulas after finite extensions](papers/number_fields/unchanged_formula_obstruction_20261116_v42.tex) | A fixed formula, or finite menu of formulas, cannot define the rings of integers unchanged over every finite extension. The paper includes degree bounds and an explicit quadratic-extension example. |
| [Products of elliptic abscissas](papers/number_fields/abscissa_product_obstruction_20261116_v42.tex) | A valuation obstruction excludes 5 from every finite multiplicative combination of rational abscissas on the stated positive-rank curve. |

The positive [definability reductions](../papers/number_fields/number_field_definability_20261109_v12.tex) are kept separately. A failure of one formula after extending its coefficient field is a statement about that formula, not a counterexample to the existence of every possible Diophantine definition.

## Sharpness and necessary hypotheses of positive theorems

An optimality clause or an example showing why a hypothesis is needed remains attached to the positive theorem it qualifies. This includes the [optimal quadratic-field square predicate](../papers/square_predicates/quadratic_square_predicates_20261108_v10.tex), the exact [product-height equality criterion](../papers/elliptic_heights/product_height_20261113_v23.tex), and the exceptional-constant condition in the [translated-point chart](../papers/elliptic_charts/fixed_difference_charts_20261110_v18.tex).

## Reproduction

The [separate theorem catalog](data/results.json) contains the obstruction records extracted from the historical results metadata. The current positive construction table remains in the main README.

The computations linked by the papers retain their existing paths when they are shared with constructive results. The repository's verification commands and manifest cover both directories. The manuscripts state the infinite results; finite examples and coefficient checks certify only the computations they actually perform.
