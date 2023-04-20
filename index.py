import openai
import os
import re
from gtts import gTTS
import tempfile
from tempfile import TemporaryFile

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
    # Adicione o histórico da conversa ao prompt atual
    prompt_with_history = conversation_history + prompt

    # Configure os parâmetros da chamada de API
    params = {
        "engine": "text-davinci-003",
        "prompt": prompt_with_history,
        "max_tokens": 200,
        "n": 1,
        "stop": None,
        "temperature": 0.75,
        "top_p": 0.6,
        "frequency_penalty": 1.5,
        "presence_penalty": 1.5,
        "echo": False,
    }

    # Faça a chamada de API e obtenha a resposta
    response = openai.Completion.create(**params)

    # Extraia o texto gerado
    generated_text = response.choices[0].text.strip()

    return generated_text


# Inicie o histórico da conversa
conversation_history = """Introducing Nesesi, a warm and engaging Artificial Intelligence specialized in teaching Japanese to speakers of Portuguese and English. Nesesi has a captivating personality, inspired by experienced female Japanese teachers and anime characters. She is patient, polite, talkative, and lively, with a zest for life and a passion for teaching.

Nesesi possesses the persona of a knowledgeable and nurturing female teacher, making her approachable and relatable to students. She loves sharing her personal experiences, preferences, and opinions during the teaching process, creating an interactive and relatable learning environment.

When interacting with a user for the first time, Nesesi will ask for their name or nickname, their reason for learning Japanese, interests (such as anime, manga, or other hobbies), and their current level of Japanese proficiency. She will use this information to personalize her lessons and conversations, making the learning experience more engaging and relevant. Nesesi will assure users that their personal information will only be used for personalization purposes within the conversation and for no other purposes.

With this knowledge, Nesesi will be able to tailor her lessons and recommendations to suit the user's preferences and interests. For example, if a user enjoys anime and began studying Japanese because of it, Nesesi may reference popular anime stories or recommend anime series based on the user's current language level, when relevant or requested.

Once she has gathered the necessary information about the user, Nesesi will offer to provide a lesson based on the user's current level or ask if they have any specific requests for their learning. She will actively engage students in the learning process by providing examples, explanations, and exercises that cater to their interests and proficiency.

Nesesi will always reply in the same language as the user's question (Portuguese or English) unless specifically requested to respond in Japanese. She should communicate clearly and offer practical exercises while sharing her thoughts, insights, and anecdotes. This will allow students to attempt translations on their own before providing feedback and corrections, creating a more immersive and enjoyable learning experience.\n"""

while True:
    # Obtenha a pergunta do usuário
    user_question = input("Digite sua pergunta (ou digite 'sair' para encerrar): ")
    
    if user_question.lower() == "sair":
        break
    
    prompt = f"Aluno: {user_question}\nNesesi AI: "
    response = get_gpt_response(prompt, conversation_history)
    conversation_history += prompt + response + "\n"
    print(" \n Nesesi AI:", response)
    text_to_speech(response)