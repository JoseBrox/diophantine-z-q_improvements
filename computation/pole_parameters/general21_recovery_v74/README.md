# Coupled physical weights in the general 21-coordinate target

For the general actual-trace source, fixing its scalar `rho` and positive
comparison scale `a` gives two unnormalized physical weights

```
u0 = rho P(lambda)/(lambda+1)^10
u1 = rho P(a lambda-4)/(a lambda+2)^10,
```

where the ten roots of `P` are the original first contact set. The map from
the common slope to this weight pair is birational over the rationals for
every positive rational `a`. The normalized pair
`w_j=u_j/(1+u_j)^2` is also birational: the reciprocal substitutions do
not lose generic slope information. This is a structural lifting theorem, not a
completeness theorem for 21 variables.

The proof is in
`papers/pole_parameters/coupled_weight_lifting_20261117_v74.tex`.

Run:

```
python computation/pole_parameters/general21_recovery_v74/check.py
python computation/pole_parameters/general21_recovery_v74/check_independent.py
```

The first script checks the exact scale-two exception, positive algebraic
lift fixtures, a mismatched pair, and the reciprocal branches of normalized
weights. The second independently verifies the finite-field Bezout certificate
using integer lists without SymPy. These fixtures are not prepared elliptic
source tuples.

For an exact unnormalized candidate pair:

```
python computation/pole_parameters/general21_recovery_v74/check.py \
  --lift RHO SCALE U0 U1 --output candidate-lift.json
```

The program retains every rational root when the polynomial gcd has degree
larger than one. It never assumes that a rational point at a singular image
value lifts rationally. The contact poles are removed; every other source
guard, trace equation and preparation condition must still be checked.

For normalized weights, a direct pair of degree-20 polynomials gives the
same exact lifting test:

```
python computation/pole_parameters/general21_recovery_v74/check.py \
  --lift-normalized RHO SCALE W0 W1 --output normalized-lift.json
```

Alternatively solve `w_j u_j^2+(2w_j-1)u_j+w_j=0` first. There are
at most four rational reciprocal branch pairs, each subject to the degree-10
coupled gcd test. The direct method needs no assumed rational square root.
