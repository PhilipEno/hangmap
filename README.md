# hangmap
*A digital heritage / archive themed variation on hangman*

## Background & Description
This game is a variation on the HANGMAN game as found in chapters 7-9 of '[Invent Your Own Computer Games with Python, 4th Edition](https://inventwithpython.com/invent4thed/)', by Al Sweigart. It was made as part of the Python learning path of the [Bits & Bots Studygroup](https://github.com/Lotte-W/Bits-and-Bots-study-group). \
The program consists of:
* `hangmap.py` (main program, heavily based on Al Sweigart's game, with some variations)
* `aat_terms.py` (helper program that is called from hangmap.py, and returns an AAT term and URI)
* `aat_IDs.csv` (a list of AAT IDs, that are used to query the AAT API)

## Requirements
* An internet connection is required in order to retrieve words from the Art & Architecture Thesaurus (AAT).
* The `requests` module is used to collect data from the AAT. The module is not part the Python standard library, and has to be installed prior to running hangmap.py. Can als be found in requirements.txt.

## Credits
The ASCII art computer is possibly made by 'LJ'. Courtesy of https://www.asciiart.eu/computers/computers. \
Thanks to Francesca, Lotte and Susanne.
