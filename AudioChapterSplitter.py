import whisper
import ffmpeg
#import subprocess
import numpy as np
from datetime import timedelta
import traceback
from mutagen.mp3 import MP3
import argparse

# a function that takes a file and a start and length timestamps, and will return the audio data in that section as a np array 
# which the model's transcribe function can take
def getAudioBuffer(file, Start, Length):

    out, _ = (
        ffmpeg.input(file, threads=0)
            .filter('atrim', start=Start, duration=Length)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
    )

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
# a function that takes a file and an interval that deterimines the distance between each timestamp in the outputted dictionary
def transcribeTimeStamps(file, start, interval, end):
    dict = {}
    pos = start
    try:
        while(1):
            print(str(round((pos/end)*100, 2)) + "% complete")
            result = model.transcribe(getAudioBuffer(file, pos, interval))
            if "chapter" in result["text"].lower():
                #dict.update({ str(pos) + "," + str(pos+interval) : result["text"]})
                dict.update({ pos : pos+interval })

            if pos >= end:
                return dict
            if pos + interval > end:
                pos = pos + (end-pos)
            else:
                pos = pos + interval
    except:
        #traceback.print_exc()
        return dict


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help = "Defines file to read from")

args = parser.parse_args()

if args.input:
    file = args.input

print(file)

#file = input("Enter a path to an mp3 file:")

# main code 

model = whisper.load_model("base") #small

#file = "all_system_red.mp3"

#file = "long_output.mp3"

length = MP3(file).info.length

print("Starting first pass...")

dictty = transcribeTimeStamps(file, 0, 120, length)

print("Starting second pass")

dictty2 = {}
for start, end in dictty.items():

    temp = transcribeTimeStamps(file, start, 30, end)
    for tempStart, tempEnd in temp.items():
        dictty2.update({tempStart : tempEnd})

print("Starting third pass")

dictty3 = {}
for start, end in dictty2.items():

    temp = transcribeTimeStamps(file, start, 5, end)
    for tempStart, tempEnd in temp.items():
        dictty3.update({tempStart : tempEnd})

stringgy = ""
for timestamp, text in dictty3.items():
    stringgy = stringgy + "Chapter at about ~" + str(timedelta(seconds=timestamp)) + "\n"

print (stringgy)




