# Eleven variables under ordinary rational abc

The [complete manuscript](../../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex) gives an integer-polynomial family in **11 total variables**, including the input. It assumes ordinary rational abc and the explicitly retained elliptic, prime-pattern, trace-height and intrinsic-pole inputs. A sufficient fixed odd shift exists; no numerical sufficient shift is certified.

Let `M=beta^4+T^4`, `a=M^4`, and take the nine shifts

```text
-10, -8, -5, 1, 2, 3, 4, 6, 7.
```

Their sum is zero and no pair, including a repeated shift, sums to zero. The source uses

```math
G(A,Z)=\prod_c((A+c)^2-Z),\qquad H=G_A/2,\qquad
u=-9G/H=-18F/F_a,\qquad A=M^4,\quad Z=z^2.
```

The derivative denominator `H` is primitive. Removing the scale factor from `F/F_a` preserves simple contacts at every numerator and denominator prime of `M`. The resulting height loss is `(2+epsilon)h(M)`. The strict absorption margin is `44272779/198801800`.

There are eighteen simultaneous prime positions. The height argument `t=M^8-z^2` is guarded separately. On the completeness interval `a>10`, `z>a+10`, the contact product is negative and its derivative positive, so `u>0`. At every fixed place, `u` has leading term `z^2/a`, a rational square because `a=M^4`. The paper proves the preparation and guards, including all primes dividing the numerator or denominator of `M` and the zero-ordinate pole case.

The native source is [source.json](specification/source.json). The complete polynomial is [polynomial.json](specification/polynomial.json), using the stored [subalgebra specification](specification/subalgebra_parent.json), the v28 integral point algebra, v30 subalgebra norms, and v40 terminal-root separator. The final pole ordinate and radicand may vanish; all rational denominators and preceding point radicands remain guarded. The expressions `s`, `eta+v^2`, and `eta-v^2` need no nonzero guards because they are not divided by.

| Quantity | Certified bound |
|:--|--:|
| Total variables | 11 |
| Finite-algebra rank | 128 |
| Total degree | at most 234,157,441, below 2^28 |
| Monomials | fewer than 2^264 |
| Integer content | 1 |
| Scalar guard degree | at most 1,541,062 |
| Separator degree | at most 288,292 |

The stored coefficient value `B=3` is an algebraic fixture, **not a certified defining member**. For this fixture the coefficient height is at most `2^489317888`. The compiler computes a coefficient bound for each specified fixed shift.

From the repository root:

```sh
python -B computation/few_variables/derivative11_v63/build_source.py
python -B scripts/verify_derivative11_v63.py
```

The builder accepts `--shift B` and `--output DIRECTORY`. The portable specification records the equivalent arguments `--name ordinary_abc11 --parameter B`.

| Independent check | Scope |
|:--|:--|
| `check_algebra.py` | Symbolic derivative, eighteen-position factorization, numerator and denominator contacts, leading-square and collision valuations, exact height constants |
| `check_completeness.py` | Separate standard-library polynomial multiplication, odd valuations and uniform real bounds |
| `check_native.py` | Ordinary elliptic addition versus the circuit at 384 exact point-algebra character evaluations |
| `check_specification.py` | Independent full-norm, subalgebra and terminal-root traversals; every denominator, square extraction, norm rank and final bound; deliberate corruption controls |

No production-sized determinant is expanded. The exact computations certify only their stated finite scope. They do not prove abc or the external arithmetic foundations, and do not establish the 21- or 9-variable targets.
