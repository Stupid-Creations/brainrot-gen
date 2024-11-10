# # # import google.generativeai as genai

# # # genai.configure(api_key="AIzaSyARcqGtkhHuHstUjErjF3EiZw1BlHnW5L4")
# # # model = genai.GenerativeModel("gemini-1.5-flash")

# # # response = model.generate_content("You are an expert short form content creator. Write a 1 minute speech on the french revolution on basis of the class 9th NCERT for SST. Do not put in any sort of decorators, and only provide plain text. Answer in a maximum of 140 words")
# # # print(response.text)
from moviepy.editor import *
import time
import random
from gtts import gTTS
from pygame import mixer
from pydub import AudioSegment

mixer.init()
rp = """ Theres a passage in the Principia Discordia where Malaclypse complains to the Goddess about the evils of human society. Everyone is hurting each other, the planet is rampant with injustices, whole societies plunder groups of their own people, mothers imprison sons, children perish while brothers war. The Goddess answers: What is the matter with that, if its what you want to do? """

rp.replace('\n','')
rp.replace("'",'')
rp.replace(""" " """,'')
rp.replace("’",'')

import cv2 as cv

cap = cv.VideoCapture('minerot.mp4')

tf = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
cap.set(cv.CAP_PROP_POS_FRAMES,random.randint(0,120)) #change this for one min videos to 60*30 = 1800

index = 0
loaded = rp.split(" ")
i = 0
new = []
running = ""

fourcc = cv.VideoWriter_fourcc(*'H264')
out = cv.VideoWriter('output.mp4', fourcc, 25.0, (int(1080/2.5),int(1920/2.5)))

for i in loaded:
    if cv.getTextSize(running+i,cv.FONT_HERSHEY_TRIPLEX,1,2)[0][0]>int(1080/2.5):
        new.append(running)
        running = i
    else:
        running+=" "+i

if running not in new[-1]:
    new.append(running)

def say_stuff(text,name):
    tts = gTTS(text,lang = "en",tld="co.in")
    tts.save(name)

say_stuff(rp,"oopsies.mp3")

clips = []
for i in range(len(new)):
    say_stuff(new[i],str(i)+".wav")
    clips.append(AudioFileClip(str(i)+".wav"))

final = concatenate_audioclips(clips)

ss = [mixer.Sound(str(i)+".wav") for i in range(len(new))] 
ls = [s.get_length() for s in ss]
print(ls[0])
sc = time.time()
while cap.isOpened() and index<len(new):
    if time.time()-sc >= ls[index]:
        print(time.time()-sc,ls[index])
        sc = time.time()
        index+=1
        if index >= len(new):
            break
    ret, frame = cap.read()
    frame = cv.resize(frame,(int(1080/2.5),int(1920/2.5)))
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    text = new[index]
    tsize = cv.getTextSize(text,cv.FONT_HERSHEY_TRIPLEX,1,2)[0]
    gap = tsize[1] + 10
    y = int((frame.shape[0] + tsize[1]) / 2) 
    x = int((frame.shape[1] - tsize[0]) / 2)
    cv.putText(frame,text,(x,y),cv.FONT_HERSHEY_TRIPLEX,1,(0,0,0),6,cv.LINE_AA)
    cv.putText(frame,text,(x,y),cv.FONT_HERSHEY_TRIPLEX,1,(255,255,255),2,cv.LINE_AA)

    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break



    out.write(frame)


cap.release()
cv.destroyAllWindows()

out = None 

final = AudioFileClip("oopsies.mp3")
final.write_audiofile("oopsies.wav")
final = cv.VideoCapture('output.mp4')

tf = int(final.get(cv.CAP_PROP_FRAME_COUNT))
length = tf/30
audiolen = mixer.Sound("oopsies.wav").get_length()
speed = audiolen/length
speed = 1/speed

clip = VideoFileClip("output.mp4") 
print(speed)

from pydub import AudioSegment
from pydub.effects import speedup

audio = AudioSegment.from_wav("oopsies.wav")
new_file = speedup(audio,speed)
new_file.export("file.wav", format="wav")
audio = AudioFileClip("oopsies.wav")
final_clip = clip.set_audio(audio)
final_clip.write_videofile("PLEASEPLEASEPLEASE.mp4")
