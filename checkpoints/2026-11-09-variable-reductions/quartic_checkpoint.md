# Quartic checkpoint, 9 November 2026

Recovered 273-variable construction from research/checkpoints-2026-11-09 v14 and integrated into repo/computation/quartic/build_quartic273.py, check_quartic273.py, family273/*.json, and repo/papers/quartic_existence/quartic273_20261109_v14.tex. Both scripts run successfully.

Exact certificate: 273 total coordinates,247 primitive quadratic residuals, degree4,content1,3474 ordinary monomials (3475 parameter-separated terms). Quadratic SHA256 c2e2ad2838e79aa38c93bd41aa079d612826b5991c19835b88e14ec12fecc18b; polynomial SHA256 7e538c3d6714e5b699074a3e94243f5d84f38b19c216341360c1e62688ee69e5. Exact height H=max(C,A^2+1), C1520bits, A=80989^(2N+1); H=A^2+1 for N>=23. Arithmetic projection retains source hypotheses, and eventual sufficient N remains ineffective.

Investigating stronger contact amplification r>=10 to remove all formal-logarithm data. At r=10 exponent19/10<2 and formal order4 would prove Lucas exactness because4*(19/10)/4=1.9<2. Need exact coordinate accounting/contact polynomial evaluation/local packing before claiming improvement.

## New checked result: 272 total coordinates

The nonbase detector only needs F20, since its numerator power is computed separately. Every monic degree20 F has unique F=S10^2+R9. Three power coordinates t²,t⁴,t⁵ make all degrees0..10 quadratic expressions (basis exponents0,1,2,4,5), then one coordinate computesS10 and oneF. This is a five-coordinate sequential quadratic evaluation; four steps have degree≤16, so five is optimal in that precisely stated class. No division by variables and no exceptional input stratum. This saves the private V10 coordinate at detector1.

Integrated files: computation/quartic/build_quartic272.py, check_quartic272.py, family272/{quadratic-family272.json,polynomial-family272.json,construction-report272.json,independent-verification272.json}, papers/quartic_existence/quartic272_20261109_v15.tex, and updated computation/quartic/README.md.

Builder uses descending coefficients forS10; checker independently uses the truncated binomial series at infinity and reconstructs contact coefficients by finite differences. All246 rows, all272 variable incidences, and the entire sum of squares independently reconstructed. Exact degree4, content1,3450 monomials for all positiveA (3451 parameter-separated terms). Constant height1520bits; largest linear multiplier13118436242; H=80989^(4N+2)+1 exactly forN≥23. Arithmetic defining threshold remains ineffective; no stronger premise added. Quadratic SHA cb79a2ffc8f4309fbd64eb095c5bb77c2f35837102aeb0ef90b19465282fc174; quartic SHA d35396cacb98f60c1b0e7fe55c0ddeb107e021c26d358144a9a9b70453ed29a9.

Exploration limits: increasing contact blocks toremove Taylor corrections alone does not save their coordinates because their f²/f⁴ outputs already serve local factors. A seven-field-coordinate joint point chart fails on F=f (including bothidentity points), and a correct guard cancels its saving. A scalar guard cannot simply be removed: the a=1 branch collapses the needed growth bound. Torsion-shifting toavoid that branch changes local realization conditions and is not currently justified. These are no improvement claims.

## Independent thirteen-variable audit

Audit saved at /workspace/scratch/f7e003e8eb65/conditional13_independent_audit.md. Supported the additional-abc thirteen-variable family and contributed the sixth-power/order-one simplification (contactbound10/9 times scalarbound4/5 gives8/9). Sent minor CRT wording fix: h_* divisibleby16/64 mustbe explicit. Provisional conditional-quartic block accounting near110 is unverified and mustnotbe published as a numerical bound. Unsquared height scales neednew local-squareclass preparation andcannotbe substituted automatically.

## Current proved result: 267 total coordinates; prior normalization repaired

The literal affine source audit found that the old nonbase numerator chain did not compute its claimed expression. Its rows give395=a*t,396=a²(4t−1)²,397=a⁴(4t−1)^4,20100=a⁵t(4t−1)^4,20101=a¹⁰t²(4t−1)^8. Therefore F20(t)*e=a²⁰t⁴(4t−1)^16, not[a(t−1)]²⁰. This is an exact identity mismatch; no actual noninteger projection point is claimed. The former projection arguments for279/273/272 do not establish those tables' integer projections and are not retained as current theorems.

Correct normalization for degree20 contacts: R=F20(t)/(t−1)^22,e=(t−1)^20/F20(t),q=(t−1)^18/F20(t). Both detectors use the same triangular six-coordinate evaluation ofF20 andV10=(t−1)^10. Delete allfive nonbase scaled-numerator coordinates. Because the scale now enters only through t, take the positive linear scale T=one quarter ofTr(sum root abscissas), notits square; this deletes the separate scale-square coordinate. Finalcount267,241 quadraticrows,3422monomials(3423parameter-separated), degree4,content1, unchangedexactheight80989^(4N+2)+1 forN>=23. DefiningN threshold remainsineffective, underoriginalexplicit arithmeticpremises.

At any contact,delta isunitandvR=vFpositiveodd. The samefactorresidueproofextracts allrequiredtests. Atpreparedp, choosev(t)<<0; thenve0,vq=vR=−2vt. IdentityR=delta^-2 product(1+(1−theta)/delta) makesR a local square at2,3,17; sufficientdivisibilitygives depths. Prime identityR=a²⁰ product(selectedprimes)/(L²⁰delta²²) hasonlysquareextrafactors even for a nonsquarepositiverational scale. The generalprimepatternlemma permits arbitraryfixedintegercoefficients afterθ/a denominatorclearing. AtrealinfinityR~q~t^-2 andpoleinput~1/(4t²). TheheighttransferuseshT≤hλ+hTλ andC=2M1H4; onlyanineffectiveconstantchanges.

Currentfiles: computation/quartic/build_quartic267.py,check_quartic267.py,family267/*.json,papers/quartic_existence/quartic267_20261109_v15.tex,computation/quartic/README.md. Producer/checkerPASS. QuadraticSHA54c242476e796404131eb09099bd2c134adf2358e1129a112cd2b47f996ab6c7; polynomialSHAbc1f00a45bc05c72fba4fd1f117d2e7a6ec409d1c50cb9c1326794bf2ffbdf6b. Checker independently reconstructsallchangedandretainedrows,allnormalizationrowsatbothscales,thelineartrace,theentireSOS,andtheliteraloldmismatch. Theindependentmathauditbyfew_variables is/workspace/scratch/f7e003e8eb65/quartic267_independent_audit.md.

Superseded272and268code/tables/paperwere movedoutofpublicationinto/workspace/scratch/f7e003e8eb65/superseded_quartic_experiments. The273 coefficienttablesare necessarypinneddependenciesandretainexactbytes/hashes; theirbuilder/report/checkercertificatesnowexplicitlyclaimcoefficientchecks only. Root isremovingtheunsupported279projectionpaperandupdatingglobalmetadata.

## 2026-11-09 additional-abc quartic: 99-coordinate candidate

This is a new conditional construction, not yet claimed checked. Use the eight symmetric contacts Θ8={1±1,1±2,1±3,1±4}; put δ=t−1, r=δ², s=r², and F8=s²−30rs+273s−820r+576. Thus three quadratic coordinates compute F8 and δ⁸. A further simplification is F8*q=r*s and k=q*s, giving q=δ⁶/F8 and k=δ¹⁰/F8=1/R directly, without an intermediate e. It saves one coordinate per detector. If δ=0 then q=0, both packed factors are1, W=1, τ=1/2, and kb=τ² is impossible, so this chart excludes δ=0 automatically. F8=0 is also impossible.

The six order-one tests are f(H), f(U), σf(H−P), σf(U−A), C=L−σ(Lalt), I=L−β, with plain z ratios and β=2X²+B (odd fixed B). Pack T1=1+q C²+q² f(H)²+q⁴ f(U)⁴, T2=1+q I²+q² σf(H−P)²+q⁴ σf(U−A)⁴. At odd contact valuation ν>0, the three nonconstant term valuations have respective 2-adic orders0,1,2 because reciprocal-abscissa valuations are even. The source pole then extracts all six positive test valuations at one place. Formal logarithm precision4 suffices to show β≡n mod p.

Choose scales1 and a=β⁴+T⁴, where T is the single A trace. The abc contact inequality is h(t)≤(2/7)logM8+C using Granville epsilon1/4. The abc sum-of-fourth-powers inequality gives projective height H2=h(1:β:T)≤(3/2)h(a)+C (epsilon1/11). From both M8 dividing numerator N of β−n, get H2≤(6/7)logN+C. Since logN≤hβ+log(1+|n|)≤H2+log(1+|n|), H2≤6log(1+|n|)+C. The one-point elliptic trace bound n²≤A hT+J then bounds n and β uniformly independently of B. Any sufficiently large fixed B eliminates noninteger input solutions.

Completeness can use arbitrary positive rational scales because degree8 makes a⁸ a square in the prime numerator identity. Prepared local form R=δ^-2∏(1+(1−θ)/δ) and q~t^-2 is exactly as for267. The contacts include0 and exclude1; pairwise differences have only small prime divisors. The finite preparation set can retain all primes≤76176. Real R~q~t^-2, W→1, and b~1/(4t²).

A preliminary count is103 before removing e in both detectors and substituting the affine-rational formula for z(H−P) directly into the alternate ratio equations. Those two reductions target99 total coordinates. Exact builder and independent checker are being developed; do not publish99 until they pass and exceptional H-point strata are checked.
