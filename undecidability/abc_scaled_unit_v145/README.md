# v145: move the unit test into the scaled pole (ordinary abc)

Under the unchanged ordinary rational abc and other premises of v130, the quartic system has **291 variables and 240 quadratic residuals**, with twelve certified integer source coordinates. This saves one variable and row. It transfers the parity-tag compression principle rather than the entire general-route private chart, which uses a different scalar amplifier.

Write s=Tr(h_U), t=s+s^(-1); t² is already stored. In the notation of v130 the old nested selector was
R=c f_U+c² f_H²+conj(f_HP)², A=R²+ut², V=A²+c(C0-mu)²,
with c=1/u, D=Nm(V)/Tr(V), Z0=D²+cJ², Z=Z0²+c var² and alpha=u+Z². The tau equation is tau(1+alpha)=alpha.

Delete the field A and define V=R²+c(C0-mu)² directly. Store t^4=(t²)² instead. Keep Z0; use a scaled register Z'=cZ and a scaled alpha'=c² alpha_phys:
u Z'=Z0²+c var²,
alpha'=c+(Z')²+u t^4,
tau(c²+alpha')=alpha'.
Here alpha_phys=u+Z²+u³t^4. The c² register already exists. The resulting equations are quadratic.

At a retained prime v(u)=1. Positivity of v(V) now detects the three old formal conditions and the primary ratio, with the same uniqueness of the successful slot and impossibility at inert primes. The new unit term u³t^4 has odd valuation, at least 3 when s is a unit and at most -1 otherwise (v(t)=-|v(s)| if s is not a unit). Thus if alpha_phys has positive valuation, as the native obstruction requires, s must be a unit: the negative odd term cannot cancel with u or Z². The parity of the remaining terms then forces v(Z)>0, and the unchanged nested rational tests give positive v(D), v(J), v(var). The harmonic argument recovers the unique passing slot and the original unit condition, as U is formal there. The old private soundness and interpolation conclusions follow in the original order, without assuming private failure integrality in advance.

At a selected prime all these conditions hold, so alpha_phys has valuation exactly one. At a nonselected negative odd valuation v(u)=n<0, the valuations of u and u³t^4 differ by 2n+4v(t), which is 2 modulo 4; thus the odd terms cannot cancel, and neither can the even term Z² cancel their minimum. Hence alpha_phys has negative valuation, tau is a unit, and the old negative-odd normalizer still works. Even valuations and exceptional fixed places retain the original preparation.

For the real and prescribed fixed-place limits, c tends to zero and u to infinity. V tends to conj(f_HP)^4. This is nonzero and has nonzero trace, since both real embeddings of the fourth power are positive. Choose the old preliminary point neighborhoods so the harmonic quotient stays bounded; this is an open nonvanishing condition at the actual initial reference point. Then Z0 and Z stay bounded, and t is nonzero and bounded away from zero in the prepared neighborhoods. Hence alpha_phys is asymptotic to u³t^4, tau tends to one, and the old BB pole preparation holds. The same scalar-height and simultaneous preparation proof of v130 applies.

The exact sparse builder and instantiated coefficient table are committed. The named-row audit checks 234 unchanged rows and all degree, support, and census conditions. The count is 292-2+1=291 variables, 241-2+1=240 residuals. This does not establish a joint small/third Pell congruence or change the twelve-integer source, and is not an unconditional undecidability result.
