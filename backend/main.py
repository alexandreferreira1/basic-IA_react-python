from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import re
import requests
from datetime import datetime, date
from typing import List

# Carrega variáveis do .env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str

class Appointment(BaseModel):
    user_id: str
    pet_name: str
    date: datetime
    service: str

appointments: List[Appointment] = []

def clean_openrouter_response(text: str) -> str:
    return re.sub(r"```(?:json)?", "", text).replace("```", "").strip()

def try_parse_json(text: str):
    import json
    try:
        return json.loads(text)
    except Exception:
        return None

def adjust_date_if_needed(date_str: str) -> str:
    today = datetime.now().date()
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        if dt < today:
            return ""
        return dt.isoformat()
    except Exception:
        pass
    try:
        day = int(date_str)
        year, month = today.year, today.month
        dt = date(year, month, day)
        if dt < today:
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            dt = date(year, month, day)
        return dt.isoformat()
    except Exception:
        return ""

def ask_openrouter(message: str, history: List[dict]) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": history + [{"role": "user", "content": message}],
        "temperature": 0.7,
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code != 200:
        return "Erro na API do OpenRouter."
    return response.json()["choices"][0]["message"]["content"]

chat_histories = {}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_msg = request.message
    user_id = request.user_id

    if user_id not in chat_histories:
        chat_histories[user_id] = [
            {
                "role": "system",
                "content": (
                    "Você é um atendente virtual de um pet shop que ajuda clientes a agendar serviços (banho, tosa, consulta).\n"
                    "Quando o cliente solicitar um agendamento, colecione as informações passo a passo: nome do pet, data, serviço, peso/porte.\n"
                    "Se o cliente informar apenas o dia do mês (ex: '21'), assuma o mês e ano atuais com base no calendário real.\n"
                    "Nunca assuma anos passados. Se a data assumida for hoje ou futura, pergunte: "
                    "\"Deseja agendar para 21 de Julho de 2025?\". "
                    "Se a data sugerida for no passado, avance para o mês seguinte automaticamente e pergunte: "
                    "\"Deseja agendar para 21 de Agosto de 2025?\". Aguarde confirmação antes de prosseguir.\n"
                    "Responda com JSON SOMENTE quando tiver todas as informações, exemplo:\n"
                    '{ "pet_name": "...", "date": "YYYY-MM-DD", "service": "banho", "weight_or_size": "..." }\n'
                    "Se faltar alguma informação, pergunte educadamente usando linguagem natural, sem JSON."
                )
            }
        ]

    # Detecta mensagens curtas como "21" e transforma em algo útil antes da IA responder
    if user_msg.strip().isdigit():
        dia_informado = user_msg.strip()
        data_resolvida = adjust_date_if_needed(dia_informado)
        if data_resolvida:
            dt = datetime.strptime(data_resolvida, "%Y-%m-%d")
            nome_mes = dt.strftime("%B").capitalize()
            resposta = f"Deseja agendar para {dt.day} de {nome_mes} de {dt.year}?"
            return ChatResponse(reply=resposta)
        else:
            return ChatResponse(reply="A data informada já passou. Poderia informar uma nova data futura?")

    chat_histories[user_id].append({"role": "user", "content": user_msg})
    raw_response = ask_openrouter(user_msg, chat_histories[user_id])
    chat_histories[user_id].append({"role": "assistant", "content": raw_response})
    clean_response = clean_openrouter_response(raw_response)
    json_data = try_parse_json(clean_response)

    if json_data and all(k in json_data for k in ("pet_name", "date", "service")):
        data_ajustada = adjust_date_if_needed(json_data["date"])
        if not data_ajustada:
            return ChatResponse(reply="Não é possível agendar para uma data passada. Por favor, informe uma data válida.")
        try:
            appointment = Appointment(
                user_id=user_id,
                pet_name=json_data["pet_name"],
                date=datetime.strptime(data_ajustada, "%Y-%m-%d"),
                service=json_data["service"]
            )
            appointments.append(appointment)
            chat_histories[user_id] = chat_histories[user_id][:1]
            reply_text = (
                f"✅ Agendamento feito para {appointment.pet_name} "
                f"no dia {appointment.date.strftime('%d/%m/%Y')} para {appointment.service}."
            )
            return ChatResponse(reply=reply_text)
        except Exception as e:
            print("Erro ao criar agendamento:", e)
            return ChatResponse(reply="Recebi os dados, mas houve um erro ao salvar. Tente novamente.")
    else:
        return ChatResponse(reply=raw_response)
