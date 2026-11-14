# Corrected 79-variable abc quartic

The current proof is `papers/quartic_existence/quartic_abc79_20261114_v27.tex`. It retains ordinary rational abc and the stated elliptic/prime-pattern inputs, and applies Jaswal's Hexagon Theorem 1.2 at the exact prepared squareclass scope proved in the companion pole paper. The sufficient odd B is ineffective; B=3 is not a certified defining member.

`reference.py` records the corrected equations, including the f*S term missing from the earlier printed v26 table. `prove_reference.py` produces the exact algebraic certificate; `check_reference.py` verifies it without importing the producer. `build.py` produces all 71 quadratic rows and 1139 ordinary quartic monomials; `check.py` reconstructs them independently.

The correction is mathematical, not merely typographical: the displayed ideal-membership identity fails without the missing term. The original equations supply it. The earlier v26 coefficient archive was unavailable for byte comparison; no assertion that those unpublished bytes were already correct is made. Current proofs and tables are fully rebuilt.
