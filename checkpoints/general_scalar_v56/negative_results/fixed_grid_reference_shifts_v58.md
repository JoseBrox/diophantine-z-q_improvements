# Fixed linear reference shifts in the retained Lucas grid

The retained general point indices, including the fixed base point,
are

\[
1,n,s,t,b,h,nh,sh,th,bh.
\]

Here `n` is the input comparison index, `(s,t,b)` is an integer
squared-Lucas triple, and `h` is the auxiliary index chosen after the
contact primes. This note identifies which adaptive reference pairs
can be formed from these points by fixed integer group operations
while retaining the existing flexible preparation family. It does
not address a new family in which the root and auxiliary indices are
coupled arithmetically.

## An adaptive shift and its cost

If one had separate reference points `[m]P` and `[mn]P`, the usual
comparison ratios could use the denominators with indices `h` and
`h-m`. The equality of the two formal ratios has residual

\[
u(h-m)-h(u-mn)=m(nh-u).
\]

At a contact prime not dividing `m`, the same local extraction
therefore applies. The reduction-order congruences

\[
h\equiv0\pmod{r_+},\qquad h\equiv m\pmod{r_-}
\]

are compatible exactly when `gcd(r_+,r_-)` divides `m`.
Thus an adaptive nonzero `m` can remove that compatibility
obstruction when it is allowed to contain the relevant gcds and
remain a unit at the contact primes. This observation by itself
does not provide the two reference points at the existing coordinate
count, nor all of the other simultaneous congruences.

## Classification within the existing grid

Suppose `m` and `m'` are fixed integer-linear combinations of the ten
indices displayed above. Assume that, for each `n` in an infinite
set, the identity `m'=n*m` holds on a family with the following two
properties:

1. the squared-Lucas triples have unbounded `s`;
2. for every such triple, infinitely many values of `h` remain
   available.

The no-affine-relation lemma proved in
`finite_lucas_point_reconstruction_v58.tex` says that an unbounded
family of squared-Lucas triples cannot lie in a fixed proper affine
hyperplane. The equality `m'-n*m=0` has the form

\[
L_0(s,t,b;n)+hL_1(s,t,b;n)=0,
\]

where each `L_i` is affine in the three root indices. Infinitely
many `h` first make both `L_i` vanish. Unbounded root indices then
make all their coefficients vanish. Finally the infinite set of
input indices makes these coefficient polynomials in `n` vanish
identically. Direct coefficient comparison gives exactly

\[
 m=a+ch,\qquad m'=an+cnh,
\]

for fixed integers `a,c`. In particular, root roles alone supply
only a fixed constant shift and its input multiple. The auxiliary
row supplies only affine combinations of the original two rows.

This conclusion requires retention of the two stated freedoms. It
does not exclude selecting only a special coupled root/auxiliary
tuple for each input, or changing the preparation order and prime
theorem.

## Fixed row recombinations retain a fixed gcd obstruction

Consider any two denominator rows and their corresponding numerator
rows obtained from the original points:

\[
H_1=a+bh,\quad H_2=c+dh,\qquad
U_1=an+bu,\quad U_2=cn+du.
\]

Their comparison numerator is

\[
U_1H_2-U_2H_1=(ad-bc)(nh-u).
\]

If `ad-bc=0`, this cross comparison is identically zero and supplies
no information about the input-index residual. Otherwise it retains
a fixed nonzero determinant `Delta=ad-bc`.

The desired reduction conditions require

\[
r_+\mid a+bh,\qquad r_-\mid c+dh.
\]

Writing `g=gcd(r_+,r_-)` and taking the linear combination with
coefficients `d,-b` gives `g|Delta`. Thus fixed row recombinations
can absorb only divisors of one fixed integer. They do not remove
the need to control the conjugate self-order gcds uniformly.

The exact coefficient classification and determinant identities are
checked by `check_fixed_grid_reference_shifts_v58.py`; the output is
`fixed_grid_reference_shifts_v58_certificate.json`.

**Scope.** These results concern fixed integer group operations on
the retained nine-point grid and the existing preparation freedom.
They give no lower bound on the number of variables in a different
source and do not obstruct a new arithmetic coupling of the indices.
