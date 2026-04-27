"""
transcription_reader.py - Ferramenta para ler transcrições do arquivo JSON
Uso: Chamado pelo agent.py para acessar transcrições de criadores
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


def load_transcriptions() -> Optional[List[Dict]]:
    """Carrega o arquivo transcriptions.json"""
    try:
        with open('transcriptions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def list_creators() -> str:
    """
    Retorna lista de criadores disponíveis.
    
    Returns:
        str: Lista formatada dos criadores
    """
    data = load_transcriptions()
    
    if not data:
        return "Nenhum criador encontrado. Execute transcripter.py primeiro."
    
    creators = {}
    for item in data:
        creator = item.get('criador')
        if creator:
            creators[creator] = creators.get(creator, 0) + 1
    
    if not creators:
        return "Nenhum criador encontrado."
    
    result = f"📁 Criadores disponíveis ({len(creators)}):\n"
    for creator, count in sorted(creators.items()):
        result += f"  - {creator} ({count} vídeo(s))\n"
    
    return result


def get_transcriptions(creator_name: str) -> str:
    """
    Retorna todas as transcrições de um criador específico.
    
    Args:
        creator_name: Nome do criador (ex: 'juliavargasf_')
    
    Returns:
        str: Transcrições formatadas para o agente
    """
    data = load_transcriptions()
    
    if not data:
        return "ERRO: Arquivo transcriptions.json não encontrado."
    
    # Filtrar por criador
    items = [item for item in data if item.get('criador') == creator_name]
    
    if not items:
        available = list(set(item.get('criador') for item in data if item.get('criador')))
        return f"ERRO: Criador '{creator_name}' não encontrado. Disponíveis: {', '.join(available)}"
    
    # Formatar transcrições
    result = f"# Transcrições de {creator_name}\n\n"
    
    for i, item in enumerate(items, 1):
        video = item.get('video', 'desconhecido')
        transcricao = item.get('transcricao', '')
        
        if transcricao:
            result += f"## Vídeo {i}: {video}\n\n{transcricao}\n\n"
            result += "---\n\n"
        else:
            erro = item.get('erro', 'Erro desconhecido')
            result += f"## Vídeo {i}: {video}\n\n❌ Falha na transcrição: {erro}\n\n---\n\n"
    
    return result


def get_all_transcriptions() -> str:
    """
    Retorna todas as transcrições de todos os criadores.
    
    Returns:
        str: Todas as transcrições formatadas
    """
    data = load_transcriptions()
    
    if not data:
        return "ERRO: Arquivo transcriptions.json não encontrado."
    
    result = "# Todas as Transcrições\n\n"
    
    # Agrupar por criador
    by_creator = {}
    for item in data:
        creator = item.get('criador', 'desconhecido')
        if creator not in by_creator:
            by_creator[creator] = []
        by_creator[creator].append(item)
    
    for creator, items in sorted(by_creator.items()):
        result += f"## 👤 {creator}\n\n"
        
        for i, item in enumerate(items, 1):
            video = item.get('video', 'desconhecido')
            transcricao = item.get('transcricao', '')
            
            if transcricao:
                result += f"### Vídeo {i}: {video}\n\n{transcricao}\n\n"
            else:
                erro = item.get('erro', 'Erro desconhecido')
                result += f"### Vídeo {i}: {video}\n❌ {erro}\n\n"
        
        result += "---\n\n"
    
    return result


def search_transcriptions(keyword: str) -> str:
    """
    Busca palavra-chave em todas as transcrições.
    
    Args:
        keyword: Palavra ou frase para buscar
    
    Returns:
        str: Resultados da busca
    """
    data = load_transcriptions()
    
    if not data:
        return "ERRO: Arquivo transcriptions.json não encontrado."
    
    results = []
    
    for item in data:
        transcricao = item.get('transcricao', '')
        if not transcricao:
            continue
        
        if keyword.lower() in transcricao.lower():
            creator = item.get('criador', 'desconhecido')
            video = item.get('video', 'desconhecido')
            
            # Pegar contexto (100 caracteres ao redor)
            idx = transcricao.lower().find(keyword.lower())
            start = max(0, idx - 50)
            end = min(len(transcricao), idx + 100)
            context = transcricao[start:end]
            
            if start > 0:
                context = "..." + context
            if end < len(transcricao):
                context = context + "..."
            
            results.append(f"**{creator}** - {video}\n> {context}\n")
    
    if not results:
        return f"🔍 Nenhum resultado encontrado para '{keyword}'."
    
    return f"🔍 Resultados para '{keyword}':\n\n" + "\n".join(results)


def get_creator_videos_count(creator_name: str) -> int:
    """
    Retorna quantos vídeos um criador possui.
    
    Args:
        creator_name: Nome do criador
    
    Returns:
        int: Número de vídeos
    """
    data = load_transcriptions()
    
    if not data:
        return 0
    
    return sum(1 for item in data if item.get('criador') == creator_name and item.get('transcricao'))


def get_creators_dict() -> Dict[str, List[str]]:
    """
    Retorna dicionário com criadores e suas transcrições.
    Útil para o agente processar programaticamente.
    
    Returns:
        dict: {criador: [transcricao1, transcricao2, ...]}
    """
    data = load_transcriptions()
    
    if not data:
        return {}
    
    result = {}
    for item in data:
        creator = item.get('criador')
        transcricao = item.get('transcricao')
        
        if creator and transcricao:
            if creator not in result:
                result[creator] = []
            result[creator].append(transcricao)
    
    return result


# ====================================================================
# Interface para o Agente (funções simples)
# ====================================================================

def get_creator_style(creator_name: str) -> str:
    """
    Retorna o estilo do criador baseado nas transcrições.
    Esta função é chamada pelo agente para aprender o estilo.
    
    Args:
        creator_name: Nome do criador
    
    Returns:
        str: Análise do estilo ou transcrições brutas
    """
    transcriptions = get_transcriptions(creator_name)
    
    if transcriptions.startswith("ERRO"):
        return transcriptions
    
    return transcriptions


if __name__ == "__main__":
    # Teste rápido (apenas para debug)
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "listar":
            print(list_creators())
        elif command == "criador" and len(sys.argv) > 2:
            print(get_transcriptions(sys.argv[2]))
        elif command == "buscar" and len(sys.argv) > 2:
            print(search_transcriptions(sys.argv[2]))
        elif command == "tudo":
            print(get_all_transcriptions())
        else:
            print("Comandos: listar | criador <nome> | buscar <palavra> | tudo")
    else:
        # Modo simples para teste
        print(list_creators())