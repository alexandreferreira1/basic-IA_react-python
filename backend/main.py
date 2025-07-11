from fastapi import FastAPI
# Importa a classe FastAPI, que é a base para criar a aplicação web/backend.

from fastapi.middleware.cors import CORSMiddleware
# Importa o middleware para CORS, que controla quais origens (frontends) podem acessar a API.

from pydantic import BaseModel
# Importa BaseModel do Pydantic, usado para definir modelos de dados com validação automática.

app = FastAPI()
# Cria uma instância da aplicação FastAPI, que vai gerenciar as rotas e requisições.

# Permite chamadas do React em localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite que somente esse endereço acesse a API.
    allow_methods=["*"],                       # Permite todos os métodos HTTP (GET, POST, etc).
    allow_headers=["*"],                       # Permite todos os cabeçalhos HTTP.
)

class Entrada(BaseModel):
    texto: str
# Define um modelo de dados chamado Entrada, que espera um JSON com a chave "texto" do tipo string.
# Esse modelo é usado para validar e tipar a entrada da requisição POST.

@app.get("/")
def home():
    return {"mensagem": "API Python funcionando!"}
# Define uma rota GET na raiz "/" que retorna um JSON com a mensagem de confirmação.

@app.post("/processar")
def processar_texto(dados: Entrada):
    return {"resultado": dados.texto.upper()}
# Define uma rota POST "/processar" que recebe um objeto JSON que corresponde ao modelo Entrada,
# pega o campo texto, transforma em maiúsculas e retorna no JSON de resposta com a chave "resultado".
