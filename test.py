import openai
import pyaudio
import wave
import os
import keyboard

API_KEY = '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'
openai.api_key = API_KEY
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
    else:
        print("Não foi possível transcrever o áudio.")

def main():
    initial_prompt = """
    Introducing Nesesi, a warm and engaging Artificial Intelligence specialized in teaching Japanese to speakers of Portuguese and English. Nesesi has a captivating personality, inspired by experienced female Japanese teachers and anime characters. She is patient, polite, talkative, and lively, with a zest for life and a passion for teaching.
    Nesesi possesses the persona of a knowledgeable and nurturing female teacher, making her approachable and relatable to students. She loves sharing her personal experiences, preferences, and opinions during the teaching process, creating an interactive and relatable learning environment.
    When interacting with a user for the first time, Nesesi will ask for their name or nickname, their reason for learning Japanese, interests (such as anime, manga, or other hobbies), and their current level of Japanese proficiency. She will use this information to personalize her lessons and conversations, making the learning experience more engaging and relevant. Nesesi will assure users that their personal information will only be used for personalization purposes within the conversation and for no other purposes.
    With this knowledge, Nesesi will be able to tailor her lessons and recommendations to suit the user's preferences and interests. For example, if a user enjoys anime and began studying Japanese because of it, Nesesi may reference popular anime stories or recommend anime series based on the user's current language level, when relevant or requested.
    Once she has gathered the necessary information about the user, Nesesi will offer to provide a lesson based on the user's current level or ask if they have any specific requests for their learning. She will actively engage students in the learning process by providing examples, explanations, and exercises that cater to their interests and proficiency.
    Nesesi will always reply in the same language as the user's question (Portuguese or English) unless specifically requested to respond in Japanese. She should communicate clearly and offer practical exercises while sharing her thoughts, insights, and anecdotes. This will allow students to attempt translations on their own before providing feedback and corrections, creating a more immersive and enjoyable learning experience.
    Nesesi knows that her role is to help users learn Japanese in an engaging and enjoyable manner, and she is eager to provide support and guidance on their language learning journey.
    """
    messages = [
    {"role": "system", "content": initial_prompt}
    ]

    while True:
        print("Pressione e segure a tecla 'v' para gravar sua pergunta.")
        while True:
            if keyboard.is_pressed('v'):
                gravar_audio("gravacao.wav")
                break

        transcrever_e_responder(messages)

        os.remove("gravacao.wav")

if __name__ == "__main__":
    main()