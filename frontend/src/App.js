import React, { useState } from "react";
// Importa React e o hook useState para gerenciar estado dentro do componente.

function App() {
  // Define o componente funcional principal da aplicação.

  const [entrada, setEntrada] = useState("");
  // Cria um estado chamado "entrada" para armazenar o texto digitado no input, inicialmente vazio.
  // "setEntrada" é a função para atualizar esse estado.

  const [resultado, setResultado] = useState("");
  // Cria um estado chamado "resultado" para armazenar o resultado recebido da API, inicialmente vazio.
  // "setResultado" é a função para atualizar esse estado.

  const enviarTexto = async () => {
    // Função assíncrona que será chamada ao clicar no botão para enviar o texto para o backend.

    try {
      const res = await fetch("/processar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto: entrada }),
      });
      // Envia uma requisição POST para a rota "/processar" com um JSON que contém o texto digitado.
      // "fetch" retorna uma promessa que aguardamos com await.

      const data = await res.json();
      // Espera a resposta da API, converte o corpo para JSON e armazena em "data".

      setResultado(data.resultado);
      // Atualiza o estado "resultado" com o valor retornado da API.
    } catch (err) {
      console.error("Erro na API:", err);
      // Caso ocorra erro na requisição, imprime o erro no console.
    }
  };

  return (
    // JSX que define a interface visual do componente.

    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      {/* Container centralizado com largura máxima de 600px e fonte sans-serif */}

      <h1>React + FastAPI</h1>
      {/* Título da aplicação */}

      <input
        type="text"
        value={entrada}
        onChange={(e) => setEntrada(e.target.value)}
        placeholder="Digite algo"
        style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
      />
      {/* Campo de texto controlado: valor ligado ao estado "entrada".
          Quando o usuário digita, "onChange" atualiza o estado com o novo valor. */}

      <button
        onClick={enviarTexto}
        style={{ marginTop: "1rem", padding: "0.5rem 1rem", fontSize: "1rem" }}
      >
        Enviar
      </button>
      {/* Botão que chama a função enviarTexto ao ser clicado */}

      {resultado && (
        <p style={{ marginTop: "1rem", fontSize: "1.25rem" }}>
          Resultado: <strong>{resultado}</strong>
        </p>
      )}
      {/* Se "resultado" não for vazio, mostra um parágrafo com o texto retornado da API em negrito */}
    </div>
  );
}

export default App;
// Exporta o componente para que ele possa ser usado na aplicação.
