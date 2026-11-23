# Multilingual Word Chain / shiritori (しりとり)　Game

**CS50P Final Project**

**Demo Video:** [https://youtu.be/GU1vd-tEreE]

## Description

Multilingual Word Chain Game / shiritori is a command-line word chain game. It supports two languages: Japanese and English. The player chooses a language and tries to continue the word chain by entering valid words from the selected dictionary.

The purpose of this project is to implement a word-based game with different language rules, dictionary lookup, input validation, and game-ending conditions. The game is designed for one player and runs entirely in the terminal.

## How to Play

Choose `Japanese` or `English` when prompted. In English mode, enter a game-over letter.
Try to enter the word starts with 'the last letter' of the previous word. Continue as long as you can.

## Features

- Language selection: Choose between Japanese and English at the beginning of the game.
- Dictionary validation: Every submitted word is checked if it inclueded in a local dictionary.
- Word chain rules: Each new word must begin with 'the last letter' from the previous word.
- Duplicate prevention: A word that has already been used cannot be entered again.
- Game-over conditions:
  - In Japanese mode, the game ends when a word ends with 「ん」.(This is the original rule in Japanese shiritori, because there is basically no word start with 「ん」in Japanese.)
  - In English mode, the player chooses a game-over letter before starting. The game ends when a word ends with that letter.
  - In English mode, a one-letter word also ends the game.
- Quit commands: The player can enter `:quit` or `:おわり` to stop the game manually.
- Score: The game displays the number of valid words entered before the game ends.

The game also handles language-specific word chain rules. In English mode, if a word ends in `e`, the next word may begin with either `e` or the preceding letter. (Because many words I know ends with e.) In Japanese mode, small letter(kana) at the end of a word are handled according to the word chain rules, and a long vowel mark (`ー`) is handled using the preceding kana.


## Project Structure

- project.py: Contains the main game loop, word validation, game-over checks, next-letter logic, dictionary loading, and character conversion.
- test_project.py: Contains pytest tests for the main game functions and character conversion.
- data/enable1.txt: English word list used for dictionary validation.
- data/JMdict_e.xml: Japanese dictionary data used for dictionary validation.
- requirements.txt: Lists external dependencies. The game itself currently uses only Python standard library modules.

## Design Choices

The English dictionary is stored as a text file and loaded into a Python set. This allows efficient word membership checks. The Japanese dictionary is provided in XML format, so I used `xml.etree.ElementTree` to parse its entries.

There are three types of character in Japanese, which is hiragana, katakana, and kanji. Each of them can be rewrite to the others. The Japanese dictionary contains readings written in katakana, while the game accepts hiragana input. To handle this difference, I implemented `katakana_to_hiragana()` using Unicode normalization and character conversion. This allows dictionary readings to be compared with the player's hiragana input.

I used separate functions for word validation, game-over conditions, next-letter calculation, dictionary loading, and character conversion. This keeps the code organized and makes individual functions easier to test. I believe the game have big posibilities to expand and it's easier to add more functions.

## Testing

The project uses pytest. The tests cover word validation, game-ending conditions, next-letter calculation, and katakana-to-hiragana conversion.

## Dictionary Sources and Credits

- **JMdict:** Created and maintained by the Electronic Dictionary Research and Development Group (EDRDG). The dictionary data is used under the Creative Commons Attribution-ShareAlike 4.0 licence.  
  https://www.edrdg.org/wiki/JMdict-EDICT_Dictionary_Project.html  
  Licence: https://www.edrdg.org/edrdg/licence.html

- **ENABLE word list:** Enhanced North American Benchmark LExicon. Compiled by Alan Beale and maintained by M. Cooper and contributors. Released into the public domain.  
  https://norvig.com/ngrams/enable1.txt
