#! /usr/local/bin/python3.6

# blastnxml_parse.py

def choosefields():
    
    import sys                            # this is redundant (and ignored) if imported in the main script.

    exit = False
    
    availableFields = {                   # This dictionary can be modified to represent
            1: 'hit_title',               # any field in the BLAST result that you want
            2: 'hit_accession',
            3: 'hit_description',         # to include.
            4: 'hit_score',
            5: 'hit_evalue',
            6: 'percent_id',
            7: 'align_ln',
            8: 'alignments'
            }

    print()
    print()
    fieldKeys = availableFields.keys()
    for key in sorted(fieldKeys):
        print('\t {0!s})\t {1}'.format(key, availableFields[key]))
    print()
    print()
    print('Enter a number from the menu to select the field(s) to display.')
    print('Re-enter a number to remove the selection.')
    print('The fields will be displayed in the order of selection.')
    print('Enter 0 (i.e.,zero) to accept your entries.')
    print('Type "quit" or "q" to exit the program.')
    print()
    print()

    orderedFieldList = []
    while not exit:
        print('Current selection: ')
        print(orderedFieldList)
        menuChoice = input('Menu choice: ')
        if menuChoice in ['q', 'quit']:
            sys.exit()
        else:
            try:
                menuChoice = int(menuChoice)
            except:
                print('Not a valid entry!')
                continue
            if menuChoice != 0 and menuChoice not in availableFields:
                print('Selection is not in the menu!')
                continue
            else:
                if menuChoice == 0:
                    exit = True
                elif availableFields[menuChoice] not in orderedFieldList:
                    orderedFieldList.append(availableFields[menuChoice])
                elif availableFields[menuChoice] in orderedFieldList:
                    orderedFieldList.remove(availableFields[menuChoice])

    return orderedFieldList


def extractitem(field, hit):

    def extracthittitle():
        return hit.title

    def extractaccession():
        splitTitle = hit.title.split(' ')
        identifierFields = splitTitle[0].split('|')
        accession = identifierFields[3]
        return accession

    def extractdescription():
        splitTitle = hit.title.split('|')
        description = splitTitle[-1]
        return description

    def extractscores():
        scoreList =[]
        for hsp in hit.hsps:
            scoreList.append(hsp.score)
        scoreString = ','.join(map(str, scoreList))
        return scoreString

    def extractevalues():
        evalueList = []
        for hsp in hit.hsps:
            evalueList.append(hsp.expect)
        evalueString = ','.join(map(str, evalueList))
        return evalueString

    def extractpcntid():
        percentList = []
        for hsp in hit.hsps:
            percentList.append(round(((hsp.identities / hsp.align_length) * 100), 2))
        percentString = ','.join(map(str, percentList))
        return percentString

    def extractalnlen():
        lengthList = []
        for hsp in hit.hsps:
            lengthList.append(hsp.align_length)
        lengthString = ','.join(map(str, lengthList))
        return lengthString

    def extractalignment():
        hspList = []
        for hsp in hit.hsps:
            hspList.append(hsp)
        return hspList

    
    import sys

    funcDict = {
            'hit_title': extracthittitle(),
            'hit_accession': extractaccession(),
            'hit_description': extractdescription(),
            'hit_score': extractscores(),
            'hit_evalue': extractevalues(),
            'percent_id': extractpcntid(),
            'align_ln': extractalnlen(),
            'alignments': extractalignment()
            }

    if field not in funcDict:
        print('Error: "field" argument passed to extractitem() is not valid.')
        sys.exit()
    else:
        return funcDict[field]



if __name__ == '__main__':
        
    # This is test code to ensure the functions work.

    from Bio.Blast import NCBIXML

    fileName= input('Enter an xml blast result file: ')
    with open(fileName) as fileHandle:
        blastResult = NCBIXML.read(fileHandle)
        # testing only the first alignment in the blast results
        testBlastHit = blastResult.alignments[0]

        selection = choosefields()
        print('\nThe field selection list: {}'.format(selection))

        for number, item in enumerate(selection, start=1):
            print('\nreturned result from selection {0}. {1}: {2}'.format(number, item, extractitem(item, testBlastHit)))
           

