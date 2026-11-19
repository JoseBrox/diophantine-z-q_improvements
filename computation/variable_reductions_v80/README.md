# v80: one normalization coordinate and the published pole theorem

The ordinary-abc quartic now has 58 variables, 50 quadratic residuals and 867 monomials. Its source chart and shared Laurent packing derive from **notes of Gabe Conant with Astra 6.2**. The one-helper normalization is subsequent project work.

The `abc/` package contains the complete polynomial, builder, independent reconstruction, proof review and source hashes. Its new physical input is `7*tau²/u`, where `alpha=u+u²D²` and `tau(1+alpha)=alpha`. The factor seven matches Burungale's published Theorem B; the extra square-class-one twist premise retained in v79 is not required.

Run `python -B scripts/verify_v80.py` from the repository root. Published files remain unchanged during verification. The complete proof is `papers/quartic_existence/one_helper58_20261119_v80.tex`; current results and arithmetic qualifications are recorded in `docs/results_20261119_v80.md` and `data/results_20261119_v80.json`.
