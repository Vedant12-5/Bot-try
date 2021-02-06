import speech_recognition as sr
from time import ctime
import time
import playsound
import os
import random
from gtts import gTTS
import webbrowser
import psutil
import requests
import json 

raw=sr.Recognizer()

def record_audio(ask=False):
    with sr.Microphone() as source: #source is a variable in which user speech is stored
        if ask:
            bot_speak(ask)

        audio = raw.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        audio = raw.listen(source)
        voice_data = ''

        try:
            voice_data = raw.recognize_google(audio)

        except sr.UnknownValueError:
            bot_speak('sorry i didn\'t get it please try again')
            voice_data=record_audio()
            respond(voice_data)

        except sr.RequestError:
            bot_speak('sorry my speech service is down')
        return voice_data

def bot_speak(audio_string):
    tts=gTTS(text=audio_string, lang='en')
    f_name=random.randint(1, 10000000)
    audio_file ='audio-' +str(f_name) +'.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)    

def respond(voice_data):
    if 'What is your name' in voice_data:
        print('My name is Veda')
    if 'what time is it' in voice_data:
        print(ctime())
    if 'search' in voice_data:
        search=record_audio('What do you want to search for?')
        url= 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        print('Here is what I found for' + search)
    if 'location' in voice_data:
        location=record_audio('What is the location?')
        url= 'https://google.nl/maps/place/' + location +'/&amp;'
        webbrowser.get().open(url)
        print('Here is the location of' + location)
    if 'exit' in voice_data:
        exit()

def respond(voice_data):
    a={'hello':'hi','hi':'hello','how are you':'I\'m fine ','What is your name':'Alexa'}
    if voice_data in a :
        bot_speak(a[voice_data])#value of key is printed

    if 'what' and 'time' in voice_data:
        bot_speak(ctime())

    if 'search' in voice_data:
        search=record_audio("What do you want to search")
        url='https://google.com/search?q='+search
        webbrowser.get().open(url)
        bot_speak('Here is what i found for ' + search)

    if 'location' in voice_data:
        location=record_audio("Which location do you want to search?")
        url='https://google.nl/maps/place/' +location +'/&amp;'
        webbrowser.get().open(url)
        bot_speak('Here is what i found for ' + location)

    if 'open' and 'game' in voice_data:
        bot_speak('Opening valorant')
        os.startfile('"E:/Games/The Sinking City/TSCGame.exe"')

    if ('battery' or 'power') and ('status' or 'source') in voice_data:
        battery = psutil.sensors_battery()
        bat_status = battery.power_plugged    
        bat_percentage = str(battery.percent)
        status = 'Plugged in. '+ bat_percentage +' Percent charged and running' if bat_status else 'Device is running on battery backup, currently at' + bat_percentage + 'percent.'
        bot_speak(status)

    if 'weather' in voice_data:
        city_name = record_audio("What Is Your City?")
        api_key = "35769c7f686c3686a4bbb5ae1c621052"
        complete_url = "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}".format(city_name,api_key)
        api_link = requests.get(complete_url)
        api_data = api_link.json()
        temp = api_data['main']
        temp1 = temp['temp']
        temperature = str(int(int(temp1)-273.15))
        weather_desc = api_data['weather'][0]['description']
        bot_speak("Today's Temperature is " + temperature + " Degree Celcius and weather looks " + weather_desc)

    if 'CPU' and ('usage' or 'status') in voice_data:
        usage = str(psutil.cpu_percent(4)/psutil.cpu_count())
        bot_speak('The current CPU usage is: '+ usage +'percent')

    if 'enable' and 'bluetooth' in voice_data:
        os.system("Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser")
        os.system("powershell -command ./bluetooth.ps1 -BluetoothStatus On")
        bot_speak('Bluetooth enabled.')

    if 'disable' and 'bluetooth' in voice_data:
        os.system("Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser")
        os.system("powershell -command ./bluetooth.ps1 -BluetoothStatus Off")
        bot_speak('Bluetooth disabled.')

    if 'exit' in voice_data:
        exit()


time.sleep(1)
bot_speak('How can I help you?')
while 1:
    voice_data=record_audio()
    respond(voice_data)

