#!/usr/bin/env python3
"""Rebuild a flat, PDF-first handoff archive from the pinned Git source files.

All original sources remain unchanged. LaTeX files are compiled with pdflatex;
only the resulting PDFs, non-TeX source files, and handoff metadata enter ZIP.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
SOURCE_MANIFEST = ROOT / "SOURCE_MANIFEST.json"
OUTPUT = ROOT / "handoff_packages" / "zq-playground-flat-pdf-handoff-20261118.zip"
REPORT = ROOT / "handoff_packages" / "zq-playground-flat-pdf-verification.json"


def run(cmd: list[str], **kwargs):
    return subprocess.run(cmd, check=True, **kwargs)


def pdf_pages(p: Path) -> int:
    text = subprocess.check_output(["pdfinfo", str(p)], text=True)
    for line in text.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise ValueError(f"No page count in PDF: {p}")


def name_for(path: str) -> str:
    p = Path(path)
    if p.name == "README.md" and str(p) != "README.md":
        return f"{p.parent.name}_README.md"
    if p.suffix == ".tex":
        return p.with_suffix(".pdf").name
    return p.name


def main():
    original = json.loads(SOURCE_MANIFEST.read_text("utf-8"))
    files = original["files"]
    assert len(files) == 32
    assert sum(x["category"] == "must_have" for x in files) == 17
    assert sum(x["category"] == "should_have" for x in files) == 15

    final: dict[str, bytes] = {}
    records: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="zq-tex-") as tmp:
        work = Path(tmp)
        for row in files:
            source = ROOT / row["bundle_path"]
            assert source.is_file(), source
            actual_blob = subprocess.check_output(
                ["git", "hash-object", str(source)], text=True
            ).strip()
            assert actual_blob == row["source_blob_sha"], (
                source, actual_blob, row["source_blob_sha"]
            )
            data = source.read_bytes()
            assert len(data) == row["size_bytes"], source

            target = name_for(row["source_path"])
            assert "/" not in target and "\\" not in target
            assert target not in final, f"Flat filename collision: {target}"
            converted = source.suffix.lower() == ".tex"
            page_count = None
            if converted:
                output_dir = work / f"paper-{row['priority']:02}"
                output_dir.mkdir()
                # Working directory beside the original .tex accommodates
                # relative \input and bibliography paths when present.
                cmd = [
                    "latexmk", "-pdf", "-no-shell-escape", "-interaction=nonstopmode",
                    "-halt-on-error", "-file-line-error", f"-outdir={output_dir}",
                    source.name,
                ]
                print(f"PDF {row['priority']:02}: {row['source_path']}", flush=True)
                run(cmd, cwd=source.parent, stdout=subprocess.DEVNULL)
                pdf = output_dir / Path(source.name).with_suffix(".pdf").name
                assert pdf.is_file() and pdf.stat().st_size > 1000, source
                page_count = pdf_pages(pdf)
                assert page_count >= 1, pdf
                extracted = subprocess.check_output(["pdftotext", str(pdf), "-"])
                assert len(extracted.strip()) >= 200, f"Empty PDF text: {pdf}"
                data = pdf.read_bytes()
                assert data.startswith(b"%PDF-"), pdf
            else:
                print(f"KEEP {row['priority']:02}: {row['source_path']}", flush=True)

            final[target] = data
            records.append({
                "priority": row["priority"],
                "category": row["category"],
                "description": row["description"],
                "filename": target,
                "source_path": row["source_path"],
                "source_url": row["original_raw_url"],
                "source_blob_sha": row["source_blob_sha"],
                "converted_from_tex": converted,
                "pdf_pages": page_count,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            })

    assert len(records) == 32 and len(final) == 32
    assert sum(x["converted_from_tex"] for x in records) >= 15

    must = [r for r in records if r["category"] == "must_have"]
    should = [r for r in records if r["category"] == "should_have"]

    priority_md = [
        "# Z in Q: Playground research handoff — priority list",
        "",
        f"Source repository: https://github.com/{original['repository']}",
        f"Pinned source commit: \`{original['pinned_commit']}\`",
        "",
        "All 36 files are in the ZIP root, with **no subfolders**. "
        "LaTeX papers are supplied as **searchable compiled PDFs**, not .tex files.",
        "",
        "## Must have — first 17 research files",
        "",
    ]
    for group, title in ((must, None), (should, "## Should probably have — 15 supporting files")):
        if title:
            priority_md.extend([title, ""])
        for r in group:
            convert = " (PDF conversion)" if r["converted_from_tex"] else ""
            priority_md.append(
                f"{r['priority']}. **\`{r['filename']}\`**{convert} — "
                f"{r['description']}. Original: [pinned source]({r['source_url']})."
            )
        priority_md.append("")
    priority_md += [
        "## Qualifications",
        "",
        "The 21-general and 9-ordinary-abc targets have sound sources but remain "
        "**globally incomplete**. Rational realization at the ACTUAL detector traces "
        "and physical weights, with all guards at one fixed sufficient parameter, "
        "is unproved. The 25/11/193-variable results retain their stated arithmetic "
        "premises. Some fixed numerical construction files are algebraic fixtures, "
        "not certified defining parameters.",
        "",
        "The v75–v77 result records supersede older numerical summaries. Exact "
        "original file hashes and converted PDF hashes appear in SOURCE_MANIFEST.json.",
        "",
    ]

    main_readme = next(x["filename"] for x in records if x["source_path"] == "README.md")
    guide = f"""# OpenAI API Playground research handoff — flat PDF edition

