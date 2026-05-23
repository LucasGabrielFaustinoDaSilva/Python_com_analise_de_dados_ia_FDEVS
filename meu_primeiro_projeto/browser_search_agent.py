from agno.agent import Agent
from agno.models.groq import Groq
import os
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()


db = SqliteDb(db_file="agno.db")


agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[{"type": "browser_search"}],
    db=db,
    update_memory_on_run=True,
    add_memories_to_context=True
)


while True:
    pergunta = input("Digite sua pergunta: ")
    agent.print_response(pergunta)
    
    user_input = input("Digite 'sair' para encerrar ou pressione Enter para continuar: ")
    if user_input.lower() == "sair":
        break