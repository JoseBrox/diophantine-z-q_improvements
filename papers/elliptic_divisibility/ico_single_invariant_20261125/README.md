# Ordinary-abc elimination of the generic coefficient anchor; seven-coordinate single-invariant candidate

25 November 2026. This is a project-specific continuation of the [eight-coordinate coefficient anchor](../ico_coefficient_anchor_20261125/README.md). It assumes ordinary rational abc, already retained there, and does not assume generalized Szpiro. It does not improve an established defining-polynomial count.

## 1. Uniform height obstruction for all branches except b=0

Let Z be a rational point on the guarded ico chart, and z its primitive integral representative (all five coordinates nonzero). Put s=σ1(z), u=σ3(z), c=σ5(z), and T=log max |z_i|. Write h for logarithmic Weil height (h(0)=0) in this note. The coefficient equation is

    s^15 + a u^5 + b c^3 = 0,       L=h(a)+h(b).

Here s,u,c are nonzero: s²=sum z_i², so |s|≥exp T; moreover, with x_i=z_i/s, sum x_i²=1, all x_i nonzero, and each |x_i|<1. Newton's identity gives 3u/s³=sum x_i³-1<0. Finally c=product z_i≠0. Thus the only degenerate branches of the coefficient equation are a=0 or b=0, not zero invariant values.

**Theorem.** Under ordinary rational abc, whenever b≠0,

    T ≤ (61/12)L + O(1).                                      (1)

The constant is absolute after fixing the exponent 6/5 in abc. In particular the eight-coordinate anchor's budget L≤q h_ref²/100+O(1) and w=g_U with U=[m h_ref]P imply that |m| is bounded on this branch. No additional height conjecture is used.

### Both coefficients nonzero

Clear denominators with d=lcm(den a,den b)>0, A=da, B=db. All |A|, |B|, d≤exp L. At every prime at least one of s,u,c is a unit: otherwise the characteristic polynomial of the coordinates, T0^5-sT0^4-uT0²-c, is T0^5 modulo p, contradicting primitivity. Thus gcd(ds^15,Au^5,Bc^3) divides |dAB|. Their primitive abc triple has log maximum at least 15T-3L, and log radical at most 9T+3L+O(1) since s,u,c have degrees 1,3,5. Ordinary abc at exponent 6/5 yields

    (15-54/5)T ≤ (3+18/5)L+O(1),
    T ≤ (11/7)L+O(1).

This uses the actual small off-diagonal heights, not just small diagonal support. It is inapplicable to unbounded integer mixed coefficients.

### The a=0 branch

Here b=-(s^5/c)^3≠0. We give the needed reciprocal valuation argument to avoid assuming any conjectural bound for degenerate coefficient triples.

Let f_i be a primitive integral reciprocal vector. The ico equations are equivalent to sum f_i=sum f_i³=0. For e={i,j}, define d_e=gcd(|f_k|: k∉e) and write D=product_e d_e. Define r_i=|f_i|/product_{e not containing i}d_e and R=product_i r_i. The following local facts follow from the identity, for the complementary triple {k,l,n},

    (f_k+f_l)(f_k+f_n)(f_l+f_n)=-f_i f_j(f_i+f_j).

No pair sum vanishes, since its complementary triple would have sum and sum of cubes zero and hence contain a zero coordinate. A primitive f has 2, 4, or 5 units modulo any prime. Indeed, one unit contradicts sum zero; three units would make all three complementary pair sums units (their sum is zero modulo p), contradicting the identity for the two nonunits. With five units, all pair sums are units by the same identity.

With two units i,j the remaining valuations are a0≤a1≤a2, a0>0. If a0<a1, their sum has valuation a0, but the product of pair sums has valuation at least 3a0, contradicting the identity. Thus a1=a0, and write a2=a0+b0, b0≥0. Exactly d_{ij} has valuation a0; if b0>0 precisely the highest-depth r has valuation b0. With four units there is only one positive valuation, contributed to its r_i, and all d_e are units. This proves the d_e and the r_i are integers, pairwise coprime within their respective lists. The lcm of |f_i| is DR, and primitive z_i=(DR)/f_i. Hence

    |z_i| = (R/r_i) product_{e containing i} d_e,
    |c|=D²R⁴,
    B(Z)=rad(R),
    T≤log D+log R.

At a boundary prime, s is a unit and v_p(c)≥4v_p(R). Consequently R^12 divides the denominator of b, so log R≤L/12, where here L=h(b). At a nonboundary prime p dividing d_e of depth a0>0, v_p(c)=2a0. If p is not in the numerator/denominator support of b, the coefficient relation gives 15v_p(s)=6a0; in particular 5|a0. Let D_g denote the product of primes dividing D outside B(Z). Since b is a rational cube up to sign, its numerator/denominator radical has log at most 2L/3. Therefore

    log D_g ≤ (1/5)log D+(2/3)L.                               (2)

