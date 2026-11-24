# Direct polynomial testing on elliptic indices: 52/54 variables, and 48/50 with Sun's ten-unknown source

## Statement and scope

Let Q(a,Z_1,...,Z_k) be a fixed integer polynomial, a a nonnegative integer coefficient parameter. Assume the existing square-abscissa description of 2E(Q(sqrt(2))) = Z P, the all-sign simultaneous finite prime-pattern and compatible recurrence inputs of the common-numerator transfer, the modular contact-height input specified below, and the Bhargava–Burungale prepared normalized product-pole theorem used in v88. The two-contact version also uses the aggregate trace-height theorem of v9. The three-contact version instead uses the effective index-height input h(x([n]P)) >= n^2-6 and the arbitrary-length abscissa-sum theorem of v10.

Under these inputs, there is a family of integer polynomials with a uniformly bounded (not here numerically evaluated) degree, defining the same instance set as existence of integral Z with Q(a,Z)=0, in **4k+8** rational unknowns (two-contact version), or **4k+10** rational unknowns (three-contact version). The first has a fixed ineffective amplification exponent; the second gives an algorithmically specified sufficient exponent. No ordinary abc assumption is added. No assertion is made that the imported arithmetic inputs have all been proved independently. The three-contact version uses the explicitly retained full-family modular input, not the old coefficient L=143; it is a new source rather than a coefficient compression of that source.

Using the published mixed-domain theorem and its ternary positivity substitution (transfer_general_degree.tex, Lemma 2.1), k=11 gives 52 and 54. Using Zhi-Wei Sun, *Ten unknowns for Hilbert's tenth problem over the integers*, arXiv:2609.01594 (1 September 2026), Theorem 1.1, k=10 gives 48 and 50. The ten-integer theorem is an accepted project coding source, as clarified in the [source-review record](../../docs/audits/sun_september_20261124/README.md). The alternative published-source bounds are recorded separately. Unlike an application of k separate rational integer definitions, the present proof tests Q directly on elliptic indices.

## 1. Nonzero labels and a uniform height parameter

Use the finite disjunction over s=0,...,k and put
```
Psi_s(M_0,...,M_k)=Q(M_0-1,M_1-s,...,M_k-s).
```
For every integral tuple at least one s makes every m_i=Z_i+s nonzero. Conversely every such branch gives integer Z_i=m_i-s. Set m_0=a+1, and let A_0=[a+1]P be a *computed coefficient point*, not an unknown. It is finite and nonzero. Put D=max(1,max_s deg Psi_s), C=max(1,max_s ||Psi_s||_1), where degree includes M_0 and the coefficient norm is the sum of absolute values. These fixed integers are computable from Q. With B=max(1,|m_0|,...,|m_k|), every nonzero residual has
```
1 <= |Psi_s(m)| <= C B^D.
```
The coefficient point is included in the aggregate height. This is essential: it makes the eventual amplification exponent independent of the unbounded input a. There is no use of an exponent that varies with a.

For i=1,...,k use guarded square-abscissa point charts A_i=[m_i]P and U_i=[j_i]P, with a shared H=[h]P. These charts, including their rationality conditions, are exactly those of explicit27_20261110_v19.tex. Use the same guarded affine difference formulas for H-P and U_i-A_i. In particular h is neither 0 nor +/-1, and all numerator and difference points are finite with nonzero x and y.

Write Z=sum_{i=0}^k x(A_i)=U+V sqrt(2), T=Tr(Z)=2U. Every summand is positive at both real embeddings; indeed it is a nonzero square abscissa on y^2=x^3-(3-sqrt(2))^2 x, so both conjugates exceed the corresponding positive value of 3-sqrt(2). Consequently T>=6(k+1)>1.

## 2. A fixed contact-height bound

Let Theta={0,-1/2,-1,1/2399,-32/407}, Theta0=(2+Theta) union (4+Theta). Let G(t)=product_{theta in Theta0}(t-theta), delta=t+1, u=G(t)/delta^10. Guard delta and G nonzero. At any prime outside a fixed finite S including 2,7, all coefficient primes, differences of contact positions, contact differences with -1, and the bad curve primes, the positive odd support of G(t) consists of integral t, with exactly one contact factor of positive odd valuation and delta a unit. Thus the same support occurs in u.

