# Number-field checkpoint — 9 November 2026

Status: elementary reductions below are proved; no counterexample to the field-dependent statement has been established. The assertion Z Diophantine in Q is treated as a separate hypothesis, matching the bundle arithmetic scope.

## Primary sources independently read

- Bjorn Poonen, Rank stability makes rings of integers diophantine, dated July 3, 2026, https://math.mit.edu/~poonen/papers/h10_over_OK.pdf. Introduction, especially section 1.2, explicitly explains the theorem Z Diophantine in O_F for every number field F. Sections 4 and 5 give the rank-stability transfer and Shlapentokh reduction. This is NOT a theorem defining O_F in F.
- Levent Alpöge, Manjul Bhargava, Wei Ho, Ari Shnidman, Rank stability in quadratic extensions and Hilbert’s tenth problem for the ring of integers of a number field, Invent. Math. 243 (2026), 1129–1139, doi:10.1007/s00222-025-01392-3. Publisher full text states the rank-stability theorem for every quadratic extension. Published online December 1, 2025.

## Theorem A: equivalence of three definability questions

For a number field K the following are equivalent: (a) O_K is Diophantine in K; (b) Z is Diophantine in K. If Z is Diophantine in Q, these are also equivalent to (c) Q is Diophantine in K.

Proof (a)=> (b): the proved Denef–Lipshitz theorem supplies a polynomial existential definition of Z with every variable in O_K. Replace each condition that a variable belongs to O_K by the assumed existential definition inside K. Quantifier composition is existential and exactly preserves the witness domain.
Proof (b)=> (a): choose a Z-basis omega_1,...,omega_n of O_K. Then x is integral iff x=sum omega_i z_i with z_i in Z. This is an existential formula inside K.
Proof (b)=> (c): q is rational iff q=a/b with integers a,b and b nonzero; express nonvanishing by bc=1.
Proof (c)=> (b), assuming Z Diophantine in Q: take the Q-definition and restrict BOTH its input and all witnesses to Q using the assumed Q-membership definition. Merely extending coefficients does not restrict the witness field.

## Theorem B: exact coordinate bounds

If F(t,y_1,...,y_m)=0 defines Z inside K, put N=m+1 and D=deg F. The integral-basis construction defines O_K with n*N TOTAL coordinates, where n=[K:Q], not n*N+1. Retain z_1,...,z_{n-1} and eliminate z_n=(x-sum_{i<n}omega_i z_i)/omega_n. Use n disjoint copies of the m witnesses. This gives n residuals of degree at most D. They combine to one polynomial without new coordinates of degree at most ceil(sqrt(n))*D using the anisotropic norm form proved in the bundle, or at most 2D if K has a real embedding. For n=1 use the original polynomial.

If Q is defined in K by one polynomial with R total coordinates and degree E, and Z in Q by one with N total coordinates and degree D, restricting all N rational variables yields Z in K with N*R total coordinates, N+1 equations, degree at most max(D,E). Combining equations gives degree at most ceil(sqrt(N+1))*max(D,E), or 2*max(D,E) over formally real K.

## Theorem C: descent and the structure of a possible counterexample

Let L/K be finite of degree d. If O_L is defined in L by a polynomial of N total coordinates and degree D, then O_K is defined in K by a system with 1+d*(N-1) total coordinates, d equations, and degree at most D. Expand each witness in a fixed K-basis of L and equate the d coordinate components of the equation. The input x already lies in K, and O_L intersect K=O_K. The system combines without new coordinates with degree at most ceil(sqrt(d))*D, or 2D if K is formally real.

Consequently a genuine counterexample K forces every finite extension L/K to be a counterexample. Its normal closure enlarged to contain i would be a totally imaginary Galois counterexample. This is a logical reduction, not an actual counterexample.

## Forthcoming strengthening of the fixed-formula obstruction

A finite list of existential formulas over k, each with infinite k-input projection, all admit a common noninteger q in one finite Galois extension. Apply the bundle bounded-extension theorem separately, avoid the union of the finite exceptional sets, then take the compositum and normal closure. If the generic witness degrees are D_i, extension degree is at most product(D_i!). One can further adjoin i, at most doubling that bound. Therefore even a fixed finite menu of formulas cannot define rings of integers across all finite extensions. This does not obstruct a separately chosen new formula for each field.

## Theorem D: relative norm image criterion, all characteristic-zero finite extensions

For L/K finite of degree n in characteristic zero, the following are equivalent: K Diophantine in L; N_{L/K}(L) Diophantine as a subset of L; norm graph Diophantine in L; trace graph Diophantine in L.

Key identity: sum_{j=0}^{n-1} (-1)^(n-1-j) binom(n-1,j)(T+j)^n = n! T+n!(n-1)/2. The norm image is contained in K and contains all nth powers of K. The signed binomial sum of n independent norm-image elements therefore equals K exactly. If the norm-image definition has M total coordinates, its linear image needs nM total coordinates, n residuals and unchanged degree, by eliminating the last summand. The trace graph projects onto K. Conversely a definition of K lets us restrict every coefficient in a fixed K-basis of L and use the multiplication determinant and trace polynomials.

For quadratic L/K, the conjugation graph is equivalent too. Both norm and trace graphs for any proper L/K are Zariski dense in A^2_L (restrict to a+b theta and use the Jacobian Tr(theta)-n theta !=0). Thus they cannot be defined without quantifiers by polynomial equalities and inequalities in their two coordinates. This identifies the flaw in writing a formal trace or norm as an ordinary one-variable polynomial over L.

Full standalone paper now exists at work/number_fields/number_field_definability_20261109_v12.tex. Initial PDF build found pdflatex installed but its pdflatex.fmt missing; no successful PDF claimed yet.
