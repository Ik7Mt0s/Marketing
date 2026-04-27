import os
import subprocess
import json
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Configurações
CAMINHO_FFMPEG = r"C:\FFmpeg\bin\ffmpeg.exe"
VIDEOS_DIR = Path("videos")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_audio(video_path, audio_path):
    """Extrai áudio do vídeo em MP3"""
    subprocess.run([
        CAMINHO_FFMPEG, "-i", str(video_path),
        "-q:a", "0", "-map", "a", "-y", str(audio_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def transcribe_audio(audio_path):
    """Transcreve áudio usando Whisper da Groq"""
    with open(audio_path, "rb") as f:
        return client.audio.transcriptions.create(
            file=(audio_path.name, f.read()),
            model="whisper-large-v3-turbo",
            response_format="text"
        )

def main():
    # Encontrar todos os vídeos
    videos = list(VIDEOS_DIR.rglob("*.mp4"))
    
    if not videos:
        print("❌ Nenhum vídeo encontrado na pasta 'videos'")
        return
    
    print(f"🎬 Encontrados {len(videos)} vídeo(s)")
    print("-" * 50)
    
    resultados = []
    
    for i, video_path in enumerate(videos, 1):
        creator = video_path.parent.name
        audio_path = video_path.parent / f"{video_path.stem}.mp3"
        
        print(f"\n[{i}/{len(videos)}] Processando: {video_path.name}")
        print(f"   👤 Criador: {creator}")
        
        try:
            # 1. Extrair áudio
            print(f"   🔊 Extraindo áudio... ", end="", flush=True)
            extract_audio(video_path, audio_path)
            print(f"✅")
            
            # 2. Transcrever
            print(f"   📝 Transcrevendo... ", end="", flush=True)
            transcricao = transcribe_audio(audio_path)
            print(f"✅")
            
            # 3. Salvar resultado
            resultados.append({
                "video": video_path.name,
                "caminho": str(video_path),
                "criador": creator,
                "transcricao": transcricao
            })
            
            # Mostrar preview
            preview = transcricao[:80] + "..." if len(transcricao) > 80 else transcricao
            print(f"   📄 Preview: \"{preview}\"")
            
            # 4. Limpar arquivo de áudio (opcional)
            audio_path.unlink()
            print(f"   🧹 Áudio temporário removido")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            resultados.append({
                "video": video_path.name,
                "caminho": str(video_path),
                "criador": creator,
                "transcricao": None,
                "erro": str(e)
            })
    
    # Salvar tudo em JSON
    output_path = Path("transcriptions.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 50)
    print(f"✅ Processamento concluído!")
    print(f"📊 Total de vídeos: {len(resultados)}")
    print(f"📁 Arquivo salvo: {output_path.absolute()}")
    
    # Estatísticas
    sucessos = sum(1 for r in resultados if r.get("transcricao"))
    erros = len(resultados) - sucessos
    print(f"✅ Transcritos com sucesso: {sucessos}")
    print(f"❌ Falhas: {erros}")

if __name__ == "__main__":
    main()