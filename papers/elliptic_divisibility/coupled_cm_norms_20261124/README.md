# Coupled CM norm conics on elliptic multiplication graphs

## Result and scope

The [six-coordinate height-anchored quotient](../height_anchored_quotient_20261124/README.md)
needs an additional relation controlling the multiplier \(m=j/h\) of
two rational elliptic points. The previous no-cap theorems concern
uncoupled poles and independent perfect-power tests; the norm conics
below are a different type of coupled cover, with rational realizations
proved globally on infinitely many multiplication graphs.

The following facts are proved here:

* On either of the CM types \(j=1728\) and \(j=0\), a suitable real
  quadratic field lies in the residue field of every nonzero point of
  a fixed inert prime-power torsion subgroup.
* This gives actual rational norm witnesses coupling two points
  \(H,U=[m]H\), for all odd inert prime-power multipliers \(m\).
  In the \(j=1728\) case the conic works on the existing rational carrier
  \(y^2=x^3-2x\). In the \(j=0\) case two complementary conics remove the
  ambiguity caused by reduction of the reference to a torsion zero.
* At foreign odd-depth denominator primes the conics impose nontrivial
  splitting conditions. They do not exclude all foreign primes.
* For the existing six-coordinate source, adding the resulting single
  conic costs only one extra rational coordinate, but **does not establish
  a quotient-size cap**: the enlarged source still accepts the explicit
  nonintegers \(\ell^{-r}\) for every \(r\ge1\) and any fixed allowable
  inert prime \(\ell\).

No new defining-variable bound is claimed. The first two results are
unconditional elliptic identities; the last uses the same retained
ordinary-abc and BB premises as the six-coordinate source.

## 1. Quadratic splitting of CM prime-power torsion

Let \(E/\mathbb Q\) have a nonreal CM automorphism \(\iota\) defined
over \(K_0=\mathbb Q(\sqrt{D_0})\), with \(D_0=-1\) for \(j=1728\)
and \(D_0=-3\) for \(j=0\). Use the usual order-four automorphism in
the first case and order-three automorphism in the second.

Let \(\ell\) be an odd rational prime inert in \(K_0\), different from 3
in the second case, and put \(m=\ell^k\), \(k\ge1\).
Define the real quadratic field \(L=\mathbb Q(\sqrt d)\) by
\[
 d=
 \begin{cases}
 \ell,&\ell\equiv1\pmod4,\\
 |D_0|\ell,&\ell\equiv3\pmod4 .
 \end{cases}
\]
In the first CM type the inert-prime condition is \(\ell\equiv3\pmod4\),
so \(d=\ell\).

**Lemma 1.** For every nonzero \(R\in E[m](\overline{\mathbb Q})\),
both \(\mathbb Q(R)\) and \(\mathbb Q(x(R))\) contain \(L\).

**Proof.** An automorphism \(\sigma\) of \(\overline{\mathbb Q}/\mathbb Q\)
fixing \(x(R)\) sends \(R\) to \(R\) or \(-R\).
Multiplying by a suitable power of \(\ell\) gives a nonzero point
\(T\in E[\ell]\) with \(\sigma T=\pm T\).
Inertness makes \(E[\ell]\) one-dimensional over
\(\mathbb F_{\ell^2}=\mathbb F_\ell[\iota]\): the minimal polynomial
of the CM automorphism remains irreducible of degree two, and the
underlying vector space has dimension two. In the basis supplied
by \(T\), the action of \(\sigma\) is multiplication by \(1\) or
\(-1\) when it fixes \(\iota\), and multiplication by \(1\) or
\(-1\) followed by field conjugation otherwise. Its determinant
over \(\mathbb F_\ell\) is therefore respectively \(1\) or \(-1\).
Field conjugation has eigenspaces of dimensions one for both \(1\)
and \(-1\), because \(\ell\) is odd.

The Weil pairing identifies this determinant with the mod-\(\ell\)
cyclotomic character. Its quadratic character is the character of
\(\mathbb Q(\sqrt{(-1)^{(\ell-1)/2}\ell})\), the unique quadratic
subfield of the \(\ell\)-th cyclotomic field.
For \(\ell\equiv1\pmod4\), both possible determinants have trivial
quadratic character, and hence \(\sigma\) fixes \(\sqrt\ell\).
For \(\ell\equiv3\pmod4\), that quadratic character agrees on the
stabilizer with the sign of the action on \(K_0\).
Their product character is trivial there, so \(\sigma\) fixes
\(\sqrt{|D_0|\ell}\). This proves the inclusions by Galois theory. QED.

