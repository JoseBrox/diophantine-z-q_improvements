# K3 surfaces in the fixed-input pole problem

Companion paper:
`negative_results/papers/pole_parameters/fixed_input_k3_surfaces_20261116_v42.tex`.

For every fixed nonzero pair `C,D` in characteristic zero, the normalized
one-pole surface, with its conic parameter still variable, is birational to
a double cover of `P1 × P1` branched over two smooth `(2,2)` curves. Their
four tangencies produce four `A3` singularities, and the minimal resolution
is a K3 surface. The common-parameter fiber product for fixed detector
inputs dominates each of these K3 surfaces and therefore has no
rationally connected smooth projective model.

This is a geometric restriction on this fixed-input model. It does not
exclude rational points, a common rational parameter, Zariski density,
rational subvarieties, or arithmetic constructions varying the detector
inputs. It does not by itself determine uniruledness of the
higher-dimensional fiber product.

## Reproduction

Run from the repository root with Python 3 and SymPy:

```sh
python3 negative_results/computation/fixed_input_k3_v42/check.py
```

Use `--output /path/to/file.json` to avoid modifying the committed
certificate. All algebra is exact. The checker verifies:

- the rational change to the projective double-cover equation and the
  branch bidegrees;
- all eight affine smoothness criteria, with no excluded coefficient
  cases beyond `C*D != 0`;
- the intersection identities, tangency order two, and exact local `A3`
  normal forms at the four branch intersections;
- the two blow-ups resolving `ab=c^4`, together with their canonical-form
  transformations;
- the Euler-number and cohomology-dimension arithmetic used in the proof.

The K3 and rational-connectedness conclusions also use the geometric
arguments in the manuscript. The two supporting references were checked
in their primary author/publisher copies: Angermüller–Barth, Section 3,
page 319, and Debarre, Proposition 2.5(b). Their exact bibliographic data
and URLs are recorded in `verification.json`.
