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

## Inherited-premise 265-coordinate attempt: rejected completeness step

A tempting source change replaces all alternate Taylor-logarithm ratios by plain z ratios and raises the common alternate denominator test B0 to order12. The proposed packing was T2=1+q23*G²+q10*I⁴+q4*f(U3)⁴ and T3=1+q23*B0²+q*f(U2)²+q2*f(U4)²+q4*B3⁴, with all other factors unchanged. This deletes the two V0 truncated-log coordinates and V0's fourth-power pair, while adding U3's fourth-power pair, formally reaching265. Soundness's depth transfer works after integrality.

Independent review by few_variables identifies the fatal unproved completeness step: the retained primary H-depth≥3 requires h≡0 mod p², while the new alternate H−P-depth≥6 requires h≡1 mod p⁵. These conditions concern the same rational integer h and are incompatible. Arbitrary fixed congruences in the prime-selection premise do not remove this conflict. Therefore265 is NOT a theorem and must not replace267. A possible future repair would move logarithm corrections to the primary branch and deepen only the alternate branch; its coordinate budget and arithmetic realization remain open. The new abc99 construction asks only natural depth1 on both branches and is unaffected.

## abc99 finite certificate completed

Builder and independent checker: computation/quartic/build_quartic_abc99.py and check_quartic_abc99.py. Family directory family_abc99 contains99-coordinate87-row quadratic table, full quartic table, report and independent verification. Exactly881 ordinary monomials for every positive fixed shift B,883 separated parameter terms, degree4 and content1. Exact height for B≥3 is max(11600064,2B^4+833549), hence2B^4+833549 for oddB≥49. The common unit3+2sqrt2 in the compressed fixed-subtraction equation reduces the previous constant maximum294743232 to11600064 without changing any variables or roots.

Independent checker reconstructs all rows, the z(H−P) compression directly from pinned rows140/141 after replacing the truncation by1, the complete unordered-pair SOS expansion, height/support/content, and both scale-free normalizations. Quadratic SHA256 d3bdf480aec56eec938fa5b50e190e1f1c7fca022c9daae26cc3733a822e6414; quartic SHA2563a564c1aab43329ee04acc44cf0a1d6182d898a910b52474d607ab6769d33460. Few_variables additionally checked z(H−P)=N/D independently in the elliptic function field using PARI. Full arithmetic paper remains in preparation; no numerical defining B is asserted.

## Final quartic results, 2026-11-09 v16

Two fully certified current families now replace the prior candidates.

### Inherited arithmetic premises: 263 variables

Root proposed symmetrizing four affine images of the five source contacts, and the resulting construction has been implemented and independently audited. Set Θ={0,−1/2,−1,1/2399,−32/407} and Θ4=Θ∪(2−Θ)∪(Θ+5)∪(−3−Θ). Shift5 is essential for this chosen list; shift3 gives overlaps. The20 roots are distinct and symmetric about1. With r=(t−1)², F20(t)=P10(r), where P10(r)=∏θ∈Θ(r−(θ−1)²)(r−(θ+4)²).

Five quadratic outputs r,r²,r⁴,r⁵,F20 suffice because all integers0 through10 are sums of two members of{0,1,2,4,5}. The normalization F20*q=r⁴r⁵ and k=q*r² gives q=δ18/F20 and k=δ22/F20=1/R offδ0, eliminating the old e coordinate in each detector. The same16 local tests, five packed factors and original asymmetric formal depths remain, so no incompatible deeper CRT condition is introduced. Atδ0, q0 and the radical1 are harmless even though the inherited inverse-cube chain can leave q23 free; no reciprocal is used there.

The additional exceptional primes are exactly247957,368323,2029147. The four height maps2+1/t,2+1/(2−t),2+1/(t−5),2+1/(−3−t) have inverse matrix row-sum bounds3,7,14,8. Thus h(t)≤log14+H*(247957*368323*2029147)^19*M4(t)^(19/4). Fixed-place valuations, local squareclasses, positive linear trace scale and prime-pattern completeness are unchanged in form.

