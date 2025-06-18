#!/usr/bin/env python
"""Build PMID→XML path index and save it as a Parquet file.

Usage (maintainer-only, run on Jean-Zay):

    poetry run python scripts/build_index.py \
        --xml-root /lustre/.../oa_bulk/xml \
        --out pmid_xml_index.parquet \
        --nproc 128
"""
from __future__ import annotations

import concurrent.futures as _cf
import os
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

import pandas as pd
from lxml import etree
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Helpers – XML parsing
# ---------------------------------------------------------------------------

def _extract_pmid(xml_file: Path) -> Tuple[str, str] | None:
    """Return (pmid, relative_xml_path) or ``None`` if not found/invalid."""
    try:
        # Fast incremental parse – stop after first article-id node.
        for _, elem in etree.iterparse(
            str(xml_file), events=("end",), tag="article-id"
        ):
            if elem.get("pub-id-type") == "pmid" and elem.text:
                pmid = elem.text.strip()
                return pmid, str(xml_file)
    except Exception:
        # Corrupted XML; ignore.
        return None
    return None


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def _gather_xml_files(xml_root: Path) -> List[Path]:
    return [p for p in xml_root.rglob("*.xml") if p.is_file()]


def build_index(xml_root: Path, out_file: Path, nproc: int | None = None) -> None:
    xml_root = xml_root.resolve()
    files = _gather_xml_files(xml_root)
    if not files:
        print(f"No XML files found under {xml_root}", file=sys.stderr)
        sys.exit(1)

    results: List[Tuple[str, str]] = []
    with _cf.ProcessPoolExecutor(max_workers=nproc) as ex:
        for res in tqdm(ex.map(_extract_pmid, files, chunksize=1000), total=len(files)):
            if res is not None:
                pmid, fpath = res
                rel_path = str(Path(fpath).relative_to(xml_root))
                results.append((pmid, rel_path))

    df = pd.DataFrame(results, columns=["pmid", "xml_path"])
    df.to_parquet(out_file, index=False)
    print(f"Written {len(df):,} rows → {out_file}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Build PMID→XML index Parquet")
    ap.add_argument("--xml-root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--nproc", type=int, default=os.cpu_count())
    args = ap.parse_args()

    build_index(args.xml_root, args.out, args.nproc) 