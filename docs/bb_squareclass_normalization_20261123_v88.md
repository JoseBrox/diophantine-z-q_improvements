# Balanced squareclass normalization: finite computational search

23 November 2026. The exploratory search used the materialized v88 general sources
read-only and wrote all candidates in this directory. It changes only
the normalization of the two or three terminal BB product blocks.

## Certified result

| Route | Variables, including input | Degree upper bound | Guard degree | Support exponent | Coefficient-height exponent |
|---|---:|---:|---:|---:|---:|
| General | 25 | 48,318,382,080 | 8,215 | 793 | 43 |
| Explicit | 27 | 183,368,679,424 | 14,398 | 906 | 45 |

The last column means the coefficient bound has the form
`2^(2^exponent)` in the existing convention. The sources retain the
same fixed scalar parameter and all earlier arithmetic hypotheses.

The independent verifier in `computation/bhargava_burungale_v88/check_degrees.py` is the existing v88
`check_degrees.py` with only its final expected-degree assertion updated.
It imports no new producer. It reconstructs every scalar, detector,
BB product, squareclass identity, operator majorant, guard receipt,
separator, determinant degree, support bound and coefficient bound.
The successful complete report is `computation/bhargava_burungale_v88/independent_degrees.json`.
The ordinary-abc eleven-variable route remains at degree 3,261,569.

## Exact change

Write the old extraction as `b=d_0 t_0^2`. For any nonzero product
`M` of factors already occurring in `d_0`, put

\[
d=d_0M^2,\qquad t=t_0/M.
\]

Then `b=d t^2` exactly. The two product-pole charts are isomorphic:

\[
(v,s,Y)_{\rm new}=(Mv,Ms,M^4Y)_{\rm old}.
\]

All factors used in `M` already have the required nonvanishing on the
guarded source. The computed final guard sets and degrees do not change.
The transformation preserves existence, zero terminal ordinates, and
finite-guard density. It changes neither the number of retained
parameters nor the finite-algebra rank.

For the current exact DAG, the odd squareclass has numerator one.
Its denominator has 14 nonconstant factors in the order returned by
`Circuit.factors`: four scalar factors of degree two, then ten contact
factors. The contact factors have degree one for `detector0` and degree
13 for the later detectors. Constants are left in the denominator.

For `detector0`, let `M` be the product of the first two scalar factors
and the first six contact factors. For every later detector, use the
first three scalar factors and first five contact factors. A direct
patch after `d, t = self.split_square(b)` is:

```python
candidates = [node for node in self.c.factors(d.d)
              if self.c.bounds[node][0] > 0]
assert d.n == self.c.one
assert len(candidates) == 14
assert [self.c.bounds[node][0] for node in candidates[:4]] == [2]*4
contact_degree = 1 if label == 'detector0' else 13
assert [self.c.bounds[node][0] for node in candidates[4:]] == [contact_degree]*10
ns, nc = (2, 6) if label == 'detector0' else (3, 5)
selected = candidates[:ns] + candidates[4:4+nc]
M = type(d)(self.c,
            self.c.from_factors({node: 1 for node in selected}),
            self.c.one)
d, t = d*M**2, t/M
```

The exact resulting native sources and compiler receipts are under
`computation/bhargava_burungale_v88/bb_general/general25` and `computation/bhargava_burungale_v88/bb_general/explicit27`.

### Ordered factor identity for the manuscript

Set `A=beta(beta-1)`, `B=(beta-2401)(32 beta+343)`, and let
`a_j=N_j/D_j` be the exact rational circuit for the j-th detector's
scaled slope. Thus `D_0=1`; for the later detectors,
`D_j=(B+7T A)^2`, with the numerator inherited from the unchanged
comparison scale. Use the ordered contacts

\[
\theta_{j,\ell}=4j+2+\theta_\ell\quad(1\le\ell\le5),\qquad
\theta_{j,5+\ell}=4j+4+\theta_\ell,
\]

\[
(\theta_1,\ldots,\theta_5)=(0,-1/2,-1,1/2399,-32/407).
\]

If `theta_{j,l}=a/b` in lowest terms, `b>0`, define
`L_{j,l}=b N_j-a D_j`. These are exactly the ten nonconstant
contact factors returned by the circuit in that order. Direct replay
of the source verifies

\[
d_{j,\mathrm{old}}^{-1}
 =C_j A B\prod_{\ell=1}^{10}L_{j,\ell},
\]

where

\[
C_j=7\cdot67\cdot102^2=4\,879\,476\quad(j\ge1),
\]

\[
C_0=C_1(2\cdot2399\cdot407)^2
 =18\,607\,262\,822\,027\,698\,896.
\]

The selected normalization can consequently be written without
reference to node ordering:

\[
d_{0,\mathrm{new}}
 =\frac{A\prod_{\ell=1}^{6}L_{0,\ell}}
        {C_0 B\prod_{\ell=7}^{10}L_{0,\ell}},
\]

\[
d_{j,\mathrm{new}}
 =\frac{A(\beta-2401)\prod_{\ell=1}^{5}L_{j,\ell}}
        {C_j(32\beta+343)\prod_{\ell=6}^{10}L_{j,\ell}}
 \qquad(j\ge1).
\]

Here `M_0=A product_{l=1}^6 L_{0,l}` and
`M_j=A(beta-2401) product_{l=1}^5 L_{j,l}`; replacing
`t_j` by `t_j/M_j` keeps `b_j=d_j t_j^2` exactly.
The polynomial degree pairs for numerator and denominator are `(10,8)`
and `(71,67)`, respectively. These are degree majorants of the
specified coefficient circuits, which is the convention used by the
finite-algebra compiler.

The general25 projective receipt has numerator and denominator degree
37,864, and guard degree 8,215. Therefore

\[
2^{20}\max(37864,1+8215+37864)=48\,318\,382\,080.
\]

The explicit27 receipt has separator degree 73,038 and guard degree
14,398. Therefore

\[
2^{21}(1+14398+73038)=183\,368\,679\,424.
\]

Their exact `log2_l1` majorants are 6,235,064,631,296 and
28,636,742,680,576, respectively. The terminal root/envelope degree
pairs are `(4485,4486)` for detector0 and `(24315,24316)` for the
later detectors.

## Search scope

The initial menu tested every prefix of the 14 nonconstant factors,
all factors including constants, contact factors only, and alternating
nonconstant factors, for both routes: 18 menus per route. A second
search tested all 55 choices consisting of the first `a` scalar
factors and first `b` contact factors, where `0<=a<=4` and
`0<=b<=10`, on the general route. Its individual pole bounds permit
the two different choices above. The final combined choice was then
compiled and independently verified for both routes.

Results are recorded in `computation/bhargava_burungale_v88/general_menu_results.json` and `computation/bhargava_burungale_v88/general_grid_results.json`.
The scratch discovery generator accepted these menus through
`ZQ_FACTOR_MENU`, with comma-separated entries for successive poles.
The final commands used `2_6,3_5` for general25 and `2_6,3_5,3_5`
for explicit27.

This is a finite optimization of a fixed compiler and factor menu.
No global minimality assertion is made, and no new variable reduction
is claimed.
