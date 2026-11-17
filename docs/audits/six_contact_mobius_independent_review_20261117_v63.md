# Independent internal review: finite menus of integer coupling exponents

**Verdict:** the stated theorem is proved. I found no essential gap in the extension to every fixed integer exponent at least four or to a fixed finite menu. The conclusion remains scoped to the prescribed root point, six-contact source, finite multiplier menu and common local pole implication. It does not rule out a chosen individual shift or arbitrary other constructions.

Audited source: `six_contact_mobius_obstruction_20261117_v63.tex`.
Source SHA-256: `ddffc8298135f4aa0558a88e4789a5bb0b12f9413284ca16bee52711448f2de5`.

## Root-field lemma and ramification

For odd `e`, the polynomial `Y^e+m` has at least one irreducible factor of odd degree. A root of that factor generates an odd-degree extension of Q, which cannot contain the quadratic field. This case requires only positive odd `m`, not its nonsquareness.

For even `e`, write `e=2^r s` with `r>=1` and `s` odd. Because `m` is an odd nonsquare, an odd prime `ell` has odd `v_ell(m)`. For any root `beta` of `Y^(2^r)+m`, a valuation above `ell` normalized by `v(ell)=1` has `v(beta)=v_ell(m)/2^r`, whose reduced denominator is exactly `2^r`. Its ramification index must therefore be divisible by `2^r`. The upper degree bound `[Q(beta):Q]<=2^r` forces equality, one prime above `ell`, ramification index `2^r`, and residue degree one.

This excludes `Q(sqrt(2))` inside `Q(beta)`: the quadratic field is unramified at `ell`; a split prime would give at least two primes upstairs, while an inert prime would force even residue degree. The argument does not incorrectly assume `Y^e+m` irreducible.

An irreducible odd-degree factor of `Y^s-beta` exists because its total degree is odd. A root `alpha` gives an odd extension of `Q(beta)`, and `beta=alpha^s` verifies that the smaller field is actually contained in `Q(alpha)`. Thus adjoining `alpha` cannot introduce the missing quadratic field. This completes the lemma for every even exponent, including those with nontrivial odd part.

For `m=57^e-4^(e+1)` with even `e`, put `k=e/2>=2` and `n=57^k`. The inequality `4*16^k<57^k<2*57^k-1` follows already at `k=2` and strengthens thereafter. Hence `(n-1)^2<m<n^2`; in particular `m` is positive, odd and nonsquare.

## Chebotarev step

The normal closure obtained by adjoining all binomial roots and `sqrt(2)` is finite Galois over Q. Since `sqrt(2)` is absent from the chosen root field, the nontrivial automorphism of its quadratic compositum extends to the normal closure while fixing the chosen root. Its conjugacy class therefore acts nontrivially on `Q(sqrt(2))` and has a fixed point in its action on the binomial roots. Every conjugate retains both properties.

Chebotarev supplies infinitely many primes with this conjugacy class. Excluding the polynomial discriminant gives simple roots modulo those primes, and exclusion of any additional finite set preserves infinitude. I opened the cited primary reference, Milne's *Algebraic Number Theory*, version 3.08 (19 July 2020), and verified that Theorem 8.31 is precisely the conjugacy-class density theorem. The reference is accurate: https://www.jmilne.org/math/CourseNotes/ANT.pdf, printed page 147 (PDF page 149).

## Exact-valuation lifting and finite-menu progression

For a root `y_e mod p_e`, the congruence `B+1=y_e/4 mod p_e` gives `a_e(B)=4 mod p_e`. Avoiding primes dividing `e*m` ensures that `e(B+1)^(e-1)` is a unit. Exactly one lift modulo `p_e^2` has `a_e(B)=4 mod p_e^2`; every other lift gives exact valuation one for `a_e(B)-4`. Since `H'(4)=11250=2*3^2*5^4` and the exceptional set contains 2,3,5, the valuation of `H(a_e(B))` is also exactly one.

Distinct primes can be chosen successively by the infinite-prime result. CRT with the parity condition then produces one odd progression satisfying every exact-valuation condition. This is stronger than choosing an unrelated progression for each exponent. The coefficient multipliers are units at the chosen primes after their finite supports are excluded.

At the involution, `t_0=-1/4`, `t_1=-1 mod p_e`. Thus both `t_j-1`, the Möbius denominator, and all denominators of the factorization are units. Both detector weights and contact inputs have valuation one. The inert-place argument applies to either retained pole condition separately.

## Uniform square gaps

The ten discriminant identities and all initial values `g_4` are correct. The recurrence

```text
g_(e+1)-16*g_e = 82*delta^2*57^e - 24*c*4^e + 15
```

is exact. Its right-hand side is positive because `delta^2>=1`, `c<=5`, and `57^e>2*4^e`. Induction proves every required integer-exponent gap, not only the sample values. Positivity of `2N-1-|K_0|q^2` also forces `N>0`; the quantities lie strictly between consecutive integer squares. A rational solution of the quadratic coupling would make its integer discriminant an integer square, so the contradiction is valid.

## Inert-place obstruction

At an inert prime different from 2 and 7, the curve has good reduction and the fixed point P reduces to a nonidentity affine point. The two reciprocal tests cannot both have positive valuation, because conjugation fixes the unique prime and would put both H and H-P in the formal subgroup. At least one factor in W therefore has valuation at most -1. All other factors have nonpositive valuation by the odd/even comparison, without cancellation. Hence the inverse product lies in `p O_Kp`, and its trace lies in `p Z_p`. A nonzero trace makes `v_p(b)=1-2v_p(V)` negative odd; a zero trace violates the retained guard. This works for every auxiliary tuple and every permitted unit multiplier.

## Independent finite verification

I independently reconstructed the symmetry menu using 120 rational matrix-nullspace calculations, rather than the manuscript's explicit formula. Exactly the twelve stated maps survive. I checked every multiplier, discriminant and involution identity symbolically, all ten initial gaps, and the one-step recurrence at all exponents from 4 through 66, giving 630 exact finite controls. The infinite induction is justified separately above.

I also independently checked all nine displayed prime fixtures, including exponents 5 and 7, by trial division, inertness, simple modular roots, the exact contact valuations modulo `p_e^2`, the denominator units, and CRT. The resulting sample progression is

```text
B = 9240295498757600662604714622082342869933423356250381011889458783508259762533475470959205
    mod 15340612353908186276228270139121960971199494607770775140372839079547518211681019103609458.
```

The all-exponent audit receipt is `audit_work/independent_odd_extension_certificate.json`, reproducible with `audit_work/check_odd_extension.py`. The initial symmetry, even-exponent and seven-prime controls remain in `audit_work/independent_finite_certificate.json` and `audit_work/independent_crt_certificate.json`. These calculations are checks of explicit identities and fixtures; Chebotarev and the universal arguments are mathematical proofs, not computational inferences. This is an independent internal review within the present agent team, not external non-author peer review.
