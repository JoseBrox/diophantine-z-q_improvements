# Thirteen variables under an additional abc hypothesis

This is a separate conditional coefficient family. Its projection theorem assumes the rational **abc conjecture**, together with the specified elliptic group, pole obstruction and nonzero realization, and simultaneous prime-pattern inputs. It is not a thirteen-variable construction under the assumptions of the twenty-seven-variable theorem alone.

For each fixed odd integer `B >= 3`, the input is transformed by `beta = 2*X^2+B`. The theorem proves that every sufficiently large such `B` gives a definition of the integers. The sufficient threshold is ineffective. The supplied `B=3` files are an exact algebraic fixture and are **not certified to define the integers**.

## Specification

The source has exactly twelve retained rational coordinates: the input, three pairs for the points `A,H,UA` over `Q(sqrt(2))`, a common comparison slope, and two independent pole parameter pairs. Three quartic point roots and two quadratic pole roots form a finite algebra of rank 256. The separating-element theorem eliminates all five roots with one extra coordinate, giving **13 total coordinates**, including the input.

There are six local tests, all at order one. The ratios use `z=-x/y` directly. The two comparison scales are `1` and `(beta^6+(Tr x(A))^6)^2`. The complete rational source, guards, soundness, completeness, and both uses of abc are proved in [the conditional paper](../../../papers/conditional_few_variables/conditional13_20261109_v15.tex).

For every fixed odd `B >= 3`, the specified polynomial has degree at most **13155996618240**, strictly below `2^44`. The final finite product has 64 factors. The stored fixture has logarithmic coefficient-height bound 31315024824505, strictly below `2^45`; that coefficient estimate does not determine a sufficient defining shift.

## Reproduce

Run from the repository root:

```sh
python3 computation/few_variables/conditional13/build_conditional_source.py \
  --shift 3 --output computation/few_variables/conditional13/certificate
python3 computation/few_variables/conditional13/check_conditional_source.py \
  computation/few_variables/conditional13/certificate \
  --output computation/few_variables/conditional13/independent-source-verification.json
python3 computation/few_variables/active_elimination/build_active_specification.py \
  computation/few_variables/conditional13/certificate/source-polynomial-specification.json \
  computation/few_variables/conditional13/active13
python3 computation/few_variables/active_elimination/check_active_specification.py \
  computation/few_variables/conditional13/active13 \
  --output computation/few_variables/conditional13/independent-bound-verification.json
```

The independent source auditor uses exact expression identities to check every affine conversion, all three point quartics and automatic guards, both pole square clearings, and all 46 atomic guard factors. It also confirms that the fixed shift is a coefficient parameter of weight zero, which makes the degree proof uniform. The separate bound checker imports no builder code and verifies the point/pole dependencies, guard exponents, companion-column inequalities, and all 64 factors separately.

The `certificate/source-polynomial-specification.json` file is the integer version of the guarded source and contains the intermediate generic elimination grammar. The current final polynomial is specified by `active13/polynomial-specification.json`, whose separating-element grammar and coefficient bounds are used in the paper. Neither grammar materializes a rank-sized monomial expansion.
