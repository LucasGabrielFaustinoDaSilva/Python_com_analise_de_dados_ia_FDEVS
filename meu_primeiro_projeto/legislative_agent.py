from agno.agent import Agent
from agno.models.groq import Groq
import os
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.models.openai import OpenAIChat
from agno.embedders.openai import OpenAIEmbedder
from agno.vectordb.chroma import ChromaDb


load_dotenv()


db = SqliteDb(db_file="agno.db")

vector_db = ChromaDb(
    collection="quadro_geral_dados_municipais",
    path="vector_db/Chromadb",
    embedder=OpenAIEmbedder(
        id="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    ),
    persistent_client=True,
)

agent = Agent(
    name="comentarista_esportivo",
    user_id="user1",
    session_id="esportes",
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[{"type": "browser_search"}],
    db=db,
    vector_db=vector_db,
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