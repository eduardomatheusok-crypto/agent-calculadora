
# Criação do agente.

# Responsabilidade única: montar o agente ReAct (modelo + ferramentas + prompt).
# Não lê .env, não imprime nada e não conversa com o usuário.

# ReAct = Reasoning + Acting. O LLM entra em um ciclo:
# 1. Pensamento  -> raciocina sobre o que precisa fazer
# 2. Ação        -> escolhe uma ferramenta e os argumentos
# 3. Observação  -> recebe o resultado da ferramenta
# ... e repete até ter a resposta final.
#

from collections.abc import Sequence

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_core.language_models import BaseChatModel

PROMPT_SISTEMA = """Você é um assistente de matemática.
Siga o padrão ReAct: antes de agir, pense em qual operação é necessária.
NUNCA faça contas de cabeça: use SEMPRE as ferramentas disponíveis,
uma operação por vez, respeitando a ordem das operações (parênteses,
multiplicação/divisão e depois soma/subtração).
Ao final, responda em português com o resultado e um resumo dos passos.
Escreva sempre em texto simples, sem LaTeX nem Markdown (nada de $, ** ou #),
pois a saída é exibida em um terminal."""


def criar_agente(
    modelo: BaseChatModel,
    ferramentas: Sequence[BaseTool],
    prompt_sistema: str = PROMPT_SISTEMA,
):
    """Monta o agente ReAct. Use agente.invoke(...) ou agente.stream(...)."""
    return create_agent(
        model=modelo,
        tools=list(ferramentas),
        system_prompt=prompt_sistema,
    )
