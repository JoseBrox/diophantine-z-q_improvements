"""Build a finite 11-variable coefficient specification from the pinned upstream compiler."""
import argparse
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import sys
import textwrap

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PARAMETERS = {"weak": (6, 8, 21), "strong": (4, 5, 8),
              "weak-compact": (8, 1, 18), "strong-compact": (6, 1, 6)}
SHIFTS = [0, 15, 20, 24, 30, 60]


def contact(builder, beta, trace, parameters, compact):
    d, m, cutoff = parameters
    scale = beta**d + trace**d
    a = scale**m
    left = a - builder.z
    right = a + builder.z

    def shifted_product(point):
        value = builder.c.rational(1)
        for shift in SHIFTS:
            value = value * (point + shift)
        return value

    g, h = shifted_product(left), shifted_product(right)
    linear, product = g + h, g * h
    cubic = linear**3 + g**2*h**2
    quadratic = linear**2 + g**2*h
    denominator = cubic * quadratic * (g**cutoff+h) * (g+h**cutoff)
    weight = product**5 * (1 + denominator*product)**2 / denominator
    if compact:
        normalization = 1 + scale**(3*m*(cutoff+11))*product
        builder.c.nonzero(normalization, "contact.scale_normalizer")
        weight = weight / normalization**2
    for value, label in [(scale, "height.M"), (product, "contact.F"),
                         (denominator, "contact.Q"), (weight, "contact.u"),
                         (1 + weight, "contact.one_plus_u")]:
        builder.c.nonzero(value, label)
    event = dict(
        operation="weak_abc_collision_resolvent", shifts=SHIFTS, d=d, m=m, K=cutoff,
        **{name:builder.rr(value) for name, value in
           dict(beta=beta, T=trace, M=scale, a=a, x=left, y=right, g=g, h=h,
                L=linear, F=product, N=cubic, D=quadratic, Q=denominator, u=weight).items()})
    if compact:
        event["normalization"] = builder.rr(normalization)
    return weight, event


def build(compiler_file, output, shift, flavor):
    modspec = importlib.util.spec_from_file_location("weak_eleven_parent", compiler_file)
    parent = importlib.util.module_from_spec(modspec)
    modspec.loader.exec_module(parent)
    body = textwrap.dedent(inspect.getsource(parent.Derivative11.build))
    start, end = body.index("    M = beta**4"), body.index("    w =")
    body = body[:start] + "    u, event = contact(self, beta, trace, parameters, compact)\n" + body[end:]
    start, end = body.index("        dict(operation='moving_contact_height'"), body.index("        dict(operation='balanced_actual_detector'")
    body = body[:start] + "        event,\n" + body[end:]
    env = dict(parent.__dict__, contact=contact, parameters=PARAMETERS[flavor], compact=flavor.endswith("-compact"))
    exec(compile(body, __file__, "exec"), env)
    parent.Derivative11.build = env["build"]
    source = parent.make_source(shift)
    source.update(name=flavor+"_abc11_collision_resolvent",
                  format="guarded-11-coordinate-source/collision-resolvent",
                  proof="proof.md", arithmetic_status=(
                      "Fixed weak rational abc exponent " +
                      ("121/100" if flavor.startswith("weak") else "16/15") +
                      " and the retained v63 elliptic, prime preparation, trace and intrinsic pole inputs."))
    output.mkdir(parents=True, exist_ok=True)
    parent._terminal.ROOT = output
    base_path = output/"subalgebra_parent.json"
    base = parent.parent_specification(source)
    base["native_source_generator"] = "build.py"
    base_path.write_text(json.dumps(base, indent=2)+"\n")
    spec = parent._terminal.compile_specification(source, base, base_path)
    spec["native_source_generator"] = "build.py"
    spec["arithmetic_scope"] = source["arithmetic_status"]
    source_path = output/"source.json"
    source_path.write_bytes(parent.canonical(source))
    spec_path = output/"polynomial.json"
    spec_path.write_text(json.dumps(spec, indent=2)+"\n")
    bounds = spec["bounds"]
    report = dict(name=source["name"], parameters=PARAMETERS[flavor], shift=shift,
                  shift_certified=False, compiler_sha256=hashlib.sha256(compiler_file.read_bytes()).hexdigest(),
                  hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (source_path, base_path, spec_path)},
                  nodes=len(source["coefficient_dag"]), guards=len(source["guard_numerators"]),
                  **{k:bounds[k] for k in ("degree_bound", "support_strict_power_of_two",
                                            "total_variables", "full_rank")})
    (output/"certificate.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=HERE.parents[1]/"source")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--shift", type=int, default=3)
    parser.add_argument("--flavor", choices=PARAMETERS, default="weak")
    args=parser.parse_args()
    build(args.repo.resolve()/"computation/few_variables/derivative11_v63/build_source.py",
          (args.output or HERE/args.flavor).resolve(), args.shift, args.flavor)
