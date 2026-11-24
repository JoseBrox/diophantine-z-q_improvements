# Integral second-Pell coordinates do not replace the i quotient

**Status: exact obstruction for a proper norm/congruence subsystem.
This is not a full-source counterexample. No predicate is deleted.**

The newly proved half-trace replacement for `c` exploits a second,
independently integral shifted trace. The analogous suggestion for `i`
would also have to recover the divisibility `c^2 | E`, not just the
integrality of the second Pell coordinates `F,E`. The following exact
example separates these requirements.

| Coordinate | Value |
|---|---:|
| `a` | 6 |
| `Delta=a^2-1` | 35 |
| `c` | 143 |
| `d` | 846 |
| `b` | 2 |
| `w` | 4 |
| `gamma` | 14 |
| `B` | 71 |
| `r=(B-1)/2` | 35 |
| `F` | 6 |
| `E` | 1 |
| `i=E/c^2` | 1/20449 |
| `G` | 4974 |
| `H` | 98962703 |
| `I` | 492240474774 |
| `J` | 115344 |
| first half-trace root | 142 |
| second half-trace root | 12 |

These values satisfy

```math
d=bw+(a-2)c+(4a-5)\gamma,\qquad d^2-\Delta c^2=1,
```

```math
E=ic^2,\qquad F^2-\Delta E^2=1,
```

```math
G=a+F^2(c+1-a),\qquad
H=c+F^2(B-c)+cFJ,\qquad I^2-(G^2-1)H^2=1,
```

and both half-trace-square equations

```math
142^2=2(ad+\Delta c+1),\qquad
12^2=2(aF+\Delta E+1).
```

In particular `3|a`, `a,c,d,F,E,G,H,I,J` are positive integers,
`B` is odd, and `c>B`. Both quotients `gamma,J` are integers, and
`i` is positive and nonzero. Nevertheless `i` is nonintegral.

The construction is transparent in Pell coordinates:

```math
c=Y_3(6)=143,\quad d=X_3(6)=846,\quad
H=Y_3(G)=4G^2-1,\quad I=X_3(G)=4G^3-3G.
```

The third-Pell quotient is integral because

```math
c+F^2(B-c)=-2449,\qquad cF=858,
\qquad H+2449=858\cdot115344.
```

Thus even adding integral `E,F` and a second half-trace square does not
justify deleting the `i` certificate from the index argument. Its
required divisibility is substantive.

## Scope of the obstruction

The example is not a witness to the full source. In particular it
cannot satisfy its defining identity

```math
a=(wM+1)rsM
```

with `M>=16` and a nonzero integer `s`: its right side has magnitude at
least `(4*16+1)*35*16=36400`, while `a=6`. No claim is made that the
full small-Pell norm or closeness inequality holds. Those additional
constraints remain possible tools for a future integrality theorem.

For the odd-quotient chart, setting
`i_half=(i-1)/2=-10224/20449` satisfies the affine interpretation
`i=2*i_half+1`; its integer interface is precisely what this example
lacks. The distinct odd-*integral*-i obstruction is recorded separately
by the abc-source audit and addresses deletion of the c predicate
without the restored half-trace square.

## Reproducibility

```sh
python -B undecidability/pell_quotient_obstruction_v109/verify_obstruction.py
```

The checker verifies every displayed equality with exact integers and
rationals, independently computes the two index-three Pell pairs, and
checks the source-growth exclusion. Its receipt states the subsystem
scope explicitly.
