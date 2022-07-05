import speech_recognition as sr
import pyttsx3
from googletrans import Translator
from dotenv import load_dotenv
from time import ctime
import webbrowser
import random
import time
import smtplib
import requests
import os

r = sr.Recognizer()     # instance of Recognizer class to recognize speech
translator = Translator()   # initialization- creating instance
speaker = pyttsx3.init()    # object creation

voices = speaker.getProperty('voices')  # getting details of current voice

# changing index, changes voices. 0 for male
# changing index, changes voices. 1 for female
speaker.setProperty('voice', voices[1].id)

# getting details of current speaking rate
rate = speaker.getProperty('rate')

speaker.setProperty('rate', 150)    # setting up new voice rate

todo_path = "todo.txt"

def configure():
    load_dotenv()
 


class Person:   # creating Person class to store the name of the Person object
    name = 'Pallav'

    def set_name(self, name):
        self.name = name


languages = {'english': 'en', 'hindi': 'hi', 'spanish': 'es', 'french': 'fr', 'german': 'de', 'italian': 'it'}


def record_audio(query=False):  # Recording voice
    with sr.Microphone() as source:  # microphone as source
        if query:
            sallie_speak(query)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)

        except sr.UnknownValueError:
            sallie_speak('Sorry, I did not get that')
        except sr.RequestError:
            # error: recognizer is not connected
            sallie_speak('Sorry, I cannot process your request at the moment')
        print(f"Me: {voice_data.lower()}")  # print what user said
        return voice_data.lower()

# Voice Assistant reply


def sallie_speak(audio_string):
    print('Sallie: ' + audio_string)
    speaker.say(audio_string)
    # speaker.save_to_file(audio_string, 'test.mp3')
    speaker.runAndWait()


# function to iterate over the list of commands
def there_exists(list_of_words):
    for word in list_of_words:
        if word in voice_data:
            return True


def send_mail(content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('algomessiaha@gmail.com', 'sduzbwlzdsealkdx')

    subject = 'python project'
    body = content

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'algomessiaha@gmail.com',  # from mail
        'f786jamil@gmail.com',  # to mail
        msg
    )
    sallie_speak('EMAIL HAS BEEN SENT!')

    server.quit()


def create_todo():
    with open(todo_path, 'r+') as file:
        file.seek(0)
        content = []
        todo = True
        sallie_speak('what you want to add')
        while todo:
            item = record_audio()
            if 'stop' in item:
                sallie_speak('todo list completed')
                break
            content.append(item)
            sallie_speak('next item')
        print(content)
        for item in content:
            file.write(item+'\n')
        file.truncate()


# Respond to voice data
def respond(voice_data):
    # 1: greeting
    if there_exists(['hello', 'hi', 'hey']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}",
                     f"I'm listening {person_obj.name}", f"hello {person_obj.name}",
                     f"It's really good to hear from you {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        sallie_speak(greet)

    elif there_exists(["how are you", "how are you doing"]):
        sallie_speak(f"I'm very well, thanks for asking {person_obj.name}")

    elif there_exists(["what's up", "what are you up to"]):
        sallie_speak(
            "Not much! Just been looking into ways to stay healthy")
        sallie_speak("Hope you are rocking one!")

    # 2: name
    elif there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            sallie_speak("my name is Sallie")
        else:
            sallie_speak("my name is Sallie. what's your name?")

    elif there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        sallie_speak(f"okay, i will remember that {person_name}")
        person_obj.set_name(person_name)  # remember name in person object

    elif there_exists(["wrong name"]):
        sallie_speak("what should I call you?")
        person_name = record_audio()
        sallie_speak(f"Nice to meet you {person_name}")
        person_obj.set_name(person_name)  # remember name in person object

    # 4: time
    elif there_exists(["what time is it", "tell me the time", "what's the time"]):
        # time format: 'Wed Nov 11 16:49:13 2020'
        time = ctime().split()[3].split(":")[0:2]  # time = ['16', '49']
        if time[0] == "00":
            hours = "12"
            minutes = " am"
        elif time[0] == "12":
            hours = "12"
            minutes = " pm"
        elif "13" <= time[0] <= "23":
            hours = str(int(time[0]) - 12)
            minutes = " pm"
        else:
            hours = time[0]
            minutes = " am"
        minutes = time[1] + minutes
        time = f"{hours} {minutes}"  # time = '4 49 pm'
        sallie_speak(time)

    # 5: search google - ask: search for mountains
    elif there_exists(["search for"]) and ('on youtube' not in voice_data):
        search_term = voice_data.split("for")[-1].strip()
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        sallie_speak(f'Here is what I found for {search_term} on google')

    # 6: search youtube - ask: search for mountains on youtube
    elif there_exists(["on youtube"]):
        search_term = voice_data.split("for")[-1].split("on")[0].strip()
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        sallie_speak(f'Here is what I found for {search_term} on youtube')

    # 7: search location - ask: find location, search for location etc
    elif there_exists(["location"]):
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        sallie_speak('Here is the location for ' + location)

    # 8: Translator
    elif there_exists(["translate"]):
        sallie_speak('in which language do you want to translate?')
        dest_lang = record_audio()
        if dest_lang in languages.keys():
            to_translate_text = record_audio('What do you want to translate')
            translated_text = translator.translate(to_translate_text, dest=languages[dest_lang])
            sallie_speak(translated_text.text)
        else:
            sallie_speak("I didn't understand")

    # 9: Send mail
    elif there_exists(["mail", "email"]):
        try:
            sallie_speak('what should i say?')
            msg = record_audio()
            send_mail(msg)
        except Exception as e:
            sallie_speak("Sorry I am not able to send this email")

    # 10: To-Do
    elif there_exists(["todo", "list"]):
        create_todo()

    # 11: weather
    elif there_exists(["weather", "what is the weather"]):
        location = record_audio('What is the location?')
        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+os.getenv('user_api')
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()
        # create variables to store and display data
        temp_city = ((api_data['main']['temp']) - 273.15)
        weather_desc = api_data['weather'][0]['description']
        hmdt = api_data['main']['humidity']
        wind_spd = api_data['wind']['speed']
        sallie_speak(
            f'temperature is {temp_city} weather is {weather_desc} humidity is {hmdt} and wind speed is {wind_spd}')

    # 12: Exit
    elif there_exists(["exit", "quit", "goodbye", "bye"]):
        sallie_speak("going offline")
        exit()


person_obj = Person()   # create Person object
sallie_speak('How can I help you?')
while True:
    configure()
    voice_data = record_audio()  # get the voice input
    respond(voice_data)  # respond to voice data
    time.sleep(0.5)
