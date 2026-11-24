# A one-pole simple-denominator amplifier and Lucas-free general routes

## Statement and scope

Work over the original quadratic carrier
\[
 K=\mathbb Q(\sqrt2),\quad d=3-\sqrt2,\quad D=d^2,\quad
 E:y^2=x^3-Dx,\quad
 P=(57/8-7\sqrt2/2,\,-165/8+417\sqrt2/32).
\]
Retain the rank-one square-abscissa chart of the general sources:
its rational characters give precisely the nonzero integer multiples of \(P\).

For an integer \(c\ne0\), define \(R(c)\) to be the product of the rational primes \(p\) of good reduction, unramified in \(K\), outside \(\{2,7,29\}\), at which the maximum of the formal depths of \([c]P\) over the places above \(p\) is exactly one. A nonformal point has depth zero. **No primitive-prime condition is imposed.** Introduce the following additional arithmetic hypothesis:
\[
 \tag{SD} \log R(c)\ge |c| \qquad (|c|\ge c_*).
\]
Here \(c_*\) is some fixed finite threshold. This is a simple-denominator mass hypothesis for one fixed elliptic curve and point, not a consequence asserted of the existing modular-height premises. Section 5 proves it under a fixed weak abc inequality over \(K\) of exponent \(\kappa<12/11\). Such a consequence does not make (SD) unconditional.

**Theorem.** Retain all the arithmetic premises of the respective general [v78](../../few_variables25/four_contact_scalar_20261119_v78.tex) and [v88](../../few_variables25/bb_product_degree_transfer_20261123_v88.tex) constructions and additionally assume (SD).

* The two-scale route has a defining polynomial for \(\mathbb Z\) in **19 total rational coordinates**, rather than 25.
* The three-scale route has one in **21 total rational coordinates**, rather than 27. If a valid effective value of \(c_*\) is provided, its coefficient is completely specified by taking the smallest odd \(L\ge143\) with \(67^{2L+1}\ge c_*\). Without such a bound the sufficient choice of \(L\) is ineffective, including when (SD) is deduced from a conjectural weak abc inequality with unspecified constant.

These are conditional alternatives with an extra hypothesis. They do **not** replace the existing no-additional-abc general variable records or the fixed \(L=143\) explicit record. Nor are they improvements on the 11-coordinate ordinary/weak rational abc routes in their overlapping hypothesis range. Their purpose is to isolate a much more specific growth premise and remove the Lucas recurrence altogether. No numerical degree or quartic bound is asserted here.

## 1. Local amplifier on the original carrier

Write \(Q=[c]P\), with \(c\ne0\), and take an independent point \(T=[j]P\), \(j\ne0\). Put \(y(Q)=y_0+y_1\sqrt2\). Use a two-element fixed disjunction \(\epsilon\in\{1,2\}\), and define
\[
 \ell=y_0^5+\epsilon y_1^7\ne0,\qquad
 z(B)=-x(B)/y(B),\quad
 Z=\ell^2/x(T)^{24},\quad \chi=(1+Z)^{-1},
\]
\[
 F=z(T)/z(Q),\qquad J=F^2/(\ell^{-1}+F^2),\qquad
 C=2-\operatorname{Tr}_{K/\mathbb Q}\bigl(\chi(1-J)\bigr).
\]
Require the displayed denominators to be nonzero. The two branches suffice because the nonzero ordinate \(y(Q)\) has at least one nonzero rational component, and if both expressions vanished, subtraction would give \(y_1=0\) and then \(y_0=0\). Define the rational pole argument
\[
 b=1+\ell C^2,\qquad e=112b/841,
\]
and impose \(e\ne0\) and the BB product-pole equation
\[
 Y^2=(1-e)(v^4-e^2)(s^4-e^2).
\]
Only \(v,s\) are ordinary new pole variables. The terminal root \(Y\) is finite, and may be zero. The elementary negative-odd-valuation obstruction and the prepared converse are those of v88.

