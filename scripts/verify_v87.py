#!/usr/bin/env python3
"""Exact integer certification of the v87 BB index and coefficient wrapper.

The proof uses the audited v22/v86 Vojta, arithmetic, elliptic geometry and
compiler lemmas. This checker does not independently prove those lemmas
or evaluate Busy Beaver. It is read-only and source-independent.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"computation/bb_v87"

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report",type=Path)
    args=ap.parse_args()
    record=json.loads((HERE/"certificate.json").read_text())
    assert record["schema"]=="diophantine-bb-compact-v87"
    m,dim=10,9
    psi=math.prod(3*j+1 for j in range(2,m*dim+1))
    lam=2**(m*m)*(8*m*dim)**(m*dim) * 3**8 * 4 * (math.factorial(10)*3**8)**(3*m)
    assert (lam.bit_length(),psi.bit_length())==(2004,602)
    kappa=27160+16032*psi
    assert kappa.bit_length()==616
    assert kappa==int(record["kappa"])
    assert 2**615<kappa<2**616
    # Logarithmic upper bounds. Crucially, U=2^kappa needs no rounding
    # of kappa up to a power of two.
    e1=3+2004*psi
    e22=2+8016*psi
    mu=2+2004*psi
    e3=27150+16032*psi
    records=36+8016*psi
    assert max(e1,e22,mu,e3)+10<=kappa
    assert records<kappa
    assert e3+10==kappa
    assert kappa>4_000_000 and kappa>330_770
    assert kappa.bit_length()<=1000  # source fixed-literal loader
    t1=2**20*(16*kappa+2**186+1)*(2**186+3)
    assert 2**825<t1<2**826
    assert int(record["t1"])==t1 and t1.bit_length()==826
    assert len(str(t1))==249
    # Coefficient wrapper: at most 2*t1 transition entries, 829
    # bits/entry (826 state bits + 3 flags), each hardcoded bit costs
    # fewer than 16 instructions. The source's fixed core costs
    # fewer than 2^148 instructions, the counter budget <2^149.
    table_bits=2*t1*829
    assert table_bits <2**837
    assert 16*table_bits<2**841
    assert 16*table_bits+2**148<2**841
    assert 2**20 * 2**841 * 2**149==2**1010
    assert record["coefficient_height_upper"]=="BB(2^1010)"
    assert record["new_U"]=="2^kappa"
    assert record["arithmetic_threshold"]=="U^3*(Rfinal+3)"
    # Check that the resulting target is a *fixed index relative
    # to BB*, not a decimal-coefficient polynomial.
    source=(ROOT/"data/results_20261120_v82.json")
    table={r["id"]:r for r in json.loads(source.read_text())["current_constructions"]}
    assert (table["quartic163"]["variables"],table["quartic163"]["monomials"])==(163,2789)
    assert table["quartic163"]["exact_height"].startswith("max(")
    manuscript=(ROOT/"papers/quartic/bb163_compact_record_20261120_v87.tex").read_text()
    assert r"t_1=2^{20}(16\kappa+2^{186}+1)(2^{186}+3)" in manuscript
    assert r"F_{\BB(t_1)}" in manuscript
    readme=(ROOT/"README.md").read_text()
    assert "bb163_compact_record_20261120_v87.tex" in readme
    assert "2^826" in readme and "BB(2^1010)" in readme
    out={
      "schema":"diophantine-bb-compact-verification/v87","status":"PASS",
      "Lambda_bit_length":lam.bit_length(),"psi_bit_length":psi.bit_length(),
      "kappa_bit_length":kappa.bit_length(),"t1_bit_length":t1.bit_length(),
      "t1_decimal":str(t1),"coefficient_height_upper":"BB(2^1010)",
      "numeric_BB_index_certified_relative_to_v22_arithmetic_geometry_compiler":True,
      "source_externally_reproved_by_this_check":False,
      "scope":"Independent exact arithmetic and repository consistency, not a standalone reproof of the v22 analytic/compiler lemmas."
    }
    text=json.dumps(out,indent=2)+"\n"
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(text)
    print(text)

if __name__=="__main__":
    main()
