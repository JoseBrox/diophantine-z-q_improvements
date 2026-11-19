"""Compile the three-scale L=117 source with the v72/75 auxiliary point charts."""
from pathlib import Path
import importlib.util
import inspect
import json
import sys
import textwrap

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
REPO = PROJECT / "source"
OUTPUT = HERE / "compact117" / "explicit27"


def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def compile_member():
    sys.argv = ["positive.py", "--termwise", "--route", "explicit27", "--parameter", "117", "--repo", str(REPO)]
    pos = load_module("effective_positive", PROJECT / "fewvars" / "positive.py")
    parent = load_module("effective_chart", pos.BASE / "even_valuation25_v75" / "build_source.py")
    parent.patch()
    import build_sources as upstream

    class Full27(upstream.Explicit27):
        point = parent.FullAuxiliary25.point

    body = textwrap.dedent(inspect.getsource(upstream.Explicit27.build))
    for old, new in [
        ("for C,order in zip(tests,comparison_orders):", "for i,(C,order) in enumerate(zip(tests,comparison_orders)):"),
        ("self.scale(self.square(C),weight)", "self.scale(C if i<10 else self.square(C),weight)"),
    ]:
        assert body.count(old) == 1
        body = body.replace(old, new)
    edits = [
        ("beta=216*self.X**4+450459", "beta=102*self.X**2+2957"),
        ("32*beta+343,2*beta-1", "32*beta+343,beta+24"),
    ]
    for previous, revised in edits:
        assert body.count(previous) == 1
        body = body.replace(previous, revised)
    assert body.count("76249") == 2
    body = body.replace("76249", "167")
    # Normalize a positive rational A/B. Its reduced numerator and
    # denominator give a square denominator after t -> t/(1+t)^2.
    mark = "scalar_denominator=1+17*(prime_power+1)*raw"
    pieces = """A=beta*(beta-1)*(beta-2401)
    B=(32*beta+343)*(beta+24)
    T=(102*(prime_power+2))**2
    scalar_denominator=B+T*A"""
    assert body.count(mark)==1
    body = body.replace(mark,pieces)
    assert body.count("102**2*contact_power*raw/(scalar_denominator**2)")==1
    body = body.replace("102**2*contact_power*raw/(scalar_denominator**2)",
                       "102**2*contact_power*T*raw/(scalar_denominator**2)")
    Full27.build = pos.transform(body, upstream.Explicit27.build.__globals__)
    source = Full27(117).build()
    source.update(format="point-block-guarded-source/full-three-scale",
                  auxiliary_chart="Four root points use square abscissas. Five auxiliary points use full abscissas.",
                  proof="PROOF.md and COMPACT.md", positive_balancing=False,
                  positive_detector_factors=True, squared_reciprocal_traces=False,
                  arithmetic_status="Defining member at L=117 under retained arithmetic premises.")
    source["family_parameter"].update(certified_sufficient_lower_bound=117, selected_member_certified_to_define_Z=True)
    for event in source["events"]:
        if event["operation"] in ("comparison_and_scalar_tests", "combined_detector"):
            event["comparison_powers"] = [1]*10 + [2]*6
    parent_spec = parent.helper.old._subalgebra.compile_specification(source)
    certificate = pos.calculate(source, parent_spec)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, obj in (("native", source),("parent", parent_spec),("certificate", certificate)):
        (OUTPUT / (name + ".json")).write_text(json.dumps(obj,sort_keys=True,separators=(",",":")) + "\n")
    return {k:certificate[k] for k in ("source_sha256","degree","separator_degree","guard_degree","height_double_power","log2_l1","support_power")}


if __name__ == "__main__":
    print(compile_member())