In particular every rational Galois orbit in
\(E[m]\setminus\{O\}\) splits into two conjugate orbits over \(L\).
Choose one orbit from each pair, and write \(D_+\) for their sum
as an effective divisor with multiplicities one. If
\(\gamma\) is the nontrivial automorphism of \(L/\mathbb Q\),
\[
 \tag{1}
 D_++\gamma D_+=\sum_{R\in E[m]\setminus\{O\}}[R].
\]
The divisor \(D_+\) is defined over \(L\); no effective torsion
factorization or choice of individual points over \(L\) is needed.

## 2. A general norm identity by translation of divisors

For a degree-zero divisor on an elliptic curve, the class in
\(\operatorname{Pic}^0\) is determined by the group-law sum of its
points with multiplicities. For a rational function, let its
norm from \(L(E)\) to \(\mathbb Q(E)\) be the product with its
coefficient conjugate.

Suppose \(f,f'\) are rational functions over \(\mathbb Q\) with
\[
 \operatorname{div}(f)=\sum_T n_T[T],\qquad
 \operatorname{div}(f')=\sum_T n_T[T'] ,
\]
where all \(T\) are torsion of order coprime to \(m\), and \(T'\)
denotes the unique inverse image of \(T\) under multiplication by
\(m\) within the torsion subgroup of order prime to \(m\).
Assume both functions are normalized with the same leading coefficient
at \(O\), where their order is \(-b\). The finite sum
\(\sum_T n_T[T']\) is principal by hypothesis; the identities below
also apply when some \(T\) are nonrational but their weighted divisor
is rational.

For each \(T'\) translate \(D_+\) by \(T'\) and form
\[
 D_g=\sum_T n_T\,\tau_{T'}D_+ .
\]
This divisor is defined over \(L\), has degree zero, and its
group-law sum is
\[
 (\sum_T n_T)\,s(D_+)+\deg(D_+)\sum_T n_T T'=O .
\]
It is therefore principal. As \(O\) does not occur in its support,
there is a unique defining rational function \(g\) normalized
by \(g(O)=1\). This normalization also proves its definition
over \(L\): Galois conjugates fixing \(L\) have the same divisor
and same normalization.

By (1),
\[
 \operatorname{div}(\operatorname{Nm}_{L/\mathbb Q}g)
 = [m]^*\operatorname{div}(f)-\operatorname{div}(f').
\]
At the origin the local parameter satisfies \([m]z=mz+O(z^2)\).
The ratio \(f([m]H)/f'(H)\) has limit \(m^{-b}\).
Comparing the two normalized functions gives the exact identity
\[
 \tag{2}
 m^b\frac{f([m]H)}{f'(H)}=\operatorname{Nm}_{L/\mathbb Q}g(H).
\]
For rational nontorsion \(H\), the value \(g(H)\) is defined and nonzero:
its divisor is supported on torsion. Hence the identity supplies an
actual rational solution of the norm conic at every such \(H\).
There is no step passing from local solubility to global solubility.

## 3. A single conic on the existing rational carrier

Take \(E:y^2=x^3-2x\), with \(P=(9/4,-21/8)\), as in the previous
six-coordinate construction. Here
\[
 \operatorname{div}(y)=\sum_{T\in E[2]\setminus\{O\}}[T]-3[O].
\]
For every odd \(m=\ell^k\) with \(\ell\equiv3\pmod4\), multiplication
by \(m\) fixes this two-torsion divisor. Apply (2) with \(f=f'=y\)
and \(b=3\), then divide the norm by the rational square \(m^4\).
We obtain
\[
 \tag{3}
 \frac{y([m]H)}{m\,y(H)}\in
      \operatorname{Nm}_{\mathbb Q(\sqrt\ell)/\mathbb Q}
               (\mathbb Q(\sqrt\ell)^\times).
\]

An independent algebraic verification uses the usual division
polynomials. For odd \(m\), the monic polynomial
\(\psi_{2m}/(m\psi_2)\) has simple roots at the abscissas of
\(E[2m]\setminus E[2]\), paired under sign. Every such abscissa
field contains \(\mathbb Q(\sqrt\ell)\) by Lemma 1 applied to the
nonzero \(\ell\)-primary component. Thus this monic polynomial
is the product of a polynomial over that quadratic field and
its conjugate. The identity
\(\psi_{2m}(H)=\psi_2([m]H)\psi_m(H)^4\),
with \(\psi_2=2y\), gives (3), since \(\psi_m(H)^4\)
is a rational norm. This verification yields explicit rational
functions if torsion polynomials are computed for a particular \(m\).

For an external input \(X\ne0\) we can therefore impose the genuinely
coupled conic
\[
 \tag{4}
 A^2-\ell B^2=\frac{y(U)}{Xy(H)} .
\]
When \(X=m=\ell^k\) and \(U=[m]H\), (3) proves completeness,
for every rational nontorsion \(H\), not only for some well-prepared
reference. In the existing cyclic chart the ordinates are finite
quadratic roots. After retaining \(B\), equation (4) makes \(A\)
one more finite quadratic root, with the nonzero denominator
guards imposed as before. It therefore adds one ordinary rational
coordinate to the six-coordinate source using a joint finite encoder.
This is a seven-coordinate *relation* complete at all positive powers
of the fixed prime \(\ell\), not a seven-coordinate definition.

For soundness consider a good odd prime \(p\nmid\ell\) inert in
\(\mathbb Q(\sqrt\ell)\), with \(v_p(X)=0\).
Valuations of nonzero rational norms from the unramified quadratic
local extension are even. If \(U\) is formal of odd depth \(b\)
and \(H\) is integral with unit ordinate, the right side of (4)
has valuation \(-3b\), a contradiction.
If both points are formal of depths \(a,b\), the same argument forces
\(b-a\) even.

In particular suppose \(h\mid j\), \(m_*=j/h\), and \(|m_*|>2\).
A primitive denominator prime of \([j]P=U\) has reduction
order \(|j|\) for \(P\). At such a prime \(H=[h]P\) has reduction
order \(|j|/\gcd(|j|,|h|)=|m_*|>2\). It is neither the origin
nor a two-torsion point, and its ordinate is a unit.
Consequently (4) forbids every odd-depth primitive prime of \(U\)
which is inert in the quadratic field and does not divide the
numerator or denominator of \(X\) or the fixed exceptions.

This is selective soundness. The known total simple-primitive
mass theorem supplies primes without a splitting condition.
In fact one must not infer the inert mass universally:
on the true prime-power multiplication graphs (3) itself
excludes just these inert contacts.

## 4. Two complementary conics for the \(j=0\) type

Let \(a\in\mathbb Q^\times\) and \(E_a:y^2=x^3+a^2\).
The rational points \(T_\pm=(0,\pm a)\) have order three.
The functions \(f_\pm=y\mp a\) have divisor
\(3[T_\pm]-3[O]\), and have common Laurent leading coefficient
at the origin. This follows directly from
\((y-a)(y+a)=x^3\) and the unit value of the other factor
at \(T_\pm\).

For odd \(m=\ell^k\) with \(\ell\equiv2\pmod3\), let
\(\epsilon\in\{1,-1\}\) be the residue of \(m\) modulo three,
and choose the real field \(L=\mathbb Q(\sqrt d)\) of Lemma 1
(\(D_0=-3\)). Then \(T_\pm'=\epsilon T_\pm\).
Equation (2) gives both identities
\[
 \tag{5}
 m^3\frac{y([m]H)-a}{y(H)-\epsilon a},\qquad
 m^3\frac{y([m]H)+a}{y(H)+\epsilon a}
 \ \in\operatorname{Nm}_{L/\mathbb Q}(L^\times).
\]
They provide two norm conics with globally realized rational
witnesses on every indicated multiplication graph.

At an inert prime outside the fixed bad primes, primes dividing
\(2a\), and \(\ell\), if \(H\) is not formal, its ordinate is
integral, and at least one of \(y(H)-\epsilon a\),
\(y(H)+\epsilon a\) is a unit: their difference is the unit
\(2\epsilon a\). If \(U\) has odd positive formal depth, its
two corresponding numerator functions have negative odd
valuation. Thus at least one conic fails. If both points are
formal, (5) forces the two depths to have the same parity.
This pair of tests removes the ordinate-zero ambiguity in
(4), again only at inert primes.

For example \(a=3\), \((3,6)\in E_a(\mathbb Q)\) is nontorsion:
its double has abscissa \(-15/16\), hence depth two at 2,
inside the injective formal logarithm disk.
No assertion about its rank or saturation is needed here,
and no rank-one transfer to that carrier is claimed.

## 5. Explicit false positives persist even with the coupled conic

The conic (4) is not an independent perfect-power test covered
by the earlier geometric no-cap theorem. We now show its failure
by an explicit construction, not by that theorem.

Fix an allowable prime \(\ell\equiv3\pmod4\),
\(\ell\notin\{2,7,29\}\), and any integer \(r\ge1\).
In the original six-coordinate source fix the noninteger input
\(X=\ell^{-r}\). It is integral at the three preparation primes.

Follow the exact false-positive witness preparation of
[the six-coordinate source, Section 6](../height_anchored_quotient_20261124/README.md).
In particular choose \(H=[h]P\) with arbitrarily large positive
\(h\), sufficiently deep at all fixed exceptional primes and the
finite support of the input contact function \(u\), in the prescribed
compact real arc, and with **even positive formal depth at \(\ell\)**.
All these conditions are compatible as proved there. Fix this
reference point, and put \(a_p\) for its formal depth.

There are now finitely many required congruences on the integer
multiplier \(m_*\), namely
\[
 \tag{6} m_*\equiv X\pmod{p^{(N+4)a_p}}
\]
at each odd-depth formal prime and at the three preparation
primes (even if their depths are even). Every prime in this list
differs from \(\ell\), since the latter has even depth and is
not a preparation prime.

We can satisfy **all** the congruences with \(m_*=\ell^k\).
For each listed prime the order of the unit \(\ell\) modulo the
indicated prime power is finite. Choose positive \(k\), arbitrarily
large, with \(k\equiv-r\) modulo twice the least common multiple
of those orders (take the empty lcm as one). Then (6) holds
simultaneously and \(k+r\) is even.
The original ordered local and real calculation, with
\(U=[m_*]H\), proves the actual BB scalar is prepared: all
nonintegral input primes have even reference depth, the required
odd-depth comparisons satisfy (6), and the real inequalities
are independent of the multiplier. The published BB converse
thus supplies the original six-coordinate witnesses.

Finally by (3) and \(m_*/X=\ell^{k+r}\),
\[
 \frac{y(U)}{Xy(H)}
   = \ell^{k+r}\,\frac{y([m_*]H)}{m_*y(H)}
\]
is a norm from \(\mathbb Q(\sqrt\ell)\): the extra factor
is a rational square, hence a norm. Therefore (4) has rational
witnesses as well. All denominators in (4) are nonzero
because \(X\ne0\) and \(H\) is nontorsion.

This proves that the enlarged seven-coordinate relation admits
\(X=\ell^{-r}\), for every \(r\ge1\), with arbitrarily large
references and, **for each fixed prepared reference**, arbitrarily
large multipliers \(m_*\). It violates every finite quotient-size
cap depending only on \(h\) and \(X\), in particular any uniform
bound \(O(h^2)\) for \(\log(1+|m_*|)\).
This actual counterexample is stronger than merely noting that
a selective primitive-prime estimate is missing.

## 6. Conclusion

The new norm identities provide fully realized coupled conics, but
only prime-power completeness was established, and their arithmetic
selectivity is insufficient even there. They do not solve the desired
all-integer quotient cap. A proposed successor must prevent the
common positive-exponent approximation of negative powers in
Section 5, or employ a different mechanism that controls all
foreign primes instead of just primes inert in one quadratic field.

The proofs use elementary CM action on prime torsion, the Weil
pairing, principal divisors on elliptic curves, and the existing
ordered witness theorem for the false-positive continuation.
The accompanying checker gives finite exact polynomial factorizations,
norm witnesses and exponent-congruence checks. It does not assert
a selective inert primitive-divisor theorem, or any improvement to
the established defining-polynomial counts.
