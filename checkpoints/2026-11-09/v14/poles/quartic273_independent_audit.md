# Independent mathematical audit of the 273-variable quartic

## Result and scope

**PASS.** The new construction is a valid reduction from the pinned 279-coordinate source, under the arithmetic premises and ineffective eventual coefficient threshold explicitly retained by the paper. This review does not discharge those inherited arithmetic premises. It found no strengthened premise, lost completeness case, or unhandled denominator-zero stratum in the new steps.

Reviewed source: `work/v14/quartic/quartic273_20261109_v14.tex`.
The independent standard-library checker `work/v14/quartic/check_quartic273.py` was read and rerun successfully.

Verified output:

- 273 rational coordinates, including the input;
- 247 primitive quadratic residuals;
- sum of squares of degree exactly four and content one;
- 3474 coordinate monomials for every positive coefficient parameter;
- quadratic-table SHA256: `c2e2ad2838e79aa38c93bd41aa079d612826b5991c19835b88e14ec12fecc18b`;
- polynomial-table SHA256: `7e538c3d6714e5b699074a3e94243f5d84f38b19c216341360c1e62688ee69e5`.

## Local separation and extraction

At a good unramified contact prime every finite reciprocal-abscissa valuation is even. For negative abscissa valuation the curve equation gives `2v(y)=3v(x)`; for positive abscissa valuation it gives `2v(y)=v(x)` because the curve coefficient is a unit. The identity point is handled by a zero test, which simply removes its term.

In the four three-term factors, nonconstant term valuations lie in the disjoint classes odd, twice odd, and four times odd. In the four-term factor T3, the first three valuations have residues `nu,-nu,2` modulo four and the last has residue four modulo eight. This proves separation for every odd integer nu, including negative nu. Constant valuation zero is separate. Thus each factor is nonzero, has valuation at most zero, and has residue one whenever its valuation is zero.

The literal trace equation forces the scalar trace numerator nonzero because otherwise both rational components of W vanish. The pole input is consequently exactly `R/Tr(W^-1)^2`. If ell is the largest valuation of W over a contact prime, the trace inequality gives `v(b)<=nu+2ell`. The pole obstruction and oddness give `nu>0` and `ell>-nu/2`. At the place attaining ell every factor, and then each term, has valuation greater than `-nu/2`.

The resulting orders are precisely: high comparisons and Lucas residual 12; input error I 6; first cross-comparison C1 3; reciprocal abscissa of H 6; all remaining reciprocal abscissas at least 2. The claimed order 6 for H correctly uses evenness. These are fixed integer orders, not orders multiplied by nu.

## Formal ratios and completeness

The exceptional H classes are excluded using the reciprocal-abscissa test and bounded contact radicals before any comparison denominator is interpreted. The new approximation polynomial has no zero in Q(sqrt(2)), so it introduces no global denominator exception. At the local places, integrality of one full ratio follows from h or h-1 being a unit. The cross-test transfers integrality to the other full ratio. Only after that step does the proof infer that the primary numerator points have the depth of H. This ordering avoids a circular formal-depth argument.

The primary approximation error has order at least 12 in soundness; the alternate errors have orders 4 and 12. They give the needed label congruences of orders 3 and 12, including zero numerator points, half-integral h, and inert primes. In completeness the source chooses primary depth 20, and the exact full ratio is the integer label, giving primary error 80. The stronger input test therefore imposes no new arithmetic restriction. The opposite-place trace is a unit because the factor residue possibilities are zero or one after inversion; the trace residue is one or two, and the contact primes are odd.

At prepared fixed primes the exact formula `v(q)=18v(a*)-2v(lambda)` shows that the retained fixed denominator dilation can make every weighted term small. For large positive real lambda, both R and q are positive and tend to zero; the factors tend to one. The pole input thus tends to zero through positive values. The new factors use only even test powers, so no new real-sign condition is needed.

## All-input contact evaluation and zero strata

Let V=(t-1)^10 and divide F4=VS+R, with deg R<=9. Then the leading coefficient of S-V is

`a0 = -62183708/976393 != 0`.

The polynomials U=(S-V)/a0 and L=V-tU have degrees 9 and at most 9. The exact identities

`V=tU+L`, `F4=V^2+a0*U*V+R`

produce the claimed six-coordinate circuit. Every exponent from zero through nine is a sum of two elements of `{0,1,2,3,6}`. Three coordinates compute t^2,t^3,t^6; the remaining three successively compute U,V,F4. Only fixed rational coefficients are divided. The identities therefore hold at t=1, all contacts, and every other input. The checker reconstructs these identities independently by finite differences and descending coefficient equations.

The clearing equation forbids every contact value because none is 1 and the scale is nonzero. If q=0, the clearing equations imply delta=0. The converse is not needed and is not asserted: q may be arbitrary when delta=0. On that stratum the contact radical is one, so neither reciprocal weights nor local trace inversion are needed for the height argument. On an actual contact prime q is nonzero and the weight equations force the advertised powers.

## Global exponents and finite coefficient data

The amplified contact exponent is 19/4. With a twelfth-power divisor of a Lucas residual of size at most 14B^4, the global exponent is 19/12<2, so the scalar lower bound excludes a nonzero residual for sufficiently large coefficient parameter. The input numerator has a cubed contact divisor and size at most `2B*exp(h(beta))`; rearrangement gives the coefficient 19/5 on h(beta). The source estimate h(beta)=O(c^(19/24)) contradicts the integral Lucas lower bound log B>c-4. No new effectiveness claim is made.

The checker independently reconstructs every changed row, compares all retained rows with a pinned source, and expands the complete sum of squares by unordered pairs. It confirms the unique coefficient A^2+1, constant coefficient maximum of 1520 bits, linear multiplier maximum 13118436242, and the exact height threshold N>=23. The arithmetic defining threshold remains ineffective.
