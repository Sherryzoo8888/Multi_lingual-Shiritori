from lexical_database_v2 import load_lexical_database, search_entries


def test_load_lexical_database_extracts_entry_fields(tmp_path):
    xml_file = tmp_path / "sample.xml"
    xml_file.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
        <JMdict>
          <entry>
            <ent_seq>12345</ent_seq>
            <k_ele><keb>桜</keb></k_ele>
            <r_ele><reb>サクラ</reb></r_ele>
            <sense>
              <pos>noun</pos>
              <gloss xml:lang="eng">cherry tree</gloss>
              <gloss xml:lang="dut">kersenboom</gloss>
            </sense>
          </entry>
        </JMdict>""",
        encoding="utf-8",
    )

    entries = load_lexical_database(xml_file)

    assert len(entries) == 1
    assert entries[0].sequence_id == "12345"
    assert entries[0].written_forms == ("桜",)
    assert entries[0].readings == ("サクラ",)
    assert len(entries[0].senses) == 1
    assert entries[0].senses[0].part_of_speech == ("noun",)
    assert entries[0].senses[0].english_glosses == ("cherry tree",)


def test_search_entries_matches_written_form_and_hiragana_reading():
    entries = load_lexical_database()

    by_written_form = search_entries(entries, "桜")
    by_hiragana = search_entries(entries, "さくら")

    assert by_written_form
    assert by_hiragana
    assert any("サクラ" in entry.readings for entry in by_hiragana)


def test_search_entries_matches_katakana_reading():
    entries = load_lexical_database()

    matches = search_entries(entries, "サクラ")

    assert matches
    assert any("サクラ" in entry.readings for entry in matches)


def test_search_entries_returns_empty_for_blank_or_unknown_query():
    entries = load_lexical_database()

    assert search_entries(entries, "   ") == []
    assert search_entries(entries, "これは存在しない検索語") == []
