# Effectivity checkpoint for the 163-variable Busy Beaver quartic

**Status: conditional quantitative lemma proved; no numerical Busy Beaver
index certified.** This note refines the threshold analysis of
[the v82 163-variable quartic](../papers/quartic/scalar_point163_179_20261120_v82.tex)
and the [v84 Busy Beaver specification](busy_beaver_and_expanded_sizes_20261120_v84.md).
It does not change any polynomial coefficients, variables, arithmetic
hypotheses or existing result records.

## The precise residual constants

Let \(F_N\) be the 163-variable polynomial with \(C=149^N\), and
write
\[
L_N=\left\lfloor\frac{9(2N-1)}4\right\rfloor+1,\quad
T_N=149^{L_N},\quad
B_0=\max(1,|n|,|a|,|t|,|b|),\quad\tau_\beta=h(\beta).
\]
The complete v82 argument obtains, for every putative rational zero
and every \(N\ge1\), the following inequalities with constants
independent of \(N\), the input and the point indices:
\[
B_0\ge |a|\ge T_N,\qquad
\tau_\beta\le K_0T_N^{-1}|a|,
\tag{1}
\]
\[
h(R)\le4\tau_\beta+(2N+1)\log149+\log1801500.
\tag{2}
\]
After incorporating the fixed contact-height and weighted-trace
constants, its two soundness stages have the form
\[
\begin{aligned}
B_0^2 &\le C_1|a\Delta|^{7/18}
                  +A h(R)+D_\Delta
                    &&(\Delta\ne0),\\
B_0^2 &\le C_4 B_0^{7/6}\exp(7\tau_\beta/6)
                  +A h(R)+D_X
                    &&(\Delta=0,\ J_X\ne0).
\end{aligned}
\tag{3}
\]
Here \(|a\Delta|\le14B_0^5\); the \(D_\Delta,D_X\)
are nonnegative fixed additive constants, enlarged if needed to
absorb the weighted-height additive constant \(J\). The source
proof uses the second inequality after the same scalar-height
absorption. Assume all constants in (1)--(3) have the signs shown.

**Quantitative lemma.** If a *proved explicit integer* \(M\ge2\)
satisfies
\[
A,\ K_0,\ C_1,\ C_4,\ D_\Delta,\ D_X\le M,
\tag{4}
\]
then every \(F_N\) with
\[
\boxed{N\ge N_M:=\max\{3,M\}}
\tag{5}
\]
has only integral rational inputs, under the original arithmetic
premises. Since the original integer-completeness argument holds
for every \(N\ge1\), each of these \(F_N\) defines
\(\mathbb Z\subseteq\mathbb Q\). Consequently
\[
\boxed{t=N_M}
\tag{6}
\]
is a sufficient **numerical** Busy Beaver index whenever (4) has
actually been established numerically: \(BB(t)\ge t\) gives
\(F^{BB}_t=F_{BB(t)}\).

**Proof.** For \(N\ge N_M\) we have
\(L_N\ge4N-1\), \(M\le N\), and \(N\ge3\).
Using \(\log149<6\) and \(\log1801500<15\),
(1)--(2) imply
\[
\begin{aligned}
\frac{Ah(R)+\max(D_\Delta,D_X)}{B_0^2}
&\le\frac{
4AK_0+A((2N+1)\log149+\log1801500)
+\max(D_\Delta,D_X)}{T_N^2}\\
&\le\frac{4M^2+12MN+22M}{T_N^2}\\
&\le\frac{16N^2+22N}{149^{8N-2}}<\frac12 .
\end{aligned}
\tag{7}
\]
The last inequality follows from
\(149^{8N-2}>47N^2\) for \(N\ge3\).

