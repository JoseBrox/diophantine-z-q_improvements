# Checkpoint: the three Pell norms do not by themselves certify c

**Status: a proved obstruction and an unresolved full-source question.**
No integer predicate is removed and no variable count is improved here.
The present complete tables still certify the integrality of c.

The exact rational counterfamily below satisfies the first linear
congruence, all three Pell norms, and the one-quotient third-Pell
equation with integral quotients, but has c=1/5. It does **not**
satisfy the full source or its small-Pell closeness inequality.
It therefore rules out an argument using only that norm subsystem,
not a possible integrality theorem using the remaining source equations.

## What the first linear row already proves

Put D=4a−5 and Δ=a²−1. Suppose a and
T=bw+Dγ are integers, and rational c,d satisfy

    d=(a−2)c+T,                 d²−Δc²=1.

Substitution gives

    D c²−2(a−2)T c−(T²−1)=0.

For c=u/v in lowest terms with v>0, reduction of the denominator-cleared
equation modulo v gives v | D. Thus every denominator prime is odd.
The exact identity

    16Δ = (4a−5)(4a+5)+9

also gives gcd(D,Δ) | 9. In particular the possible common factor is
controlled by 9, not 21. At every denominator prime p≠3,
Δ≡(3/4)² mod p, a nonzero square. A nonsquare-discriminant argument
cannot exclude those primes.

## An exact nonintegral family for the norm subsystem

For any odd integer B≥3, set

| Coordinate | Value |
|---|---:|
| a | 5 |
| c | 1/5 |
| d | −7/5 |
| b | 2 |
| w | 14 |
| γ | −2 |
| i | 250 |
| F | 49 |
| J | −1812−245B |
| G | −45594/5 |
| H | −91188/5 |
| I | 4157625647/25 |

These values satisfy, exactly,

    d = bw+(a−2)c+(4a−5)γ,
    d²−(a²−1)c² = 1,
    F²−(a²−1)i²c⁴ = 1,
    G = a+F²(c+1−a),
    H = c+F²(B−c)+cFJ,
    I²−(G²−1)H² = 1.

Indeed the first linear right side is 28+3/5−30=−7/5.
The first norm is (49−24)/25=1, and the second is
49²−24·100=1. The formulas for G and H follow by direct substitution;
the B terms cancel in H. Finally H=2G and I=2G²−1, so the
third norm is the polynomial identity

    (2G²−1)²−(G²−1)(2G)² = 1.

The quotients γ,i,J are integers and i≠0. If a positive J is
desired, replacing F,J by −F,−J changes neither the bridge nor H.
This optional sign change still does not make the tuple a full source
witness.

The missing hypotheses are substantive. Here |c|=1/5<B. More
decisively, for any nonzero integer k and any integer Y with |Y|≥16,

    |c/k−Y| ≥ 16−1/5 > 1/2.

Thus the required small-Pell closeness inequality cannot hold.
Also a=5 is incompatible with a=(wM+1)rsM for the source's positive
r, M≥16 and nonzero integer s at w=14. No full-source counterexample
is asserted.

## Local solvability persists at denominator primes

The following lemma explains why the second and third norms alone
provide no local obstruction at an odd denominator prime.

**Lemma.** Let p be odd, a,B∈Z_p, and c∈Q_p satisfy v_p(c)=−k<0.
Choose any nonzero i∈p^(2k+1) Z_p and any unit J∈Z_p. There exist
F,I∈Q_p satisfying the second norm, the definitions of G,H above,
and the third norm. One may choose

    v_p(F)=0,       v_p(G)=v_p(H)=−k,       v_p(I)=−2k.

**Proof.** Since Δ is p-integral,
v_p(Δi²c⁴)≥2. Hensel's lemma gives the root F≡1 mod p of
F²=1+Δi²c⁴. In the bridge, F²c is the unique term of negative
valuation, hence v_p(G)=−k. In
H=F²B+c(1−F²+FJ), the coefficient of c is a unit, because
1−F² lies in p²Z_p and FJ is a unit. Therefore v_p(H)=−k.
Now

    1+(G²−1)H² = G²H² [1−G^(−2)+(GH)^(−2)].

The bracket belongs to 1+p^(2k)Z_p and has a square root by Hensel's
lemma. Multiplication by GH gives I with the stated valuation.
This proves the lemma.

The lemma requires only local integrality of i,J and does not assert
that these locally chosen square roots are rational. It is a local
solvability statement, separate from the exact rational counterfamily.
The first norm itself also admits denominator examples at all odd
p≠3 dividing D: take

    c=2(a−2)/D,       d=(2a²−4a+3)/D,       T=1.

Then c has valuation −v_p(D). At p=3 an explicit example is
a=8,c=4/9,d=11/3,T=1. These identities and the local continuation
are checked below.

## Reproducibility and the remaining question

Run:

    python undecidability/c_integrality_checkpoint_v102/verify_c_obstruction.py

The independent script verifies the symbolic identities, the exact
counterfamily, denominator examples, and finite Hensel lifts at several
odd primes. Its deterministic receipt is certificate.json. The finite
lifts illustrate the local lemma; its quantified proof is given above.
Regenerate the receipt with the explicit --write-certificate option.

The remaining question is whether the complete small-Pell equations,
their closeness inequality, the source identities for a,p,r,M, and the
other integral inputs exclude every surviving denominator. Neither
the counterfamily nor the local lemma settles that question. A future
removal of the c predicate must use those additional constraints or
a genuinely global argument.
