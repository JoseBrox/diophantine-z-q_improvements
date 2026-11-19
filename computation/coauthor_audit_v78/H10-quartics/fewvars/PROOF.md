# Simultaneous zero pole ordinates in the Brox finite-algebra rows

All counts include the input. These are degree upper bounds for proposed determinant specifications, relative to commit `d3a8c22` of JoseBrox/diophantine-z-q_improvements. They inherit the arithmetic hypotheses, variable charts, and coefficient thresholds of their respective source rows.

| Source | Variables | Upstream degree | New degree | New support below | Degree with one extra coordinate |
|---|---:|---:|---:|---:|---:|
| General | 25 | 4,863,007,848,923,136 | 2,286,911,582,371,840 | 2^1166 | 475,749,416,960 |
| Certified L=20483 | 27 | 99,279,020,543,180,800 | 15,777,368,968,790,016 | 2^1332 | 1,791,685,033,984 |
| Weak abc, 121/100 | 13 | 43,211,777 | 20,034,049 | 2^271 | 3,978,753 |
| Weak abc, 16/15 | 13 | 39,858,177 | 16,521,729 | 2^267 | 3,026,433 |
| Ordinary abc | 11 | 230,932,097 | 212,710,785 | 2^262 | 36,442,881 |
| Ordinary abc, seven-contact variant | 11 | 356,146,817 | 327,974,273 | 2^269 | 56,345,345 |

The 27-variable height is strictly below 2^(2^67) at L=20483. All other displayed degree and support bounds are uniform in the admissible fixed parameter. For those families the coefficient bounds in bounds.json apply only to the stored small-parameter arithmetic fixtures.

## Arithmetic source

Retain the integral free point algebra of the quoted source. Its point part has successive quadratic generators t_i=W,z per point. The W and z radicands never vanish at any geometric character over a rational base tuple. This follows from the anisotropic quantities N,M,B' and the identity in the upstream v30 paper under “Separation in a quadratic tower.” The generators distinguish all geometric characters of the point algebra. The remaining, reduced generators q_j satisfy q_j²=d_j. Every d_j belongs to the point algebra. There are at most three such generators. These facts are verified from each source DAG.

Retain every native nonzero guard except the individual pole ordinates. Every remaining native guard, every denominator recorded in the source charts and all denominators in source events are protected by the new scalar guard G. Specifically, factor those remaining guard numerators into their syntactic multiplicative atoms, discard nonzero integer constants, and multiply the source subalgebra norm of each distinct atom. Each such norm is a unit test on all geometric point characters. The exhaustive native guard, excluded ordinate, remaining norm, and deleted norm lists are in bounds.json. Compared with the upstream v40 policy, the earlier pole radicands and square multipliers need not be units unless separately used as native guards.

For every character of the reduced algebra the formula Z_j=S_j q_j reconstructs a root of the native equation Z_j²=S_j²d_j, including at zero. Here S_j is the product (with multiplicities) in the source's square extraction. In the other direction the old prepared witnesses have S_j and every d_j nonzero, so q_j=Z_j/S_j constructs the needed new character. This direction is needed only at an upstream prepared tuple for each integer. The retained chart denominators permit reversal to the original pole equations. The local lemma in the upstream v40 paper, “The pole obstruction with zero ordinates,” applies to *each* pole separately and permits zero ordinates. In its notation, a negative odd valuation of b forces v(e)=0 by the first square equation, then the two factors on the right of the second equation have equal finite valuation and their product has even valuation. The other side is zero or has odd valuation. This excludes the same nonintegers as before. The one-pole intrinsic 11-variable row already used this relaxation in its source. Input zero is treated exactly as upstream by the input factor where present.

## Arithmetic separation

