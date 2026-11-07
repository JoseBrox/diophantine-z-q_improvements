#!/usr/bin/env python3
"""Independent exact audit of the blocked detector source system.

No builder, finalizer, or compiler producer is imported.  The audit replays
constant-pivot elimination certificates, reconstructs the two new source
changes, and expands the final SOS by a separate polynomial implementation.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from collections import defaultdict, Counter
import hashlib
import json
import shutil
import subprocess
import tempfile

from exact_arithmetic import read_terms, normalize, sos, sha
from exact_arithmetic import add, product, fm

HERE = Path(__file__).resolve().parent
UP = HERE / "source"
SOURCE = UP / "blocked"
PACKAGE = HERE / "data/system485"
EXPECTED_COMPILED = 508
EXPECTED_FINAL = 485
REUSE_FOURTH_POWERS = True


def variables(p):
    return {v for m, s in p for v in m}


def degree(p):
    return max((len(m) for m, s in p), default=0)


def substitute(p, variable, replacement):
    result = {}
    for (m, s), a in p.items():
        term = {(tuple(v for v in m if v != variable), s): a}
        for _ in range(m.count(variable)):
            term = product(term, replacement)
        result = add((1, result), (1, term))
    return result


def scalar(p, factor):
    return {k: a * factor for k, a in p.items() if a * factor}


def audit_source_patch():
    original = (UP / "builders/odd-product-asymmetric-source.cjs").read_text()
    changed = (SOURCE / "build_source.cjs").read_text()
    old_line = "let coeffs={};for(let m of [1,40])coeffs[m]=polyProduct('symmetric.'+m,tests.filter(t=>t.order===m).map((t,j)=>fsq('testSquare.'+m+'.'+j,t.value)));"
    assert original.count(old_line) == 1
    fixed_marker = "start('fixed_height_scales',[3352,3405]);"
    start = changed.index("let coeffs={};")
    end = changed.index(fixed_marker, start)
    coefficient_region = changed[start:end]
    expected_coefficients = """let coeffs={};
