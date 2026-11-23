import pytest
from shiritori_v1 import (
      get_next_letter,
      validate_word,
      check_game_over,
      load_english_dictionary,
      load_japanese_dictionary,
      katakana_to_hiragana
)

# get_next_letter()
def test_get_next_letter_english():
      assert get_next_letter("apple", "english") == ["e", "l"]
      assert get_next_letter("cat", "english") == ["t"]

def test_get_next_letter_japanese():
      assert get_next_letter("さくら", "japanese") == ["ら"]
      assert get_next_letter("やくしょ","japanese") == ["よ"]
      assert get_next_letter("しょくしゅ","japanese") == ["ゆ"]
      assert get_next_letter("やくしゃ","japanese") == ["や"]
      assert get_next_letter("かれー","japanese") == ["れ"]

def test_get_next_letter_empty_word():
      with pytest.raises(ValueError):
            get_next_letter("", "english")

def test_get_next_letter_unsupported_language():
      with pytest.raises(ValueError):
            get_next_letter("apple", "spanish")


# validate_word()
def test_validate_word_english():
      dictionary = load_english_dictionary()

      assert validate_word("apple", "english", dictionary) == True
      assert validate_word("cat!","english", dictionary) == False
      assert validate_word("appl","english", dictionary) == False
      assert validate_word("12345","english", dictionary) == False
      assert validate_word("d1o2g","english", dictionary) == False
      

def test_validate_word_japanese():
      dictionary = load_japanese_dictionary()

      assert validate_word("さくら","japanese", dictionary) == True
      assert validate_word("sakura","japanese", dictionary) == False
      assert validate_word("桜","japanese", dictionary) == False
      assert validate_word("サクラ","japanese", dictionary) == False
      assert validate_word("しやのねこ","japanese", dictionary) == False
      assert validate_word("ゃ", "japanese", dictionary) == False
      assert validate_word("ゅ", "japanese", dictionary) == False
      assert validate_word("ょ", "japanese", dictionary) == False
      assert validate_word("ー", "japanese", dictionary) == False

def test_validate_word_empty_word():
      with pytest.raises(ValueError):
            validate_word("", "english", set())
      with pytest.raises(ValueError):
            validate_word("","japanese", set())
            
def test_validate_word_unsupported_language():
      with pytest.raises(ValueError):
            validate_word("樱花","chinese", set())


# check_game_over()
def test_check_game_over_english():
      assert check_game_over("apple", "english", "e") == True
      assert check_game_over("cat", "english", "e") == False
      assert check_game_over("a", "english", "e") == True
      assert check_game_over("cherry", "english", "y") == True

def test_check_game_over_japanese():
      assert check_game_over("りんご", "japanese") == False
      assert check_game_over("みかん", "japanese") == True

def test_check_game_over_unsupported_language():
      with pytest.raises(ValueError):
            check_game_over("樱花","chinese")

def test_check_game_over_no_gameover_alpha():
      with pytest.raises(ValueError):
            check_game_over("cat", "english", None)

def test_check_game_over_empty_word():
      with pytest.raises(ValueError):
            check_game_over("", "japanese", "e")

#hiragana_to_katakana

def test_katakana_to_hiragana():
    assert katakana_to_hiragana("ゴリラ") == "ごりら"
    assert katakana_to_hiragana("ランプ") == "らんぷ"
    assert katakana_to_hiragana("ラジオ") == "らじお"
    assert katakana_to_hiragana("コンピューター") == "こんぴゅーたー"
    assert katakana_to_hiragana("さくら") == "さくら"