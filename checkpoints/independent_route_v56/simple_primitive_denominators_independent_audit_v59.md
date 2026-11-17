# Independent audit: simple primitive denominator primes

Date: 17 November 2026. Updated for the strengthened duplication proof.

Audited manuscript:
`checkpoints/general_scalar_v56/simple_primitive_denominators_v59.tex`.

**Result: PASS.** The preferred theorem is proved under weak rational abc with
exponent 4/3 for a fixed congruent-number curve over Q and a fixed nontorsion
point in 4E(Q). It does not supply a defining polynomial by itself. The direct
16/15 argument for a point in 2E(Q), audited below, is also valid.

## Preferred duplication refinement

Write P=2Q with Q in 2E(Q). For nQ use A,B,C as in the direct audit below.
Direct abc gives `log rad(ABC)>=(4/kappa)h(A:B)-O(1)`. The duplication
identity is

`sqrt(x(nP))=(A^4+d^2 B^4)/(2|ABC|)`.

Outside the fixed primes dividing 2d, A,B,C are pairwise coprime and the
displayed numerator is coprime to ABC. Hence the denominator exponent of
sqrt(x(nP)) is exactly v_p(ABC). Since `log|ABC|<=4h(A:B)`, its simple
support has logarithm at least `(8/kappa-4)h(A:B)-O(1)`.
Canonical height changes by four under doubling, so in terms of the height
of the square abscissa at nP this coefficient is `2/kappa-1`.
At kappa=4/3 the coefficient is 1/2, and the same old-support subtraction
below leaves the exact positive gap 311/44100. Thus the stronger theorem
and its divisibility corollary pass independently. The old-support bound
also permits every `1<kappa<88200/65839`.

The manuscript was checked for denominator cancellation outside 2d,
the fourfold canonical-height conversion, and the fixed-set cost. No
additional arithmetic assumption is used in the refinement.

## Decisive checks

1. If `x(nP)=(A/B)^2` with coprime positive A,B, the ordinate is
   `AC/B^3`, with integral C satisfying `C^2=A^4-d^2 B^4`.
   The square-abscissa assertion follows from the exact duplication formula.
   Since d is a positive integer, A>B and `h(A:B)=log A`.

2. The common divisor of the three terms in the quartic abc identity is
   `gcd(A^4,d^2 B^4)=gcd(A^4,d^2)<=d^2`, independently of n.
   Dividing by this common divisor really does give a primitive positive abc
   triple. Its radical is at most `d A^3 rad(B)` because `|C|<A^2`.

3. Consequently `log rad(B)>=(4/kappa-3)h-O(1)`. Prime by prime,
   the product of simple prime factors is at least `rad(B)^2/B`, so its
   logarithm is at least `(8/kappa-7)h-O(1)`. At kappa=16/15 this coefficient
   is exactly 1/2. Deleting any fixed finite set costs only a constant.

4. Outside bad reduction, the rank of apparition of p is exactly the order
   of P modulo p. Every nonprimitive p dividing B_n therefore divides some
   B_(n/ell), with ell a prime divisor of n. This support argument requires
   no valuation lifting formula and has no issue when p divides n.

5. Canonical height gives `h(A_n:B_n)=n^2 hhat(P)+O(1)` uniformly in n.
   Thus the nonprimitive support has logarithm at most
   `n^2 hhat(P) sum_(ell|n) ell^(-2)+O(omega(n))`.

6. The exact elementary upper bound is
   `1/4+1/9+1/25+1/49+1/14=21739/44100<1/2`.
   The positive gap is `311/44100`. This contradicts the simple-support
   lower bound for all sufficiently large n, since `omega(n)<=log_2(n)`.

7. A simple primitive prime for B_|h| has reduction order exactly |h|.
   Therefore inclusion of the odd denominator support of B_|h| in that of
   B_|j| forces h|j, including negative nonzero indices. The converse is the
   elementary reduction-order divisibility property.

## Literature and scope

I independently opened the primary Cornelissen--Zahidi paper:
https://arxiv.org/html/math/0412473v3 .
Its elliptic Zsigmondy proposition gives odd primitivity for j=0 or 1728
under abc and cites Silverman, *Wieferich's criterion and the abc-conjecture*,
Lemma 13. Its following discussion explicitly distinguishes denominator
support inclusion from a Diophantine formula for that inclusion. The current
manuscript correctly attributes this background and proves the stronger
valuation-one assertion with an explicit weak exponent directly.

The proof is over Q. It does not infer abc over a quadratic number field,
does not encode the support predicate, and does not identify an external
rational input with j/h. No variable-count improvement follows yet.
