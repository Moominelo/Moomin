import os

def supprimer_fichiers_temporaire():
    """
    Supprime les fichiers audio et de transcription temporaires.
    """
    fichiers_a_supprimer = [
        'output_audio.wav',
        'part1.wav',
        'part2.wav',
        'part3.wav',
        'transcription_part_1.txt',
        'transcription_part_2.txt',
        'transcription_part_3.txt',
        'end_transcription_part_1.txt',
        'end_transcription_part_2.txt',
        'end_transcription_part_3.txt'
    ]

    for fichier in fichiers_a_supprimer:
        if os.path.exists(fichier):
            try:
                os.remove(fichier)
                print(f"✅ Fichier supprimé : {fichier}")
            except Exception as e:
                print(f"❌ Impossible de supprimer le fichier {fichier} : {e}")
        else:
            print(f"⚠️ Fichier non trouvé : {fichier}")

if __name__ == "__main__":
    supprimer_fichiers_temporaire()