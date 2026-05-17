from agno.agent import Agent, RunOutput
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.decorator import tool
from pydantic import BaseModel, Field
from typing import List

from dotenv import load_dotenv
load_dotenv()

class CotacaoSchema(BaseModel):
    empresa: str = Field(description="Nome da empresa")
    cotacao_usd: float = Field(description="Cotacao da empresa em dolares(USD)")
    cotacao_brl: float = Field(description="Cotacao da empresa em reais(BRL)")
    
class RespostaFinal(BaseModel):
    cotacao_dolar: float = Field(description="cotacao dolar (BRL por USD)")
    cotacoes: List[CotacaoSchema]
    
@tool(name="Converte_para_brl", description="converte um valor em USD para BRL usando a cotacao atual do dolar")
def converte_para_brl(valor_usd: float) -> str:
    """Converte um valor em dolares americanos(USD) para reais brasileiros(BRL).
  Args:
    valor_usd(float): O valor em USD a ser convertido
  Returns:
    str: O valor convertido em BRL formatado como moeda brasileira."""
    import yfinance as yf
    ticker = yf.Ticker("USDBRL=X")
    cotacao = ticker.fast_info["last_price"]
    valor_brl = valor_usd * cotacao
    return f"Usd {valor_usd:.2f} = BRL {valor_brl:.2f}(cotacao do dolar: R$ {cotacao:.4f})"

# Criando o agente principal 
agent_coletor = Agent(
    model=Groq(id="openai/gpt-oss-120b"),  # Adicionando o modelo
    tools=[YFinanceTools(enable_stock_price=True), converte_para_brl],  # Adicionando as ferramentas
    instructions=[
        "Voce é um agente financeiro especializado em coletar cotações de ações",
        "Use as ferramentas disponíveis para buscar informações financeiras atualizadas",
        "Forneça os valores em USD e também converta para BRL usando a ferramenta de conversão"
    ]
)

agent_formatador = Agent(
    model=Groq(id="openai/gpt-oss-120b"),  # Adicionando o modelo
    instructions=[
        "Voce é um agente de formatacao de dados financeiros",
        "Recebera uma lista de empresas com cotacoes em USD e BRL",
        "Estruture os dados exatamente no sistema solicitado, sem alterar os valores",
    ],
    output_schema=RespostaFinal,
)


# Executando o agente
coleta: RunOutput = agent_coletor.run("Informe a cotacao atual das 5 principais empresas de tecnologia")
formatado: RunOutput = agent_formatador.run(coleta.content)


print(formatado.content.model_dump_json(indent=2))
print("___" * 3, "Metricas - Agente Coletor", "___" * 3)
print(coleta.metrics)
print("___" * 3, "Metricas - Agente Formatador", "___" * 3)
print(formatado.metrics)