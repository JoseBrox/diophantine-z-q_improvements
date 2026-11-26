# Reciprocal normalization of moving differences and higher-depth comparisons

27 November 2026. Research checkpoint, based on 6864691d536057574be873667936610da6a4ea99. No new defining-variable record and no change to the existing 161/175/52 quartic bounds. The results concern the ordinary-abc 52-variable route with its previously retained arithmetic premises.

## Exact guarded quadratic moving-difference chart

Use K=Q(rho), rho^2=2, a=1+rho, b=4-2rho, delta=a-b^2, D=a delta=11-6rho, P=(a,ab)=R0. For field coordinates r,q,k put the affine expressions

    L=(1-2 b k-a(r+q))/delta,
    S*=1-b k-a r, T*=a q-1+b k.

Require arq=k^2=L and g Tr(L)=1, where g is a single rational coordinate. The trace of k^2 is 2(k0^2+2 k1^2), so k!=0, and arq=k^2 gives r,q!=0. The inverse map v_H=1/k, u_H=r/k, w_H=q/k recovers exactly the two reference equations of v65:

    a u_H w_H=1,
    v_H(v_H-a(u_H+w_H)-2b)=delta.

Thus r=f(H), q=f(H-P), S*=k S_H, T*=k S_(H-P), where f=1/x and S=y/x. Conversely the original reference chart gives a unique lift including g. This uses the entire v40/v65 reference chart, including its tangent fibers.

