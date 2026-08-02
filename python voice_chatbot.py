# IMPORT PACKAGES
import speech_recognition as sr   # Import library for taking voice input from microphone 
import pyttsx3  # import library for converting text into speech
import webbrowser # opening websites in browser
import datetime # for date and time
import wikipedia #for wikipedia search
import os # for system commands like opening apps ,shut down etc.
import requests #for weather API request
import time # for delay in reminder

# INITIALIZE TEXT-TO-SPEECH ENGINE
engine=pyttsx3.init()  
engine.setProperty('rate',170)

#STORE USERNAME
USER_NAME="Babita"

#STORE WEATHER API KEY
WEATHER_API_KEY = "52bda67c2ee18d2c568c640be58e8116"

#SPEAK FUNCTION
def speak(text):
    print("Bot:",text)
    engine.say(text)
    engine.runAndWait()

#Greeting function 
def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak(f"Good Morning {USER_NAME}")
    elif hour>=12 and hour<18:
        speak(f"Goor Afternoon {USER_NAME}")
    else:
        speak(f"Good Evening {USER_NAME}")
    speak("I am your voice activated AI chatbot. How can I help you?")

# VOICE INPUT FUNCTION
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold =1
        r.energy_threshold =300
        audio=r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print("You said:",query)
        return query.lower()
    except Exception:
        speak("Sorry, I did not understand. Please say that again.")
        return "none"
    
#TIME FUNCTION
def tell_time():
    current_time=datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

#WIKIPEDIA SEARCH FUNCTION
def search_wikipedia(query):
    try:
        topic=query.replace("search wikipedia","")
        topic=topic.replace("wikipedia","")
        topic=topic.strip()
        if topic==" ":
            speak("Please say a topic to search on wikipedia.")
            return 
        result=wikipedia.summary(topic,sentences=2)
        speak("According to Wikipedia")
        speak(result)
    except Exception:
        speak("Sorry ,I could not find information on wikipedia.")

#WEBSITE OPENING FUNCTION
def open_website(query):
    if "google" in query:
        webbrowser.open("https://www.google.com/")
        speak("Opening Google")

    elif "youtube" in query:
        webbrowser.open("https://www.youtube.com/")
        speak("Opening Youtube")

    elif "wikipedia" in query:
        webbrowser.open("https://www.wikipedia.org/")
        speak("Opening Wikipedia")

    else:
        speak("Website not recognized:")

#NOte SAVING FUNCTION
def save_note():
    speak("What should I write in the note?")
    note_text = takeCommand()

    if note_text !="none":
        with open("notes.txt","a") as file:
            file.write(note_text+"\n")
        speak("Your note has been saved.")
    else:
        speak("I could not save the note.")

# OPEN DESKTOP APPLICATIONS
def open_application(app_name):
    try:
        if "notepad" in app_name:
            os.system("notepad")
            speak("Opening Notepad")
        elif "calculator" in app_name:
            os.system("calc")
            speak("Opening Calculator")
        elif "paint" in app_name:
            os.system("mspaint")
            speak("Opening paint")
        elif "command prompt" in app_name or "cmd" in app_name:
            os.system("start cmd")
        else:
            speak("Application not recognized:")
    except Exception:
        speak("Sorry , I could not open the application.")
# CALCULATOR FUNCTION

def calculator_expression(query):
    try:
        expression= query.replace("calculate"," ")
        expression=query.replace("what is"," ")
        expression=query.strip()
        expression=query.replace("plus","+")
        expression=query.replace("minus","-")
        expression=query.replace("multiplied by","*")
        expression=query.replace("into","*")
        expression=query.replace("times","*")
        expression=query.replace("divide by","/")
        expression=query.replace("divided by","/")
        expression=query.replace("mod","%")

        result =eval(expression)
        speak(f"The answer is {result}")
    except Exception:
        speak("Sorry , I could not calculate that")

# WEATHER FUNCTION

