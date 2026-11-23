# v88 continuation of the v78 sources and Gabe Conant notes with Astra 6.2.
# The archived files are materialized and hash-checked by scripts/verify_v88.py.
"""Compile twelve derivative contacts at the first height scale."""
from pathlib import Path
import argparse
import importlib.util
import json
import math
import sys
from functools import cache

HERE=Path(__file__).resolve().parent
ARCHIVE=HERE.parent/"H10-quartics"
REPO=HERE.parents[1]/"diophantine"
SHIFTS=[-9,-8,-7,-5,-4,-3,-2,-1,6,10,11,12]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--B",type=int,default=3)
    parser.add_argument("--dg",type=int,default=0)
    parser.add_argument("--dh",type=int,default=0)
    parser.add_argument("--output",type=Path,default=HERE/"twelve")
    options=parser.parse_args()
    assert options.B >= 3 and options.B % 2
    sys.argv=["positive.py","--termwise","--balanced","--route","abc11","--repo",str(REPO),"--parameter",str(options.B)]
    code=(ARCHIVE/"fewvars/positive.py").read_text()
    before='        if args.balanced:\n            start=text.index("        if i < 2:")'
    extra='''        assert text.count("M**(8 if self.contact_count == 7 else 4)")==1
        text=text.replace("M**(8 if self.contact_count == 7 else 4)","M")
        old_shifts="([-7,-6,-4,1,3,5,8] if self.contact_count == 7 else [-10,-8,-5,1,2,3,4,6,7])"
        assert text.count(old_shifts)==1
        text=text.replace(old_shifts, "[-9,-8,-7,-5,-4,-3,-2,-1,6,10,11,12]")
        old_pole="radicand = eta*(eta+self.v**2)**2*self.s**4 - eta*(eta-self.v**2)**2*(1-eta)**2"
        assert text.count(old_pole)==1
        text=text.replace(old_pole,"d = REPLACE_D\\n    radicand = (1-eta)*(self.v**4-d**2)*(self.s**4-d**2)")
'''
    expression="7*u"
    if options.dg:
        expression+=("*" if options.dg>0 else "/")+f"G**({2*abs(options.dg)})"
    if options.dh:
        expression+=("*" if options.dh>0 else "/")+f"primitive_denominator**({2*abs(options.dh)})"
    extra=extra.replace("REPLACE_D",expression)
    assert code.count(before)==1
    namespace={"__name__":"twelve_source_positive", "__file__":str(ARCHIVE/"fewvars/positive.py")}
    exec(compile(code.replace(before,extra+before),"twelve_source_positive","exec"),namespace)
    source,compiler=namespace["native"]("abc11")
    obsolete=[node for node,label in source["guard_descriptions"] if label=="height.nonzero signed argument"]
    assert len(obsolete)==1
    assert all(node not in obsolete or label=="height.nonzero signed argument" for node,label in source["guard_descriptions"])
    source["guard_numerators"]=[i for i in source["guard_numerators"] if i not in obsolete]
    source["guard_descriptions"]=[entry for entry in source["guard_descriptions"] if entry[0] not in obsolete]
    source.update(contact_count=12,scale_exponent=1,
                  square_class_exponents=[options.dg,options.dh],
                  positive_balancing=True,positive_detector_factors=True,
                  squared_reciprocal_traces=False,
                  balancing="Positive sum-of-squares denominators; first four tests use their even valuations.",
                  name="ordinary_abc11_bb_product_v88",
                  proof="bb_product_degree_transfer_20261123_v88.tex",
                  deleted_signed_argument_guard=obsolete,
                  arithmetic_status="Ordinary rational abc and retained elliptic, height and prime-pattern inputs; BB v2 Lemma 2.2 supplies the pole. The sufficient odd shift remains ineffective.")
    for block in source["finite_blocks"]:
        if block["kind"] == "pole":
            block["zero_stratum_rule"] = ("Terminal zero roots are allowed in the published v88 positive encoder. "
                "The inherited source-level ordinate guard is explicitly removed by the final certificate; "
                "no denominator or retained guard may depend on a terminal pole root.")
    source["final_pole_policy"] = {"terminal_zero_roots_allowed": True,
        "source_ordinate_guards_removed_by_final_encoder": True,
        "standalone_legacy_guarded_source_is_not_the_published_polynomial": True}
    spec=compiler(source)
    certificate=namespace["calculate"](source,spec)
    output=options.output/"abc11"
    output.mkdir(parents=True,exist_ok=True)
    for name,obj in [("native",source),("parent",spec),("certificate",certificate)]:
        (output/(name+".json")).write_text(json.dumps(obj,sort_keys=True,separators=(",",":"))+"\n")
    nodes=source["coefficient_dag"]
    @cache
    def atoms(i):
        op,*ys=nodes[i]
        if op=="int":
            assert ys[0]
            return set()
        if op in ("neg","pow"):
            return atoms(ys[0]) if op=="neg" or ys[1] else set()
        if op=="mul":
            return set().union(*(atoms(j) for j in ys))
        return {i}
    guaranteed=[node for node,label in source["guard_descriptions"] if label in ("height.M","contact.one_plus_u")]
    assert len(guaranteed)==2
    automatic=set().union(*(atoms(i) for i in guaranteed))&set(certificate["norm_guard_nodes"])
    index={tuple(row):i for i,row in enumerate(nodes)}
    point_atoms=set()
    blocks={b["name"]:b for b in source["finite_blocks"] if b["kind"]=="point_block"}
    for event in (e for e in source["events"] if e["operation"]=="point_block"):
        h0,h1=event["h"]
        assert h0["denominator"]==h1["denominator"]==index[("int",1)]
        a=index[("pow",h0["numerator"],2)]; b=index[("pow",h1["numerator"],2)]
        negative=index[("mul",*sorted([index[("int",-1)],index[("int",2)],b]))]
        point_atoms.add(index[("add",*sorted([a,negative]))])
        if event.get("chart")!="full_auxiliary":
            point_atoms.add(blocks[event["name"]]["variable_nodes"][2])
    assert len(point_atoms)==4 and point_atoms<=set(certificate["norm_guard_nodes"])
    assert not point_atoms & automatic
    removed=automatic|point_atoms
    factors={r["node"]:r for r in spec["subalgebra_norm_factors"]}
    kept=set(certificate["norm_guard_nodes"])-removed
    final=dict(certificate)
    final["automatic_height_atoms"]=sorted(automatic)
    final["automatic_point_atoms"]=sorted(point_atoms)
    final["norm_guard_nodes"]=sorted(kept)
    dg=sum(factors[i]["scalar_norm_degree_bound"] for i in removed)
    lg=sum(factors[i]["scalar_norm_log2_l1_bound"] for i in removed)
    final["guard_degree"]-=dg
    final["degree"]-=128*dg
    final["log2_l1"]-=128*lg
    final["height_double_power"]=final["log2_l1"].bit_length()
    d=final["degree"]-1
    final["support_power"]=(math.comb(d+11,11)-math.comb(d-128+10,11)).bit_length()
    (output/"strengthened.json").write_text(json.dumps(final,sort_keys=True,separators=(",",":"))+"\n")
    print("Strengthened", {k:final[k] for k in ["degree","guard_degree","separator_degree","support_power","log2_l1","automatic_height_atoms"]})
    print({k:certificate[k] for k in ["degree","rank","guard_degree","separator_degree","support_power","log2_l1"]})


if __name__=="__main__":
    main()
