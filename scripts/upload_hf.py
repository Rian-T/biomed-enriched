#!/usr/bin/env python
"""Upload a Parquet PMID→XML index to a Hugging Face dataset.

Example
-------
poetry run python scripts/upload_hf.py --dataset rntc/pmid-xml-index --file pmid_xml_index.parquet

Requirements
------------
A valid *write* token must be available in the ``HF_TOKEN`` or
``HUGGINGFACE_TOKEN`` environment variable, or you must be already logged in
via ``huggingface-cli login``.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import datasets
from huggingface_hub import HfApi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_repo_exists(dataset_id: str, private: bool = False) -> None:
    """Create the dataset repository on the Hub if it does not exist."""

    api = HfApi()
    try:
        api.repo_info(repo_id=dataset_id, repo_type="dataset")
    except Exception:
        print(f"Creating new dataset repository {dataset_id} (private={private})…")
        api.create_repo(repo_id=dataset_id, repo_type="dataset", private=private)


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def upload(file_path: Path, dataset_id: str, *, split: str = "train", private: bool = False) -> None:
    if not file_path.is_file():
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    _ensure_repo_exists(dataset_id, private=private)

    print(f"Loading Parquet file {file_path}…")
    df = pd.read_parquet(file_path)

    if set(df.columns) != {"pmid", "xml_path"}:
        print("Parquet must contain exactly two columns: 'pmid' and 'xml_path'", file=sys.stderr)
        sys.exit(1)

    ds = datasets.Dataset.from_pandas(df, preserve_index=False)
    print(f"Pushing {len(ds):,} rows → {dataset_id} (split={split})…")
    ds.push_to_hub(dataset_id, split=split)
    print("✓ Upload complete.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Upload Parquet index to Hugging Face Hub")
    ap.add_argument("--dataset", required=True, help="Target dataset repository (e.g. rntc/pmid-xml-index)")
    ap.add_argument("--file", required=True, type=Path, help="Local Parquet file to upload")
    ap.add_argument("--split", default="train", help="Dataset split name (default: train)")
    ap.add_argument("--private", action="store_true", help="Create a private dataset repo")
    args = ap.parse_args()

    upload(args.file, args.dataset, split=args.split, private=args.private) 