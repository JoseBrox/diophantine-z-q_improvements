# Recovery and current verification

9 November 2026. Active publication base: main commit 439435bd761de201400bc4b931882ff6d9112da2.

The previous v14 checkpoint is intact on this branch. The 273-variable quartic has been copied into the publication layout and independently reconstructed: 273 total coordinates, 247 quadratic equations, 3474 monomials; the recovered exact hashes agree. The prepared pole counterexample has been rerun with cypari2 2.2.4 and PARI 2.17.2: the two rank bounds are [0,0] and [1,1]. All local witnesses, maps, squareclasses and Cassels matrix ranks pass. The finite-correspondence exceptional-surface checker passes.

Work in progress, not yet publication claims: a proof that quadratic systems with infinite S-integral projection need at least five total coordinates; a discriminant-free improvement of the recovered finite-algebra degree bounds; further quartic circuit compression. General arbitrary-degree lower bound currently established: at least three total coordinates. Its optimality is not established. No construction below 27 coordinates or quartic below 273 is claimed at this checkpoint.

The v14 proofs and certificates remain in checkpoints/2026-11-09/v14. Publication integration preserves their arithmetic premises and ineffective-parameter qualifications. The original elliotglazer repository is read-only for this work.
