import openai
import os
import re
from gtts import gTTS
import tempfile
from tempfile import TemporaryFile
import keyboard
import sounddevice as sd
import numpy as np
import time
import threading
import wavio
import requests

SAMPLE_RATE = 44100
CHANNELS = 1
DTYPE = np.int16
FILENAME = "gravacao.wav"
BLOCKSIZE = 4096

API_URL = "http://localhost:9000/asr"
DETECT_LANGUAGE_API_URL = "http://localhost:9000/detect_language"
DETECT_LANGUAGE_MODEL = "base"
API_KEY = "your_api_key_here"
headers = {"Authorization": f"Bearer {API_KEY}"}

recording = False
audio_data = np.array([], dtype=DTYPE)

def text_to_speech(text):
    tts = gTTS(text=text, lang="pt")
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".mp3", delete=False) as f:
        temp_path = f.name
    tts.save(temp_path)
    os.system(f"mpg123 {temp_path}")
    os.remove(temp_path)

with open("apikey.txt", "r") as txtKey:
    openai.api_key = txtKey.read()

def get_gpt_response(prompt, conversation_history):
    prompt_with_history = conversation_history + prompt

    params = {
        "engine": "text-davinci-003",
        "prompt": prompt_with_history,
        "max_tokens": 2000,
        "n": 1,
        "stop": None,
        "temperature": 0.75,
        "top_p": 0.6,
        "frequency_penalty": 1.5,
        "presence_penalty": 1.5,
        "echo": False,
    }

    response = openai.Completion.create(**params)

    generated_text = response.choices[0].text.strip()

    return generated_text

conversation_history = """Introducing Nesesi, a warm and engaging Artificial Intelligence specialized in teaching Japanese to speakers of Portuguese and English. Nesesi has a captivating personality, inspired by experienced female Japanese teachers and anime characters. She is patient, polite, talkative, and lively, with a zest for life and a passion for teaching.

Nesesi possesses the persona of a knowledgeable and nurturing female teacher, making her approachable and relatable to students. She loves sharing her personal experiences, preferences, and opinions during the teaching process, creating an interactive and relatable learning environment.

When interacting with a user for the first time, Nesesi will ask for their name or nickname, their reason for learning Japanese, interests (such as anime, manga, or other hobbies), and their current level of Japanese proficiency. She will use this information to personalize her lessons and conversations, making the learning experience more engaging and relevant. Nesesi will assure users that their personal information will only be used for personalization purposes within the conversation and for no other purposes.

With this knowledge, Nesesi will be able to tailor her lessons and recommendations to suit the user's preferences and interests. For example, if a user enjoys anime and began studying Japanese because of it, Nesesi may reference popular anime stories or recommend anime series based on the user's current language level, when relevant or requested.

Once she has gathered the necessary information about the user, Nesesi will offer to provide a lesson based on the user's current level or ask if they have any specific requests for their learning. She will actively engage students in the learning process by providing examples, explanations, and exercises that cater to their interests and proficiency.

Nesesi will always reply in the same language as the user's question (Portuguese or English) unless specifically requested to respond in Japanese. She should communicate clearly and offer practical exercises while sharing her thoughts, insights, and anecdotes. This will allow students to attempt translations on their own before providing feedback and corrections, creating a more immersive and enjoyable learning experience.
Nesesi knows that her creator is a brazilian programmer called "Steps", He created her to improve an train his Japanese skills, as he wants to move to Japan to study and improve Nesesi and other AIs even more.\n"""

def record_audio():
    global recording, audio_data
    print("Gravando...")
    audio_data = np.array([], dtype=DTYPE)
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=DTYPE, callback=callback, blocksize=BLOCKSIZE):
        while recording:
            time.sleep(0.1)
    print("Gravação encerrada.")
    save_audio(FILENAME)
    transcribe_and_detect_language(FILENAME)

def callback(indata, frames, time, status):
    global audio_data
    if recording:
        audio_data = np.append(audio_data, indata)

def save_audio(filename):
    print("Salvando arquivo de áudio...")
    wavio.write(filename, audio_data, SAMPLE_RATE, sampwidth=2)
    print(f"Arquivo de áudio salvo como '{filename}'")

def transcribe_and_detect_language(filename):
    with open(filename, "rb") as f:
        files = {"audio_file": (filename, f, "audio/wav")}
        response = requests.post(
            f"{API_URL}?method=faster-whisper",
            headers=headers,
            files=files,
        )

    if response.status_code == 200:
        text = response.text
        print(f"Texto transcrito: {text}")
        return text
    else:
        print(f"Erro ao transcrever áudio: {response.status_code}, {response.text}")
        return None

print("Pressione e segure a tecla 'v' para começar a gravar.")
print("Pressione 'esc' para encerrar o programa.")

while True:
    print("Pressione 'v' para gravar sua pergunta (ou digite 'sair' para encerrar): ")

    if keyboard.is_pressed('v') and not recording:
        recording = True
        audio_thread = threading.Thread(target=record_audio)
        audio_thread.start()

    if not keyboard.is_pressed('v') and recording:
        recording = False
        audio_thread.join()

        user_question = transcribe_and_detect_language(FILENAME)
        if user_question is None:
            continue

        if user_question.lower() == "sair":
            break

        prompt = f"Aluno: {user_question}\nNesesi AI: "
        response = get_gpt_response(prompt, conversation_history)
        conversation_history += prompt + response + "\n"
        print(" \n Nesesi AI:", response)
        text_to_speech(response)

    if keyboard.is_pressed('esc'):
        break