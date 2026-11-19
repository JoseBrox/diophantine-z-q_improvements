"""Bounds for the compact separator on a guarded, single-pole source."""
from functools import cache
from math import comb


def encode(source,parent,keep_balance=False):
    nodes=source["coefficient_dag"]
    @cache
    def factors(i):
        op,*ys=nodes[i]
        if op=="int":
            assert ys[0]
            return set()
        if op=="neg":return factors(ys[0])
        if op=="pow":return factors(ys[0]) if ys[1] else set()
        if op=="mul":return set.union(*(factors(j) for j in ys))
        return {i}
    root=source["finite_blocks"][-1]["generator_node"]
    native=set.union(*(factors(i) for i in source["guard_numerators"] if i!=root))
    assert root not in native
    u=next(e for e in source["events"] if e["operation"]=="moving_contacts")["u"]
    early=set(factors(u["numerator"])|factors(u["denominator"]))
    intermediate=set()
    norm1=set()
    tests=[e for e in source["events"] if e["operation"]=="test"]
    for e in tests:
        for c in [*e["C"],*e["den"],e["den_norm"]]:early.update(factors(c["denominator"]))
        for c in [*e["t"],*e["summand"]]:intermediate.update(factors(c["denominator"]))
        norm1.update(factors(e["den_norm"]["numerator"]))
    e=next(e for e in source["events"] if e["operation"]=="detector")
    for c in [*e["W"],e["norm"]]:intermediate.update(factors(c["denominator"]))
    norm2=factors(e["W"][0]["numerator"])|factors(e["norm"]["numerator"])
    guaranteed_1=(native&norm1)-early
    if keep_balance:guaranteed_1=set()
    guaranteed_2=(native&norm2)-early-intermediate-guaranteed_1
    kept=native-guaranteed_1-guaranteed_2
    assert early<=kept and intermediate<=kept|guaranteed_1
    rows=[f for f in parent["subalgebra_norm_factors"] if f["node"] in kept]
    assert len(rows)==len(kept)
    gd=sum(x["scalar_norm_degree_bound"] for x in rows)
    gh=sum(x["scalar_norm_log2_l1_bound"] for x in rows)
    tower=parent["quadratic_tower"]
    pole=tower[-1]
    w=pole["root_weight"];h=pole["root_operator_log2_norm"]
    wd=pole["envelope_degree"];hd=2+pole["envelope_log2_l1"]
    for p in reversed(tower[:-1]):
        w=p["root_weight"]+max(w,wd);h=p["root_operator_log2_norm"]+1+max(h,hd)
        wd+=p["envelope_degree"];hd+=2+p["envelope_log2_l1"]
    n=parent["bounds"]["full_rank"];v=parent["bounds"]["total_variables"]
    d=n*(1+gd+w);lc=n*(1+gh+h)
    count=comb(d+v,v)-comb(d-n+v-1,v)
    return dict(rank=n,variables=v,native_source_sha256=parent["native_source_sha256"],
                suppressed_pole_node=root,positive_balancing_atoms=sorted(guaranteed_1),
                positive_product_atoms=sorted(guaranteed_2),retained_norm_atoms=sorted(kept),
                guard_degree=gd,separator_degree=w,degree_bound=d+int(source["multiply_by_input"]),
                support_power=count.bit_length(),coefficient_log2_l1=lc,coefficient_double_power=lc.bit_length())
