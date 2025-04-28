import os
import pykakasi

def romanize_file(input_file, output_file):
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    # Initialize Kakasi for romanization
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "a")  # Hiragana to ascii
    kakasi.setMode("K", "a")  # Katakana to ascii
    kakasi.setMode("J", "a")  # Japanese to ascii
    kakasi.setMode("r", "Hepburn")  # Use Hepburn Romanization
    converter = kakasi.getConverter()

    # Read the input file and romanize its content
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            romanized_line = converter.do(line.strip())
            outfile.write(romanized_line + "\n")

    print(f"Romanization complete. Output saved to '{output_file}'.")


