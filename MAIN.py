import speech_recognition as sr
from function import recognate, radio, speak, datetimes, today, pogodas, gmai, napomni, napomni_speek, budilnik, emailsend
import json, pyttsx3, time, datetime
from fuzzywuzzy import fuzz

opts = {
    "alibas":('алтын адам','алтын адам','алтын адам'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнести','какая сегодня','задай','сделай','отправь'),
    "cmds":{
        "ctime":('текущее время','сейчас время','который час','время'),
        "datatime":('какое сегодня число','какой сегодня день','день недели'),
        "radio":('включи музыку','воспроизведи музыку','включи радио'),
        "stupid1":('расскажи анигдот','рассмешименя','ты знашеь анигдоты'),
        "aisystem":('вопросс неиросети', 'вопросс искуственному интелекту'),
        "pogoda":('погода', 'температура'),
        "pkcontrol":('выключи компьютер', 'включи компьютер'),
        "napominalka":('напоминалку', 'напоминание'),
        "emailsend":('сообщение на емайл','сообщение')
    }

}


kaz_opts = {
    "alibas":('алтын адам','алтың адам','алтын адам'),
    "tbr": ('айтыңыз','расскажи','покажи','сколько','қойыңыз','айты','айт'),
    "cmds":{
        "ctime":('маған қазіргі уақыты айт','қазіргі уақытты айтшы','сағат неше болды','қазыр сағат неше','қазыр уақыт қанша'),
        "datatime":('Бүгін қандай күн','маған қазіргі күнді айт','Бүгін нешесі','қандай ай'),
        "radio":('музыканы қосады','музыканы қосады','радионы қос',),
        "pogoda":('бүгін ауа райы қандай', 'бүгін кар райы салқын','ауа температурасы неше градус'),
        "stupid1":('расскажи анигдот','рассмешименя','ты знашеь анигдоты'),
        "emailsend":('хабарлама жыберу','электрондык пошта аркылы хабарлама жыберыныз'),
        "aisystem":('задай вопросс неиросети', 'задай вопросс искуственному интелекту')
    }

}

now = datetime.datetime.now()



def slushaem(r, audio):
    try:
        voice = r.recognize_google(audio, language = "ru-RU").lower()

        if voice.startswith(opts["alibas"]): # ессли строка нанчинается на имя
            cmd = voice

            for x in opts['alias']: 
                cmd = cmd.replace(x,"").strip() # заменяем имя на ничего и я хз что дальше

            for x in opts['tbr']:
                cmd = cmd.replace(x,"").strip() # заменяет функция на ничего 
            
            cmd = recognize_cmd(cmd) # вызываем определение нашей команды
            execute_cmd(cmd['cmd']) # запускаем нашу команду
    except sr.UnknownValueError:
        speak("простите")
        time.sleep(0.5)
        speak("я вас не понял")
    except sr.RequestError as e: 
        speak("подключите меня к интеренету через настройки чтобы я мог вас понимать")

def recognize_cmd(cmd, lang):
    if lang == "ru-RU": # мы узнаем 
        RC = {'cmd': '', 'percent': 0} # словарь
        for c,v in opts['cmds'].items(): # тут мы оределяем ключи и их значения

            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt == 0:
                    speak("я вас не понял")
                    return None  #сравниваем нашу команду и функцию
                if vrt > RC['percent']: # если сраванения больше нуля
                    RC['cmd'] = c # точная наша команда
                    RC['percent'] = vrt
        return RC
    if lang == "kk-KZ":
        RC = {'cmd': '', 'percent': 0} # словарь
        for c,v in kaz_opts['cmds'].items(): # тут мы оределяем ключи и их значения

            for x in v:
                vrt = fuzz.ratio(cmd, x)  #сравниваем нашу команду и функцию
                if vrt > RC['percent']: # если сраванения больше нуля
                    RC['cmd'] = c # точная наша команда
                    RC['percent'] = vrt
        return RC
    
with open("config.json", "r") as file:
    data = json.load(file)

def execute_cmd(cmd):
    if cmd == "ctime":  # тут просто узнаем какая это функция
        datetimes(data["language"])
    elif cmd == "radio":
        radio()
    elif cmd == "datatime":
        today(data["language"])
    elif cmd == "pogoda":
        pogodas(data["language"])
    elif cmd == "aisystem":
        gmai(r, data["language"])
    elif cmd == "napominalka":
        napomni(r, data["language"])
    elif cmd == "emailsend":
        emailsend(r, data["language"])



r = sr.Recognizer()
m = sr.Microphone(device_index = 1)

with m as source:
    r.adjust_for_ambient_noise(source) # очишает звук от шумов

speak("Алтын адам готов к работе")
while True:
    if now.hour == data["BUDILHOUR"] and str(now.min) == data["BUDILMINUT"]:
        budilnik(data["language"])
    if now.hour == data["HOURNAPOM"] and now.min == data["MINUTNAPOM"]:
            napomni_speek()
    z = None
    while z == None:
        comands = recognate(r, opts, kaz_opts, data["language"])
        if comands == "none":
            continue
        elif comands == "no me":
            continue
        else:
            cmd = recognize_cmd(comands, data["language"])
            execute_cmd(cmd["cmd"])
            z = "good"


