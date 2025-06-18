from pathlib import Path

import datasets

from biomed_enriched._enricher import _Enricher
from biomed_enriched._mapper import _IndexLoader


def _create_dummy_dataset(tmp_path: Path):
    # Create simple dataset with single row
    data = {
        "article_id": ["123"],
        "path": ["p[0]"],
    }
    ds = datasets.Dataset.from_dict(data)
    path = tmp_path / "hf_ds"
    ds.save_to_disk(path)
    return path, ds


def _create_dummy_xml(tmp_path: Path):
    # Return xml root and mapping dict
    xml_root = tmp_path / "xml"
    xml_root.mkdir()
    xml_file = xml_root / "dummy.xml"
    xml_content = """
    <article>
      <article-id pub-id-type=\"pmid\">123</article-id>
      <body><p>Hello world.</p></body>
    </article>
    """
    xml_file.write_text(xml_content)
    mapping = {"123": xml_file.relative_to(xml_root).as_posix()}
    return xml_root, mapping


def test_enrich_dataset(tmp_path: Path):
    xml_root, mapping = _create_dummy_xml(tmp_path)
    lookup_loader = _IndexLoader(lookup=mapping)

    hf_path, original_ds = _create_dummy_dataset(tmp_path)

    enricher = _Enricher(xml_root, index_loader=lookup_loader, num_proc=1)
    enriched = enricher.enrich_dataset(original_ds)

    assert "text" in enriched.column_names
    assert enriched[0]["text"] == "Hello world." 