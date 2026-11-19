# Fixed squarefree scalar anchor

## Replace the forced prime power

Write $\beta=51X^2+2504$ and $r=\beta(\beta-1)(\beta-2401)(32\beta+343)$. Let $A$ be the product of the 16 distinct primes

$$23,149,263,337,631,1063,1093,1171,1439,2161,2437,2837,2851,3187,3343,3793.$$

Replace the physical scalar normalizer by $R=Ar/(1+25r)$. For every rational input $X$, all $p\mid A$ satisfy $v_p(R)=1$. For $p$-integral $X$, the checker enumerates the entire residue field and verifies $r(X)(1+25r(X))\not\equiv0\pmod p$. For $v_p(X)<0$, the leading coefficient $32\cdot 51^4$ is a unit, so $v_p(r)=8v_p(X)<0$; then $v_p(1+25r)=v_p(r)$.

The scalar radical $M_S(\beta)$ in the cited theorem considers the four finite contacts $0,1,2401,-343/32$ and infinity, outside $S=\{2,3,5,7,11,13,17,37,41,2399\}$. The valuation at infinity is even, since any negative valuation of $\beta$ equals $2v_p(X)$. The finite contacts have pairwise differences supported on $2,3,5,7$. Hence a contributing prime has $v_p(r)$ positive and odd. None divides $A$ by the preceding computation. At such a prime $v_p(R)=v_p(r)$, since the denominator is a unit.

The unchanged scalar pole equations give, at a positive odd $\mu=v_p(R)$ outside $S$, $v_p(F)>7\mu/4$, for $F=\operatorname{Nm}(1/x(H))$, and then $v_p(a)>9\mu/4$ for the integral label $a$. The order of reasoning here matters: apply the first inequality at $149$ with $\mu=1$ before using point ratios. The allowed finite points with index $-1,0,1$ have reciprocal-abscissa norm a 149-adic unit, by the torsion-translate calculation of the [source](https://github.com/JoseBrox/diophantine-z-q_improvements/blob/d3a8c223716a0fc0dbf5af4eb7998d640c21048d/papers/quartic/quartic262_20261110_v21.tex). Indeed $\operatorname{Nm}(x(P)),\operatorname{Nm}(x(P)-d),\operatorname{Nm}(x(P)+d)$ are $41^2/64,17^2/64,63^2/64$, and $\operatorname{Nm}(d)=7$. This excludes the exceptional strata first. The unchanged good-reduction formal logarithm and label argument of the explicit theorem then applies at every consumed prime. Every $p\mid A$ contributes at least $p^3$ to $a$. Thus

$$
A^3 M_S(\beta)^3 \mid |a|,\qquad
A=645904574641049503754777843805872291231896003979>149^{22}.
$$

Consequently $|a|\ge149^{66} M_S(\beta)^3$. It follows that both numerical conclusions used in effective soundness hold, $\log|a|\ge66\log149$ and $h(\beta)<2^{238}149^{-66}|a|$. The integral Lucas and input-label comparisons of the explicit theorem apply word for word from these two bounds. In particular no new height estimate is assumed.

## Integer witnesses

If $X$ is an integer, $r\ge1$, so $R\ge A/26>2^{20}$. This is the same real neighborhood bound used in the original witness construction. With $D=1+25r$, one has $\gcd(D,Ar)=1$ by the finite checks and the identity $D-25r=1$. Thus $R(R+9792)$ has square reduced denominator. The checker finds $r\bmod16\in\{4,8,12\}$, $r\bmod3=1$ and $r\bmod17=13$ uniformly in integer $X$. The denominator is a unit at all three primes, and $A$ is also a unit at them. Since $9792=2^6\cdot3^2\cdot17$, the unit $1+9792/R$ lies in $1+8\mathbb Z_2$, $1+3\mathbb Z_3$ and $1+17\mathbb Z_{17}$, respectively. Therefore $R(R+9792)$ is locally square at all three places. The choices of the shared reference, scalar index, real neighborhoods, Lucas labels, prime progression and prepared pole witnesses in the explicit theorem use just these scalar properties and the actual finite odd-valuation support. The preparatory progression can include this support for each fixed integer input. The other three detector arguments and their contact sets are exactly those of that theorem.

## Transferring the physical scalar to the 180-coordinate hybrid

The pinned generic 180-coordinate table has SHA-256 1a4621da15c17eadcf914fb3d9294bb2b0f8301b814dc6c47d636eb9af9967a0. It has 180 coordinates and 152 rows. The three terms of its forced row are $1+22201x_{78}x_{90}-149C x_{78}$. Coordinate 163 stores the common contact weight $c$, with an explicit inverse. The recovered scalar identities of the pinned Laurent source are $r=x_{78}x_{90}$ and $R=Cx_{90}$. Equivalently $x_{78}=Cr/R$. The old relation is $1+149^2r=149C^2r/R$. For the present specialization use $C=U=401902039283859944994457$, and set $V=A/U=1607119425897843409348547$. In this row alone change 22201 to 25 and $-149C$ to $-V$. Its zero set gives exactly $1+25r=Ar/R$. Since $r>0$ for every rational input, the expression for $R$ has its indicated sign and all physical divisions here are legitimate.

The compiled physical gauge in `parameter-map.json` assigns coordinates 78, 90, 163 the exponents 1, −1, 0. Replacing every stored coordinate by $C$ to its listed power times a new coordinate removes $C$ from each of the other 151 equations, up to an invertible row factor. The checker verifies this directly, including the input with exponent zero. Thus modifying the split constant in the forced row and choosing $C=U$ changes only the physical scalar normalizer. The scalar-transfer audit in the hybrid package identifies the common scalar block with the source of the effective 229 theorem. The hybrid gate and shifted-aggregate argument establishes the remaining hypotheses of that theorem on the modified system.

To produce the final literal, apply the input-fixing diagonal map in `fixed-map.json`, multiply each row by a power of $U$ that clears denominators, then divide by the coefficient gcd. Each recorded elementary operation $(i,j,b,d)$ replaces $Q_i$ by the primitive row proportional to $dQ_i+bQ_j$, with $i\ne j$, $d>0$. Renumber the witness coordinates by their frequency in the quartic and apply the input-fixing integral shears, if provided. These are rational bijections on variables and invertible changes of row equations. The single integer polynomial is the sum of the 152 final squares. Run `python verify.py` to reconstruct it, verify the finite scalar arithmetic and gauges, compare two exact expansions, and measure the canonical literal with the upstream parser. No numerical optimizer is needed for verification.

## Running on another certified hybrid family

`anchor_generic.py` accepts the path and SHA-256 of a compatible generic coefficient table. Use a source whose arithmetic transfer has already been proved. The program independently derives the parameter gauge and checks that the forced scalar row has the expected three terms. Without a preset it specializes at $U=1,V=A$ and produces its own unoptimized literal. Passing this package as `--preset` reproduces the optimized fixed member byte for byte. Examples assume the shell is in this package and both output directories are new.

```sh
python anchor_generic.py source.json --sha256 1a4621da15c17eadcf914fb3d9294bb2b0f8301b814dc6c47d636eb9af9967a0 --out ordinary-build
python anchor_generic.py source.json --sha256 1a4621da15c17eadcf914fb3d9294bb2b0f8301b814dc6c47d636eb9af9967a0 --preset . --out optimized-build
```
