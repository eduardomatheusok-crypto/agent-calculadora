# Ponto de entrada: o único arquivo que conhece todas as peças.

# Responsabilidades: carregar a configuração, montar as peças,
# conversar com o usuário e mostrar os passos na tela.


import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from agente import criar_agente
from ferramentas import criar_ferramentas


def exibir_passo(mensagem: BaseMessage) -> None:
    """Imprime uma mensagem do agente no formato do ciclo ReAct."""
    if isinstance(mensagem, AIMessage):
        # .text junta os blocos de texto do Gemini 3.x numa string simples
        # e descarta metadados como a assinatura de pensamento.
        if mensagem.tool_calls:
            if mensagem.text:
                print(f"\nPensamento: {mensagem.text}")
            for chamada in mensagem.tool_calls:
                argumentos = ", ".join(f"{k}={v}" for k, v in chamada["args"].items())
                print(f"Ação: {chamada['name']}({argumentos})")
        else:
            print(f"\nResposta: {mensagem.text}")
    elif isinstance(mensagem, ToolMessage):
        print(f"Observação: {mensagem.text}")
    # A mensagem do usuário já aparece no cabeçalho "Pergunta:".


def perguntar(agente, pergunta: str) -> None:
    """Executa o agente e imprime cada passo do ciclo ReAct."""
    print(f"\n{'=' * 70}\nPergunta: {pergunta}\n{'=' * 70}")

    # stream_mode="values" devolve o estado a cada passo, permitindo ver
    # as chamadas de ferramenta (Ação) e os resultados (Observação).
    for passo in agente.stream(
        {"messages": [{"role": "user", "content": pergunta}]},
        stream_mode="values",
    ):
        exibir_passo(passo["messages"][-1])


def main() -> None:
    load_dotenv() 

    modelo = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        temperature=0,  # respostas determinísticas são melhores para cálculos
    )
    ferramentas = criar_ferramentas()
    agente = criar_agente(modelo, ferramentas)

    print("Digite uma conta (ou 'sair'):")
    while (entrada := input("> ").strip()).lower() not in {"sair", "exit", "q"}:
        if entrada:
            perguntar(agente, entrada)


if __name__ == "__main__":
    main()
