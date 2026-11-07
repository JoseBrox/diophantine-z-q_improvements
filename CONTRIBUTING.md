# Contributing

Submissions should state a mathematical result precisely, give its proof, identify every external hypothesis, and include reproducible data for decisive calculations. Keep the result in the paper devoted to its subject, with definitions and notation that can be read independently.

For a polynomial construction, specify the input coordinate, total variable count, total degree, coefficient normalization, all denominator guards, and the exact equivalence between the source system and the final polynomial. Distinguish exact counts from upper bounds. An implementation check certifies only the assertions it actually checks.

The public tree contains completed proofs, conditional theorems with explicit premises, and their reproducibility dependencies. Do not add conjectural constructions, exploratory rankings, or unsupported numerical records to the published documents or result tables.

Before proposing a change, run `python3 scripts/verify.py --full`, rebuild affected papers, inspect their rendered PDFs, and update the file manifest. Changes to the underlying arithmetic premises require a proof and precise primary references. Changes to numerical tables require an independent checker or a complete certificate where feasible.

Contributions of original material are made under the repository's CC BY 4.0 license. Retain third-party attribution and licensing notices.
