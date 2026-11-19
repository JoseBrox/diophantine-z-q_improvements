"""Run the checks for the delivered quartics and finite-algebra degree bounds."""
import hashlib,json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent;src=root/'source'
def run(*args,cwd=root):
    subprocess.run([sys.executable,'-B',*map(str,args)],cwd=cwd,check=True)
q=root/'quartics'
phys=src/'computation/quartic/seven_units193_v74/primitive/laurent-source.json'
for name in ('general-physical','explicit-physical'):
    run(q/'check_physical.py',phys,q/name)
run(q/'check_balancing.py',q/'general-physical/quadrics.json',q/'general')
run(q/'check_scalar.py',src)
assert (q/'explicit/source.json').read_bytes()==(q/'explicit-physical/quadrics.json').read_bytes()
run('verify.py',cwd=q/'explicit')
run('check.py',cwd=root/'abc68')
for folder in sorted(root.glob('abc[0-9]*')):
    if folder.name!='abc68':
        run('verify.py',cwd=folder)
        run(folder/'audit/verify_abc.py',src/'computation/quartic/abc68_v65/quadratic-family.json',folder)
run('check_positive.py','--repo',src,cwd=root/'fewvars')
run('projective.py',cwd=root/'fewvars')
run('check_positive.py','--balanced','--repo',src,cwd=root/'fewvars')
print('All requested checks passed.')
