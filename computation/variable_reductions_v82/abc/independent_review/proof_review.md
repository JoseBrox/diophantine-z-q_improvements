# Independent audit of the v82 genus-one criterion

Reviewer: independent child agent `audit_genus_v82`.

Reviewed source: `package/genus_one_sound_criterion_20261120_v82.tex`, SHA256
`c226917f9546bb56380c77146374384e360d97ca744d0d3164f6c4906dfc9aa0`.

**Outcome:** the mathematical statements and their stated scope pass review.
The only issue found in the initial snapshot was a bibliographic mismatch:
the encoder reference named the sixteen-coordinate `amplified_rationality_descent`
paper. The author corrected it to the actual v81 compression paper,
`ten_coordinate_rationality_20261119_v81.tex`. The v78 eleven-coordinate
source also already supplies a rank-128 encoder. This reviewer edited no
package file.

## Soundness and local solubility

The positive odd contact argument is valid, including the zero-coordinate
cases. If \(\mu=v_p(d)>0\) is odd and \(2v_p(V)>\mu\), then
\(v_p(H)=\mu\). The two nonzero summands of
\(d(s^4-H^2)\) have distinct odd valuations
\(\mu+4v_p(s)\) and \(3\mu\); equality would require a nonintegral
valuation of \(s\). With \(s=0\), the remaining term still has odd
valuation. Thus neither a square nor zero occurs. At the contact primes,
\(p\ne2,7\), this is exactly the scalar inequality used by the old source.

The everywhere-local theorem covers all valuation patterns:

- For odd \(v_p(d)\), the square-denominator condition on
  \(e=4d/V^2\) forces \(v_p(d)-2v_p(V)>0\), even when \(v_p(d)<0\).
  Hence \(H/V^2\) is a local square. The point \(s^2=H,Y=0\) is smooth
  because \(4ds^3\ne0\).
- For even \(v_p(d)=2m\), the local-square and negative-local-square
  cases give points at large \(s\), or at \(s=0\), respectively.
  In the remaining case, \(v_p(V)<m\) again makes \(H\) square.
  Otherwise \(v_p(H)=2m\); any cancellation at \(v_p(V)=m\) would
  make \(-d\) a local square, contrary to the case assumption.
- The remaining integral unit model
  \(Y_0^2=D(s_0^4-H_0^2)\) has smooth genus-one reduction at every odd
  prime: its quartic has four distinct geometric roots. The Weil lower
  bound is positive, and nonsquare \(D\) excludes rational points at
  infinity. An affine smooth point therefore lifts.
- At two, \(d\in7\mathbb Q_2^{\times2}\) implies \(-d\) is square.
  The point at \(s=0\) is smooth over \(\mathbb Q_2\); the implicit
  function argument does not require its derivative to be a two-adic unit.
  At the real place, sufficiently large \(s\) works.

Every smooth local disk contains points avoiding the finite set
\(sY=0\). This is an argument for every place, not an inference from
testing finitely many primes. No square-denominator hypothesis on \(d\)
itself is used in this theorem.

## The ten-coordinate statement is a criterion only

I compared the manuscript with the twelve-contact v78 source. The contact
scalar \(u\), and hence \(d=7u/(1+u)^2\), depends on the rational base
coordinates, independently of the finite point-ordinate characters.
For every point-algebra character the new terminal radicand is a nonzero
polynomial in \(s\), with leading coefficient \(d\). Once the existing
base guards hold, only finitely many values of \(s\) are excluded.

Under the additional stated hypothesis of a rational point with
\(sY\ne0\) on an actual prepared fibre, the map
\((s,Y)\mapsto(ds^2,dsY)\) gives a point outside the two-torsion on a
nonzero congruent-number curve. Such a point has infinite order. Odd
multiples have the same first Kummer class, so they lift to infinitely
many rational \(s\) on the cover. This supplies the required finite
avoidance without invoking an equality consequence of Zariski density.
The guarded rank-64 point algebra plus one terminal quadratic root has
rank 128 and still costs one encoder coordinate.

The coordinate count \(1+6+1+1+1=10\) is consequently correct **under
the explicitly additional actual-input hypothesis**. The local theorem
does not prove that hypothesis. No theorem defining the integers in ten
coordinates follows from this manuscript alone. I did not re-audit all
retained arithmetic premises of the v78 source.

### The added quadratic-progression criterion

The final source's Corollary 3 is valid with its stated requirement of one
fixed admissible source constant \(B\). Before completeness, the guarded
construction is already a sound ten-coordinate partial source polynomial
\(P_B(T,\mathbf Y)\). Substituting \(T=cX^2+b\) introduces no new
coordinate. For a reduced rational input \(X=a/q\), with \(q>0\), a
zero of the substituted polynomial implies
\(q^2\mid ca^2\). Coprimality implies \(q^2\mid c\), and the
positive squarefree integer \(c\) forces \(q=1\). Thus the pullback
remains sound for the rational integers.

