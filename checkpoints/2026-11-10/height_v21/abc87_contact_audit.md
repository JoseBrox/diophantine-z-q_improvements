# Independent arithmetic and all-strata audit of abc87

**Result: PASS.** The exact source uses a genuinely different contact polynomial. It is an exact quadratic encoding of the new-contact arithmetic construction, not a rational projection equivalence with the old abc89 construction and its different pole values. The new construction needs the same stated arithmetic inputs. Only fixed ineffective height constants and hence the sufficient defining shift may change.

## Contacts, height estimate, and exceptional primes

The contacts are Theta={-5,-2,-1,0,2,3,4,7}={1+-1,1+-2,1+-3,1+-6}. They are eight distinct integers, contain zero, and omit the pole at one. The nonzero differences have prime support exactly {2,3,5,7}; the nonzero distances from one have support {2,3}. Thus every prime p>76176 separates all contacts from each other and from the pole. The cutoff still excludes the unchanged elliptic bad primes and exceptional torsion-coordinate primes.

For a reduced rational x/y, y>0, the binary form G(x,y)=product_theta(x-theta*y) is integral, homogeneous of degree eight, and has no repeated factor. Granville Proposition 1 gives, under ordinary rational abc, rad(G)>=c max(|x|,y)^(11/2), after fixing epsilon=1/2 and absorbing bounded heights into c. The upper bound |G|<=C max(|x|,y)^8 and primewise inequality rad(G)^2<=|G|sf(G) therefore give sf(G)>=c' max(|x|,y)^3. Outside the cutoff, a prime divides at most one linear factor; a prime dividing y divides none. Hence its odd squarefree support is exactly the contact radical M(x/y), and the omitted primes have bounded product. It follows that h(t)<=log M(t)/3+C0. C0 changes with the contact set but is independent of input and shift B.

The comparison scale remains beta^4+T(n)^4. The separate height inequality h(1:beta:T)<=4h(beta^4+T^4)/3+C1 is unchanged. Combining two contact bounds still gives the crucial coefficient 8/9<1. The torsion exclusion and the final index-height contradiction therefore remain valid for all sufficiently large odd B. No numerical sufficient B was claimed, so changing C0 creates no gap in an explicit threshold.

Primary check: Granville's author manuscript, https://dms.umontreal.ca/~andrew/PDF/hyperelliptics.pdf, Section 2, Proposition 1 (PDF page 6), states the radical bound for an integral homogeneous form without repeated factors and coprime integer arguments. These are exactly the hypotheses verified above. The original publication is IMRN (2007), article rnm027, DOI 10.1093/imrn/rnm027.

## Rational contact circuit, including zero strata

Put delta=t-1 and r=delta^2. Then

P(r)=(r-1)(r-4)(r-9)(r-36)=r^4-50r^3+553r^2-1800r+1296.

The exact reciprocal identity is P(r)/r^2=(r+36/r)^2-50(r+36/r)+481. Store R=r-1 and Z=z-37. The rows

R=t^2-2t,
RZ+Z-R^2+35R=0,
(R+1)s=Z^2+24Z

are equivalent to r=delta^2, r(z-r)=36, and rs=z^2-50z+481. The middle equation immediately excludes r=0; at R=-1 its left side is -36. With s2=s^2 and s3=s*s2, if s=0 then both scalar weights vanish. The two factor equations force both numerator reciprocal-square field coordinates to vanish. The unchanged pair chart implies V=Q=W_A=0 and contradicts its last equation with constant one. Thus s is nonzero.

Consequently z=r+36/r, P(r)=s r^3 is nonzero, q=1/s=delta^6/F, and k=r^2/s=delta^10/F, with F=P(r). In particular contacts and the pole are excluded. All inverse coordinate formulas are unique on this domain.

The new factor equations are s3*A_i=s2^2+s3*C_i^2+s2*f_i^2+g_i^4. Dividing by s^4 recovers T_i=A_i/s=1+q*C_i^2+q^2*f_i^2+q^4*g_i^4. The stored product and trace give

