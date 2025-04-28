import tkinter as tk
from tkinter import ttk

def get_video_and_timestamps_gui():
    def format_time(seconds):
        """Convertit les secondes en format mm:ss."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_start_label(value):
        """Met à jour l'affichage du timestamp de début."""
        start_label.config(text=f"Début : {format_time(int(value))}")

    def update_end_label(value):
        """Met à jour l'affichage du timestamp de fin."""
        end_label.config(text=f"Fin : {format_time(int(value))}")

    def submit():
        video_name = video_name_entry.get()
        start_time = start_slider.get()
        end_time = end_slider.get()

        if start_time >= end_time:
            result_label.config(text="Erreur : Le timestamp de début doit être inférieur au timestamp de fin.")
        else:
            result_label.config(
                text=f"Vidéo : {video_name}\nTimestamps : Début = {format_time(start_time)}, Fin = {format_time(end_time)}"
            )
            # Vous pouvez retourner ces valeurs ou les utiliser dans votre programme
            print(f"Vidéo : {video_name}")
            print(f"Timestamps : Début = {format_time(start_time)}, Fin = {format_time(end_time)}")

    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Sélection de la vidéo et des timestamps")

    # Entrée pour le nom de la vidéo
    tk.Label(root, text="Nom de la vidéo :").pack(pady=5)
    video_name_entry = ttk.Entry(root, width=40)
    video_name_entry.pack(pady=5)

    # Slider pour le timestamp de début
    tk.Label(root, text="Timestamp de début :").pack(pady=5)
    start_slider = tk.Scale(root, from_=0, to=3600, orient="horizontal", length=400, command=update_start_label)
    start_slider.pack(pady=5)
    start_label = tk.Label(root, text="Début : 00:00")
    start_label.pack(pady=5)

    # Slider pour le timestamp de fin
    tk.Label(root, text="Timestamp de fin :").pack(pady=5)
    end_slider = tk.Scale(root, from_=0, to=3600, orient="horizontal", length=400, command=update_end_label)
    end_slider.pack(pady=5)
    end_label = tk.Label(root, text="Fin : 00:00")
    end_label.pack(pady=5)

    # Bouton pour soumettre
    submit_button = ttk.Button(root, text="Soumettre", command=submit)
    submit_button.pack(pady=10)

    # Label pour afficher le résultat
    result_label = tk.Label(root, text="", fg="green")
    result_label.pack(pady=10)

    # Lancer la boucle principale
    root.mainloop()

# Exemple d'utilisation
if __name__ == "__main__":
    get_video_and_timestamps_gui()