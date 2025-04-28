import whisper
from pydub import AudioSegment
import tkinter as tk
from tkinter import ttk
from romanisation import romanize_file  # Importer la fonction de romanisation

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
    model = whisper.load_model("small")  # Charger le modèle Whisper
    result = model.transcribe(audio_path, language=language)

    # Sauvegarder la transcription dans un fichier
    with open(output_file, "w", encoding="utf-8") as file:
        for segment in result["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            file.write(f"[{start_time:.2f}s - {end_time:.2f}s] {text}\n")

    print(f"✅ Transcription sauvegardée dans : {output_file}")

def get_user_choice_and_timestamps():
    """
    Interface graphique pour demander si l'utilisateur souhaite découper l'audio
    et récupérer les timestamps si nécessaire.
    """
    def convert_to_seconds(minutes, seconds):
        """Convertit les minutes et secondes en secondes totales."""
        return int(minutes) * 60 + int(seconds)

    def submit():
        nonlocal split_choice, timestamps
        split_choice = split_var.get()
        if split_choice:
            try:
                start_minutes = int(start_min_entry.get())
                start_seconds = int(start_sec_entry.get())
                end_minutes = int(end_min_entry.get())
                end_seconds = int(end_sec_entry.get())

                start_time = convert_to_seconds(start_minutes, start_seconds)
                end_time = convert_to_seconds(end_minutes, end_seconds)

                if start_time >= end_time:
                    error_label.config(text="Erreur : Le début doit être inférieur à la fin.")
                else:
                    timestamps = [start_time, end_time]
                    root.destroy()
            except ValueError:
                error_label.config(text="Erreur : Veuillez entrer des valeurs valides.")
        else:
            root.destroy()

    split_choice = False
    timestamps = []

    root = tk.Tk()
    root.title("Découper l'audio ?")

    # Question : Découper l'audio ?
    tk.Label(root, text="Souhaitez-vous découper l'audio ?").pack(pady=10)
    split_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(root, text="Oui", variable=split_var).pack(pady=5)

    # Champs pour les timestamps
    tk.Label(root, text="Début (mm:ss) :").pack(pady=5)
    start_frame = ttk.Frame(root)
    start_frame.pack(pady=5)
    start_min_entry = ttk.Entry(start_frame, width=5)
    start_min_entry.pack(side="left")
    tk.Label(start_frame, text=":").pack(side="left")
    start_sec_entry = ttk.Entry(start_frame, width=5)
    start_sec_entry.pack(side="left")

    tk.Label(root, text="Fin (mm:ss) :").pack(pady=5)
    end_frame = ttk.Frame(root)
    end_frame.pack(pady=5)
    end_min_entry = ttk.Entry(end_frame, width=5)
    end_min_entry.pack(side="left")
    tk.Label(end_frame, text=":").pack(side="left")
    end_sec_entry = ttk.Entry(end_frame, width=5)
    end_sec_entry.pack(side="left")

    # Bouton pour soumettre
    ttk.Button(root, text="Soumettre", command=submit).pack(pady=10)

    # Label pour afficher les erreurs
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack(pady=5)

    root.mainloop()
    return split_choice, timestamps

def get_language_choice(prompt):
    """
    Interface graphique pour demander à l'utilisateur de choisir une langue.
    """
    def submit():
        nonlocal selected_language
        selected_language = language_var.get()
        root.destroy()

    selected_language = None

    root = tk.Tk()
    root.title("Choix de la langue")

    tk.Label(root, text=prompt).pack(pady=10)
    language_var = tk.StringVar(value="en")  # Langue par défaut : anglais
    ttk.Radiobutton(root, text="Anglais", variable=language_var, value="en").pack(anchor="w")
    ttk.Radiobutton(root, text="Français", variable=language_var, value="fr").pack(anchor="w")
    ttk.Radiobutton(root, text="Japonais", variable=language_var, value="ja").pack(anchor="w")
    ttk.Radiobutton(root, text="Finnois", variable=language_var, value="fi").pack(anchor="w")

    ttk.Button(root, text="Soumettre", command=submit).pack(pady=10)

    root.mainloop()
    return selected_language

if __name__ == "__main__":
    audio_path = "output_audio.wav"

    # Demander à l'utilisateur s'il souhaite découper l'audio
    split_choice, timestamps = get_user_choice_and_timestamps()

    if split_choice:
        print(f"Découpage demandé avec les timestamps : {timestamps}")
        parts = split_audio(audio_path, timestamps)

        # Demander les langues pour chaque partie
        languages = []
        for i in range(len(parts)):
            language = get_language_choice(f"Choisissez la langue pour la partie {i + 1} :")
            languages.append(language)

        output_files = [
            f"transcription_part{i + 1}.txt" for i in range(len(parts))
        ]

        for part, language, output_file in zip(parts, languages, output_files):
            transcribe_audio(part, language=language, output_file=output_file)
            if language == "ja":  # Appliquer la romanisation si la langue est japonaise
                romanized_output_file = output_file.replace(".txt", "_romanised.txt")
                romanize_file(output_file, romanized_output_file)
    else:
        # Demander la langue pour la transcription complète
        language = get_language_choice("Choisissez la langue pour la transcription complète :")
        print("Pas de découpage demandé. Transcription complète de l'audio.")
        transcribe_audio(audio_path, language=language, output_file="transcription_full.txt")
        if language == "ja":  # Appliquer la romanisation si la langue est japonaise
            romanize_file("transcription_full.txt", "transcription_full_romanised.txt")
