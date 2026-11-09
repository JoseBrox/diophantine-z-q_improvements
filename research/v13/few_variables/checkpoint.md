# Few-variable structural research: V13 checkpoint

## Scope

The published V12 baseline remains unchanged: 27 total variables in an ineffective family (degree below 2^151), and 29 with specified coefficients (degree below 2^157). Counts include the input, and all inherited arithmetic hypotheses remain explicit. No V13 variable-count improvement has been proved. No publication file or compiler specification was changed.

All files named below are in `work/v13/few_variables/`.

## Proved uniform scalar normalization

Full proof: `uniform_scalar_normalization_20261109_v13.tex` and matching PDF. Verifier: `check_uniform_scalar_normalization.py`. Exact output: `uniform-scalar-normalization-certificate.json`. Both parent and number-fields agent independently audited the decisive valuation and real estimates.

Write rho(X)=r(216X^4+450459), where r(T)=T(T-1)(T-2401)(32T+343)(2T-1). Set ell=76249, q=1021, and

    h0(X)=2239488 X^10+11663498286 X^6
          +(9330368884708461/512) X^2.

The remainder F=rho-6h0^2 has degree eight with positive coefficients. If N is their sum, choose the least integer T>=max(ceil(N)+1,2239488) congruent to 2 modulo ell. It is

    T=1181553994055396276117553880104.

Set h=h0+T, H=512h, delta=rho-6h^2. Define integral polynomials rho_tilde,H_tilde by rho(X)=rho_tilde(X^2) and H(X)=H_tilde(X^2), and put J=Res_Y(rho_tilde,H_tilde).

**Final notation:** J is the smaller Y-resultant, of 1313 bits. The X-resultant is J^2 and has 2626 bits. The multiplier below is J^2, not J^4. The checker verifies the 15 by 15 Sylvester determinant, five quadratic-factor formulas, and the square relation to the 30 by 30 determinant independently.

The polynomial delta is negative on the real line, and rho/delta^2 has fixed positive upper and lower bounds. Exhaustive exact checks show rho has no root modulo ell or q, and delta has no root modulo ell. Its degree-ten leading coefficient is an ell-unit.

The essential denominator argument: for an integer input and p!=2,3, let u=v_p(rho) be odd, v=v_p(h), and j=v_p(J). The resultant identity gives min(u,v)<=j; differing parity gives v_p(delta)=min(u,2v). A three-case check proves

    2j+u-2min(u,2v)>0.

Thus J^2 rho/delta^2 has positive valuation wherever v_p(rho) is odd. At 2,3,17, rho is locally square and 6 locally nonsquare, giving v_p(delta)<=v_p(rho)<=2. The factor 102^6 supplies the required depths.

For odd L>=3, define

    R_L(X)=102^6 J^2 ell^L rho(X)/(q^(2k(L)) delta(X)^2),

with k(L) minimally making the fixed real upper bound less than 1. This gives a fixed positive lower bound independent of L. For every integer input, R_L has square reduced denominator and the required local squareclasses and depths. For every rational input,

    v_ell(R_L)=L+2v_ell(J),

which is positive and odd. All exceptional prime sets, height constants, and test-scaling constants are independent of L. The exact checker gives k(3)=139, k(5)=141, and k(101)=219.

Replace z=-x/y by w=y/(x^2+D). Then w/z=-(1-D f^2)/(1+D f^2), a unit at good formal points. Both f and w have absolute value below 1 on nonzero real doubles. Choose the auxiliary point H in a fixed real neighborhood where both embeddings of w(H) are bounded away from zero. The six components of f(H), f(S-P), w(S-P)/w(H) are uniformly bounded independently of S. Dividing them by one sufficiently large fixed integer K, coprime to ell, makes all normalized leaves at most 1/4 in absolute value. The original norm tree then obeys

    1 <= W <= 86249/65536 < 3/2,
    0 < R_L W^2 < 9/4 < 17.

This removes the **real approximation restriction on S-P**. The finite preparation at 2,3,17 is explicitly retained: the point depths must absorb K and the powers of R_L. Other positive odd valuation primes are prepared as before. The scalar index depth is still at least 19L+1.

The scalar normalizer has numerator and denominator degree twenty. This is a source-level degree improvement, not a new compiled defining-polynomial degree certificate, and not a variable reduction.

The initially attempted denominator 1+C(1+X^2)^5 is not used: common numerator-denominator primes can introduce negative odd valuations, and an L-dependent C can spoil independence of the exceptional set.

## Proved structural constraints

Full note: `structural_constraints_20261109_v13.tex` and matching PDF.

1. Generic finite algebraic recovery of arbitrary r-tuples from the cyclic subgroup of the simple Weil restriction needs at least 2r retained rational coordinates. This does not constrain a specially selected arithmetic witness subset.
2. The graph {(n,[n]P): n in Z} is Zariski dense in the product of the additive group and the abelian variety whenever P generates a dense cyclic subgroup. Thus finite algebraic recovery cannot uniformly reveal all integer indices. The same holds on each nonconstant arithmetic progression.
3. A rational elliptic curve and rational P cannot support the current paired-place condition at unbounded contact primes: H=[h]P formal at one conjugate place and H-P formal at the other force P to reduce to the identity, possible at only finitely many good primes.
4. If the common-index pairs on two rational elliptic curves lie on an algebraic curve, the curves have an isogeny relation between their fixed points. Their reduction orders are then commensurable up to a fixed factor, so can be coprime at only finitely many good primes. This limits the strategy of enforcing a shared index through a curve correspondence.
5. Sharing a nondegenerate pole parameter e forces a common squareclass. The values e=1,-1/3 are separate degenerate cases. Sharing the chart parameter tau is different and not excluded by this argument; its simultaneous completeness is not supplied by the inherited realization theorem.

## Exact parity counterexample

`search_reduction_parities.py` and `reduction-parity-certificate.json` give order 3 at both conjugate reductions over p=23 and order 25 at both over p=113. Explicit point coordinates and proper-divisor multiple witnesses are recorded. Among 209 split good primes below 3000, 72 have odd orders at both places. This refutes the shortcut that odd labels single out one formal embedding; it does not refute the aggregate height theorem.

## Unresolved variable-reduction step

The proposed prescribed scalar index c=a-1=M rho(X)^e still needs to be divisible by the reduction order of P at every varying contact prime. Divisibility by a large power of the residue characteristic does not imply formal-group membership. The uniform scalar normalization solves the real approximation problem but does not provide these varying reduction-order factors.

The monic Lucas equation makes rational t integral if a,b are available integers. In this source they are hidden point indices, so this observation does not yet remove the t point witness.

## Literature and next effective-height strategy

The structural note records H. Pasten, Bivariate polynomial injections and elliptic curves, arXiv:1811.02416, and B. Poonen, Multivariable polynomial injections on rational numbers, Acta Arith. 145 (2010), 123–127. Rational-point injectivity does not imply finite geometric fibers, so neither result alone supplies finite-algebra witness compression. Poonen's stated existence result also assumes a nondensity hypothesis, which has not been imported.

An open secondary strategy uses the CM rescaling to y^2=x^3-x: for a single label, quadratic leading cancellation of the conjugate formal logarithms factors into linear combinations with coefficients +/-i, hence logarithms of fixed sums of points on the CM curve. Local-height addition identities might exploit this. No effective global one-scalar estimate has been proved, and four independent labels create an additional difficulty.

Both final TeX files compile without overfull boxes, undefined references, or LaTeX warnings. All exact certificates pass.
