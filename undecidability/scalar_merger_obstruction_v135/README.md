# A local obstruction to fixed rational-function scalar-pole mergers (v135)

The twelve scalar poles of v131–v134 have simultaneous witness preparation already (v104), but distinct native arguments. The following strengthens the fixed-product parity obstruction: **fewer than twelve arbitrary fixed rational functions of the scalar input tuple cannot replace the twelve local tests by their native pole equations alone**. The statement is about the scalar subinterface with independently variable input coordinates, not an impossibility theorem for all encodings or for the full Jones source.

## Proposition

Fix the nonzero common physical scalar data \(H,A_a\) of v131, with \(f=1/x(H)\ne0,\ Z=2z(A_a)/z(H)\ne0\), and \(C=149^N\) for any fixed positive integer \(N\). Let there be \(n\) independent rational inputs \(X_1,\ldots,X_n\), and write

\[
 P(X)=r(51X^2+2504),\qquad r(\beta)=\beta(\beta-1)(\beta-2401)(32\beta+343).
\]
The old physical scalar data are
\[
 R_i=\frac{149 C^2 P(X_i)}{1+149^2P(X_i)},\quad
 J_i=R_i^{-5}(Z^2+R_if^2),\quad
 \tau_i=\frac{\operatorname{Nm}J_i}{\operatorname{Tr}(Z^2/R_i^5)},\quad
 d_i=\frac79R_i(R_i+9792)\tau_i^2 .
\]

Suppose a proposed merger uses \(m<n\) rational functions \(D_j(X_1,\ldots,X_n)\) as native pole arguments. Coefficients may depend on the fixed common data and on \(C\); we assume the specialized functions are defined on a nonempty Zariski-open subset. This includes any rational-function composition of the old scalar quantities and the inputs, with the common data fixed. Zero functions can be omitted from the argument below, as the native equations at zero are soluble. Then outside any prescribed finite set there exist a prime \(p\) and integer inputs \(X_i\) at which every \(D_j\) is defined and the merged native equations are simultaneously soluble over \(\mathbb Q_p\), whereas at least one original native scalar equation is insoluble over \(\mathbb Q_p\).

### Proof

1. The degree-eight polynomial \(P\) is squarefree over \(\mathbb Q\): its four factors in \(X^2\) have distinct roots in \(X^2\), all nonzero. Choose any algebraic root \(\alpha\). Expand every nonzero numerator and denominator of the \(D_j\) as a polynomial in \(Y_i=X_i-\alpha\), over \(\mathbb Q(\alpha)\). Each such polynomial has nonempty finite support. There is a positive integral weight vector \(v\in\mathbb Z_{>0}^n\) outside the finitely many hyperplanes on which two distinct monomials of any of these polynomials have equal weight. Thus every polynomial has a unique least-weight monomial.

2. Let \(e_j\in\mathbb Z^n\) be the exponent vector of the leading numerator monomial minus that of the leading denominator monomial for \(D_j\). Since \(m<n\), the matrix with rows \(e_j\) has a nonzero kernel vector \(\epsilon\) over \(\mathbb F_2\), with representatives in \(\{0,1\}^n\). Set \(\mu_i=2T v_i+\epsilon_i\) for a sufficiently large positive integer \(T\). All \(\mu_i\) are positive, and every unique least-weight monomial remains the same. Moreover \(e_j\cdot\mu\) is even for all \(j\), while some \(\mu_i\) is odd.

3. Choose a number field containing \(\alpha,\sqrt2\) and square roots of every nonzero coefficient in the finite expansions in step 1. Infinitely many rational primes admit an embedding of this field into \(\mathbb Q_p\). Indeed choose an integral primitive element; Schur's elementary theorem gives infinitely many prime divisors of values of its nonconstant minimal polynomial, and outside the discriminant these give a simple root and hence a root in \(\mathbb Q_p\) by Hensel. (Schur follows by evaluating a nonconstant integer polynomial \(F\) at \(a+kF(a)M\) for \(F(a)\ne0\): the resulting integer quotient by \(F(a)\) is \(1\bmod M\), nonconstant, and has arbitrarily large absolute values. Take \(M\) divisible by all proposed prime divisors.) Exclude finitely many primes so that all nonzero coefficients and their square roots are units, \(\alpha\) is integral, \(P'(\alpha)\) is a unit, all fixed nonzero scalar data and their relevant traces/norms are units, \(p\) is odd and does not divide \(7\cdot149\cdot9792\) or any fixed exceptional constants. The \(\sqrt2\) embedding ensures two unramified split slots; exclude the bad primes for both conjugates of \(Z,f\).