Use the ten-contact bound h(t)<=2^551 M(t)(199+(log M(t))/2)^2 in four_contact_scalar_20261119_v78.tex for j=0. Here M(t) is the product of the consumed positive odd primes, with the fixed exclusions of that theorem. This is a consequence of the retained full-family modular premise, not an unconditional modular-height theorem established here. Include its exclusions in S; for definiteness one may include every prime <=76176. The weaker bound h(t)<=H M_S(u)^3 follows with H=2^551*200^2*R^3, where R is the product of all primes of S (or any computable upper bound on this product). Indeed 199+(log M)/2<=200 M for M>=1, and restoring excluded primes multiplies the radical by at most R. One can instead use the older ineffective ten-contact bound with any fixed exponent E and H, replacing 3 by E in the sequel. The effective claims below use exponent 3 and the stated H.

## 3. Polynomial local logarithm precision

Fix L=3D+1. The finite logarithm
```
ell_L(z)=sum_{0<=r<=L} (-1)^r binom(2r,r) D_E^r z^(4r+1)/(4r+1),
D_E=11-6 sqrt(2)
```
has the same linear term as the formal logarithm. Its coefficients and signs follow from the integral differential in effective_elliptic_sums_20261108_v10.tex, section 2. At an odd unramified good prime, for v(z)>=1, the exact formal logarithm divided by z is a unit and the omitted term of index r>=L+1 has relative valuation at least 4r-v_p(4r+1)>=2r>=L, since 3^(2r)>4r+1. Thus ell_L(z)/log_E(z) belongs to 1+p^L O at every such place. The series converges; its logarithm is injective. Enlarge S by the coefficient denominator primes of ell_L, which are computable from L, before forming H.

Let zeta=-x/y, f=1/x. Define
```
r_i=ell_L(zeta(U_i))/ell_L(zeta(H)),
r'_i=conj(ell_L(zeta(U_i-A_i))/ell_L(zeta(H-P))).
```
Guard both reference denominators. At a given contact argument t, use tests
```
f(H), f(U_i), conj f(H-P), conj f(U_i-A_i)  (i=1,...,k);
(r_i-r'_i)/u^(L-1)                        (i=1,...,k);
Psi_s(a+1,r_1,...,r_k)/u^(L-1).
```
Divide every test by delta^2 and denote the resulting field elements by C_j. Repeated identical tests may be omitted. All divisions are guarded, but zero test values are allowed.

If all C_j have strictly positive valuation at a place over a consumed prime p (so nu=v_p(u)>0 is odd), the reciprocal tests place the points in the two formal subgroups, and the comparison/target tests have precision >=(L-1)nu+1>=L. The exact logarithm ratios, at the first and conjugate places respectively, are j_i/h and (j_i-m_i)/(h-1). This follows by multiplying P into each local formal subgroup, as in the rank-one logarithm identity of v10. The relative truncation estimate gives
```
h r_i = j_i mod p^L,  (h-1)r'_i = j_i-m_i mod p^L.
```
These congruences do not require either r_i or r'_i integral beforehand: the errors after multiplication are integer indices times errors of valuation >=L. Subtraction using the comparison yields r_i=m_i mod p^L, now in the local valuation ring. Evaluating the fixed integer polynomial and using the target test gives p^L | Psi_s(m). Rational integer divisibility follows because K is unramified at the selected odd prime. This proves the extraction even for arbitrary rational solutions with shared primes between contact arguments.

## 4. One pole per contact argument, with unconditional local calculation

For each argument t set
```
D_j=C_j^2/(1+u C_j^2),  W=product_j(1+D_j^2/u),
V0=Tr(W^(-1)),  d=7u,
e=7u*(16/(101*(1+u)*V0))^2.
q^2=(1-e)*(v^4-d^2)*(w^4-d^2).
```
Here only v,w are retained rational pole parameters; q is a finite quadratic root. All displayed denominators and e,d are guarded; zero tests and q=0 are allowed.

The pole equation excludes every negative odd valuation of e: since e=d times a nonzero rational square, d has odd valuation, each quartic factor has even valuation (the competing valuations 4v_p(v) and 2v_p(d) are distinct, also when v=0), and 1-e has odd valuation. For any odd unramified prime with nu=v_p(u) odd, v_p(D_j)=max(2v_p(C_j),-nu). If nu<0, W is congruent to 1 in every slot and V0 congruent to 2 at an odd prime; then e has positive valuation at primes outside 2,7,101. At even nu the valuation of e is even outside 7. For nu>0 at a consumed prime, every factor of W has valuation <=0 with valuation min(0,2v_p(D_j)-nu). The trace V0 has valuation at least minus the maximum slot valuation q0 of W. The pole condition and oddness of v_p(e) give
```
0 < v_p(e) <= nu+2q0
```
outside S. Therefore at a slot attaining q0 every factor's valuation is greater than -nu/2, so v_p(D_j)>nu/4>0, hence every C_j is positive in that slot. By section 3, M_S(u)^L divides the integral residual if it is nonzero. This establishes the local argument without any assumption about a rational solution's contact-prime disjointness.

