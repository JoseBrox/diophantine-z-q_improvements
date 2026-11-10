# Final abc89 proof-transcription audit

**Result: PASS.** Audited paper:

`papers/quartic_existence/quartic_abc89_20261110_v21.tex`

SHA256 at audit: `127c1dc795b263e492cc19afaef2f42afc48467c6df5fb7328a076e7c8726db5`.

The stored shifted contact outputs r0,u0,v0 have exactly the formulas in the coefficient tables. The virtual expressions r=r0+1, r2=u0+1=r^2, xi=v0-29 undo the affine shift without colliding with the separate normalized-pole coordinates u,v. The virtual contact rows give P4(r)=s r^3 with s=s3/s2, and the zero-weight and r=0 exclusions are stated before division.

The paper clearly distinguishes stored A1,A2,Omega,eta from derived unscaled T1,T2,W0,tau0. Its domain lemma establishes, before local extraction,

T_i=A_i/s, W0=r Omega/s^2=T1 T2, tau0=r eta/s^2,

q=1/s=delta^6/F, k=q r^2=delta^10/F=1/R,

and k b=tau0^2, hence b=R tau0^2.

The homogeneous trace argument is valid before assuming factors, product components, or traces nonzero. The converse explicitly assumes r=delta^2 and qF=r^3 with rq nonzero, and reconstructs the unique stored values with the same pole input b.

Every local valuation argument uses the unscaled packed factors and W0,tau0. In particular ell=max_v v(W0)<=0 and v_p(b)<=nu+2ell apply to the same pole input as before. No inequality intended for the old product is applied to stored Omega. The original nonzero point, ratio-integrality, formal-logarithm, and height arguments are unchanged.

Completeness prepares the unscaled product W0: its reciprocal trace has residue one or two at selected contact primes, approaches two at fixed preparation primes, and W0 approaches one on the fixed real neighborhoods. The pole input remains b=R/Tr(W0^{-1})^2. Only after the original pole witness is obtained does the domain lemma fill the stored scaled factors, product, and trace. Thus the large real or local values of Omega and eta cause no new preparation requirement. The comparison scales, fixed elliptic curve and points, prime-pattern input, and local depths are unchanged.

The displayed census and coefficient statements match the independently reconstructed tables: 89 variables, 77 quadratic rows, 936 ordinary monomials, 937 terms with parameter powers separated, and height max(4153456,B^2+797681), reducing to B^2+797681 for odd B>=1833. The literal coefficient of the fourth power of the rational component h0 is one, as claimed. No superseded count, product definition, inverse-weight equation, or coefficient offset survives in the current proof. Labels are unique and references are defined.
