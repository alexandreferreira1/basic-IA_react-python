# Importa o FastAPI, que é o framework para criar a API backend
from fastapi import FastAPI

# Importa o BaseModel do Pydantic para validar os dados recebidos no corpo da requisição
from pydantic import BaseModel

# Importa a função para carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv

# Importa o módulo os para acessar variáveis de ambiente
import os

# Importa o requests, que é usado para fazer requisições HTTP externas (nesse caso, para a API do OpenRouter)
import requests


# Carrega as variáveis de ambiente do arquivo .env (como a chave da API)
load_dotenv()

# Cria a instância do FastAPI (nossa aplicação)
app = FastAPI()

# Obtém a chave da API do OpenRouter que está na variável de ambiente
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# Define o modelo de dados esperado na requisição: um JSON com campo "message"
class ChatRequest(BaseModel):
    message: str


# Cria a rota POST /chat que vai receber a mensagem do usuário e encaminhar para o OpenRouter
@app.post("/chat")
async def chat(request: ChatRequest):
    # Define os cabeçalhos da requisição, incluindo a chave de autenticação
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",  # autenticação da API
        "Content-Type": "application/json"                # tipo do corpo da requisição
    }

    # Monta o corpo da requisição para enviar ao OpenRouter (prompt do usuário)
    payload = {
        "model": "gpt-4o-mini",  # modelo de linguagem escolhido
        "messages": [
            {"role": "user", "content": request.message}  # mensagem enviada pelo usuário
        ]
    }

    # Faz a requisição POST para a API do OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    # Mostra no terminal a resposta bruta da OpenRouter (útil para debug)
    print("Resposta da OpenRouter:", response.text)

    # Se a resposta não for 200 OK, retorna um erro
    if response.status_code != 200:
        return {"error": "Erro na API OpenRouter", "detalhes": response.text}

    # Converte o JSON da resposta para dicionário Python
    data = response.json()

    # Extrai a resposta do modelo
    answer = data["choices"][0]["message"]["content"]

    # Retorna a resposta para o frontend
    return {"reply": answer}


# Rota básica GET / que só retorna uma mensagem para confirmar que o backend está funcionando
@app.get("/")
def read_root():
    return {"message": "Backend rodando com OpenRouter!"}
