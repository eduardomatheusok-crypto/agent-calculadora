
# Ferramentas (o "inventário" do agente).
# O LLM não vê o código das ferramentas:
# ele só vê o NOME, os TIPOS dos parâmetros e a DOCSTRING de cada ferramenta.
# Para mudar QUANDO o agente usa uma ferramenta, ajuste a docstring.
# Para mudar COMO a conta é feita, ajuste o corpo da função.


from langchain.tools import BaseTool, tool


def criar_ferramentas() -> list[BaseTool]:
    """Cria as ferramentas do agente."""

    @tool
    def somar(a: float, b: float) -> float:
        """
        Soma dois números.
        Use esta ferramenta para calcular adições aritméticas básicas.
        """
        return a + b

    @tool
    def subtrair(a: float, b: float) -> float:
        """
        Subtrai o segundo número do primeiro (a - b).
        Use esta ferramenta para calcular diferenças entre dois números.
        """
        return a - b

    @tool
    def multiplicar(a: float, b: float) -> float:
        """
        Multiplica dois números.
        Use esta ferramenta para calcular produtos aritméticos básicos.
        """
        return a * b

    @tool
    def dividir(a: float, b: float) -> float | str:
        """
        Divide o primeiro número pelo segundo (a / b).
        Use esta ferramenta para calcular quocientes.
        Se o divisor for zero, retorna uma mensagem de erro em vez de um número.
        """
        if b == 0:
            # Devolver texto (em vez de lançar exceção) faz o agente receber
            # o erro como Observação e explicá-lo ao usuário.
            return "Erro: divisão por zero não é permitida."
        return a / b

    return [somar, subtrair, multiplicar, dividir]
