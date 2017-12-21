#! /usr/local/bin/python3.6

# blast_xmltotext.py

import sys
from Bio.Blast import NCBIXML
import blastxml_parse as bxp

E_VALUE_THRESHOLD = 0.4

while True:
    inFileName = input('\nEnter the .xml file you wish to parse: ')
    try:
        inFileHandle = open(inFileName)
        break
    except OSError:
        print('This file cannot be found in the current directory.')

outFileName = input('Enter the name of the text file to contain the output.')

blastResult = NCBIXML.read(inFileHandle)
inFileHandle.close()

alignmentChosen = False
fieldSelections = bxp.choosefields()
if 'alignments' in fieldSelections:
    alignmentChosen = True
    # find the index of 'alignments' in the fieldSelections list and
    # remove it, returning 'alignments' and storing in a variable.
    # This is done because I want the alignments data to be printed
    # after a table presenting the other chosen fields. I will return
    # to alignments later in the code.
    alignmentItem = fieldSelections.pop(fieldSelections.index('alignments'))

outFileHandle = open(outFileName, 'w')
headerLine = '\t'.join(fieldSelections)
outFileHandle.write(headerLine + '\n')

for alignment in blastResult.alignments:
    if alignment.hsps[0].expect < E_VALUE_THRESHOLD:
        for field in fieldSelections[:-1]:
            outFileHandle.write(bxp.extractitem(field, alignment) + '\t')
        outFieldHandle.write(bxp.extractitem(fieldSelections[-1], alignment) + '\n')


# add the alignments now at the end of the file if they were chosen by the user.
if alignmentChosen == True:
    outFileHandle.write('\n****Alignments****\n')
    for alignment in blastResult.alignments:
        for hsp in bxp.extractitem(alignmentItem, alignment):
            if hsp.expect < E_VALUE_THRESHOLD:
                outFileHandle.write('{0}\ne_value: {1:<15}length: {2:<15}identities: {3:<18}pcnt_id: {4:.2%}\n{5}{11}{6}\n{7}{11}{8}\n{9}{11}{10}\n\n'.format(
                    alignment.title,
                    hsp.expect,
                    hsp.align_length,
                    hsp.identities,
                    ((hsp.identities / hsp.align_length) * 100),
                    hsp.query[:50],
                    hsp.query[-6:],
                    hsp.match[:50],
                    hsp.match[-6:],
                    hsp.sbjct[:50],
                    hsp.sbjct[-6:],
                    '...'
                    ))


outFileHandle.close()