If the additional actual-fibre hypothesis is supplied for all but finitely
many source inputs \(cm^2+b\), the finitely many omitted integer values
of \(m\) are restored by multiplying by their linear factors. Every
added root is an integer. Any zero source input occurs for at most two
integer \(m\), and is explicitly included among these exceptions.
No coordinate is added and no degree bound is asserted. The same fixed
\(B\) is essential; varying \(B\) with \(m\) would not give this
single polynomial. Actual realization on a progression remains unproved.

## Independent exact counterexample reconstruction

`check_independent.py` imports no producer code. It reconstructs the
prepared fractions, all three curve maps, and the norm conic directly.
It calls PARI algebraic descent on
\(E_{6305215}:y^2=x^3-6305215^2x\), obtaining

\[
[1,1,2,[[-6002500,4729026750]]],
\qquad E(\mathbb Q)_{\rm tors}\simeq(\mathbb Z/2)^2.
\]

The independent two-isogenous specialization returns \([1,1,2,[]]\).
These are two specializations of the **same implementation**, not two
independently implemented rank algorithms. The PARI function catalogue
states that the first two entries are unconditional algebraic bounds;
the checker does not use analytic rank or BSD.

The eight Kummer classes were reconstructed using actual additions of
the explicit non-torsion point to each rational two-torsion point. This
gives eight distinct classes. Since the rank is one and the rational
two-torsion has order four, they exhaust \(E(\mathbb Q)/2E(\mathbb Q)\).
This argument needs no claim that the displayed point generates the full
Mordell-Weil group.

For the zero-coordinate torsion exceptions, the checker separately adds
each nonzero shifted coordinate. Every coordinate class is in
\(\langle-1,2,35,6305215\rangle\). Each generator has equal valuation
parity at 17 and 10597. The target \(119\kappa N^j\) has unequal
parity there whenever \(\kappa\) is supported on \(\{2,3,5,7\}\).
The independent check covers the entire 64-class target set, rather
than only the sixteen displayed multipliers and two choices of level
parity. None belongs to the containing subgroup.

The rational scaling \(dH=N(r^2/8)^2\) preserves every shifted
abscissa square class. The explicit tuple has all the claimed real
inequalities, square denominators, two-adic valuations, and
\(v_{17}(u)=1\). It is prepared scalar data only; no identification
with an actual contact detector or actual trace is claimed or proved.

## Arbitrary two-adic depth and small real size

The extension in the remark is valid. The conic
\(a^2+119b^2=52985\) is rational, and its parametrization was checked
symbolically. The real branch near \((\sqrt{52985},0)\) makes
\(q=a/b\) positive and arbitrarily large. The two-adic branch has
\(a\) a unit and can have \(v_2(b)=k\) for every \(k\ge2\):
\(52985-119b^2\) remains a square. Weak approximation on the rational
conic supplies both requirements at once.

At 7 or 17 the terms \(a^2\) and \(119b^2\) have opposite valuation
parities. A negative minimum cannot cancel to the unit 52985. Hence
both coordinates are integral, and \(a\) is a unit; thus
\(v_p(q)\le0\). This proves that \(e=476/q^2\) has square reduced
denominator at every odd prime, and \(v_2(e)=2+2k>0\).

Choose \(t\) simultaneously large and positive, with
\(v_2(t)=-(k+1)\), \(v_{17}(t)=0\), and \(v_7(t)\ge1\).
Rational weak approximation, or elementary congruences with a power-of-two
denominator, gives such a \(t\). Then \(r=t/(1+17t^2)\) has
\(v_2(r)=k+1\), is a unit at 17, and has positive valuation at 7.
It follows that \(d=119r^2\) has square denominator and
\(v_2(V)=v_2(qr)=1\), while \(v_{17}(u)=1\). Taking \(t\) large
makes \(0<V<2\). Finally
\(dH=119\cdot52985\,(r^2/b)^2\), so the same squareclass
obstruction persists. This does not remedy the open actual-source
realization problem.

## Source checks and limitations

Primary references inspected:

- PARI/GP elliptic-curve catalogue, `ellrank`:
  <https://pari.math.u-bordeaux.fr/dochtml/html/Elliptic_curves.html#ellrank>.
- Burungale, arXiv:2611.16130v1, Section 3.2, for the standard Kummer map
  and its exceptional two-torsion values:
  <https://arxiv.org/html/2611.16130v1>.
- The local v78 eleven-coordinate manuscript and the local v81 finite
  algebra compression manuscript, for the conditional transfer.

The computation is exact but trusts PARI's algebraic descent
implementation for the rank upper bound. The proof review makes clear
where finite computation ends and universal mathematical arguments are
used. A smaller actual integer-definition record has not been certified.
