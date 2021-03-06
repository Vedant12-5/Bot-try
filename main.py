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

raw=sr.Recognizer()

def record_audio(ask=False):
    with sr.Microphone() as source: #source is a variable in which user speech is stored
        if ask:
            bot_speak(ask)

        raw.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        audio = raw.listen(source)

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
        
    if 'open' in voice_data:
        extensions = {'python': '.py', 'text': '.java', 'executable': '.exe', 'java': '.txt'}
        flag = 0
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        search_file = record_audio("Name the file you want to search")
        
        for extension in extensions:
            buffer = search_file + extensions[extension]
            for drive in drives:
                listing = os.walk(drive)
                for root_path, directories, files in listing:
                    if buffer in files:
                        path = os.path.join(root_path, search_file)
                        bot_speak("File found at" + path +" Opening file")
                        flag = 1
                        os.startfile(path)
                        break
        if flag == 0:
            bot_speak("File Not Found At: " + path)

    if 'camera' and 'audio' in voice_data: #with audio
        cam = cv2.VideoCapture(0)
        count = 1
        capture_success = 0
        while capture_success == 0:
            ret, img = cam.read()
            bot_speak("Camera Opened")
            cv2.imshow("CAMERA", img)
            task = record_audio()
            if capture_success == 1:
                break
            elif not ret:
                capture_success = 1
                break
            if 'close' in task:
                cam.release()
                cv2.destroyAllWindows()
                capture_success = 1
                bot_speak("Closing Camera")
                break
            elif 'capture' in task:
                file = record_audio("What is you file name")
                file = file.lower()
                file = 'E:/Python/'+file+'.jpg'
                cv2.imwrite(file, img)
                bot_speak("Capture Successful")
                capture_success = 1
                
                
    if 'camera' and 'keys' in voice_data:
        cam = cv2.VideoCapture(0)
        address = "http://192.168.43.150:8080/video" #IP address from IP-Cam
        cam.open(address)
        count = 0
        while True:
            ret, img = cam.read()
            cv2.imshow("Test", img)
            if not ret:
                break
                
            k=cv2.waitKey(1)

            if k%256==27:
                #For Esc key
                print("Close")
                break

            elif k%256==32:
                #For Space key
                print("Image "+str(count)+"saved")
                file = record_audio("What do you want to keep the file name??")
                file = file.lower()
                file='E:\python'+file+'.jpg'
                cv2.imwrite(file, img)
                count +=1
                
        cam.release()

        cv2.destroyWindow('Test') 
        
    if 'restart' in voice_data:
        bot_speak('Restarting your laptop')
        subprocess.call(["shutdown","/r"])
        
     if 'shutdown' in voice_data:
        bot_speak('Shutting down your laptop')
        subprocess.call(["shutdown","/s"])       

    if 'exit' in voice_data:
        exit()


time.sleep(1)
bot_speak('How can I help you?')
while 1:
    voice_data=record_audio()
    respond(voice_data)

