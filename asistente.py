import datetime
from datetime import date

import pyttsx3
import sounddevice as sd
import numpy as np
import speech_recognition as sr


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