At any unramified odd rational prime with \(\nu=v_p(\ell)\) odd, the valuation of \(Z\) at every slot above \(p\) is
\[
 2\nu-24v(x(T))\equiv2\pmod4.
\]
Thus \(\chi\) is integral and its residue is 0 or 1, with residue 1 exactly when \(v(Z)>0\). In the denominator of \(J\), the terms \(\ell^{-1}\) and \(F^2\) have distinct parity of valuation; hence \(J\) too is integral with residue 0 or 1. The zero numerator case is included. Its residue is 0 exactly when \(2v(F)>-\nu\).

If \(\nu<0\) is odd and \(p\notin\{2,7,29\}\), the pole equation forces
\[
 \tag{1} v_p(C)>-\nu/2.
\]
Otherwise \(v_p(\ell C^2)\) would be negative odd and adding 1 would not change it. Consequently \(C\equiv0\bmod p\). At a split prime the two residues of \(\chi(1-J)\) belong to \(\{0,1\}\), and their sum equals 2 modulo \(p\); both must be 1. At an inert prime the residue belongs to \(\{0,1\}\subset\mathbb F_p\), so its residue trace is twice that residue, with the same conclusion. Therefore
\[
 \tag{2} v(x(T))<0,\qquad 2v(z(T)/z(Q))>-\nu
\]
at **every** slot over \(p\). The first inequality follows from \(v(Z)>0\) and \(\nu<0\).

Now suppose \(p\mid R(c)\). In at least one slot \(v(y(Q))=-3\), and in every slot \(v(y(Q))\ge-3\). Since the basis \(1,\sqrt2\) is integral and its determinant is a unit at unramified odd \(p\), this is equivalent to
\[
 \min(v_p(y_0),v_p(y_1))=-3.
\]
At a split prime this follows by taking the half-sum and the scaled half-difference of the two local values. At an inert prime it follows from the integral basis of the unramified quadratic extension. If \(v_p(y_1)=-3\), then \(\nu=-21\): the other term has valuation at least \(-15\). Otherwise \(v_p(y_0)=-3\) and \(v_p(y_1)\ge-2\); then \(\nu=-15\), since the second term has valuation at least \(-14\). These are strict, noncancelling minima. In particular the asymmetrically chosen odd exponents 5 and 7 work in both branches and even when both original local depths are one.

At a slot where \(Q\) is formal of depth one, (2) puts \(T\) in the formal group as well. The isometric formal logarithm applied to \([c]T=[j]Q\) gives
\[
 v(z(T)/z(Q))=v_p(j/c).
\]
Since \(2v_p(j/c)>15\) or \(>21\), in either case \(p^8\mid j\). There is no need for \(p\) to be primitive for \(c\), or for \(p\) to split. Multiplying these divisibilities gives
\[
 \tag{3} R(c)^8\mid j,\qquad
 \log|j|\ge8\log R(c).
\]
This amplification is different from the Lucas polynomial: it reads the support of simple elliptic denominator primes directly, with a fixed rational pole.

## 2. Ordered completeness of the amplifier

Fix any allowed nonzero \(Q=[c]P\), then choose \(\epsilon\) with \(\ell\ne0\). The primes with negative odd valuation of \(\ell\), together with 2,7,29, form a finite set depending on \(Q\), not on \(T\). Choose \(j\) sufficiently divisible so that \(T=[j]P\) is arbitrarily deep in the formal groups at **all** places over those primes. Such divisibility is possible because the formal group is open of finite index in each compact local group, and subsequent multiplication brings a point arbitrarily close to the identity. For fixed \(Q,\ell\) this gives \(\chi\to1,J\to0,C\to0,b\to1\) locally. In particular \(b\) is a unit at every prepared prime, with \(b\equiv1\bmod8\) at two.

