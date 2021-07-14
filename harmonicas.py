"""
This file contains the translation information
for harmonicas. I.e. C4 is 1 blow on a C harmonica

The essential idea was to make this easy to program
with standard diatonic harmonicas.

make_harm creates a dictionary mapping for
the playable notes (holes / overblows / bends)
on the diatonic harmonica, in increasing order.
The first four notes are 1, 1', -1, and 1o which
correspond to C4, C4#, D4, and D4# on a 'C' harmonica
respectively.
"""
import music21 as m21

#%------------------------------------------%
def make_harmonica(starting_note):
    harm = dict()
    harm_notes = ['1', '(1\')', '(1)', '1o', '2', '(2\'\')', '(2\')',
                  '(2)/3', '(3\'\'\')', '(3\'\')', '(3\')', '(3)', '4',
                  '(4\')', '(4)', '4o', '5', '(5)', '5o', '6', '(6\')',
                  '(6)', '6o', '(7)', '7', '(7o)', '(8)', '8\'', '8', '(9)',
                  '9\'', '9', '(9o)', '(10)', '10\'\'', '10\'', '10', '(10o)']
    note = m21.pitch.Pitch(str(starting_note))
    for pos in harm_notes:
        harm[str(note)] = pos
        note = note.transpose(1)
    return harm
