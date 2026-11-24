"""Read-only independent audit of the theta-block deletion."""
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
def digest(b): return hashlib.sha256(b).hexdigest()
def gitblob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def named(table,row):
    d={}
    for t in row['terms']:
        key=tuple(sorted(table['variable_names'][i-1] for i in t['monomial']))
        assert key not in d
        d[key]=t['coefficient']
    return d
def pos(role,term,constant):
    out={():constant,(term,):'2'}
    for j in range(1,4):
        v=f'positive_{role}_{j}'
        out[(v,)]=out[(v,v)]='-1'
    return out
for c in json.loads((HERE/'certificate.json').read_text())['routes']:
    p=(ROOT/c['source']).read_bytes()
    assert digest(p)==c['source_sha256'] and gitblob(p)==c['source_git_blob']
    old=json.loads(p)
    b=(HERE/(c['route']+'_quadrics.json')).read_bytes()
    assert gitblob(b)==c['table_git_blob']
    new=json.loads(b)
    removed={f'positive_theta_{j}' for j in range(1,4)}
    assert set(old['variable_names'])-set(new['variable_names'])==removed
    assert new['variable_names']==[v for v in old['variable_names'] if v not in removed]
    assert old['variables']==c['old_variables'] and new['variables']==c['new_variables']==old['variables']-3
    assert len(old['residuals'])==c['old_rows'] and len(new['residuals'])==c['new_rows']==c['old_rows']-1
    o={r['name']:named(old,r) for r in old['residuals']}
    n={r['name']:named(new,r) for r in new['residuals']}
    assert o.pop('jones1980.positive.theta')==pos('theta','B5','-4*z - 2')
    for role,term,param in [('t','ell','u'),('m','e','y')]:
        assert o.pop('jones1980.positive.'+role)==pos(role,role,'-2')
        assert n.pop('jones1980.positive.'+term+'_minus_'+param)==pos(role,term,f'-2*{param} - 2')
    assert n==o and len(n)==c['unchanged_rows']
    assert new['parameters']==old['parameters']
    support={i for r in new['residuals'] for t in r['terms'] for i in t['monomial']}
    assert support==set(range(1,new['variables']+1))
    assert all(len(t['monomial'])<=2 for r in new['residuals'] for t in r['terms'])
    assert o['jones1980.positive.g'][('positive_g_1','positive_g_1')]=='-1'
    print(c['route'],new['variables'],len(new['residuals']),'PASS')
