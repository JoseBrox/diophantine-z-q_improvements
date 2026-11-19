# Rational and local points on the diagonal intrinsic pole curve

The November 17 source `negative_results/papers/pole_parameters/intrinsic_specializations_20261117_v57.tex` leaves the coupling \(s=cv\) open. Consider its simplest member \(s=v\) and set
\[
F_d(v)=d\big[(d+v^2)^2v^4-(d-v^2)^2(1-d)^2\big].
\]
Call \(d\) prepared when \(0<d<1\), its reduced denominator is a square, \(d\in7\mathbf Q_2^{\times2}\), and \(v_2(d)\ge4\). We establish everywhere local solubility on every prepared fiber, prove rational solubility on explicit infinite subfamilies, and give an everywhere locally soluble prepared fiber with no rational point. The arithmetic gap for the defining-polynomial counts is identified below.

## Every prepared fiber has points everywhere locally

For every prepared \(d\), the smooth projective curve \(C_d\colon Y^2=F_d(v)\) has genus three. Every completion of \(\mathbf Q\) has affine solutions with \(Y\ne0\). In particular, for any finite set of places one can choose a **single rational** \(v\) with \(F_d(v)\) a nonzero square in each indicated local field. At the real place one can take \(v\) large enough that additionally \(F_c(v)>0\) for any prescribed finite set of positive real character values \(c\), including \(c=1\).

Put \(h=1-d\). At \(r=v^2\), the bracket in \(F_d\) factors as
\[
  [(d+r)r+h(d-r)][(d+r)r-h(d-r)].
\]
The factors are coprime since \(dh\ne0\). Their discriminants in \(r\) are \(d^2\pm6dh+h^2\), both nonzero over the rational numbers because the quadratic roots for \(d/h\) are irrational. Their nonzero constant terms and substitution \(r=v^2\) therefore give eight distinct roots. This proves the genus claim.

Large real \(v\) works. At any finite place where \(d\) is square take \(|v|_p\) sufficiently large since \(F_d(v)/(dv^8)\to1\). Wherever \(-d\) is square, take \(v^2=-d\) and the remaining term is a nonzero square. This applies at 2 since \(-7\equiv1\pmod8\). At odd \(p\) with \(v_p(d)>0\), the bracket modulo \(p\) is \(v^4(v^4-1)\), which has a simple root at 1. Lift the bracket root, and then perturb the zero-ordinate point on the smooth curve over \(\mathbf Q_p\) to get a nonzero ordinate.

At the remaining odd primes the valuation of \(d\) is even, its normalized unit is nonsquare, and \(p\equiv1\pmod4\). When \(v_p(d)=0\), put \(D=d\), \(h=1-d\), both units. When \(v_p(d)=-2k<0\), set \(x=p^kv,\ y=p^{5k}Y,\ D=p^{2k}d,\ h=p^{2k}-D\). In the first case \(x=v,y=Y\). Both integral equations have the form
\[
 y^2=f(x)=D[(D+x^2)^2x^4-(D-x^2)^2h^2].
\]
Modulo \(p\), the two quadratics in \(r=x^2\) from the displayed factorization are coprime and can have at most one zero discriminant, since the discriminants differ by \(12Dh\). If both are separable, the genus-three Hasse–Weil bound gives at least \(p+1-6\sqrt p>0\) rational points when \(p\ge37\). Both points at infinity are nonrational since \(D\) is nonsquare. If one discriminant vanishes its factor is a square, and removing it gives a smooth genus-one quartic. Again neither point at infinity is rational. At most four rational points lie above the two excluded values of \(x\) where the removed factor vanishes. For \(p\ge13\) the Hasse–Weil lower bound \(p+1-2\sqrt p>4\) suffices. In both cases we have a smooth affine point of the original integral model. For \(p=5,13,17,29\), the companion script verifies all 60 combinations of a nonsquare \(D\) and either \(h=1-D\) or \(h=-D\) modulo \(p\). Smooth lifting and local perturbation complete the proof. Rational weak approximation applies because nonzero local square classes are open and the adjustable abscissa is an affine-line coordinate.

## An everywhere locally soluble prepared fiber with no rational point

Take \(d=112/289=7(4/17)^2\). It is prepared, so the preceding theorem gives nonzero affine points at every completion. Yet its diagonal curve \(C_d\) has no rational point.

For a rational abscissa \(v=a/b\) in lowest terms, denote \(r=a^2, s=b^2\) and clear the two quadratic factors above to the integral binary quartics
\[
 U_\pm=289r(112s+289r)\ \pm\ 177s(112s-289r).
\]
Their product has square class 7 when nonzero, as follows by clearing the square denominators of \(F_d(v)\). A common prime divisor of \(U_+,U_-\) belongs to \(S=\{2,3,7,17,59\}\). Indeed away from \(2\cdot112\cdot289\cdot177\), a divisor of both has to divide their half-sum and half-difference. Neither \(a\) nor \(b\) can then vanish modulo this prime by primitivity. Both \(112s+289r\) and \(112s-289r\) would vanish, a contradiction.

