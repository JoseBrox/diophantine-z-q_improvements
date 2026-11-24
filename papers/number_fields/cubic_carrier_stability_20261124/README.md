# Exact rank stability for the original carrier in a cubic extension

Put
[
F=\mathbb Q(\sqrt2),\qquad d=3-\sqrt2,\qquad
E:y^2=x^3-d^2x,
]
and let (K=\mathbb Q(z)), where (z=2\cos(2\pi/7)) satisfies
(z^3+z^2-2z-1=0). Then, unconditionally,
[
\operatorname{rank}E(FK)=\operatorname{rank}E(F)=1.
]
In particular this is a genuine example of the original carrier rank-stability hypothesis, not the rank stability of an unrelated elliptic curve. It does not require finiteness of Sha, an analytic-rank computation, or the Mazur–Rubin stability theorem.

## Arithmetic of the compositum

Write (L=FK). Its ring of integers has the basis
(1,z,z^2,\sqrt2,\sqrt2z,\sqrt2z^2). Indeed the two subfields are linearly disjoint and have coprime discriminants 8 and 49 (the real cyclotomic cubic of conductor 7). Thus the product order is maximal and (D_L=8^3 49^2). The field is totally real. The Minkowski bound is
[
\frac{6!}{6^6}\sqrt{8^3 49^2}<18.
]
The only prime ideals of norm less than 18 are the unique prime above 2 of norm 8 and the two primes above 7 of norm 7. To check this, 2 is inert in (K) and ramified in (F); 7 is totally ramified in (K) and split in (F). The cubic polynomial is irreducible modulo 3, 5, 11 and 17 (it has no root), and 13 is inert in (F). These exhaust the rational primes up to 17. The prime above 2 is principal with generator (\pi=\sqrt2). The element
[
g=-1-z+\sqrt2(-1-z+z^2)
]
has norm -7, vanishes at (z=2,\sqrt2=3\pmod 7), and is nonzero in the other residue field, where (\sqrt2=4). Its (F)-conjugate generates the other prime above 7. Hence every ideal class is trivial. Also (d) generates the cube of ((g)).

The following six units, recorded in the indicated integral basis as integer tuples, all have norm -1:
```
(-1,-1,-1,-1,-1,0)
(-1,-1,-1,0,-1,-1)
(-1,-1,-1,0,-1,0)
(-1,-1,-1,0,1,0)
(-1,-1,-1,0,1,1)
(-1,-1,-1,1,1,0)
```
Order the embeddings by increasing real root of the cubic, and for each root take the negative and positive square roots of 2 in that order. Their negative-sign bitmasks (least significant bit first) are 59, 47, 61, 62, 31, 55, which are independent over (\mathbb F_2). The masks are certified using rational isolating intervals, not floating point. Dirichlet's unit theorem gives (|\mathcal O_L^\times/\mathcal O_L^{\times2}|=2^6), so the six units generate all unit squareclasses. In particular a computation of the full fundamental unit lattice or its regulator is unnecessary.

## Complete isogeny upper bound

Use the rational 2-isogeny from (E) to
[
E':y^2=x^3+4d^2x .
]
For a curve (y^2=x^3+Bx), the Kummer image of the relevant isogeny is given by the classes (b\in L^\times/L^{\times2}) admitting
[
N^2=bU^4+(B/b)V^4,quad (U,V)\ne(0,0).
]
This includes the usual exceptional classes at the identity and ((0,0)). The standard 2-isogeny descent formula gives (2^{r+2}=|I||I'|), since (E) has full rational 2-torsion. Away from primes dividing (B), a negative or positive odd valuation of (x) is impossible (respectively the cubic or linear term dominates), so only unit classes are needed there. Since the class group is trivial, the candidates for (E) are the six unit generators and (g); for (E') also include (\pi). All chosen representatives (b) divide (B) in the integral ring, so (B/b) is integral.

