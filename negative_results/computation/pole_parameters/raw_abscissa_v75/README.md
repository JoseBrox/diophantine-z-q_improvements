# Actual failure of automatic raw-abscissa preparation

The exact tuple is `X=2, B=3, A=2P, H=10336P, U=20672P` with the
physical nine-contact slope `z=670434583579295`. The two candidate
raw detectors replace the first four factors by `1+C_i/u` or
`1+C_i^2/u`, keeping the original balanced comparison factors.

At `p=76777`, the actual physical weight has valuation `-1`, and
`H-P` reduces to `(0,0)` with abscissa valuation two in both slots.
The two actual traces have valuations one and three. The resulting
pole inputs have valuations **-1 and -5**; both actual-trace square
radicands have valuation **one** and hence are not rational squares.

All pre-pole point, contact and detector guards are nonzero at every
point character. The actual slope satisfies `z>a+100`; all real pole
inputs satisfy `0<eta<847/10000<1`. This does not verify the selected
prime factorization or fixed finite-place preparation. The example
refutes automatic preparation for these raw factors, not global
completeness or all choices of witnesses. `B=3` is a fixture only.

Reproduce from the repository root:

```sh
python negative_results/computation/pole_parameters/raw_abscissa_v75/check.py
python negative_results/computation/pole_parameters/raw_abscissa_v75/check_independent.py
python negative_results/computation/pole_parameters/raw_abscissa_v75/check_division.py
```

The producer uses guarded projective multiplication modulo `p^2`;
the independent checker uses affine multiplication with explicitly
verified unit denominators and imports no producer module.
A third checker evaluates division polynomials modulo `p^3`, importing
neither group law, and obtains the abscissa valuations directly. It
also verifies all inverted denominators, the curve equation, and a
doubling control. The recurrence formulas are cited in its docstring
and in the paper.

Proof:
[`raw_abscissa_preparation_20261117_v75.tex`](../../../papers/pole_parameters/raw_abscissa_preparation_20261117_v75.tex).
