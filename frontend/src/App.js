// Importa o React e o hook useState (para lidar com estados no componente)
import React, { useState } from "react";

// Função principal que define o componente App (nosso frontend do chatbot)
function App() {
  // Estado que armazena a mensagem digitada pelo usuário
  const [message, setMessage] = useState("");

  // Estado que armazena a resposta recebida do backend
  const [reply, setReply] = useState("");

  // Função que envia a mensagem para o backend ao clicar no botão
  async function enviarMensagem() {
    try {
      // Faz uma requisição POST para a rota /chat do backend
      const res = await fetch("/chat", {
        method: "POST", // método HTTP
        headers: { "Content-Type": "application/json" }, // informa que o corpo é JSON
        body: JSON.stringify({ message }), // envia a mensagem do usuário no corpo da requisição
      });

      // Converte a resposta da API para JSON
      const data = await res.json();

      // Atualiza o estado com a resposta recebida
      setReply(data.reply);
    } catch (error) {
      // Em caso de erro na requisição, exibe no console e mostra mensagem no frontend
      console.error("Erro ao chamar API:", error);
      setReply("Erro ao obter resposta.");
    }
  }

  // JSX que renderiza a interface do chatbot na tela
  return (
    <div
      style={{
        maxWidth: 600,
        margin: "2rem auto",
        fontFamily: "sans-serif"
      }}
    >
      {/* Título do chatbot */}
      <h1>Chatbot OpenRouter</h1>

      {/* Campo de texto onde o usuário digita a pergunta */}
      <textarea
        rows={4} // número de linhas visíveis
        value={message} // valor vinculado ao estado message
        onChange={(e) => setMessage(e.target.value)} // atualiza o estado ao digitar
        placeholder="Digite sua mensagem aqui..."
        style={{
          width: "100%",
          padding: "0.5rem",
          fontSize: "1rem"
        }}
      />

      {/* Botão que chama a função para enviar a mensagem */}
      <button
        onClick={enviarMensagem}
        style={{
          marginTop: "1rem",
          padding: "0.5rem 1rem"
        }}
      >
        Enviar
      </button>

      {/* Se houver uma resposta, ela é exibida abaixo */}
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

// Exporta o componente App para ser usado pelo React
export default App;
