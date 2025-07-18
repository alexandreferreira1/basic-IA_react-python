import React, { useState } from "react";

function App() {
  const [userId, setUserId] = useState("usuario123"); // Novo campo de identificação
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");

  async function enviarMensagem() {
    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message }) // envia user_id + mensagem
      });

      const data = await res.json();
      setReply(data.reply);
    } catch (error) {
      console.error("Erro ao chamar API:", error);
      setReply("Erro ao obter resposta.");
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Chatbot OpenRouter</h1>

      {/* Campo para definir o user_id */}
      <input
        type="text"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        placeholder="Seu ID de usuário"
        style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem", fontSize: "1rem" }}
      />

      <textarea
        rows={4}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Digite sua mensagem aqui..."
        style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
      />

      <button
        onClick={enviarMensagem}
        style={{ marginTop: "1rem", padding: "0.5rem 1rem" }}
      >
        Enviar
      </button>

      {reply && (
        <div
          style={{
            marginTop: "1rem",
            whiteSpace: "pre-wrap",
            backgroundColor: "#f0f0f0",
            padding: "1rem",
            borderRadius: 4
          }}
        >
          <strong>Resposta:</strong>
          <p>{reply}</p>
        </div>
      )}
    </div>
  );
}

export default App;