## 5. Height contradiction and sufficient fixed powers

For each argument whose pole equation holds, if Psi_s(m)!=0 then M_S(u)^L<=C B^D. Hence with E=3 and L=3D+1,
```
h(t)<=H C^(3/L) B^(3D/L) <= H C B^2.
```
The following two choices of argument lists use this inequality independently for every argument.

**Two arguments:** t0=lambda, t1=lambda+T^J. The aggregate trace theorem (aggregate_trace_height_20261108_v9.tex, sum version and its application to this source) gives B^2<=A h(T)+A0 for fixed constants for k+1 nonzero labels, including m_0. Since h(T)>=1, absorb A0 into A_* = A+A0. Choose one fixed positive integer J>A_*(2HC+1). The height inequality for subtraction gives J h(T)<=2HC B^2+log 2, contradicting B^2<=A_* h(T). The existence of J suffices to fix a finite polynomial family, but no numerical J is asserted.

**Three arguments:** t0=lambda, t1=lambda+U^J, t2=lambda+V^J. Use the arbitrary-length version of Theorem 1.1 in effective_elliptic_sums_20261108_v10.tex (the positive-abscissa theorem, not a four-point specialization), with r=k+1. Under the retained individual lower bound, it yields
```
h(Z)>= B^2-6-a_r log B-b_r,
a_r=(r-1)2^(r-1), b_r=sum_{j=1}^r binom(r-1,j-1) log j.
```
Use a_r log B<=B^2/2+a_r^2/2 (from log B<=B and 2a_r B<=B^2+a_r^2), and b_r<=r*2^(r-1). Also h(Z)<=h(U)+h(V)+(3/2)log 2. Therefore
```
B^2 <= 2(h(U)+h(V)) + 16+a_r^2+2r*2^(r-1).
```
As U=T/2>=3(k+1), h(U)>=1; hence B^2<=K_r(h(U)+h(V)), for the explicit integer K_r=18+a_r^2+2r*2^(r-1). Set J=2K_r(4HC+3), a positive even integer, independently of a. The bounds on the three arguments give J h(U), J h(V)<=2HC B^2+log 2 individually, even if V=0 (height zero). Consequently J B^2<=K_r(4HC B^2+2 log 2), contradicting the displayed choice of J. All the constants in this route are explicit computations from Q and the fixed contact-height input.

In either case Psi_s(m)=0. Since the indices are integers, Z_i=m_i-s witness the required integer equation.

## 6. Completeness, in the order actually used

Fix an integral solution, choose the common shift s, and set A_i=[m_i]P. The aggregate and the translated contact lists are now fixed. Use U_i=[hm_i]P; no independence of the U_i is claimed or needed in the construction of a witness. The common reference point H can first be chosen among the multiples of 64P to avoid the finitely many poles of all the guarded functions in sections 1 and 3, including zeros of the finite-logarithm reference functions. These are finite because the functions of H are nonconstant point maps followed by nonzero rational functions, and m_i!=0. Also avoid H=O, +/-P. At both real embeddings and at any finitely many prescribed finite places, shrink neighborhoods of this initial allowed H to preserve the guards and boundedness of the raw tests. Choose a common fixed modulus M as in the common-numerator CRT lemma to preserve these finite-place neighborhoods and the real component.

Form the union of the rational positions theta-shift for every contact list. Repeated positions are merged, which is legitimate here because every contact tests exactly the same integer labels and the same polynomial. Apply the retained simultaneous prime supplier with these positions, arbitrary fixed denominator divisibility and real slope, finite avoidance including the coefficient primes, all nonzero position differences, all fixed poles (avoid a selected prime at a pole of its own argument), m_i and M. Include primes of all denominators of the fixed translations and the finite set S among the prepared places. The slope tends to infinity at these fixed places and really; all t then tend to infinity simultaneously. Thus u->1, delta^-1->0, C_j->0 uniformly on the fixed point neighborhoods, W->1 and V0->2. The fixed pole input tends to e0=112/10201, a positive rational in (0,1), in 7 Q_2^{times 2} with valuation 4. Its only denominator prime is 101 with even valuation -2, so these limiting preparations also preserve the square denominator property at every prepared finite place.

