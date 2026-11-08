# Optimal polynomial square tests

Read [the proof](../../papers/square_predicates/quadratic_square_predicates_20261108_v10.pdf) or [its TeX source](../../papers/square_predicates/quadratic_square_predicates_20261108_v10.tex).

The complete degree-six square predicate over $\mathbb Q(\sqrt2)$ uses two rational input components and one rational auxiliary variable. It has ten monomials and coefficient height seven. Its degree and auxiliary-variable degree are optimal for this form of definition. Height seven is proved optimal within the stated integral linear-multiplier family. These are unconditional square-membership results, not integrality definitions.

Run `python3 check_square_predicates.py` and `python3 check_height7_linear_multiplier.py` to reproduce the complete coefficient tables and exact certificates. Only Python 3.10 or newer and its standard library are required. The first checker includes an independent Sylvester-determinant calculation; the second independently expands the displayed polynomial and checks the sixteen cases after the coefficient-lower-bound proof reduces to them.
