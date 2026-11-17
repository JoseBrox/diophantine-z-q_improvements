# Six-contact Möbius obstruction

This exact certificate accompanies the manuscript
`negative_results/papers/pole_parameters/six_contact_mobius_obstruction_20261117_v62.tex`.

Run from this directory:

```sh
python check.py --output certificate.json
python check_independent.py --output independent_certificate.json
```

The only nonstandard dependency is SymPy. The checker exhausts all 120 possible
images of three roots, recovers the complete 12-element rational Möbius group,
and checks the multiplier identities. It proves the finite inequalities used
for the uniform square gaps, checks the two full congruence progressions by
exact rational arithmetic, and supplies a primality and finite-field point-order
certificate at 76253. The finite-field group computation uses direct integer
arithmetic, independently of SymPy's elliptic-curve functionality.

The second checker uses only Python's standard library. It reconstructs every
Möbius map by explicit fractional interpolation, verifies each rational identity
by polynomial coefficient multiplication, and checks the twenty uniform gaps
and two contact fixtures using their integer numerators.

The proof for arbitrary finite exceptional sets uses Chebotarev and the two
Eisenstein fields stated in the manuscript. The computation checks the field
input and local splitting data; it does not claim to verify infinitude by search.

This is an obstruction to the specified prescribed-index completeness route.
It is not a variable lower bound. Variable nonunit square rescalings, a different
height scale, and other contact systems are outside its scope.
