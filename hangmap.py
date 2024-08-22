"""Made as part of the Python learning path of the Bits & Bots Studygroup.
Variation on the HANGMAN game as found in chapters 7-9 of 'Invent Your Own Computer Games with Python, 4th Edition', by Al Sweigart.
The ASCII art computer is possibly made by 'LJ'. Courtesy of https://www.asciiart.eu/computers/computers.
An internet connection is required in order to retrieve words from the Art & Architecture Thesaurus (AAT).
The requests module is used to collect data from the AAT. The module is not part the Python standard library, and has to be installed prior to running hangmap.py.
"""

import random
import aat_terms
import re

HANGMAP_PICS = [r'''
 ___________________
 | _______________ |
 | | BBB     BBB | |
 | | B  B    B  B| |
 | | BBB  &  BBB | |
 | | B  B    B  B| |
 | | BBB     BBB | |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | | BBB     BBB | |
 | | B  XX  XB  B| |
 | | BBB  &  BBB | |
 | | B  B    B  B| |
 | | BBB     BBB | |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []| 
L___________________J 
 ___________________  
/###################\ ''',r'''
 ___________________
 | _______________ |
 | | BBB     BBB | |
 | | B  XX  XB  B| |
 | | XBB  &  BBB | |
 | | BX B    B  B| |
 | | BBB     BBBX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | | BBB   X BBX | |
 | | B  XX  XB  B| |
 | | XBB  &  BBB | |
 | | BX B  XXB XB| |
 | | BBB     BBBX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXBX   X BBX | |
 | | B  XX  XB XB| |
 | | XBB X&  BBB | |
 | | BX B  XXBXXB| |
 | | BBB X   BBBX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXBX   X BBX | |
 | | B  XX  XB XB| |
 | |XXBB X&  BBB | |
 | |XBX B  XXBXXB| |
 | |XBBB X   BBBX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXBX   X BBX | |
 | | B  XX  XB XB| |
 | |XXBB XX  BBBX| |
 | |XBX B  XXBXXB| |
 | |XBBB X XXXXXX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXBX X X XBX | |
 | | BX XX XXB XB| |
 | |XXBB XX  XBBX| |
 | |XBX XX XXBXXB| |
 | |XBBB X XXXXXX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXXX XXX XBX | |
 | | BX XX XXB XB| |
 | |XXBB XXXXXBXX| |
 | |XBX XX XXBXXB| |
 | |XBXB X XXXXXX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXXX XXX XBX | |
 | | BXXXX XXXXXB| |
 | |XXBB XXXXXBXX| |
 | |XBXXXX XXBXXX| |
 | |XXXX XXXXXXXX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXXX XXX XXXX| |
 | | BXXXX XXXXXX| |
 | |XXBBXXXXXXXXX| |
 | |XBXXXXXXXBXXX| |
 | |XXXX XXXXXXXX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXXX XXXXXXXX| |
 | |XXXXXXXXXXXXX| |
 | |XXBXXXXXXXXXX| |
 | |XBXXXXXXXXXXX| |
 | |XXXX XXXXXXXX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |XXXXXXXXXXXXX| |
 | |XXXXXXXXXXXXX| |
 | |XXXXXXXXXXXXX| |
 | |XXXXXXXXXXXXX| |
 | |XXXXXXXXXXXXX| |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ ''',r'''
 ___________________
 | _______________ |
 | |             | |
 | |  --     --  | |
 | |             | |
 | |    _---_    | |
 | |   -     -   | |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []|
L___________________J
 ___________________ 
/###################\ '''
]

