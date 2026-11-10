# Independent proof audit: abc91 to abc89

**Result: PASS**, subject to the literal-interface checks in the accompanying standard-library checker. The construction preserves the rational projection onto the input and every unmodified elliptic and pole coordinate, with the identical pole input b. It requires no new arithmetic or completeness hypothesis.

## Zero-weight branch

The new equations are s4=s2^2 and s3^2=s2*s4. If s2=0, then s3=s4=0. Each factor equation then forces the square of its numerator reciprocal-square field coordinate to vanish. Since Q(sqrt(2)) is a field, both reciprocal-square coordinates vanish. The unchanged pair chart gives a I^2=a^2-D V^4 and I^2=a-D a R_U, hence V^4=a^2 R_U=0, and likewise Q^4=0 for the other numerator point. Thus V=Q=0, and VQ=a W_A with a nonzero gives W_A=0. The final pair-chart equation becomes 0=1. This proves s2 nonzero without using any local extraction, contact nonvanishing, or formal logarithm.

## Contact recovery and the final affine coordinates

The actual stored coordinates are R=r-1, U=u-1, V=v+29. Their equations are

R=delta^2-1, U=R^2+2R, (U-30R-V)s2=(R+1)s3, UV+V+244U-820R=0.

The inverse substitution r=R+1, u=U+1, v=V-29 is an everywhere-defined affine isomorphism. Expanding these equations gives exactly the unshifted contact equations used below. The last row loses its constant because P4(1)=0. If r=0 then R=U=-1, and its left hand side is still 576, independently of V. Thus the affine shift does not alter the nonzero boundary argument.

Put t=s3/s2. The two inverse-weight equations give t^2=s2, t^3=s3, t^4=s4. In particular t is nonzero. The new contact equations

u=r^2, (u-30r-v)s2=r s3, uv+273u-820r+576=0

give v=u-(30+t)r and

P4(r)=r^4-30r^3+273r^2-820r+576=t r^3.

If r=0 then u=0 and the final equation reads 576=0. Therefore r and P4(r) are nonzero. Recover q=1/t, c=r/t, k=r^2/t. The old contact equation is q^2 P4(r)=q r^3, and is now exact. The old inverse-weight equations q s4=s3 and q s3=s2 also hold. Thus no extra branch is introduced at any contact or pole of the rational weight.

## Factors, product, trace, and pole

The old factors satisfy s4 T_i=R_i, where R_i is the unchanged right hand side involving the comparison square and reciprocal tests. The new factors satisfy s3 A_i=R_i. Therefore A_i=t T_i. The new product equation (R+1)W=A_1 A_2, or equivalently rW=A_1 A_2, yields

W=(t^2/r) W_old.

The trace equation is w0^2-2w0 tau-2w1^2=0. It is homogeneous of degree two in all three coordinates. Set tau_old=(r/t^2) tau; together with W_old=(r/t^2) W, the old trace equation follows exactly. This reasoning remains valid even before excluding zero products or zero traces.

The new pole equation is s3 b=tau^2, that is t^3 b=tau^2. Consequently

k b=(r^2/t)(tau^2/t^3)=(r tau/t^2)^2=tau_old^2.

Every normalized pole-realization equation is unchanged, including its input b. Thus the local obstruction and all completeness witnesses transfer literally through this rational equivalence.

Conversely, the old zero-weight argument excludes q=0 and then r=0. Put t=1/q, u=r^2, v=r^2-(30+t)r, A_i=tT_i, W=(t^2/r)W_old, and tau=(t^2/r)tau_old. All new equations hold. These formulas are inverse to the reconstruction above, so the complete rational solution sets are in bijection after the stated repurposing of coordinates.

## Literal dependencies and degree

The removed old q coordinates are 30010 and 30032. The old r coordinates become R; the old c coordinates 30011 and 30033 become U; the old k coordinates 30012 and 30034 become V. The checker verifies that every occurrence of all these old coordinates is in a replaced or removed equation. Each scaled factor component occurs only in its factor and product equations. Each product component occurs only in its product and homogeneous trace equations. Each trace coordinate occurs only in the homogeneous trace and pole-input equations. All other 53 rows agree exactly, up to the common primitive row normalization.

Every replacement row is quadratic in retained coordinates. Squared comparison tests and squared reciprocal tests are already stored coordinates, so no hidden fourth-degree residual is introduced. There are 89 coordinates and 77 quadratic rows. The independent checker expands the entire sum of squares, verifies all literal coefficients, and certifies 936 ordinary monomials, degree four, content one, and coefficient height max(4153456,B^2+797681) for every positive integer B. For odd B at least 1833 the latter simplifies to B^2+797681. The final affine shift removes every absolute constant from the contact rows, reducing the constant coefficient by 2(576^2+1)=663554 relative to the unshifted 89-variable presentation. As in the inherited construction, an arbitrary small fixture value of B is not a certified defining parameter.
