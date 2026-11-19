# Physical normalization of the shared general quartics

The general quartics in the notes of **Gabe Conant with Astra 6.2**, and their
v78 enhanced versions, use different Laurent weights in their first and second
native pole blocks. The common physical pole coordinate is

\[
b_j=c\,x_{B_j},
\]

where \(B_0=82\), \(B_1=96\), and \(B_2=582\) for the explicit third block.
In particular it is not \(x_{B_j}/c\).

The exact physical substitutions are:

| Block | \(e\) | \(u\) | \(v\) | \(p\) | \(q\) |
|:--|:--|:--|:--|:--|:--|
| 0 | \(x_3/c\) | \(x_4\) | \(x_{84}\) | \(x_5/(Cc x_{113})\) | \(x_6/x_{113}\) |
| 1 | \(cx_7\) | \(cx_8\) | \(cx_{98}\) | \(cx_9/x_{113}\) | \(cx_{10}/x_{113}\) |
| 2 | \(x_{503}/c\) | \(x_{504}\) | \(x_{584}\) | \(x_{505}/(Cc x_{113})\) | \(x_{506}/x_{113}\) |

Here \(C,c,x_{113}\ne0\), as required by the retained source chart. Using
\(cx_{112}=Cx_{113}^2\), the published conic and product rows become

\[
3e^2-34e-289+17bp^2=0,\qquad
e(17-b)=17uv,\qquad
u^2+34uv-867v^2=17bq^2.
\]

The gate and pole-input rows give, with \(q_j\) the corresponding reciprocal
contact weight,

\[
2cx_{T_j}=g_j=1+D^2+\frac{(c-q_j)^2}{q_j},\qquad
cx_{B_j}(1+q_j)=\left(\frac{408}{409}\right)^2(cx_{T_j})^2.
\]

Consequently the actual pole input is exactly

\[
b_j=\left(\frac{408}{409}\right)^2\frac{g_j^2}{4(1+q_j)}
=\left(\frac{408}{409}\right)^2\frac{R_j g_j^2}{4}.
\]

There is no additional factor \(c^{-2}\). Thus this normalization check finds
no change to the pole valuation inequality used in the v78 proof.

Run `python -B computation/variable_reductions_v79/pole_normalization/check.py`.
The checker reads the literal quadratic tables and Laurent weights, without
importing any producer or earlier checker. It verifies all ten pole blocks in
the supplied and enhanced 165- and 180-coordinate presentations, and explicitly
rejects the expression with an additional factor \(c^{-2}\). The certificate
records the exact input hashes and the nonzero Laurent factors relating the
published rows to the native equations. This is an algebraic audit; it does not
establish the retained arithmetic premises or a smaller variable count.
