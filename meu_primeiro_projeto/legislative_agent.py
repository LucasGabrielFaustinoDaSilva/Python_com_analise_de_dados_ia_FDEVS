from agno.agent import Agent
import os
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.models.openai import OpenAIChat
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.knowledge import Knowledge


load_dotenv()


db = SqliteDb(db_file="agno.db")

db_vetor = ChromaDb(
    collection="quadro_geral_dados_municipais",
    path="vector_db/Chromadb",
    embedder=OpenAIEmbedder(
        id="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    ),
    persistent_client=True,
)
knowledge = Knowledge(vector_db=db_vetor) 
#Leitor de PDFs

pdf_reader = PDFReader(
    chunking_strategy=RecursiveChunking(
        chunk_size=2000,
        overlap=200,
    ),
)
knowledge.insert(path="docs/", reader=pdf_reader)

agent = Agent(
    name="analista_legislativo",
    user_id="user1",
    session_id="politica_local",
    model=OpenAIChat(
        id="gpt-5-nano",
        api_key=os.getenv("OPENAI_API_KEY")),
    db=db,
    instructions=[
        "Voce é um analista legislativo especializado em  analisar atas de reunioes de camaras municipais. Seu objetivo é extrair informaçoes relevantes"
        
        "Utilize a base de conhecimento contruida a partir das atas para responder as perguntas de forma precisa e consisa"
    ],
    enable_agentic_memory=True,
    add_memories_to_context=True,
    debug_mode=True,
    
    #RAG
    knowledge=knowledge,
    search_knowledge=True
    
)


while True:
    pergunta = input("Digite sua pergunta sobre o pdf : ")
    agent.print_response(pergunta)
    
    user_input = input("Digite 'sair' para encerrar ou pressione Enter para continuar: ")
    if user_input.lower() == "sair":
        break