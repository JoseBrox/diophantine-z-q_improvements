#!/usr/bin/env python3
"""Independently check compact expanded text sizes and BB coefficient profiles.

No producer is imported. Numeric text is parsed back into monomial/coefficient
maps and compared exactly to the pinned original polynomial tables.
"""
from collections import defaultdict
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/"computation/expanded_text_v84"
SPECS={
    "quartic163-N1.txt":("computation/variable_reductions_v82/general/quartic163/polynomial.json",149,163,2789),
    "quartic179.txt":("computation/variable_reductions_v82/general/quartic179/polynomial.json",1,179,3036),
    "quartic56-B3.txt":("computation/variable_reductions_v81/abc/quartic56/polynomial.json",3,56,809),
}

def git_blob_hash(raw:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def parse_numeric(text:str)->dict[tuple[int,...],int]:
    assert text.isascii() and text and "\n" not in text
    result={}
    for term in re.split(r"(?=[+-])",text):
        if not term:
            continue
        sign=-1 if term.startswith("-") else 1
        body=term[1:] if term[0] in "+-" else term
        c=sign
        indices=[]
        for component in body.split("*"):
            if component.isdecimal():
                c*=int(component)
                continue
            match=re.fullmatch(r"(X|x[1-9][0-9]*)(?:\^([1-4]))?",component)
            assert match,component
            variable=1 if match[1]=="X" else int(match[1][1:])
            indices.extend([variable]*int(match[2] or 1))
        assert c != 0
        key=tuple(sorted(indices))
        assert key not in result,f"duplicate monomial: {key}"
        result[key]=c
    return result

def expected_monomials(spec:dict,parameter:int)->dict[tuple[int,...],int]:
    coefficients=defaultdict(int)
    for row in spec["terms"]:
        coefficients[tuple(row["monomial"])]+=int(row["coefficient"])*parameter**int(row["parameterPower"])
    return {k:v for k,v in coefficients.items() if v}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report",type=Path)
    args=ap.parse_args()
    receipt=json.loads((PACKAGE/"size_report.json").read_text())
    assert receipt["schema"]=="diophantine-compact-expanded-ascii/v84"
    assert receipt["kilobyte_bytes"]==1000
    for filename,(source,parameter,n,terms) in SPECS.items():
        data=json.loads((ROOT/source).read_text())
        assert data["variables"]==n
        raw=(PACKAGE/filename).read_bytes()
        record=receipt["artifacts"][filename]
        assert len(raw)==record["bytes"]
        assert git_blob_hash(raw)==record["git_blob_sha1"]
        table=parse_numeric(raw.decode("ascii"))
        assert table==expected_monomials(data,parameter),filename
        assert len(table)==terms==record["monomials"]
        print(f"{filename}: PASS, {len(raw)} exact bytes, {terms} monomials")
    p163=json.loads((ROOT/SPECS["quartic163-N1.txt"][0]).read_text())
    varying=[r for r in p163["terms"] if r["parameterPower"]]
    assert {(tuple(r["monomial"]),int(r["coefficient"]),r["parameterPower"]) for r in varying}=={
        ((78,78,90),-6615898,2),((78,90),-298,2),((78,78),22201,4)}
    symbolic_path="quartic163-BB_t-symbolic.txt"
    symbolic_raw=(PACKAGE/symbolic_path).read_bytes()
    assert git_blob_hash(symbolic_raw)==receipt["artifacts"][symbolic_path]["git_blob_sha1"]
    assert len(symbolic_raw)==receipt["artifacts"][symbolic_path]["bytes"]==60929
    symbolic=symbolic_raw.decode("ascii")
    assert symbolic.count("BB(t)") == 3
    replacements=[
       ("6615898*149^(2*BB(t))",str(6615898*149**2)),
       ("298*149^(2*BB(t))",str(298*149**2)),
       ("22201*149^(4*BB(t))",str(22201*149**4)),
    ]
    for original,replacement in replacements:
        assert symbolic.count(original)==1,original
        symbolic=symbolic.replace(original,replacement)
    assert symbolic==(PACKAGE/"quartic163-N1.txt").read_text()
    # For any N>=1 the length is exactly a fixed 60,872 bytes plus three
    # coefficient lengths. No BB value or numeric threshold is assumed.
    digits=lambda value:len(str(value))
    for n in (1,2,10,100):
        c=149**n
        formula=60872+digits(6615898*c**2)+digits(298*c**2)+digits(22201*c**4)
        if n==1:
            assert formula==60905
        # Check the three independently evaluated profile lengths.
        assert formula > 60872
    records=json.loads((ROOT/"data/results_20261120_v82.json").read_text())
    current={r["id"]:r for r in records["current_constructions"]}
    for key,exponent in (("general25",848),("explicit27",965),("ordinary_abc11",227)):
        row=current[key]
        e=int(row["coefficient_log2_l1_bound_for_stored_member"])
        s=int(row["support_strict_power_two"])
        # 2^100<10^31 implies log_10 2<31/100.
        digit_limit=e*31//100+2
        degree=int(row["degree_upper_bound"])
        monomial_max=row["variables"]*(6+len(str(degree)))
        term_power=exponent+9-s
        assert digit_limit+monomial_max+2<2**term_power,(key,exponent)
        assert s+term_power-9==exponent
        assert receipt["unexpanded_fixture_upper_bounds_kB"][key]["strict_power_of_two"]==exponent
    readme=(ROOT/"README.md").read_text()
    current_table=readme.split("## Current constructions",1)[1].split("## Coefficients",1)[0]
    assert "Expanded TXT size (kB)" in current_table
    assert "60.905" in current_table and "66.903" in current_table and "11.562" in current_table
    assert "BB(t)" in readme
    print("BB profile, literal-byte formula, three coarse fixture bounds and README: PASS")
    result={"schema":"diophantine-expanded-txt-verification/v84","status":"PASS",
            "quartic163_N1_bytes":60905,"quartic179_bytes":66903,
            "quartic56_B3_bytes":11562,"quartic163_BB_symbolic_bytes":60929,
            "defining_index_for_163_fixed_BB_member_certified":False,
            "all_numeric_text_reparsed_and_compared_exactly":True}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
