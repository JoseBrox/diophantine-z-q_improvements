# Exact actual detector traces at fixed admissible levels

The [manuscript](../../../papers/pole_parameters/admissible_levels_native_traces_20261116_v47.tex)
proves the local implication for admissible fixed levels and gives this
exact two-block source fixture for inputs **−1 and 1**, with **B=3**.
The original source's point functions, detector products, traces and coupled
arguments are retained. Fixed positive rational coefficients supported on
the original exceptional set rescale only the physical weights and inputs.

The two equations `(m V)^2 - 2 Y^2 = 4 w_rescaled / 17` then hold with
the actual prescribed reciprocal traces. The constants are frozen in
`scaling.json`. All 64 point-algebra characters and all 128 complement
guards are checked. This is not a uniform realization theorem, a sufficient
defining shift, or a new defining-variable bound.

`build-fixture.py` uses exact rational pairs. `check.py` independently
reconstructs the field arithmetic with SymPy's number-field domain.
`independent-check.py` uses polynomial residues modulo `t^2-2` and imports
neither producer nor the preceding checker. Each script accepts `--output`;
the scaling and check scripts also accept explicit input-table paths.

Run the complete reconstruction and byte comparison from the repository root:

```sh
python -B scripts/verify_v47.py
```
