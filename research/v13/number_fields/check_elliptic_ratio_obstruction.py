#!/usr/bin/env python3
"""Certify the elliptic ratio obstruction, using PARI's unconditional 2-descent.

Install cypari2>=2.2.4 in the active environment, or supply its directory with
PYTHONPATH.  No numerical analytic-rank or BSD calculation is used.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import json
import sys

local_python = Path(__file__).resolve().parent / "python"
if local_python.is_dir():
    sys.path.insert(0, str(local_python))
from cypari2 import Pari


def finite_points(B, p):
    pairs = [(x, y) for x in range(p) for y in range(p)
             if (y*y-x*x*x-B) % p == 0]
    legendre_count = 1 + sum(1 if (x*x*x+B) % p == 0 else
                              2 if pow((x*x*x+B) % p, (p-1)//2, p) == 1 else 0
                              for x in range(p))
    assert len(pairs)+1 == legendre_count
    return len(pairs)+1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pari = Pari()
    records = []
    expected = {9: (1, 3, "972c1"),
                81: (0, 3, "972b2"),
                -9: (0, 1, "3888k1")}
    for B, (rank, torsion, label) in expected.items():
        E = pari.ellinit([0, 0, 0, 0, B])
        r = pari.ellrank(E)
        t = pari.elltors(E)
        two_covers = pari.ell2cover(E) if rank == 0 else None
        assert int(r[0]) == int(r[1]) == rank
        assert int(t[0]) == torsion
        if rank == 0:
            assert len(two_covers) == 0
        records.append({"B": B, "ainvariants": [0, 0, 0, 0, B],
                        "cremona_label": label,
                        "ellrank": str(r), "elltors": str(t),
                        "rank_lower": int(r[0]), "rank_upper": int(r[1]),
                        "torsion_order": int(t[0]),
                        "nontrivial_2covers": str(two_covers) if two_covers is not None else None,
                        "independent_finite_field_orders":
                        {str(p): finite_points(B, p) for p in (5, 7)}})

    quadratic_fields = []
    for d in (-15, -13, -11, -10, -1, 3, 5, 7):
        E = pari.ellinit([0, 0, 0, 0, 9*d**3])
        r = pari.ellrank(E)
        t = pari.elltors(E)
        assert int(r[0]) == int(r[1]) == 0
        assert int(t[0]) == 1
        quadratic_fields.append({"squarefree_d": d, "twist_B": 9*d**3,
                                 "ellrank": str(r), "elltors": str(t),
                                 "rank_lower": 0, "rank_upper": 0,
                                 "torsion_order": 1})

    # A fully elementary positive-rank witness on E_9: twice (3,6)
    # is nonintegral, so Nagell--Lutz excludes torsion.
    x = Fraction(3)
    y = Fraction(6)
    slope = 3*x*x/(2*y)
    x2 = slope*slope-2*x
    y2 = slope*(x-x2)-y
    assert (x2, y2) == (Fraction(-15, 16), Fraction(183, 64))
    assert y2*y2 == x2*x2*x2+9

    # Identity for the forbidden ratio -1:
    # (9+u^3)(9-u^3)=81-u^6=(-u^2)^3+81.
    product = {}
    for i, a in {0: 9, 3: 1}.items():
        for j, b in {0: 9, 3: -1}.items():
            product[i+j] = product.get(i+j, 0)+a*b
    product = {e: c for e, c in product.items() if c}
    elliptic_rhs = {0: 81, 6: -1}
    assert product == elliptic_rhs
    for u in [Fraction(0), Fraction(1), Fraction(-2), Fraction(3, 5)]:
        assert (9+u**3)*(9-u**3) == (-u*u)**3+81

    # Exact conditions supplying local roots by Hensel's lemma.
    local_checks = []
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        u = 9 if p == 3 else p
        vals = [9+u**3, 9-u**3]
        if p == 2:
            assert all(v % 8 == 1 for v in vals)
            reason = "both odd parts are 1 modulo 8"
        elif p == 3:
            assert all(v % 9 == 0 and (v//9) % 3 == 1 for v in vals)
            reason = "after division by 9, both are 1 modulo 3"
        else:
            assert all(v % p == 9 % p and v % p != 0 for v in vals)
            reason = "both reduce to the nonzero square 9 modulo p"
        local_checks.append({"p": p, "u": u, "values": vals, "reason": reason})
    assert 9+1 > 0 and 9-1 > 0

    # Sparse expansion of the explicit four-coordinate polynomial.
    # Exponent order is (t,w,u,v).
    F = {(0, 1, 2, 0): 1, (0, 3, 0, 0): -9, (0, 0, 0, 0): -1}
    G = {(1, 1, 0, 2): 1, (3, 3, 0, 0): -9, (0, 0, 0, 0): -1}
    polynomial = {}
    for Q, factor in [(F, 1), (G, -2)]:
        for e, a in Q.items():
            for f, b in Q.items():
                h = tuple(ei+fi+(i == 0) for i, (ei, fi) in enumerate(zip(e, f)))
                polynomial[h] = polynomial.get(h, 0)+factor*a*b
    polynomial = {e: c for e, c in polynomial.items() if c}
    degree = max(map(sum, polynomial))
    height = max(map(abs, polynomial.values()))
    assert (len(polynomial), degree, height) == (11, 13, 162)
    # Distinct rational samples, independent factored evaluation.
    for t, w, u, v in [(1, 2, 3, 4), (-1, 1, 1, 1),
                        (Fraction(2, 3), Fraction(3, 5), Fraction(-4, 7), Fraction(5, 11))]:
        expanded = sum(c*t**e[0]*w**e[1]*u**e[2]*v**e[3]
                       for e, c in polynomial.items())
        factored = t*((u*u*w-9*w**3-1)**2-2*(v*v*t*w-9*t**3*w**3-1)**2)
        assert expanded == factored

    result = {
        "status": "PASS", "pari_version": str(pari("version()")),
        "rank_method": "ellrank: unconditional 2-Selmer and Cassels-pairing bounds; matching lower and upper bounds",
        "bsd_or_analytic_rank_used": False,
        "curves": records,
        "additional_quadratic_fields": quadratic_fields,
        "positive_rank_witness": {"P": ["3", "6"],
                                  "2P": [str(x2), str(y2)]},
        "forbidden_ratio_identity": "(9+u^3)(9-u^3)=(-u^2)^3+81",
        "local_witness_checks": local_checks,
        "uniform_local_proof": "For every odd prime p other than 3 use u=p and Hensel at roots +/-3. For p=3 use u=9 and divide each radicand by 9. For p=2 use u=2. Over R use u=1.",
        "four_coordinate_polynomial": {
            "variable_order": ["t", "w", "u", "v"],
            "formula": "t*((u^2*w-9*w^3-1)^2-2*(v^2*t*w-9*t^3*w^3-1)^2)",
            "total_coordinates": 4, "degree": degree, "height": height,
            "ordinary_monomials": len(polynomial),
            "terms": [{"exponents": list(e), "coefficient": c}
                      for e, c in sorted(polynomial.items())]
        },
        "references": {
            "pari_ellrank": "https://pari.math.u-bordeaux.fr/dochtml/ref/Elliptic_curves.html#ellrank",
            "cremona_data": "https://github.com/JohnCremona/ecdata/blob/master/allcurves/allcurves.00000-09999",
            "lmfdb_81": "https://www.lmfdb.org/EllipticCurve/Q/972/d/2",
            "lmfdb_minus9": "https://www.lmfdb.org/EllipticCurve/Q/3888k1/"
        },
        "scope": "Certifies arithmetic inputs for a proper locally dense Diophantine subset of Q inside Q(i). It is not a counterexample to Diophantine definability of Z[i] in Q(i)."
    }
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "pari_version": result["pari_version"],
                      "curves": [{"B": r["B"], "rank_bounds": [r["rank_lower"], r["rank_upper"]],
                                  "torsion_order": r["torsion_order"]} for r in records]}, indent=2))


if __name__ == "__main__":
    main()
