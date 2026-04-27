from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.groq import Groq
from agno.models.openrouter import OpenRouter

from agno.db.sqlite import SqliteDb

from transcription_reader import (list_creators,
    get_transcriptions,
    search_transcriptions,
    get_all_transcriptions,
)

from agno.os import AgentOS
"""
cd agent-ui
npm run dev
"""

from dotenv import load_dotenv
load_dotenv()

# IMPORTANTE: Criar ferramentas no formato que o Agno espera
from agno.tools import tool

@tool
def tool_list_creators():
    """Lista todos os criadores disponíveis com seus estilos."""
    return list_creators()

@tool
def tool_get_transcriptions(creator_name: str):
    """Pega as transcrições de um criador específico para aprender o estilo.
    
    Args:
        creator_name: Nome do criador (ex: 'juliavargasf_')
    """
    return get_transcriptions(creator_name)

@tool
def tool_search_transcriptions(keyword: str):
    """Busca uma palavra-chave em todas as transcrições.
    
    Args:
        keyword: Palavra ou frase para buscar
    """
    return search_transcriptions(keyword)

@tool
def tool_get_all_transcriptions():
    """Pega todas as transcrições de todos os criadores."""
    return get_all_transcriptions()

agentGroq = Agent(
    name="groqwriter",
    #model = Groq(id="llama-3.3-70b-versatile"),
    model = Groq(id="openai/gpt-oss-120b"),

    add_history_to_context=True,
    num_history_runs=10,
    db = SqliteDb(db_file="tmp/agent.db"),
    tools=[
        TavilyTools(),
        tool_list_creators,
        tool_get_transcriptions,
        tool_search_transcriptions,
        tool_get_all_transcriptions,
    ],
    instructions=open("prompts/copywriter.md", "r", encoding="utf-8").read()
)

agentOpenRouter = Agent(
    name="openrouterwriter",
    model = OpenRouter(id="deepseek/deepseek-v4-flash"),

    add_history_to_context=True,
    num_history_runs=10,
    db = SqliteDb(db_file="tmp/agent.db"),
    tools=[
        TavilyTools(),
        tool_list_creators,
        tool_get_transcriptions,
        tool_search_transcriptions,
        tool_get_all_transcriptions,
    ],
    instructions=open("prompts/copywriter.md", "r", encoding="utf-8").read()
)

agent_os = AgentOS(agents=[agentGroq, agentOpenRouter])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agent:app", reload=True)

