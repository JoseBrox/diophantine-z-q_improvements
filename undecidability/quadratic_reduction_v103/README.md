# Shared denominator coefficients remove private contact combinations

The exact compression here gives **963 variables / 818 quadratic rows** in the general route and **1140 variables / 991 rows** in the specified route. It saves five and three variables, respectively, from the v102 complete systems. All thirteen / eleven integer predicates remain. The ordinary-abc route is unchanged at 695/590.

Polynomial division lowers the inverse-weight equation's remaining numerator to degree three. An affine change of the old inverse-weight coordinate then lets nine common denominator coefficients replace one private combination register at every contact on the existing progression: fourteen contacts in the general chart, twelve in the specified chart. The root block's second contact is already index 16, so it participates without any new arithmetic construction.

The proof gives a **bijective rational reconstruction of the entire predecessor zero set**. No new nonzero guard or arithmetic premise is added. The retained common gauge is nonzero; the transformation does not divide by a contact value, inverse weight, or new denominator coefficient. Zero weights and zero spacing are covered.

## Exact reusable identity

Let `u^2=k*f`, with nonzero `k`, and fixed constants `A,B,C,D,E,F`, where `C!=0`. Write

```
Comb = A*u*f+(B*u+C*f)*(W+k)-k*t
Rel  = (D*u+E*f+F*k)*(W+k)+f*t
V    = C^2*(W+k)+A*C*u-A*B*k
P    = C*f^2+B*u*f+E*k*f+D*k*u+F*k^2
R    = A*(B^2-C*E)*u*f+A*(B*E-C*D)*k*f
       +A*(B*D-C*F)*k*u+A*B*F*k^2.
```

Then, identically,

```
P*V+k*R-C^2*(k*Rel+f*Comb)
    = A*C*(B*f+D*k)*(u^2-k*f).
```

If `k*p=P`, the two old contact rows can be replaced by `p*V+R=0`, deleting `t` and using `V` in place of `W`. The inverse map is

```
W = (V-A*C*u-(C^2-A*B)*k)/C^2
t = (A*u*f+(B*u+C*f)*(W+k))/k.
```

For a common square/fourth-power progression, `P` is a polynomial of degree eight in the contact index. Its nine coefficients are shared and satisfy quadratic definitions. With `r` such contacts, this saves `r-9` coordinates and rows.

## Files and reproduction

- `contact_denominator_compression.tex`: complete proof, exact constant tuples, guards, inverse maps, and counts.
- `denominator_general_quadrics.json`, `denominator_specified_quadrics.json`: complete coefficient tables.
- Adjacent `_certificate.json` files: source hashes, transformation dictionaries, occurrence lists, and result hashes.
- `build_contact_denominator.py`: deterministic compiler.
- `verify_contact_denominator.py`: independent exact audit, with no compiler import.

Run from the repository root:

```sh
python -B undecidability/quadratic_reduction_v103/build_contact_denominator.py
python -B undecidability/quadratic_reduction_v103/verify_contact_denominator.py
```

The checker proves the displayed identity and the retained progression identity, checks the original contact templates, reconstructs every changed row, compares every unchanged row, and verifies degree, coefficients, complete support, counts, and hashes. These finite checks do not prove the inherited arithmetic premises or the externally cited Jones coding theorem. The sufficient general parameter remains ineffective. No quartic bound near 263 is asserted.

The exploratory `search_affine.py` also checks the rank of all quadratic homogeneous row parts over rational constant combinations, expanding fixed parameters into separate monomials. The three predecessor ranks are 823, 994, and 590: there is no nontrivial rational constant row combination with zero quadratic part in that restricted search. This is not a lower bound for guarded, nonlinear, or parameter-dependent changes.
