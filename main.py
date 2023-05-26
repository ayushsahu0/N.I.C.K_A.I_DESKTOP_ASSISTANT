import datetime
import webbrowser
import time
import speech_recognition as sr
import os
import cohere
import random
import requests
import wikipedia
import pyjokes


def news():
    main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=f98955c2a3624b83b03fa83002e45ec5"
    news = requests.get(main_url).json()
    # print (news)
    art = news["articles"]
    news_article = []
    try:
        for arti in art:
            news_article.append(arti['title'])
        for i in range(len(news_article)):
            print(news_article[i])
            say(news_article[i])
    except Exception as e:
        return "Some error Occurred"


def weather(query):
    api_key = "90421dc3c3c0afa180b699112925982c"

    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=imperial"
    )

    if weather_data.json()['cod'] == '404':
        say("Sorry sir,No City Found")
    else:
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        cel = (temp - 32) / 1.8
        say(f"Sir The weather in {query} is: {weather}")
        print(f"Sir The weather in {query} is: {weather}")
        say(f"Sir The temperature in {query} is: {int(temp)}ºF or {int(cel)}ºC")
        print(f"Sir The temperature in {query} is: {int(temp)}ºF or {int(cel)}ºC")


def temp(query):
    api_key = "90421dc3c3c0afa180b699112925982c"

    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=imperial")

    if weather_data.json()['cod'] == '404':
        say("Sorry sir,No City Found")
    else:
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        cel = int((temp - 32) / 1.8)
        say(f"Sir The temperature in {query} is: {int(temp)}ºF or {cel}ºC")
        print(f"Sir The temperature in {query} is: {int(temp)}ºF or {cel}ºC")


def ai(prompt):
    co = cohere.Client('Q2pCS3C0XxqcSYnUMPfHy9EiJCHpsqHtufeXaP8X')  # This is your trial API key
    text = f"cohere response for Prompt: {prompt} \n *********************************************** \n"
    response = co.generate(
        model='command',
        prompt=prompt,
        max_tokens=300,
        temperature=0.9,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE')
    try:
        print('{}'.format(response.generations[0].text))
        text += '{}'.format(response.generations[0].text)
        if not os.path.exists("COHERE"):
            os.mkdir("COHERE")

        # with open(f"COHERE/prompt-{random.randint(1,9999999999999999)}","w") as f:
        with open(f"COHERE/prompt-{prompt[35:70]}.txt", "w") as f:
            f.write(text)
            say(f"Your Response is saved at COHERE/prompt-{prompt[0:25]}.txt")
    except Exception as e:
        return "Some error Occurred"


def say(text):
    os.system(f"say {text}")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error Occurred"


if __name__ == '__main__':
    say("Hello I am NICK A.I")
    while True:
        say("Do you want to talk to me??")
        print("Say YES or NO")
        print("Listening....")
        res = takecommand()
        if res.lower() == "yes":
            say("How can I help You")
            print("Listening....")
            query = takecommand()
            if query.lower() == "bye nick":
                say("Bye from NICK A.I")
                quit()
            else:
                sites = [["youtube", "https://youtube.com"], ["wikipedia", "https://wikipedia.com"],
                         ["google", "https://google.com"]
                    , ["github", "https://github.com"], ["instagram", "https://instagram.com"],
                         ["spotify", "https://spotify.com"]]
                apps = [["spotify", "/Applications/Spotify.app"]]
                if f"open".lower() in query.lower():
                    for site in sites:
                        if f"{site[0]}".lower() in query.lower():
                            webbrowser.open(site[1])
                            say(f"Opening {site[1]} sir")
                        elif f"chadgpt open {site[0]}".lower() in query.lower():
                            webbrowser.open(site[1])
                            say(f"Opening {site[1]} sir")

                elif f"time".lower() in query.lower():
                    strftime = datetime.datetime.now().strftime("%H:%M:%S")
                    say(f"Sir the time is {strftime}")
                    print(f"{strftime}")
                elif f"using artificial intelligence".lower() in query.lower():
                    ai(query)
                elif f"temperature".lower() in query.lower():
                    cities = query.split(" ")
                    city = cities[-1]
                    temp(city)
                elif f"weather".lower() in query.lower():
                    cities = query.split(" ")
                    city = cities[-1]
                    weather(query)
                elif f"news".lower() in query.lower():
                    news()
                elif f"google search".lower() in query.lower():
                    words = query.split(" ")
                    word = " ".join(words[2:])
                    webbrowser.open('https://www.google.com/search?q=' + word)
                    say("Opening google sir")
                elif f"wikipedia".lower() in query.lower():
                    words = query.split(" ")
                    word = " ".join(words[1:])
                    res = wikipedia.summary("word")
                    text = f"response for Wikipedia Search:  \n *********************************************** \n"
                    if not os.path.exists("Wikipedia"):
                        os.mkdir("Wikipedia")
                    with open(f"Wikipedia/res {word}.txt", "w") as f:
                        text += res
                        f.write(text)
                        say(f"Your wikipedia Response is saved at Wikipedia/res {word}.txt")
                elif f"joke".lower() in query.lower():
                    try:
                        joke = pyjokes.get_joke()
                        say(joke)
                        print(joke)
                    except Exception as e:
                        say("Some error Occurred")



        elif res.lower() == "no":
            say("Thank you sir Hope to see you soon")
            say("Bye from NICK A.I")
            quit()
        else:
            say("Sorry i didnot understand that")
            say("Please try again")