In the physical v65 pair chart, write s=X S_U, t=X S_V, F=X^2 f(U), G=X^2 f(V), p=h+s+t, d=pF=hG, D(F+G)=(s-t)h-t^2, X^4=d(s-t)-DFG. The physical tests are J=rF, K'=qG, C2=(s-S_H)^2, I2=(t-S_(H-P))^2. Set s'=ks, t'=kt, h'=kh, d'=kd, p'=h'+s'+t'. Instead of F,G store J,K' directly, and use one full field coordinate A for the moving-difference abscissa:

    r d'=p'J,
    q d'=h'K',
    Da(qJ+rK')=(s'-t')h'-t'^2,
    L X4=d'(s'-t')-Da JK',
    L A=h'p',
    L C2=(s'-S*)^2,
    L I2=(t'-T*)^2.

Here X4=X^4 is the old input-power coordinate. These are quadratic in the rational components. Dividing by the established nonzero r k, q k, and L=k^2=arq recovers the original pair chart, all raw test values and A=hp. Conversely substitution gives all displayed equations. Thus the original v65 pair theorem proves A=X^2 x(U-V) for nonzero X, including tangencies and every finite two-torsion difference. This is the physical trace, independent of the reference on the canonical multiplication family, so its preparation order is unchanged. The X=0 fiber also lifts by the same algebraic map: use H=2R0, s=S_H, t=S_(H-P), F=G=d=J=K'=0, h=t^2/(s-t), A=hp. The exact norm of s-t there is 7199/328.

The unpacked reference/point/comparison block changes from 27 to 25 rational coordinates, and from 21 to 19 quadratic rows (excluding shared input-power and detector registers). Old: 6 reference, 12 pair, 4 product, 1 half-trace, 4 square coordinates. New: 6 reference, 12 pair including products, 2 difference, 1 guard, 4 squares. Both private reciprocal-abscissa field registers are removed. The guard is essential: k=0,r=0,q=1/a, s'=1, t'=h'=d'=J=K'=C2=I2=0 satisfies all remaining equations with arbitrary X,A. Hence the unguarded moving difference is false.

## Stronger comparison at every consumed odd depth

In the current reciprocal-gate construction use u=1/c and mu=v_p(u)>0 odd, outside the fixed exceptional set. The 53-coordinate proof, section 2, gives v_p(D_gate)>-mu/2. Its norm/trace equation D_gate Tr(W)=Nm(W-1) yields a slot with v(W)>-mu/2: if both slots are negative, v_p(D_gate)<=max(v(W),v(bar W)); otherwise use a nonnegative slot. The terms of W=1+c C^4+c^2 J^2-c^3 bar(I)^4-c^4 bar(K')^2 have distinct nonconstant classes modulo four (J,K' have even valuations); the only constant tie can occur at zero. A negative minimum is unique, and each term must exceed -mu/2. Thus

    v(C)>mu/8, v(J)>3mu/4, v(I)>5mu/8, v(K')>7mu/4,

with the last pair evaluated at the conjugate slot. The parent v65 inverse lemma supplies integrality of X, and for unit X both relevant pairs are formal with equal reference/numerator depth d1 and d2 in their respective slots. Their reciprocal products have valuations 4d1 and 4d2. Therefore the parameter ratio errors have depth at least

    e1=floor(mu/8)+floor(3mu/16)+2,
    e2=floor(5mu/8)+floor(7mu/16)+2.

At good p>5 the invariant differential on the given short Weierstrass curve has integral formal coefficients with first nonconstant term of degree four. For n>=5 and depth d>=1, integration loses at most v_p(n), and (n-1)d-v_p(n)>=4d. Consequently the relative formal-logarithm errors have depths at least 4d_i>=e1, and e2>=e1. The ordinary ratio of logarithms is the ratio of integral free labels (doubling removes the torsion). Multiply the two comparisons by the respective reference labels h0 and h0-1, which are integers. Subtracting proves, for m the integral label of U-V,

    v_p(m-X)>=floor(mu/8)+floor(3mu/16)+2   if v_p(X)=0.

In particular v_p(m-X)>=2 at every consumed prime where X is a unit. For positive v_p(X), only p|num(X) is asserted. For X nonzero and X!=m, split the consumed squarefree radical into M0 supported on the input numerator and M1 on unit-input primes. Writing X=c1/d1 reduced gives M0||c1| and M1^2||m d1-c1|. Hence

    log M_u <= (3/2) h(X)+(1/2) log(1+|m|).

Combining this with the 52-route denominator-sensitive estimate R_u>=(347/200)H-(3/4)h(X)-O(1) and h(X)<=(501/997)H+O(1) gives improved strict margin 120509/199400, in place of 70409/199400. The same trace-index argument works; no new numerical defining cutoff follows.

## Scope of remaining packing problem

The actual 52 table uses two hyperbolic pairs, not an unpacked block appended to an unchanged detector. Inserting the old comparison pair, 2C2=U+c V_s and 2bar(I2)=u U-V_s, in the new normalized comparison rows produces cubic terms c L V_s and u bar(L) U. The reciprocal-product pair similarly introduces higher-degree terms in the new pair rows. In the symmetric-scale diagonal-gauge model, with r,q,k of common weight w and s',t',h' of common weight z, the secant and comparison equations force J,K',C2,I2 to have common weight 2z-w, incompatible with their odd-offset hyperbolic packing without further changes. This is a restricted obstruction, not a lower bound for all charts. The exact new 25-coordinate block therefore does NOT imply a 50-variable defining quartic. Joint packing or a new detector with complete prepared-pole realizations remains necessary. The 161/175 general constructions need separate comparison interfaces; no transfer is asserted.

## Source references

Pinned source 6864691d536057574be873667936610da6a4ea99: papers/quartic_existence/quartic_abc68_20261117_v65.tex (reference, pair, inverse lemma, local proposition and zero fiber); papers/elliptic_charts/three_coordinate_reference_20261115_v40.tex; computation/denominator_radical52_20261125/README.md and quadrics.json; computation/reciprocal_gate53_20261124/README.md sections 1-3. The published arithmetic suppliers and their hypothesis qualifications are inherited, not independently reproved in this checkpoint.

Exact local replay: universal residual identities; 32 allowed reference fixtures, 2244 pair/scale fixtures, including 64 tangent and 196 finite torsion-difference fixtures (68 of abscissa zero); canonical zero-input and missing-guard negative controls; 25000 depth profiles and revised height margin. The accompanying local Python/SymPy checker and full detailed note were delivered separately. These tests supplement the exact proofs; they do not prove the retained group, prime-pattern, abc or BB realization results.
