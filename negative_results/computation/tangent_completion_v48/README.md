# Quadratic completion obstruction for the compressed pairing

The manuscript is [tangent_completion_20261116_v48.tex](../../papers/elliptic_charts/tangent_completion_20261116_v48.tex).

At the fixed reference `H=2P` and input scale `beta=1`, the complete
geometric secant image in ten field coordinates has precisely nineteen
identities of total degree at most two. All of them vanish on an explicit
spurious tangent family. The proposed difference height is therefore not
repaired by adding such identities. This remains true for arbitrary rational
quadrics in the twenty rational components, including products of conjugate
components: degree-bounded zero closures commute with products, and
restriction of scalars splits into conjugate factors.

The package gives exact counterexamples with zero and nonzero coupling
coordinates. The first has proposed height zero and true trace `57/4`.
The second has both coupling coordinates nonzero and assigns four times the
true difference abscissa. These are counterexamples to the specified local
pairing, not purported solutions of a finished global detector.

## Reproduction

Use Python 3.12 and SymPy 1.14.0. From this directory:

```sh
python check.py --output /tmp/tangent-certificate.json
python independent-check.py --certificate /tmp/tangent-certificate.json --output /tmp/tangent-independent.json
```

The outputs reproduce `certificate.json` and `independent-verification.json`.
Both programs print their full JSON output when `--output` is omitted. They
write no package files unless explicitly given those output paths.

`check.py` represents `Q(sqrt(2))` by exact rational pairs, checks duplication
and the two tangent examples, and uses modular elimination. It evaluates
676 deterministically selected secant pairs modulo 1009 and records a
47-row full-rank subset. The certificate includes the selected parameter
four-tuples, the minor columns, and the independent identity minor.
Their determinants are respectively 541 and 968 modulo 1009.

`independent-check.py` imports no producer code. It uses SymPy's algebraic
number field and `DomainMatrix` over `GF(1009)`, reconstructs both minors,
and verifies all sample curve and nonzero conditions. It also reduces the
nine generating identities to zero in the characteristic-zero function
field using the free basis `1,s,t,s*t`, and checks the entire false tangent
family as a polynomial in its parameter. Thus the symbolic identity audit
is not inferred from finite samples.

The characteristic-zero dimension proof combines the certified minors with
a monic normal-form argument over the localization at `(1009,sqrt(2)-439)`.
The extension to rational component quadrics is proved by the product-closure
lemma in the manuscript; it does not rely on a numerical rank experiment
in twenty coordinates.

## Scope

The first theorem preserves the complete geometric secant image in the
stated coordinates. The strengthened theorem below also permits the
physical rational trace, but no genuinely new helper coordinate. It permits
specialization of pre-existing reference coordinates to the displayed
reference. It does not cover a different embedding, new helper
coordinates, or equations required only on a smaller arithmetic witness
family. It gives no lower bound for the number of variables in defining
quartics, and uses no prime-pattern, pole, Mordell–Weil-rank, or abc premise.

## The physical trace does not complete the same embedding

The strengthened theorem also permits the existing rational height
`T=Tr x(U-V)`. After splitting restriction of scalars, it is the sum of
the two independent physical abscissas

```
h = f*g*(s+t)^2/(g-f)^2.
```

The corresponding 21-coordinate graph has 253 monomials of degree at most
two. An exact 194-by-194 evaluation minor is 451 modulo 1009, and a
59-by-59 known-identity minor is 929. The rank-16 Laurent normal-form
argument for four curve equations lifts these certificates to characteristic
zero. All quadratic identities still vanish on the false tangent family
with **arbitrary rational T**. Thus the physical trace alone does not repair
the same embedding. Genuinely new helpers or different embeddings remain
outside the theorem.

Reproduce this certificate pair with:

```sh
python trace-check.py --output /tmp/trace-certificate.json
python trace-independent-check.py --certificate /tmp/trace-certificate.json --output /tmp/trace-independent.json
```

The outputs reproduce `trace-certificate.json` and
`trace-independent-verification.json`. The independent checker reconstructs
both minors using SymPy, verifies the physical abscissa formula by an exact
curve-ideal identity, and checks the entire split false tangent family with
independent coupling parameters and arbitrary trace symbolically. It imports
no producer or sibling-checker code.
