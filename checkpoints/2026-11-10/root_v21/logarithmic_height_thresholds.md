# Retaining logarithms in the contact-height bound

Status: proposed rigorous coefficient improvements; awaiting independent audit.
The polynomial families and variable counts do not change. All their retained arithmetic premises remain in force.

Start with the proved estimate h(q) <= C M_5(q)^2 (1+log M_5(q))^2, C < 2^221231.
If two contact blocks have disjoint support outside an exceptional product E, their radicals m_1,m_2 have product M. If their inverse height changes are at most log A, then

  h(t) <= log A + C E^2 M (1+log E+log M/2)^2.

Indeed multiply the two bounds for h(t)-log A and take a square root, then use (u+x)(u+y) <= (u+(x+y)/2)^2. This is valid also when h(t)<=log A.

## Explicit quartic with 265 coordinates

Here E=2029147<2^21 and A=7. Set K=2^221274. The bound becomes

  h(t) <= K M (22+log M/2)^2.

The existing three-scale argument gives, if M_j^k divides J != 0,

  B^2 <= 5 K |J|^(1/k) (22+log|J|/(2k))^2.

If Delta != 0, |Delta|<=14 B^4 and k=3 yield

  B^(2/3) < 13 K (23+2 log B/3)^2.

The quotient exp(2b/3)/(23+2b/3)^2 is increasing for b>=0. Put T=331969. Since log2<7/10, the exact integer inequality

  2^(2T-663822) * 15^6 > 13^3 * (345+7T)^6

excludes B>=2^T. The forced-prime exponent is L_N=floor(19(2N-1)/8)+1. For N=9682, L_N=45988 and

  149^45988 - 1 >= 2^331969.

Also 149^45988 > 40*2^221234 and >4640000. Therefore the existing scalar estimate gives h(beta)<c/40, with c>=149^45988 and B>=c-1. This forces Delta=0.

For a nonzero input residual J, |J|<=2 exp(h(beta)) B. Write b=log B and t=h(beta). The logarithmic transfer gives

  b <= log(10 K) + t + 2log(23+(b+t)/2).

Using log(1+x)<=x gives

  b <= (12/11)t + (23/22)log(5290 K) < 2t+232000 < c/10.

Here log(5290 K) <221287 and 23*221287<22*232000. The existing Lucas bound b>=c/2 is a contradiction. Thus the existing complete family defines the integers for every N>=9682.

New coefficient height at this member: 149^38730+1, exactly279599 binary digits (was419333). No degree or variable-count change.

## Explicit source with 27 coordinates

Here E_*<2^100 and A=35. Set K=2^221432. Then

  h(t_j) <= K M_j (101+log M_j/2)^2.

The existing three-scale proof and its scalar bound h(beta)<=c/120 give

  B^2 <= 2K |Nc|^(1/k)(101+log|Nc|/(2k))^2
         +30h(beta)+4Llog(76249)+340.

The final three terms are less than B^2/2 exactly as in the current proof, for c>=100. If Delta!=0, |Delta c|<=10B^5 and k=3 give

  B^(1/3) < 9K(102+5log B/6)^2.

Its left/right quotient is increasing in log B>=0. Put T=664417. The exact inequality

  2^(T-664296)*12^6 > 9^3*(1224+7T)^6

excludes B>=2^T, using log2<7/10. At the odd parameter L=20483,

  76249^(40967)-1 >= 2^664417,
  76249^40967 > 120*2^221470,
  76249^40967 > 10^6.

Thus the old scalar estimate applies with its old constant, and Delta=0 follows. Every larger odd L also works.

For nonzero input numerator N, |Nc|<=2exp(h(beta))Bc. Put b=logB and t=h(beta)+logc. After absorption,

  b <= log(8K)+t+2log(102+(b+t)/2)
    <= (103/101)t+(102/101)log(8K*102^2)
    < 2t+224000
    <= (31/60)c+224000 <c-4

for c>=10^6. The constant uses log(8K*102^2)<221449 and 102*221449<101*224000. This contradicts the existing Lucas inequality log B>c-4.

The exact 27-coordinate family is therefore certified at L=20483. Its coefficient-size recurrence must be rerun at that member before announcing a new coefficient bound. Degree and support bounds are uniform and unchanged.

## Checks still required

Independent audit of all exponents/constants and interface to existing proofs. Rebuild 27-coordinate coefficient fixture at L=20483 and certify coefficient bounds. Revise the leading explicit papers and metadata coherently only after this audit. Quartic reconstruction itself is unchanged: its fixed-parameter specialization becomes149^19365.
