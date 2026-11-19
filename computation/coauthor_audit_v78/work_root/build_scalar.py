"""Compile the four-contact scalar with a square-shifted integral target.

Arithmetic certification and independent reconstruction are separate.
"""
from pathlib import Path
import argparse
import importlib.util
import inspect
import json
import math
import sys
import textwrap
from functools import cache

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parent / "H10-quartics"
REPO = HERE.parents[1] / "diophantine"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--route", choices=["general25", "explicit27"], required=True)
    ap.add_argument("--L", type=int, default=143)
    ap.add_argument("--retain-square-scales", action="store_true")
    ap.add_argument("--output", type=Path, default=HERE/"four_contact")
    args = ap.parse_args()
    assert args.L >= 3 and args.L % 2
    sys.argv = ["positive.py", "--termwise", "--route", args.route,
                "--parameter", str(args.L), "--repo", str(REPO)]
    positive = load("four_contact_positive", ARCHIVE/"fewvars/positive.py")
    parent = load("four_contact_chart", positive.BASE/"even_valuation25_v75/build_source.py")
    parent.patch()
    import build_sources as upstream
    base = upstream.General25 if args.route == "general25" else upstream.Explicit27

    class Revised(base):
        point = parent.FullAuxiliary25.point

    body = textwrap.dedent(inspect.getsource(base.build))
    edits = [
        ("for C,order in zip(tests,comparison_orders):",
         "for i,(C,order) in enumerate(zip(tests,comparison_orders)):"),
        ("self.scale(self.square(C),weight)",
         "self.scale(C if i<10 else self.square(C),weight)"),
        ("beta=216*self.X**4+450459", "beta=1632*self.X**2+2477"),
        ("self.sub(L[0],self.field(beta))", "self.sub(L[0],self.field(self.X**2+1))"),
        ("32*beta+343,2*beta-1", "32*beta+343"),
        ("scalar_denominator=1+17*(prime_power+1)*raw",
         "A=beta*(beta-1)\n    B=(beta-2401)*(32*beta+343)\n"
         "    T=(1224*(prime_power+1))**2\n    scalar_denominator=B+T*A"),
        ("102**2*contact_power*raw/(scalar_denominator**2)",
         "102**2*contact_power*T*raw/(scalar_denominator**2)"),
    ]
    for before, after in edits:
        assert body.count(before) == 1, before
        body = body.replace(before, after)
    if args.route == "explicit27" and not args.retain_square_scales:
        for before, after in [
            ("(1+rs*aggregate[0]**2)**2", "1+rs*aggregate[0]**2"),
            ("(1+rs*(aggregate[0]+aggregate[1])**2)**2", "1+rs*(aggregate[0]+aggregate[1])**2"),
        ]:
            assert body.count(before) == 1
            body = body.replace(before, after)
    assert body.count("76249") == 2
    body = body.replace("76249", "67")
    Revised.build = positive.transform(body, base.build.__globals__)
    native = Revised(args.L).build()
    native.update(
        format="point-block-guarded-source/four-contact-scalar-v78",
        proof="four_contact_scalar_20261119_v78.tex",
        positive_balancing=False, positive_detector_factors=True,
        squared_reciprocal_traces=False,
        arithmetic_status="Under the explicitly retained arithmetic premises; four-contact scalar transfer.",
        target="X^2+1", scalar_prime=67,
        unsquared_scales=args.route == "general25" or not args.retain_square_scales,
    )
    native["family_parameter"].update(
        certified_sufficient_lower_bound=143 if args.route == "explicit27" else None,
        selected_member_certified_to_define_Z=args.route == "explicit27" and args.L >= 143,
    )
    for event in native["events"]:
        if event["operation"] in ("comparison_and_scalar_tests", "combined_detector"):
            event["comparison_powers"] = [1]*10+[2]*6
    specification = parent.helper.old._subalgebra.compile_specification(native)
    certificate = positive.calculate(native, specification)
    destination = args.output/args.route
    destination.mkdir(parents=True, exist_ok=True)
    for name, value in (("native", native), ("parent", specification), ("certificate", certificate)):
        (destination/(name+".json")).write_text(json.dumps(value, sort_keys=True, separators=(",", ":"))+"\n")
    nodes = native["coefficient_dag"]
    @cache
    def atoms(i):
        op, *values = nodes[i]
        if op == "int":
            assert values[0]
            return set()
        if op in ("neg", "pow"):
            return atoms(values[0]) if op == "neg" or values[1] else set()
        if op == "mul":
            return set().union(*(atoms(j) for j in values))
        return {i}
    scale = next(e for e in native["events"] if e["operation"] == "combined_height_scales")
    early = set()
    for fraction in [scale["scalar_contact"], scale["scalar_denominator"], *scale["scales"]]:
        early |= atoms(fraction["numerator"]) | atoms(fraction["denominator"])
    early &= set(certificate["norm_guard_nodes"])
    index = {tuple(row): i for i, row in enumerate(nodes)}
    point_atoms = set()
    point_blocks = {b["name"]: b for b in native["finite_blocks"] if b["kind"] == "point_block"}
    for event in (e for e in native["events"] if e["operation"] == "point_block"):
        h0, h1 = event["h"]
        assert h0["denominator"] == h1["denominator"] == index[("int", 1)]
        a = index[("pow", h0["numerator"], 2)]
        b = index[("pow", h1["numerator"], 2)]
        negative = index[("mul", *sorted([index[("int", -1)], index[("int", 2)], b]))]
        point_atoms.add(index[("add", *sorted([a, negative]))])
        if event.get("chart") != "full_auxiliary":
            point_atoms.add(point_blocks[event["name"]]["variable_nodes"][2])
    assert len(point_atoms) == 13 and point_atoms <= set(certificate["norm_guard_nodes"])
    assert not point_atoms & early
    removed = early | point_atoms
    factors = {r["node"]:r for r in specification["subalgebra_norm_factors"]}
    degree_saved = sum(factors[i]["scalar_norm_degree_bound"] for i in removed)
    log_saved = sum(factors[i]["scalar_norm_log2_l1_bound"] for i in removed)
    reduced = dict(certificate)
    reduced["early_positive_atoms"] = sorted(early)
    reduced["automatic_point_atoms"] = sorted(point_atoms)
    reduced["norm_guard_nodes"] = sorted(set(certificate["norm_guard_nodes"])-removed)
    reduced["guard_degree"] -= degree_saved
    reduced["degree"] -= reduced["rank"]*degree_saved
    reduced["log2_l1"] -= reduced["rank"]*log_saved
    reduced["height_double_power"] = reduced["log2_l1"].bit_length()
    n = reduced["rank"]
    d = reduced["degree"]-int(native["multiply_by_input"])
    v = native["total_external_variables"]
    reduced["support_power"] = (math.comb(d+v,v)-math.comb(d-n+v-1,v)).bit_length()
    reduced["extra_witness_degree"] = 2*max(1+reduced["guard_degree"], n*(1+reduced["separator_degree"]))+int(native["multiply_by_input"])
    (destination/"reduced.json").write_text(json.dumps(reduced, sort_keys=True, separators=(",", ":"))+"\n")
    if args.route == "general25":
        sys.argv = ["projective.py", "--source", str(args.output)]
        projective = load("four_contact_projective", ARCHIVE/"fewvars/projective.py")
        proj = projective.bounds("general25")
        proj["early_positive_atoms"] = sorted(early)
        proj["automatic_point_atoms"] = sorted(point_atoms)
        proj["guard_degree"] -= degree_saved
        proj["degree"] -= n*degree_saved
        proj["log2_l1"] -= n*log_saved
        proj["height_double_power"] = proj["log2_l1"].bit_length()
        d = proj["degree"]
        proj["support_power"] = (math.comb(d+v,v)-math.comb(d-n+v-1,v)).bit_length()
        (destination/"projective.json").write_text(json.dumps(proj, sort_keys=True, separators=(",", ":"))+"\n")
        print("Projective", proj)
    print("Early positivity", {key:reduced[key] for key in ("degree", "guard_degree", "log2_l1", "height_double_power", "support_power")})
    print({key:certificate[key] for key in ("route", "degree", "guard_degree", "separator_degree", "rank", "log2_l1", "height_double_power", "support_power")})


if __name__ == "__main__":
    main()
