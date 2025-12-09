import speech_recognition as sr
import datetime, os, psutil, datetime, json, pyttsx3, requests, re, smtplib
from google import genai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pogoda_spisok=["Thunderstorm","Drizzle","Rain","Snow","Mist","Smoke","Haze","Dust","Fog","Sand","Ash","Squall","Tornado","Clea","Clouds"]
pogoda_spisok_ru=["сейчас идет гроза","идет мелкий дождь","идет дождь","идет снег","есть туман","имеется большая влажность","имеется мгла","идет небольшая пыльная буря","имеется густой туман","имеется песчанная пыль","идет вулканический пепел","идет сильный ветер","сейчас идет торнадо","ясно","облачно"]
kz_time_hour = ["нол","быр","екы","уш","торт","бес","алты","жеты","сегыз","тогыс","он","он быр","он екы", "он уш", "он торт", "он бес", "он алты", "он жеты", "он сегыз", "он тогыс", "жиырма", "жиырма быр", "жиырма екы", "жиырма уш"]
months_ru = ["none","январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
minutes_kz = ["нол","быр", "екы", "уш", "торт", "бес", "алты", "жеты", "сегыз", "тогыз","он", "он быр", "он екы", "он уш", "он торт", "он бес", "он алты", "он жеты", "он сегыз", "он тогыз","жиырма", "жиырма быр", "жиырма екы", "жиырма уш", "жиырма торт", "жиырма бес", "жиырма алты", "жиырма жеты", "жиырма сегыз", "жиырма тогыз","отыз", "отыз быр", "отыз екы", "отыз уш", "отыз торт", "отыз бес", "отыз алты", "отыз жеты", "отыз сегыз", "отыз тогыз","кырык", "кырык быр", "кырык екы", "кырык уш", "кырык торт", "кырык бес", "кырык алты", "кырык жеты", "кырык сегыз", "кырык тогыз","елу", "елу быр", "елу екы", "елу уш", "елу торт", "елу бес", "елу алты", "елу жеты", "елу сегыз", "елу тогыз"]
months_kz = ["none","кантар", "акпан", "наурыз", "сауыр", "мамыр", "маусым", "шылде", "тамыз", "кыркуйек", "казан", "караша", "желтоксан"]
pogoda_spisok_kz = ["казыр найзахай болып жатыр","усак жанбыр жауып жатыр","жанбыр жауып жатыр","кар жауып жатыр","туман бар","ылхалдылык жохары","калын мнар бар","аздап шанды дауыл сохып жатыр","калын туман бар","шанды ауа бар","вулкандык кул тусып жатыр","катты жел сохып жатыр","казыр торнадо журып жатыр","ашык","бултты"]
with open("config.json","r", encoding="utf-8") as file:
    data = json.load(file)
    
def speak(what):
    speak_engine = pyttsx3.init()
    speak_engine.say(what)
    speak_engine.runAndWait()

def recognate(rec, opts, kz_opts, lang):
    try:
        with sr.Microphone(device_index=1) as source:
            print("скажи что нибуть")
            audio = rec.listen(source)
        query = rec.recognize_google(audio, language=lang)
        query = query.lower().strip()
        if lang == "ru-RU":
            for x in opts["alibas"]:
                if query.startswith(x):
                    query = query[len(x):].strip()
                    break
                else:
                    return "no me"
            for x in opts["tbr"]:
                if query.startswith(x):
                    query = query[len(x):].strip()
                    break
            print("После обработки:", query)
            return query
        elif lang == "kk-KZ":
            for x in kz_opts["alibas"]:
                if query.startswith(x):
                    query = query[len(x):].strip()
                    break
            for x in kz_opts["tbr"]:
                if query.startswith(x):
                    query = query[len(x):].strip()
                    break
            print("После обработки:", query)
            return query

    except sr.exceptions.UnknownValueError:
        return "none"

def radio():
    os.system("start https://rusradio.hostingradio.ru/rusradio128.mp3")
    otvet = input("выключить радио")
    if otvet == "да":
        for i in psutil.process_iter():
            if i.name() == "360extremebrowser.exe":
                i.kill()
            else:
                pass
def datetimes(lang):
    hourkz = "none"
    now = datetime.datetime.now()
    if lang == "ru-RU":
        print(now.hour, now.minute)
        speak("Сейчас" + str(now.hour) + "часов" + str(now.minute) + "минут")
    elif lang == "kk-KZ":
        for i in range (23):
            if i == now.hour:
                hourkz = kz_time_hour[i]
        for i in range(59):
            if i == now.minute:
                minutekz = minutes_kz[i]
        print("Казыр," + hourkz + ", " + "сахат, " + minutekz + ",минут")
        speak("Казыр," + hourkz + ", " + "сахат, " + minutekz + ",минут")        
def today(lang):
    if lang == "ru-RU":
        now = datetime.datetime.today()
        year = now.year - 2000
        mount = months_ru[now.month]
        day = now.day
        speak("сейчас" + str(day) + mount + " две тысячи " + str(year) + " года")
    elif lang == "kk-KZ":
        now = datetime.datetime.today()
        year = "екы мын жиырма бес"
        mount = months_kz[now.month]
        day = minutes_kz[now.day]
        speak("бугын " + str(day) + ','+ mount + ',' + str(year) + " жылы")
        
def pogodas(lang):
    responce = requests.get("").json()
    gradys = str(int(responce["main"]["temp"]))
    if lang == "ru-RU":
        for i in range(15):
            if responce["weather"][0]["main"] == pogoda_spisok[i]:
                pogoda = pogoda_spisok_ru[i]
        if '-' in gradys:
            gradys.replace('-',"минус ")

        result = "сейчас температура " + gradys + " градусов, " + "скорость ветра " + str(int(responce["wind"]["speed"])) + " метра в секунду, " + pogoda
        speak(result)
    elif lang == "kk-KZ":
        for i in range(15):
            if responce["weather"][0]["main"] == pogoda_spisok[i]:
                pogoda = pogoda_spisok_kz[i]
        skorost_vetra = minutes_kz[int(responce["wind"]["speed"])]
        if '-' in gradys:
            gradys = abs(int(gradys))
            print(gradys)
            gradys = "минус " + minutes_kz[int(gradys)]
        else:
            gradys = minutes_kz[int(gradys)]

        result = "казыр температура " + gradys + " градус, " + "жел жылдамдығы " + str(skorost_vetra) + " секундына метр, " + pogoda
        print(result)
        speak(result)

def gmai(rec, lang):
    client = genai.Client(api_key="")
    if lang == "ru-RU":
        speak("говорите свой вопросс")
    elif lang == "kk-KZ":
        speak("сурахынызды айтыныз")
    try:
        with sr.Microphone(device_index=1) as source:
            audio = rec.listen(source)
            query = rec.recognize_google(audio, language=lang)
    except sr.exceptions.UnknownValueError:
        if lang == "ru-RU":
            speak("реч не распознанна, отмена действий")
        elif lang == "kk-KZ":
            speak("сойлеу танылмахан арекеттерды болдырмау")
        return None
    speak("ответ генерируется, этой займет время")
    responce = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=query
    )
    text = responce.text.lower() # <-- вызываем метод
    if lang == "ru-RU":
        new_s = re.sub(r"[{}:()!?\-\"*\[\]]", " ", text)
    elif lang == "kk-KZ":
        new_s = re.sub(r"[{}:()!?\-\"*\[\]]", " ", text)
        new_s = re.sub(r"[әғқңөһі]", "ахкнохы", new_s)
    speak(new_s)
    
