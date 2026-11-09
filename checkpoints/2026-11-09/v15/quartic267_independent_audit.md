# Independent audit of the 267-variable quartic normalization

Auditor: few_variables agent. Date: 9 November 2026.

## Literal discrepancy in the superseded numerator

Reading the pinned 273-variable quadratic table directly, write a=c343 and t=c391. Its rows 349, 350, 351, 20100, 20101, and 352 give

- c395 = a t;
- c396 = (4 c395-a)^2 = a^2(4t-1)^2;
- c397 = c396^2 = a^4(4t-1)^4;
- c20100 = c395 c397 = a^5 t(4t-1)^4;
- c20101 = c20100^2 = a^10 t^2(4t-1)^8;
- F20(t)e = c20101^2 = a^20 t^4(4t-1)^16.

Thus the literal table does not encode the asserted numerator a^20(t-1)^20. The same chain occurs in the 279-variable family and survives into 272. This is an exact circuit discrepancy, not a demonstrated counterexample to the rational projection of those tables. Their claimed projection cannot be inherited from the stated normalization proof.

The new 267-variable construction removes this chain. It replaces row 352 by F20(t)e=V10(t)^2, where the existing triangular contact circuit gives V10(t)=(t-1)^10 at every rational input. It also replaces the scale equation by 2t=lambda(c82+c84+2c86+c88). The chart equations identify the resulting scale as one quarter of the trace of the sum of the four root abscissas. This is positive and nonzero. Multiplication of the aggregate trace by a fixed nonzero rational changes its height by a fixed additive constant only.

## Scale-independent normalization

For arbitrary fixed positive rational a, put t=a lambda, delta=t-1, and

R=F20(t)/delta^22, e=delta^20/F20(t), q=delta^18/F20(t).

The literal equations are F20(t)e=delta^20, q delta^2=e, and e delta^2 b=tau^2, together with the original trace equation. On delta!=0 they imply b=R/Tr(W^-1)^2 whenever the local noncancellation argument gives W!=0.

At a contact prime outside the fixed exceptional set, delta is a unit and v(F20(t)) is positive odd. Hence v(R) is positive odd and v(q)=-v(R); every factor-valuation and extraction argument is unchanged. The contact polynomial cannot vanish: its vanishing would force delta=0, contrary to 1 not being a contact. If q=0 then e=0 and delta=0. At delta=0 no reciprocal formula is used, and the certified contact radical M4(1)=1 suffices for the height argument. The converse delta=0 implies q=0 is not asserted and is unnecessary.

## Simultaneous prime preparation with a nonsquare scale

Sun, arXiv:2610.20691v2, Theorem 4.1 was inspected directly at
https://arxiv.org/html/2610.20691v2 .
It accepts any fixed finite distinct integer coefficient list, arbitrary fixed divisibility of w, lower prime and slope bounds, and the stated simultaneous order conditions. Repeated positions may be removed. No square condition on the resulting rational scales is required by this theorem.

Choose a fixed positive integer D0 with D0^2 theta/a integral for every scale and contact, enlarging D0 for all fixed local preparation. Set v=D0^2 w^2 and lambda=u/v. The coefficient list is c=-D0^2 theta/a, with repeated values removed. The exact identity is

R = a^20 product_theta(u-(theta/a)v)/(v^20 delta^22).

All displayed extra factors are rational squares, even when a is nonsquare. Outside the selected prime numerators, valuations of R and of the pole input are even. At a selected prime, after fixed numerator and denominator primes have been avoided, its valuation is one. The existing finite denominator-dilation and order-separation arguments therefore apply to a=T as well as a=1.

At a fixed prepared prime, choose v_p(t) sufficiently negative. Then

v_p(e)=0, v_p(q)=v_p(R)=-2v_p(t),

and

R = delta^-2 product_theta(1+(1-theta)/delta).

Each factor can be made arbitrarily close to one, giving the required local squareclass, including at 2 by choosing depth at least three. The weighted tests tend p-adically to zero, W tends to one, and Tr(W^-1) tends to two. The required pole-input valuation lower bounds follow by increasing the fixed denominator divisibility.

On the fixed real compact neighborhoods and as lambda tends to positive infinity, R and q are asymptotic to (a lambda)^-2, W tends to one, and the pole input is asymptotic to 1/[4(a lambda)^2]. Thus both pole inputs are positive and eventually smaller than the required bound.

## Height transfer

Using scales 1 and T gives h(T)<=h(lambda)+h(T lambda). The previous scale T^2 gave 2h(T) on the left. This change only doubles the fixed constant in the aggregate-height transfer and may alter its fixed additive term because of the trace normalization. None of the decisive exponents changes. In particular the exponent 19/12 remains below two, and the final sublinear exponent in the scalar parameter remains unchanged. The eventual coefficient threshold remains ineffective.

## Audit status

PASS for the new scale-independent normalization, arbitrary positive rational scale T, exceptional zero strata, and preservation of the existing arithmetic hypotheses. The separate 267-variable checker is responsible for the complete coefficient-table reconstruction and expansion. No additional arithmetic conjecture is introduced by this normalization. The old table discrepancy must not be obscured by claiming projection equivalence with every old witness.
