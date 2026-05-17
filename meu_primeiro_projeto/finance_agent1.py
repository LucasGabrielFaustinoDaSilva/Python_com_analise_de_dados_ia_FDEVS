from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools

from datetime import datetime

from dotenv import load_dotenv

from agno.utils.pprint import pprint_run_response
from rich.pretty import pprint

from agno.tools.decorator import tool
from agno.agent import Agent, RunOutput



load_dotenv()

@tool(name="converte_para_brl", description="Converte um valor em USD para BRL usando a cotaçao atual do dolar")
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
    

agent = Agent(
  model=Groq(id="openai/gpt-oss-120b"),
  tools=[YFinanceTools(enable_stock_price=True), converte_para_brl],
  
  instructions=[
    "Voce é um agente financeiro especializado em fornecer informaçoes sobre o mercado de acoes e cotaçoes de empresas",
    "Use as ferramentas disponiveis para obter as cotaçoes das empresas e conversao de moedas.",
    "Retorne uma lista contendo somente a empresa, codigo na bolsa de valores, cotacao atual em USD e conversao para BRL",
    "Informe a cotaçao de dolar e mais nenhuma informaçao adicional"
  ],
  markdown=True,
)
run_output: RunOutput = agent.run("Informe a cotaçao atual das 5 principais empresas de tecnologia do mundo")

pprint_run_response(run_output)
print("___" * 3,"Collected Metrica","___"*3)
pprint_run_response(run_output.metrics)

