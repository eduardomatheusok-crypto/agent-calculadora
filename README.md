# Agente Calculadora

Um agente de IA que resolve contas usando **ferramentas** em vez de calcular "de cabeça".
Feito com **Python**, **LangChain** e **Google Gemini** para estudar como funcionam
os agentes e o padrão **ReAct**.

```
> Quanto é (10 + 5) * 3?

Pensamento: Primeiro preciso resolver o que está entre parênteses.
Ação: somar(a=10, b=5)
Observação: 15.0
Ação: multiplicar(a=15, b=3)
Observação: 45.0

Resposta: O resultado é 45. Primeiro somei 10 + 5 = 15 e depois multipliquei 15 por 3.
```

## O que é um agente?

Um agente é um LLM com um **inventário de ferramentas**: funções Python que ele pode
chamar quando precisa. O LLM não executa as contas. Ele decide **qual ferramenta usar
e com quais argumentos**, e o código Python faz o cálculo.

Ferramentas disponíveis:

| Ferramenta | Operação |
|---|---|
| `somar(a, b)` | a + b |
| `subtrair(a, b)` | a - b |
| `multiplicar(a, b)` | a * b |
| `dividir(a, b)` | a / b (devolve uma mensagem de erro se b = 0) |

## O padrão ReAct

ReAct vem de **Reasoning + Acting** (raciocinar e agir). O agente repete um ciclo
até ter a resposta:

1. **Pensamento:** decide qual operação precisa fazer.
2. **Ação:** chama uma ferramenta com os argumentos.
3. **Observação:** recebe o resultado da ferramenta.
4. Volta ao passo 1 ou, se já terminou, dá a **Resposta** final.

Quem executa esse ciclo é a função `create_agent` do LangChain. O programa mostra
cada passo no terminal para você acompanhar o raciocínio do agente.

### Como o LLM sabe quando usar cada ferramenta?

O LLM **não vê o código** das funções. Ele só recebe o **nome**, os **tipos dos
parâmetros** e a **docstring** de cada ferramenta:

```python
@tool
def somar(a: float, b: float) -> float:
    """
    Soma dois números.
    Use esta ferramenta para calcular adições aritméticas básicas.
    """
    return a + b
```

Por isso a docstring é o que "ensina" o agente. Uma descrição vaga leva o agente a
escolher a ferramenta errada.

## Estrutura do projeto

Cada arquivo tem uma única responsabilidade:

| Arquivo | Responsabilidade |
|---|---|
| `ferramentas.py` | Define as ferramentas (`@tool`) e as docstrings que o LLM lê |
| `agente.py` | Monta o agente com `create_agent` e define o prompt de sistema. Não imprime nada |
| `main.py` | Lê a configuração, cria o modelo Gemini, conversa com o usuário e mostra os passos |

```
main.py ──► criar_ferramentas()  (ferramentas.py)
        ──► criar_agente(modelo, ferramentas)  (agente.py)
        ──► loop: pergunta → agente.stream(...) → exibe Pensamento / Ação / Observação / Resposta
```

## Como rodar

**Requisitos:** Python 3.10+ e uma chave gratuita da API do Gemini
([Google AI Studio](https://aistudio.google.com/apikey)).

```bash
# 1. Clonar o projeto
git clone https://github.com/eduardomatheusok-crypto/agent-calculadora.git
cd agent-calculadora

# 2. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Configurar a chave
cp .env.example .env             # depois edite o .env e coloque a sua GOOGLE_API_KEY

# 5. Rodar
python main.py
```

Digite uma conta depois do `>` e aperte Enter. Para encerrar, digite `sair`.

### Configuração (`.env`)

| Variável | Obrigatória | Descrição |
|---|---|---|
| `GOOGLE_API_KEY` | Sim | Sua chave da API do Gemini |
| `GEMINI_MODEL` | Não | Modelo usado, por exemplo `gemini-3.8-flash` |

O `.env` está no `.gitignore`. **Nunca envie a sua chave para o GitHub.**

## Problemas comuns

| Erro | Causa e solução |
|---|---|
| `No module named 'dotenv'` | O ambiente virtual não está ativo. Rode `source .venv/bin/activate` |
| `API key required` | Falta o arquivo `.env` ou a `GOOGLE_API_KEY` dentro dele |
| `404 NOT_FOUND` | O modelo em `GEMINI_MODEL` não está disponível para a sua chave. Troque por outro |
| `503 UNAVAILABLE` ou o programa parece travado | Os servidores do Gemini estão sobrecarregados. Espere e tente de novo, ou troque de modelo |

## Próximos passos de estudo

- **Memória de conversa:** usar um `checkpointer` para o agente entender "multiplique isso por 2".
- **Descrição dos parâmetros:** docstrings com `Args:` e `@tool(parse_docstring=True)`.
- **Tratamento de erros:** `timeout`, `max_retries` e `try/except` para falhas da API.
- **Novas ferramentas:** potência, raiz quadrada, porcentagem.

## Tecnologias

- [LangChain](https://python.langchain.com/) (`create_agent`, `@tool`)
- [langchain-google-genai](https://pypi.org/project/langchain-google-genai/) (integração com o Gemini)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (leitura do `.env`)
