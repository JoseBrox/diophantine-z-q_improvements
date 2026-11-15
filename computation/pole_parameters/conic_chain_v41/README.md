# Conic-chain pole obstructions

The accompanying [paper](../../../papers/pole_parameters/conic_chain_obstruction_20261115_v41.tex) proves that every fixed rational coefficient `c` in

    P=p², e²+bP=1, D=1+(c b−1)P, z²=bD

has local obstructions on arbitrarily small prepared positive inputs. The case `c=0` reduces to three quadrics in four auxiliary coordinates. For every `c` integral at an odd prime, the five-coordinate system forbids negative odd input valuations there. Local soundness does not provide completeness.

The explicit families `272/29^(2n)` and `528/31^(2n)`, for `n>=1`, obstruct the four-coordinate system and the coefficient `c=1`, respectively. The example `c=-9/25`, `b=272/441` illustrates a third local mechanism. The general proof combines three local lemmas, an elementary quadratic-character argument, the Chinese remainder theorem, and primitive Pythagorean triples.

Run:

    python -B computation/pole_parameters/conic_chain_v41/check.py

To reconstruct the certificate in another location:

    python -B computation/pole_parameters/conic_chain_v41/check.py --output /absolute/path/certificate.json

The checker verifies five symbolic identities, exact preparation and nonresidue data, finite residue obstructions, and thirteen sample coefficient classifications. The infinite theorems are proved in the paper. No variable-count improvement or lower bound for arbitrary quartics is claimed.