W0=r*Omega/s^2=T1*T2, tau0=r*eta/s^2,
k*b=tau0^2, b=(F/delta^10)*tau0^2.

The trace identity is homogeneous, so this reconstruction is valid even before excluding zero products or traces. Conversely, for the new contact polynomial F, these formulas reconstruct every stored coordinate. The pole realization is unchanged and sees exactly this b.

## Local extraction

At a consumed contact prime p>76176, delta is a unit and exactly one factor of F has positive odd valuation nu. Thus v_p(F/delta^10)=nu and v(q)=-nu. For the unscaled packed factors, the three nonconstant terms have valuation classes odd, 2 modulo4, and4 modulo8, because the finite reciprocal abscissa valuations remain even. Their valuations are distinct from each other and from the constant term. The original trace inequality and pole obstruction therefore give a place where C,I and all four reciprocal tests have positive valuation; the reciprocal valuations are at least two. This argument is unchanged at split or inert primes and introduces no assumption that every contact prime was selected in the completeness construction.

## Prime-pattern completeness and denominator preparation

For a fixed integer input, both scales are fixed positive rationals. Apply the retained simultaneous prime-pattern theorem to the coefficients -theta/a after a fixed common-square denominator clearing. This is permitted for arbitrary finite rational coefficient lists by the retained arithmetic-dependencies paper, Lemma `lem:rational-contacts`. Repeated coefficients are removed; zero remains, so the slope numerator u is a selected prime. The Gaussian congruences and reduction-order conditions depend on that theorem, not on the previous numerical contact list. Enlarging the fixed avoidance set and the prime lower bound handles every scale denominator or coefficient difference. The same compatible congruence progression supplies the common elliptic index in the prepared real and finite neighborhoods.

At a selected contact prime, nu=1. The reciprocal tests have valuation at least2 and the comparison residuals at least4. The three nonconstant term valuations are therefore at least7,2,4. The unscaled reciprocal trace has residue one or two and is a unit; b has valuation1. The exact squareclass identity is still

F(a*lambda)/(a*lambda-1)^10 = a^8 product_theta(u-(theta/a)L1) / (L1^8 (a*lambda-1)^10).

Every prefactor or denominator has even valuation. Thus away from the selected prime numerators the pole input has even valuation, while at selected primes it has positive valuation1. The reduced denominator of b is square.

At each fixed preparation prime, the common denominator dilation makes v(t) arbitrarily negative before prime selection. Since all contacts are fixed integers,

R_contact=delta^-2 product_theta(1+(1-theta)/delta)

has valuation -2v(t), and the product approaches1. At2, ensure the product lies in1+8Z2; at3 and17, ensure it lies in1+pZp. Thus R_contact is a local square at all three places. The unscaled factors approach1, so tau0 approaches1/2. In particular v2(b)=-2v2(t)-2 and v_p(b)=-2v_p(t) for p=3,17 once preparation is deep enough. These exceed the required bounds3,1,2, respectively. This verifies squareclasses and depths; the rescaled stored quantities need satisfy no additional local preparation condition.

At the two real embeddings, on the fixed compact elliptic neighborhoods and for lambda tending to positive infinity, q and R_contact are asymptotic to t^-2, the unscaled factors and W0 approach1, and b is asymptotic to1/(4t^2). All factors are positive once the argument exceeds the largest contact7. Hence eventually 0<b<17 and the required denominators are nonzero. The same original pole-realization input applies. Only afterward are the stored scaled coordinates filled.

## Exact data audit

The accompanying standard-library checker independently verifies the contact polynomial and reciprocal identity, exceptional prime supports, all12 changed rows and2 deleted rows, all63 unchanged rows, every occurrence of removed/repurposed coordinates, and the complete sum-of-squares expansion. It certifies87 coordinates,75 quadratic rows,918 ordinary monomials,919 symbolic terms, degree4, content1, and coefficient height max(4153456,B^2+797681). The latter simplifies for odd B>=1833. These coefficient thresholds do not certify a sufficient defining shift.
