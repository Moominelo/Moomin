from extraction_audio import select_video_file,extract_audio # Remplacez 'some_function' par le nom de la fonction que vous voulez importer
from transcribe import split_audio
from romanisation import romanize_file
from generate_srt import write_srt, read_file, parse_line_with_timestamps
import whisper
from deep_translator import GoogleTranslator

def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

if __name__ == "__main__":

    """
    Etape 1 : Extraction de l'audio
    Demande à l'utilisateur de sélectionner un fichier vidéo et extrait l'audio au format WAV.
    """
    # Demander à l'utilisateur de sélectionner un fichier vidéo
    print("📹 Sélectionnez un fichier vidéo (format MKV) pour extraire l'audio...")
    video_path = select_video_file()
    if not video_path:
        print("❌ Aucun fichier sélectionné. Opération annulée.")
    else:
        audio_path = "output_audio.wav"
        # Extraire l'audio
        extract_audio(video_path, audio_path)

        print(f"Audio extrait avec succès dans {audio_path}.")

    """
    Etape 2 : Récupération de ce que souhaite l'utilisateur
    Demande à l'utilisateur s'il souhaite découper l'audio et récupère les timestamps si nécessaire.

    """
    print("🎥 Lancement de l'application Tkinter pour les options de transcription...")

    # Appeler la fenêtre principale Tkinter et récupérer les résultats
    split_choice, timestamps, selected_languages = True, [input("Début en min:sec = "), input("Fin en min:sec = ")], ["ja", "fi","ja"]  

    timestamps = [time_to_seconds(t) for t in timestamps]

    print(f"Découpage audio : {split_choice}")
    print(f"Timestamps : {timestamps}")
    print(f"Langues sélectionnées : {selected_languages}")

    """
    Etape 3 : Découpage de l'audio
    """

    if split_choice:
        # Découper l'audio selon les timestamps fournis
        audio_parts = split_audio(audio_path, timestamps)

    """
    Etape 4 : Chargement model Whisper
    """
    print("Chargement du modèle Whisper...")
    model = whisper.load_model("medium")  # Charger le modèle Whisper
    print("Modèle Whisper chargé.")

    """
    Etape 5 : Transcription de chaque partie audio
    """

    for i, audio_part in enumerate(audio_parts):

        print(f"📝 Transcription de la partie {i + 1} en cours...")
        result = model.transcribe(audio_part, language=selected_languages[i])
        print(f"Transcription de la partie {i + 1} terminée.")
        # Sauvegarder la transcription dans un fichier
        with open(f"transcription_part_{i+1}.txt", "w", encoding="utf-8") as file:
            for segment in result["segments"]:
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"]
                file.write(f"[{start_time:.2f}s - {end_time:.2f}s] {text}\n")

        print(f"✅ Transcription sauvegardée dans : {f'transcription_part_{i+1}.txt'}")

    """
    Etape 6 : Romanisation des fichiers de transcription et traduction en anglais
    """
    print("Romanisation et traduction des fichiers de transcription...")
    for i in range(len(audio_parts)):
        if selected_languages[i] == "ja":
            # Romaniser uniquement si la langue est le japonais
            print(f"📜 Romanisation de la partie {i + 1}...")
            input_file = f"transcription_part_{i + 1}.txt"
            output_file = f"end_transcription_part_{i + 1}.txt"
            romanize_file(input_file, output_file)
            print(f"✅ Romanisation terminée pour : {input_file} -> {output_file}")
    
        elif selected_languages[i] == "fi":
            print(f"🌍 Traduction de la partie {i + 1} du finnois vers l'anglais...")
            input_file = f"transcription_part_{i + 1}.txt"
            output_file = f"end_transcription_part_{i + 1}.txt"
            with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
                for line in infile:
                    translated_line = GoogleTranslator(source="fi", target="en").translate(line.strip())
                    outfile.write(translated_line + "\n")
            print(f"✅ Traduction terminée pour : {input_file} -> {output_file}")
    """
    Etape 7 : Décalage des timestamps et génération du fichier SRT
    """
    offsets = [0, timestamps[0], timestamps[1]]  # En secondes

    files = [f"end_transcription_part_{i + 1}.txt" for i in range(len(audio_parts))]
    srt_lines = []
    output_srt = video_path.replace(".mkv", ".srt")
    index = 1

    for file_path, time_offset in zip(files, offsets):
        print(f"📄 Traitement du fichier : {file_path} avec un décalage de {time_offset}s...")
        lines = read_file(file_path)
        for line in lines:
            start_time_str, end_time_str, text = parse_line_with_timestamps(line, time_offset=time_offset)
            if start_time_str and end_time_str and text:
                srt_lines.append(f"{index}\n")
                srt_lines.append(f"{start_time_str} --> {end_time_str}\n")
                srt_lines.append(f"{text}\n\n")
                index += 1

    # Write to output file
    write_srt(output_srt, srt_lines)
    print(f"✅ Fichier SRT généré : {output_srt}")