It follows that there is a signed squarefree integer \(k\) supported on \(S\) such that \(kU_+\) and \(jU_-\) are integer squares, with \(j\) the signed squarefree representative of \(7k\). When both factors are nonzero, take their signed squarefree parts: outside \(S\) only one factor can contain any given prime, and its exponent must be even. If either factor vanishes, the other has prime support in \(S\) by the same coprimality argument, and one can select the class of the nonzero factor first. The two factors cannot both vanish in characteristic zero. Thus the descent includes every zero-ordinate case.

The companion script `hasse-failure.py` enumerates all 64 signed classes and both primitive projective charts at the four indicated moduli. It lists \((a,b)=(t,1)\) for all residues \(t\) and \((1,t)\) for \(t\) divisible by the residue characteristic. These represent all primitive local pairs up to multiplication by a unit, which scales each binary quartic by a fourth power. It tests both quantities against the full set of quadratic residues, including zero.

| Modulus imposed successively | Classes surviving |
|---:|---:|
| 256 | 32 |
| 27 | 16 |
| 49 | 4 |
| 41 | 0 |

The four pairs before the last sieve are \((7,1),(14,2),(-413,-59),(-826,-118)\). The two points at infinity on the smooth projective model are nonrational because \(d\) is nonsquare. This gives a Hasse-principle failure and disproves the diagonal specialization as a uniform prepared-input theorem. The single value \(d=112/289\) has not been identified as an actual detector input for an integer in the full defining-polynomial problem.

The same input disqualifies infinitely many fixed linear couplings. If \(s=cv\), write \(c=m/n\) in lowest terms. The two integral quartics replace the half-sum by \(m^2\) times itself and the half-difference by \(n^2\) times itself. The only new primes in the descent support divide \(mn\). Suppose each prime divisor of \(mn\) is \(1\bmod 13{,}886{,}208\), the product \(256\cdot27\cdot49\cdot41\). Then all these factors are 1 at every sieve modulus. Their presence changes neither any tested quartic residue nor any of the old local class patterns of \((k,j)\); the sieve again leaves no global point. In particular Dirichlet's theorem gives infinitely many distinct prime slopes disqualified by this one input, and arbitrary products and quotients of them fail together.

There is a separate elementary obstruction for \(s=c v^m\), for every integer \(m\ge2\) and every nonzero fixed rational \(c\). Choose arbitrarily large \(p\equiv13\pmod{28}\) avoiding the support of \(c\) and take the v57 prepared inputs \(d=112/p^2\). Here neither \(d\) nor \(-d\) is a local square and \(v_p(d\pm v^2)\) agree for every \(v\). To escape dominance by a nonsquare term in the original radicand, it is necessary that \(v_p(s)=-1\). This forces \(m v_p(v)=-1\), impossible. A single prime outside the support of all coefficients suffices for any finite list of such higher-power couplings. If \(c\) is a nonzero rational function of \(d\), the same proof gives the necessary divisibility \(m\mid 2\deg_\infty(c)-1\), with \(\deg_\infty\) denoting numerator degree minus denominator degree, for all sufficiently large primes in this progression.

## Infinitely many prepared inputs with a nonzero rational ordinate and nonsquare complement

