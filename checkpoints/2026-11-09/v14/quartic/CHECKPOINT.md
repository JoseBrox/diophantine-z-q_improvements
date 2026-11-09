# Quartic research checkpoint, 9 November2026

## Complete candidate under construction:273 variables

Two proved local/circuit changes to the certified279 source predict273 total variables and247 quadratic rows, without changing the global arithmetic premises or ineffective parameter scope.

### Residue classes and asymmetric completeness

Use5 factors:

T1=1+q23 C2²+q10 H²+q4 B1⁴.
T2=1+q23 G²+q2 A3²+q4 B0⁴.
T3=1+q23 I⁴+q A2²+q2 A4²+q4 B3⁴.
T4=1+q23 C3²+q10 C1⁴+q4 B4⁴.
T5=1+q23 C4²+q2 A1²+q4 B2⁴.

Here qj=q^j; H=f(H), A_i=f(U_i), B_i=conjugate f(V_i). The T3 first3 nonconstant terms have distinct nonzero residue classes mod4, since f-valuations are even and v(q) is odd. Its last term has class4 mod8. All other factors retain exact2-adic valuation classes0,1,2. The same one-place trace proof forces H order6, high comparison order12, C1 order3, all formal tests order1, and I order6. The stronger I order causes no completeness issue: I is the PRIMARY ratio minus its exact integer target and has order≥12 (indeed≥80 in the retained preparation). It does not share the weaker V1 approximation error. The global comparison n−beta still needs only min(C1,I)=3.

Only C1⁴,I⁴,B1⁴ need new shared field outputs:6 rational coordinates versus8. No factor usesq8. The source279 q5=q*q4, q10=q5², c*q23=q10² does not depend onq8, so delete both q8 gates. This gives275.

### Two simultaneous degree20 polynomial evaluations in6 coordinates

Let F=F4(t), V=(t−1)^10. Euclidean division gives F=V*S+R, degR≤9. Put a=coefficient of t9 in S−V; this fixed rational is nonzero for the20 contacts. Set U=(S−V)/a, monic of degree9. Then

F=V²+a U V+R, and V=tU+(V−tU), with deg(V−tU)≤9.

After t²,t³,t6 have been computed, every polynomial of degree≤9 is a quadratic polynomial in1,t,t²,t³,t6. Hence U needs1 coordinate, V needs1, and F needs1:6 total. The base numerator(t−1)^20 is V² automatically. All divisions are by fixed rational coefficients, never by witnesses. Each detector saves1 coordinate, giving273.

## Point-chart research

A7-field-coordinate joint chart for root abscissa and paired U,V was derived using reciprocal parameters r,g,J,k and f=r²,F=g², plus root square roota:
J²+D f²=1, k²+D F²=1, a(F−f)=r k+g J.
On F≠f this forces a²=x(U−V), saving1 field coordinate against the current8-coordinate joint root/auxiliary block. However F=f allows V=−U and leavesa arbitrary; r=g=0 is also spurious. The globally correct rationalized relation a(gJ−rk)=1+D fF has a positive nonzero right side, but is cubic and needs an extra field gate, cancelling the saving. No coordinate improvement is claimed from this unguarded chart. Seeking a shared guard or another quadratic presentation remains worthwhile.

## Narrow optimization screen

`search_residue_packing.py` tests specified residue classes up tomod32 and a fixed acyclic scalar-weight gate DAG, using known stronger completeness depths on primary U_i and I. Outputs are circuit candidates, not global lower bounds. It finds no improvement to322 for3–5 factors in that class;273 arises from the279 packing plus the separate contact polynomial circuit lemma.
