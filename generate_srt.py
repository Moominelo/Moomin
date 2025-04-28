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