Index poles by j=0,...,s-1. For s=1 set k=1. Otherwise set k=3. Define E=sum_j 2^j q_j^k. On any *fixed point character*, the only freedom in the q_j is a sign for each nonzero root. For two extensions with different sign vectors, the difference for k=3 is twice a nonempty signed sum of terms 2^j q_j³. All geometric conjugates of all these values lie in a common finite Galois extension of Q of degree a power of two. Indeed at each stage adjoin square roots of the radicands evaluated at *all* preceding characters in the existing splitting field. This appends a multiquadratic extension stable under all automorphisms of the preceding splitting field. Induction proves the assertion, including any zero radicands. At any prime over 2, normalize the additive valuation to take integer values. Then e=v(2) is a power of two. The terms in the difference have valuations je+3v(q_j). Their residues modulo three are pairwise different for s≤3. Hence the least valuation occurs exactly once, so the difference is nonzero. This also handles repeated radicands and arbitrary dependencies between their square classes, including when exactly one sign survives. The single-pole case is immediate.

Let M_i and M'_j be the explicit positive scalar polynomial envelopes for the point roots and pole roots respectively in the source's quadratic_tower. They bound the complex absolute values on all characters at every rational base specialization. Form B=1+sum 2^j (M'_j)^k, giving |E/(4B)|≤1/4. For m point generators, define

    phi_(m+1) = E/(4B)
    phi_i = t_i (1 + phi_(i+1)) / (4 M_i),  i=m,...,1.
    Omega = 4B (product_i 4M_i) phi_1.

All point-layer values satisfy |phi_i|≤1/3. If two characters first disagree at point generator t_i, this generator takes opposite nonzero values. Their phi_i values lie in disjoint disks centered at ±t_i/(4M_i), each of radius at most |t_i|/(12M_i). Every common earlier stage is an injective affine map because its t value is nonzero. If the point characters agree, E already separates the pole signs. This proves injectivity on the full set of distinct geometric characters. Each phi_1 is nonzero since t_1 is nonzero and its bracket cannot vanish. The clearing factor is rational, positive at rational specializations, and Omega belongs to the original integral algebra. An expanded formula is

    Omega = sum_i 4B (product_{a<=i} t_a)(product_{a>i} 4 M_a)
            + (product_a t_a) E.

Use the original integral free basis and its multiplication operator M_Omega. The defining polynomial is

    det(I - Y G M_Omega),

times input X when the source calls for it. The determinant equals one at G=0. Otherwise a rational zero is equivalent to a character with rational Omega value, by the eigenvalues of multiplication in a finite algebra over an algebraically closed field. This eigenvalue description holds in the presence of nilpotents, since decomposition into Artin local factors gives the residue character value on the diagonal at every factor. A character giving a rational Omega value is fixed by every Galois automorphism by injectivity; all its coordinate values are therefore rational. Conversely for a rational character take Y=1/(G chi(Omega)). This proves the claimed inheritance of the projected input set.

With an extra rational witness Z one can instead use

    (ZG-1)^2 + det(I-Y M_Omega)^2

and multiply the whole result by X on the indicated families. Vanishing of this sum over Q is equivalent to both equations vanishing. This gives the last table column. Content one for the single-witness polynomial also follows by taking Y=0, including the X-factor case.

## Bounds and reproduction

With N the retained rank, g the scalar guard-degree bound, and w the point-algebra operator weight of Omega, the determinant has degree at most N(1+g+w), plus one when multiplied by X. Its degree in Y is at most N. The extra-coordinate formula has degree at most 2 max(1+g,N(1+w)), plus the same possible input factor. We use the upstream weighted basis, integer column-norm bounds for multiplication and the upstream absolute Hadamard coefficient estimate; the only altered operator is the explicitly displayed Omega. The term-by-term maximum of its expanded formula gives w. The scalar guard bounds sum the costs of exactly the retained norm factors. At total variable count v, the bound on support at degree d before multiplication by X is binom(d+v,v)-binom(d-N+v-1,v). Multiplication by X translates the support. The JSON records the intermediate values separately.

Place this directory beside a `source` directory containing the pinned upstream checkout. Alternatively provide the path to the checkout as the first argument to either script. Run `python -B build.py` and `python -B check.py`. The former generates the exhaustively itemized bounds. The latter reads the upstream factorization receipts, checks source/specification digests, verifies all denominator and independence conditions, computes Omega's degree from its expanded sum, and tests finite sign cases with repeated and zero roots. Both use the upstream certified elementary subalgebra norm and tower operator bounds. The production determinant is given by a formula and has not been expanded. No external arithmetic hypothesis was verified by a finite computation.
