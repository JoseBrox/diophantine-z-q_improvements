# v156: global S-unit counterexamples on the specialized higher-genus Pell fibers

**The proposed power-sum integrality theorem of v154 is false on the actual sparse-packed source, for every fixed even exponent \(d\) with \(1\le v_2(d)\le40\).** In particular, it fails for the genus-five and genus-25 candidates \(d=2,4\), not merely for an abstract choice of Pell coefficients. For every instance of the uniform v145/v155 packed source, one can choose a false packed digit tuple, satisfy every row of the proposed v148/v150/v154 replacement, including the strict real margin and its actual rational triangular equations, and have \(h,j>0\) nonintegral with a single certified integer \(\Lambda=h^d+j^d\) satisfying the v154 size guard. Both reduced denominators are powers of the same prime. There are arbitrarily large common denominator exponents and, for fixed admissible small-Pell witness, arbitrarily large distinct \(\Lambda\)'s.

The proof is unconditional arithmetic. It uses the classical finiteness of the ideal class group of a quadratic number field, Hensel lifting, irrational rotation, and the three- and four-square theorems. No abc, elliptic rank hypothesis, conjecture about rational points on varying higher-genus curves, primitive divisor theorem, or prime-pattern hypothesis is used. It rules out the proposed seven-certificate source for the covered exponents, **not** other nonlinear certificates or a general lower bound. The preferred v155 polynomial systems still use the separate certificates and are not affected.

Throughout, \(X_n(a)+Y_n(a)\sqrt{a^2-1}=(a+\sqrt{a^2-1})^n\), also for negative integer exponents, so \(Y_{-n}=-Y_n\). In this document \(d\) denotes the exponent of the nonlinear certificate; the first Pell trace is denoted by \(d_0\).

## 1. Two norm-one groups with a common single-prime denominator

We first prove an auxiliary lemma for fixed positive nonsquare integers \(\Delta_1,\Delta_2\), with \(\Delta_i=P_i^2-1\), \(P_i\ge2\). Suppose \(b_i\) are integers, \(n_i>0\) are integers, and the congruence conditions
\[
 Y_{t_i+T_i l}(P_i)\equiv b_i\pmod{n_i}\qquad(l\in\mathbb Z)
 \tag{1}
\]
hold for integers \(t_i,T_i\), \(T_i>0\). Suppose there is an odd prime \(p\nmid n_1n_2\Delta_1\Delta_2\) at which both discriminants are squares. Choose square roots \(\delta_i=\sqrt{\Delta_i}\) in \(\mathbb Z_p^\times\), equivalently specified by their nonzero residues in \(\mathbb F_p\). Put \(\epsilon_i=P_i+\sqrt{\Delta_i}\) in the real quadratic fields, with the positive real square roots; their \(p\)-adic images use the chosen \(\delta_i\).

Assume that
\[
 v_p(\epsilon_2^{T_2(p-1)}-1)=1
 \tag{2}
\]
in this \(p\)-adic embedding. Define the nonzero residue classes
\[
 h_*=\frac{\epsilon_1^{t_1}}{2\delta_1 n_1}\bmod p,\qquad
 j_*=\frac{\epsilon_2^{t_2}}{2\delta_2 n_2}\bmod p .
 \tag{3}
\]
Let \(d\) be a positive even integer such that \((j_*/h_*)^d=-1\) in \(\mathbb F_p^\times\). For any nonempty bounded open interval \(\mathcal I\) for the real small ordinate \(k\), there are rational numbers \(k,H,\tau,I,h,j\) satisfying
\[
 \tau^2-\Delta_1 k^2=1,\qquad I^2-\Delta_2 H^2=1,\qquad
 k=b_1+n_1h,\quad H=b_2+n_2j,
 \tag{4}
\]
with \(k\in\mathcal I\), \(h,j\in\mathbb Z[1/p]\) of the same exact negative valuation \(-E\), and
\[
 \Lambda=h^d+j^d\in\mathbb Z.
 \tag{5}
\]
The exponents \(E\) are arbitrarily large. For a fixed such \(k,\tau,h,E\), one can choose \(j>0\) arbitrarily large, in particular to meet any finite lower bound on \(\Lambda\). If \(\mathcal I\subset(b_1,\infty)\), then both quotients can be required positive.

### 1.1. Constructing the single-prime norm-one elements