For the ten primitive rational abc triples proportional to f_i,f_j,f_i+f_j, a nonboundary prime dividing d_e can contribute to their radicals only if e meets {i,j}, exactly seven possible pairs. To see this, at this prime the three nonunits all have the same depth a0. Their scaled residues sum to zero by the complementary identity, and each scaled pair sum is a unit. Thus the primitive triple for any pair disjoint from e has no p in its radical. At nonboundary primes where all f_i are units, no pair sum vanishes modulo p, as proved above. Boundary primes can contribute to at most ten radicals. Summing ordinary abc with exponent 6/5, and using h(f_i:f_j)≤h(f_i:f_j:f_i+f_j), gives

    sum_{i<j} h(f_i:f_j) ≤ (6/5)(10 log B(Z)+7 log D_g)+O(1).   (3)

For the opposite direction, product |f_i|=D³R and the product of the ten pair gcds is D³: at a two-unit prime exactly the three pairs of nonunits have gcd depth a0; at a four- or five-unit prime none do. Thus

    sum_{i<j} h(f_i:f_j)
    =sum_{i<j} log max(|f_i|,|f_j|)-3 log D
    ≥ 2 sum_i log |f_i|-3 log D =3 log D+2 log R.

Insert (2), log B≤log R≤L/12 into (3). This gives (33/25)log D≤(33/5)L+O(1), i.e. log D≤5L+O(1). Therefore T≤(61/12)L+O(1), completing (1).

### Transfer to the actual reference

The inverse plane-chart formula is particularly inexpensive: w=-f_2/(f_1+f_4)=-z_1 z_4/[z_2(z_1+z_4)], so h(w)≤2T+log 2. The first equality follows directly from the factored chart in the [interpolation note](../ico_boundary_interpolation_20261125/README.md). If w=g_U and U=[m h_ref]P then h(w)=q m²h_ref²+O(1). Under the actual anchor budget L≤q h_ref²/100+O(1), equation (1) implies

    q m² h_ref² ≤ (61/600) q h_ref²+O(1).

Since q>0 and |h_ref|≥1, only bounded m can occur with b≠0. Moreover, beyond a sufficiently large fixed reference cutoff, no nonzero true multiplier can occur on that branch at all. This does not require a large-reference assumption for the bounded-m conclusion.

## 2. Seven-coordinate candidate and precise completeness implication

All witnesses for sufficiently large |m| in any complete eight-coordinate coefficient-anchor construction must therefore use b=0. On that branch define

    v=s³/u<0,     a=-v^5,     b=0.

These are rational functions of w,t; u is never zero on the guarded real rational chart. Substitute them in the actual original equations, including the recursive anchor (X,a,0). Its last update is identically the identity, because the third argument is zero. The resulting seven ordinary variables are exactly

    X, g_H, g_U, t, v_1, v_2, encoder.

The symbols v_1,v_2 are the original two pole coordinates, not the invariant v. This is a restriction and direct substitution in the sound eight-coordinate relation, with the same finite-character encoder, guards and retained arithmetic premises. In the unrestricted-degree compiler it introduces no ordinary variable. It is sound for integers wherever the original is sound.

If the eight-coordinate relation can be made complete, then its seven-coordinate restriction is complete outside a finite interval, by the uniform bound just proved. Multiply its defining relation by the finite integer polynomial product_{|k|≤M}(X-k), choosing a fixed M large enough, to restore completeness without adding variables. The cutoff M may be ineffective. Thus the existence of a complete eight-coordinate construction of the stated kind implies existence of a seven-coordinate one; there is not yet a proof of either. The implication does not assume one can select a larger reference while keeping a,b fixed.

A second, not logically equivalent, seven-coordinate variant uses the anchor arguments (X,v) instead of (X,-v^5). The cubic interpolation s³-vu=0 already gives B(Z) supported on den v (at a boundary prime s is a unit and u is not), so the intrinsic effective ico estimate applies. The two-argument version of the original height calculation gives

    2h(u_anchor)+h(X)+h(v) ≤ (171/191360)q h_ref²+O(1)
                          < q h_ref²/100+O(1).

Here u_anchor is the original adaptive scalar, not σ3. Its real bounds, pole soundness and comparison margin are unchanged or improved; the same direct cap proof therefore gives a sound seven-coordinate candidate. The substitution v instead of -v^5 changes the reference preparation, so completeness of the old branch does not imply completeness of this variant. No new degree ceiling is claimed.

## 3. Exact remaining cancellation condition

The remaining problem is now explicit: find guarded lifts at elliptic numerator points for which h(v)=h(s³/u) is small relative to q h_ref², with the actual scalar/reference preparation. This requires massive simultaneous prime-power cancellation in s and u, not merely small boundary radical.

For each p let k_p=min(v_p(s),v_p(u)). Since gcd(s³,u) has exponent at most 3k_p and the reduced numerator of v has size ≤exp h(v),

    sum_p k_p log p ≥ T-h(v)/3.

