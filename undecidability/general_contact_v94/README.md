# Shared affine contact progressions

The corrected general and specified quartics now use **1043** and **1223**
rational variables, with **907** and **1063** quadratic residuals, after
composing the shared contact progression with automatic positivity in the
signed binomial source. The progression alone uses **1048 / 1228** variables
and **908 / 1064** residuals.
The final polynomial in each case is the sum of the squares of the complete
listed residuals, hence has degree exactly four.

After the root points and aggregate shifts are fixed, one sufficiently large
integer spacing separates all twelve contact lists. Quantifying its scaled
or unscaled value permits a common progression of first contact arguments.
Seven common registers represent its spacing and the coefficients of its
centered square and fourth power. They replace thirty-three private registers,
saving **26 variables and 16 rows** in each complete system.

The signed-source theorem removes the two private three-coordinate positivity
wrappers for `w` and `s`, replacing them by one inverse coordinate and
`s*s_inverse=1`. It saves another **5 variables and 1 row**. These source
coordinates and rows have disjoint supports from the contact substitutions;
their exact rational reconstruction arguments therefore compose. The combined
savings relative to the corrected ceiling-power systems are **31 variables
and 17 rows**. The ordinary rational abc branch independently reaches
**781 variables / 684 rows**, using the fixed contact offsets and the same
signed-source theorem; its tables remain in `source_repair_v93/coefficients`.

Soundness follows from literal rational reconstruction. Every omitted row
has an exact polynomial identity in the root block's two retained rows and
the six new rows. Completeness uses the same fixed-family prime supplier,
finite avoidance, common-index congruences, local preparation and asymptotics
as the predecessor. The spacing is chosen after the input-dependent shifts;
no fixed numerical spacing is assumed to work for all source inputs.

The corrected source uses Jones (1980), Theorem 2, and the independently
proved binomial and signed-Pell certificates. The old `U_em` premise is not
used. The arithmetic hypotheses of the integer-defining interfaces remain;
these are not unconditional undecidability claims or minimum-variable claims.

## Reproduce

```sh
python undecidability/general_contact_v94/build_affine_contacts.py
python undecidability/general_contact_v94/verify_affine_contacts.py
python undecidability/general_contact_v94/build_signed_affine_contacts.py
python undecidability/general_contact_v94/verify_signed_affine_contacts.py
```

The independent verifier does not import the builder. It checks every
coefficient transformation, all 22 omitted-row polynomial identities,
unchanged guards, integer coefficient domains, support, counts and hashes.
The independent composite verifier checks every retained coefficient, the
six private positivity supports, the new inverse equation, the disjoint
supports of the two transformations, all inherited qualifications, and the
full count and hash chain. Neither independent verifier imports a builder.

- `affine_contact_progressions.tex` and `.pdf`: complete proof and coefficient recipe.
- `affine_contact_m163_quadrics.json`, `affine_contact_m179_quadrics.json`: complete coefficient tables.
- `signed_affine_contact_m163_quadrics.json`, `signed_affine_contact_m179_quadrics.json`: the complete composed coefficient tables.
- Adjacent `*_certificate.json`: hashes, exact savings and qualification ledger.