For \(d=7r^2, v=3r\), substitution \(Z=Y/(2r^3)\) gives the fixed elliptic quartic
\[
 Z^2=35945r^4+98r^2-7.
\]
There is a rational seed
\[
 r=8/67,\quad d=448/4489,\quad v=24/67,\quad Y=5999616/1350125107,
 \qquad 1-d=9\cdot449/67^2.
\]
Here \(Z=5859/4489\). For \(L=35945,M=98,N=-7\), its quartic maps by \((x,y)=(Lr^2,LrZ)\) to \(y^2=x^3+Mx^2+LNx\). Both curves are smooth since \(LN(M^2-4LN)\ne0\). The image \(P\) of the seed has abscissa with denominator \(67^2\). The change \(X=9x+3M,\ Y'=27y\) gives a short integral Weierstrass equation, and \(X(P)\) still has a denominator divisible by 67. Nagell–Lutz proves that \(P\) is nontorsion. Give the quartic the seed \(O=(r,Z)\) as origin. The point \(T=(-r,Z)\) maps to \(-2P\) under the elliptic-curve homomorphism obtained by translating the displayed map by \(-P\), so \(T\) is also nontorsion.

An infinite subsequence of multiples of \(T\) can be taken arbitrarily close to \(O\) in \(\mathbf R,\mathbf Q_2,\mathbf Q_7,\mathbf Q_{449}\) at once. Indeed choose a positive even multiple lying in all indicated finite-place open subgroups; its multiples are dense in the real identity component, a circle. In appropriate neighborhoods, \(0<7r^2<1\), \(v_2(r)=3\), \(v_7(r)=0\), \(Z\ne0\) and \(v_{449}(1-7r^2)=1\). At primes other than seven, \(d=7r^2\) has even denominator valuations automatically. This proves infinitely many distinct prepared, nonzero-ordinate specializations with nonsquare complement. They all have global square class 7. The infinitely many values are distinct up to finite repetitions because \(r\) has finite fibers.

## Infinitely many prepared inputs in distinct global square classes

The zero-ordinate branch gives another genus-one source
\[
 z^2=1+8v^4,\qquad d=(1+2v^2-z)/2.
\]
Indeed \(d^2-(1+2v^2)d+v^2(1-v^2)=0\) makes one of the two factors of \(F_d(v)/d\) vanish. The map \((x,y)=(8v^2,8vz)\) to \(y^2=x^3+8x\) sends \(A=(0,1)\) to \((0,0)\) and \(T=(1,3)\) to \(P=(8,24)\). Since \(x(2P)=49/36\), Nagell–Lutz gives infinite order. Use \(A\) as origin on the smooth projective quartic and translate the nonconstant map on its target by \((0,0)\). The translated map is a homomorphism, so \(T\) has infinite order. At \(T\), \(d(T)=0\) and \(\mathrm d d/\mathrm d v=-2/3\).

For any finite set of primes \(S\) including 2, the closure of \([1+2n]T\) in the product of the local groups contains an open neighborhood of the tuple \((T)_{p\in S}\). To see this, first take a positive even integer \(M\) so that \([M]T\) lies in each formal-logarithm domain. Its logarithm is nonzero at each prime because \(T\) is nontorsion. The diagonal ordinary integers are dense in \(\prod_{p\in S}\mathbf Z_p\) by the Chinese remainder theorem. Their multiples of the corresponding logarithm vector therefore fill a product of open additive subgroups. The local inverse-function theorem at \(T\) for \(d\) transfers the open product to a neighborhood of zero in the local inputs. One can select \(v_2(d)\) sufficiently large and even, with normalized unit \(7\bmod8\), and any prescribed sufficiently small open sets at the remaining primes. An arithmetic progression of indices attains these open conditions. Choose an even step and keep the indices odd, so its real closure contains the whole real component of \(T\). Near \(T\), one side has \(0<d<1\) by its nonzero derivative. Infinitely many indices achieve both sets of conditions.

These \(d\) have square denominators. At an odd prime where \(v\) is integral, so are \(z,d\). If \(v_p(v)<0\), write \(t=z/(2v^2)\), which satisfies \(t^2\equiv2\pmod p\) and cannot be 1 modulo \(p\). Consequently \(d=1/2+(1-t)v^2\) has valuation \(2v_p(v)\). At two integrality was prescribed.

For any fixed nonzero square class \(k\), the two smooth projective double covers of this elliptic curve adjoining \(\sqrt{d/k}\) and \(\sqrt{(1-d)/k}\) both ramify. The function \(d\) has a simple zero at \(T\), and \(1-d\) has a simple zero at \((v,z)=(i,-3)\) over the algebraic closure. Riemann–Hurwitz then gives genus at least two. Each cover has finitely many rational points by Faltings. Thus any finite collection of square classes of \(d\) or of \(1-d\) can be excluded simultaneously in the infinite prepared family. The companion script also checks a point with \(v_2(d)=4\) obtained by lifting \([71]P\) on the cubic.

## Counts and the remaining gap

In the ordinary-abc eleven-coordinate v75 source, setting \(s=v\) removes one free coordinate and restricts to a sound ten-coordinate source. Soundness is inherited because every diagonal witness is an original witness. The finite terminal root can be zero there. In the general twenty-five-coordinate **intrinsic transfer** of v57 (with its specific scalar and retained arithmetic hypotheses), restricting one or both pole pairs gives sound 24- or 23-coordinate sources. Its nonvanishing requirements on the finite-algebra radicands still apply. Local approximation can meet their real-character bounds for a fixed positive character list. A proof that the required actual detector inputs from every integer have the needed global rational points, with the retained guards, is missing. Local squareness at any prescribed finite set and infinitely many globally soluble prepared fibers establish neither that step nor any new complete variable count. Genus three also means every fixed diagonal fiber has only finitely many rational points by Faltings, so the original two-parameter Zariski-density argument cannot be transferred.

There is an additional obstruction to replacing two *independent* diagonal parameters by the same one. Take \(p=13\), \(d_0=112/p^2\), \(d_1=112/p^4\); both are prepared and both have nonsquare normalized unit locally, as do their negatives. If \(v_p(d)=-2k\), the valuations of \(d+v^2\) and \(d-v^2\) are equal, because their leading residues cannot cancel. For the two summands of \(F_d(v)\) to avoid dominance by a nonsquare of class \(d\) or \(-d\), it is necessary that \(v_p(v)=-k\). The two displayed fibers require different valuations of a single shared \(v\). This only excludes a universal statement over arbitrary prepared pairs; actual alignment imposes additional structure.