In the same divisibility progression choose \(j\) with \(T\) arbitrarily close to the identity at both real embeddings, by recurrence in the compact closure of the cyclic subgroup. This does not require the closure to be the whole product. The nonzero index can be arbitrarily large. The same limits hold over the reals; all rational expression denominators are then nonzero, and \(0<112b/841<1\).

At any other rational prime with odd positive valuation of \(\ell\), the local parity calculation of Section 1 makes \(C\) integral, so \(b\) is integral. At even valuations of \(\ell\), every negative valuation of \(1+\ell C^2\) is even. Hence every denominator of \(b\) is square in reduced form, including those at primes where the newly chosen point \(T\) happens to introduce foreign denominators. At 7 the fixed multiplier has valuation 1 and \(b\) is a unit, at 29 its valuation is even, and at two
\[
 v_2(e)=4,\qquad e\in7\mathbb Q_2^{\times2}.
\]
Thus the actual argument \(e\) is prepared for the BB converse. Supply \(v,s,Y\) after choosing \(T\). No simultaneous prime-pattern assumption is used in this amplifier completeness lemma.

## 3. Lucas-free defining sources

We give all changes to the unrestricted-degree arithmetic sources. Keep the v88 scalar, including its fixed odd \(L\):
\[
 \begin{split}
 \beta&=1632X^2+2477,\quad \tau=X^2+1,\\
 A_0&=\beta(\beta-1),\quad B_0=(\beta-2401)(32\beta+343),\\
 T_L&=(1224(67^{(L+1)/2}+1))^2,\quad q=T_L A_0/B_0,\\
 \rho&=102^2 67^L\,7q/(1+7q)^2.
 \end{split}
\]
Here \(\rho\) denotes the class-seven scalar \(\rho_*\) of v88. Retain just five point charts
\[
 A=[n]P,\quad S=[a]P,\quad T=[j]P,\quad H=[h]P,\quad U=[u]P .
\]
All five use the old square-abscissa chart; this is an allowed subfamily of the auxiliary charts. Require the indicated nonzero and affine-difference guards of the old sources. The three root points are now \(A,S,T\); put
\[
 c=|a-1|>0,\quad B=\max(1,|n|,|a|,|j|),\quad
 Q=S-P,\quad \mathcal Z=x(A)+x(S)+x(T).
\]
Impose the Section 1 amplifier on \(Q,T\). There is no Lucas residual, no fourth root, and no auxiliary comparison numerators for \(S,T\).

Use the six field tests, all of order one,
\[
 f(H),\ f(U),\ \sigma f(H-P),\ \sigma f(U-A),\
 r-r',\ r-\tau ,
 \quad f(W)=1/x(W),\ r=z(U)/z(H),\
 r'=\sigma(z(U-A)/z(H-P)).
\]
The six scalar tests \(S_k\) are unchanged: the two rational components of \(f(H),f(S-P),z(S-P)/z(H)\), with orders \((1,1,1,1,3,3)\).

