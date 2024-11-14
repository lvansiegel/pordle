# hi
<img src="logo.ico" width="128" style="display:inline; vertical-align:middle;">

- this is a python recreation of the famous word game "wordle"
- it uses the tkinter and configparser packages, and is built using pyinstaller
- word lists taken from [here (legal answers)](https://www.wordunscrambler.net/word-list/wordle-word-list) and [here (legal guesses)](https://word-lists.com/word-lists/list-of-common-5-letter-words/)
- includes themes!

# instructions
- run pordle.exe. it requires the words and _internal folders to be present to run correctly. if they are not, redownload the latest release [here](https://github.com/lvansiegel/pordle/releases/latest)
- if text does not appear correctly, try changing the `changetextscaling` variable in config.ini to `1` and restarting the program.
- your goal is to guess a randomly-chosen word.
- enter a 5-letter word. if it is in the dictionary, it will indicate which letters of your guess are in the correct position (green) or in the answer but not in the correct position (yellow).
- you get 6 guesses by default. once you run out of guesses, you can restart the game.
- hard mode makes it so that each correct letter must be included in the next guess. if a letter is in the correct position, subsequent guesses must also have the letter in that position.

# future goals
- [ ] add options for different word lengths (requires separate dictionaries for each length)
- [ ] also an option for different word languages (also requires separate dictionaries)
- [x] give themes ~~optional~~ values to control all of the colors used in the program
