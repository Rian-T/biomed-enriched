from pathlib import Path

import pandas as pd

from scripts.build_index import build_index


def _create_sample_corpus(tmp_path: Path):
    xml_root = tmp_path / "xml"
    xml_root.mkdir()
    # Two files
    for pmid in ("111", "222"):
        p = xml_root / f"PMC{pmid}.xml"
        p.write_text(
            f"""
        <article>
          <article-id pub-id-type=\"pmid\">{pmid}</article-id>
        </article>
        """
        )
    return xml_root


def test_build_index(tmp_path: Path):
    xml_root = _create_sample_corpus(tmp_path)
    out_file = tmp_path / "idx.parquet"
    build_index(xml_root, out_file, nproc=1)

    df = pd.read_parquet(out_file)
    assert set(df.columns) == {"pmid", "xml_path"}
    assert sorted(df["pmid"]) == ["111", "222"] 