For the dual curve (E'), positivity of (x^3+4d^2x) forces (b) totally positive. At the prime ((g)) of residue field (mathbb F_7), the valuation of (d) is 3 and (-1) is nonsquare. The original image contains the classes (-1,d) from the 2-torsion and these generate all four local classes. The local isogeny index product equals 4 in odd residue characteristic, so the dual local image is trivial. Thus in the dual enumeration reject odd exponent of (g) and nonsquare residue modulo ((g)). These filters are necessary; sufficiency is not needed for an upper bound.

At the unique dyadic prime, use the integral primitive quartic chart: after dividing (U,V) by a common local scalar, one is a unit, and division by that coordinate sets it to 1. Since both coefficients are integral, (N) is integral in the normalized equation. Thus either (b+(B/b)t^4) or (B/b+bt^4) must be a square modulo 8. In the six-element integral basis every square modulo 8 depends only on the argument modulo 4, and every fourth power modulo 8 depends only on the argument modulo 2, by binomial expansion. This leaves 1856 square residues and 64 fourth-power residues. The complete enumeration leaves exactly eight candidates for (I) and one for (I'). Their bit vectors, with (g) last for (I), are
```
0000000 0000111 0010001 0010110
1101000 1101111 1111001 1111110
```
The sole dual bit vector is zero. Consequently (2^{r+2}\le8), giving (r\le1). The original non-torsion point over (F) (also the independently certified rank-one result in the [twist audit](../carrier_twist_parity_20261124/README.md)) yields the reverse inequality. This establishes rank stability exactly.

## Consequence for defining integers

The hypotheses of the [carrier-specific transfer theorem](../carrier_rank_stability_20261124/README.md) concerning rank stability and linear disjointness now hold unconditionally for this explicit cubic. Keeping ordinary (abc) over (K) and the other stated local/prime-supplier and height hypotheses of that construction, we obtain:

- (\mathbb Z^k\subset K^k): **(3k+8)** total variables, including inputs.
- (\mathbb Z\subset K): **11** total variables.
- (\mathcal O_K\subset K): **17** total variables.

These are arbitrary-degree polynomial counts, not quartic counts. They do not discharge the other arithmetic premises or the (abc) assumption. Nor do they assert that the group equality (E(L)=E(F)) holds: rank equality suffices because a fixed multiplication maps the group into the original rank-one subgroup. The checker `verify.py` performs all finite parts of the above certificate in the standard Python library using integer and rational arithmetic. The rank conclusion uses the stated standard descent, Minkowski and Dirichlet theorems.


## Second exact example: conductor 9

The same conclusion holds for \(K_9=\mathbb Q(2\cos(2\pi/9))\), with the defining polynomial \(z^3-3z+1\). Its discriminant is 81, coprime to 8, and the compositum again has the same six-element integral basis. Its Minkowski bound is less than 29. The only primes of norm less than 29 are those above 2 (norm 8), 3 (norm 9), and 17 (six primes of norm 17). The splitting statements follow by reduction of the two defining polynomials: at 3 the cubic is totally ramified and the quadratic inert, at 17 both split, at 5, 11, 13 and 19 the quadratic is inert, and at 7 and 23 the cubic is inert. The prime above 2 is generated by \(\pi\), the prime above 3 by \(1+z\) of norm 9, and one prime above 17 by
\[
-1-z-z^2+\sqrt2(-1-z^2)
\]
of norm 17. Its conjugates give all six primes over 17, since the compositum is Galois. Thus the class group is again trivial.

In the same basis six unit generators modulo squares are
```
(-1,-1,-1,0,-1,0)
(-1,-1,-1,0,1,0)
(-1,-1,0,-1,0,0)
(-1,-1,0,-1,1,1)
(-1,-1,0,1,-1,-1)
(-1,-1,0,1,0,0)
```
Their norms have absolute value 1 and their certified signature masks are 61, 62, 58, 29, 46, 53, again independent. Now 7 is inert in the cubic and splits in the quadratic, so \(d\) itself generates the unique prime of its support, of norm \(7^3\), and has valuation 1 there. Use \(g=d\) in the enumeration. The dual residue test at that prime is the square test in \(\mathbb F_{7^3}\), implemented by exponent 171. All other steps of the proof are identical, with the cubic multiplication relation changed. The modulo-8 square and fourth-power sets again have sizes 1856 and 64. The original candidate bit vectors are
```
0000000 0000001 0110100 0110101
1001010 1001011 1111110 1111111
```
and the dual image has the unique candidate 1. The companion checker `verify_conductor9.py` verifies these computations with exact arithmetic. Hence the rank over \(FK_9\) is also exactly one. The same conditional 11-variable and 17-variable conclusions apply to this second cubic field.

