# Reciprocal contact symmetry and a candidate quartic in 87 variables

Use the eight rational contacts
\[
\Theta=\{-5,-2,-1,0,2,3,4,7\}
       =\{1\pm1,1\pm2,1\pm3,1\pm6\}.
\]
For a detector argument \(t\), put \(\delta=t-1\), \(r=\delta^2\). The contact polynomial is
\[
F(t)=P(r),\quad
P(r)=(r-1)(r-4)(r-9)(r-36)
=r^4-50r^3+553r^2-1800r+1296.
\]
Its roots are paired by \(r\mapsto36/r\). Consequently, with \(z=r+36/r\),
\[
P(r)/r^2=z^2-50z+481.
\]
The normalization \(q=r^3/P(r)\), with inverse \(s=1/q\), is therefore equivalent to
\[
r(z-r)=36,\qquad rs=z^2-50z+481.
\]

## Literal quadratic equations

Store only two contact outputs \(R=r-1\), \(Z=z-37\), and three weights \(s,s_2,s_3\). Impose
\[
R=t^2-2t,
\]
\[
RZ+Z-R^2+35R=0,
\qquad (R+1)s=Z^2+24Z,
\]
\[
s_2=s^2,\qquad s_3=ss_2.
\]
The contact equations have no constant terms. The factors and product are
\[
s_3A_1=s_2^2+s_3C^2+s_2f_H^2+f_U^4,
\]
\[
s_3A_2=s_2^2+s_3I^2+s_2g_H^2+g_U^4,
\qquad (R+1)\Omega=A_1A_2.
\]
The field fourth powers are direct quadratic expressions in stored squares. For \(\Omega=\omega_0+\omega_1\sqrt2\), retain
\[
\omega_0^2-2\omega_0\eta-2\omega_1^2=0,
\qquad s_3b=\eta^2.
\]
Every equation is quadratic. The pole-realization equations are unchanged.

## All finite strata

The relation \(r(z-r)=36\) forbids \(r=0\). If \(s=0\), then \(s_2=s_3=0\), and the two factor equations force both numerator reciprocal squares to vanish. The unchanged pair chart excludes this, so \(s\ne0\). Hence
\[
P(r)=sr^3\ne0,
\qquad q=s^{-1},\quad F=P(r),\quad k=r^2/s.
\]
Set \(T_i=A_i/s\), \(W_0=r\Omega/s^2\), \(\tau_0=r\eta/s^2\). Exactly as in the abc89 scaling identity,
\[
T_1=1+qC^2+q^2f_H^2+q^4f_U^4,
\quad
T_2=1+qI^2+q^2g_H^2+q^4g_U^4,
\]
\[
W_0=T_1T_2,
\quad k b=\tau_0^2,
\quad b=F\delta^{-10}\tau_0^2.
\]
Thus the original local trace inequality and the real/finite preparation apply to the unscaled factors and exactly the same form of pole input. The inverse coordinate formulas are unique on this domain.

## Arithmetic consequences of the contact change

The contacts are still eight distinct integers, symmetric about one, include zero, and omit one. All nonzero differences and all distances from one have prime factors below the existing cutoff76176. The rational abc argument based on a squarefree binary form of degree8 again gives
\[
h(t)\le\tfrac13\log M(t)+C_0,
\]
with a possibly different fixed ineffective constant. The two comparison scales and absorption coefficient8/9 are unchanged.

At every consumed contact prime, \(v(q)=-\nu\), with \(\nu>0\) odd, and the local valuation classes and completeness orders are unchanged. For fixed positive scales, the prime-product squareclass identity remains valid because the contact polynomial still has degree8 and the pole denominator has degree10. At preparation primes and at real infinity,
\[
q\sim F\delta^{-10}\sim t^{-2}.
\]
The completeness proof therefore retains its finite preparation and real decay; no new approximation to a real elliptic point is required.

## Count and pending verification

The detector now uses five contact/weight coordinates instead of six in abc89. With two detectors, the expected total is **87 variables and75 quadratic rows**. All absolute contact constants still vanish, so the expected constant coefficient is \(B^2+797681\). Complete coefficient expansion and independent checks are pending; no final numerical support claim is made here.
