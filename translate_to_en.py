from deep_translator import GoogleTranslator
import re

# File paths
input_file = 'transcription_part2.txt'
output_file = 'transcription_part2_englished.txt'

# Dictionnaire personnalisé pour adapter le vocabulaire des Moomins
moomin_vocabulary = {
    "Muumilaaksoon": "Moominvalley",
    "Muumipeikosta": "Moomintroll",
    "Niiskuneiti": "Snorkmaiden",
    "Haisuli": "Stinky",
    "Mörkö": "Groke",
    "Hemuli": "Hemulen",
    "Nipsu": "Sniff",
    "Muumipappa": "Moominpappa",
    "Muumimamma": "Moominmamma",
}

def apply_moomin_vocabulary(text):
    """
    Remplace certains mots ou expressions par des termes spécifiques au vocabulaire des Moomins.
    """
    for finnish_word, english_word in moomin_vocabulary.items():
        text = text.replace(finnish_word, english_word)
    return text

def parse_and_translate_lines(lines, translator):
    """
    Parse et traduit plusieurs lignes contenant des timestamps tout en conservant les timestamps.
    """
    translated_lines = []
    for i, line in enumerate(lines, start=1):
        match = re.match(r"\[(\d+\.\d+)s - (\d+\.\d+)s\]\s+(.*)", line)
        if match:
            start_time, end_time, text = match.groups()
            if text.strip():  # Vérifier que le texte n'est pas vide
                try:
                    # Traduire le texte
                    print(f"Translating line {i}: {text.strip()}")
                    translated_text = translator.translate(text)
                    # Appliquer le vocabulaire des Moomins
                    translated_text = apply_moomin_vocabulary(translated_text)
                    print(f"Translated line {i}: {translated_text}")
                    # Reconstruire la ligne avec les timestamps
                    translated_lines.append(f"[{start_time}s - {end_time}s] {translated_text}\n")
                except Exception as e:
                    print(f"Error translating line {i}: {line.strip()} - {e}")
                    translated_lines.append(line)  # Retourner la ligne inchangée en cas d'erreur
            else:
                translated_lines.append(line)  # Retourner la ligne inchangée si le texte est vide
        else:
            translated_lines.append(line)  # Retourner la ligne inchangée si elle ne correspond pas au format attendu
    return translated_lines

try:
    # Initialize the translator
    print("Initializing translator...")
    translator = GoogleTranslator(source='fi', target='en')

    # Read the Finnish transcription file
    print(f"Reading input file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    print(f"Found {len(lines)} lines to translate.")

    # Translate all lines
    translated_lines = parse_and_translate_lines(lines, translator)

    # Write the translated lines to the output file
    print(f"Writing translated lines to output file: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

    print(f"Translation completed. Translated text saved to '{output_file}'.")
except Exception as e:
    print(f"An error occurred: {e}")
