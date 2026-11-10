# Independent audit of the logarithmic coefficient thresholds

The proposed thresholds `N=9682` for the explicit quartic and odd `L=20483` for the explicit 27-variable source are valid under the unchanged arithmetic premises. The audit checked the analytic inequalities against the current papers, not only the concluding integer comparisons. The exact independent arithmetic results are in `logarithmic_threshold_audit.json`.

## Amplification

For each of two contact blocks, the original radical is at most `E*m_i`, and the height loss is at most `log A`. If `h(t)>log A`, multiply the two bounds

`h(t)-log A <= C E^2 m_i^2 (1+log E+log m_i)^2`

and take a square root. Since `m_1*m_2=M`, the product of the two logarithmic factors is at most

`(1+log E+log M/2)^2`.

Thus

`h(t) <= log A + C E^2 M(1+log E+log M/2)^2`.

If `h(t)<=log A`, the same final inequality is immediate. No independence of the three detector radicals is used; only disjointness of the two blocks inside each detector is needed.

For the quartic, `C<2^221231`, `E<2^21`, `A=7` imply

`h(t) < 2^221274 M(22+log M/2)^2`.

For the 27-variable source, `E_*<2^100`, `A=35` similarly imply

`h(t_j) < 2^221432 M_j(101+log M_j/2)^2`.

The spare factor two in each constant absorbs the additive translation height even at `M=1`.

## Explicit quartic

The unchanged three-scale sum-height inequality is

`B^2 <= h(t_1)+h(t_2)+2h(t_0)+82`.

When `M_j^k|J!=0`, monotonicity gives

`B^2 <=5K |J|^(1/k)(22+log|J|/(2k))^2`, `K=2^221274`.

For `J=Delta`, `k=3`, and `|Delta|<=14B^4`, use `5*14^(1/3)<13` and `log14<6` to obtain

`B^(2/3)<13K(23+2log B/3)^2`.

The function `exp(2b/3)/(23+2b/3)^2` is increasing for `b>=0`: its logarithmic derivative is `2/3-(4/3)/(23+2b/3)>0`.

With `T=331969`, the exact integer inequality

`2^(2T-663822)*15^6 >13^3*(345+7T)^6`

implies the opposite strict inequality at `B=2^T`, using `log2<7/10`. Hence `B<2^T`. At `N=9682`, the unchanged local forcing gives `L_N=45988` and

`c>=149^45988`, `149^45988-1>=2^331969`,

a contradiction. The same parameter also gives `149^45988>40*2^221234`, so the old scalar estimate still yields `h(beta)<c/40`. There is no need to replace the scalar estimate by a logarithmic estimate.

For a nonzero input numerator `J`, use `|J|<=2exp(t)B`, with `t=h(beta)`, to get

`b<=log(10K)+t+2log(23+(b+t)/2)`.

The elementary inequality `log(1+x)<=x` gives

`b <=(12/11)t+(23/22)log(5290K)<2t+232000`.

Since `c>4640000` and `t<c/40`, this is less than `c/10`, contradicting the unchanged Lucas lower bound `b>=c/2`.

The coefficient formula remains `149^(4N+2)+1`. At `N=9682` this is `149^38730+1`, with exactly 279599 binary digits.

## Explicit 27-variable source

The unchanged scale-height calculation gives

`B^2 <=2K |Nc|^(1/k)(101+log|Nc|/(2k))^2 +30h(beta)+4Llog(ell)+340`,

where `K=2^221432`, `ell=76249`. Its hypotheses remain `M_j^3|Delta*c` for the Lucas residual and `M_j|N*c` for the input residual; shared prime support is retained.

At odd `L=20483`, the existing scalar argument gives

`c>=ell^40967>120*2^221470`, hence `h(beta)<=c/120`.

Also `4Llog ell<=2log c`. For `c>=100`, the additive terms are bounded by `c/4+2log c+340`, strictly less than `(c-1)^2/2<=B^2/2`. The previous absorption proof therefore applies unchanged.

If `Delta!=0`, use `|Delta*c|<=10B^5` and `4*10^(1/3)<9` to get

`B^(1/3)<9K(102+5log B/6)^2`.

The logarithmic derivative of `exp(b/3)/(102+5b/6)^2` is
`1/3-(5/3)/(102+5b/6)>0` for `b>=0`.

At `T=664417`, the exact inequality

`2^(T-664296)*12^6 >9^3*(1224+7T)^6`

excludes `B>=2^T`. But

`ell^40967-1>=2^664417`,

contradicting `B>=c-1`. Thus `Delta=0`.

For the input residual retain `c` separately and put `t=h(beta)+log c`. The absorbed inequality gives

`b<=log(8K)+t+2log(102+(b+t)/2)`

and hence

`b <=(103/101)t+(102/101)log(8K*102^2)<2t+224000`.

Using `h(beta)<=c/120` and `log c<=c/4`, valid here since `c>10^6`, yields

`b<(31/60)c+224000<c-4`.

This contradicts the existing Lucas inequality. Thus the smaller parameter proves soundness.

## Interfaces and remaining implementation work

All local point, pole, torsion-exclusion, and divisibility arguments are unchanged. Quartic completeness holds already for `N>=1`; the 27-variable construction uses arbitrary odd `L>=3`. Neither proof needs its old larger threshold for a separate arithmetic reason. The contact strata with radical one remain covered by the new inequalities.

The exact source degree and support estimates are uniform in the fixed parameters. Only the coefficient-height recurrence for the new 27-variable specialization must be rebuilt before a new coefficient-size bound is stated.
