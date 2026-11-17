# Independent seven-coordinate chart audit

Let the field have characteristic different from two, let D and beta be nonzero, and set Q=beta^4. Put p=h+s+t. The five rows are

\[
 a=hp,\qquad d=pF,\qquad D(F+G)=(s-t)h-t^2,
 \qquad d=Gh,\qquad Q=d(s-t)-DFG.
\]

## Exact domain and recovery

They describe exactly the ordered pairs U,V of finite points on
\(E:y^2=x^3-Dx\) with nonzero abscissas and U different from V.
All coordinates are uniquely determined. The meanings are

\[
 F=\beta^2/x(U),\quad G=\beta^2/x(V),\quad
 s=\beta y(U)/x(U),\quad t=\beta y(V)/x(V),
 \quad a=\beta^2x(U-V).
\]

For clarity, recover scaled points on E': y^2=x^3-DQx by

\[
 U'=(Q/F,sQ/F),\qquad V'=(Q/G,tQ/G).
\]

The equations imply
\(Q=DF^2+s^2F=DG^2+t^2G\), so F and G cannot vanish. These identities prove the curve equations. If U'=V', then F=G and s=t; the second and fourth rows force s=t=0, and the third forces F=0, a contradiction. Thus the difference is finite.

Write T0=(0,0) on E'. Translation gives

\[
 U'+T_0=(-DF,DsF),\qquad -(V'+T_0)=(-DG,-DtG).
\]

The line y=(h+t)x+Dd contains these points. Its exact cubic intersection factors as

\[
 x^3-DQx-((h+t)x+Dd)^2=(x+DF)(x+DG)(x-a)
\]

on the five-row zero set. With intersection multiplicities, its third point is the negative of U'-V'. Consequently

\[
 U'-V'=(a,-(h+t)a-Dd).
\]

If F differs from G the line is the ordinary secant. If F=G, the rows force t=-s and s nonzero, and

\[
 h=\frac{2DF+s^2}{2s},\qquad
 h+t=\frac{2DF-s^2}{2s},
\]

which is exactly the tangent slope at (-DF,DsF). Triple intersections cause no additional exclusion. Zero ordinates of either original numerator and nonzero-abscissa two-torsion differences are included.

## Converse and regularity

Given any allowed ordered pair, translate as above. The line through the first translated point and the negative of the second is nonvertical: a distinct vertical pair would force U'=V', which is excluded. If the two line points coincide, their ordinate is nonzero; otherwise that coincidence would again force U'=V'. Use the tangent in this case. With its slope mu put h=mu-t and d=Gh. The secant or tangent law gives every displayed equation and a=x(U'-V').

An explicit regular inverse for h uses the two formulas

\[
 h=\frac{(s+t)F}{G-F},\qquad
 h=\frac{D(F+G)+t^2}{s-t}.
\]

Their equality on the overlap follows from the two curve equations. At G=F the second denominator equals 2s, which is nonzero. Thus the inverse extends across the whole allowed tangent locus. These two opens cover every allowed pair. No division by a variable ordinate is made on the secant locus, and no division by the difference abscissa occurs anywhere.

## Extra difference T0 and soundness

The chart newly allows U-V=(0,0). This is a finite torsion difference, not the identity. Its elliptic index is zero, so the needed inequality m(U-V)^2 <= C h(Tr x(U-V))+J holds trivially. Alternatively the existing all-finite-point trace theorem already includes it.

All remaining 71-source interpretations transfer unchanged. The product rows v_H J=u_H F and v_H K=w_H G give the same physical reciprocal products. F,G and the three reference coordinates are nonzero for beta nonzero, so J,K are nonzero and the proof excluding zero detector weights remains valid. The inverse-parameter extraction, pole obstruction, local residual beta(m-beta), and the height-gap argument use precisely these same quantities. The affine carrier is still Tr(a)=beta^2 Tr x(U-V); it is unchanged on the intended completeness family.

## Completeness and zero input

Every old nonzero-input witness lies in the new domain, since its numerator points are finite with nonzero abscissas and their difference [X]R0 is nonzero. The new chart supplies a unique lift, including tangencies. Its functions are regular on that domain, so the same compact local and real neighborhoods can be retained or shrunk. No new prime avoidance, point guard, arithmetic hypothesis, or sufficient-shift enlargement is required for the transfer.

At beta=0 retain the old reference and put s=S, t=T_H with s different from t. Set

\[
 F=G=d=0,\qquad h=\frac{t^2}{s-t},\qquad
 a=\frac{s^2t^2}{(s-t)^2}.
\]

All five chart rows vanish literally. This a equals the old c^2, so the gap and every remaining detector and pole witness are unchanged. In particular zero input remains complete without an additional coordinate.

## Census and verification scope

The full field abscissa a is not needed as a stored coordinate. The other rows do not consume it, and the height gap consumes only Tr(a). Store the single rational coordinate a_real=Re(h(h+s+t)); recover the omitted imaginary component uniquely as Im(h(h+s+t)). This introduces no denominator, guard, or boundary exclusion. The actual 69-coordinate intermediate table was checked: its imaginary component appears in exactly one residual, its own linear definition.

Consequently the final chart uses six field coordinates (s,t,F,G,h,d), four field equations, and one rational quadratic output equation for a_real. Replacing the old eight-field-coordinate block removes three rational coordinates and three rational quadratic rows. The final source has 68 total rational coordinates and 56 quadratic rows.

The independent standard-library checker `computation/quartic/abc68_v65/check.py` reconstructs all 56 literal rows, every invertible basis operation, and the full sum-of-squares expansion. Its receipt `computation/quartic/abc68_v65/independent-verification.json` records 1078 coordinate monomials, 1081 parameter-separated terms, degree exactly four, integer content one, and exact coefficient height B^2+1 for every B>=81. The count includes the input and every helper. Its zero-input fixture is an algebraic identity check, not a sufficient defining parameter.

`computation/quartic/abc68_v65/chart-check.py` verifies explicit ideal-membership identities for both curve equations, the full line factorization, both line evaluations, regularity on the two slope charts, and the zero-input substitution. It independently compares the entire chart with an elliptic group law over all nonzero coefficients in seven small odd prime fields. The finite checks supplement the all-field proof above; they do not establish the external arithmetic source premises.
