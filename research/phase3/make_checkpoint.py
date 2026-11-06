#!/usr/bin/env python3
"""Write the complete phase-three review checkpoint without changing git."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import hashlib
import json
import os
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=REPO.parent/"diophantine_research_20261106_v3.zip")
    args = parser.parse_args()
    research = [p for p in sorted((REPO/"research").rglob("*"))
                if p.is_file() and "__pycache__" not in p.parts]
    baseline = [p for p in sorted((REPO/"quartics/quartic-12504").rglob("*"))
                if p.is_file() and "__pycache__" not in p.parts]
    refs = [REPO/p for p in ("quartic_12504.tex", "README.md", "CITATION.bib",
                            "CONTRIBUTING.md", "THIRD_PARTY_NOTICES.md")
            if (REPO/p).is_file()]
    manifest = []
    readme = (
        "Research checkpoint for the conditional Diophantine constructions.\n\n"
        "Current status and hypotheses: research/phase3/state.json.\n"
        "Preferred current constructions and commands: research/phase3/README.md.\n"
        "The updated standalone paper has a fresh filename ending _20261106_v3.tex.\n"
        "Earlier papers and comparisons are preserved unchanged.\n\n"
        "Only research/ is proposed for the local fork. The baseline and reference\n"
        "copies are unchanged dependencies supplied for offline review.\n"
        "No commit, push, or pull request has been made.\n"
    )
    args.output = args.output.resolve()
    fd, temporary_name = tempfile.mkstemp(prefix=args.output.name + ".building-", dir=args.output.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    with ZipFile(temporary, "w", ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr("README.txt", readme)
        for p in research+baseline+refs:
            name = ("reference_upstream/"+p.name if p in refs
                    else str(p.relative_to(REPO)))
            raw = p.read_bytes()
            archive.writestr(name, raw)
            manifest.append({"path": name, "bytes": len(raw),
                             "sha256": hashlib.sha256(raw).hexdigest()})
        archive.writestr("MANIFEST.json", json.dumps({
            "pinned_revision": "28e87b1b62af0effd954605af7f70b2699dd5672",
            "files": manifest,
        }, indent=2)+"\n")
    with temporary.open("rb") as stream:
        os.fsync(stream.fileno())
    with ZipFile(temporary) as archive:
        assert archive.testzip() is None
    os.replace(temporary, args.output)
    print(json.dumps({
        "file": str(args.output.resolve()), "files": len(manifest),
        "bytes": args.output.stat().st_size,
        "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
        "archive_crc_check": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
