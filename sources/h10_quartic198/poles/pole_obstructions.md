# Pole compression: exact findings

Source: Jose Brox repository, commit `d337a5500e2531139445bd7e30f966f62c4db03a`, especially `papers/pole_parameters/congruent_twist_poles_20261114_v27.tex` and the unbalanced 204-coordinate table.

This note establishes obstructions to several particular proposed reductions. It does **not** establish a lower bound for the number of variables and does not certify a new defining polynomial.

## 1. The new pole equations do not themselves save variables

The new system is

\[
 e^2+bp^2=1,\qquad uv=e(1-b),\qquad u^2-v^2=bq^2.
\]

It has five basic witnesses but needs the two square outputs `p2=p^2`, `q2=q^2` to become quadratic. Thus it has seven auxiliary coordinates, exactly as does the existing pole in the 204-coordinate construction. Its coefficients are smaller; its realization consumes Jaswal's simultaneous-twist theorem rather than merely the previously retained pole-realization premise. A direct substitution is consequently neither a variable improvement nor automatically an implication under precisely the same list of premises.

## 2. A tempting four-coordinate replacement fails

Set `u=e` in the new equations. If `b` is not a rational square, the first equation forces `e != 0`; the middle equation then gives `v=1-b`. Eliminating `e^2` from the last equation gives

\[
 p^2+q^2=2-b.
\]

Consequently this restriction can be represented using only `e,p,q,p2`: `p2=p^2`, `e^2+b*p2=1`, `p2+q^2=2-b`. It would save three coordinates per pole, but it fails the actual prepared-input converse.

Take

\[
 b=409(204/5011)^2=17020944/25110121.
\]

Then `0<b<1`; its reduced denominator is a square; it is a square in each of `Q_2,Q_3,Q_17`; and its valuations there are respectively `4,2,2`. Thus it lies even in the older, more restrictive prepared class. However

\[
 2-b=33199298/25110121,\qquad v_{11}(2-b)=1.
\]

The valuation at a prime congruent to 3 modulo 4 of a nonzero sum of two rational squares is even: after factoring out the smaller of the two square valuations, cancellation would make `-1` a residue square. Since `11=3 mod 4`, no `p,q` exist. The restriction `u=e` is therefore invalid.

For completeness, the local square checks are exact. The squarefree part is 409, which is 1 modulo 8, 1 modulo 3 and 1 modulo 17. The square multiplier is `(204/5011)^2`, giving the indicated even valuations. The rational `b` is not a square because 409 is prime.

## 3. Fixing `u=1` also fails

Let `b=409(204/1013^2)^2`. This is positive and less than one, and again has the same prepared squareclasses and depths at 2,3,17. At `ell=1013`, one has `v(b)=-4`, while both 409 and -409 are nonsquare units: `ell=1 mod 4` and `409^506=-1 mod ell`.

Suppose the pole equations had `u=1`. The first equation forces `v(e)=0` and `v(p)>=2`; otherwise its smallest-valuation terms cannot cancel because `-b` has nonsquare unit part. Then `v=e(1-b)` has valuation -4. The third equation `1-v^2=bq^2` has left side of valuation -8 and leading unit class -1, whereas its right side has unit squareclass 409. This is impossible because -409 is nonsquare modulo 1013. Thus this other natural reduction of the free twist parameter also fails.

## 4. Product merger of the two contact coefficients loses parity

Write the current symmetric contact coefficient as

\[
 R(t)=\prod_{\theta\in\Theta}(t-\theta)/(t-1)^{10},
 \qquad \Theta=\Theta_0\cup(2-\Theta_0).
\]

Then `R(2-t)=R(t)`. In the current additive construction, `t0=lambda`, `t1=lambda+T`. On the locus

\[
 \lambda=1-T/2
\]

one has `t1=2-t0` and hence `R(t0)R(t1)=R(t0)^2`. Multiplying the two pole inputs therefore erases every odd valuation of these coefficients, independently of the trace squares. For sufficiently large real `T`, both weights `q_j=1/R(t_j)-1` are positive, so a positivity restriction does not remove this obstruction.

This rules out the straightforward product merger. It does not rule out a differently constructed single detector, or an argument that controls common contact primes by other means.

## 5. Circuit observations without a theorem of optimality

Each of the current five factors packs one arbitrary-valuation comparison square in an odd valuation class, one squared reciprocal in class 2 modulo 4, and one fourth power of a reciprocal in class 4 modulo 8. Together with the constant term, these classes give a unique minimum and force each factor valuation to be nonpositive. The fourth powers are doing arithmetic work, rather than simply reflecting an unnecessarily high polynomial degree.

A naive binary norm tree `N_r(x,y)=x^2+r*y^2` is not automatically smaller: each internal operation needs the square output for its right input unless that output is already shared. Its algebraic count must include these gates. Conversely, replacing fourth powers by squares permits a nonconstant summand to have valuation zero and cancel the constant, so a positive valuation of one factor can compensate a negative valuation of another. No valid compression of this kind has yet been obtained.

Absorbing the squared reciprocal trace from `B(1+q)=gamma^2*tau^2` into the two pole variables removes `B*p^2` and `B*q^2`, but introduces `(1+q)*e^2` and `e*tau^2` in the other equations. The naive quadratization adds back the square/product outputs just removed. This observation is not an impossibility proof for a more sophisticated coordinate change.

## 6. A narrow remaining question for the two-witness pole

The earlier proposal

\[
 Y^2=1+b(1+bv^2)^2
\]

has the right negative-odd-valuation obstruction, but the repository proves it incomplete on the full prepared-input class. That argument uses a prime `p=1 mod 4` where `b` has negative even valuation and nonsquare leading unit. There is a genuine reason this particular counterexample does not immediately settle the actual contact-shaped inputs.

Outside the fixed contact bad-prime set, all five squared distances `alpha_i=(1-theta_i)^2` are p-adic square units. Put `delta=t-1` and

\[
 R(t)=\prod_{i=1}^5(1-\alpha_i/\delta^2).
\]

If `v_p(R(t))<0`, necessarily `v_p(delta)>0`; each factor then has valuation `-2v_p(delta)`. Therefore

\[
 R(t)\delta^{10}\equiv-\prod_i\alpha_i\pmod p,
\]

so its leading unit has squareclass `-1`. Multiplication by the actual trace square and `gamma^2` preserves this leading squareclass when the trace has valuation zero. In particular, the repository's obstruction cannot occur at a pole contributed by `R(t)` itself at a prime `p=1 mod 4`.

This qualification does **not** prove local or global realization for the actual pole input. A negative even valuation can instead be contributed by the trace factor at a prime where `R(t)` is a nonsquare unit. Nor does everywhere local solvability, if separately proved on some further subfamily, imply rational solvability of the genus-one equation. No exact point follows merely from `b=gamma^2*R(t)*tau^2`.