When k_p>0, c is a unit (primitivity). For p≠5, the coordinates modulo p are all five distinct roots of T0^5-c, so p≡1 mod 5. Over Q_p their ratios to a fixed coordinate agree modulo p^k_p with the five fifth roots of unity, by simple-root lifting. For p=5 one has k_p≤2: if k_p≥3, the fifth-power congruences imply each coordinate ratio is 1 modulo 25 (the valuation identity v_5(r^5-1)=v_5(r-1)+1 for r≡1 mod 5); then their sum is 5 modulo 25, contradicting v_5(s)≥3.

Scale f_2 to 1. The inverse formula w=-1/(f_1/f_2+f_4/f_2) and the fifth-root congruences imply, for p≠5 and k_p>0, that w is integral and

    v_p(F(w))≥k_p,
    F(W)=(W²+W-1)(W⁴-3W³+4W²-2W+1).

Indeed the product of 1+W(ζ^i+ζ^j) over 1≤i<j≤4 for a primitive fifth root ζ is -F(W). The pair denominator is a p-adic unit, because distinct fifth roots cannot be negatives at these primes. Hence

    sum_{p≡1 mod 5, v_p(w)≥0} max(0,v_p(F(w))) log p
       ≥ T-h(v)/3-2 log 5
       ≥ (h(w)-log 2)/2-h(v)/3-2 log 5.                    (4)

This bound identifies a fixed degree-six numerator contact divisor on the elliptic chart which any small-height lift must exploit. It does not provide an upper bound on that mass strong enough to prove impossibility, nor a global rational lift with the required simultaneous cancellations. Ordinary abc for fixed curves must not be confused with a uniform height bound on this varying pencil. A possible next step is a direct height inequality h(w)≪1+h(v) on the elliptic pullback of the cubic pencil, or a constructive family contradicting it and satisfying the prepared-reference constraints. Either outcome is relevant to the project's witness counts. A Szpiro-only counterexample outside those constraints would not prove completeness.

## 4. Exact checks and limitations

The finite exact check below can be run with Python and SymPy. It tests the two reciprocal product formulas, real nonvanishing, inverse formula, both denominator divisibilities and the degree-six contact congruences; it does not prove abc or any asymptotic height bound. Executed at coordinate-height bound 10, it passed 7,598 guarded chart pairs and 2,120 non-5 cancellation-prime fixtures (no 5-adic cancellation fixtures in this grid). The p=5 proof above is analytic and independent of these tests.

```python
from fractions import Fraction as Q
from itertools import combinations
from math import gcd,lcm,prod
from sympy import factorint

vals=sorted({Q(a,b) for b in range(1,11) for a in range(-10,11)}
            -{Q(0),Q(1)})
edges=list(combinations(range(5),2))
N=contacts=five=0
for i,w in enumerate(vals):
 for t in vals[i:]:
    a,b,c,d=w.numerator,w.denominator,t.numerator,t.denominator
    f=(b*(c-d)*(a*c+(a-b)*d),
       -d*(a-b)*((a+b)*c-b*d),
       -a*(b*c*c+(a-b)*d*d),
       -(b*c-a*d)*(b*c+(a-b)*d),
       c*(b*b*c+(a*a-b*b)*d))
    if not all(f): continue
    g=gcd(*f); f=tuple(x//g for x in f)
    z=tuple(lcm(*f)//x for x in f)
    assert gcd(*z)==1 and sum(f)==sum(x**3 for x in f)==0
    ds={e:gcd(*(f[k] for k in range(5) if k not in e)) for e in edges}
    D=prod(ds.values())
    rs=[abs(f[k])//prod(x for e,x in ds.items() if k not in e)
        for k in range(5)]
    R=prod(rs)
    s=sum(z); U=sum(prod(x) for x in combinations(z,3)); C=prod(z)
    assert s*s==sum(x*x for x in z) and s*U<0 and C
    assert -Q(f[2],f[1]+f[4])==w
    assert prod(map(abs,f))==D**3*R
    assert prod(gcd(a,b) for a,b in combinations(f,2))==D**3
    assert prod(max(abs(a),abs(b)) for a,b in combinations(f,2))>=prod(map(abs,f))**2
    F=(w*w+w-1)*(w**4-3*w**3+4*w*w-2*w+1)
    for p,k in factorint(gcd(s,U)).items():
        if p==5: assert k<=2; five+=1; continue
        assert p%5==1 and gcd(w.denominator,p)==1 and F.numerator%p**k==0
        contacts+=1
    assert (-Q(s**15,C**3)).denominator%R**12==0
    v=Q(s**3,U); assert v<0 and v.denominator%R**2==0
    N+=1
print(N,contacts,five)
```

The project status is unchanged for the established general/specified/ordinary-abc defining polynomials. The seven-coordinate result is a genuine conditional compression of the incomplete eight-coordinate approach, plus a stronger obstruction under its existing premise. No counterexample to Szpiro or proof of completeness is claimed.
