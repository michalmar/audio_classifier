import sys
import os
from os import path
from pydub import AudioSegment
import uuid

# os.getcwd()

def main(foldername, classname="cough", srate=44100):
    files = os.listdir(foldername)
    i = 0
    for filename in files:

        print(filename)
        fileparts = filename.split('.')
        # process only mp3 files
        if (len(fileparts) < 2):
            continue
        if (fileparts[1] != 'mp3'):
            continue
        # assert fileparts[1] == 'mp3'

        filepath = os.path.join(foldername, filename)

        # files                                                                         
        # src = "../COVID-19-train-audio/not-covid19-coughs/PMID-16436200/1745-9974-2-1-S1.mp3"
        src = filepath

        #TODO
        dst = f"./data/{classname}-{uuid.uuid1()}.wav"

        # convert wav to mp3                                                            
        sound = AudioSegment.from_mp3(src)
        sound = sound.set_frame_rate(srate)
        sound.export(dst, format="wav")
        i += 1

    return i
    

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError(' usage python convert_mp3_to_wav.py <FOLDER> <CLASSNAME>')
    
    num_files = main(sys.argv[1], classname=sys.argv[2])
    print(f"Converted {num_files} files.")