Files: computation/quartic/build_quartic263.py, check_quartic263.py, family263 tables/reports; papers/quartic_existence/quartic263_20261109_v16.tex. Counts263 total variables,237 quadratic residuals,3312 ordinary monomials,3313 separated parameter terms, degree4, content1. Exact coefficient height80989^(4N+2)+1 forN≥23; defining N remains sufficiently large and ineffective. Independent checker uses no producer and verifies everyrow/fullSOS, Newton interpolation, all20 roots, exceptional primes and four height matrices. Independent mathematical audit byfew_variables PASS; recurrence condition j≥2 explicitly restored. Quadratic SHA26876d3f9fa9a42478c4465edf36f9e8647df44ee2cc744df551300465fe58e3; quartic SHA4ac70724c340aa26440c0cdee1cae1445455bdf5fe702efa623037ec1a252f20.

### Additional rational abc: 98 variables

This supersedes99 and has no dependency on its files. Use six symmetric contactsΘ6={−2,−1,0,2,3,4}. For r=δ², F6=(r−1)(r−4)(r−9). Four scalar coordinates r,q,c,k satisfy r=δ²,c=qr,k=cr,kr−14k+49c−36q=r². Thus qF6=r² and k=qδ4=δ8/F6=1/R withR=F6/δ8, without storingF6. This removes one coordinate perdetector. AtF6=0 the normalization forcesr0 butF6(0)=−36; atδ0 it forcesq=c=k0,W1,τ1/2,kb0, contradiction. Thus all four quantitiesδ,F6,q,k are nonzero for every solution.

The comparison scale is a=β6+T6, evaluated in four quadratic coordinates s=β²+T²,p=βT,v=s²−3p²,a=sv. This adds one coordinate compared with the prior fourth-power scale, for a net reduction99→98. Granville epsilon1/4 gives h(t)≤(2/3)logM6+C0. Rational abc epsilon1/11 gives h(1:β:T)≤(2/5)h(β6+T6)+C1, C1=(7/30)log2+(11/30)logK_(1/11). The two scales therefore give H2≤(8/15)logN+C2, whereC2=(4/5)C0+C1 andN is the reduced numerator ofβ−n. Absorption gives H2≤(8/7)log(1+|n|)+(15/7)C2. The one-point trace bound then uniformly boundsn andβ unlessβ=n; choose sufficiently largeoddB inβ=2X²+B. All six tests remain order1, natural formal depth1 onboth conjugatebranches, with no CRT conflict.

Files: computation/quartic/build_quartic_abc98.py, check_quartic_abc98.py, family_abc98; paper papers/quartic_existence/quartic_abc98_20261109_v16.tex. Counts98 total variables,86 quadratic residuals,882 ordinary monomials,885 separated parameter terms, degree4, content1. Exact heightmax(11600064,2B4+169997) forintegerB≥3, hence2B4+169997 foroddB≥49. The three mixed profiles are2B4+169997,48B²+1,12B²−19; the last nevervanishes atintegerB. No numerical definingB is asserted.

Both few_variables and lower_bounds independently audited normalization, six-contact/pairheight constants, all exceptionalH strata and completeness. Full paper audit PASS. The H-exceptional exclusion includesh∈{−1,0,1} plus2torsion; evenness of storedF0 before interpretingH−P follows directlyfromfF0=g². The paired-point converse has an explicit Vieta/sign proof. Separate check_z_difference_identity.py usescypari2/PARI, imports no producer, and verifies9 exact identities in the elliptic function field; its report isfamily_abc98/z-difference-identity.json. Maincoefficient checker uses onlystandardlibrary and no producer. Quadratic SHA006eff7658ab3625c385d1ce684f4eca90c4bd46a1df5dfa34d990d08eeb7929; quartic SHA8d4c69fef8b61961ab537b6071ee20ae600568cedfa204583797ff1e2e9c566b.

Root is building finalPDFs, updating metadata/README/PROVENANCE/verify, removing superseded99newfiles and267paper from main, preserving the necessary267 coefficient dependency, and publishing. No more repo mutations byquartic agent unless a mathematical issue is found.
