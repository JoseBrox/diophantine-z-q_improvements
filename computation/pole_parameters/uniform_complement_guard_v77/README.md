# Uniform complement guards on the full auxiliary derivative source

The note proves a uniform positive bound at every point character of an
actual full auxiliary tuple in either even-valuation derivative source:

`u >= 10  =>  0 < eta=28w/V^2 < 147/242 < 1`.

It uses only the real elliptic equation, retained point/difference guards,
the first four factors `D=1/(x+u)`, and the two squared balanced comparisons.
It does not restrict the auxiliary points to `2E(K)`. The original physical
choice `z>a+10` already forces `u>10` for both the seven- and nine-contact
sets, by the exact harmonic-mean estimates in the certificate.

Consequently `1-eta` is a positive unit at every point character. If its
selected value is a rational square `c^2`, replacing the two retained pole
coordinates by the single finite root `c` automatically satisfies every new
character-unit and real-root condition. The identity

`P_eta(1,c) = [2 eta (1-eta)]^2`

also gives a native witness with nonzero ordinate in every character.
The finite point rank remains 64, the final rank remains 128, and the source
has nine total rational coordinates, including the input. Its soundness
assumes ordinary rational abc, the retained arithmetic premises, and a
sufficiently large fixed odd defining parameter of the derivative construction.

**The selected rational square has not been proved to exist.** The package
does not prove nine-variable completeness, a sufficient numerical defining
parameter, a new degree bound, or a twenty-one-variable construction.
The inequality `u>=10` is a completeness choice, not an extra condition in
the global sound source.

## Reference-normalizer variant

Keeping the detector unchanged, the alternative
`w_star=16u/(4+7u)^2`, `eta_star=28w_star/V^2` retains every old guard and
adds `4+7u!=0`. The complete eleven-coordinate native source transfers
under ordinary rational abc and the same retained arithmetic premises.
The proof checks every valuation case and fixed-place preparation; it does
not infer square reduced denominators merely from a square ratio.

The full auxiliary bound strengthens to `0<eta_star<294/1369<1`.
At the reference value `V=2`, the complement is
`1-7w_star=((4-7u)/(4+7u))^2`. Every finite guarded actual tuple has
`V<2`, so that identity alone supplies no actual square witness.
The nine-coordinate complement variant still requires the actual square
`V^2-448u/(4+7u)^2`. Its realization remains open. No new coefficient source
or degree bound is claimed.

## Reproduction

From the repository root:

```sh
python -B computation/pole_parameters/uniform_complement_guard_v77/check.py
python -B computation/pole_parameters/uniform_complement_guard_v77/check_independent.py
```

The checker uses only the Python standard library. It verifies the exact
integer margin, both contact sums, and the native specialization by integer
polynomial convolution. It also verifies the reference-normalizer identity
and stronger exact upper bound, and checks and binds the previously audited
source metadata, retained guards, finite ranks and coordinate census. The
universal real inequalities are proved in the manuscript; finite numerical
sampling is not used to infer them.

The independent checker imports neither the producer nor a computer algebra
system. It independently expands the native identity and recomputes the
integer margin, harmonic sums and coordinate count. The separate mathematical
review covers the universal inequalities, actual character hypotheses,
denominator signs, soundness premises and remaining realization gap.

Complete proof:
`papers/pole_parameters/uniform_complement_guard_20261117_v77.tex`.
The build and visual-inspection receipt is
`data/audits/tex_uniform_complement_guard_20261117_v77.json`.
