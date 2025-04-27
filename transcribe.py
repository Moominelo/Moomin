import whisper
from pydub import AudioSegment

def split_audio(audio_path, split_times):
    """
    Découpe un fichier audio en plusieurs parties selon les temps de découpage spécifiés.
    """
    print(f"✂️ Découpage de l'audio aux temps suivants : {split_times} secondes...")
    audio = AudioSegment.from_wav(audio_path)
    parts = []
    start_time = 0

    for i, split_time in enumerate(split_times):
        part = audio[start_time * 1000:split_time * 1000]  # Découper en millisecondes
        part_path = f"part{i + 1}.wav"
        part.export(part_path, format="wav")
        parts.append(part_path)
        start_time = split_time

    # Ajouter la dernière partie (après le dernier point de découpage)
    part_path = f"part{len(split_times) + 1}.wav"
    part = audio[start_time * 1000:]  # De start_time à la fin
    part.export(part_path, format="wav")
    parts.append(part_path)

    print(f"✅ Audio découpé en {len(parts)} parties : {parts}")
    return parts

def transcribe_audio(audio_path, language, output_file):
    """
    Transcrit un fichier audio en texte avec des timestamps en utilisant Whisper.
    """
    print(f"📝 Transcription de l'audio : {audio_path} (Langue : {language})...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=language)

    # Sauvegarder la transcription dans un fichier
    with open(output_file, "w", encoding="utf-8") as file:
        for segment in result["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            file.write(f"[{start_time:.2f}s - {end_time:.2f}s] {text}\n")

    print(f"✅ Transcription sauvegardée dans : {output_file}")

if __name__ == "__main__":
    audio_path = "episode78_audio.wav"

    # Découper l'audio en trois parties : japonais, finnois, japonais
    split_times = [90, 1389]  # 1min30 (90s) et 23min09 (1389s)
    parts = split_audio(audio_path, split_times)

    # Transcrire chaque partie avec la langue appropriée
    languages = ["ja", "fi", "ja"]  # Japonais, finnois, japonais
    output_files = [
        "transcription_japanese_part1.txt",
        "transcription_finnish.txt",
        "transcription_japanese_part2.txt"
    ]

    for part, language, output_file in zip(parts, languages, output_files):
        transcribe_audio(part, language=language, output_file=output_file)
