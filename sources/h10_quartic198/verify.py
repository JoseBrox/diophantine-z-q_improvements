from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
programs=['circuits/build_affine200.py', 'circuits/check_affine200.py', 'circuits/build_inverse198.py', 'circuits/check_inverse198.py', 'circuits/balance_inverse198.py', 'circuits/check_balanced198.py', 'audit/check_affine200_third.py', 'audit/check_inverse198_third.py', 'audit/check_inverse198_balanced.py', 'charts/check_inverse_vieta.py', 'charts/reference_no_quadrics.py', 'alternatives/check_structural_obstructions.py', 'poles/check_pole_obstructions.py']
for program in programs:
    result=subprocess.run([sys.executable,'-B',str(root/program)],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if result.returncode:
        print(result.stdout)
        raise SystemExit(result.returncode)
    print('PASS '+program)
print('All algebraic checks passed. Arithmetic premises remain explicitly inherited.')
