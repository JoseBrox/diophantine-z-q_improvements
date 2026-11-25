# Deterministic input--target anchors cannot replace the derivative prime supplier

25 November 2026. Project-specific obstruction to eliminating the independent
slope from the eleven-coordinate [derivative detector](../../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex)
and its [full-auxiliary](../../../papers/conditional_few_variables/full_auxiliary11_20261117_v71.tex)
and [even-valuation](../../../papers/conditional_few_variables/even_valuation_detector_20261117_v75.tex)
versions. This does not concern Szpiro or require ordinary abc for the
obstruction itself. No new defining-variable record is claimed.

## 1. Scope and theorem

Use the existing carrier

    K=Q(sqrt(2)), d=3-sqrt(2), E:y²=x³-d²x,
    P=((57-28sqrt(2))/8,(-660+417sqrt(2))/32).

Retain the subgroup input 2E(K)=Z P. Put
R=(1+sqrt(2),2sqrt(2)), so 2R=P, and use target A_n=[n]P.
The target point chart, including its two possible square-root abscissae,
can be written using Q_n=[n]R:
g_A=±(x(Q_n)^2+d²)/(2y(Q_n)), y(A_n)=y([2]Q_n).
Thus even dependence on a selected target square-root sign is covered
by a finite menu of rational functions of Q_n. Write
B=Res_{K/Q} E, viewing Q_n as a Q-point of B.

Consider replacing the free slope and its scalar construction by any
finite menu of fixed nonzero rational functions

    u_i(X,Q) in Q(B)(X),

evaluated on the target chart (with ordinary rational-function
nonvanishing guards). The index extraction tests C_1,...,C_6,
the balanced denominator detector, and the prepared product pole
are otherwise retained. The relevant detector is

    D_l=C_l²/(1+u C_l²), W=product_l(1+D_l²/u),
    V=Tr(W^(-1)), e=28 u/((1+u)² V²),

or the even-valuation modification of the first four D_l. The
normalization by a nonzero rational square in the BB product pole
does not change this argument. The nonzero fixed scalar 28 corresponds
to the class-seven BB realization of the derivative detector.

In particular, a positive odd valuation of u at an odd good prime
outside the fixed scaling primes forces some slot in which both H
and the conjugate of H-P are formal. The other property we use is
that every negative odd valuation of u outside the same finite set
gives V ≡ 2 (mod p). These follow from the v63/v75 balanced valuation
identity. We allow the full auxiliary group E(K), not only 2E(K).

A **prepared** completeness witness uses the actual BB input e with
square reduced denominator, 0<e<1, even v_2(e)≥4 and squareclass 7
in Q_2. The fixed-place and real preparation in the cited detector
is of precisely this form after the class-seven pole replacement.

**Theorem.** A finite menu of deterministic rational anchors of the
displayed kind cannot be both sound and prepared-complete with target
A_n=[n]P for all nonzero integer inputs X=n (even up to finitely many
exceptions). More precisely:

* A generic finite odd-multiplicity zero in X of an anchor forces
  failure of that anchor on an infinite arithmetic progression of
  canonical true inputs. All such anchors in a fixed finite menu
  can be made to fail on the same progression.
* An anchor whose generic finite zeros in X all have even
  multiplicity admits noninteger solutions arbitrarily near any
  prepared integer witness at which its generic factorization
  specializes regularly, if the remaining equations are just the
  stated point charts, rational definitions, nonzero guards and
  BB pole equation.

The theorem does not rule out new exact equations relating X to the
other witnesses, genuinely coupled anchors depending on the free
auxiliary points, nonrational algebraic covers of the anchor base,
a different local extractor, or completeness using a different
target label without retaining exact index extraction. Nor does it
claim that all possible eleven-variable constructions have this
obstruction. Its positive-odd-prime part applies to any variant
retaining the simultaneous shifted formalness implication; its
negative-odd-prime part uses the particular balanced detector.

## 2. Incompatible primes with prescribed splitting fields

