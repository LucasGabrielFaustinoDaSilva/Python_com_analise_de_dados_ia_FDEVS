from agno.agent import Agent
from agno.models.groq import Groq
import os
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()


db = SqliteDb(db_file="agno.db")


agent = Agent(
    name="comentarista_esportivo",
    user_id="user1",
    session_id="esportes",
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[{"type": "browser_search"}],
    db=db,
    update_memory_on_run=True,
    add_memories_to_context=True,
    add_history_to_context=True,
    num_history_runs=5
)


while True:
    pergunta = input("Digite sua pergunta sobre futebol: ")
    agent.print_response(pergunta)
    
    user_input = input("Digite 'sair' para encerrar ou pressione Enter para continuar: ")
    if user_input.lower() == "sair":
        break