For two scales take \(a_0=1,\ a_1=1+\rho(\operatorname{Tr}\mathcal Z)^2\). For three scales write \(\mathcal Z=U_0+S_0\sqrt2\), \(V_0=U_0+S_0\), and take \(a_0=1,a_1=1+\rho U_0^2,a_2=1+\rho V_0^2\). Use the v78 balanced contact functions with the single nonzero rational slope \(\lambda\):
\[
 \Theta=\{0,-1/2,-1,1/2399,-32/407\},\
 \Theta_i=(4i+2+\Theta)\cup(4i+4+\Theta),\
 t_i=a_i\lambda,\ \delta_i=t_i+i+1,\
 R_i=\prod_{\theta\in\Theta_i}(t_i-\theta)/\delta_i^{10},\
 w_i=\rho R_i.
\]
All contacts, \(R_i,\delta_i,w_i\) and divisions are guarded. For clarity we use the original v19/v28 squared-numerator product detector, which is convenient for the unrestricted-degree count; no degree optimization is claimed. For the six field tests \(C_k\) above put
\[
 G_{i,k}=R_i^{\kappa_k}\frac{R_i S_k}{1+R_i S_k},\qquad
 W_i=\prod_{k=1}^6\left(1+\frac{C_k^2}{\delta_i^2 w_i}\right)
       \prod_{k=1}^6\left(1+\frac{G_{i,k}^2}{w_i^{2\kappa_k-1}}\right),
\quad e_i=4w_i/\operatorname{Tr}(W_i^{-1})^2.
\]
The scalar denominators, the trace and \(e_i\) are nonzero. For every \(i\) impose the unnormalized BB product equation with argument \(e_i\), two independent ordinary parameters and one finite square root. At any odd valuation of \(w_i\), each nonzero detector second summand has odd valuation, hence the valuation of every factor is nonpositive and its inverse has residue 0 or 1 when the valuation of \(w_i\) is one. Thus the v19 extraction lemma applies to this reduced test list. In particular removal of the other ten tests does not weaken the required estimates on the six retained comparisons or on the six scalar components: the maximum slot valuation of the product still exceeds \(-v_p(w_i)/2\) by the pole obstruction, and each retained factor individually has valuation at least that of the product in the selected slot.

### Soundness and thresholds