For each \(i\) let \(K_i=\mathbb Q(\sqrt{\Delta_i})\), with maximal order \(\mathcal O_i\), and let \(R_i=\mathbb Z[\sqrt{\Delta_i}]\) (not necessarily maximal). Let \(m_i=[\mathcal O_i:R_i]\). Since \(p\nmid\Delta_i\), it does not divide \(m_i\); this also follows from the discriminant-index identity with discriminant \(4\Delta_i\). The chosen embedding specifies one of the two primes \(\mathfrak p_i,\overline{\mathfrak p_i}\) above \(p\). The two primes have residue degree one and ramification index one because the defining quadratic has distinct roots modulo \(p\).

Finiteness of the ideal class group gives an \(e_i'>0\) such that \(\mathfrak p_i^{e_i'}=(\alpha_i)\) is principal. The ideal norm identity gives \(|N_{K_i/\mathbb Q}\alpha_i|=p^{e_i'}\). Hence \(\bar\alpha_i/\alpha_i\) is a norm-one unit of \(\mathcal O_i[1/p]\), with valuations \(-e_i',e_i'\) in the two chosen local factors, and no other nonzero finite valuations. The ring \(\mathcal O_i[1/p]/n_i m_i\mathcal O_i[1/p]\) is finite, since \(p\) is prime to \(n_i m_i\), and the image of this unit is invertible. Raise it to a positive even multiple of its finite unit-group order in this quotient. The result \(\omega_i\) is positive at both real embeddings, has norm one, and satisfies
\[
 \omega_i\in 1+n_i R_i[1/p],\qquad v_p(\omega_i)=-e_i<0 .
 \tag{6}
\]
Indeed \(m_i\mathcal O_i\subseteq R_i\), so the congruence in the maximal order implies the asserted congruence in the Pell order. Its inverse (its quadratic conjugate) satisfies the same localization and congruence requirements. This proves (6) without any assumption about the class number being one, nor any bound on the class number.

Choose \(e=\operatorname{lcm}(e_1,e_2)\) and replace \(\omega_i\) by \(\Omega_i=\omega_i^{e/e_i}\). Both have valuation \(-e\). In the chosen embedding, \(p^e\Omega_i\) is a unit. Restrict a positive integer \(n\) to multiples of \(p-1\). With \(E=en\), we have
\[
 p^E\Omega_i^n\equiv1\pmod p.
 \tag{7}
\]

### 1.2. The real margin is compatible with the denominator and all congruences

Consider
\[
 \alpha=\Omega_1^n\epsilon_1^{t_1+T_1(p-1)L},\qquad L\in\mathbb Z,
 \qquad
 k=\frac{\alpha-\bar\alpha}{2\sqrt{\Delta_1}},\quad
 \tau=\frac{\alpha+\bar\alpha}{2}.
 \tag{8}
\]
Its norm is one, and its two coordinates belong to \(\mathbb Z[1/p]\) by (6). The congruence (1), interpreted in the localized order, gives \(k\equiv b_1\bmod n_1\mathbb Z[1/p]\). Thus \(h=(k-b_1)/n_1\) belongs to \(\mathbb Z[1/p]\). At \(p\) the two norm-unit terms have valuations \(-E,E\); it follows that \(v_p(h)=-E\), and
\[
 p^E h\equiv h_*\pmod p .
 \tag{9}
\]
This is valid for every integer \(L\), including negative values.

The real numbers \(\log\Omega_1\) and \(\log\epsilon_1\) have irrational ratio: a rational relation, on exponentiating, would identify a nontrivial power of \(\Omega_1\) with an integer power of \(\epsilon_1\); taking the chosen \(p\)-adic valuation contradicts \(-e\ne0\), since \(\epsilon_1\) is a local unit. Therefore as \(n\) ranges over positive multiples of \(p-1\), the values of
\(\log(\Omega_1^n)+t_1\log\epsilon_1\) modulo \(T_1(p-1)\log\epsilon_1\) are dense in that real circle, with arbitrarily large \(n\) in every open arc. Adding the integer multiples indexed by \(L\) gives a value in any prescribed nonempty open interval on the real line. The real map from \(\log\alpha\) to \(k\) in (8) is strictly increasing and onto \(\mathbb R\), since \(\bar\alpha=\alpha^{-1}\) and \(\alpha>0\). We can therefore choose arbitrarily large \(n\) and an \(L\) so that \(k\in\mathcal I\), while (9) and every congruence away from \(p\) continue to hold.

### 1.3. Use the third norm to make the power sum exactly integral

Fix \(n,L,h\) from (8). Let \(h_p=p^E h\in\mathbb Z_p^\times\). Because \(d\) is even and \(p\) is odd, choose the Teichmüller lift \(\zeta\in\mathbb Z_p^\times\) of \(j_*/h_*\). It satisfies \(\zeta^d=-1\): its \(d\)-th power is a root of unity of order dividing \(p-1\), with residue \(-1\). This argument does **not** require \(p\nmid d\).

Use
\[
 \alpha_2=\Omega_2^n\epsilon_2^{t_2+T_2(p-1)J},\qquad J\in\mathbb Z .
\]
The corresponding \(H,I\) and \(j=(H-b_2)/n_2\) as in (8) are in \(\mathbb Z[1/p]\), satisfy (4), and \(v_p(j)=-E\). If \(w=p^E\Omega_2^n\epsilon_2^{t_2}\in\mathbb Z_p^\times\) and \(u=\epsilon_2^{T_2(p-1)J}\), then
\[
 p^E j=\Phi(u)
 :=\frac{w u-p^{2E}w^{-1}u^{-1}}{2\delta_2 n_2}
       -\frac{p^E b_2}{n_2} .
 \tag{10}
\]
For \(u\in1+p\mathbb Z_p\) the residue of this expression is \(j_*\), by (7), and its derivative is a \(p\)-adic unit. Multiplying the equation \(\Phi(u)=\zeta h_p\) by the unit \(u\) gives a quadratic over \(\mathbb Z_p\) with a simple root \(u=1\bmod p\). Hensel's lemma gives a solution \(u_*\in1+p\mathbb Z_p\). By (2), the powers of \(\epsilon_2^{T_2(p-1)}\) exhaust \(1+p\mathbb Z_p\) modulo each \(p^N\): the binomial valuation formula \(v_p((1+z)^m-1)=v_p(z)+v_p(m)\) for \(v_p(z)\ge1\) proves that their order modulo \(p^N\) is \(p^{N-1}\). Choose \(J\) so that \(u\equiv u_*\bmod p^{dE}\); the solutions include a full arithmetic progression. It follows that
\[
 (p^Eh)^d+(p^E j)^d\equiv
 h_p^d+(\zeta h_p)^d=0\pmod{p^{dE}} .
\]
Since \(h,j\in\mathbb Z[1/p]\), the sum in (5) is integral at every prime, not just at the selected one. Finally \(J\) can be made arbitrarily large and positive in this progression. At the real place \(\epsilon_2>1\) and \(\Omega_2>0\), so \(j\) tends to positive infinity and (5) can satisfy any lower bound. This completes the lemma. Notice that \(\Lambda\) has been allowed to vary. We have not used or contradicted any weak approximation theorem on a fixed high-genus fiber.

## 2. Specialization to every actual sparse-packed instance

Use the exact prefix of [v145](../sparse_radix_v145/README.md), still present in the v155 general compiler. Its inner 63-variable natural source is specialized first; hence the positive integer \(\beta=4^{z_0}\) in its radix is already fixed. The following choices work for every such \(z_0\), independent of its size and of the coefficients of the inner quadrics.

Write \(\mathcal D=2^{45}\) for the fixed packing center (\(64\cdot2^{37+2}\)), and let \(B=2r+1\) denote the intended first Pell index (not the radix). Take
\[
 b=4^u,\quad f=2^{u-1},\quad
 \mathcal B=\beta b^2=2^{L_{\mathcal B}},\quad L_{\mathcal B}=2z_0+4u,
 \qquad N_0=\mathcal B^{2\mathcal D},\quad V_{\rm pack}=\mathcal B^{8\mathcal D}.
\]
The prefix has \(N=4N_0V_{\rm pack}=2^{E_N}\), \(M=N^2\), where \(E_N=2+10\mathcal D L_{\mathcal B}\), and
\[
 \begin{split}
 K(g)&=(g+d_{\rm dummy})^2 P_{\rm pack}
          +(\mathcal B/2)(V_{\rm pack}-1)/(\mathcal B-1),\\
 S(g)&=g+2K(g)N_0,\qquad
 T=N_0-1-(b-1)\sum_{i\ge1}\mathcal B^{n_i}
       +(\mathcal B-2)N_0\sum_{j=0}^{63}\mathcal B^{4\mathcal D+j},\\
 r(g)&=(N-1)\big((S(g)+T+1)N+T+1\big).
 \end{split}                                                   \tag{11}
\]
Here \(P_{\rm pack}\), \(d_{\rm dummy}\) and the active positions \(n_i\) are exactly those of the parent compiler; in particular the geometric quotient is an integer. No property of the integer \(P_{\rm pack}\) modulo the new prime is assumed.

Since \(N\equiv1\bmod3\), \(3\mid r\). Also \(N,T+1\) are divisible by \(2^{41}\) (in fact by a vastly higher power), since all the active digit positions are at least \(3\mathcal D/4\) and \(\mathcal B\) is an even power of two. Thus
\[
 3\cdot2^{41}\mid r.
 \tag{12}
\]
All the primes used below have \(p-1=2^K\) or \(3\cdot2^K\) with \(K\le41\), so \(r\equiv0\bmod p-1\), \(B\equiv1\bmod p-1\), and \(r\) is even.

For each prescribed \(t=v_2(d)\in\{1,\ldots,40\}\) choose a row from [residue_certificates.csv](residue_certificates.csv) for \(z_0\bmod3\); a row with beta class -1 works for all three residues. The row specifies \(p,u,\sigma,\mu,V,\delta_{1,0},\delta_{2,0},l\) with \(\sigma=\pm1,\ \mu=1\) or \(3\), and the expected normalized residue ratio. The columns of the CSV are literal integers with header
\[
 t,\ z_0\bmod3,\ p,\ u,\ \sigma,\ \mu,\ V,\
 \delta_{1,0},\ \delta_{2,0},\ l,\ \text{ratio}.
\]
Set \(w=2^B/b\), \(U=wM\), \(Y=sM\) (s to be chosen). All of \(w,U\) are positive integers because \(B\) is much larger than \(2u\) by the prefix size. Then, modulo \(p\), (12) gives
\[
 U\equiv 2M/b,\qquad
 a=(U+1)rY,\quad P=1+2U r^2Y^2 .
 \tag{13}
\]
The finite table is constructed to make \(N\not\equiv1\bmod p\) and \(U+1\) a unit. Given \(r\not\equiv0\bmod p\), choose \(s\) so that \(r sM\equiv V\bmod p\). Its prescribed residues then give
\[
 a_0\equiv\sigma/2,\quad
 P\equiv1+2UV^2,\quad
 \Delta_1=P^2-1\equiv\delta_{1,0}^2\ne0\bmod p .
 \tag{14}
\]
The dependence of \(N\bmod p\) on \(z_0\) is only through its residue modulo 3: \(10\mathcal D\) is divisible by the full 2-part of \(p-1\), and the odd part is one or three. This proves that the finite check for each class applies to all source coefficients with that class.

### 2.1. Choose the packed integer g, without any favorable-coefficient assumption

Modulo \(p\), (11) is a nonconstant polynomial of degree at most two in \(g\). Indeed \(N(N-1)\ne0\); if \(P_{\rm pack}\not\equiv0\bmod p\) its quadratic coefficient is nonzero, and if \(P_{\rm pack}\equiv0\bmod p\) its linear coefficient is \(N(N-1)\ne0\). Its value set has cardinality at least \((p+1)/2\). We exclude at most three values of \(r\bmod p\): zero, \(B=2r+1=0\bmod p\), and the possible single value making the derivative in (18) below zero. Every table prime is at least 13. Thus some residue class of \(g\) gives an allowed \(r\). Choose \(g\) in the interval \(1,\ldots,p\) in that class.

This is an admissible packed prefix: \(g<N_0\) and the original interval guard has its usual integer nonnegative slack. Moreover this \(g\) always gives a **false** digit tuple: \(g>0\), \(g<\mathcal B^{\min n_i}\), and the mask in the low block of \(T\) has every bit equal to one below the first active digit position. Hence the binary sum has a carry, so the v142/v145 carry equivalence gives \(M\nmid\binom{2r}{r}\). The bounds \(r\ge N^2-1\), \(M\ge4b\), \(M^2>3r+2\), \(M\ge16\) and \(3\mid Mr\) of the retained v148/v150 construction all hold. In particular no assertion about the truth of the source instance is needed; every no-instance has a false prefix of this form.

### 2.2. The fixed first and second Pell data

Choose positive \(s\) with the prescribed class in (14) for the moment. It may be increased in that class and later refined modulo \(p^2\). Put
\[
 c=Y_B(a),\quad d_0=X_B(a),\quad
 \gamma=\frac{d_0-(a-2)c-bw}{4a-5}.
\]
The shifted trace recurrence in v101/v151 gives positive integral \(\gamma\): \(X_n-(a-2)Y_n\equiv 2^n\bmod 4a-5\) by its recurrence, and \(bw=2^B\). The halftrace square is supplied by \(\zeta_0=2X_{r+1}(a)\). These are exactly the retained first norm and shifted trace. In particular \(c\) is odd, \(c>B\) and \(c>a\). The simple identities modulo 6 give \(c\equiv1\bmod6\), since \(a\equiv0\bmod6\) and \(r\) is even.

Set the second Pell exponent
\[
 q=4\mu B c,\qquad F=X_q(a),\quad i'=Y_q(a)/(M c^2).
 \tag{15}
\]
The binomial expansion of \((d_0+c\sqrt{a^2-1})^c\) gives \(c^2\mid Y_{Bc}(a)\), and hence \(c^2\mid Y_q(a)\). Since \(a\equiv0\bmod M\) and \(q\) is even, \(Y_q(a)\equiv0\bmod M\). Also \(c\) is odd and \(M\) a power of two, so these imply \(Mc^2\mid Y_q(a)\). Thus \(i'>0\) is an integer, and the modified second Pell norm is exact. Put
\[
 G=a+F^2(c+1-a),\qquad
 b_1=r+1,\quad n_1=M^2,\quad
 b_2=c+F^2(B-c),\quad n_2=cF .
 \tag{16}
\]
We have \(G\ge c+1\), so \(\Delta_2=G^2-1>0\) is nonsquare. Both coprime-modulus properties of v148 hold: \(c\) is a unit modulo \(M\), \(F^2\equiv1\bmod M\), so \(\gcd(n_1,n_2)=1\). Both \(\Delta_1,\Delta_2\) are positive nonsquares for the actual positive \(s\).

We now check the local identities. At \(a_0=\sigma/2\) in the quadratic algebra over \(\mathbb F_p\), the norm-one element \(\epsilon_a=a_0+\sqrt{a_0^2-1}\) has sixth power one: \(X_3(a_0)=-\sigma,\ Y_3(a_0)=0\). By (12), \(B\equiv1\bmod6\), so \(c\equiv1\bmod p,\ X_B(a)\equiv a_0\bmod p\), regardless of whether the quadratic algebra splits. Since \(c\equiv1\bmod6\) as well, the exponent \(q=4\mu Bc\) has the following residues:
\[
 \begin{array}{c|cc}
 & F\bmod p &Y_q(a)\bmod p\\ \hline
 \mu=1 &-1/2&-\sigma\\
 \mu=3 &1&0 .
 \end{array}                                                   \tag{17}
\]
They follow directly from \(\epsilon_a^{4}\), respectively \(\epsilon_a^{12}\). The table checks that \(\Delta_2\bmod p=(a_0+F^2(2-a_0))^2-1\) is the nonzero square \(\delta_{2,0}^2\). Hence \(p\nmid n_1n_2\Delta_1\Delta_2\). Also \(p\nmid q\) by the choice of \(B\) and \(c\equiv1\bmod p\); \(p\ne2,3\).

### 2.3. Obtain the full principal-unit variation at p

The freedom to choose a lift of \(s\bmod p^2\) avoids any non-Wieferich hypothesis. For all lifts, \(c\equiv1\bmod6p\), hence the variable exponent \(q=4\mu Bc\) is constant modulo \(6p\). In the Pell algebra modulo \(p^2\), \(\epsilon_a^{6p}=1\) because \(\epsilon_a^6\equiv1\bmod p\). Thus for differentiating \(F\bmod p^2\) along these lifts, use a single fixed exponent \(q_0\equiv4\mu B\bmod6p\). The classical polynomial derivative identities are
\[
 X_n'(a)=nY_n(a),\qquad
 (a^2-1)Y_n'(a)=nX_n(a)-aY_n(a).
\]
In particular \(c'\equiv-2\sigma(B-1)/3\bmod p\). Differentiating \(G=a+F^2(c+1-a)\), using (17), gives
\[
 G'(a_0)\equiv
 \begin{cases}
 (70B+11)/12,& \mu=1,\ \sigma=1,\\
 (7-118B)/12,& \mu=1,\ \sigma=-1,\\
 -2\sigma(B-1)/3,& \mu=3 .
 \end{cases} \pmod p .                                         \tag{18}
\]
Each is a nonzero affine polynomial or nonzero constant in \(B\bmod p\) (the displayed numerator coefficients have greatest common divisor one). The choice of \(g\) in section 2.1 avoids its zero. The derivative of \(a\) with respect to \(s\) is the unit \((U+1)rM\) modulo \(p\). Consequently the possible \(s\)-lifts give every lift of the prescribed \(G\bmod p\) modulo \(p^2\).

At this split residue \(X_{p-1}(G)\equiv1,\ Y_{p-1}(G)\equiv0\bmod p\); the derivative formula shows \(Y_{p-1}'(G)\equiv-1/\Delta_2\bmod p\), a unit. Thus choose an \(s\)-lift for which \(Y_{p-1}(G)\not\equiv0\bmod p^2\), and then choose a sufficiently large positive integer \(s\) in this class. The norm identity gives \(X_{p-1}(G)-1\equiv0\bmod p^2\). In either chosen local embedding this proves
\[
 v_p((G+\sqrt{\Delta_2})^{p-1}-1)=1.
 \tag{19}
\]
Since \(p\nmid4q\), the binomial valuation formula gives (2) with \(T_2=4q\).

### 2.4. Match both original modulus conditions and the power-sum residues

For the first congruence of (1) take \(P_1=P\), \(T_1=M^2\), and \(t_1\equiv r+1\bmod M^2\), since \(P\equiv1\bmod M^2\). Here choose
\[
 t_1=r+1+M^2l_0,\qquad
 M^2l_0\equiv2^K l\bmod p-1 .
\]
This is possible because \(p-1=2^K\cdot\text{odd}\), with odd part one or three, and \(M^2\) is a sufficiently high power of two. By (12) the first unit residue is then \((P+\delta_{1,0})^{1+2^Kl}\).

For the second congruence of (1) take \(P_2=G\), \(t_2=B,\ T_2=4q\). The exact v95 identities give for all integer \(v\equiv B\bmod4q\)
\[
 G\equiv1\bmod c,\quad G\equiv a\bmod F,\quad
 Y_v(G)\equiv B\bmod c,\quad Y_v(G)\equiv c\bmod F.
\]
Indeed \(c\mid q,\ F^2\equiv1\bmod c\) and \(\gcd(c,F)=1\); reducing the Pell identity gives period \(4q\) for the ordinate modulo \(X_q(a)=F\). This also works for negative exponents by the signed recurrence. Therefore \(Y_v(G)\equiv b_2\bmod cF\), the exact redesigned third-ordinate congruence, not merely the condition at \(p\). Note that we chose \(c=Y_B(a)\) for this construction even though the prefix is false.

The selected \(p\)-adic square roots of \(\Delta_i\) are the Hensel lifts of the two table roots. Equations (3) become exactly the checked residue pair
\[
 h_*=\frac{(P+\delta_{1,0})^{1+2^Kl}}{2\delta_{1,0}M^2},\qquad
 j_*=\frac{G+\delta_{2,0}}{2\delta_{2,0}F}\quad\bmod p,
 \tag{20}
\]
using \(c\equiv1\bmod p,\ B\equiv1\bmod p-1\). The table verifies that \(j_*/h_*\) has exact order \(2^{t+1}\) in \(\mathbb F_p^\times\), so \((j_*/h_*)^d=-1\) for every positive exponent with \(v_2(d)=t\). We have now checked every hypothesis of section 1 using the actual specialized packed data.

## 3. Full false source witnesses and the actual margin equations

With the fixed positive integers above, \(c/Y>r+1\) and \(c/Y>1\), for example by \(a=(U+1)rY\) and \(c\ge4a^2-1\). At \(k=c/Y\),
\[
 \eta=k^2-4(c-kY)^2=(c/Y)^2>1 .
\]
Choose a bounded nonempty open interval \(\mathcal I\) around \(c/Y\), contained in \(k>r+1,\ \eta>1\). Apply section 1. It supplies \(k,\tau,H,I,h,j\) satisfying both rational norms, both congruence rows, \(h,j>0\) with common reduced denominator \(p^E>1\), and
\[
 \Lambda=h^d+j^d\in\mathbb Z,\qquad
 \Lambda>(b_1^2+b_2^2+2)^{d/2}.
\]
The last inequality is available by increasing the third-unit exponent in its permitted progression, keeping the small witness fixed. The nonnegative integer difference after subtracting the bound and 1 is a sum of four integer squares, so the additional guard of v154 has its actual rational polynomial witnesses.

Since all four norm coordinates and both quotients lie in \(\mathbb Z[1/p]\), \(k\in\mathbb Z_2\) and \(\eta\in\mathbb Z_2\). The strict margin gives \(8\eta-5>0\), with \(8\eta-5\equiv3\bmod8\) in \(\mathbb Z_2\). Write \(8\eta-5=A_*/B_*\) in lowest terms, \(B_*>0\) odd. Then \(A_* B_*>0\) is an integer congruent to 3 modulo 8. Legendre's three-square theorem supplies integers \(z_1,z_2,z_3\) with \(A_* B_*=\sum z_i^2\). The rational numbers \(u_i=(z_i/B_*-1)/2\) satisfy
\[
 2(\eta-1)=\sum_i u_i(u_i+1).
\]
These are precisely the rational triangular rows of the outer binomial margin. The retained helper coordinates are then defined by their equations, including the modified small parameter, the second quotient \(i'\), and the third CRT ordinate. All other proposed certified inputs \(f,g+1,w,s,\gamma,i',\Lambda\) are nonzero integers. Both \(h,j\) and both \(k,H\) are nonintegral because the common denominator prime is coprime to both congruence moduli. We have thus constructed actual rational zeros of the **proposed modified source** on a packed tuple known to fail central-binomial divisibility. They work on every no-instance of the inner coding problem by choosing the prefix as above. Under the retained simultaneous integer-tuple interface premises, that proposed seven-input transfer would also have false rational zeros.

This proof does not put infinitely many rational points on a single fixed v154 high-genus curve: \(\Lambda\) changes. In fact for each fixed small witness, \(j\) can be made arbitrarily large in a progression, giving infinitely many different admissible \(\Lambda\)'s. Every such value satisfies the guard of v154 and its geometric genus statement, including genus five for \(d=2\) and genus 25 for \(d=4\). It is the family of fibers, not the rational points of one fiber, that is exploited.

## 4. Generalization and scope

The S-unit argument gives a test for other proposed nonlinear integer certificates. Under the hypotheses of section 1 through (3), let \(\Phi(h,j)\in\mathbb Z[h,j]\) have total degree \(D_0\ge1\), and let \(\Phi_{\rm top}\) be its homogeneous part of degree \(D_0\). If
\[
 \Phi_{\rm top}(h_*,j_*)=0\bmod p,\qquad
 \partial_2\Phi_{\rm top}(h_*,j_*)\ne0\bmod p,
\]
the same construction makes \(\Phi(h,j)\) integral with both \(h,j\) nonintegral, and arbitrary prescribed real small-ordinate margin. To see this, at fixed \(h_p=p^E h\) use the polynomial over \(\mathbb Z_p\) in \(J_p\)
\(p^{D_0 E}\Phi(h_p/p^E,J_p/p^E)\). Its reduction is \(\Phi_{\rm top}(h_*,J_p)\); it has a simple root at \(j_*\). Hensel gives a target \(J_p\equiv j_*\bmod p\). Equation (10) and the principal-unit variation approximate that root modulo \(p^{D_0 E}\), proving the integrality globally. If the polynomial tends to positive infinity as \(j\to+\infty\) with this \(h\) fixed, any lower guard on its value can also be met. In the pure power-sum case the Teichmüller argument was stronger because no derivative assumption on \(d\bmod p\) was needed. This is a sufficient counterexample criterion, not a universal obstruction for every polynomial.

The fixed finite table proves failure for every \(d\) with \(1\le v_2(d)\le40\). It does not prove failure for exponents with \(2^{41}\mid d\), or for an additional equation coupling the rational witnesses to other variables in a genuinely different way. In the ordinary straightforward quadratic compilation a pure power exponent with \(v_2(d)\ge41\) would already require many successive squares of both quotients; no general arithmetic-circuit lower bound is asserted. The present result is a strong reason to abandon the unmodified power-sum merger as a practical source reduction, not a proof that all seven-integer sources are impossible.


## 5. Why a straightforward polynomial upper cap on the third quotient is not a canonical repair

There is also an elementary size obstacle to supplementing the power sum by an upper bound of fixed polynomial degree in the pre-third-Pell data. This statement concerns the positive canonical binomial completion with arbitrarily large intended index \(B=2r+1\); it is not a claim about arbitrary alternative source presentations.

For \(c=Y_B(a)\), the positive second norm has \(F=X_q(a)\) with \(q\ge c>B\), so \(F>c\ge2a\). The bridge satisfies \(G=a+F^2(c+1-a)>F^2\) and \(|b_2|=|c+F^2(B-c)|\le F^2c\). For any *integral* third quotient \(j\) with the two exact retained congruences, the signed v95 comparison modulo \(F\) gives \(v\equiv\pm B\bmod2q\) for the absolute third Pell index \(v\). Because \(0<B<q\), \(v\ge B\). Thus
\[
 |H|=Y_v(G)\ge G^{B-1}>F^{2B-2},\qquad
 |j|=\frac{|H-b_2|}{cF}>
 \frac{F^{2B-2}-F^3}{F^2}\ge\frac12 F^{2B-4}.
\]
The last inequality holds for \(B\ge3,F\ge2\). On these same canonical completions the old pre-third parameters \(a,c,d_0,w,s,M,r,b,P,G,F,i',\gamma,b_1,n_1,b_2,n_2\) are bounded in magnitude by fixed powers of \(F\) with absolute constant factors: \(w,s,M,r,b\le a\), \(d_0\le ac\), \(P\le1+2a^2\), \(G\le a+F^2(c+1)\), \(i'\le F\), \(|\gamma|\le d_0+ac+bw\), \(n_1=M^2,n_2=cF\), and \(b_2\) has the preceding bound. Here the inequalities involving \(b\) use \(b\le M/4\), and the positivity of the canonical parameters is essential.

Consequently a fixed polynomial magnitude bound on \(|j|\), or on the positive even-power sum \(\Lambda\ge j^d\), expressed solely in this list of already fixed pre-third-Pell data, cannot preserve the binomial completion for all valid prefixes with unbounded \(B\). A bound using the exponent \(B\) in an essential way, a different relation, or a different coding source could behave differently. This rules out one simple proposed response to the unbounded third-unit variation of the counterexample proof. It is not a lower bound on the size of every possible witness system.

## 6. Exact certificates, references and verification scope

The modular table contains 106 literal rows covering all 120 pairs \((v_2(d),z_0\bmod3)\) with \(1\le v_2(d)\le40\). It uses twelve primes, the largest \(6597069766657=3\cdot2^{41}+1\). The [independent verifier](verify.mjs) checks primality by exact order certificates (an element of order \(p-1\) modulo every prime divisor forces that prime divisor to be \(p\)), the residue identities (14),(17),(20), the exact 2-power orders, and the coverage. It also independently checks the derivative and lift calculations modulo \(p^2\) on four representative large \(r\)'s per profile. All computations are exact integers; no factorization of the astronomical Pell numbers is performed. See the [executed receipt](verification.json). The finite checks verify the finite constants in a quantified proof, not a finite numerical search extrapolated to all source instances.

Class-group finiteness is the classical Minkowski theorem; see the precise statement in J.-H. Evertse, [*Diophantine equations*, algebraic number theory notes](https://pub.math.leidenuniv.nl/~evertsejh/dio2011-algnumbers.pdf), Theorem 1.4.1, or MIT 18.785 [Lecture 13, Theorem 13.18](https://opencw.aprende.org/courses/mathematics/18-785-number-theory-i-fall-2015/lecture-notes/MIT18_785F15_Lec13.pdf). The use of Hensel, the binomial valuation formula and the lifting of roots of unity is standard (the elementary valuation formula is explicitly proved in section 4 of [these local-field notes](https://openmaths.org/courses/NT-LOC/NT-LOC-03.html)). The congruences of the third Pell ordinate are the proved identities in [v95](../pell_crt_v95/one_quotient_pell.tex). The binary carry reduction is the one already proved in [v142](../packed_quadrics_v142/README.md), with the exact packed constants from [v145](../sparse_radix_v145/README.md). Only the hypothetical nonlinear source is disproved; no new positive variable bound or independent discharge of the retained integer-interface assumptions is claimed.
