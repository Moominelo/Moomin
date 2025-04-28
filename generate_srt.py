import os
import re

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_srt(output_path, lines):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def parse_line_with_timestamps(line, time_offset=0):
    """
    Parse une ligne contenant des timestamps au format [start - end] et retourne les valeurs formatées pour SRT.
    Applique un décalage temporel (time_offset) en secondes.
    """
    match = re.match(r"\[(\d+\.\d+)s - (\d+\.\d+)s\]\s+(.*)", line)
    if match:
        start_time, end_time, text = match.groups()
        start_time = float(start_time) + time_offset
        end_time = float(end_time) + time_offset

        # Convertir les timestamps en format SRT (hh:mm:ss,ms)
        start_time_str = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02},{int((start_time % 1) * 1000):03}"
        end_time_str = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02},{int((end_time % 1) * 1000):03}"

        return start_time_str, end_time_str, text.strip()
    return None, None, None

def get_files_in_order():
    """
    Récupère les fichiers dans l'ordre : part1, part2, part3.
    Utilise les fichiers romanisés si disponibles.
    """
    files = []
    for i in range(1, 4):  # part1, part2, part3
        romanised_file = f"transcription_part{i}_romanised.txt"
        normal_file = f"transcription_part{i}.txt"
        if os.path.exists(romanised_file):
            files.append(romanised_file)
        elif os.path.exists(normal_file):
            files.append(normal_file)
        else:
            print(f"⚠️ Fichier manquant pour part{i}.")
            files.append(None)
    return files

def generate_srt():
    # Récupérer les fichiers dans l'ordre
    files = get_files_in_order()

    # Vérifier si tous les fichiers nécessaires sont présents
    if None in files:
        print("❌ Impossible de générer le fichier SRT : certains fichiers sont manquants.")
        return

    # Output file
    output_srt = "output.srt"

    # Offsets pour chaque partie
    offsets = [0, 90, 1389]  # En secondes : part1 = 0s, part2 = +1min30, part3 = +23min09

    # Combine all lines with appropriate time offsets
    srt_lines = []
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

if __name__ == "__main__":
    generate_srt()
