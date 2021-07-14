"""

This program tells you the note to play on
a harmonica given any note.

For example:

input harmonica is C harmonica
input note is C4
output note is 1 blow

"""
import harmonicas
import music21 as m21

key = input('Select harmonica key (and pitch): ')
if len(key) < 2:
    key = input('No, you have to choose something like "C4" or "B4-" or else it doesn\'t work: ')
harm = harmonicas.make_harmonica(key)

#This is for use with a MXL file
input_file = 'toconvert/Littleroot Town.mxl'
mxl_file = m21.converter.parse(input_file)
part_num = input('which part? (int, 0-#ofstaves)')
remove_chords = input('Reduce chords? (no or (keep) "high"/"low"): ')
output_name = input("File output name: \n")
outfile = open('output/' + output_name + '.txt', 'w')

#We want only the Treble Clef
part = mxl_file.getElementsByClass(m21.stream.Part)[int(part_num)]

#First break down part into measures
for m in range(len(part)):
    try:
        if part[m].isMeasure:
            #then for elements (notes and chords and garbage)
            for e in range(len(part[m])):
                #for notes, just get pitch
                try:
                    if part[m][e].isNote:
                        outfile.write(str(part[m][e].pitch)+'\t'+ harm[str(part[m][e].pitch)]+'\n')
                        #append harmonica note as lyric
                        part[m][e].addLyric(harm[str(part[m][e].pitch)])
                except AttributeError:
                    continue
                #for chords, convert each individual note
                try:
                    if part[m][e].isChord:
                        if remove_chords not in ['high', 'High', 'low', 'Low']:
                            tmp = [str(a.pitch) for a in part[m][e]]
                            pos = [harm[e] for e in tmp]
                            outfile.write(str(tmp)+'\t'+str(pos)+'\n')
                            chord_lyric = str()
                            for _ in range(len(tmp)):
                                chord_lyric += pos[_] + '\n'
                            part[m][e].addLyric(chord_lyric)
                        elif remove_chords in ['High', 'high']:
                            outfile.write(str(part[m][e][-1].pitch)+'\t'+ harm[str(part[m][e][-1].pitch)]+'\n')
                            part[m][e].addLyric(harm[str(part[m][e][-1].pitch)])
                        elif remove_chords in ['Low', 'low']:
                            outfile.write(str(part[m][e][0].pitch)+'\t'+ harm[str(part[m][e][0].pitch)]+'\n')
                            part[m][e].addLyric(harm[str(part[m][e][0].pitch)])
                except AttributeError:
                    continue
    #resolve from first try (check if measure)
    except AttributeError:
        continue

outfile.close()
part.write('mxl', fp= 'output/' + output_name)