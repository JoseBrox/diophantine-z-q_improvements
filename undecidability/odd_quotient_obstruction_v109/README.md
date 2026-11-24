# Oddness of the second Pell quotient alone does not certify c

**Proved subsystem obstruction; no full-source counterexample and no
variable-saving claim.** This extends the v102 norm obstruction to an
odd second-Pell quotient. It does not contradict the new integrality
replacement theorem: the example has `a=5`, so it fails the source's
necessary `3 | a`, and its half-trace expression is negative.

Put

```text
N  = 3915331224839183366
L  = 14018146210311261
J0 = 400518463151751 = (L+24)/35.
```

For any odd integer `B >= 3`, choose

| Coordinate | Value |
|---|---:|
| a | 5 |
| c | 1/5 |
| d | −7/5 |
| b, w, gamma | 2, 14, −2 |
| i, i_half | 5, 2 |
| F | 7/5 |
| G | −306/125 |
| J | J0−7B |
| H | L/125 |
| I | N/15625 |

All of the following hold exactly:

```math
\begin{aligned}
d&=bw+(a-2)c+(4a-5)\gamma,\\
d^2-(a^2-1)c^2&=1,\\
F^2-(a^2-1)i^2c^4&=1,\\
G&=a+F^2(c+1-a),\\
H&=c+F^2(B-c)+cFJ,\\
I^2-(G^2-1)H^2&=1.
\end{aligned}
```

Here `i=2*i_half+1` is a positive odd integer and all indicated source
quotients `gamma, i_half, J` are integers. Thus the odd-quotient repair
does not, by itself, eliminate the nonintegral first-Pell branch.

The third norm has an elementary exact certificate:

```math
N^2-78011L^2=125^4,\qquad G^2-1=78011/125^2.
```

The large integers were found through a generalized Pell orbit. Their
verification does not require a Pell solver: the checker multiplies the
norm-one pair `(11428909442110, 40919175003)` by the norm-`125^4` pair
`(171647, 612)` in the quadratic algebra with square root of `78011`.
The product is exactly `(N,L)`, and each norm is independently checked.
The bridge holds for every `B` because its coefficient of `B` is
`F^2-7*c*F=0`, while its constant term is `L/125`.

This is not a witness for the full source. Besides failing `3 | a`, it
has `|c|=1/5<B`. For any nonzero integer `k` and integer `Y` with
`|Y|>=16`, the required small-Pell closeness fails:
`|c/k-Y| >=16-1/5>1/2`. Its half-trace expression is
`2*(a*d+(a^2-1)*c+1)=-12/5`, so it also has no rational half-trace root.
The proved 605-variable reduction uses the stronger prefix and
half-trace hypotheses, not merely the odd quotient.

Run the exact audit from the repository root:

```sh
python -B undecidability/odd_quotient_obstruction_v109/verify_odd_obstruction.py
```

The checker uses exact integer and rational arithmetic, verifies the
Pell multiplication certificate, the affine identity for arbitrary `B`,
and 32 explicit odd-`B` fixtures. Its receipt is `certificate.json`.
