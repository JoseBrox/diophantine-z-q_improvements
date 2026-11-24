# Uniform pole replacements: finite-fibre and genus-zero obstructions

The following are limitations on a proposed **standalone** replacement for the published prepared pole theorem. They neither exclude a one-free-parameter genus-one pole nor establish a lower bound on the full defining-polynomial problem. In particular, the actual contact and trace data of the elliptic detector may impose relations not present in this standalone problem.

## Setting

Let \(b\) be a rational scalar. A prepared input means
\[
0<b<1,\qquad \operatorname{den}(b)\text{ is a square},\qquad
v_2(b)\ge4,\qquad b\in7\mathbb Q_2^{\times2}.
\]
Here the denominator is positive and in lowest terms. Let \(\mathcal P\) denote this set. A proposed uniform pole consists of a finite menu of polynomial equations and inequations over \(\mathbb Q\) in \(b\) and witness coordinates. Regard each branch as a locally closed variety with a map to the \(b\)-line. We require:

* Completeness: every \(b\in\mathcal P\) is the input of a rational solution in at least one branch.
* Rational soundness: for any rational solution, \(v_p(b)\) is not negative odd at any prime outside a fixed finite set.
* Local soundness, when specified: the same exclusion holds for solutions over \(\mathbb Q_p\) for every prime outside that finite set, even with \(b\in\mathbb Q_p^\times\).

The ordinary prepared product pole satisfies the stronger local soundness property. The separation between these two forms of soundness is important for the results below.

## 1. The prepared set is not thin

**Theorem.** The set \(\mathcal P\) is not contained in a finite union of images of generically finite covers of the rational \(b\)-line of degree at least two, together with a finite subset. Here covers are taken integral, and degree is the degree of the corresponding extension of function fields. Equivalently \(\mathcal P\) is not thin.

**Proof.** For any positive multiple \(c\) of 14 use the rational map
\[
b=\frac{112t}{(1+ct)^2}.
\]
For every positive integer \(t\equiv1\pmod8\), its image is prepared. Indeed \(b<1\); the denominator is coprime to \(112t\) since it is odd, congruent to 1 modulo 7, and coprime to \(t\). The dyadic valuation is 4 and its local squareclass is 7, since \(t\equiv1\pmod8\).

As an extension of \(\mathbb Q(b)\) the degree-two parameter field \(\mathbb Q(t)\) is obtained by adjoining the square root of
\[
1-\frac{c}{28}b.
\]
This follows by solving \(b(1+ct)^2=112t\) for \(t\). The corresponding quadratic extensions are pairwise distinct, as their finite branch points \(28/c\) differ.

Let \(M_j/\mathbb Q(b)\) be the finitely many nontrivial finite function-field extensions in a proposed thin cover. If any \(M_j\otimes_{\mathbb Q(b)}\mathbb Q(t)\) has a degree-one factor over \(\mathbb Q(t)\), then \(M_j\) embeds in \(\mathbb Q(t)\). Since the latter extension has degree two, \(M_j\) must be that quadratic field. By varying \(c\) we can avoid all such exceptions. For the resulting \(c\), every factor in every base-changed cover has degree at least two over \(\mathbb Q(t)\).

Use the integral form of Hilbert's irreducibility theorem, simultaneously on the finitely many irreducible factors (one may first substitute \(t=8n+1\)). There exist positive integer specializations \(n\) at which none has a rational point. Avoid the finitely many specialization exceptions, including the preimages of the given finite subset of the \(b\)-line. The corresponding prepared \(b\) is outside the proposed thin cover. This proves the assertion. \(\square\)

Only the classical Hilbert irreducibility theorem over \(\mathbb Q\), including its integer specialization form, is used here.

## 2. No uniformly complete generically finite pole

**Corollary.** A finite menu of branches generically finite over the \(b\)-line cannot simultaneously satisfy completeness and rational soundness.

**Proof.** Discard components not dominating the \(b\)-line, whose images are finite. Decompose the remaining varieties into irreducible components. On each dominating generically finite component the function field is a finite extension of \(\mathbb Q(b)\). A degree-one component with nonempty guard locus has a rational section on a nonempty Zariski open of the line, because the generic point itself is a \(\mathbb Q(b)\)-point. Its coordinates are rational functions of \(b\); all required inequations hold identically at the generic point. Specialize this section at \(b=1/p\) for a sufficiently large prime \(p\) outside the allowed exceptions and the finitely many exceptional specialization values. This gives a rational solution with \(v_p(b)=-1\), a contradiction. Therefore every dominating component has degree at least two. Their images, together with the excluded finitely many specializations, are thin. Section 1 contradicts completeness. \(\square\)

In particular, just absorbing every pole witness into a finite algebra over the scalar, with no genuine free witness before finite-algebra encoding, cannot give a standalone prepared pole theorem of this type. This does not prohibit such absorption when the scalar is coupled to other free source coordinates.

## 3. No geometrically integral genus-zero branch with local soundness

