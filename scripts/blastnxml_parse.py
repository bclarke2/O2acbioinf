#! /usr/local/bin/python3.6

# blastnxml_parse.py

def choosefields():
    
    import sys                            # this is redundant (and ignored) if imported in the main script.

    exit = False
    
    availableFields = {                   # This dictionary can be modified to represent
            1: 'hit_title',               # any field in the BLAST result that you want
            2: 'hit_description',         # to include.
            3: 'hit_score',
            4: 'hit_evalue',
            5: 'hit_numalignments',
            6: 'alignments'
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
        print('\nCurrent selection: ')
        print(orderedFieldList)
        menuChoice = input('\nMenu choice: ')
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

if __name__ == '__main__':
        
   selection = choosefields()
   print('\n{}'.format(selection))

