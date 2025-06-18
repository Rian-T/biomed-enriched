from pathlib import Path

import datasets

from biomed_enriched import populate
from biomed_enriched._mapper import _IndexLoader


def _create_dummy_xml(tmp_path: Path):
    xml_root = tmp_path / "xml"
    xml_root.mkdir()
    xml_file = xml_root / "dummy.xml"
    xml_file.write_text(
        """
    <article>
      <article-id pub-id-type=\"pmid\">123</article-id>
      <body><p>Hello.</p></body>
    </article>
    """
    )
    return xml_root, {"123": xml_file.relative_to(xml_root).as_posix()}


def _create_and_save_dataset(tmp_path: Path):
    ds = datasets.Dataset.from_dict({"article_id": ["123"], "path": ["p[0]"]})
    ds_dir = tmp_path / "ds"
    ds.save_to_disk(ds_dir)
    return ds_dir


def test_populate_inplace(tmp_path: Path, monkeypatch):
    xml_root, mapping = _create_dummy_xml(tmp_path)

    # Monkeypatch IndexLoader to use our mapping (both original and re-export)
    monkeypatch.setattr(
        "biomed_enriched._mapper._IndexLoader", lambda *a, **k: _IndexLoader(lookup=mapping)
    )
    monkeypatch.setattr(
        "biomed_enriched._IndexLoader", lambda *a, **k: _IndexLoader(lookup=mapping)
    )

    ds_path = _create_and_save_dataset(tmp_path)

    populate(ds_path, xml_root, output_path=None, num_proc=1)

    # Reload dataset to verify enrichment
    enriched = datasets.load_from_disk(ds_path)
    assert enriched[0]["text"] == "Hello." 