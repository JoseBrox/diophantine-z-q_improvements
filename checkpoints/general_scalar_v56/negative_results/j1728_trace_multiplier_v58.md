# A contact obstruction to the centered quartic multiplier

Let

\[
U=V-w/2,\qquad D=w(2-w/4),\qquad
C=V^2+w(2-V)=U^2+D.
\]

The multiplier

\[
\delta=\frac{U^2-D}{w}
\]

gives the centered quartic

\[
\delta C=\frac{U^4-D^2}{w}.
\]

This proposed test is incompatible with every selected contact of
positive odd weight valuation and unit trace. It therefore cannot be
inserted in the retained completeness preparation.

## The two valuation regimes

Fix an odd prime and write its valuation as `v`.

At a hypothetical bad pole, put `nu=v(w)>0`, with `nu` odd, and
assume `2v(V)>nu`. Then `v(D)=nu` and
`v(U)>nu/2`, including possible cancellation when `v(V)=nu`.
Consequently both `U^2+D` and `U^2-D` have valuation `nu`.
The multiplier is a unit, so `v(delta*C)=nu` is odd. Thus the
proposed multiplier has the desired bad-pole parity implication.

At a prepared fresh contact, however, the actual conditions are
`v(w)=nu>0` odd and `V=1` or `2` modulo the prime. Now `U` is a
unit and `v(D)=nu`, so both `C` and `U^2-D` are units. Therefore

\[
v(\delta C)=-\nu,
\]

which is odd. The test has no local square at that contact. The
contradiction applies in particular to the selected simple contacts,
where `nu=1`. It does not depend on any cancellation in the detector
or on the remaining point coordinates.

Multiplication by any nonzero rational square changes this valuation
by an even integer and cannot repair the failure. The same conclusion
holds after any weight normalization that retains the two stated
fresh-contact valuation conditions.

## What a nonsquare correction changes

Multiplying this multiplier by `C/w` changes the radicand to

\[
\frac{C^2}{w^2}(U^2-D).
\]

On the retained nonzero locus, squareness is therefore equivalent to
the different conic condition

\[
U^2-D=V^2-wV+w^2/2-2w\in\mathbb Q^2.
\]

This passes the elementary fresh-contact parity check, but does not
preserve the reference square or automatic real positivity. At
`V=2,w=1/4` the radicand is `97/32`, which is not a rational square.
At `V=w/2` it equals `-D<0` throughout `0<w<=1/4`. Thus positivity
of the original prepared rectangle does not suffice for this new
condition. These observations do not exclude a separately restricted
minus-conic construction; they exclude treating this correction as
the same centered quartic test with the original preparation intact.

The exact elementary checks are recorded in
`check_j1728_trace_multiplier_v58.py` and
`j1728_trace_multiplier_v58_certificate.json`.

**Scope.** This is an obstruction to the displayed multiplier and its
correction by existing squares. It is not an obstruction to all
constant-invariant curves, all trace multipliers, individual rational
witnesses, or smaller defining polynomials.