This ZIP contains **32 selected original repository files**, with each TeX paper
converted to a searchable mathematical PDF, plus these four handoff files:
\`README_START_HERE.md\`, \`PRIORITY_LIST.md\`, \`HANDOFF_PROMPT.md\`,
and \`SOURCE_MANIFEST.json\`.

All files are in the **root of the ZIP**. There are no directories and no
\`.tex\` files. The full 17/15 priority split is in \`PRIORITY_LIST.md\`.

Start with:
1. \`PRIORITY_LIST.md\` and \`HANDOFF_PROMPT.md\`;
2. \`{main_readme}\`, \`research_directions.md\`, and results_v75–v77;
3. the papers and additional source files relevant to the current question.

The source commit is {original['pinned_commit']}.
Original source paths and exact blob SHA values, PDF conversion details,
page counts, and SHA-256 checksums are in \`SOURCE_MANIFEST.json\`.

Global rational realization is still open for 21 general / 9 ordinary-abc
variables. Do not confuse sound source equations, local solubility or real
positivity with a proof of completeness.
"""

    prompt = f"""Continue our research on Diophantine definability of Z in Q
using the attached flat PDF-first handoff bundle, pinned to
{original['pinned_commit']}.

First read README.md, research_directions.md, results_20261117_v75.md,
results_20261117_v76.md, results_20261117_v77.md, and
criteria_20261117_v77.json. The v75-v77 records override older summaries.
Read original LaTeX papers as their same-named PDF counterparts.

Priorities:
1. Prove global rational realization and complete the 21-variable general
   and 9-variable ordinary-abc definitions, preserving actual detector
   traces, physical slope/weight relations, every original and whole-character
   guard, and fixed-shift completeness quantifiers.
2. Improve general quartic variable counts with constructions beyond already
   excluded compression architectures.
3. Improve general and abc-conditional constructions, prioritizing variable
   count, then degree, then coefficient heights.
4. Investigate Diophantine definability of integer rings of number fields.

State assumptions precisely. Separate proved, conditional, conjectural and
computational statements. Reconstruct decisive identities and use exact
independent checks. Real/local points do not imply global rational points.
Do not claim 21/9 completeness without an actual global theorem.
"""

    extra = {
        "README_START_HERE.md": guide.encode("utf-8"),
        "PRIORITY_LIST.md": ("\n".join(priority_md) + "\n").encode("utf-8"),
        "HANDOFF_PROMPT.md": prompt.encode("utf-8"),
        "SOURCE_MANIFEST.json": (json.dumps({
            "archive_type": "flat-pdf-first",
            "source_repository": original["repository"],
            "source_commit": original["pinned_commit"],
            "counts": {
                "must_have": 17, "should_have": 15, "total_research_files": 32,
                "pdf_conversions": sum(r["converted_from_tex"] for r in records),
                "supplemental_handoff_guides": 4,
            },
            "files": records,
        }, indent=2) + "\n").encode("utf-8"),
    }
    for key, value in extra.items():
        assert key not in final
        final[key] = value

    assert len(final) == 36
    assert len(set(final)) == 36
    assert all("/" not in name and "\\" not in name for name in final)
    assert all(not name.lower().endswith(".tex") for name in final)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(final.items()):
            z.writestr(name, data)
    with zipfile.ZipFile(OUTPUT) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == 36
        assert all("/" not in n and "\\" not in n for n in z.namelist())
        assert all(not n.endswith(".tex") for n in z.namelist())
        assert {n: hashlib.sha256(z.read(n)).hexdigest()
                for n in z.namelist()} == {
                n: hashlib.sha256(b).hexdigest() for n, b in final.items()
            }
    report = {
        "zip": str(OUTPUT.relative_to(ROOT)),
        "zip_size_bytes": OUTPUT.stat().st_size,
        "zip_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "source_commit": original["pinned_commit"],
        "total_files": len(final),
        "original_file_count": len(records),
        "pdf_count": sum(r["converted_from_tex"] for r in records),
        "metadata_count": len(extra),
        "all_archive_entries_flat": True,
        "no_tex_files": True,
        "pdfs_have_searchable_text": True,
        "zip_crc_check_passed": True,
        "all_source_blob_shas_verified": True,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