lerenPreserverenWords = {
"aanwinstencontract":"https://lerenpreserveren.nl/woordenlijst/aanwinstencontract/","aip":"https://lerenpreserveren.nl/woordenlijst/aip/","analoog filmobject":"https://lerenpreserveren.nl/woordenlijst/analoog-filmobject/","authenticiteit":"https://lerenpreserveren.nl/woordenlijst/authenticiteit/","besturingssysteem":"https://lerenpreserveren.nl/woordenlijst/besturingssysteem/","betrouwbaarheid":"https://lerenpreserveren.nl/woordenlijst/betrouwbaarheid/","bitpreservering":"https://lerenpreserveren.nl/woordenlijst/bitpreservering/","bitrot":"https://lerenpreserveren.nl/woordenlijst/bitrot/","bruikbaarheid":"https://lerenpreserveren.nl/woordenlijst/bruikbaarheid/","checksum":"https://lerenpreserveren.nl/woordenlijst/checksum/","cloud opslag":"https://lerenpreserveren.nl/woordenlijst/cloud-opslag/","compressie":"https://lerenpreserveren.nl/woordenlijst/compressie/","content drift":"https://lerenpreserveren.nl/woordenlijst/content-drift/","converteren":"https://lerenpreserveren.nl/woordenlijst/converteren/","device":"https://lerenpreserveren.nl/woordenlijst/device/","digitaal archief":"https://lerenpreserveren.nl/woordenlijst/digitaal-archief/","digitaal erfgoed":"https://lerenpreserveren.nl/woordenlijst/digitaal-erfgoed/","digitaal geboren erfgoed":"https://lerenpreserveren.nl/woordenlijst/digitaal-geboren-erfgoed/","digitaal object":"https://lerenpreserveren.nl/woordenlijst/digitaal-object/","digital preservation":"https://lerenpreserveren.nl/woordenlijst/digital-preservation/","dip":"https://lerenpreserveren.nl/woordenlijst/dip/","documentatie":"https://lerenpreserveren.nl/woordenlijst/documentatie/","duurzaamheidsbeleidsplan":"https://lerenpreserveren.nl/woordenlijst/duurzaamheidsbeleidsplan/","duurzame toegang":"https://lerenpreserveren.nl/woordenlijst/duurzame-toegang/","emulatie":"https://lerenpreserveren.nl/woordenlijst/emulatie/","ftp":"https://lerenpreserveren.nl/woordenlijst/ftp/","gedefinieerde doelgroep":"https://lerenpreserveren.nl/woordenlijst/gedefinieerde-doelgroep/","gedigitaliseerde informatie":"https://lerenpreserveren.nl/woordenlijst/gedigitaliseerde-informatie/","harvesting":"https://lerenpreserveren.nl/woordenlijst/harvesting/","herinterpretatie":"https://lerenpreserveren.nl/woordenlijst/herinterpretatie/","informatieobject":"https://lerenpreserveren.nl/woordenlijst/informatieobject/","ingest":"https://lerenpreserveren.nl/woordenlijst/ingest/","installatie":"https://lerenpreserveren.nl/woordenlijst/installatie/","integriteit":"https://lerenpreserveren.nl/woordenlijst/integriteit/","linkrot":"https://lerenpreserveren.nl/woordenlijst/linkrot/","masterbestand":"https://lerenpreserveren.nl/woordenlijst/masterbestand/","metadata":"https://lerenpreserveren.nl/woordenlijst/metadata/","metadatamapping":"https://lerenpreserveren.nl/woordenlijst/metadatamapping/","metadataschema":"https://lerenpreserveren.nl/woordenlijst/metadataschema/","migreren":"https://lerenpreserveren.nl/woordenlijst/migreren/","normaliseren":"https://lerenpreserveren.nl/woordenlijst/normaliseren/","oais":"https://lerenpreserveren.nl/woordenlijst/oais/","persistent identifier":"https://lerenpreserveren.nl/woordenlijst/persistent-identifier/","preserveringsniveaus":"https://lerenpreserveren.nl/woordenlijst/preserveringsniveaus/","referentiemodel":"https://lerenpreserveren.nl/woordenlijst/referentiemodel/","selectie":"https://lerenpreserveren.nl/woordenlijst/selectie/","sip":"https://lerenpreserveren.nl/woordenlijst/sip/","software compatibiliteit":"https://lerenpreserveren.nl/woordenlijst/software-compatibiliteit/","trusted digital repository":"https://lerenpreserveren.nl/woordenlijst/trusted-digital-repository/","vectorbestand":"https://lerenpreserveren.nl/woordenlijst/vectorbestand/","voorkeursformaat":"https://lerenpreserveren.nl/woordenlijst/voorkeursformaat/","webarchivering":"https://lerenpreserveren.nl/woordenlijst/webarchivering/","zorgdrager":"https://lerenpreserveren.nl/woordenlijst/zorgdrager/"}

