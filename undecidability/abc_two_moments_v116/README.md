# Two moment tests replace the product of twelve selective gates

**417 variables, 364 quadratic residuals.** Same ordinary rational abc, group, trace-height, finite prime-pattern, pole and external Jones coding premises as [v115](../abc_unscaled_aggregate_v115/README.md). The sufficient coefficient remains ineffective. All twelve integer predicates remain.

For the retained good primes of v115, both contact arguments x,y are integral (the soundness proof discards denominator primes of M), and outside the fixed set of shift differences each of x,y can meet at most one linear contact factor. Thus among the twelve affine contact values F_i at most two have positive valuation. Their indices need not be known, and both can occur in the same group.

Keep exactly the first three equations of each v115 gate, namely Rgate_i=F_i D_i, Tgate_i=u+Rgate_i^2 and Vgate_i*Tgate_i=D_i^2. At a retained good prime v_p(u)=1 and v_p(F_i)=s>=0. As proved in v115, inactive s=0 gives v(Vgate_i)>=0, and active s>=1 gives v(Vgate_i)>=0 if and only if v(D_i)>=1. This includes D_i=0; no denominator zero occurs at such a prime.

Write V_i=Vgate_i, S0=sum_i V_i, S1=sum_i i V_i with indices i=1,...,12. Replace the whole product aggregation by

    A=S0^2,
    B=u*S1,
    Z=u*A+B^2,
    alpha=u+Z^2.

The unchanged tau and native-pole rows still give square reduced denominator of b=7c*tau^2. At v_p(u)=1, the odd valuation term u and even valuation term Z^2 imply alpha!=0 and v(alpha)>1/2. Hence Z has positive valuation. The summands u*S0^2 and u^2*S1^2 in Z have opposite parity, so each has positive valuation. This implies S0,S1 are integral. The only possibly nonintegral V_i are the at most two active ones. Subtract all inactive terms from the two integral sums. For one active index the first sum suffices; for two distinct indices i,j the coefficient matrix [[1,1],[i,j]] has determinant j-i, a p-adic unit after excluding primes <=12. Hence both active V_i are integral. Every retained R_i prime is still detected, and the v115 proof of input integrality applies unchanged. No assertion that distinct contact groups have disjoint reductions is made.

For completeness the v115 prime preparation gives v_p(u)=1 at a selected prime, with exactly one active contact and v(D_i)>0 there; every inactive V_i is integral automatically. Thus S0,S1 integral, Z positive in valuation, v(alpha)=1 and v(b)=1. At fixed prepared places the v115 asymptotics give V_i=O(z^-32), u~z^2/a, so Z tends to zero and alpha~u. All real and dyadic pole preparations remain the same. Negative odd valuations of u are still harmless since alpha=u+Z^2 has distinct valuation parities; even valuations give even b valuation away from the prepared prime seven. The unchanged BB-native theorem gives the remaining pole witness.

The exact table drops the twelve factor coordinates Wgate_i and eleven product coordinates, and introduces A,B,Z. It keeps 360 old rows and adds four, giving 417/364. Run node build.js. The builder verifies unchanged named monomials, absence of external occurrences, support and degrees, and 10,201 exact integer valuation pairs for the moment criterion. The two-column minor is the explicit integer j-i. These checks supplement the above proof and do not establish the inherited arithmetic inputs.