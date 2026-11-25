# Final smaller-degree variant: 339969

This is a further **proved** transfer of [the six-test sum
construction](README.md). The same arithmetic premises, base
coordinates, point algebra, pre-contact guards, and input factor
are retained. Only the contact and detector expressions and
terminal clearing are changed. The resulting eleven-variable
family has degree at most **339969**, for sufficiently large
fixed odd B (cutoff ineffective).

## Contact modification

Keep \(M=\beta^4+T^4,\ a=M+16,\ x=a-z,\ y=a+z\), and
\(A_0=G_8(x), H_0=G_8(y)\) with the same fixed degree-eight
polynomial \(G_8\). Use
\[
 c=H_0/A_0-1+3/H_0=P_c/Q_c,\qquad
 P_c=H_0(H_0-A_0)+3A_0,\qquad Q_c=A_0H_0.
\]
Guard \(P_cQ_c\ne0\). No denominator y is needed.
The simple-contact proof of Section 2 is unchanged: the
nonpositive valuations of \(H_0\) are even, and the extra
constant -1 cannot cancel a unique negative minimum.
The same positive margin 96309/200200 follows. This also
establishes existence of a consumed prime independently
of the terminal equation.

For completeness use the same sixteen-position prime pattern
and fixed finite avoidance. At a selected prime \(v_p(c)=-1\).
At nonselected primes outside the temporary set where z is
integral both \(A_0,H_0\) are units, hence c is integral.
At any nonintegral slope prime outside that set, the leading
asymptotic is
\[
             c\sim16a/z .
\]
Here the leading coefficient is a unit (the temporary set includes
the support of a and 2). Indeed \(G_8(a+z)-G_8(a-z)\)
has leading term \(16az^7\), and \(3/G_8(a+z)\) has order
\(z^{-8}\). Thus \(v_p(c)=-v_p(z)\) is positive **even**
because the chosen slope has square reduced denominator at
all such primes. This parity uses the square denominator of the
actual prime-pattern slope, not an assertion on arbitrary z.

At each fixed preparation place the same asymptotic holds as
the prescribed denominator grows sufficiently large, with c
tending to zero. At 2 there is an additional squareclass check.
For the canonical root \(A=[n]P\), the dyadic trace lemma of
[twelve_contact_first_scale v78](../twelve_contact_first_scale_20261119_v78.tex)
gives \(v_2(T)\le-2\), \(T\in\mathbb Q_2^{\times2}\), whereas
\(\beta\) is integral. Hence \(M=T^4(1+\beta^4/T^4)\) is a
dyadic square of valuation at most -8, and \(a=M+16\) remains
a dyadic square. The retained Gaussian prime supplier gives all
selected rational primes congruent to 1 modulo 8 (their Gaussian
generators are 9 modulo 16). By taking the prescribed square
denominator \(D_z^2 L_z^2\) with sufficiently large 2-adic depth,
each selected prime is congruent to \(N_z\bmod8\), so
\(N_z\equiv1\bmod8\). Thus \(z=N_z/(D_z^2L_z^2)\) is a
dyadic square. It follows that c is a dyadic square for deep
enough prepared z, with arbitrarily large positive even depth.
At the positive real infinity c is positive and tends to zero.

These are the only changed contact preparations. They use
exactly the prime supplier and dyadic trace already present
in the v78 source.

## Even-valuation product

For the original six tests put \(m_i=1\) for the first four
reciprocal-abscissa tests and \(m_i=2\) for the final two
comparison tests. Use
\[
                     W=\prod_{i=1}^6(1+cC_i^{m_i}).
\]
This is an *unbalanced* product; its foreign-prime control
comes from the reciprocal gate rather than from the previous
six positive balancing denominators.

The reciprocal tests have even valuation at every good
unramified slot, by \(y^2=x(x^2-D)\) on the good curve:
negative x valuation is even by the cubic term, positive
x valuation is even since D is a unit, and zero valuation
is already even. The zero tests cause no difficulty.
Hence for any odd valuation of c every nonconstant term
\(c C_i^{m_i}\), when nonzero, has odd valuation. Each factor
has nonpositive valuation and is 1 modulo the prime whenever
integral. The same holds for W. If \(v_p(u)=\nu>0\) is odd,
the reciprocal gate of Sections 3--4 gives a slot with
\(v(W)>-\nu/2\). Every factor there has valuation greater than
\(-\nu/2\) since all the others have nonpositive valuation.
Therefore \(m_i v(C_i)>\nu/2\) and every raw test passes.
The proof that \(\operatorname{Nm}W+1\ne0\) at a consumed
prime still applies, including inert primes.

