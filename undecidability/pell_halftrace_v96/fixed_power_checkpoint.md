# Fixed-power replacement: integrality progress and the remaining cycle

**Status, 23 November 2026.** This is an important partial checkpoint, not a new complete source or a numerical record. The complete quartic counts in this directory come only from the proved half-trace guard reduction. Nothing in this note changes those counts.

## Objective

The retained source has the fixed power

\[
q=b^L,\qquad L=5^{60},
\]

whose present ceiling-binary implementation uses 139 actual power coordinates, counting the two retained prefix coordinates and the 137 subsequent steps. A Pell-based exponential certificate could, in principle, replace that long rational circuit by a shorter system with additional integer predicates. An acceptable replacement must establish its integer reconstruction in a noncircular order.

## A proved integrality step with an already certified parameter

Suppose that \(A,b,\Delta,\alpha\) are integers, \(A\ge2\), and \(C,D,q\) are rational numbers satisfying

\[
\begin{aligned}
C&=L+\Delta(A-1),\\
D^2-(A^2-1)C^2&=1,\\
q&=D-(A-b)C-\alpha\bigl(b(2A-b)-1\bigr).
\end{aligned}
\]

Then \(C,D,q\) are integers. Indeed the first equation makes \(C\) integral, the second makes \(D^2\) integral, and a rational number with integer square is an integer. The last equation is then an integer expression. This argument uses no interpretation of the Pell index and no assertion that \(q=b^L\).

In the current source, **\(A=s\) is an available choice of an already certified integer**, independent of the power circuit. Adding a lower-bound condition on \(s\) would establish \(A\ge2\) before using the new Pell block. Thus two additional integer predicates, for \(\Delta\) and \(\alpha\), can recover the integrality of \(q\) without a separate predicate for \(q\). This is a genuine ordering improvement over choosing the source's derived Pell parameter \(a\) before its integrality has been established.

This step alone does **not** prove the desired exponent. If \(C>0\), Pell classification supplies an index \(\nu\ge1\) with \(C=Y_\nu(A)\). Reduction modulo \(A-1\) gives only

\[
\nu\equiv L\pmod{A-1}.
\]

To infer \(\nu=L\), one needs a separately justified index range. The usual power-of-\(b\) congruence likewise needs bounds proving that its residue is the intended integer \(b^\nu\), rather than an arbitrary congruent value. Neither conclusion follows from the displayed three equations alone.

## The remaining geometric-quotient cycle

The coding prefix contains

\[
\lambda(b^5-1)=q^4-1.
\]

For the established power \(q=b^L\), the fact that \(5\mid L\) makes \(\lambda\) an integer geometric sum. If the power circuit is replaced before its exponent has been proved, knowing only that \(q\) is an integer does **not** establish this divisibility. Consequently \(\lambda\) may still be rational.

The source expression for \(r\) uses \(\lambda\). The derived Pell parameter

\[
a=(wn^2+1)rsn^2,\qquad n=q^{16},
\]

therefore need not yet be known integral. The existing first-Pell index theorem cannot be invoked at that point. In particular, an attempted argument of the form

1. use the source's first Pell coordinate \(c\) to bound the new power index;
2. conclude \(q=b^L\);
3. recover integral \(\lambda,r,a\), which justified the first Pell classification in step 1,

is circular.

Taking \(A=s\) resolves the integrality of the *new* Pell parameter, but not this separate reconstruction of \(\lambda,r,a\). The source's intended positive witnesses do make \(s\) very large compared with several other quantities. Those size relations cannot be used for an arbitrary zero of a proposed replacement before the necessary integrality and signed reconstruction have been proved.

## A possible congruence refinement, still incomplete

If one also arranged \(A\equiv1\pmod5\), then the index congruence above, together with \(5\mid L\), would imply \(5\mid\nu\). Once the separate equality \(q=b^\nu\) had been established, this would already make \(\lambda\) integral, even before identifying \(\nu=L\).

This observation does not close the proof: the required power-extraction equality and its size bounds remain unproved in a noncircular order. Nor has a complete low-cost implementation of the extra restriction on \(A\) been supplied. It is recorded as a specific avenue to investigate, not as a conditional variable-count improvement.

## Cost and the next decisive step

One straightforward way to break the remaining cycle is to add a third integer predicate for \(\lambda\). With the current ordinary-\(abc\) tuple interface, each additional input contributes 48 coordinates including its distinguished input; three extra inputs already cost 144 coordinates before the new Pell arithmetic and bounds are compiled. This exceeds the 139 coordinates offered by deleting the present power circuit. The general and specified interfaces cost more per new input. Therefore this straightforward repair gives no reduction with the current interfaces.

The next useful result would be one of the following:

- a proof recovering \(\lambda\), or the needed \(r,a\), integrally from the replacement equations without another integer predicate;
- a different exponent certificate with fewer than three new integer inputs and a complete reconstruction order;
- a way to share an additional divisibility condition with an existing integer predicate while preserving both soundness and simultaneous completeness.

Until such a result is proved and compiled, the verified ceiling-binary circuit remains the source of the fixed-power relation. No experimental search or finite sample can repair the quantified reconstruction gap described here.
