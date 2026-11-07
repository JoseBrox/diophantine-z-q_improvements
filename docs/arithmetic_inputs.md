# Arithmetic inputs and theorem scope

The construction papers prove explicit implications from stated arithmetic premises. Their coefficient tables and finite-algebra specifications are defined regardless of whether those premises have been established independently.

The four common premises are stated in full in the arithmetic-input section of the [small-variable paper](../papers/few_variables/few_variables_20261107_v7.pdf) and the [quartic paper](../papers/quartic/quartic_20261107_v7.pdf).

| Input | Mathematical content used | Computational boundary |
|:--|:--|:--|
| Elliptic group and index height | For the specified curve over $\mathbb Q(\sqrt2)$ and point $P$, the equality $2E(K)=\mathbb ZP$ and the lower bound $h(x([n]P))\ge n^2-6$ | Exact point identities and local valuations are checked. The checkers do not prove the full Mordell–Weil group assertion or the global lower bound. |
| Contact height | The five-contact radical bounds the height with exponent 19 and the explicitly stated constant $H_{19}$ | Two exact prime enumerations and integer computations certify the constant. They do not prove the contact-height inequality. |
| Pole obstruction and realization | The specified pole equations exclude the forbidden negative odd valuations and have solutions under the stated positivity, squareclass, and local-depth conditions | Coordinate transformations and their nonzero domains are checked. The arithmetic obstruction and simultaneous realization remain premises. |
| Simultaneous prime patterns | The prescribed prime values, fixed congruences, arbitrary fixed avoidance, and two conjugate reduction-order conditions can be achieved together | The use of the congruences is explicit. Finite arithmetic checks do not establish existence of infinitely many prime patterns. |

For the **456-variable quartic**, an additional weighted prime-pattern input supplies a lower count in a shrinking strip with the prescribed congruences. The paper states the count precisely and proves how it gives the required separation between chosen primes and opposite reduction orders. The 29- and 31-variable constructions do not use this strengthening.

## Ingredients proved directly

The papers prove the odd-product height identity, the rational point charts, the fourth-power input normalization, the local index-depth formulas, the elementary Lucas growth estimate, the new quadratic upper height estimate, and the finite-algebra elimination theorem. Their proofs identify any uses of the four premises above. In particular, the Lucas estimate is an elementary integral descent result and is not an additional arithmetic assumption.

The degree and coordinate lower bounds, the equation-combination theorem, and the field-extension and elliptic-chart obstructions have no dependency on these construction premises.

## Source identification

The arithmetic citations refer to the pinned sources listed in the computational manifests and to their precise theorem or lemma labels. In particular, the small-variable package pins the upstream source at commit `14e8f601fe0d9173d4a5f084aedc3e07066a7688`. The complete source graph and separate checker for the quartic are supplied with the baseline circuit.

“Proved conditional theorem” means that the implication from the listed premises to the specified projection is proved. It does not mean that a numerical audit establishes the premises. No entry in the result table should be read as an independent unconditional solution of Hilbert's tenth problem over the rationals.