If \(\Delta\ne0\), the first inequality (3) and (7) give
\[
\frac{B_0^2}{2}\le C_1 14^{7/18} B_0^{35/18},
\quad\text{hence}\quad
B_0\le(2C_1)^{18}14^7\le(2M)^{18}14^7.
\tag{8}
\]
But \(B_0\ge T_N\ge149^{4N-1}\), and
\[
149^{4N-1}>(2N)^{18}14^7\ge(2M)^{18}14^7
\quad(N\ge3).
\tag{9}
\]
For (9), the base case is the exact integer inequality
\[
149^{11}=803616698647447868139149
>6^{18}14^7=10705790898505896689664.
\]
The ratio of successive left/right sides increases since
\(149^4(3/4)^{18}>1\). Thus \(\Delta=0\).

If \(J_X\ne0\), the second inequality (3) and (7) give
\[
\log B_0\le \frac75\tau_\beta+
            \frac65\log(2C_4)
\le \frac{7M}{5T_N}|a|+\frac65\log^+(2M)
\le 2|a|,
\tag{10}
\]
because \(T_N>100\), \(T_N>7M/5\),
and \(T_N>(6/5)\log(2M)\). On the other hand
the unchanged Lucas inequality in the v82 manuscript gives
\[
\log B_0\ge(|a|-6)\log(|a|-3)>2|a|
\quad(|a|\ge T_N>100),
\]
contradicting (10). Therefore \(J_X=0\), and the
remaining half-integrality and squarefree-denominator descent in
v82 gives \(X\in\mathbb Z\). This proves the lemma. \(\square\)

## What is, and is not, effective

The bound \(N_M=\max(3,M)\) is rigorous **conditional on
the actual upper bounds (4)**. It improves the cruder
\(10M\) criterion and is checked by
[an independent integer-inequality gate](../scripts/verify_v85.py).

However, no explicit numerical \(M\) satisfying (4) is supplied by
the published arguments. The crucial input is the uniform weighted
elliptic-height theorem
\[
B_0^2\le A(h(R)+h(T))+J
\]
deduced from Jérôme von Buhren, *Borne de hauteur semi-effective
pour le problème de Mordell--Lang dans une variété abélienne*,
J. Théorie des Nombres de Bordeaux **29** (2017), 307--320,
Theorem 1.1, https://doi.org/10.5802/jtnb.981.
Its additive constant is **ineffective** in the application.
The constants \(D_\Delta,D_X\) may depend on it.

Therefore **no literal numeral**—including
\(3\), \(10^6\), \(2^{1000}\), or an arbitrarily longer decimal
integer—has been proved sufficient for \(t\) on the strength of
the current arithmetic hypotheses. A statement such as
“if \(M\le10^6\), then \(t=10^6\) works” is valid, but its
antecedent is presently unproved.

## Why Busy Beaver growth alone cannot repair this gap

**Computability lemma.** There is no total computable rule \(g\)
which, from an index \(e\) of an ordinary Turing program enumerating
a **finite** computably enumerable set \(W_e\), is always guaranteed
to produce a standard Busy Beaver argument satisfying
\(\max W_e\le BB(g(e))\).

**Proof.** If such \(g\) existed, Kleene's recursion theorem
would give an index \(e\) for the following enumerator. It computes
\(q=g(e)\) and dovetails every blank-tape machine having at most
\(q\) states. Whenever a simulated machine halts at time \(s\),
it enumerates \(s+1\). Only finitely many machines were simulated,
so the resulting set is finite (and, for the usual machine
convention, nonempty). Its largest member is
\(BB(q)+1>BB(g(e))\), a contradiction. \(\square\)

This shows that mere proof of eventual absence of recursively
enumerable counterexamples does **not** yield a uniform numerical
cutoff by choosing a huge Busy Beaver index from the enumerator's
description. It does **not** show that an effective height estimate
for this particular 163-variable family is impossible.

The v84 Busy Beaver **oracle** procedure for a successful index
remains valid and separate: it computes such an index relative to
an oracle, not as an evaluated natural-number numeral.

## Reproducibility

```sh
python -B scripts/verify_v85.py
```

The verifier checks the exact base-case and growth inequalities,
the uniform scalar-error absorption surrogates, representative
integer parameters, source text anchors and the separation
between an effective conditional formula and the missing
numerical height-constant bounds. Its finite tests do not
establish the full universal arithmetic theorem or provide
an actual value of \(M\).
