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

def generate_srt():
    # Input files
    part1_file = "romanised_transcription_part1.txt"
    finnish_file = "transcription_english_moomin.txt"
    part2_file = "romanised_transcription_part2.txt"

    # Output file
    output_srt = "output.srt"

    # Read input files
    try:
        part1_lines = read_file(part1_file)
        finnish_lines = read_file(finnish_file)
        part2_lines = read_file(part2_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Combine all lines with appropriate time offsets
    srt_lines = []
    index = 1

    # Process part 1 (no offset)
    for line in part1_lines:
        start_time_str, end_time_str, text = parse_line_with_timestamps(line, time_offset=0)
        if start_time_str and end_time_str and text:
            srt_lines.append(f"{index}\n")
            srt_lines.append(f"{start_time_str} --> {end_time_str}\n")
            srt_lines.append(f"{text}\n\n")
            index += 1

    # Process Finnish part (+1min30 offset)
    for line in finnish_lines:
        start_time_str, end_time_str, text = parse_line_with_timestamps(line, time_offset=90)  # 1min30 = 90s
        if start_time_str and end_time_str and text:
            srt_lines.append(f"{index}\n")
            srt_lines.append(f"{start_time_str} --> {end_time_str}\n")
            srt_lines.append(f"{text}\n\n")
            index += 1

    # Process part 2 (+23min09 offset)
    for line in part2_lines:
        start_time_str, end_time_str, text = parse_line_with_timestamps(line, time_offset=1389)  # 23min09 = 1389s
        if start_time_str and end_time_str and text:
            srt_lines.append(f"{index}\n")
            srt_lines.append(f"{start_time_str} --> {end_time_str}\n")
            srt_lines.append(f"{text}\n\n")
            index += 1

    # Write to output file
    write_srt(output_srt, srt_lines)
    print(f"SRT file generated: {output_srt}")

if __name__ == "__main__":
    generate_srt()
    print("Bravo")