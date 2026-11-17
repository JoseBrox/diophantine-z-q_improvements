# Independent recovery audit of the 229-coordinate quartic

17 November 2026. Sources: recovered publication archive and pinned upstream
`elliotglazer/diophantine-z-q@498efba6fe75e9d28d6804f1391d7f70e4150afa`.

Verdict: the recovered 229-coordinate construction at N=15 is suitable for
publication with its explicitly retained arithmetic premises. No new proof gap
was found. This audit does not independently reprove the external prime-pattern,
modular-height, elliptic-group or prepared-pole foundations.

The independent finite-algebra, arithmetic and literal-polynomial checkers all
pass. They certify 229 coordinates including input, 207 quadratic rows, 3312
coordinate monomials, degree four, content one, and coefficient height 149^32
at N=15 (232 bits). The literal polynomial checksum is
00484fd8f27d6f6d8435d175c44ad84737a7258fc54d5930e2966496ae5e2528.

The following proof details were checked independently against the manuscript
and pinned upstream source:

* Both abscissa components are available quadratically; the two displayed
  aggregate equations give shifts 13+S0/2 and 17+(S0-S1)/2. Real lower bounds
  give separation by at least 7 and 9 on all allowed torsion fibers.
* The ten center-3/11 contacts have their collision, denominator and midpoint
  support in the stated fourteen-prime exceptional set. The H4.1 radical is
  the full five-contact radical outside the stated ten-prime set; its use at
  small primes is explicitly justified, not inferred from an older cutoff.
* The direct formal-logarithm calculation gives relative precision four at
  all consumed primes. Scalar term valuations occupy distinct residue classes.
  It yields the strengthened divisibility 149^L M_S(beta)^3 | |a|, L=66 at N15.
* Reciprocal valuations and all five detector factors give the claimed orders.
  The integrality-first step makes the later precision absolute. Half-integral
  root labels and the odd fourth label agree with the current source charts.
* The positive-subset torsion sum argument and its full-domain numerical
  corollary are valid. The change to both conjugate components avoids assuming
  an effective lower bound for the rational trace alone.
* The N15 logarithmic comparison is strict. The coarser input bound has the
  stated constants; the Lucas growth contradicts it whenever beta differs
  from the half-integral root label. The denominator endpoint v^2 | 102 is
  sufficient since 102 is squarefree.
* The complete-witness ordering is compatible with the source: choose scalar
  neighborhoods and index first, then the four fixed points and thirty distinct
  contact positions, then primes and final reference progression, and finally
  fresh pole witnesses for every actual final input. The explicit scalar
  inequality needs only N>=3. Prepared primes include 2, 3 and 17 regardless
  of membership in the odd scalar support.

The recovery branch CI did not yet invoke the new v62 publication verifier.
The final main publication adds that verifier, updated result tables, and a fresh
TeX render and inspection receipt.
