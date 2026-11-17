# Independent review of the 68-variable quartic

**Verdict: PASS under the arithmetic premises retained by the 71-variable source.** No additional arithmetic hypothesis, denominator guard, or sufficient-shift enlargement is required by this change. The final polynomial still requires ordinary rational abc; this audit does not convert it into a result under a weaker fixed-exponent hypothesis.

## Algebra and all boundary strata

The native six-field-coordinate chart (s,t,F,G,h,d), with p=h+s+t and Q=beta^4, uses

\[
 d=pF,\quad D(F+G)=(s-t)h-t^2,\quad d=Gh,
 \quad Q=d(s-t)-DFG.
\]

The difference abscissa is the derived function a=hp. Its real component alone is retained as one rational coordinate. The imaginary component has no other consumer and is recovered polynomially, so its deletion preserves the full rational solution set of the intermediate chart presentation.

For beta nonzero, the equations force F,G nonzero and give both scaled elliptic curve equations. The translated chord gives U-V, with abscissa a/beta^2. The two slope formulas cover the entire domain, including every allowed tangent and all finite two-torsion differences. U=V is impossible. The added difference (0,0) has index zero and therefore satisfies the required index-height inequality with the same nonnegative additive constant. No previous proof step divides by its abscissa.

The physical comparison errors, reciprocal products, scaled trace and both pole inputs are unchanged. The inverse-parameter extraction and nonzero-weight argument therefore continue to hold on every rational solution with nonzero input. Every previous nonzero-integer completeness witness has a unique new chart lift. At input zero, the explicit old witness transfers with h=t^2/(s-t), F=G=d=0 and a=s^2t^2/(s-t)^2. The gap is identical to the old one.

## Independent exact verification

`computation/quartic/abc68_v65/check.py` imports neither the producer nor any old residual table. It reconstructs every source equation with standard-library rational-pair sparse arithmetic, applies the fixed reference matrix, verifies every primitive row normalization and constant elimination in both directions, and independently expands all quadratic squares.

The independently verified final counts and bounds are:

- 68 total rational coordinates, including the input;
- 56 primitive quadratic residuals;
- exact degree four and coefficient one on X^4, hence content one for every integer B;
- 1078 nonzero coordinate monomials for every B>=81;
- 1081 parameter-separated terms;
- maximum fixed coefficient 3554;
- constant coefficient B^2+1, and exact coefficient height B^2+1 for every B>=81.

The certificate includes hashes of the checked quadratic and polynomial tables, checks every coordinate is used, and evaluates all 56 original and transformed rows and the full polynomial at an exact rational zero-input algebraic fixture. That fixture is not claimed to satisfy the arithmetic sufficient-shift requirement.

`computation/quartic/abc68_v65/chart-check.py` independently verifies six universal polynomial identities, all five rows on the zero-input substitution, and complete finite-field fibers with a separately implemented elliptic group law. Across seven odd prime fields and all 68 nonzero coefficient choices it finds exactly 12,960 chart solutions, with 812 tangent pairs, 1,556 pairs involving a zero numerator ordinate, 880 differences equal to (0,0), and 744 other two-torsion differences. The finite enumeration supplements the all-field proof; it is not the basis for the infinite-domain conclusion.

## Proof scope

The independent chart proof and complete coefficient reconstruction are retained with the mathematical paper and its reproducibility package. The finite-field comparisons supplement the all-field proof. They do not certify the inherited external arithmetic foundations. The sufficient odd shift remains ineffective.