**Theorem.** Assume local soundness. No dominating irreducible branch whose generic fibre over \(\mathbb Q(b)\) is geometrically integral and of dimension one can have geometric genus zero.

**Proof.** Put \(t=1/b\). The smooth projective model of the genus-zero function field over \(\mathbb Q(t)\) is a smooth plane conic. Diagonalize it in characteristic zero and write
\[
A(t)X^2+B(t)Y^2+C(t)Z^2=0
\]
with nonzero rational-function coefficients. Each coefficient has an expansion \(t^m(a+O(t))\) at zero, for an integer \(m\) and \(a\in\mathbb Q^\times\). For infinitely many odd primes \(p\), all three leading constants and \(-1\) are squares in \(\mathbb Q_p^\times\): take primes splitting completely in the finite multiquadratic extension generated by their square roots, and avoid denominators and zeros of the constants. Existence follows from Chebotarev (equivalently elementary quadratic reciprocity and primes in arithmetic progressions here).

Specialize \(t=p\), so that \(b=1/p\). For all sufficiently large such primes, the coefficient with expansion \(t^m(a+O(t))\) has valuation \(m\) and square unit part. Among the three valuations, two have the same parity. Their negative ratio is a square in \(\mathbb Q_p\), so the conic has a smooth \(\mathbb Q_p\)-point (take the third coordinate zero).

A conic with a local point has infinitely many local points, dense in each nonempty Zariski open. The birational equivalence between its generic function field and the original branch, including the nonzero guards, restricts to an isomorphism of nonempty opens after removing finitely many base specializations. This follows by clearing the finitely many rational-function denominators in both birational maps and their identities. Thus a local point can be chosen in the guarded open of the original branch. This gives a solution at \(v_p(b)=-1\), contrary to local soundness. \(\square\)

For a general dominating irreducible relative-dimension-one branch, the relative algebraic closure of \(\mathbb Q(b)\) in its function field is a finite extension. If its degree exceeds one, rational images of the branch are contained in a thin subset, up to finitely many exceptional base values: factor the rational map through the integral curve corresponding to that field extension, and remove the exceptional specializations where the rational map is undefined on a component. One can justify the latter assertion also by normalizing the base curve in the constant field: on the normal locus of the dominating component the integral elements extend regularly over the affine base. Singular loci of the original variety may be treated separately by finite stratification into normal locally closed pieces, decreasing dimension each time. This finite stratification makes the thin-image assertion valid on all remaining pieces. Consequently, if a menu of relative dimension at most one is complete and locally sound, at least one dominating branch on such a stratification must have geometrically integral generic fibre of genus at least one. This does not claim that every branch in the menu has that property.

## 4. A ramification test for all multisections

A stronger local obstruction, not limited to genus zero, is useful in designing new covers.

Let \(M/\mathbb Q(b)\) be the residue field of a closed point of any guarded generic fibre. Equivalently, its coordinates give a rational solution over the finite extension \(M\). Let \(C\) be the smooth projective integral curve over \(\mathbb Q\) with this function field. If the constant field is larger than \(\mathbb Q\), use its smooth curve over that constant field; the following argument is unchanged. The function \(t=1/b\) defines a map to the base line. At any closed point \(R\) above \(t=0\), let \(e=\operatorname{ord}_R(t)\).

**Necessary condition:** if the proposed pole is locally sound, every such \(e\) is even.

Indeed, the residue field \(k(R)\) is a number field. After extending constants to it, there is a rational point above \(R\) with unchanged order \(e\) (the residue extension is separable in characteristic zero). Choose a local uniformizer \(s\) at this point and write \(t=s^e h\) with \(h\) a regular unit. Spread this smooth point, its etale parameter \(s\), the unit and the finitely many rational functions defining the multisection over a localization of the ring of integers of a number field containing all their coefficients. At all but finitely many primes completely split in that number field, the residue point has an etale disk over \(\mathbb Z_p\). Hensel's lemma gives points in this disk with \(v_p(s)=1\); there are infinitely many, since \(s\) is a local coordinate. At each, \(h\) remains a unit and \(v_p(b)=-e\). Choose a point avoiding the finite sets of zeros and poles of all denominators and guards, as the multisection satisfies those guards at its generic point. The resulting \(\mathbb Q_p\)-solution contradicts local soundness whenever \(e\) is odd.

This provides an elementary necessary boundary condition at infinity for any candidate finite cover or curve family. It does not prove global solubility when the ramification is even.

## Status and scope

The result rules out finite-fibre and purely genus-zero generic replacements in the uniform prepared-input setting, without using the \(abc\) conjecture or any assumption about elliptic ranks. It leaves the actual one-parameter genus-one problem open. In particular it does not rule out the sound genus-one cover in the [v82 criterion](genus_one_sound_criterion_20261120_v82.tex), where the unresolved condition is existence of global rational points on actual source fibres. It also does not rule out a pole coupled to a different height/contact construction, or a soundness proof that uses global arithmetic instead of the all-prime local exclusion. No new rational defining-variable count is claimed.
