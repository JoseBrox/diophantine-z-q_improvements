# Research checkpoint — 9 November 2026

The verified V11 publication is on main at commit 29199c229008aa150373c1bacb9dea508802a43e. Fresh verification: all 27 stages passed. All counts include the input. Conditional projections and ineffective coefficient thresholds were preserved accurately.

## Source clarification: quantitative prime selection

Read Sun, arXiv:2610.20691v2, Proposition 5.1, Proposition 6.2 and Section 6.1 directly at https://arxiv.org/html/2610.20691v2. With the finite cutoff L fixed before the limiting parameter, the proof leaves weight at least c*N*T/(8*(log L)^(4k)) after all order-obstruction removals, T=tau(N)*sqrt(N), with tau decreasing sufficiently slowly. Thus the weighted premise retained separately in the quartic papers is a consequence of the precise estimates already used in Sun's proof, conditional only on accepting that cited theorem and its estimates. This is a dependency clarification, not a newly discovered proof of the source theorem. The matching upstream argument is the Version 9 separation subsection retained in work/upstream/quartic_v13.tex near line 19708, at current upstream blob 70483fe426792915a8ce66e6e44022607faa175d.

The elementary consequence allows w>=N^alpha for any fixed 1/4<alpha<1/2. The excluded strip has at most O(N^(1+alpha)) pairs, each weight O((log N)^k), so its total is o(N*T) after a slower diagonal choice. Hence distinct selected primes differ by at least c*N^(2alpha), larger than the Hasse error O(sqrt(N)); no selected prime divides another selected prime's opposite order. A selected prime cannot divide its own opposite order because that order is divisible by 4 and asymptotic to the prime.

## Denominator preparation for the new quartic candidate

For fixed rational scales a_i and fixed finite prime set S, take t_i=a_i*u/(D^2*w^2), with u prime outside S. Choose D with 2*v_p(D)>v_p(a_i) for all i,p in S. Then v_p(t_i)<0, hence v_p(t_i-1)=v_p(t_i)<0. This is compatible with Sun's fixed denominator dilation. Therefore replacing q_m by q_1^(2m-1)=q_m*(t_i-1)^(-6(m-1)) multiplies each local weight by an integral factor at every prepared prime. At consumed contact primes t_i-1 is a unit; at both real embeddings the new weights decay faster. Full q=0 degeneracy and source-row checks are being independently audited.

## Current candidates, not yet promoted

- Quartic researcher has a 297-variable existence family and a 342-variable explicit candidate using shared reciprocal powers. Exact tables, proofs and independent checks pending.
- Few-variable researcher has exact degree bounds below 2^151 and 2^157 at 27 and29 variables, and explicit coefficient bound below 2^(2^168). Independent coefficient checks and paper pending.
- Number-field transfer, descent, trace/norm and norm-image equivalences are proved in a separate draft with primary bibliography. No actual counterexample or general affirmative solution is claimed.
