from agno.agent import Agent
from agno.models.groq import Groq

from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Groq(id="openai/gpt-oss-safeguard-20b"),
    tools=[{"type": "browser_search"}],
    debug_mode=True
)
while True:
    agent.print_response(input("Digite sua pergunta: "))

    user_input = input("Digite sair para encerrar ou pressione Enter para continuar: ")
    if user_input.lower() == "sair":
        break