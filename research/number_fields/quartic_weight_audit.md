# Independent audit of the pure-power weight replacement

9 November 2026. The conclusions below concern the proposed 297/342-coordinate constructions and retain all arithmetic premises of the 301/351-coordinate sources.

## 1. Exact domain and zero branches

The unchanged rows assert F(t)e=(a delta)^5 and q delta^3=e, where a is a nonzero rational square, delta=t−1, and no root of F equals 1. Thus F(t) cannot vanish. Whenever delta is nonzero, e and q are nonzero. The new rows

- q2=q^2;
- q4=q2^2;
- c q4=q;
- q8=q4^2;
- c q19=q8^2;
- q38=q19^2;
- c q79=q38^2

then force c=q^(−3), q19=q^19, q38=q^38, q79=q^79. All rows are quadratic.

If q=0, the two unchanged rows force e=0 and delta=0. In that branch t=1 and the contact radical M(t)=1, so no contact-prime divisibility is consumed. The argument need not claim that the new chain has its intended rational interpretation on that branch. In particular one must not globally cancel q or impose an unproved inverse condition. The soundness proof uses cancellation only at a consumed contact, where delta is a unit. Completeness chooses delta nonzero by making lambda large.

## 2. Contact-prime soundness

For every consumed prime p, delta is a p-adic unit, nu=v_p(R) is odd, and q=1/(R delta^4). Therefore v(q^(2m−1))=(1−2m)nu. This is exactly the valuation of the old weight q_m=R^(1−2m)delta^(−2m−2).

Each nonzero summand at position j has valuation 2^j((1−2m)nu+2v(D)), an odd integer times 2^j. Distinct positions cannot cancel. The unchanged literal trace rows imply W nonzero, w0 nonzero, T0=1/Tr(W^(−1)) nonzero, and b=R/Tr(W^(−1))^2. The original pole-obstruction argument therefore yields every required order at one common place, with no new loss or change in the orders 1,10,40.

## 3. Finite preparation, with an explicit sufficient choice

Fix the root data, nonzero square scales a_i, and finite-place neighborhoods on which all test functions have a common lower bound for their valuations. Include the finitely many relevant denominator primes in S. At p in S, choose v_p(lambda) so negative that for every scale t_i=a_i lambda its valuation is smaller than 0 and than every finite valuation v_p(theta) for nonzero theta in Theta. Then

v_p(delta_i)=v_p(t_i),
v_p(F(t_i))=5v_p(t_i),
v_p(e_i)=5v_p(a_i),
v_p(q_i)=2v_p(a_i)−3v_p(lambda).

Consequently every q_i^(2m−1)D^2 has arbitrarily large positive valuation when v_p(lambda) is made sufficiently negative, uniformly on the fixed neighborhoods. Taking its powers in the mixed factors preserves smallness. This makes W arbitrarily close to 1, and Tr(W^(−1)) arbitrarily close to 2. At p=2 the preparation must be sufficiently deep to preserve valuation exactly 1 of that trace, rather than incorrectly calling it a unit.

Write lambda=u/(D0^2 w^2). The theta=0 prime in the pattern is u itself, which can be required to avoid S. Choose the fixed integer D0 sufficiently divisible at S before the prime-pattern theorem is applied. Then v_p(lambda)=−2v_p(D0)−2v_p(w) is bounded above by the prescribed sufficiently negative value. This is fixed finite divisibility already permitted by the inherited selection premise.

## 4. All denominator primes and local squareclasses

The unchanged exact product identity is

R = product_theta (u−(theta/a) D0^2 w^2) / ((D0^2 w^2)^5 delta^6).

Its denominator is a rational square. At selected contacts, v_p(R)=1. At every other prime its valuation is even. At each selected split contact the primary W is 1 modulo p, and the opposite W either is 1 modulo p or has negative valuation. Thus Tr(W^(−1)) is congruent to 2 or 1 modulo p and is a unit. The pole input b has valuation 1 there and even valuation elsewhere; its reduced denominator is a square. The prescribed local squareclasses of the selected primes supply those of R and b at 2,3,17. The new coefficients c=q^(−3) need not be integral and cause no extra restriction: they are rational witnesses only.

## 5. Real preparation and scalar parameter

For fixed a>0 and lambda tending to positive infinity, R~a^(−6)lambda^(−1) and q~a^2 lambda^(−3). Therefore q^(2m−1)~a^(4m−2)lambda^(−3(2m−1)). The new weights are positive and decay at least as rapidly as the old ones. On the fixed compact neighborhoods all mixed factors approach 1 and b approaches 0 from above. The weighted-selection premise is not strengthened. The numerical scalar parameter is used only in soundness and is unchanged.

## Audit conclusion

The mathematical replacement is valid on the consumed-contact domain and preserves simultaneous completeness under exactly the previous arithmetic contract. No independent validation of the deep source arithmetic premises is claimed here. Exact full coefficient checks and variable counts remain the responsibility of the independent generator/checker pair.
