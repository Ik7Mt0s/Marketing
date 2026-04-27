# Agentes de IA para Marketing

Um sistema inteligente para criação de conteúdo de marketing utilizando IA, capaz de analisar e imitar o estilo de criadores de conteúdo.

## 🎯 Sobre o Projeto

Este projeto utiliza agentes de IA para criar roteiros de Reels e conteúdo de marketing, inspirados no estilo de criadores específicos. O sistema analisa transcrições de vídeos para aprender o estilo de escrita de cada criador e utiliza essa informação para gerar novos roteiros no mesmo formato.

### 🚀 Funcionalidades Principais

- **Transcrição de Vídeos**: Converte áudio de vídeos em texto usando Whisper da Groq
- **Análise de Estilos**: Aprende e imita o estilo de diferentes criadores de conteúdo
- **Geração de Roteiros**: Cria roteiros de Reels no estilo do criador selecionado
- **Busca Inteligente**: Pesquisa informações na web para enriquecer o conteúdo
- **Interface Web**: Interface moderna para interação com os agentes

## 🛠️ Pré-requisitos

Antes de começar, certifique-se de ter:

1. **Python 3.12+** instalado
2. **uv** (gerenciador de pacotes Python)
3. **Node.js 18+** para a interface web
4. **Conta na Groq** (para usar o Whisper)
5. **Chave de API da Groq** (GROQ_API_KEY)
6. **Chave de API da Open Router** (OPENROUTER_API_KEY)
7. **Chave de API Tavily** (TAVILY_API_KEY)


## 📦 Instalação com uv

Siga estes passos para configurar o projeto corretamente:

### 1. Inicialize o projeto com uv

```bash
# Cria o ambiente virtual e instala as dependências
uv init

# Ativa o ambiente virtual
uv venv
```

### 2. Instale as dependências do Python

```bash
# Instala todas as dependências declaradas no pyproject.toml
uv pip install -e .
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_groq_aqui
OPENROUTER_API_KEY=sua_chave_openrouter_aqui
TAVILY_API_KEY=sua_chave_tavily_aqui
```

### 4. Instale dependências do frontend (agent-ui)

```bash
# Para clonar a interface do agente, execute o seguinte comando no seu terminal (conforme a documentação oficial do AgentUI do Agno):
npx create-agent-ui@latest

```

## 📁 Estrutura do Projeto

```
.
├── agent.py                 # Principal arquivo do agente
├── transcription_reader.py  # Módulo para ler transcrições
├── transcripter_debug.py   # Ferramenta de transcrição
├── videos/                  # Pasta para armazenar vídeos
│   ├── juliavargasf_/      # Pasta de cada criador
│   │   └── video1.mp4
│   └── leticiavaz/
│       └── video1.mp4
├── prompts/                 # Prompts para os agentes
│   └── copywriter.md
├── agent-ui/                # Interface web (Next.js)
├── transcriptions.json      # Banco de dados com transcrições
├── pyproject.toml          # Configuração do projeto
└── .env                    # Variáveis de ambiente
```

## 🎮 Como Usar

### 1. Transcrevídeos (Opcional)

Se você quiser adicionar seus próprios vídeos:

```bash
# Coloque vídeos na pasta videos/ organizados por criador
# Ex: videos/nome_do_criador/video.mp4

# Execute o transcriptor
python transcripter_debug.py
```

### 2. Execute o Agente

```bash
# Inicia o servidor do agente
python agent.py
```

### 3. Acesse a Interface Web

```bash
# Inicia a interface web (em outra janela terminal)
cd agent-ui
npm run dev
```

Abra [http://localhost:3000](http://localhost:3000) no seu navegador.

## 🤖 Como Funciona

1. **Pesquisa Web**: O agente pesquisa informações atualizadas sobre o tema
2. **Listar Criadores**: Mostra todos os criadores disponíveis no banco
3. **Aprender Estilo**: Analisa as transcrições do criador selecionado
4. **Gerar Hooks**: Cria frases de abertura no estilo do criador
5. **Criar Roteiro**: Gera o roteiro completo imitando o estilo

### Exemplo de Fluxo

1. Usário: "Quero um reels sobre produtividade"
2. Agente pesquisa fatos curiosos na web
3. Lista criadores disponíveis
4. Usário seleciona "juliavargasf_"
5. Agente analisa seu estilo e cria 10 hooks
6. Usário escolhe um hook
7. Agente gera o roteiro completo

## 🔧 Configuração Adicional

### FFmpeg (para extração de áudio)

Se você precisar transcrever vídeos:

1. Baixe o FFmpeg: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extraia para `C:\FFmpeg\` (ou configure o caminho em `transcripter_debug.py`)

### Agentes Disponíveis

O projeto usa dois modelos:
- **Groq**: `openai/gpt-oss-120b` (gratuito e rápido)
- **OpenRouter**: `deepseek/deepseek-v4-flash` (mais avançado)

## 📝 Criando Novos Criadores

Para adicionar um novo criador ao banco:

1. Coloque seus vídeos em `videos/nome_do_criador/`
2. Execute `python transcripter_debug.py`
3. As transcrições serão automaticamente adicionadas ao `transcriptions.json`

## 🚀 Desenvolvimento

### Executando em Desenvolvimento

```bash
# Terminal 1: Agente (com hot-reload)
uv run python agent.py

# Terminal 2: Interface web
cd agent-ui
npm run dev
```

### Atualizando Dependências

```bash
# Atualiza dependências Python
uv pip sync --upgrade

# Atualiza dependências Node.js
cd agent-ui
npm update
```

## 📊 Banco de Dados

As transcrições são armazenadas em `transcriptions.json` no formato:

```json
[
  {
    "video": "video1.mp4",
    "criador": "juliavargasf_",
    "transcricao": "texto da transcrição..."
  }
]
```

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `GROQ_API_KEY` | Chave API da Groq para Whisper | Sim |
| `TAVILY_API_KEY` | Chave API para pesquisa Tavily | Sim |
| `OPENROUTER_API_KEY` | Chave API da OpenRouter para modelos pagos | Não |


## 📄 Licença

[Adicionar licença do projeto]

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -am 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas:
- Verifique os prompts em `prompts/`
- Confira as dependências em `pyproject.toml`
- Teste o agente com `python agent.py`
- Confira na documentação oficial do [Agno](https://docs.agno.com/)