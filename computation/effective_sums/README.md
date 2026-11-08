# Effective heights of elliptic abscissa sums

Read [the theorem and proof](../../papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf). For four nonzero integer multiples on the stated integral elliptic curve, with positive abscissas at both real embeddings, the theorem gives

$$h(\sum_i x([n_i]P))\ge\max_i h(x([n_i]P))-24\log B-\log864,$$

where $B=\max_i|n_i|$. Every finite place is included. The theorem is unconditional; its application to an index bound invokes the separate index-height input stated in the construction papers.

Run `python3 check_effective_elliptic_sums.py` to reproduce the exact curve, formal-series, valuation, combinatorial and numerical certificates. The global all-place argument is proved in the paper rather than inferred from the finite tests.
