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
    print("✅ Découpage terminé.")
    print("parts : ", parts)
    return parts