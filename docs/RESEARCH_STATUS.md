# Mathematical scope, dependencies, and known obstructions

**Date: 6 November 2026.** This note summarizes the claims *recorded by the supplied research manuscript*. It does not independently adjudicate the named arithmetic hypotheses.

## Definitions and counting conventions

For \(P\in\mathbb Q[X,Y_1,\ldots,Y_r]\), a Diophantine definition of \(\mathbb Z\) in \(\mathbb Q\) would establish
\(x\in\mathbb Z\iff \exists y\in\mathbb Q^r:P(x,y)=0\).
Variables means **r+1**, counting \(X\). An auxiliary circuit node used only to *specify* a polynomial is not quantified; a free coordinate constrained by an equation is a witness. Height is the maximum primitive-integer coefficient after fixing numerical constants.

## Status categories

| Claim or object | Status represented in this release |
|:--|:--|
| Original 12,504-variable quartic and source-preserving transformations | Exact algebraic certificates and verification receipts supplied; identification with Z requires upstream source arithmetic theorem |
| 558-variable indexed polynomial | Source-preserving algebraic compiler with independently checked specification; final arithmetic interpretation inherits upstream arithmetic |
| 41- and 43-variable indexed polynomials | Explicit indexed descriptions, finite coefficient DAGs, and check receipts; integrality interpretation additionally requires the identified shared-point arithmetic and Sun's prime-pattern theorem |
| 1,315- and 1,335-variable quartics | Complete sparse coefficient tables, transformation receipts and independent checks; interpretation as Z depends on the same arithmetic inputs |
| Two-variable lower bound | Manuscript includes a proof, independent of the external arithmetic theorem |
| General degree-four lower bound for one defining polynomial | Manuscript includes a proof under the stated definition |
| Two quadratic equations cannot define an infinite subset of the integers by input projection | Manuscript includes a proof with hypotheses; yields five-variable/three-equation necessity for a quadratic system |
| Definitions with at most ten total variables | **Not constructed**; only two variables are ruled out universally here |
| Extension of these polynomial formulas to all number fields | **Not established**; counterexamples and scope restrictions recorded |

## Arithmetic assumptions are not certificate contents

The named sources are the pinned reciprocal-comparison system, its elliptic and height estimates, formal-logarithm/Lucas results, and a prime-pattern theorem attributed in the report to Z.-W. Sun (Theorem 4.1 of its cited 2026 version). A Python script verifying an algebraic identity is not a proof of an analytic/number-theoretic theorem. The finite-fibre reductions also involve hypotheses about pole guards, finite-choice witnesses, and rational solution sets: they are made explicit in the manuscript.

## Issues outside the rational base field

The manuscript exhibits a generic \(\mathbb Q(i)\) section for the literal new quartics, so those *same formulas* do not define the ring of integers of \(\mathbb Q(i)\). Some unshifted indexed formulas reject specific algebraic integer inputs; translated versions with \(\beta=X^2+2402\) repair those finite scalar contacts, **not** the entire arithmetic obstruction. The manuscript also gives a totally real quartic-field counterexample to a particular finite elliptic-anchor inference. Field-dependent division norms combine systems into one equation at degree 72 without addressing the arithmetic projection problem.

## Most useful next checks

Independent review should audit the arithmetic source and Sun theorem, scrutinize the simultaneous-point sharing mechanism, and attempt a genuinely new rational-compression or integrality argument if a ten-variable target is desired. Do not reinterpret a formal-algebra check as a global arithmetic proof.

**Primary source for all technical proofs:** [`paper/diophantine_optimization_20261106_v3.tex`](../paper/diophantine_optimization_20261106_v3.tex).
