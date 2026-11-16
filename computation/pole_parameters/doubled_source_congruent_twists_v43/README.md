# Doubled source points on congruent-number twists

Run from the repository root with Python and SymPy:

```sh
python computation/pole_parameters/doubled_source_congruent_twists_v43/verify.py
```

To regenerate the saved certificate:

```sh
python computation/pole_parameters/doubled_source_congruent_twists_v43/verify.py --output computation/pole_parameters/doubled_source_congruent_twists_v43/certificate.json
```

The checker verifies the three duplication square identities and the
rational norm formulas symbolically. It checks the resulting point on
the congruent-number twist and verifies the exact fixture
`P=2(1+sqrt(2),2sqrt(2))`, including the signed norm `b=-1071/64`.

The paper proves the source nonzero conditions and the positivity that
make the construction valid for every nonzero doubled source point.
The target abscissa has the square class of `3*x0+2*x1`; no arbitrary
input square class or complementary twist relation is asserted.
