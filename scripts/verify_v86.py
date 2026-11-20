#!/usr/bin/env python3
"""Exact v86 Busy Beaver numerical envelopes (no BB evaluation).

The 163-variable theorem and the v22 compiler and arithmetic arguments are
mathematical dependencies: finite checks do not replace their proofs.
Optionally pass --source-tex /path/to/quartic_v22.tex for the uploaded-source
SHA256 and unexecuted Python AST checks.
"""
from pathlib import Path
import argparse, ast, hashlib, json, math, re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "3ac000a6481badf818d58fb409d3b217b22709c7cb92039935fb5e68e6d452b6"

def source_inspection(source):
    raw = source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    te = raw.decode()
    selector = te.split(r"\section{Reference record selector}", 1)[1].split(
        r"\section{Reference coefficient interpreter}", 1)[0]
    section = re.search(r"\\begin\{verbatim\}(.*?)\\end\{verbatim\}",
                        selector, re.S).group(1)
    assert section.count("scale = power(2,power(2,1000))") == 1
    assert section.count("return power(scale,1000)*(record+3)") == 1
    tree = ast.parse(section)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert len(functions) == 16
    assert sum(1 for node in ast.walk(tree)) == 1506
    assert not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))
    assert not any(isinstance(node, ast.Call) and
                   not isinstance(node.func, ast.Name) for node in ast.walk(tree))
    graph = {name: {node.func.id for node in ast.walk(function)
                    if isinstance(node, ast.Call) and node.func.id in functions}
             for name, function in functions.items()}
    def depth(name, path=frozenset()):
        assert name not in path
        return 1 + max((depth(target, path | {name}) for target in graph[name]), default=0)
    assert max(depth(name) for name in functions) == 10
    assert max(node.value for node in ast.walk(tree)
               if isinstance(node, ast.Constant) and type(node.value) is int) == 1000
    return {"sha256": SOURCE_SHA256, "AST_nodes": 1506,
            "functions": 16, "max_acyclic_call_depth": 10}

def main():
    arg = argparse.ArgumentParser(description=__doc__)
    arg.add_argument("--report", type=Path)
    arg.add_argument("--source-tex", type=Path)
    args = arg.parse_args()
    d, m = 9, 10
    nA, nP = 3**8, 4
    degV = math.factorial(10) * 3**8
    La = 2**(m*m) * (8*m*d)**(m*d) * nA*nP*degV**(3*m)
    psi = math.prod(3*j+1 for j in range(2, m*d + 1))
    assert (degV, La.bit_length(), psi.bit_length()) == (23808556800, 2004, 602)
    e1log = 3 + 2004*psi
    e22log = 2 + 8016*psi
    mulog = 2 + 2004*psi
    e3log = 27150 + 16032*psi
    rec_log = 36 + 8016*psi
    bound = 2**616
    assert max(e1log, e22log, mulog, e3log, rec_log) + 8 < bound
    assert 330770 < bound and 4000000 < bound
    assert 45*4 < 149**2
    # Sharpened state count: 16 instructions per hardwired bit, 2 scratch
    t0 = 2**20 * (2**620 + 2**186 + 1) * (2**186 + 3)
    assert 2**826 < t0 < 2**827
    assert t0 < 2**826 + 2**642
    assert t0.bit_length() == 827
    assert 2**20 * 2**843 * 2**149 == 2**1012
    # Representative checks only; the universal argument is in the manuscript.
    for U in (2**16, 2**20, 2**32):
        assert U**3 > 1000*math.log(U)/math.log(149)
        assert 10*math.log(U) < U**3/100
        assert (U**3*math.log(149))/18 > math.log(20*U**3)
        assert U**3*(U+3) > U**2*(U+4)
    data = json.loads((ROOT/"data/results_20261120_v82.json").read_text())
    row = next(a for a in data["current_constructions"] if a["id"] == "quartic163")
    assert (row["variables"], row["monomials"], row["degree"]) == (163, 2789, 4)
    assert row["retained_R_square"] and row["parameter_effective"] is False
    readme = (ROOT/"README.md").read_text()
    assert "2^827" in readme and "BB(2^1012)" in readme
    tex = (ROOT/"papers/quartic/bb163_fixed_20261120_v86.tex").read_text()
    assert r"\BB(t_0)" in tex and "27150+16032" in tex
    report = {
        "schema":"diophantine-busy-beaver-sharpening/v86",
        "status":"PASS", "source_theorem_v22_sha256":SOURCE_SHA256,
        "Lambda_bit_length":2004,"psi_bit_length":602,
        "log2_e3_upper_bit_length":e3log.bit_length(),
        "record_count_log2_upper_bit_length":rec_log.bit_length(),
        "U":"2^(2^616)","parameter_threshold":"U^3*(R_final+3)",
        "fixed_BB_index_decimal":str(t0),
        "rounded_sufficient_index":"2^827",
        "coefficient_height_upper":"BB(2^1012)",
        "source_AST_checked": bool(args.source_tex),
        "scope":"Exact integer envelopes; inherited v22 arithmetic, geometric height bounds and compiler templates not independently reproved here."
    }
    if args.source_tex:
        report["source_AST"] = source_inspection(args.source_tex)
    result = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(result)
    print(result)

if __name__ == "__main__":
    main()
