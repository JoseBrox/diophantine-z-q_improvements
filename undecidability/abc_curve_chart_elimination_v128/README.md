# Exact curve-coordinate elimination (v128)

**295 rational variables, 244 quadratic residuals.** This is an exact bijective rechart/projection of v126, including its 12 certified integer inputs and one native pole. The retained arithmetic premises (ordinary rational abc included) and the ineffective sufficient positive coefficient shift are unchanged. Every step below is an algebraic equivalence over \(\mathbb Q\) or \(K=\mathbb Q(\sqrt2)\); no extra local or real restriction is added.

## 1. Homogeneous numerator chart: two coordinates

The old numerator chart of v119/v126 stores \(x,y,x_2,f,h\in K\) with
\[
 x_2=x^2,\quad y^2=x x_2-\Delta x,\quad fx=1,\quad h x_2=-y.
\]
Delete \(x_2\), and replace the other curve and ordinate equations by
\[
 yf+hx=0,\qquad hy+x=\Delta f,\qquad fx=1.
\]
All are quadratic over the rationals in the two components of each field. Since \(fx=1\), the first gives \(y=-hx^2\); multiply the second by \(x^2\) to get \(y^2=x^3-\Delta x\). Conversely the old equations imply the new ones by division by the nonzero \(x\). Recover \(x_2=x^2\) uniquely. This includes every allowed numerator point, including its zero ordinate if present at the algebraic chart level. The remaining nonzero guards are untouched.

## 2. Inline the opposite reference square: two coordinates

After v125, \(f_{H-R_0}^2\) is unscaled in the slot selector. Its two components occur only linearly with constant coefficients in the reference secant and the slot polynomial (apart from their defining equations). Replace them by
\[
 f_0^2+2f_1^2,\qquad 2f_0f_1
\]
in those rows and delete the two square-defining equations. The exact occurrence scan in the compiler rejects any unexpected occurrence in a retained row. This changes no predicate or zero set; both components are uniquely recovered.

## 3. Eliminate the shifted abscissa center: two coordinates

Write \(d=2y(U)h_{H-R_0}\), \(D=d^2\), \(I D=1\). The previous chart used
\[
 x_*=x(U)-d\mu,\quad L=I x_*,\quad
 T_{\rm tr}=\operatorname{Tr}(12x_*+D\sum_i e_i).
\]
Instead use
\[
 DL=x(U)-d\mu,\quad
 T_{\rm tr}=\operatorname{Tr}(12x(U)-12d\mu+D\sum_i e_i).
\]
Both are quadratic, with the same trace and exact reconstruction since \(ID=1\). Delete the two components of \(x_*\) and recover them by the original formula.

## 4. Shift the private error squares: one coordinate

The previous private shifted cubic uses
\[
 S=L^2-\Delta I^2,\quad K_0=3L^2-\Delta I^2,\quad
 Q_i=e_i^2,\quad
 Y_i^2=LS+K_0 e_i+3LQ_i+e_iQ_i .
\]
Its failure fraction is \(D_i(u+\operatorname{Tr}Q_i)=\operatorname{Tr}Q_i\).
Instead store
\[
 T=S-3K_0=-8L^2+2\Delta I^2,\quad k=\operatorname{Tr}(K_0),
 \quad Q_i'=e_i^2+3L^2-\Delta I^2.
\]
Only the two components of \(T\) and the scalar \(k\) are common, instead of the four components of \(S,K_0\). The new private equations are
\[
 Y_i^2=(e_i+3L)Q_i'+LT,\quad
 D_i(u+\operatorname{Tr}(Q_i')-k)=\operatorname{Tr}(Q_i')-k .
\]
Every formula is quadratic. In the old-to-new map add \(K_0\) to each private square. In the reverse map compute \(K_0=3L^2-\Delta I^2\), \(S=L^2-\Delta I^2\) and subtract \(K_0\) from each \(Q_i'\). Expansion of the displayed cubic gives the identity in both directions; the rational failure fractions are literally unchanged under recovery, including zero errors and every valuation stratum. Thus there is no weakening of the v123/v125 Boolean or height arguments.

## 5. Census

Delete eight coordinates, add one, and replace seven more quadratic rows than are added: \(302-7=295,\ 251-7=244\). The old field-norm and source guards, integer-input squares, derivative coefficients, trace, height tree, and terminal pole are all retained or exactly recovered. The degree of the sum of squared residuals is exactly four (nonzero quadratic rows and no cancellation of their leading real squares). The complete deterministic compiler, pinned v126 predecessor and coefficient table are included. Run `node build.mjs` in this directory to replay it. The compiler checks full support, ordinary variable degrees, named-coordinate occurrences and exact counts. No global minimality or new arithmetic proof is claimed.
