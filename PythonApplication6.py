
#   imports for face recognition    #
import cv2
import numpy as np
import face_recognition as fr
import os
import re
from datetime import *

#   imports for speech recognition  #
import speech_recognition as sr
#import tensorflow
#import transformers
#import sounddevice as sd
#from gtts import gTTS

#   some extra imports   #
import pyttsx3
import psutil
import webbrowser
import pyjokes
import wikipedia
import pywhatkit
from browser_history.browsers import *

#   capture Video   #
cap = cv2.VideoCapture(0)

#   some global declaration    #
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
userType = ""


#   face recognition function   #
def faceRecognition():
    print("this is face recogniton function")
    path = "PrimaryUserImages"
    myList = os.listdir(path)
    classNames = []
    images = []
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    #   finding encodings   #
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    encodeListKnown = encodeList
    print('Encoding Complete')
    #   capture Video   #
    #cap = cv2.VideoCapture(0)
    #   Logic to check userType    #
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = fr.face_locations(imgS)
        encodesCurFrame = fr.face_encodings(imgS,facesCurFrame)
        try:
            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = fr.compare_faces(encodeListKnown,encodeFace)
                faceDis = fr.face_distance(encodeListKnown,encodeFace)
            if (not matches) and (not faceDis):
                userType = "NonPrimary User"
                #return userType
                greet(userType)
        except:
            continue
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            #name = classNames[matchIndex].upper()
            userType = "Primary User"
            greet(userType)
            #break
        else:
            userType = "NonPrimary User"
            greet(userType)
            #break
    #return userType
    #speechRecognition(userType)


#   speak function   #
def speak(audio):
    engine.say(audio)
    print('RON: ',audio)
    engine.runAndWait()

#   function to take commands   #
def takeCommand():
    #   It takes microphone input from the user and returns string output   #
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 1000
        r.pause_threshold = 1
        audio = r.listen(source, timeout = 5, phrase_time_limit = 5)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:   
        print("Say that again please...")
        query = takeCommand().lower()
    return query

#   function for query processing   #
def queryProcessing():
    pass

#   function to search something on wikipedia   #
def wikiSearch(query):
    speak('Searching Wikipedia ...')
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    print("According to Wikipedia ",results)
    speak(results)

#   function to play something on youtube   #
def youtubeSearch(query):
    msg = "playing " + query
    speak(msg)
    pywhatkit.playonyt(query)

#   fucntion to search something on google  #
def webSearch(query):
    msg = "searching google"
    speak(msg)
    pywhatkit.search(query)

#   fucntion to show recent browser histories    #
def browseHistory():
    if userType == "Primary User":
        try:
            e = Edge()
            outputs = e.fetch_history()
            eis = outputs.histories
            ran = len(eis)
            speak("Your past 5 web searches are:")
            print("Your past 5 web searches are:")
            for l in range(ran, ran - 5, -1):
                for j in range(0, 2):
                    print(eis[l-1][j], "\n")
        except:
            print('MS Edge not found')
    else:
        speak("You are not my Primary User and that's why you cannot have such details")

#   function to find a location on google map   #
def showLocation(query):
    query = query.split(" ")
    url = "https://www.google.com/maps/place/" + str(query[2])
    webbrowser.register('edge', None, webbrowser)
    webbrowser.get("edge").open(url)

#   function to send messages on whatsapp   #
def whatsapp(query):
    print('you')
    pywhatkit.sendwhatmsg('+919410602135', 'query', )

#   email function     #
def sendEmail():
    print('this is an email function')
    with open("UserDetails\\User Detail 1.txt", "r+") as fp:
        for line in fp:
            lilo = line
            if 'outlook: ' in lilo:
                lilo = lilo.replace('outlook: ',"")
                print(lilo)

#   greet function     #
def greet(userTypeValue):
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        msg = "Good Morning!" + userTypeValue
        speak(msg)
    elif hour >= 12 and hour < 18:
        msg = "Good Afternoon!" + userTypeValue
        speak(msg)
    else:
        msg = "Good Evening!" + userTypeValue
        speak(msg)

    speak("I am RON a chatbot. What is your name ?")
    query = takeCommand().lower()
    msg = "Hello " + query + " will you be my friend ?"
    speak(msg)
    
    query = takeCommand().lower()
    friendRespNo = ["no", "no i will not", "i hate you", "get lost", "go away", "leave me alone", "sorry but not this time", "bye"]
    for response in friendRespNo:
        if response in query:
            msg = "well ok then, Goodbye and have a wonderful journey !"
            speak(msg)
            os._exit(0)
    friendRespYes = ["yes", "yeah sure", "fine", "okay", "ok", "of course", "yes i will", "i will"]
    for response in friendRespYes:
        if response in query:
            msg = "cool, we will be great friends"
            speak(msg)
    main()

#   main function   #
def main():

    speak("lets chat")    
    query = takeCommand().lower()
    if 'wikipedia' in query:
        wikiSearch(query)
    if 'youtube' in query:
        youtubeSearch(query)
    if 'google' in query and 'search' in query:
        webSearch(query)
    if 'history' in query and 'browser' in query:
        browseHistory()
    if 'where is' in query:
        showLocation(query)
    if 'whatsapp' in query:
        whatsapp(query)
    if 'send' in query and ' email' in query:
        sendEmail()

    #   ask user to end this conversation if they want to   # 
    msg = "Hey buddy do you want to continue this conversation ?"
    speak(msg)
    query = takeCommand().lower()
    contThisConvo = ["no", "no please end this", "please end this", "no bye for now", "this is it", "end this", "get lost", "get lost you moron"]
    for response in contThisConvo:
        if response in query:
            msg = "ok bye, take care"
            speak(msg)
            os._exit(0)
        else:
            speak("cool")
            main()
    
    cv2.waitKey(1)
    
#   calling main function   #
if __name__ == "__main__":
    faceRecognition()