const blockSizes={"1":[3,3,3],"40":[3,4]};
for(let m of [1,40]){
 const ys=tests.filter(t=>t.order===m).map((t,j)=>fsq('testSquare.'+m+'.'+j,t.value));
 let at=0;
 coeffs[m]=blockSizes[m].map((n,j)=>{
  const co=polyProduct('symmetric.'+m+'.block'+j,ys.slice(at,at+n));at+=n;return co;
 });
 if(at!==ys.length)throw Error('Wrong partition');
}
"""
    if REUSE_FOURTH_POWERS:
        old_loop = """ let at=0;
 coeffs[m]=blockSizes[m].map((n,j)=>{
  const co=polyProduct('symmetric.'+m+'.block'+j,ys.slice(at,at+n));at+=n;return co;
 });
 if(at!==ys.length)throw Error('Wrong partition');"""
        checked_loop = """ if(m===1){
  function saved(name){return new Map(values[name].terms.map(t=>[key(t.monomial,t.sPower||0),Q(...t.coefficient.split('/'))]));}
  const partitions=[[0,1,4],[2,3,5],[6,7,8]],thirdPoints=[0,1,4];
  coeffs[m]=partitions.map((ids,j)=>{
   const [a,b,c]=ids.map(i=>ys[i]),ab=fadd(a,b);
   const w2=[saved('logV'+thirdPoints[j]+'.wPower2.0'),saved('logV'+thirdPoints[j]+'.wPower2.1')];
   const c2=fconj(fmul('reusedFourthPower'+j,w2,fc(Q(193,2401),Q(132,2401))));
   const e2raw=fadd(rawFmul(a,b),rawFmul(ab,c));
   const e2=saveF('symmetric.1.block'+j+'.co2',e2raw.map((v,k)=>assign('symmetric.1.block'+j+'.co2.'+k,v)));
   const e3raw=fsub(rawFmul(e2,c),rawFmul(ab,c2));
   const e3=saveF('symmetric.1.block'+j+'.co3',e3raw.map((v,k)=>assign('symmetric.1.block'+j+'.co3.'+k,v)));
   return [fc(1),fadd(ab,c),e2,e3];
  });
 }else{
  let at=0;
  coeffs[m]=blockSizes[m].map((n,j)=>{
   const co=polyProduct('symmetric.'+m+'.block'+j,ys.slice(at,at+n));at+=n;return co;
  });
  if(at!==ys.length)throw Error('Wrong partition');
 }"""
        assert expected_coefficients.count(old_loop) == 1
        expected_coefficients = expected_coefficients.replace(old_loop, checked_loop)
    assert coefficient_region == expected_coefficients + "\n"
    reduced_new = changed[:start] + "COEFFICIENT_REGION\n" + changed[end:]
    reduced_old = original.replace(old_line + "\n", "COEFFICIENT_REGION\n")
    evaluation_start = "function evalSym(name,"
    evaluation_end = "function pole(name,b,p,prep){"
    def separate(text):
        a = text.index(evaluation_start)
        b = text.index(evaluation_end, a)
        return text[:a], text[a:b], text[b:]
    op, old_evaluation, os = separate(reduced_old)
    np, evaluation, ns = separate(reduced_new)
    assert op == np and os == ns, "Changes outside the two stated circuit regions"
    expected_evaluation = """function evalSym(name,blocks,q){
 const top=Math.max(...blocks.map(c=>c.length-1));
 const powers=[one,q];
 for(let k=2;k<=top;k++)powers[k]=rm(name+'.power'+k,powers[Math.floor(k/2)],powers[Math.ceil(k/2)]);
 const evaluated=blocks.map((co,b)=>{
  const out=[zero,zero];
  for(let k=0;k<co.length;k++)for(let j=0;j<2;j++)out[j]=add(out[j],mul(co[k][j],powers[k]));
  return saveF(name+'.block'+b,[assign(name+'.block'+b+'.0',out[0]),assign(name+'.block'+b+'.1',out[1])]);
 });
 let out=evaluated[0];
 for(let j=1;j<evaluated.length;j++)out=fmul(name+'.join'+j,out,evaluated[j]);
 return saveF(name,out);
}
"""
    assert evaluation == expected_evaluation
    # Universal identity in Z[Y_1,...,Y_n,q].  A monomial is recorded by
    # its Y-index subset; the q-exponent is its cardinality.
    universal = {}
    for order, sizes in [(1, (3, 3, 3)), (40, (3, 4))]:
        count = sum(sizes)
        start = 0
        accumulated = {frozenset(): 1}
        groups = [[0,1,4],[2,3,5],[6,7,8]] if REUSE_FOURTH_POWERS and order == 1 else None
        for block_index, size in enumerate(sizes):
            indices = groups[block_index] if groups is not None else range(start, start+size)
            block = {frozenset(c): 1 for k in range(size+1) for c in combinations(indices, k)}
            next_product = defaultdict(int)
            for a, x in accumulated.items():
                for b, y in block.items():
                    assert not (a & b)
                    next_product[a | b] += x*y
            accumulated = dict(next_product)
            start += size
        expected = {frozenset(c): 1 for k in range(count+1) for c in combinations(range(count), k)}
        assert accumulated == expected and len(expected) == 2**count
        powers = [0, 1]
        for k in range(2, max(sizes)+1):
            powers.append(powers[k//2] + powers[(k+1)//2])
            assert powers[k] == k
        universal[str(order)] = {"partition": sizes, "factorCount": count, "universalMonomialsChecked": len(expected)}
    reuse_checks = None
    if REUSE_FOURTH_POWERS:
        a,b,c = [{((j,),0):Q(1)} for j in range(3)]
        ab = add((1,a),(1,b))
        e2 = add((1,product(a,b)),(1,product(ab,c)))
        e3 = add((1,product(e2,c)),(-1,product(ab,product(c,c))))
        assert e2 == add((1,product(a,b)),(1,product(a,c)),(1,product(b,c)))
        assert e3 == product(product(a,b),c)
        # (193-132*sqrt(2))*(193+132*sqrt(2))/2401=1.
        assert 193**2-2*132**2 == 2401
        assert [4,5,8] == [4+j for j in [0,1,4]]
        reuse_checks = {"cubicIdentities": "e2=ab+(a+b)c; e3=e2*c-(a+b)c^2=abc",
                        "thirdFactorIndices": [4,5,8], "alternatePointIndices": [0,1,4],
                        "constantFieldInverse": "D^(-2)=(193+132*sqrt(2))/2401",
                        "orderOfOperations": "Conjugation is applied after division by D^2, so the reused value is conjugate(f(V)^4)."}
    return {"onlyTwoRegionsChanged": True, "upstreamBuilderSha256": sha(UP / "builders/odd-product-asymmetric-source.cjs"),
            "blockedBuilderSha256": sha(SOURCE / "build_source.cjs"), "universalProductIdentities": universal,
            "reusedFourthPowerIdentities": reuse_checks}


def replay_raw_builder_and_gate_checker():
    node = shutil.which("node")
    assert node
    with tempfile.TemporaryDirectory(prefix="source-audit-", dir=HERE) as temp:
        directory = Path(temp)
        shutil.copy2(SOURCE / "build_source.cjs", directory / "build_source.cjs")
        subprocess.run([node, str(directory / "build_source.cjs")], check=True, capture_output=True, text=True)
        assert (directory / "raw-translated-ir.json").read_bytes() == (SOURCE / "raw-translated-ir.json").read_bytes()
        report_path = directory / "gate-check.json"
        command = [node, str(UP / "tools/checker.cjs"), "--input", str(SOURCE / "raw-translated-ir.json"),
                   "--compiled", str(SOURCE / "compiled/compiled-ir.json"), "--certificate", str(SOURCE / "compiled/reduction-certificate.json"),
                   "--coordinate-map", str(SOURCE / "compiled/coordinate-map.json"), "--quartic", str(SOURCE / "compiled/polynomial.json"),
                   "--report", str(report_path)]
        subprocess.run(command, check=True, capture_output=True, text=True)
        report = json.loads(report_path.read_text())
        assert report["status"] == "passed_exact_algebra_checks"
        assert not report["gateIdentities"]["unverified"]
        for artifact in report["artifactHashes"].values():
            assert sha(Path(artifact["file"])) == artifact["sha256"]
        return {"rawBuilderByteExactReplay": True, "upstreamIndependentGateIdentities": report["gateIdentities"]["checked"],
                "gateCheckerSha256": sha(UP / "tools/checker.cjs"), "unverifiedGates": []}


def replay_compiler():
    raw = json.loads((SOURCE / "raw-translated-ir.json").read_text())
    compiled = json.loads((SOURCE / "compiled/compiled-ir.json").read_text())
    cert = json.loads((SOURCE / "compiled/reduction-certificate.json").read_text())
    assert cert["inputSha256"] == sha(SOURCE / "raw-translated-ir.json")
    rows = {r["id"]: read_terms(r["terms"]) for r in raw["residuals"]}
    coords = {c["id"]: c for c in raw["coordinates"]}
    counts = Counter()
    for op in cert["operations"]:
        counts[op["kind"]] += 1
        if op["kind"] == "normalize":
            factor = Q(op["multiplier"])
            assert factor
            rows[op["residual"]] = scalar(rows[op["residual"]], factor)
            continue
        assert op["kind"] == "eliminate"
        x, pivot = op["coordinate"], op["pivot"]
        assert x != 0 and not coords[x].get("protected")
        p, q = rows[pivot], read_terms(op["replacement"])
        assert p[((x,), 0)] == Q(op["coefficient"])
        assert all(x not in m or (m, s) == ((x,), 0) for m, s in p)
        assert x not in variables(q) and substitute(p, x, q) == {}
        affected = {rid for rid, row in rows.items() if x in variables(row)}
        assert affected - {pivot} == set(op["affected"])
        for rid in affected - {pivot}:
            rows[rid] = substitute(rows[rid], x, q)
            assert degree(rows[rid]) <= 2
        del rows[pivot]
        del coords[x]
    assert rows == {r["id"]: read_terms(r["terms"]) for r in compiled["residuals"]}
    assert coords == {c["id"]: c for c in compiled["coordinates"]}
    assert len(coords) == EXPECTED_COMPILED and len(rows) == EXPECTED_COMPILED-31
    return compiled, rows, coords, dict(counts)


def main():
    source_patch = audit_source_patch()
    gate_replay = replay_raw_builder_and_gate_checker()
    source, rows, coords, compiler_counts = replay_compiler()
    cert = json.loads((PACKAGE / "transformation-certificate.json").read_text())
    emitted = json.loads((PACKAGE / "residuals.json").read_text())
    polynomial = json.loads((PACKAGE / "polynomial.json").read_text())
    report = json.loads((PACKAGE / "construction-report.json").read_text())
    assert cert["sourceSha256"] == emitted["sourceSha256"] == json.loads((HERE / "PROVENANCE.json").read_text())["originalSha256"]["source/blocked/compiled/compiled-ir.json"]
    assert cert["sourceCoordinates"] == EXPECTED_COMPILED and len(cert["steps"]) == 5
    row_meta = {r["id"]: r for r in source["residuals"]}
    names = {c["name"]: c["id"] for c in source["coordinates"]}
    row_names = {r["name"]: r["id"] for r in source["residuals"]}
    for step in cert["steps"]:
        assert step["kind"] == "eliminate_modulo"
        x, pivot = step["coordinate"], step["pivot"]
        assert x and not coords[x].get("protected")
        p, q = rows[pivot], read_terms(step["replacement"])
        assert p.get(((x,), 0)) and all(x not in m or (m, s) == ((x,), 0) for m, s in p)
        assert x not in variables(q) and substitute(p, x, q) == {}
        affected = {r for r, p in rows.items() if x in variables(p)}
        assert affected - {pivot} == {item["row"] for item in step["changes"]}
        assert len(step["changes"]) == len(affected)-1
        changes = {}
        for item in step["changes"]:
            expected = substitute(rows[item["row"]], x, q)
            for multiple in item["multiples"]:
                other, factor = multiple["row"], read_terms(multiple["factor"])
                assert other not in affected and x not in variables(factor)
                expected = add((1, expected), (1, product(factor, rows[other])))
            assert expected == read_terms(item["result"]) and degree(expected) <= 2
            changes[item["row"]] = expected
        rows.update(changes)
        del rows[pivot]
        del coords[x]
    assert len(coords) == EXPECTED_COMPILED-5 and len(rows) == EXPECTED_COMPILED-36

    # Independently reconstruct the parity/physical-anchor merge.
    merger = cert["mergedAnchor"]
    odd_coords = {i for i, c in coords.items() if ".odd." in c["name"]}
    odd_rows = {i for i in rows if ".odd." in row_meta[i]["name"]}
    assert len(odd_coords) == len(odd_rows) == 16
    assert odd_coords == set(merger["deletedCoordinates"]) and odd_rows == set(merger["deletedRows"])
    assert all(not (variables(p) & odd_coords) for i, p in rows.items() if i not in odd_rows)
    for x in odd_coords:
        del coords[x]
    for i in odd_rows:
        del rows[i]
    product_coords = []
    rescalings = {}
    for j in (0, 1):
        p = read_terms(source["values"][f"heightProduct.{j}"]["terms"])
        assert len(p) == 1
        (m, s), a = next(iter(p.items()))
        assert len(m) == 1 and s == 0
        x = m[0]
        factor = Q(1, 6*2**12) / a
        product_coords.append(x)
        rescalings[str(x)] = str(factor)
        rows = {i: substitute(p, x, {((x,), 0): factor}) for i, p in rows.items()}
    assert rescalings == merger["productRescalings"]
    f0, f1 = names["Sscalar.f.0"], names["Sscalar.f.1"]
    g = names["anchor.physicalA.quadratic"]
    assignment = row_names["anchor.physicalA.definition"]
    assert rows[assignment] == {((f0,f0),0):Q(1), ((f0,f1),0):Q(1), ((f1,f1),0):Q(-1), ((g,),0):Q(-1)}
    b0, b1 = product_coords
    assert [f0, f1] == merger["fCoordinates"] and g == merger["gCoordinate"]
    assert product_coords == merger["newProductCoordinates"] and assignment == merger["assignmentRow"]
    rows[assignment] = {((f0,f0),0):Q(6), ((f0,f1),0):Q(6), ((f1,f1),0):Q(-6), ((g,),0):Q(-6),
                        ((b0,b0),1):Q(1), ((b0,b1),1):Q(1), ((b1,b1),1):Q(-1)}

    # Independently check both old and new primary quotient equations and all
    # occurrences, retaining the original nonzero chart-domain obligations.
    primary = cert["primaryRatios"]
    v = lambda x: {((x,),0):Q(1)}
    pair = lambda prefix: [v(names[prefix+str(j)]) for j in (0,1)]
    hH, jH, zH = pair("H.chart.h"), pair("H.chart.j"), pair("U0.z.")
    z_ids = {names[f"U{i}.z.{j}"] for i in range(5) for j in (0,1)}
    z_rows = {row_names[f"U{i}.z.definition.{j}"] for i in range(5) for j in (0,1)}
    l_rows = {row_names[f"L{i}.definition.{j}"] for i in range(1,5) for j in (0,1)}
    assert z_ids == set(primary["deletedCoordinates"])
    assert z_rows == set(primary["deletedRows"]) and l_rows == set(primary["replacedRows"])
    assert all(not (variables(p) & z_ids) for i, p in rows.items() if i not in z_rows|l_rows)
    for j, value in enumerate(fm(jH,zH)):
        assert rows[row_names[f"U0.z.definition.{j}"]] == add((1,value),(1,hH[j]))
    replacement_rows = {}
    new_coordinate_ids = set()
    for i, (point, block) in enumerate(zip(("UA","US","UT","UZ"), primary["blocks"]), 1):
        assert block["i"] == i
        expected_names = {"hH":"H.chart.h", "jH":"H.chart.j", "h":point+".chart.h", "j":point+".chart.j", "L":f"L{i}."}
        for key, stem in expected_names.items():
            assert block[key] == [names[stem+str(j)] for j in (0,1)]
        h, j, ell, z = pair(point+".chart.h"), pair(point+".chart.j"), pair(f"L{i}."), pair(f"U{i}.z.")
        A = list(map(v, block["A"]))
        assert len(block["A"]) == 2 and not set(block["A"]) & (set(coords)|new_coordinate_ids)
        new_coordinate_ids.update(block["A"])
        for k in (0,1):
            assert rows[row_names[f"U{i}.z.definition.{k}"]] == add((1,fm(j,z)[k]),(1,h[k]))
            assert rows[row_names[f"L{i}.definition.{k}"]] == add((1,fm(zH,ell)[k]),(-1,z[k]))
            replacement_rows[row_names[f"L{i}.definition.{k}"]] = add((1,fm(A,ell)[k]),(-1,fm(h,jH)[k]))
        for k, x in enumerate(block["A"]):
            candidates = [r for r in emitted["residuals"] if r["name"] == f"primaryRatio{i}.denominator.definition.{k}"]
            assert len(candidates) == 1
            rid = candidates[0]["sourceId"]
            assert rid not in rows and rid not in replacement_rows
            replacement_rows[rid] = add((1,A[k]),(-1,fm(j,hH)[k]))
            coords[x] = {"id":x, "name":f"primaryRatio{i}.denominator.{k}"}
    assert len(new_coordinate_ids) == 8
    for x in z_ids:
        del coords[x]
    for i in z_rows:
        del rows[i]
    rows.update(replacement_rows)
    assert len(coords) == EXPECTED_FINAL and len(rows) == EXPECTED_FINAL-31
    assert all(degree(p) <= 2 for p in rows.values())
    assert set(coords) == set().union(*(variables(p) for p in rows.values()))
    mapping = {x:i for i,x in enumerate(sorted(coords))}
    assert mapping[0] == 0 and cert["oldToNew"] == {str(x):i for x,i in mapping.items()}
    assert [c["sourceId"] for c in emitted["coordinates"]] == sorted(coords)
    assert [c["id"] for c in emitted["coordinates"]] == list(range(EXPECTED_FINAL))
    assert [r["sourceId"] for r in emitted["residuals"]] == sorted(rows)
    expected_rows = []
    for final, rid in zip(emitted["residuals"], sorted(rows)):
        p, factor = normalize(rows[rid])
        assert factor == Q(cert["rowMultipliers"][str(rid)])
        p = {(tuple(sorted(mapping[x] for x in m)), s):a for (m,s),a in p.items()}
        assert p == read_terms(final["terms"])
        expected_rows.append(p)
    assert polynomial["coordinates"] == emitted["coordinates"]
    assert polynomial["fixedParameter"] == emitted["fixedParameter"] == {"name":"S","value":"3^(2^26)","coordinate":False}
    table = read_terms(polynomial["terms"])
    assert sos(expected_rows) == table
    assert degree(table) == 4 and table[((0,0,0,0),0)] == 1
    assert {x for m,s in table for x in m} == set(range(EXPECTED_FINAL))
    grouped = defaultdict(dict)
    for (m,s),a in table.items():
        assert a.denominator == 1 and 0 <= s <= 2
        grouped[m][s] = a.numerator
    u = mapping[names["anchor.U"]]
    assert grouped[(u,u)] == {2:64}
    bound = 0
    for m,c in grouped.items():
        if m == (u,u):
            continue
        assert abs(c.get(2,0)) <= 2
        bound = max(bound, abs(c.get(1,0))+abs(c.get(0,0)))
    assert bound.bit_length() == 1520 < 2**26
    assert len(grouped) == report["monomials"]
    assert len(table) == report["coefficientParameterTerms"]
    assert report["variables"] == EXPECTED_FINAL and report["quadraticResiduals"] == EXPECTED_FINAL-31
    assert report["exactCoefficientHeight"] == "64*3^(2^27)" and report["coefficientContent"] == 1
    for name, digest in report["sha256"].items():
        assert sha(PACKAGE/name) == digest
    receipt = {"status":"PASS", "independence":"No producer or finalizer imports. Independent polynomial arithmetic, explicit old/new quotient identities, complete certificate replay and coefficient comparison.",
               "sourcePatch":source_patch, "gateAndSourceReplay":gate_replay, "independentCompilerReplay":compiler_counts,
               "postCompilerEliminations":5, "mergedAnchorCoordinatesSaved":16, "directRatioCoordinatesSaved":2,
               "totalVariables":EXPECTED_FINAL, "existentialWitnesses":EXPECTED_FINAL-1, "quadraticResiduals":EXPECTED_FINAL-31, "degree":4,
               "ordinaryMonomials":len(grouped), "coefficientParameterTerms":len(table), "coefficientContent":1,
               "exactCoefficientHeight":"64*3^(2^27)", "lowerCoefficientEnvelopeBits":1520,
               "arithmeticScope":"The block-product change and direct quotient change are exact source identities. The merged anchor uses the separately proved semilocal/parity theorem on the upstream point domain. All inherited Diophantine arithmetic inputs remain unchanged; this finite checker does not prove them.",
               "fixedConstantNote":"All checked operations are over Q[S]. The raw source declares S=3^(2^27); the supplied baseline table specializes S=3^(2^26). The final456 construction supplies its own proved specialization.",
               "sha256":{name:sha(PACKAGE/name) for name in ["residuals.json","polynomial.json","transformation-certificate.json","construction-report.json"]}}
    (PACKAGE/"independent-verification.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__ == "__main__":
    main()
