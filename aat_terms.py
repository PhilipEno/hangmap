# Program that returns a word and uri from the Art & Architecture Thesaurus (AAT), excluding words that contain special characters (except space, single quote and hyphen).

import requests
import csv
import random
import xml.etree.ElementTree as ET
import re

# Documentation for Getty API: https://www.getty.edu/research/tools/vocabularies/vocab_web_services.pdf and http://vocabsservices.getty.edu/AATService.asmx
API = 'http://vocabsservices.getty.edu/AATService.asmx/AATGetSubjectTerms?subjectID='
fileName = 'aat_IDs.csv'

# Function the picks a random id from csv file. Solution for selecting random value from csv from: https://stackoverflow.com/questions/43476754/using-python-how-do-you-select-a-random-row-of-a-csv-file
def chooseId(file):
    
    # Read file into reader object, turn it into a list and choose random value from list
    with open(file) as csvFile:
        readerObject = csv.reader(csvFile)
        randomTerm = random.choice(list(readerObject))

        # Return first (and only) value from the list
        return randomTerm[0]


def main():

    while True:
        # Select random id from csv file
        aatId = chooseId(fileName)

        # Make API call using random aat ID and store result in response
        response = requests.get(f'{API}{aatId}')

        # Exit if the API call returns an error
        if response.status_code != 200:
            print(f'Unable to query API. Error: {response.status_code}.')
            return 1
        
        # Read response from API call and store in reader object 'xmlResult'
        xmlResult = ET.fromstring(response.text)

        # Search for the preferred term in the XML result and store in variable
        for t in xmlResult.findall("./Subject/Terms/Preferred_Term/Term_Text"):
            term = t.text

        # Check if term contains limited set of characters. If not, pick a new term. Repeat until valid term is returned.
        checkChars = re.findall(r"^([A-Za-z\s\-\(\)\']+)$", term)
        if checkChars:
            # Break out of while True loop
            break
            
    # Check if string contains parenthesized suffix. If so, remove - including content and leading whitespace - using regex.
    checkParentheses = re.search(r"^(.+)(\s\(.+\))$", term)
    if checkParentheses:
        term = checkParentheses.group(1)

    # Return term and uri
    uri = f'http://vocab.getty.edu/page/aat/{aatId}'
    return [term, uri]

if __name__ == "__main__":
    main()