The v78 scalar-unit argument is unchanged because \(\rho\) and the positive unsquared scales have the same rational form. At an odd \(\mu=v_p(\rho)\) at least one \(R_i\) is a unit outside the fixed scalar exceptions (also at 67); at that scale the six scalar estimates yield \(v_p(c)>9\mu/4\), using the full logarithm ratio \(z(S-P)/z(H)\). For a positive odd valuation of \(R_i\), either the odd scalar alternative gives \(p\mid c\), or the even scalar alternative gives positivity of the six field tests in one slot. They put \(H,U\) in the formal group at that slot, \(H-P,U-A\) in the group at the conjugate slot, and give \(r\equiv r'\equiv\tau\pmod p\). The exact logarithmic ratios are \(u/h,(u-n)/(h-1)\). At least one reference index is a unit at \(p\); the ratio comparison and relative logarithm precision make both ratios integral. Subtracting after multiplication by the respective reference indices yields \(n\equiv\tau\pmod p\). This uses only the remaining root \(A\), not any removed test. Consequently the old necessary divisibilities survive:
\[
 \tag{4}67^{2L+1}M_\beta^3\mid c,\qquad M_i\mid Nc
 \quad(N=\operatorname{num}(\tau-n)\ne0).
\]
Here \(M_\beta,M_i\) and their finite exceptional sets are exactly the corresponding v78 scalar and comparison radicals. The other local arithmetic checks (including the smaller prime 67 and the four-contact scalar normalization) are unchanged. In particular \(c\ge67^{2L+1}\).

For two scales, the v28/v78 estimate gives \(h(\beta)\le H_1c^{7/9}\) and \(h(t_i)\le H_2 M_i^{7/6}\), with fixed constants. The aggregate trace-height theorem v9 is stated for any fixed number of positive summands. Its three-point specialization gives \(B^2\ll h(\operatorname{Tr}\mathcal Z)+1\). The quotient of the two scales is \(1+\rho(\operatorname{Tr}\mathcal Z)^2\), so the ordinary height inequalities and the v88 bound on \(h(\rho)\) give
\[
 B^2\ll |Nc|^{7/6}+c^{7/9}+\log c+1
 \qquad(N\ne0).
\]
Since \(B\ge c-1\) and \(|Nc|\le2B c\,\exp(h(\beta))\), absorption of the final lower-order terms gives
\[
 \log B\le (7/5)\bigl(h(\beta)+\log c\bigr)+O(1)=o(c).
\]
But (3) and (SD) give \(\log B\ge 8c\) once \(c\ge c_*\). Increasing the fixed odd \(L\) proves the contradiction, so \(N=0\). Then \(\tau=n\) is an integer, which forces \(X\in\mathbb Z\).

For three scales, retain the v78/v88 explicit modular bounds \(h(\beta)<2^{342}M_\beta^3\) and \(h(t_i)\le 2^{551} M_i(199+\tfrac12\log M_i)^2\). The effective three-point version of v10 suffices for the original aggregate inequality: its constants are \(A_3=8,B_3=\log12\) in \(h(\mathcal Z)\ge B^2-6-A_3\log B-B_3\). Using \(8\log B\le B^2/2+4\log8-4\) and the height inequality for \(\mathcal Z=(1-\sqrt2)U_0+\sqrt2 V_0\) gives \(B^2\le2h(U_0)+2h(V_0)+82\), with room to spare. Hence the v78 nonzero-input-residual ledger applies literally:
\[
 B^2\le4\cdot2^{551}|Nc|(199+\tfrac12\log|Nc|)^2
            +30h(\beta)+4L\log67+340 .
\]
For every \(L\ge143\), (4) gives \(h(\beta)<c/120\) and \(4L\log67\le2\log c\); \(B\ge c-1\), \(c-1\ge2^{1727}\). The existing absorption and log-linear inequality give
\[
 \log B<2(h(\beta)+\log c)+574\le (31/60)c+574<c-4 .
\]
This is incompatible with (3) and (SD) for \(c\ge c_*\). No separate Lucas-residual stage is needed. This explains precisely the new effective dependence on \(c_*\) and why \(L=143\) is not unconditionally sufficient.

### Ordered completeness of the combined source

Fix integral \(X\) and \(n=X^2+1\ne0\). Fix the initial \(H_0\) in the scalar preparation, sufficiently deep at the finite support of \(\rho\) and the fixed preparation primes, and close to the identity at both real embeddings. Then choose \(c>0\) a sufficiently divisible integer with \(Q=[c]P\) still closer to the identity at all these places; put \(S=Q+P\). This is exactly the v19 scalar preparation, with its six scalar components arbitrarily small in all the required local and real neighborhoods. The Section 2 amplifier chooses \(T\) and its pole witnesses **now**, independently of the final \(H,U,\lambda\). Fix \(A=[n]P\). All root abscissas and the scales are now fixed.

In the old common-reference construction choose the reference neighborhood and compatible congruence progression, with \(U=[hn]P\), avoiding the finitely many guards, and preserve the scalar preparation by shrinking the neighborhood. Apply the retained simultaneous prime-pattern theorem to the merged contact lists \(\theta/a_i\), with the same fixed avoidance, denominator divisibility and positive-real conditions as the parent sources. In particular enlarge avoidance by the numerator and denominator support of any newly fixed coordinates, the scales and differences. The reference index is chosen **after** the primes by the old simultaneous CRT, including divisibility by every selected prime. This remains compatible: the selected prime cluster makes every selected prime coprime to every prescribed even reduction order; the old conjugate-order coprimality and fixed moduli apply without alteration. At the designated slot \(H,U\) are formal, and \(H-P,U-A\) are formal at the opposite slot. Both exact ratios equal \(n\). The six field tests therefore have the required positive valuations, and all their detector factors are units congruent to one there.

At each selected prime \(p\), the six scalar components have the v19 alternatives \(v_p(S_k)\ge0\) or \(v_p(S_k)\le-2\): in the primary slot \(H\) has depth at least two because \(h\) is divisible by \(p\) and the reduction order is prime to \(p\); in the opposite slot \(H\) reduces to \(P\). The preselected \(S-P\) has unit local coordinates and parameter at both slots. Taking the rational components of \(z(S-P)/z(H)\) preserves the strictly smaller valuation. Hence \(R_i S_k\) cannot have valuation zero at a contact of scale \(i\), and the scalar factors are congruent to one at both slots. The original proof that \(\operatorname{Tr}(W_i^{-1})\) is a unit (residue 1 or 2) now applies to the reduced product.

At each fixed preparation place use \(R_i\to1,\delta_i^{-1}\to0\) and the prepared small scalar components. The required closeness of \(W_i\) to 1 is uniform on the chosen reference neighborhood; the slope supplies the remaining smallness. The exact squareclass identity
\[
 R_i=(a_i/(v\delta_i))^{10}\prod_\theta
                      \bigl(u-(\theta/a_i)v\bigr),\qquad\lambda=u/v,
\]
shows that all unselected valuations of \(R_i\) are even. At selected primes the odd valuations of \(e_i\) are positive, at the fixed support of \(\rho\) the local preparation preserves the required parity, and all other valuations are even. At two \(e_i\) has the class-seven squareclass and sufficient depth inherited from \(\rho\); at the reals \(0<e_i<8\rho<1\) by the same closeness conditions and the v88 bound on \(\rho\). Each actual \(e_i\) is therefore prepared, so apply the BB product converse independently. The amplifier had already been completed, and the later reference and slope choices do not change any of its data. This proves all integer inputs are admitted.

## 4. Exact finite coefficient specification and census

Use five copies of the rank-four monic square-abscissa point chart from v28/v88, in the order \(A,S,T,H,U\). Use numerator-denominator pairs for every rational operation above, field norm for every nonzero field denominator, and enforce the actual selected-character guards. For each of the two or three comparison poles and the independent amplifier pole, adjoin a monic quadratic root \(Y_*^2=ND\) for its rational radicand \(N/D\), recovering \(Y=Y_*/D\) where the denominator is nonzero. The finite algebra has rank \(4^5\,2^{k+1}\) where \(k\in\{2,3\}\) counts the comparison poles. The generators, products, coefficient maps and the finite two-branch menu have been specified explicitly. Apply the selected-character determinant of the [joint finite algebra encoder](../../../undecidability/papers/joint_finite_algebra_encoder.tex) and clear the fixed coefficient denominators. Multiply the two branch polynomials. This uses one shared ordinary encoder, allows zero terminal roots and does not require all the unselected geometric characters to be admissible.

The total ordinary coordinate count, including the input, is
\[
 1+5\cdot2+1+2k+2+1=15+2k,
\]
namely **19 and 21**. In contrast, the old 25/27 presentation has nine point pairs and no independent amplifier: removing the four unnecessary pairs saves eight variables and adding one pole costs two. These counts are for unrestricted degree only. The exact coefficient recipe is finite, not an expanded polynomial; no degree majorant is claimed here.

## 5. A sufficient weak abc hypothesis for (SD)

Let \(\mathfrak B_m\) denote the denominator ideal of the local square root of the abscissa of \([m]P\): at a finite prime of \(K\), its exponent is \(\max(0,-v(x([m]P))/2)\). Normalize ideal logarithmic norm by division by \([K:\mathbb Q]=2\). Write this normalization as \(\mathcal N\); for example \(\mathcal N(\mathfrak p)=\tfrac12\log N\mathfrak p\). Set \(q_E=\widehat h(P)>0\) with \(h(x([m]P))=2q_E m^2+O(1)\).

The standard denominator asymptotic for a fixed nontorsion elliptic sequence, obtained from the archimedean Siegel approximation estimate or a lower bound for a linear form in elliptic logarithms, is
\[
 \tag{5} \mathcal N(\mathfrak B_m)=q_E m^2+o(m^2).
\]
Here the archimedean positive part of the abscissa height is \(o(m^2)\) at each of the two fixed embeddings, exactly as in the rational denominator argument of v82. One can use the fixed-point elliptic logarithm estimate of David–Hirata-Kohno cited and audited in the project's v63 effective-sums paper. This is an asymptotic, not a numerical threshold. A fixed finite set of finite places contributes \(O(1+\log |m|)\) to the denominator height: outside the fixed formal entry modulus no formal poles occur, and inside it the logarithm formula controls their growth (at bad or dyadic places first pass to a sufficiently deep subgroup). Thus fixed excluded primes can be discarded at a cost \(o(m^2)\).

Assume over \(K\) a fixed weak abc inequality
\[
 h(q)\le\kappa\,N^{(1)}(q;0,1,\infty)+C_\kappa
 \quad(q\in K\setminus\{0,1\}),
 \qquad 1<\kappa<12/11,
\]
where \(N^{(1)}\) is the normalized truncated finite-prime counting function and all valuations are normalized consistently. For the rational function \(q=x([m]P)^2/D\), its height is \(4q_E m^2+O(1)\). The degree-four map \(E\to\mathbb P^1,\ (x,y)\mapsto x^2/D\) is branched over \(0,1,\infty\). Away from the fixed bad primes and those dividing \(2D\), a finite-place contact of this map occurs precisely when the point reduces to one of the four two-torsion points \(O,(0,0),(d,0),(-d,0)\). For \(O\) its truncated weight is \(\mathcal N(\operatorname{rad}\mathfrak B_m)\). For each of the other three torsion points \(T_2\), the corresponding truncated weight is at most the denominator height of \([m]P-T_2\), which is at most \(h(x([m]P-T_2))/2=q_E m^2+O(1)\) since the canonical height is unchanged by torsion. These observations and the weak abc inequality yield
\[
 \tag{6}\mathcal N(\operatorname{rad}\mathfrak B_m)
       \ge(4/\kappa-3)q_E m^2-O(1).
\]
In particular the weighted total multiplicity surplus
\[
 H_m=\mathcal N(\mathfrak B_m)-\mathcal N(\operatorname{rad}\mathfrak B_m)
\]
is at most \(4(1-1/\kappa)q_E m^2+o(m^2)\).

Now remove all rational primes at which **some** local denominator exponent is at least two. At an inert prime of exponent \(b\ge2\), the removed full multiplicity weight is at most twice its surplus weight. At a split prime with one exponent \(b\ge2\) and the other at most one, the removed weight is at most \(3(b-1)\) times the single-place weight, since \(b+1\le3(b-1)\). If both exponents are at least two, the factor two suffices again. At the fixed ramified or bad places discard the \(o(m^2)\) term from (5). Consequently the retained multiplicity weight is at least
\[
 \mathcal N(\mathfrak B_m)-3H_m-o(m^2)
 \ge \bigl(1-12(1-1/\kappa)\bigr)q_E m^2-o(m^2).
\]
On the retained support every local exponent is zero or one, with at least one equal to one. Its normalized multiplicity contribution is at most the logarithm of its underlying rational prime; thus \(\log R(m)\) is at least the preceding expression. The coefficient is strictly positive exactly in the displayed range of \(\kappa\). For example \(\kappa=13/12\) gives \(1/13\). It follows that \(\log R(m)\ge |m|\) for every sufficiently large \(|m|\), proving (SD) under this weak abc premise. This proof is a simple-depth estimate and deliberately does not impose primitivity; the stronger primitive mass question is separate. Weak abc over the number field and ordinary/weak abc over the rationals are not silently interchanged.

## Status

The new ingredients are the unequal-power valuation detector on rational ordinate components, the simultaneous two-slot Boolean selector, and the conditional replacement of both Lucas-growth labels and all three auxiliary Lucas numerator points by one independently chosen elliptic point. The arithmetic inputs on local index comparisons, modular contact heights, tailored primes and the BB pole converse remain inherited from v19/v28/v78/v88. The additional (SD) assumption is indispensable in the proof as given; neither a derivation from the original modular premises nor a new unconditional defining-variable bound is claimed. The fixed three-scale construction is effective relative to a supplied valid threshold for (SD), not otherwise.