# Small trace classes and the cubic rank theorem

The manuscript `papers/pole_parameters/small_trace_classes_20261117_v58.tex`
proves the local, whole-character and finite-algebra claims. Its smallest
radicand is `V^3+(2-w)*V^2+4*w`. The change `x=V+2` gives
`y^2=x*(x^2-(w+4)*x+4*(w+1))`.

For every rational `0<w<=1/4`, the point `(4,4)` has infinite order.
The torsion proof uses Mazur's classification and exact rational-root
exclusions for the evaluated division polynomials of orders 8, 10 and 12.

- `check.py` verifies the class and local polynomial identities.
- `check_rank.py` uses only standard-library exact polynomial arithmetic
  to recompute every saved coefficient in `rank_coefficients.json`, the
  primitive contents and the modulo-three exclusion at `w=1/5`.
- `independent_rank.py` uses exact tangent/chord arithmetic in `Q(w)`,
  without division-polynomial recurrences, to recover the same primitive
  polynomials from reduced multiple-coordinate denominators. It requires
  SymPy 1.14.0.

Run both rank scripts with `--output PATH` to reproduce their certificates.
The integration command is `python -B scripts/verify_v58.py`.

These checks and the proved positive rank do not prescribe the abscissa
`x=2+Trace(W^-1)` of an actual detector. Simultaneous actual-trace
realization and the proposed 21/9 defining-variable bounds remain unproved.
