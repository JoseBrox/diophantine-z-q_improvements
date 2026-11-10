# An exact two-coordinate reduction of the abc quartic

Write
\[
P(r)=r^4-30r^3+273r^2-820r+576,
\quad r=\delta^2,
\quad q=r^3/P(r).
\]
The existing abc91 circuit stores \(r,q,c=qr,k=qr^2\), together with the inverse weights \(s_j=q^{-j}\), \(j=2,3,4\). Its factors are
\[
T_1=1+qC^2+q^2f_H^2+q^4f_U^4,
\quad
T_2=1+qI^2+q^2g_H^2+q^4g_U^4.
\]
It sets \(W_0=T_1T_2\), \(\tau_0=1/\operatorname{Tr}(W_0^{-1})\), and \(kb=\tau_0^2\).

## New quadratic equations

Retain three contact outputs \(r,u,v\), and the same three inverse-weight coordinates. Impose
\[
r=\delta^2,\qquad u=r^2,
\]
\[
s_4=s_2^2,\qquad s_3^2=s_2s_4,
\]
\[
(u-30r-v)s_2=rs_3,
\qquad uv+273u-820r+576=0.
\]
All six equations are quadratic. The two new field factors \(A_1,A_2\) satisfy
\[
s_3A_1=s_4+s_3C^2+s_2f_H^2+f_U^4,
\]
\[
s_3A_2=s_4+s_3I^2+s_2g_H^2+g_U^4.
\]
The numerator fourth powers are still direct quadratic expressions in the stored reciprocal squares. Define the product by the quadratic field equation
\[
rW=A_1A_2.
\]
For \(W=w_0+w_1\sqrt2\), retain the quadratic trace equation and the new pole row
\[
w_0^2-2w_0\tau-2w_1^2=0,
\qquad s_3b=\tau^2.
\]
All pole-realization equations remain literally unchanged.

## Zero strata and recovery

If \(s_2=0\), the inverse-weight equations give \(s_3=s_4=0\). The factor equations then force both numerator reciprocal squares to vanish. The existing pair-chart identities give both numerator parameters zero, contradicting its equation with constant term one. Hence \(s_2s_3s_4\ne0\).

Put \(t=s_3/s_2\). Then \(t^2=s_2\), \(t^3=s_3\), \(t^4=s_4\). The contact equations give
\[
v=u-(30+t)r,
\qquad P(r)=tr^3.
\]
The case \(r=0\) would give \(u=0\), and then the last contact equation would say \(576=0\). Thus \(r\ne0\), and \(P(r)=tr^3\ne0\). Recover
\[
q=t^{-1},\qquad c=qr,\qquad k=qr^2.
\]
These satisfy every old contact and reciprocal-weight equation.

The factor equations give \(A_i=tT_i\), hence
\[
W=\frac{t^2}{r}W_0.
\]
The trace equation is homogeneous of degree two in \((w_0,w_1,\tau)\). Therefore the old trace coordinate recovers as
\[
\tau_0=\frac r{t^2}\tau.
\]
This works even if the trace equation is considered before any nonvanishing argument. Finally
\[
kb=\frac{r^2}{t}\frac{\tau^2}{t^3}
   =\left(\frac r{t^2}\tau\right)^2=\tau_0^2.
\]
Thus the old pole input \(b\) is unchanged. Conversely, every old solution uniquely determines the new outputs and scaled factor/product/trace coordinates by these formulas. The two complete systems have exactly the same rational projection onto the input and all unmodified elliptic and pole coordinates.

## Count and status

Each detector has six contact/weight coordinates instead of seven and six defining equations instead of seven. With two detectors, the resulting counts should be **89 total variables** and **77 quadratic rows**. Exact literal reconstruction, expanded coefficient counts and independent audit are in progress. The arithmetic and completeness arguments are inherited through the exact projection equivalence, not modified by a new real or local preparation argument.
