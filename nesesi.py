import openai
import pyaudio
import wave
import os
import keyboard

def load_api_key(filename):
    with open(filename, 'r') as file:
        return file.read().strip()
openai.api_key = load_api_key('apikey.txt')
model_id = 'gpt-4'

def gravar_audio(nome_arquivo):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("Gravando...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Gravação finalizada.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(nome_arquivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def transcrever_e_responder(messages):
    with open("gravacao.wav", "rb") as audio_file:
        response = openai.Audio.transcribe(
            file=audio_file,
            model="whisper-1",
        )

    user_input = response.get("text", "")
    if user_input:
        print(f'Usuário: {user_input}')
        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model=model_id,
            messages=messages,
        )

        assistant_response = response['choices'][0]['message']['content']
        print("Nesesi Ai:", assistant_response)
        messages.append({"role": "assistant", "content": assistant_response})
        return user_input, assistant_response  # Retorne o texto transcrito e a resposta da AI
    else:
        print("Não foi possível transcrever o áudio.")
        return None, None


