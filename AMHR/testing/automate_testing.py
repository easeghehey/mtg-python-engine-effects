import json
import os
import subprocess

# Incomplete

def parseJson(filename_json) -> list:
    with open(filename_json) as json_file:
        cards = json.load(json_file)
        card_list = []
        for _set in cards.values():
            card_list.extend(_set['cards'])
    cards = set()
    for card in card_list:
        cards.add(card["name"])
    return cards

def countCards():
    with open("automation.txt", "r") as file:
        i = 0
        for card in file:
            card = card.rstrip()
            if not card:
                continue
            if card[0] in {'#','\t', ' '}:
                continue
            i += 1
    return i

def addCardsToFile(file_w, card) -> None: # given a filename, adds card to that file
    file_w.write("#"*30 + "\n")
    for c in card:
        file_w.write(c)
        file_w.write("\n")
    file_w.write("\n\n" + "#"*30)

def runTest(command) -> bool: # returns true if all tests passed
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = p.stdout.readlines()[-1].strip()
    return 'OK' in res

def runFileAddition() -> None:
    m15 = open("m15_cards.txt", "a") # change to actual m15cards
    cc = open("cube_cards.txt", "a") # change to actual cube_cards

    c = parseJson("/Users/emanuelaseghehey/Development/mtg-python-engine-effects/parser/data/M15.json")
    with open("automation.txt", "r") as automation_file:
        lines = []  # buffer

        for line in automation_file:
            line = line.rstrip()
            if not line:
                continue

            if line[:3] == '###':  # end of a card
                if not lines: 
                    continue

                if lines[0] in c: 
                    addCardsToFile(m15, lines)
                else:
                    # has to be AllSets so goes to cube_cards_automation
                    addCardsToFile(cc, lines)
                lines = []
            else:  # wait to parse cards until we've read in all information about a card
                lines.append(line)
    m15.close()
    cc.close()

def createDecks(): # create two decks opposite, test more cards
    pass

if __name__ == "__main__":
    print(countCards())
    '''
    runFileAddition()
    res_runTest = runTest("bash ./test.sh") # call ./test.sh for the game to parse it

    #TODO
    if not res_runTest:
        print('no')

    createDecks()
    '''