# Independent audit of the small trace classes

Date: 17 November 2026.

Audited source: `checkpoints/independent_route_v56/small_trace_classes_20261117_v58.tex`.

## Verdict

The stated algebraic pole implication, fixed and selected local preparation,
whole-character guards, and conditional coordinate census pass. The
simultaneous rational realization at the actual detector traces remains an
explicit additional hypothesis. No complete 21- or 9-variable definition is
established by this paper.

## Pole and real-place checks

At a hypothetical negative odd pole of `b=4w/V^2` outside the retained
exceptional set, the source assumption gives an odd `nu=v_p(w)>0` and
`2v_p(V)>nu`. Thus `v_p(V)>=1`, `2-V` is a unit, and
`v_p(V^2+w(2-V))=nu`. The three multiplier residues are respectively
`2,2,1`; they are units at every such prime. No assumption that these
residues are squares is used in soundness.

For every prepared real character, `w>0` and `0<V<=2`. The conic radicand
is at least `V^2>0`; the multipliers `V+2`, `V^2-V+2`, and `1+w(2-V)`
are all strictly positive. This applies to all geometric characters of the
prepared finite point algebra, including its sign choices.

## Prime construction and local squares

The primary source was opened and its exact Theorem 4.1 checked:

- Z.-W. Sun, *48 unknowns for Hilbert's tenth problem over the rationals*,
  arXiv:2610.20691v3, Theorem 4.1,
  <https://arxiv.org/html/2610.20691v3#S4> and
  <https://arxiv.org/pdf/2610.20691v3>.
- Its modulus `M` is any odd squarefree integer not divisible by 7, so
  including 3 is permitted. The prescribed Gaussian generator satisfies
  `pi=9 mod16` and `pi=i modM`. Norms therefore give `p=1 mod8` and,
  when `3|M`, `p=1 mod3`. Hence `p=1 mod24`, making both 2 and 3 squares.
- The same theorem includes the cross-order gcds, self-order gcds,
  avoidance, arbitrary lower bounds, and prescribed divisibility of the
  square-denominator parameter. None is replaced by a separate prime
  existence assumption.

At selected fresh contacts, the retained actual trace is 1 or 2 modulo
the selected prime and `v_p(w)>0`. The multiplier residues are
`(3,2,1)` or `(4,4,1)` respectively; multiplying by the conic residue
1 or 4 gives a nonzero local square. Hensel's lemma applies since the
selected primes are odd.

At fixed finite places, the original ordered preparation makes `V`
arbitrarily close to 2 and keeps `w` bounded (or tending to zero in the
conditional source). The limiting radicands are 16, 16, and 4. At 2,
write `e=V-2`; the sufficient conditions
`v_2(e)>=5` and `v_2(w e)>=5` ensure that
`(V+2)/4`, `(V^2-V+2)/4`, `1-w e`, and
`(V^2-w e)/V^2` all belong to `1+8 Z_2`.
The original order of choices first fixes scalar neighborhoods and then
selects the slope, so it permits these extra fixed precisions.

The local conclusion concerns only the selected contacts and fixed
preparation places. It does not prove local solubility at uncontrolled
new primes or rational solubility.

## Exact algebra and encoding

The expansions, degrees, monomial counts, discriminants, and tangent
identity agree with direct symbolic calculation and the supplied checker.
The two cubic changes of variables are invertible at `w!=0`. The stated
two-torsion translation is `x -> B/x` on the monic model
`z^2=x(x^2+A x+B)`, and transforms to the displayed trace formula.
The tangent identity gives `R=-[2]Q` with the point at infinity as origin.

All multipliers are polynomials in the already guarded weight and trace.
Writing a radicand as `N/D` and adjoining `Y^2=ND` introduces no new
unrestricted rational coordinate. At every prepared character,
`ND=D^2 R_i>0`; its numerator and denominator norms are nonzero.
Consequently the two extensions have rank factor 4 and are finite,
etale, and totally real on the prepared locus. The retained separator
forces a rational character of the entire algebra, hence rationality of
the square roots. The resulting census is `1+2p+1+1=2p+3`, giving
21 for `p=9` and 9 for `p=3`, subject to actual realization.

For a single-cover conditional source there is one square extension,
giving rank `4^3*2=128`; replacing the slope coordinate by its retained
cover parameter leaves the same formal count 9. Its separate height
and rational-realization requirements are still necessary.

The finite-menu product construction is a genuine finite disjunction
and adds no coordinate. The displayed coefficient bounds concern only
the polynomial blocks before actual-source substitution and determinant
compilation, exactly as stated.
