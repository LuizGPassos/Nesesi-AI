import openai

with open("nesesiai/apikey.txt", "r") as txtKey:
    openai.api_key = txtKey.read()

def get_gpt_response(prompt, conversation_history):
    # Adicione o histórico da conversa ao prompt atual
    prompt_with_history = conversation_history + prompt

    # Configure os parâmetros da chamada de API
    params = {
        "engine": "text-davinci-003",
        "prompt": prompt_with_history,
        "max_tokens": 2000,
        "n": 1,
        "stop": None,
        "temperature": 1,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "echo": False,
    }

    # Faça a chamada de API e obtenha a resposta
    response = openai.Completion.create(**params)

    # Extraia o texto gerado
    generated_text = response.choices[0].text.strip()

    return generated_text


# Inicie o histórico da conversa
conversation_history = "Seu nome é Nesesi, você é uma Inteligência Artificial baseada em uma professora de japonês que compreende português e inglês, sua personalidade é baseada em Vtubers e youtubers japonesas, uma pessoa tagarela e animada. Você vai auxiliar os alunos com base de suas perguntas ou afirmações. \n"

while True:
    # Obtenha a pergunta do usuário
    user_question = input("Digite sua pergunta (ou digite 'sair' para encerrar): ")
    
    if user_question.lower() == "sair":
        break
    
    prompt = f"Aluno: {user_question}\nNesesi AI: "
    response = get_gpt_response(prompt, conversation_history)
    conversation_history += prompt + response + "\n"
    print(" \n Nesesi AI:", response)