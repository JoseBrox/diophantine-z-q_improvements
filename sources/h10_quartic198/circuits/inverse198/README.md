# The 198-coordinate quartic

This directory contains complete quadratic and expanded quartic tables. The arithmetic proof is `../../arithmetic/inverse_vieta_198.tex`; it retains the arithmetic premises of Brox's pinned 204-coordinate source. The sufficient defining threshold is ineffective. Finite algebraic checks do not certify those inherited premises.

Every count includes the rational input. The unbalanced and balanced polynomials both have 198 variables, 184 quadratic residuals, total degree four, integer content one, and exactly 2,945 nonzero coordinate monomials for every permitted parameter. Their expanded tables have respectively 2,945 and 2,959 terms when parameter powers are stored separately.

Let `K0=31581660^28`, `J0=5898050446009651968`, and `H0=(J0*K0)^2`. The unbalanced fixed parameter is `A=149^(2N+1)`, and its exact coefficient height is `max(H0,A^2)`. The constant H0 has 458 decimal digits; the A² term dominates from N=53. The balanced parameter is `C=149^N`, and its exact height is `max(H0,K0*C^2)`, with crossover N=57. These are coefficient crossovers, not sufficient defining thresholds.

## Coordinate conventions

The `id` entries are the coordinates in the delivered polynomial. `formalId` records coordinates before final compaction: 1–204 refer to the pinned Brox 204-coordinate table; 205–214 are the new reciprocal fourth-point pair; 215–228 are the inverse Vieta scalar chart. The `source200Id` entries identify retained coordinates of the separately checked 200-coordinate intermediate.

For an ordinary field pair `(i,j)`, the represented element of Q(sqrt(2)) is `z_i+sqrt(2)*z_j`. In the two square-output pairs specifically indicated below, it is `z_i+2*sqrt(2)*z_j`.

| Quantity | Delivered coordinates | Meaning |
|---|---:|---|
| Input X | 1 | Rational input |
| lambda, t1 | 2, 88 | Comparison arguments; t1=lambda+T |
| f(H) | 15,16 | Ordinary field pair |
| S | 17,18 | y(H)/x(H) |
| T_H | 153,154 | y(H-P)/x(H-P) |
| F_U | 54,55 | f(U2)^2; doubled second-component convention |
| F_V | 23,24 | f(V2)^2; doubled second-component convention |
| L2 | 33,34 | 2*z(U2)/z(H), now unscaled |
| L2^0 | 35,36 | 2*z(V2)/z(H-P), now unscaled |
| Z_stored | 105,106 | 2*z(Q2)/(R*z(H)) |
| r_contact_stored | 104 | r_beta/R |
| R2, R | 115,116 | R2=R^2; R>0 |
| u | 185,186 | Inverse Vieta coordinate |
| v | 187,188 | Inverse Vieta coordinate |
| w | 189,190 | Inverse Vieta coordinate |
| m | 191,192 | Inverse Vieta coordinate |
| r | 193,194 | Scaled line intercept; r is nonzero |
| p | 195,196 | Exactly x(Q2) |
| r2 | 197,198 | Exactly r^2 as a field element |

Here `z(Q)=-x(Q)/y(Q)`, `f(Q)=1/x(Q)`, and `D=11-6*sqrt(2)`. The final scalar chart satisfies

```
u*v = R2*p,
p*w = r,
r*(u+v+w+2*m) + D*R2 = 0,
R2*p+w*(u+v) = m^2,
r2 = r^2,
F_U*r2 = u^2,
F_V*r2 = v^2,
L2*(m+u) = 2*R*S,
L2^0*(m+v) = -2*R*T_H,
Z_stored*(m+w) = -2*S.
```

All are field quadrics. The defining rational row `R2=R^2` is retained; it is not simplified away while rescaling other rows. Since R>0 and D is nonzero, the third equation forces r nonzero. The first two then force u,v,w,p nonzero. The ratio equations, with S and T_H nonzero, force all three corresponding ordinates nonzero. The recovered points are

```
x(U2)=r/u,       y(U2)/x(U2)=(m+u)/R,
x(V2)=r/v,       y(V2)/x(V2)=-(m+v)/R,
x(Q2)=p,        y(Q2)/x(Q2)=-(m+w)/R,
Q2=U2-V2.
```

The scalar arithmetic label is `a=2*nu(Q2)`, hence is a nonzero integer under the inherited elliptic group premise. The third label is likewise doubled. The fourth is `b=4*nu(Q4)+1`, hence odd and nonzero. The Lucas parameter is a+1. Its defect is

```
t^2-(a+1)*(a-1)*t*b+(a-1)^2*b^2-1.
```

The aggregate is

```
T = 7 + Tr(x(Q1)+x(Q2)+x(Q3)+x(Q4))/4.
```

It is positive on the stated point domain. All four roots, and therefore T, are fixed before comparison-prime selection. The aggregate uses p linearly, so no additional coordinate is needed for x(Q2).

## Exact rescaling and the R=0 stratum

For each retained old coordinate the compiler uses `x_old=R^e*z_new`, with the integer e recorded in `rescalingExponent`. For the new chart, the unscaled physical inverse Vieta coordinates u0,v0,w0,m0,r0,p0 satisfy

```
u0=u/R, v0=v/R, w0=w/R, m0=m/R, r0=r/R, p0=p,
r20=r2/R^2.
```

The old source comparison coordinates 35–38 become R times the delivered L2 and L2^0. The old scalar coordinates 107–108 are unchanged, and therefore continue to store the physical scalar quotient divided by R.

No spurious R=0 component is admitted by division of rows. The retained scalar contact equations give `r_beta=R*r_contact_stored`, where

```
beta=51*X^2+2504,
r_beta=beta*(beta-1)*(beta-2401)*(32*beta+343)>0.
```

Consequently R cannot vanish. The rescaled forced-prime equation gives `A*r_contact_stored=1+22201*r_beta`, so the stored contact coordinate and R are both positive. The other rescalings therefore give inverse rational substitutions on the entire zero set.

The independent checker reverses the Laurent rescaling for 182 rows, checks R2=R² literally, reconstructs the aggregate, verifies three generic chart identities, and independently expands every quadratic square. It does not import the producer.

## Reproduction

From the enclosing `circuits` directory run:

```
python build_affine200.py
python check_affine200.py
python build_inverse198.py
python check_inverse198.py
python balance_inverse198.py
python check_balanced198.py
```

The deterministic builders use the pinned source tables, the sparse arithmetic helpers from the pinned Brox source, and the saved integer weight certificates. The independent checkers require Python and SymPy; they import no producer. The optimization searches that discovered the weights are retained separately and need SciPy, but are not part of deterministic reconstruction.

The balanced presentation makes the further invertible change `z_unbalanced_i=C^e_i*z_balanced_i`; all e_i are explicitly listed in `balancing-weights.json`, with input weight zero. The balanced checker reconstructs every rescaled row and every expanded coefficient. Its exact coefficient inequalities prove the stated height formula. The only mixed coefficient profiles with opposite signs have even constant coefficient and odd C² coefficient; because C=149^N is odd, these cannot vanish. Thus the monomial count is fixed for every N>=1.
