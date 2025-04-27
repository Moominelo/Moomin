import subprocess

def extract_audio(video_path, audio_path="output_audio.wav"):
    """
    Extrait l'audio d'une vidéo au format MKV et le convertit en WAV en utilisant ffmpeg.
    """
    if not video_path.endswith(".mkv"):
        raise ValueError("Le fichier fourni doit être au format MKV.")
    
    # Commande ffmpeg pour extraire l'audio
    command = [
        "ffmpeg", "-i", video_path, "-vn",  # -vn pour ignorer la vidéo
        "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2",  # Format WAV
        audio_path
    ]
    print(f"🎞️ Conversion de {video_path} en {audio_path}...")
    
    try:
        subprocess.run(command, check=True)
        print(f"✅ Audio extrait avec succès : {audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'extraction audio : {e}")
        raise

if __name__ == "__main__":
    video_path = r"C:\Users\rdgza\OneDrive\Bureau\saison 1\episode78.mkv"
    audio_path = "episode78_audio.wav"
    
    # Extraire l'audio
    extract_audio(video_path, audio_path)

