# Prepared native inputs obstructing two adaptive scalar criteria

Two exact **abstract native products** meet the intrinsic-pole preparation,
but a local certificate at `p = 100003` excludes every value of the added
scalar in each of two adaptive square tests. Neither fixture is asserted
to arise from the actual elliptic tests and physical contact map of a
21-variable or 9-variable source.

Write

```text
w = u/(1+u)^2,  V = Tr(W^-1),  b = 4w/V^2,
C = V^2 + w*(2-V).
```

Both fixtures have a positive product `W=1+w*h^2` over `Q(sqrt(2))`,
`200/101 < V < 2`, `0<b<1/7`, square reduced denominator of `b`,
`b` a square in `Q_2`, `v_2(b)>=4`, and `v_7(b)>=0`. They also satisfy
the older square-class and positive-depth preparation at 3 and 17.
The proofs allow arbitrarily strong preparation at any fixed finite
set of places away from the fresh obstructing prime.

## First criterion

```text
q = 2+w*c^2,  Delta = (q^2-2q-1)^2 + 4q(q^2-1)*V.
```

For the first fixture `w=V=1 mod p`, so `C=2 mod p` is a nonsquare.
Because `p=3 mod 4` and `V=1 mod p`, the identity

```text
Delta = (q^2+1)^2 + 4(V-1)*q*(q^2-1).
```

shows that `Delta` is a nonzero `Q_p` square for **every `q in Q_p`**.
Thus `C*Delta` is never square, even with `q` unrestricted.

## Second criterion

```text
Lambda(c) = 1+w^2*V^4*c^4.
```

For the second fixture the exact fresh-prime valuations are

| Quantity | Valuation at 100003 |
| --- | ---: |
| `w` | -4 |
| `V` | 0 |
| `2-V` | 3 |
| `C` | -1 |
| `b` | -4 |

The negative valuation of `b` is even and is allowed by preparedness.
For `p=3 mod 4`, every `1+r^2` has even valuation. Hence `Lambda(c)`
has even valuation for every `c in Q_p`, and `C*Lambda(c)` cannot
be square.

The second scalar curve transforms exactly into

```text
y^2 = B*(1+b^2*z^4),  B = 1+b*(2-V)/4,  z = V^2*c/2.
```

It maps to `Y^2=X^3+(Bb)^2 X` with a prescribed abscissa square
class, and by a degree-two map to the congruent-number curve
`Y^2=X^3-(2Bb)^2 X`. These identities do not give the required
rational point; the local counterexample rules one out.

## Reproduction and proof

From the repository root:

```sh
python negative_results/computation/pole_parameters/adaptive_prepared_pairs_v76/check.py
python negative_results/computation/pole_parameters/adaptive_prepared_pairs_v76/check_independent.py
```

The checker writes `certificate.json` containing all exact rational values,
preparation checks, modular residues, valuations, and symbolic identities.
It verifies the universal formulas; no claim that a finite search proves
the universal exclusion is made. Those exclusions follow from the two
valuation lemmas in the complete paper:

`negative_results/papers/pole_parameters/adaptive_prepared_pairs_20261117_v76.tex`.

The independent checker imports neither the producer nor a computer algebra
system. It reconstructs both native products, preparation and local data,
and the curve maps using exact rational and sparse-polynomial arithmetic.
The mathematical review and its hash-bound receipt are in
`independent_review.md` and `independent_review.json`. The complete five-page
paper was compiled twice and every rendered page was visually reviewed;
the receipt is `data/audits/tex_adaptive_prepared_pairs_20261117_v76.json`.

The results show that neither one-free-scalar criterion is complete for
all prepared native inputs merely by the existing intrinsic-pole theorem.
They do not disprove the existence of suitably chosen actual elliptic
witnesses, do not establish a variable lower bound, and do not complete
the 21-variable or 9-variable targets.
