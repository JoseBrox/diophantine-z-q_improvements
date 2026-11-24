#!/usr/bin/env python3
"""Verify integer comparisons in the conditional v85 BB threshold.

This check neither computes an ineffective height constant nor asserts that
any concrete numerical Busy Beaver index has been certified.
"""
from pathlib import Path
import argparse
import json
import re
import sys

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

ROOT=Path(__file__).resolve().parents[1]

def L(n:int)->int:
    return (9*(2*n-1))//4+1

def sample(m:int,n:int):
    assert m>=2 and n>=max(3,m)
    t=149**L(n)
    d=4*m*m+m*(6*(2*n+1)+15)+m
    assert t*t>2*d, (m,n,"scalar error")
    assert t>(2*m)**18*14**7,(m,n,"comparison")
    assert 5*t>7*m and 5*t>12*m and t>100,(m,n,"Lucas")
    return len(str(t))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report",type=Path)
    args=ap.parse_args()
    assert 149**11 == 803616698647447868139149
    assert 6**18*14**7 == 10705790898505896689664
    assert 149**11 > 6**18*14**7
    assert 149**4*3**18>4**18
    assert all(L(n)>=4*n-1 for n in range(1,101))
    tested=[]
    for m in [2,3,4,5,10,31,100,1000]:
        for n in [max(3,m),max(3,m)+1,2*max(3,m)]:
            digits=sample(m,n)
            tested.append({"m":m,"n":n,"digits_of_149_power":digits})
    source=(ROOT/"papers/quartic/scalar_point163_179_20261120_v82.tex").read_text()
    assert r"L_N=\lfloor9(2N-1)/4\rfloor+1" in source
    assert "ineffective" in source
    assert "C_1|J_0|^{7/18}" in source
    assert "B_0^{7/6}" in source
    assert r"h(R)\le4\tau_\beta" in source
    note=(ROOT/"docs/explicit_BB_threshold_20261120_v85.md").read_text()
    assert "no literal numeral" in note
    assert r"N_M:=\max\{3,M\}" in note
    assert "Kleene" in note
    table=(ROOT/"README.md").read_text()
    assert "Expanded TXT size (kB)" in table
    assert table.split("## Fewest variables currently recorded for undecidability", 1)[0].count("| Ordinary rational abc |")==2
    out={"schema":"bb-conditional-threshold/v85","status":"PASS",
         "conditional_index":"max(3,M)",
         "numeric_M_certified":False,"numeric_t_certified":False,
         "all_tested_integer_inequalities":tested,
         "scope":"Universal proof is in the v85 note; arithmetic constants remain ineffective."}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
if __name__=="__main__":
    main()
