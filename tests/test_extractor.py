from pathlib import Path

import pytest

from biomed_enriched._extractor import _XmlParagraphExtractor


@pytest.mark.parametrize(
    "input_path,expected",
    [
        ("sec[0]/p[1]", [("sec", 0), ("p", 1)]),
        ("p[0]", [("p", 0)]),
    ],
)
def test_parse_path(input_path, expected):
    assert _XmlParagraphExtractor._parse_path(input_path) == expected


def test_extract_simple(tmp_path: Path):
    # Minimal XML example with two <p> tags inside <body>
    xml_content = """
    <article>
      <body>
        <sec><p>First paragraph.</p><p>Second paragraph.</p></sec>
      </body>
    </article>
    """
    xml_file = tmp_path / "test.xml"
    xml_file.write_text(xml_content)

    extractor = _XmlParagraphExtractor(xml_file)

    assert extractor.extract("sec[0]/p[0]") == "First paragraph."
    assert extractor.extract("sec[0]/p[1]") == "Second paragraph."
    # Out-of-bounds returns None
    assert extractor.extract("sec[0]/p[2]") is None


@pytest.mark.parametrize(
    "bad_path",
    ["", "sec", "sec[]", "sec[p]", "sec[0]/bad"],
)
def test_parse_path_errors(bad_path):
    with pytest.raises(ValueError):
        _XmlParagraphExtractor._parse_path(bad_path) 