# Even abscissa valuations in the eleven-variable source

Every guarded point of `y^2=x(x^2-(11-6sqrt(2)))` has even abscissa
valuation outside the retained primes 2 and 7. Thus the first four tests
may use `D=C/(1+u*C)`; the two comparison tests retain
`D=C^2/(1+u*C^2)`. The full auxiliary point domain remains available.

The complete ordinary-abc eleven-variable family now has degree at most
**230,932,097**, improving 232,094,337. It has 1,865 arithmetic nodes,
32 native guards, rank 128, content one and fewer than `2^264` monomials.
The seven-contact arithmetic variant has degree at most **356,146,817**
and physical weight degree seven in the squared slope.

The sufficient odd coefficient shift is ineffective. Stored `B=3` files
are algebraic fixtures, not certified defining members. The source with
nine total coordinates remains sound; global actual-trace realization
and its completeness are unproved.

Reproduce from the repository root:

```sh
python computation/few_variables/even_valuation11_v75/build_source.py
python computation/few_variables/even_valuation11_v75/check.py
python computation/few_variables/even_valuation11_v75/build_source.py --contacts 7
python computation/few_variables/even_valuation11_v75/check.py --specification computation/few_variables/even_valuation11_v75/seven_contact
```

Each checker run independently traverses the specification, checks 384
finite-field point characters, and rejects two deliberately corrupted
specifications. The source computes direct inverse-abscissa formulas;
the independent native check evaluates the distinct formula `C/(1+u*C)`.
The proof is
[`even_valuation_detector_20261117_v75.tex`](../../../papers/conditional_few_variables/even_valuation_detector_20261117_v75.tex).
