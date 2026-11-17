# Independent route v56: final checkpoint

## Proved result

`affine_pheidas_theorem.tex` is the latest polished manuscript. It compiles cleanly to `affine_pheidas_theorem.pdf` (5 pages). The independent audit by `single_cover_realization_v56` checked the local, Galois, reduction, disjointness, torsor and Harpaz–Skorobogatov hypotheses. Its prime-range correction has been incorporated: selected discriminant primes lie outside **{2,3,7}**, and may equal 5.

Let f_(c,i)(X)=c²X⁴+X+i, for i=1,2. The predicate

    c=2±4b,
    c z²=f_(c,1)(x) f_(c,2)(y),
    cz≠0

excludes every negative odd valuation of b away from 2. Assuming finiteness of the 2-primary Tate–Shafarevich groups of elliptic curves over Q, it holds for every b whose reduced denominator is an odd square, including all integers. There are only two free rational parameters x,y; c is a finite sign choice and z a quadratic root. This removes the free parameter t in the Pheidas block of Kozachinskiy–Pasten–Vidaux, but does not save coordinates relative to the repository's existing two-parameter pole block.

The arithmetic reason t is unnecessary is that the general Harpaz–Skorobogatov Theorem 2.3 requires **odd geometric component-group order**, not discriminant valuation one. For these quartics, independent primes of odd discriminant valuation always exist, and at those primes the Jacobians have multiplicative reduction with odd component-group order. The affine shift ensures v₂(c)=1 and c≥2 for the completeness choice, forcing S₄ uniformly by a Newton polygon.

An additional corollary proves that **t=0 itself** works for the original c=±2b predicate on integer inputs. The relevant cubic resolvent T³−4ic²T+c² has no rational root for nonzero integer c. This corollary is narrower than the affine theorem because it does not assert completeness on every rational input with odd square denominator.

## Guards and exact checks

The polynomial finite equations may be taken as

    (c−2)²=16b²,
    Z²=c f_(c,1)(x) f_(c,2)(y),   Z=cz.

The explicit simultaneous guard

    (1−4b²) ∏_(ε=±1) f_(2+4εb,1)(x) f_(2+4εb,2)(y) ≠ 0

can be imposed without losing completeness. H–S gives Zariski density, so all extra factors can be avoided. This makes c and Z units on all characters, including the unused sign. If separability of the sign algebra is required, handle b=0 separately and add b≠0.

Run `python checkpoints/independent_route_v56/check_affine_pheidas.py` from the workspace root. It writes `affine_pheidas_certificate.json` and verifies all symbolic discriminant/Jacobian/factorization identities, every small-prime case used in the all-prime local proof, the prime-5 correction, and rational witnesses including

    b=1, c=6, x=−5/14, y=−8/5, z=17043/2450.

Both sign guards are nonzero at this witness.

## Unproved one-coordinate route

The specialization

    c z²=2(c²x⁴+x+1)

is everywhere locally soluble for every positive c with v₂(c)>0 and no negative odd valuations. Hence it is locally soluble for every completeness input of the affine theorem. Its global rational solubility is **unproved**; finite Sha alone does not imply the Hasse principle for this genus-one curve.

`search_affine_single_curve.py` and `affine_single_curve_search.json` record a bounded exact point search (height at most 300), with points for b=0,3,4,5,6,7 and no point found for b=1,2,8,9,10. These absences are not nonexistence proofs. For b=1 the Jacobian is isomorphic to Y²=X³−1296X+972; a possible Sha obstruction deserves a genuine descent or certified rank computation. No working PARI/Sage environment is available in this restored runtime, and no installation was attempted.

The earlier rational normalization files are superseded research checkpoints; use only the affine theorem as the current polished result.

## Scope and bibliography

No **21/9** result is proved here. Current repository counts remain **25/13**. The new theorem assumes finite 2-primary Sha, not ordinary abc. The KPv paper's integrality theorem assumes abc, Dickson, and finite 2-primary Sha; it has no small-variable census and cannot be imported as a 9-variable ordinary-abc result.

Primary references inspected:

* A. Kozachinskiy, H. Pasten, X. Vidaux, *Why should Z be Diophantine in Q?*, arXiv:2611.17124v1 (12 Nov 2026), Theorem 1.1 and Section 4. https://arxiv.org/html/2611.17124v1
* Y. Harpaz, A. N. Skorobogatov, *Hasse principle for Kummer varieties*, Algebra & Number Theory 10 (2016), 813–841; conditions (a)–(g), Theorem 2.3 and proof of Theorem A. https://msp.org/ant/2016/10-4/ant-v10-n4-p05-p.pdf

Web refs available to the parent after opening the sources: turn156view0, turn157view0, turn157view1, turn157view2, turn158view0. The source content confirms that Theorem 2.3 only needs finiteness for the relevant quadratic twists whose 2-Selmer group has rank 1; the manuscript uses the simpler stronger global finiteness assumption.


## Follow-up: higher Kummer products

`negative_results/higher_kummer_sharing.md` contains the new follow-up proof and count audit. A common quadratic twist for four elliptic factors still uses four free abscissas. Identifying one reference abscissa produces a threefold of Kodaira dimension 1, with exact plurigenera P_m=2m+1; the H–S Kummer theorem therefore does not apply directly. Replacing the two references by one input-dependent reference does yield a three-factor Kummer format, but an explicit rational family defeats its pole soundness. The fully checked example has a valid positive first input with odd square denominator and a positive second input with a negative odd pole at 1133551, outside the present exceptional set. The equations and all raw sign guards are satisfied. These counterexamples are not claimed to be actual detector tuples.

Run `python checkpoints/independent_route_v56/negative_results/check_higher_kummer_sharing.py`; it writes `higher_kummer_sharing_certificate.json`. A separate Newton-polytope parity argument rules out a single rational common coefficient that would detect either independent input's odd pole uniformly. This argument also leaves open restricted actual-trace families.

No rigorous nonexistence proof for the c=6 one-coordinate curve was obtained. Its bounded-search absences remain only computational evidence, and no rank is asserted.
