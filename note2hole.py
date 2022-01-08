"""

This program prints tabs on sheet music
in the key of any diatonic harmonica you desire

"""
import harmonicas
import music21 as m21


#For Diatonics

key = input('Enter key of harmonica (e.g. A-3 or C4)')
harm = harmonicas.make_harmonica(key)
harm_type = 'diatonic'
"""

#For 10 hole chromatica
harm = harmonicas.make_chrom()
harm_type = 'chromatic'
"""

#This is for use with a MXL file
input_file = 'toconvert/Leadsheet_-_Californication_-_Red_Hot_Chili_Peppers.midi'
mxl_file = m21.converter.parse(input_file)
part_num = int(input('which part? (int, 0-#ofstaves)'))
trans_number = int(input('Transpose? Enter number steps or "0"'))
remove_chords = input('Reduce chords? (no or (keep) "high"/"low"): ')
output_name = input("File output name: \n")
outfile = open('output/' + output_name + '.txt', 'w')

#transpose if transpose
if trans_number != 0:
    mxl_file = mxl_file.transpose(trans_number)

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
                        outfile.write(str(part[m][e].pitch)+'\t'+ harm[part[m][e].pitch.ps] +'\n')
                        #append harmonica note as lyric
                        part[m][e].addLyric(text = harm[part[m][e].pitch.ps])
                except AttributeError:
                    pass
                #for chords, convert each individual note
                try:
                    if part[m][e].isChord:
                        if remove_chords not in ['high', 'High', 'low', 'Low']:
                            #extract notes
                            tmp = [a for a in part[m][e]]
                            #get positions
                            pos = [harm[n.pitch.ps] for n in tmp]
                            #convert to names
                            tmp = [str(a.pitch) for a in part[m][e]]
                            outfile.write(str(tmp)+'\t'+str(pos)+'\n')
                            chord_lyric = str()
                            for _ in range(len(tmp)):
                                chord_lyric += pos[_] + '\n'
                            part[m][e].addLyric(text = chord_lyric)
                        elif remove_chords in ['High', 'high']:
                            outfile.write(str(part[m][e][-1].pitch)+'\t'+ harm[part[m][e][-1].pitch.ps] +'\n')
                            part[m][e].addLyric(text = harm[part[m][e][-1].pitch.ps])
                        elif remove_chords in ['Low', 'low']:
                            outfile.write(str(part[m][e][0].pitch)+'\t'+ harm[part[m][e][0].pitch.ps]+'\n')
                            part[m][e].addLyric(text =harm[part[m][e][0].pitch.ps])
                except AttributeError:
                    pass
    #resolve from first try (check if measure)
    except AttributeError:
        pass

outfile.close()
part.write('mxl', fp= 'output/' + output_name)