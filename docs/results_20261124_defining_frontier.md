# Defining-polynomial frontier, 24 November 2026

This checkpoint concerns only the representation of Z inside Q. Under the retained arithmetic premises, the new ordinary rational abc quartic in 54 total coordinates supersedes the 56-coordinate v81 construction. At that checkpoint, the 25/27/11 unbounded-degree and 163/179 general quartic bounds were unchanged. No conditional one-parameter pole specialization is promoted to a defining result.

Proof, complete quadrics, symbolic expanded coefficients, a finite coefficient fixture, and independent verification: [54-variable construction](../computation/asymmetric_contact54_20261124/README.md).

The new contact weight is (H^2/A-1+1/H), with A and H the asymmetrically normalized eight-root contact products. Its odd-prime support is bounded below by (23h(M)/20-O(1)), whereas the input error contributes at most (1002h(M)/997+O(\log(1+|m|))). This removes the need for the fourth power of the height parameter and the derivative circuit. Integer completeness is proved separately at the selected primes, the nonselected primes, and the prepared fixed places.

Retained hypotheses and effectivity are exactly as stated in the proof. In particular B=1 is a coefficient fixture, not an effective defining cutoff.

The independent exact construction check [passed on GitHub Actions](https://github.com/JoseBrox/diophantine-z-q_improvements/actions/runs/45376829320). The B=1 fixture has 11,174 bytes and coefficient height 5,531,402,752.

[Two scoped obstructions](../negative_results/defining_gate_obstructions_20261124/README.md) record the full rank of the quadratic parts of the 163/179/54 tables and an elementary obstruction to a universal single rational-function parity-OR gate for arbitrary scalar inputs. These do not establish global lower bounds.

## Effective weighted explicit construction

The [178-coordinate specified quartic](../computation/weighted_explicit178_20261124/README.md) replaces the 179-coordinate specified quartic. The proof extends the effective finite-place abscissa-sum estimate to positive rational weights and absorbs the explicit height loss in the original fixed scalar anchor. Its 150 quadrics expand to 3,009 monomials with 748-bit coefficient height and a 66,278-byte literal. The same arithmetic premises are retained. No new ineffective constant or additional conjecture is needed.
