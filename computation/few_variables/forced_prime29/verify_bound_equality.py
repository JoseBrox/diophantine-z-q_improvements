#!/usr/bin/env python3
"""Verify that the refined coefficient bound describes the identical polynomial.

The certificate stores only the preceding bound annotations and hashes.
Replacing the current bound annotations by these recorded annotations must
reconstruct the complete preceding specification byte for byte. Removing
all annotations must give the same mathematical-data hash in both cases.
"""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent

def digest(data): return hashlib.sha256(data).hexdigest()
def encode(obj): return (json.dumps(obj,separators=(',',':'))+'\n').encode()

def main():
    raw=(HERE/'polynomial-specification.json').read_bytes()
    new=json.loads(raw)
    certificate=json.loads((HERE/'coefficient-bound-equality.json').read_text())
    assert certificate['removed_field']=='bounds'
    old=dict(new);old['bounds']=certificate['original_bounds']
    assert digest(encode(old))==certificate['original_specification_sha256']
    old_core=dict(old);old_core.pop('bounds')
    new_core=dict(new);new_core.pop('bounds')
    assert old_core==new_core
    assert digest(encode(new_core))==certificate['mathematical_data_sha256']
    assert new['source_json_sha256']==certificate['unchanged_source_sha256']
    assert old['bounds']['degree_bound']==new['bounds']['degree_bound']
    assert old['bounds']['coefficient_height_log2_bound']>new['bounds']['coefficient_height_log2_bound']
    assert new['bounds']['degree_bound_power_of_two_exponent']==174
    assert new['bounds']['coefficient_height_bound_double_power_of_two_exponent']==177
    report={'status':'passed','identical_mathematical_specification':True,'only_bounds_changed':True,'exact_degree_majorant_unchanged':True,'mathematical_data_sha256':digest(encode(new_core)),'original_specification_sha256':digest(encode(old)),'refined_specification_sha256':digest(raw),'degree_bound_power_of_two_exponent':174,'coefficient_height_bound_double_power_of_two_exponent':177,'checker_sha256':digest(Path(__file__).read_bytes())}
    (HERE/'coefficient-bound-equality-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
