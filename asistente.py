import datetime
import webbrowser
from datetime import date
import pyjokes
import pyttsx3
import pywhatkit
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import wikipedia
import yfinance as yf


def transformar_audio_en_texto():
    r = sr.Recognizer()

    # Parameters
    samplerate = 16000
    duration = 5  # seconds

    print("Listening...")

    # Capture audio data using sounddevice
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished

    # Convert the audio data to bytes
    audio_data = audio_data.flatten()  # Flatten the array
    audio_data_bytes = audio_data.tobytes()

    # Create AudioData instance
    audio = sr.AudioData(audio_data_bytes, samplerate, 2)

    try:
        # Recognize speech using Google Web Speech API
        pedido = r.recognize_google(audio, language='es-MX')
        print(pedido)
        return pedido
    except sr.UnknownValueError:
        print('No entendi')
        return 'Sigo esperando'
    except sr.RequestError as e:
        print('No hay servicio')
        return 'Sigo esperando'
    except Exception as e:
        print('Algo ha salido mal:', str(e))
        return 'Sigo esperando'

# Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', 'spanish-latin-am')
    engine.say(mensaje)
    engine.runAndWait()

def pedir_dia():
    #crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)
    #crear una variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    #diccionario con nombres de los dias
    calendario = {0 : 'Lunes',
                  1 : 'Martes',
                  2 : 'Miercoles',
                  3 : 'Jueves',
                  4 : 'Viernes',
                  5 : 'Sabado',
                  6 : 'Domingo'}
    #decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

#informar que hora es
def pedir_hora():
    #crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos'
    print(hora)
    #decir la hora
    hablar(hora)

# funcion saludo inicial
def saludo_inicial():
    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif hora.hour >= 6 and hora.hour < 13:
        momento = 'Buenos dias'
    else:
        momento = 'Buenas tardes'

    # decir el saludo
    hablar(f'Hola. {momento}, soy TUX, el asistente, dime en que te puedo ayudar')

# funcion central del asistente
def pedir_cosas():
    #activar el saludo inicial
    saludo_inicial()
    #variable de corte
    comenzar = True
    #loop central
    while comenzar:
        #activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()
        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com/')
            continue
        elif 'abrir el navegador' in pedido:
            hablar('Abriendo navegador')
            webbrowser.open('https://www.google.com/')
            continue
        elif 'dime el dia' in pedido:
            pedir_dia()
            continue
        elif 'dime la hora' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Buscando en internet')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar("Esto es lo que encontre")
            continue
        elif 'reproducir a' in pedido:
            hablar('Reproduciendo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'AAPL',
                   'amazon': 'AMZN',
                   'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontre, el precio de {accion} es {precio_actual} dólares')
                continue
            except KeyError:
                hablar(f'No tengo información sobre {accion}')
                continue
        elif 'terminar' in pedido:
            hablar('Terminando')
            break

pedir_cosas()
