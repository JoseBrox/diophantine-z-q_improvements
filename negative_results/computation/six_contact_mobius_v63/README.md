# Integer-power obstruction to six-contact Möbius coupling

The manuscript proves that every fixed finite menu of integer exponents
`e >= 4` fails eventual prescribed-index completeness for the displayed
six-contact coupling. One arithmetic progression of odd shifts obstructs
all exponents in the menu, all twelve rational Möbius symmetries, either
retained detector pole condition, and any fixed finite menu of nonzero
rational contact multipliers.

The theorem is an obstruction for the specified source and prescribed
point `X=1, A=P`. It does not assert impossibility of a different contact
system, of an independently chosen root index, or of an infinite menu of
exponents.

## Proof ingredients

1. Exact interpolation enumerates the twelve symmetries of the six roots.
2. A positive one-step recurrence proves the discriminant square gaps
   for ten branches for every integer exponent at least four.
3. The identity violates the contact guard.
4. For the remaining involution, a simple contact at an inert prime
   forces a forbidden negative odd detector pole for every auxiliary tuple.
5. An odd-degree root field handles odd exponents. For even exponents,
   a nonsquare odd binomial constant supplies a totally ramified
   power-of-two root field at an odd prime; it cannot contain `Q(sqrt(2))`.
   An odd-degree extension then supplies the required full binomial root.
6. Chebotarev gives infinitely many inert root primes outside every fixed
   finite exceptional set. Distinct primes and CRT obstruct a finite
   menu simultaneously.

## Exact computation

Run:

```sh
python check.py --output certificate.json
```

The checker uses only the Python standard library. It verifies:

- all 120 ordered image triples and all twelve multiplier identities;
- all ten discriminant identities, initial square gaps and positive
  recurrence coefficients;
- both rational involution identities and `H'(4)=11250`;
- nine exact prime certificates, including odd and even exponents;
- the simple modular roots, exact contact valuations, denominator units
  and a simultaneous CRT progression.

The numerical menu is `4,5,6,7,8,10,12,16,32`. The infinite theorem follows
from the mathematical proof, independently of these fixtures.

The bibliography identifies Milne's *Algebraic Number Theory*, version
3.08, Theorem 8.31, as the Chebotarev source. The theorem statement was
checked directly in the published course notes.