def napomni(rec, lang):
    with sr.Microphone(device_index=1) as source:
        if lang == "ru-RU":
            speak("говорите")
        elif lang == "kk-KZ":
            speak("сойлеу")
    audio = rec.listen(source)
    query = rec.recognize_google(audio, language=lang)
    query = query.lower().strip()
    napomnidata = open("data.txt",'w',-1,'utf-8')
    napomnidata.write(query)
    napomnidata.close()
    if lang == "ru-RU":
        speak("сохранено")
    elif lang == "kk-KZ":
        speak("сакталды")
def napomni_speek(lang):
    napomnidata = open("data.txt",'r',-1,'utf-8')
    textan = napomnidata.load().lower()
    if textan == "None":
        napomnidata.close()
    else:
        napomnidata.close()
        if lang == "kk-KZ":
            textan = re.sub(r"[әғқңөһі]", "ахкнохы", textan)
            speak("Ескертуды келтыремын, " + textan)
        elif lang == "ru-RU":
            speak("цетирую напоминание, " + textan)

        napomnidata = open("data.txt",'r',-1,'utf-8')
        napomnidata.write("None")
        napomnidata.close()
def budilnik(lang):
    if lang == "ru-RU":
        speak("доброе утро, пора вставать")
    elif lang == "kk-KZ":
        speak("кайырлы тан, туру уакыты")


def emailsend(rec, lang):
    if lang == "ru-RU":
        speak("Говротие сообщение")
    elif lang == "kk-KZ":
        speak("хабарлама айт")
    try:
        with sr.Microphone(device_index=1) as source:
            audio = rec.listen(source)
            query = rec.recognize_google(audio, language=lang)
    except sr.exceptions.UnknownValueError:
        if lang == "ru-RU":
            speak("я вас не понял, отмена действий")
        elif lang == "kk-KZ":
            speak("Мен сызды тусынбедым, арекетты токтатыныз")
        return None
    
    msg = MIMEMultipart()
    msg['From'] = data["sendemail"]
    msg['To'] = data["emailrecv"]
    msg.attach(MIMEText(query, 'plain'))
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(data["sendemail"], data["passemail"])
    text = msg.as_string()
    server.sendmail(data["sendemail"], data["emailrecv"], text)
    server.quit()
    if lang == "ru-RU":
        speak("сообщение отправленно")
    elif lang == "kk-KZ":
        speak("хабарлама жыберылды")

