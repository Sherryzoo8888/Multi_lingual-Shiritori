import xml.etree.ElementTree as ET
import unicodedata

List_hiragana = list(
    "あいうえお"
    "かきくけこがぎぐげご"
    "さしすせそざじずぜぞ"
    "たちつてとだぢづでど"
    "なにぬねの"
    "はひふへほばびぶべぼぱぴぷぺぽ"
    "まみむめも"
    "やゆよゃゅょ"
    "らりるれろ"
    "わをんっー"
)


def main(): #ゲーム全体を進行させる

      language = input("Please select language (Japanese / English): ").strip().lower()
      gameover_alpha = None

      if language == "english":
            dictionary = load_english_dictionary()
            gameover_alpha = input("Please select game-over alphabet: ").strip().lower()

      elif language == "japanese":
            dictionary = load_japanese_dictionary()

      else:
            print("Invalid language")
            return

      used_words = []
      

#最初の単語の設定
      while True:     
            word = input("Word: ").strip().lower()

            if word == ":quit" or word == ":おわり":
                  print("Game over")
                  print (f"Your score: {len(used_words)} points")
                  return


            if check_game_over(word, language, gameover_alpha):
                  print("Game over")
                  print (f"Your score: {len(used_words)} points")
                  return
            

            elif not validate_word(word, language, dictionary):
                  print("Invalid word. Try again.")
                  continue

            
            else:
                  previous_word = word
                  used_words.append(word)
                  break


#二回目以降の入力

      while True:
            word = input("Next word: ").strip().lower()

            if word == ":quit" or word == ":おわり":
                  print("Game over")
                  print (f"Your score: {len(used_words)} points")
                  return

            if check_game_over(word, language, gameover_alpha):
                  print("Game over")
                  print (f"Your score: {len(used_words)} points")
                  return

            if not validate_word(word, language, dictionary):
                  print("Invalid word. Try again")
                  continue

            elif word in used_words:
                  print("Used word. Try again.")
                  continue

            elif word[0] not in get_next_letter(previous_word, language):
                  print("Invalid word. Try again.")
                  continue


            else:
                  previous_word = word
                  used_words.append(word)


def validate_word(word, language, dictionary): #入力された単語が有効か判定

      if not word:
            raise ValueError("Word cannot be empty")

      if language == "english":
            if not word.isalpha():
                  return False
            elif word not in dictionary:
                  return False
            
            return True

      elif language == "japanese":
            if word in ("ゃ", "ゅ", "ょ", "ー"):
                  return False
                  
            for character in word:
                  if character not in List_hiragana:
                        return False

            if word not in dictionary:
                  return False
                  
            return True

      else:
            raise ValueError("Unsupported Language")


def check_game_over(word, language, gameover_alpha=None): #ゲームオーバー条件を判定

      if not word:
            raise ValueError("Word cannot be empty")
      
      if language == "english":

            if not gameover_alpha:
                  raise ValueError("Game over alphabet must be specified")
            
            if len(word) < 2:
                  return True
            
            elif word.endswith(gameover_alpha):
                  return True
            
            return False
      
      elif language == "japanese":
            if word.endswith("ん"):
                  return True

            return False
      
      else:
            raise ValueError("Unsupported Language")

            

    
def get_next_letter(word, language): #次の単語が始まるべき文字を取得
    
      if not word:
            raise ValueError("Word cannot be empty")

      small_to_large = {
            "ゃ": "や",
            "ゅ": "ゆ",
            "ょ": "よ"
      }

      if language == "english":
            
            if word.lower().endswith("e"):
                  return [word[-1], word[-2]]
            else:
                  return [word[-1]]


      elif language == "japanese":
            if word.endswith(("ゃ","ゅ","ょ")):
                  return [small_to_large[word[-1]]]
            elif word.endswith("ー"):
                  return [word[-2]]
            
            return [word[-1]]

      else:
            raise ValueError("Unsupported Language")



def load_english_dictionary():
      words = set()

      with open("data/enable1.txt", "r", encoding="utf-8") as file:# ここでファイルを処理

            for line in file:
                  word = line.strip().lower()
                  words.add(word)

      return words

def load_japanese_dictionary():
      words = set()

      tree = ET.parse("data/JMdict_e.xml")
      root = tree.getroot()

      for entry in root.findall("entry"):
            for reading in entry.findall("r_ele"):
                  reb = reading.find("reb")
                  
                  if reb is not None and reb.text:
                        words.add(katakana_to_hiragana(reb.text))

      return words


def katakana_to_hiragana(word):
      word = unicodedata.normalize("NFKC", word)

      result = ""

      for char in word:
            if "ァ" <= char <= "ヶ":
                  number = ord(char)
                  hiragana_char = chr(number - 96)
                  result += hiragana_char
            
            else:
                  result += char

      return result


if __name__ == "__main__":
      main()