def get_weather():
    speak("Please say the City Name:")
    city=takeCommand()

    if city=="none":
        speak("I could not understand the city name.")
        return 
    try:
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response=requests.get(url)
        data=response.json()
        
        if data["cod"]!=200:
            speak("Sorry,I could not find weather information for that city.")
            return 
        temperature=data["main"]["temp"]
        description=data["weather"][0]["description"]
        humidity=data["main"]["humidity"]
        speak(f"The temperature in {city} is {temperature} degree Celcius.")
        speak(f"The weather is {description}.")
        speak(f"Humidity is {humidity} percent.")

    except Exception:
        speak("Sorry,there was a problem getting the weather information.")

#TO-DO LIST FUNCTIONS

def add_todo():
    speak("What task do you want to add?")
    task = takeCommand()

    if task!="none":
        with open("todo.txt","a") as file:
            file.write(task + "\n")
        speak("Task added to your to do list.")
    else:
        speak("I could not add the task.")


#SHOW TASKS

def show_todo():
    try:
        with open("todo.text","r") as file:
            tasks=file.readlines()

        if len(tasks)==0:
            speak("Your to do list is empty.")
            return 
        speak("Your to do list contains:")

        for i, task in enumerate(tasks,start=1):
            print(f"{i},{task.strip()}")
            speak(f"Task {i} is {task.strip()}")

    except Exception:
        speak("Your to do list is empty.")

# REMAINDER FUNCTION
def set_reminder():
    try:
        speak("What should I remind you about?")
        reminder_text=takeCommand()

        if reminder_text=="none":
            speak("I could not understand the reminder text.")
            return 
        
        speak("After how many seconds should I remind you?")
        seconds_text=takeCommand()

        if seconds_text=="none":
            speak("I could not understand the time.")
            return 
        
        seconds=int(seconds_text)

        speak(f"Reminder set for {seconds} seconds.")
        time.sleep(seconds)
        speak(f"Remainder:{reminder_text}")
    except Exception:
        speak("Sorry, I could not set the remainder.")

#SYSTEM CONTROL FUNCTION

def system_control(query):
    try:
        if "shutdown" in query:
            speak("Shutting down the system.")
            os.system("shutdown /s /t 5")
        elif "restart" in query:
            speak("Restarting the system.")
            os.system("shutdown /r /t 5")
        elif "lock" in query:
            speak("Locking the system.")
            os.system("rundll31.exe user32.dll,LockWorkStation")

    except Exception:
        speak("Sorry, I could not perform the system command.")

# MAIN FUNCTION
def main():
    wishMe()
    while True:
        query=takeCommand()

        if query=="none":
            continue



# COMMAND CHECKING
        elif "open google" in query:
            open_website("google")
        
        elif "open youtube" in query:
            open_website("youtube")
        elif "open wikipedia" in query:
            open_website ("wikipedia")
        elif "search wikipedia" in query or "wikipedia" in query:
            search_wikipedia(query)
        elif "what is the time" in query or "tell me the time" in query:
            tell_time()
        elif "write a note" in query or "take a note" in query:
            save_note()
        elif "open notepad" in query:
            open_application("notepad")
        elif "open calculator" in query:
            open_application("calculator")
        #elif "open paint" in query:
         #   open_application(paint)
        elif "open command prompt" in query or "open cmd" in query:
            open_application("cmd")
        elif "calculate" in query or "what is" in query:
            calculator_expression(query)
        elif "wheather" in query:
            get_weather()
        elif "add task" in query or "add to do" in query or "add to-do" in query:
            add_todo()
        elif "show my task" in query or "show to do list" in query or "show to-do list":
            show_todo()
        elif "set reminder" in query:
            set_reminder()
        elif "shutdown" in query or "restart" in query or "lock system" in query:
            system_control(query)
        elif "hello" in query:
            speak(f"Hello {USER_NAME}, nice to meet you.")
        elif "how are you" in query:
            speak("I am fine . Thank you for asking.")
        elif "who are you" in query:
            speak("I am your voice activated AI chatbot.")
        elif "what is my name" in query:
            speak(f"Your name is {USER_NAME}")
        elif "bye" in query or "stop" in query or "exit" in query:
            speak(f"Goodbye {USER_NAME}")
            break
        else:
            speak("Sorry, I do not know this command yet.")
if __name__ == "__main__":
    main()