The common-reference CRT lemma provides a positive h with h divisible by the primary orders and h-1 divisible by the opposite orders at every selected prime; the additional prime-square congruence from that lemma is harmless. The coprimality and recurrence arguments apply unchanged, and the chosen H remains in the prepared neighborhoods. The point U_i=[hm_i]P is formal at the primary slot and U_i-A_i=[(h-1)m_i]P at the opposite one. All exact logarithm ratios are m_i; the truncated ones agree modulo p^L, so the residual and comparison tests divided by u^(L-1) still have positive valuation at any selected prime of a given contact list. At such a prime the one contact factor has valuation one and delta is a unit; u has valuation one. Every factor of W at the successful place is one modulo p, and every inverse factor at the other place has residue zero or one. Thus V0 is a unit and v_p(e)=1.

For a nonselected prime outside the prepared set, the prime linear factorization gives either integral t with all ten contact factors units, or nonintegral t, in which case the leading degrees of numerator and denominator agree. In the integral case v_p(u)=-10v_p(delta) is even; in the nonintegral case v_p(u)=0. If a selected prime is not assigned to a particular contact list, the same parity holds unless that list has a merged contact at the selected position, in which case it has the successful-slot preparation just proved. Any extra denominators of point tests only affect the rational square factor in e at such even valuations. The balanced local calculation also deals with negative odd valuations if any occur. This proves square reduced denominator of every actual e. At two, e is in class seven of positive even depth, and 0<e<1 really. The prepared normalized product-pole theorem in v88 therefore supplies each independent pair v,w and the finite root q. All guards hold; no further prime choices or point choices are needed.

## 7. Literal finite coefficient prescription

Use 2k+1 point blocks, each retaining two rational components of h_P and adjoining the free rank-four square-root algebra for j_P^2=h_P^4-D_E with the multiplication table in common_numerator_transfers.tex, section 7 (x=h_P^2,y=h_P j_P). The constant A_0 is computed by the rational group law. Form all rational functions of sections 1–5 by the specified operations, with each field division represented by a numerator and scalar denominator, using conjugation and norm to invert a field element. Use all explicit guard numerators and all scalar denominators. For each terminal pole, if the radicand has the pair N/D, adjoin q_new^2=ND and recover q=q_new/D at a guarded character. The rank is 4^(2k+1)*2^c for c=2 or 3, with 2(2k+1)+c generators. The polynomial is the exact guarded finite-algebra determinant of joint_finite_algebra_encoder.tex applied to these matrices and guard product, clearing rational coefficient denominators. Multiply the k+1 branch polynomials; a zero is equivalent to a zero in one of the branches. This is a finite coefficient recipe even when the full expansion is prohibitively large. It handles nonreduced specializations and guards vanishing at other characters. The number of coordinates is
```
2(2k+1) point parameters + 1 common slope + 2c pole parameters + 1 encoder
=4k+4+2c.
```
The degree is bounded uniformly in a since Q,L,J and all the operations, sizes and disjunctions are fixed; the computed A_0 is a coefficient only. No numeric degree ceiling is claimed. For the effective route every operation is computable, including the sufficient J; for the ineffective route the fixed finite integer J exists and can be hard-coded in the existence form of the undecidability reduction. The known nonrecursive r.e. set and its fixed Q then give the asserted bounded-variable undecidability witnesses. This construction has no assertion of quartic degree.

## References and replay

- [Original mixed-source transfer](../papers/transfer_general_degree.tex) and [source formula](../papers/finite_wrapper_transfer.tex).
- [Sun 2026, Theorem 1.1](https://arxiv.org/abs/2609.01594), accepted coding source for the 48/50 counts.
- [Contact-height input and effective ledger](../../papers/few_variables25/four_contact_scalar_20261119_v78.tex).
- [Effective sum theorem and local log expansion](../../papers/effective_sums/effective_elliptic_sums_20261108_v10.tex).
- [Aggregate trace theorem](../../papers/trace_heights/aggregate_trace_height_20261108_v9.tex).
- [CRT and fixed-place inputs](../papers/common_numerator_transfers.tex).
- [Prepared normalized BB product pole](../../papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex).
- [Guarded determinant](../papers/joint_finite_algebra_encoder.tex).

The accompanying verifier checks the fixed contacts and their separation from the pole, the exact valuation inequalities on finite ranges including negative and positive odd valuations, the log tail integer inequalities, the fixed e0 preparations, and all four coordinate/rank counts. The proof above, not these finite checks, supplies the quantified mathematical statements.
