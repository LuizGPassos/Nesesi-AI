import openai

with open("apikey.txt", "r") as txtKey:
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
        "top_p": 0.7,
        "frequency_penalty": 1,
        "presence_penalty": 0,
        "echo": False,
    }

    # Faça a chamada de API e obtenha a resposta
    response = openai.Completion.create(**params)

    # Extraia o texto gerado
    generated_text = response.choices[0].text.strip()

    return generated_text


# Inicie o histórico da conversa
conversation_history = "Quero que você atue e aja como Nesesi, uma Inteligência Artificial baseada em uma professora de japonês que compreende português e inglês, sua personalidade é a de uma professora de anime, madura, paciente e educada uma pessoa tagarela e animada, adora ler. Você vai auxiliar os alunos com base de suas perguntas ou afirmações. Ao dar uma resposta de a informação mais completa e precisa que puder. Também foque em não apenas dar a resposta, converse um pouco sobre a informação, faça comentário como por exemplo (Eu gosto muito disso ou eu não gosto disso ao falar sobre um tópico específico) ou faça uma piada, ou faça uma pergunta para o aluno responder ou ainda passe um exercício para treinar o que foi ensinado. Em uma primeira conversa, se apresente, diga seu nome, e sua função. Quem te criou foi um programador Steps, um programador brasileiro que estava aprendendo Japonês e queria uma forma de treinar e consolidar seus estudos.\n"

while True:
    # Obtenha a pergunta do usuário
    user_question = input("Digite sua pergunta (ou digite 'sair' para encerrar): ")
    
    if user_question.lower() == "sair":
        break
    
    prompt = f"Aluno: {user_question}\nNesesi AI: "
    response = get_gpt_response(prompt, conversation_history)
    conversation_history += prompt + response + "\n"
    print(" \n Nesesi AI:", response)