For canonical integer witnesses the selected-prime argument
and the foreign negative-odd-u argument of Section 5 depend
only on this nonpositive/residue-one property of W, and
on all tests passing at one selected slot. Both hold here.
At fixed places and real infinity the bounded raw tests make
\(W\to1,\ t\to1,\ e\sim7c\).
Consequently the actual e has the required positive real
interval, square reduced denominator, and class-seven dyadic
depth. No new BB realization is required.

## Smaller integral terminal equation

Write the two coordinates of each test as \(C_i=N_i/d_i\)
using exactly the denominators and numerator pairs recorded
in degree.json. Set
\[
 L=Q_c^6\prod_i d_i^{m_i},\qquad
 N=\prod_i(Q_c d_i^{m_i}+P_c N_i^{m_i}).
\]
These are integral point-algebra expressions, with the
field multiplication for each numerator pair. On the guard
\(W=N/L\). Keep \(J=\operatorname{Nm}N+L^2\) and
\(K_0=Q_cJ+P_c\operatorname{Tr}(N)L\). Set
\(d_0=7P_c/Q_c\), so
\(e=d_0(Q_cJ/K_0)^2\).
Instead of multiplying \(d_0\) by \(Q_c^2\) before using
the BB normalized product equation, retain this rational
representative and clear its square denominator at the end:
\[
 \mathcal R=
 (K_0^2-7P_cQ_c J^2)
 (Q_c^2v^4-49P_c^2)
 (Q_c^2s^4-49P_c^2),\qquad q^2=\mathcal R.
\]
Indeed the normalized BB ordinate is \(q/(K_0Q_c^2)\).
The terminal algebra remains monic over the point algebra.
There is no new guard for \(K_0,J\):
\(J\ne0\) at every rational point character by the consumed-prime
argument; if \(K_0=0\), the first factor of the displayed
radicand has finite odd valuation, and the two remaining factors
have finite even valuations because
\(v_p(P_c)-v_p(Q_c)=-\nu\) is odd. Thus rationality of q
contradicts \(K_0=0\). Once it is excluded, the old local
BB obstruction applies. Conversely a prepared BB witness
lifts by the displayed scaling, without any new condition.

## Degree ledger and final polynomial

Retain the original twelve pre-contact norm guards of degree
288. The degrees of \(G_8(x),G_8(y)\) are at most 64.
Their difference is odd in z, and every contributing
monomial from the eighth-degree term has at least one z;
since a has degree at most eight, the largest weight is
\(7\cdot8+1=57\). The smaller even degrees of \(G_8\)
do not exceed this. Consequently
\[
       \deg P_c\le121,\quad \deg Q_c\le128,\quad g\le537 .
\]
Using the identical original-test degree pairs of degree.json
gives \(\sum m_i\deg d_i=82\).
In each factor of N, the term
\(Q_c d_i^{m_i}\) bounds both terms, since the numerator
weight exceeds its denominator weight by at most one.
Thus the weighted bounds are
\[
\begin{array}{c|r}
 L,N&850\\
 J&1700\\
 K_0&1828\\
 K_0^2-7P_cQ_cJ^2&3656\\
 Q_c^2v^4-49P_c^2,\ Q_c^2s^4-49P_c^2&260\\
 \mathcal R&4176\\
 q&2088
\end{array}
\]
Use the same explicit envelope rule with
\(M_q=L_0 r_0^{1044}\). Its degree is 2088, and the
sum of the six point envelope degrees is still 30.
The separator thus has weight at most 2118.
The rank is 128. With the same determinant recipe and
the new \(\mathcal R,P_c,Q_c,M_q\), the degree bound is
\[
       1+128(1+537+2118)=\boxed{339969}.
\]
The input count is eleven, content one, and the polynomial
is specified by finite integer operations. The sufficient
B and coefficient-height bound have not been evaluated.

This supersedes the 520065 degree in the first variant
without changing its scope. The code of verify.py checks
the pinned source and first ledger; verify_final.py adds
the exact final ledger. The arithmetic proof is not a
consequence of finite regression testing.