At a rational prime p split in K of good reduction, denote by
r_+(p),r_-(p) the orders of the two reductions of P. If an odd prime
ell divides both, the simultaneous shifted formalness requirement
cannot hold in either orientation, for any H in E(K). Indeed write
2H=[h]P, h in Z. Formalness of H at the first slot gives
r_+|h; formalness of H-P at the other gives r_-|(h-2).
These contradict ell|h and ell|(h-2). This also covers the smaller
double subgroup, and no choice of numerator U can repair the failure.

We need such primes even after specifying a finite splitting field.
For that purpose use Antonella Perucca, *Prescribing valuations of the
order of a point in the reductions of abelian varieties and tori*,
J. Number Theory 129 (2009), 469--476, [arXiv:0712.2812v4](https://arxiv.org/abs/0712.2812v4),
Proposition 4.2. It prescribes, with positive Dirichlet density,
arbitrary finite sets of rational-prime valuations of reduction
orders of an independent tuple of points in a product of abelian
varieties. The independence hypothesis means that the cyclic
subgroup of the tuple is Zariski dense in the product.

Here (R,R^sigma) is independent on E x E^sigma. To check this,
d d^sigma=7 and the two elliptic curves become isomorphic via
(x,y) -> (lambda² x,lambda³ y), lambda=d/sqrt(7).
Let R' be the image of R^sigma on E. The involution of
K(i,sqrt(7))/K(i) sends R' to -R' and fixes R and all geometric
endomorphisms (End(E)=Z[i]). If alpha R+beta R' were torsion
for Gaussian integers alpha,beta, subtracting its image under
the involution shows that 2 beta R' is torsion. Since R' is
nontorsion, beta=0 and then alpha=0. A proper identity component
of the cyclic closure in E² would be killed by a nonzero
homomorphism E² -> E (Poincare reducibility); hence it would
give just such a relation up to torsion. This proves the asserted
independence, and also the density of every nonconstant arithmetic
progression of the Q_n on B.

Let F be any fixed finite Galois number field containing K, and
let T be any finite set of rational primes distinct from an odd
prime ell. Apply Perucca's Proposition 4.2 over F to the
independent tuple (R,R^sigma), prescribing ell-adic order
valuation 1 in both slots, and valuation 0 at every prime in T
in both slots. The positive Dirichlet density set of prime
ideals of F contains infinitely many residue-degree-one primes:
the sum of norm^{-s} over prime ideals of degree at least two
is bounded as s tends to 1 from above. Because F is Galois,
outside ramified primes their underlying rational primes split
completely in F. The orders of reductions of R in the two K-slots
at each such p are therefore both divisible by ell and prime to
the primes in T. The same ell divisibility holds for P=2R.

Also, p itself is prime to these orders for p>7: both reduced
curves have full rational 2-torsion, their orders are divisible
by four, and Hasse puts the orders strictly between 0 and 2p.
The only possible positive multiple of p in that interval is p,
which is odd. All these conclusions remain valid after removing
any finite set of primes.

This argument does not need conjectural prime distributions,
and can require p to split in an arbitrary fixed number field.
In particular it applies even if finite odd zeros of the proposed
scalar are chosen from irreducible polynomials intended to
force splitting in auxiliary fields.

## 3. Odd-zero anchors: force a forbidden contact

Factor the finite menu over the rational function field of B:

    u_i(X,Q)=c_i(Q) product_j F_ij(X,Q)^(e_ij),

where the F_ij are distinct monic irreducible polynomials of
positive degree in X and e_ij are nonzero integers of either sign.
Choose a common nonempty open of B where every coefficient is
regular, every c_i is a unit, and the F_ij specialize to squarefree
polynomials of the same degree, pairwise coprime within each anchor.
Such an open exists by the discriminant and resultant identities
in characteristic zero. Include all ordinary chart requirements.

Call an anchor active if one of its e_ij is positive odd.
Choose a single nonzero integer a with Q_a in the common open,
using density from Section 2. For each active anchor choose
one positive odd e_ij and an algebraic root of the specialization
F_ij(X,Q_a). Put all the finite splitting fields needed for
that choice into a Galois extension of Q containing K. Exclude
primes of bad reduction, denominators of the coefficients and
chart, zero reductions of c_i, and vanishing reductions of the
specialized discriminants and resultants.

By Section 2 we can choose a prime p_i split completely in
that field with both reduction orders of R divisible by an
odd prime ell, and with a simple root alpha_i in F_{p_i} of
F_ij(X,Q_a). For several active anchors, choose their primes
sequentially. At each new step use T consisting of the earlier
chosen p_i and choose the new prime larger than all earlier
reduction orders. Thus no chosen rational prime divides either
reduction order of R at any chosen prime, including itself.

Let L be the lcm of all the two-slot reduction orders of R
at these primes. In particular gcd(L,product_i p_i)=1. For
n≡a (mod L) the target Q_n reduces to Q_a at every p_i.
Impose in addition n≡alpha_i (mod p_i). The selected factor
is divisible by p_i and its partial X derivative is a unit;
the other factors and c_i are units.

We can ensure its valuation is exactly one. In the congruence
class n≡a (mod L), changing n by L p_i t changes Q_n by
[L p_i t]R, which reduces to the identity modulo p_i² at
both slots. This follows from the integral formal group law:
[p_i] sends a point of depth at least one to depth at least
two. Hence the coefficients of F_ij(X,Q_n) do not change
modulo p_i² under this variation. The possible lifts of n
modulo p_i² vary over all p_i choices and the unit partial
derivative implies that exactly one of them gives zero
modulo p_i². Choose any other lift b_i.

All congruences n≡a (mod L), n≡b_i (mod p_i²) are compatible.
On the resulting infinite arithmetic progression each active
anchor has positive odd valuation e_ij at its own p_i, since
all other factors have valuation zero. At that prime, the
balanced pole implication requires a shifted formal reference
which Section 2 proves impossible. This obstruction holds for
all auxiliary indices, including noncanonical U.

If a formula or guard is undefined it does not give a witness,
either. We may moreover restrict to the infinitely many n
in this progression with Q_n in the common open, by the
arithmetic-progression density. Hence finite exceptional
input factors cannot repair this failure. The proof did not
assume any uniform bound on the degree or heights of the
anchor coefficients, and a finite menu of rational sign
choices cannot avoid the common progression.

## 4. Even-zero anchors: actual noninteger false positives

For an inactive anchor and a target Q in the common open,
specialization gives a rational function of X all of whose
finite zeros have even order. Write it as

    u(X)=c F(X)^2/G(X)

with coprime rational polynomials F,G, nonzero c. Fix a
prepared integer witness at X=n and hold its target and both
auxiliary points fixed.

Put in a finite set S every fixed exceptional prime, every
prime needed for integral coefficients and unit leading
coefficients of F,G, nonzero resultant of F,G, unit c, and
the nonzero fixed rational scaling factors. Outside S, if
X is integral at p, positive valuations of u(X) are even:
the numerator and denominator cannot vanish simultaneously
modulo p. If v_p(X) is negative even, the leading terms
dominate and v_p(u(X))=(2 deg F-deg G)v_p(X) is again even.

Choose any prime l outside S and take

    X_k=n+J/l^(2k),

where J is a nonzero integer prime to l, divisible by
sufficiently large powers of all primes in S. These X_k
are nonintegers, have exactly one negative valuation
v_l(X_k)=-2k, and tend to n in the real topology. At every
p in S they are as close to n as needed by the choice of J.
Thus no p outside S has positive odd valuation of u(X_k).

The balance proof is needed here: merely observing that no
positive odd primes are consumed would not by itself supply
a global rational pole witness. When nu=v_p(u)<0 is odd,
the formula for D_l gives v_p(D_l²/u)>0 at both slots, so
V≡2 (mod p). Consequently the valuation of e is -nu>0,
outside the fixed scaling primes. When nu is even, the
square normalizers make the valuation of e even. This
handles all new primes, including the sole denominator
prime of X_k.

At each p in S, use continuity of the nonzero rational
detector input e and the fixed point/test values to keep
its valuation and, at two, its local squareclass unchanged.
For large k the strict real inequality 0<e<1 also persists.
All nonzero guards remain nonzero: with the fixed point
data they are nonzero rational functions at the original
witness, and one can avoid their finite zero/pole sets.
The same reasoning handles the finitely many geometric
point-algebra characters if whole-character guards are used.
Hence e(X_k) has square reduced denominator, the prepared
class-seven dyadic properties and the required real bound.

Bhargava--Burungale, *A Diophantine definition of Z in Q*,
[arXiv:2611.16130v2](https://arxiv.org/html/2611.16130v2),
Lemma 2.2 now supplies actual rational product-pole witnesses,
not only local solutions. The nonzero square rescaling
and finite-character encoder of the parent construction
transfer them to rational polynomial witnesses. If required,
use the Zariski-density version of the product pole proved
in the [v88 transfer](../../../papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex)
to avoid nonzero terminal polynomial guards. This produces
noninteger solutions with the same target and auxiliary
elliptic points.

In particular an inactive anchor cannot admit even a single
prepared witness on the common open in a sound version of the
stated relation. This argument needs the prepared converse,
rather than asserting that an arbitrary rational point on
a BB fiber persists as the input varies.

Combining Sections 3 and 4 proves the finite-menu theorem:
take true inputs on the active-anchor failure progression
with target in the common open. Every active anchor fails
completeness and any inactive anchor furnishing a prepared
witness would violate soundness. If there are no active
anchors take any infinite progression. Adding finitely many
integer exceptions cannot remove the obstruction.

## 5. Explicit local rejection fixture and reproducible computation

As a simple deterministic coupled input--target substitution,
take the v63 derivative scalar with B_shift=3 (an algebraic
fixture, not asserted to be a defining shift), a=M^4,
M=(X²+3)^4+Tr(x(A))^4, and set the old slope z=2a.
Use the original shifts {-10,-8,-5,1,2,3,4,6,7}.
At the prime p=76463 the two roots of 2 modulo p are ±31086.
The reduced P coordinates at the corresponding slots are
(53690,8417) and (41903,48889), with curve coefficients
d²=42884 and 33601. Their exact orders are 354 and 177,
both divisible by 3 (and by 59). At every input in the
arithmetic progression

    n = 11196313 mod 2069692990626 = 11196313 mod (354*p²)

the selected scalar has v_p(u)=1. In particular the v63
shifted tests cannot be satisfied at that prime, regardless
of H,U or pole parameters.

The verification below uses Jacobian coordinates modulo p²
rather than constructing the enormous rational point [n]P.
For the order r of the relevant reduction, compute the
formal parameter z_r=-X Z/Y of [r]P modulo p² in Jacobian
coordinates (X:Y:Z) with x=X/Z²,y=Y/Z³. The formal group
addition law gives z([k r]P)≡k z_r mod p², and translation
by P gives x(P+[k r]P)≡x(P)+2 y(P) k z_r mod p² by the
invariant differential. These are valid for both slots.
The computed Tr(x(A_n)) modulo p² is 2385435341;
M=5406239953, a=4085188702, F=2236007509=29243*p,
F_a=3585295406≡21799 mod p. Here F_a is differentiated at
fixed z before setting z=2a. Since u=-18F/F_a, the valuation
is exactly one. Changing n by 354*p² preserves all these
congruences. The witness obstruction is local, so the
ineffective sufficient defining shift of the old family
is irrelevant to this fixture; Section 3 is the general
result for arbitrary fixed shifts and active anchors.

Executed exact verification:
```python
from math import gcd, lcm, prod, isqrt

p=76463
assert all(p%k for k in range(2,isqrt(p)+1))
m=p*p
r0=31086
rt=(r0-(r0*r0-2)*pow(2*r0,-1,m))%m
assert rt*rt%m==2
ds=[(11-6*r)%m for r in (rt,-rt)]
ps=[((57-28*r)*pow(8,-1,m)%m,
     (-660+417*r)*pow(32,-1,m)%m) for r in (rt,-rt)]

def double(Q,d,m):
    X,Y,Z=Q
    S=4*X*Y*Y; M=3*X*X-d*Z**4
    x=M*M-2*S
    return (x%m,(M*(S-x)-8*Y**4)%m,2*Y*Z%m)

def mixed(Q,P,d,m):
    X,Y,Z=Q; u,v=P
    H=(u*Z**2-X)%m; R=(v*Z**3-Y)%m
    if H==0 and R==0: return double(Q,d,m)
    x=R*R-H**3-2*X*H*H
    return (x%m,(R*(X*H*H-x)-Y*H**3)%m,Z*H%m)

def mul(n,P,d,m):
    Q=(*P,1)
    for bit in bin(n)[3:]:
        Q=double(Q,d,m)
        if bit=='1': Q=mixed(Q,P,d,m)
    return Q

orders=(354,177)
prime_divs=((2,3,59),(3,59))
zs=[]
for P,d,r,qs in zip(ps,ds,orders,prime_divs):
    assert (P[1]**2-P[0]**3+d*P[0])%m==0
    X,Y,Z=mul(r,P,d,m)
    assert Z%p==0 and X%p!=0 and Y%p!=0
    assert (Y*Y-X**3+d*X*Z**4)%m==0
    zs.append(-X*Z*pow(Y,-1,m)%m)
    assert all(mul(r//q,P,d,p)[2]%p for q in qs)
assert zs==[5594415395,3115332009]
assert gcd(*orders)==177
L=lcm(*orders)
n=11196313
assert n%L==1 and n%p==32715
T=sum((P[0]+2*P[1]*((n-1)//r)*z)%m
      for P,r,z in zip(ps,orders,zs))%m
M=((n*n+3)**4+T**4)%m
a=M**4%m
cs=(-10,-8,-5,1,2,3,4,6,7)
G=lambda x:prod((x+c)%m for c in cs)%m
Gp=lambda x:sum(prod((x+c)%m for j,c in enumerate(cs)
                     if j!=i) for i in range(len(cs)))%m
x,y=-a%m,3*a%m
F=G(x)*G(y)%m
Fa=(Gp(x)*G(y)+G(x)*Gp(y))%m
assert (T,M,a,F,Fa)==(2385435341,5406239953,4085188702,
                      2236007509,3585295406)
assert F%p==0 and F%m!=0 and Fa%p!=0
assert L*m==2069692990626
print("PASS: exact orders, formal translation and slope-free rejection")
```

## 6. Consequences for further variable reductions

The independent prime supplier is not merely an inefficient
height register. It solves a genuine arithmetic compatibility
problem for the particular direct index extractor. Increasing
the degree of a deterministic input--target contact form, using
more fixed shifts, or adding a finite menu of square-root sign
charts does not cure the odd-zero obstruction. The even-zero
branch shows that suppressing every finite odd contact is
also not a repair of the unchanged equations.

A meaningful next attempt should change the local extractor
itself (for example use an index comparison not requiring
a fixed nonzero shifted reference to be formal in another slot),
or share the prime supplier with a pole witness through a
genuinely new global realization theorem rather than a fixed
rational substitution. Algebraic covers of the input--target
base with nonrational generic branches have not been ruled
out here; proving a rational point on each required fiber is
a separate issue. Neither ordinary abc nor finite local
solubility gives that completeness automatically.

The current eleven-coordinate result and all established
defining-polynomial records remain unchanged. This note
eliminates a specific broad ten-coordinate compression
strategy; it is not a general lower bound on the number of
rational variables.
