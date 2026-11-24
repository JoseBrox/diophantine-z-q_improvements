# Eliminate the theta positivity block in all three corrected quartics

**Theorem.** Under exactly the retained arithmetic and classical Jones coding premises of the v106/v108 predecessors, rational solvability remains undecidable for integer-coefficient quartics in **884 / 1049 / 602** existential rational variables (general / specified / ordinary rational abc), with **749 / 912 / 527** quadratic residuals. The instance is a coefficient, not a quantified variable. Fixed-parameter qualifications are unchanged. These are upper bounds, not unconditional H10(Q) results.

## Proof and order of reconstruction

Use the corrected Jones Theorem 2 source in [v93](../source_repair_v93/corrected_jones_source.tex) and the full signed and c-integrality transfers in [v106](../c_integrality_reduction_v106/c_predicate_deletion.tex) and [v108](../abc_pell_integrality_v108/abc_c_integrality.tex). Fix positive integers x,z,u,y in the respective predecessor instance tail, in particular x>2z. The retained integer predicates certify b,g,t,m. The unchanged power register gives B5=b^5. Write theta=B5-2z, ell=u+t theta, e=y+m theta. These identities hold before any Pell argument, even on an arbitrary rational zero. The retained positive-alpha equation gives

    (b-xy) q^2 - e ell g^2 = 1 + sum_{j=1}^3 r_j(r_j+1)/2 > 0

(the right side is at least 5/8 for real r_j). We do not assume q integral, or even nonzero, at this stage.

For every integer a, the equation 2(a-1)=sum_{j=1}^3 r_j(r_j+1) over the rationals is equivalent to a>=1. The lower bound 2(a-1)>=-3/4 proves soundness. For completeness, 8(a-1)+3 is positive and congruent to 3 mod 8, so Legendre's three-square theorem represents it by three odd integer squares; write these as (2r_j+1)^2.

Replace the t and m positivity residuals by exactly this wrapper for ell-u and e-y respectively, using their original six auxiliaries. Delete the theta positivity residual and its three private auxiliaries. Since ell-u and e-y are integers, the new wrappers force ell>u>0 and e>y>0. The unchanged positive-alpha residual implies (b-xy) q^2>0 (as e ell g^2>=0), hence q!=0 and b>xy. Because b,x,y,z are integers, y>=1 and x>2z, we have b>=2 and b^5>2z. Thus theta is a positive integer. Now ell-u=t theta and e-y=m theta imply t,m>0. The three deleted or modified predecessor conditions therefore have rational lifts by the same three-square theorem. Every new rational zero projects to an old rational zero after choosing three new sets of positivity witnesses as needed. All other coordinates and rows remain unchanged; the proof does not use the integrality of c, a Pell classification, or a recovered q prematurely.

Conversely every old rational zero has positive integer theta,t,m by the old wrappers; hence ell-u and e-y are positive integers. Choose the six wrapper witnesses by the theorem and omit the three theta witnesses. This gives a new rational zero with all non-wrapper coordinates unchanged. This is equivalence of the projected instance sets, not a bijection of full auxiliary zero sets.

The algebraic transformation is valid for every admissible fixed parameter of the predecessor. Each residual is an integer-coefficient polynomial in the rational variables with coefficients depending on the instance and fixed defining parameters. All retained and modified rows have degree at most two; the unchanged g wrapper has a nonzero quadratic coefficient, so the sum of all squared rows has degree exactly four. The original integer certificates and all non-pole arithmetic premises are retained, and no additional arithmetic conjecture is introduced.

## Tables and replay

The complete compact JSON tables are general_quadrics.json, specified_quadrics.json, abc_quadrics.json. Their variable names give the coordinate order; monomial lists are 1-based and coefficients are integer polynomials in the listed parameters. For a fixed instance and defining coefficient, sum the squares of the listed rows. The certificate pins predecessor bytes by SHA-256 and new table bytes by Git blob SHA. Run `python -B undecidability/positivity_theta_reduction_20261124/verify.py` from the repository root. The checker verifies every unaffected row by its variable names (not by trusting the producer's index map), both modified wrappers, all deleted-variable occurrences, and the exact counts. The mathematical projection argument is the proof above; the checker does not establish the inherited arithmetic premises.
