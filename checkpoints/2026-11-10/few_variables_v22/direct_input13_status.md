# Direct input comparison: proved construction and checkpoint

The new paper and complete computations are in the repository:

- `papers/conditional_few_variables/direct_input13_20261110_v22.tex`
- `computation/few_variables/direct_input13_v22/`

The final polynomials are `X*Q_B`, where `Q_B` is the guarded
finite-algebra determinant from the source. The multiplication includes
input zero without adding a variable. The source compares the elliptic
index n directly to X, and uses the independent positive height parameter
beta=2X^2+B.

## Decisive height inequality

For X=u/v reduced and B>=3, gcd(2u^2+Bv^2,v^2)<=2. The reduced
numerator of beta is therefore at least max(u^2,v^2), proving
`2*h(X)<=h(beta)` uniformly in B. Also beta>=B.

Under weak abc exponent kappa, the six-contact estimate has coefficient
`1/gamma`, gamma=8/kappa-6. For even power d, the projective sum-height
estimate has coefficient `1/alpha`, alpha=d/kappa-3. Two local detectors
give eta=h(1:beta:T(n)) <= 2/(gamma*alpha)*log N+C, where N is the
numerator of X-n. Since log N<=eta/2+log(1+|n|), the sufficient
condition becomes gamma*alpha>1. The trace-height theorem bounds n and
eta, independently of B. Taking a sufficiently large odd B contradicts
beta>=B unless X=n.

The constants from abc and aggregate trace height are ineffective; no
numerical defining shift is claimed.

## Verified variants

| kappa | d | absorption coefficient | degree bound | support bound |
|---|---|---|---|---|
| 121/100 | 6 | 14641/17538 | 11774654098433 | <2^508 |
| 16/15 | 4 | 8/9 | 11212784195585 | <2^507 |

Both use13 total variables. Ordinary Szpiro suffices for the first;
ordinary rational abc suffices for both. The new separation does not
remove the contact estimate's requirement kappa<4/3.

Each source has1757 rational nodes,753 integer nodes,48 atomic guards.
Both exact source audits and all64 independent degree cases PASS. The
new target/scale identities are checked symbolically with a formal
coefficient shift. Fifteen independent finite-field formula evaluations
per variant are supplementary bounded evidence.

## Independent arithmetic audit

The height agent checked completeness for every nonzero integer n=X,
including negative/even n and n=+/-1. The source uses A=nP, H=hP,
U=hnP. CRT formal conditions work for any integer n; U=+/-A occurs
only at h=+/-1. Some tests vanish identically for n=+/-1, which is
allowed. Multiplication by[n] is nonconstant for every n!=0, so all
prepared domains can be chosen before contact-prime selection.

The quartic agent's independent exact audit also passed: all five finite
relations, all11 events, complete guard descriptions, and all point,
test, and pole expressions match the audited predecessor under exactly
the intended target and scale substitutions. Direct summation over
all32513 allowed separator exponents confirms the support bounds.
That audit is saved in `checkpoints/quartic_v22/direct_input13_audit.py`
and its JSON report. The height agent has also read the final TeX
transcription and approved both generalized power-height constants and
the complete source realization. No published leading file has been
modified by this work.
