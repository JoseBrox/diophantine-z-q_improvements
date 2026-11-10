# Supporting eighth-power coefficient construction

This module is retained for exact reconstruction and for the supporting papers that study its eighth-power scale. The current thirteen-variable families and their complete specifications are in the [direct-input module](../direct_input13_v22/README.md).

This coefficient family assumes the rational inequality

    c <= K * rad(abc)^(121/100)

for coprime positive integers with a+b=c, with one fixed constant K.
It also retains the specified elliptic group, pole obstruction and
nonzero realization, and simultaneous prime-pattern inputs. Both ordinary
rational abc and the ordinary Szpiro discriminant-conductor conjecture
imply the displayed weak inequality; the precise statements and references
are in [the supporting eighth-power paper](../../../papers/conditional_few_variables/conditional13_20261109_v16.tex).

For each fixed odd integer B >= 3, the input is transformed to
beta=2*X^2+B. Every sufficiently large such B gives a definition
of the integers under the stated premises. The sufficient threshold is
ineffective. The supplied B=3 member is an exact algebraic fixture and
is **not certified to define the integers**.

## Rational source

There are twelve retained rational coordinates: the input, three point
pairs over Q(sqrt(2)), one comparison slope, and two independent pole
parameter pairs. Three monic point quartics and two nonzero pole quadratics
give a finite algebra of rank 256. One separating-element coordinate
replaces all its roots and guards, giving **13 total coordinates**.

All six local tests have order one and use the formal parameter
z=-x/y directly. The scales are

    1, beta^8+(Tr x(A))^8.

The six contacts are 0,-1/2,-1/4,-2/5,-1,-1/3. For each scaled
slope t, write delta=t-1 and let F be the product of its six
contact differences. The detector uses R=F/delta^8 and factors
1+D_j^2*delta^4/F. The even number of contacts makes the fixed scale
factor a rational square in the preparation identity; the scale itself
need not be a square.

The exact builder produces 1758 rational-circuit nodes and 754 integer
coefficient nodes. The independent conversion audit checks three point
quartics, two rational-square clearings, and all 48 atomic guards.
The final indexed product has 64 factors. Its certified uniform degree
bound is **12339485119488**, strictly below 2^44. For the fixture only,
the logarithmic coefficient-height bound is 29454018907833, below 2^45.
The determinant specification is finite and exact; its monomial expansion
is not materialized.

## Reproduce

Run from the repository root:

    python3 computation/few_variables/weak_abc13/build_weak_abc_source.py \
      --shift 3 --output computation/few_variables/weak_abc13/certificate
    python3 computation/few_variables/weak_abc13/check_weak_abc_source.py \
      computation/few_variables/weak_abc13/certificate \
      --output computation/few_variables/weak_abc13/independent-source-verification.json
    python3 computation/few_variables/active_elimination/build_active_specification.py \
      computation/few_variables/weak_abc13/certificate/source-polynomial-specification.json \
      computation/few_variables/weak_abc13/active13
    python3 computation/few_variables/weak_abc13/check_weak_abc_bounds.py \
      computation/few_variables/weak_abc13/active13 \
      --output computation/few_variables/weak_abc13/independent-bound-verification.json

The bound-checking wrapper changes only the source-file path for the shared
independent checker. It retains every dependency, homogeneous-guard,
companion-column, and degree-case assertion. These exact checks establish
the recorded algebraic claims, not the weak abc inequality or the inherited
arithmetic premises.
