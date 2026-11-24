"""Interactive Japanese dictionary lookup for Multilingual Shiritori V2."""

from lexical_database_v2 import LexicalEntry, load_lexical_database, search_entries


def display_entry(entry: LexicalEntry) -> None:
    forms = "、".join(entry.written_forms) or "（表記情報なし）"
    readings = "、".join(entry.readings) or "（読み情報なし）"

    print(f"表記: {forms}")
    print(f"読み: {readings}")
    for index, sense in enumerate(entry.senses, start=1):
        parts_of_speech = "、".join(sense.part_of_speech) or "（品詞タグなし）"
        glosses = "; ".join(sense.english_glosses) or "（英語語義なし）"
        print(f"語義 {index} [{parts_of_speech}]: {glosses}")
    print(f"JMdict entry ID: {entry.sequence_id}")


def main() -> None:
    print("JMdict 日本語語彙検索 (Version 2.0)")
    print("単語を入力してください。終了するには :quit と入力します。\n")
    entries = load_lexical_database()

    while True:
        query = input("検索語: ").strip()
        if query.lower() == ":quit":
            print("終了します。")
            return
        if not query:
            print("検索語を入力してください。\n")
            continue

        matches = search_entries(entries, query)
        if not matches:
            print("一致する語彙項目が見つかりませんでした。\n")
            continue

        print(f"{len(matches)} 件見つかりました。表示は最大10件です。\n")
        for index, entry in enumerate(matches[:10], start=1):
            print(f"--- {index} ---")
            display_entry(entry)
        print()


if __name__ == "__main__":
    main()