4. Choose integer \(X_i\) so that \(X_i-\alpha\equiv p^{\mu_i}\bmod p^{\mu_i+1}\) in \(\mathbb Q_p\). This is possible by reduction of \(\alpha\in\mathbb Z_p\) modulo the indicated powers; they can even be chosen positive and arbitrarily large. Taylor expansion at the simple root gives \(v_p(P(X_i))=\mu_i\). Every polynomial in step 1 has the valuation of its unique least-weight monomial, and its leading unit residue is the corresponding coefficient residue. It follows that
\[
 v_p(D_j)=e_j\cdot\mu\in2\mathbb Z
\]
and the leading unit is a quotient of squares. In particular every nonzero \(D_j\) is a square in \(\mathbb Q_p\) by Hensel. Its numerator and denominator are both nonzero.

5. In the old physical scalar data \(v_p(R_i)=\mu_i>0\), \(v_p(R_i+9792)=0\). In both slots \(Z^2+R_if^2\) is a unit and \(v_p(\operatorname{Tr}(Z^2))=0\). Thus \(\tau_i\) has valuation \(-5\mu_i\), so \(v_p(d_i)=-9\mu_i\). At the index with odd \(\mu_i\) this is negative odd. The native pole obstruction of v104 forbids a \(\mathbb Q_p\) solution. On the other hand, for every nonzero merged square \(D_j\) the native equations
\[
 e^2+D_j p_0^2=1,\quad uv=e(1-D_j),\quad u^2-v^2=D_j q_0^2
\]
have the explicit local solution \(e=u=v=q_0=0,\ p_0=1/\sqrt{D_j}\); for \(D_j=0\) take \(e=u=v=1,\ p_0=q_0=0\). Square helper coordinates are filled by actual squares. This proves simultaneous local solubility and the failure of the old separate local test. QED.

For the old input tuples we may for instance fix \(H=A_a=R_0\), so \(H-P_0=-R_0,\ f=\sqrt2-1,\ Z=2\), all finite points with the required scalar nonvanishing. A finite pair representing the scalar difference is \(2R_0,R_0\). More generally the proof works at any fixed allowed nonzero common physical data at which the proposed functions specialize generically, including an allowed fixed reference of even index if desired.

## Consequences and limits

* This rules out **all fixed rational-function mergers of fewer than n scalar arguments as pointwise local replacements of the old n native pole tests on the independent scalar subinterface**, even if the proposed proof uses local solubility rather than merely negative-odd-valuation exclusion. In particular, products, inverse products, square rescalings, rational sums and fixed rational-function selectors cannot achieve that replacement. For monomial products the mod-two rank argument is the immediate special case.
* The construction is not a rational solution of the full source and does not imply global rational solubility of the merged equations. A successful new global proof could exploit correlations of the source, comparison constraints or additional existential parameters/guards, or change the height argument so the original local tests are no longer necessary. None of these possibilities is ruled out.
* Simultaneous preparation of all physical scalar inputs with shared elliptic data remains the positive theorem of v104. It does not imply simultaneous sharing of the private pole witnesses. We retain the twelve private poles in the best tables. The proof imposes no new arithmetic premise on v134.

## Small exact fixture

At \(p=43\), \(P(3)\equiv1677=39\cdot43\bmod43^2\), so at \(X=3\) the physical pole has valuation \(-9\) for the fixed \(Z=2,f=\sqrt2-1\). For every integer \(N\ge1\), at least one of \(X=0,1\) has \(R(R+9792)\) a unit at 43. The fixture uses the multiplicative periodicity modulo 43; the verifier checks all 42 possible exponent residues. Thus any chosen subset of inputs can have old pole valuation \(-9\) at this prime while the remaining poles have even valuations. This checks the parity mechanism, not the entire general rational-function proof, which is theoretical.