def getRandomWord(wordSet, wordDict):
    
    # If wordSet choice is AAT
    if wordSet == 'A':
        
        # Call main function from helper file to store word and uri in variables
        word, url = aat_terms.main()
        
        # Return word and uri
        return [word, url]
    
    # If wordSet choice is Leren Preserveren
    if wordSet == 'L':

        # Choose a random key
        word = random.choice(list(wordDict.keys()))

        # Store value in variable
        url = wordDict[word]

        # return both key (word) and value (url)
        return [word, url]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAP_PICS[len(missedLetters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
        
        # If the word contains a space, add a space instead of a underscore
        elif secretWord[i] == ' ':
            blanks = blanks[:i] + ' ' + blanks[i+1:]
        
        # If the word contains a hyphen, add hyphen instead of underscore
        elif secretWord[i] == '-':
            blanks = blanks[:i] + '-' + blanks[i+1:]
        
        # If the word contains a single quote, add single quote instead of underscore
        elif secretWord[i] == "'":
            blanks = blanks[:i] + "'" + blanks[i+1:]

    
    for letter in blanks:
        print(letter, end=' ')
    print()
   
def getGuess(alreadyGuessed):
    
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess
        
def playAgain():
    print('Do you want to play again?')

    return input().lower().startswith('y')

# Check if string contains defined special characters (space, ' and -) and return characters as string
def checkSpecChars(word):
    
    # Find all defined special characters using regex
    charList = re.findall(r"[\'\s\-]", word)
    
    # Turn list into string
    specChars = "".join(charList)

    # Return string of special characters
    return specChars

def main():

    print('\n############################# H A N G M A P #############################')
    print('''#                                                                       #
    #             Your computer is suffering from severe bitrot.            #
    #    Can you guess the right word before all your bits have died out?   #
    #  If you don't make it in time, you'll have to start using hangmappen  #
    #     (hanging files) again for your archival endeavours. Noooooo...    #
    #                                                                       #''')
    print('############################# H A N G M A P #############################\n')

    difficulty = 'X'
    while difficulty not in 'EMH':
        print('Enter difficulty: E - Easy, M - Medium, H - Hard')
        difficulty = input().upper()
    if difficulty == 'M':
        del HANGMAP_PICS[9]
        del HANGMAP_PICS[6]
        del HANGMAP_PICS[3]
    if difficulty == 'H':
        del HANGMAP_PICS[11]
        del HANGMAP_PICS[9]
        del HANGMAP_PICS[7]
        del HANGMAP_PICS[5]
        del HANGMAP_PICS[3]
        del HANGMAP_PICS[1]
        
    missedLetters = ''
    correctLetters = ''
    
    # Let user decide what word set to use
    wordSet = 'X'
    while wordSet not in 'LA':
        print('Choose your wordSet: L - Leren Preserveren (Dutch), A - Art & Architecture Thesaurus (English)')
        wordSet = input().upper()

    secretWord, secretURL = getRandomWord(wordSet, lerenPreserverenWords)

    # If secret word contains spaces, hypens or single quotes, store them in variable
    specChars = checkSpecChars(secretWord)
    
    gameIsDone = False

    while True:
        # Print('The secret word is in the set: ' + secretSet)
        displayBoard(missedLetters, correctLetters, secretWord)
        
        guess = getGuess(missedLetters + correctLetters)
        if guess in secretWord:
            correctLetters = correctLetters + guess
            foundAllLetters = True
            for i in range(len(secretWord)):
                
                # Break if the character is not a correct letter or a correct special character
                if secretWord[i] not in correctLetters and secretWord[i] not in specChars:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print(r'''
    ___________________
    | _______________ |
    | |   _    _    | |
    | |  ( \  / )   | |
    | |   \ \/ /    | |
    | |    \  /     | |
    | |     \/      | |
    |_________________|
        _[_______]_
    ___[___________]___
    |         [_____] []|
    |         [_____] []|
    L___________________J
    ___________________ 
    /###################\ ''')
                print(f'''Yes! The secret word is '{secretWord}'! You have won!''')
                print(f'''Learn more about '{secretWord}' at {secretURL}.''')
                print()
                
                gameIsDone = True
        else:
            missedLetters = missedLetters + guess
            if len(missedLetters) == len(HANGMAP_PICS) - 1:
                displayBoard(missedLetters, correctLetters, secretWord)
                print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                print(f'''Learn more about '{secretWord}' at {secretURL}.''')
                gameIsDone = True
                
        if gameIsDone:
            if playAgain():
                missedLetters = ''
                correctLetters = ''
                gameIsDone = False
                secretWord, secretURL = getRandomWord(wordSet, lerenPreserverenWords)
            else:
                break

if __name__ == "__main__":
    main()