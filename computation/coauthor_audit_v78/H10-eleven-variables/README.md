# Eleven variables under a fixed weak abc inequality

H10-eleven-variables.pdf and its TeX source give the new count and assumptions. Two branches of the height argument now share one pole predicate. The original elliptic, trace-height, prime-pattern and pole-realization premises remain in force. Each variable count includes the input. The sufficient odd coefficient shift is ineffective. The existence argument covers every fixed exponent strictly between 1 and 3/2. Both eight-contact polynomials use the degree-six identity in the proof.

| Weak abc exponent | Variables | Degree upper bound |
|---|---:|---:|
| 121/100 | 11 | 33,344,385 |
| 16/15 | 11 | 19,861,377 |

- counts/poles/ contains the main proof, the six- and eight-contact specifications, regeneration scripts and receipts. The strongest polynomials are in eight/ and eight_strong/. Each small-shift circuit illustrates the family. The generator accepts an arbitrary fixed odd shift.
- counts/points/review-weak11.md gives an independent review of the original six-contact argument. eight_cusps.py checks the degree-six split identity and the eight-contact height constants. counts/poles/check_weak11.py audits all saved main variants.
- counts/realization/diagonal-intrinsic.md proves the local results and the global counterexample at 112/289 for the diagonal specialization of the ordinary-abc pole. hasse-failure.py implements its four-modulus descent. Whether the actual elliptic data for each integer can avoid the obstruction remains open.
- counts/points/point-restrictions.md and counts/selector/density.md examine fixed identifications of elliptic points and deletion of the rationality witness.
- counts/abc/proof.md provides a second single-pole construction using the intrinsic pole theorem. counts/abc/quartics/proof.md gives supplementary quartics under weak abc. The parent 62-coordinate equations used by those quartics are in abc/shared/record62.
- counts/effective/COMPACT.md gives a fully specified 27-variable polynomial of degree at most 702,371,856,384 under the retained modular premises. PROOF.md gives the alternate numerical exponent 53. counts/poles/ordinary_scale/proof.md gives degree at most 18,565,505 for the 11-variable ordinary-abc row.

With Python 3.11 or later and SymPy installed, run from this directory:

```sh
python -B verify.py
```

The finite checks verify the circuit arithmetic, inequalities and modular certificates stated in the corresponding proofs. Underlying arithmetic theorems and premises are identified in the notes. source/ includes selected primary sources and compiler dependencies from Brox repository commit d3a8c223716a0fc0dbf5af4eb7998d640c21048d, licensed CC BY 4.0. See UPSTREAM.txt and source/LICENSE. SHA256SUMS covers the package contents.
