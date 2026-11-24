"""Read JMdict entries as structured lexical records for Version 2.0."""

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

from shiritori_v1 import katakana_to_hiragana


@dataclass(frozen=True)
class LexicalSense:
    """Part-of-speech tags and English glosses for one JMdict sense."""

    part_of_speech: tuple[str, ...]
    english_glosses: tuple[str, ...]


@dataclass(frozen=True)
class LexicalEntry:
    """A searchable JMdict entry with its written forms and senses."""

    sequence_id: str
    written_forms: tuple[str, ...]
    readings: tuple[str, ...]
    senses: tuple[LexicalSense, ...]


def load_lexical_database(
    xml_path: str | Path = "data/JMdict_e.xml",
) -> list[LexicalEntry]:
    """Load JMdict entries while retaining readings, forms, POS tags, and glosses."""
    root = ET.parse(xml_path).getroot()
    entries: list[LexicalEntry] = []

    for element in root.findall("entry"):
        sequence = element.findtext("ent_seq", default="")
        written_forms = tuple(
            form.text.strip()
            for form in element.findall("k_ele/keb")
            if form.text and form.text.strip()
        )
        readings = tuple(
            reading.text.strip()
            for reading in element.findall("r_ele/reb")
            if reading.text and reading.text.strip()
        )
        senses = tuple(
            LexicalSense(
                part_of_speech=tuple(
                    dict.fromkeys(
                        pos.text.strip()
                        for pos in sense.findall("pos")
                        if pos.text and pos.text.strip()
                    )
                ),
                english_glosses=tuple(
                    dict.fromkeys(
                        gloss.text.strip()
                        for gloss in sense.findall("gloss")
                        if gloss.text
                        and gloss.text.strip()
                        and gloss.get(
                            "{http://www.w3.org/XML/1998/namespace}lang", "eng"
                        )
                        == "eng"
                    )
                ),
            )
            for sense in element.findall("sense")
        )

        entries.append(
            LexicalEntry(
                sequence_id=sequence,
                written_forms=written_forms,
                readings=readings,
                senses=senses,
            )
        )

    return entries


def search_entries(entries: list[LexicalEntry], query: str) -> list[LexicalEntry]:
    """Find entries whose written form or reading exactly matches the query."""
    written_query = query.strip()
    normalized_query = katakana_to_hiragana(written_query)
    if not normalized_query:
        return []

    return [
        entry
        for entry in entries
        if written_query in entry.written_forms
        or any(
            katakana_to_hiragana(reading) == normalized_query
            for reading in entry.readings
        )
    ]
