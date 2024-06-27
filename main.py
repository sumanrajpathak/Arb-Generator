import csv
import json
import os
import re
from pathlib import Path

from config import ARB_DIR, ARB_FILE_EXT, ARB_FILE_PREFIX, CSV_FILE

# Convert ARB_DIR to a Path object directly in the config, if not already.
ARB_DIR = Path(ARB_DIR)

def get_arb_file_name(lang):
    """
    Construct the ARB filename using the language code.
    """
    return f"{ARB_FILE_PREFIX}{lang}{ARB_FILE_EXT}"

def load_language_data(lang):
    """
    Load language data from an ARB file, returning it as a dictionary.
    """
    lang_file = ARB_DIR / get_arb_file_name(lang)
    try:
        with open(lang_file, 'r', encoding='utf-8') as fp:
            return json.load(fp)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file does not exist
    except json.JSONDecodeError as e:
        print(f"Error reading {lang_file}: {e}")
        return {}

def write_language_data(lang, data):
    """
    Write the provided dictionary `data` to the language-specific ARB file.
    """
    lang_file = ARB_DIR / get_arb_file_name(lang)
    try:
        with open(lang_file, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error writing to {lang_file}: {e}")

def extract_dynamic_value(value):
    """
    Extract dynamic content from a string, returning a dictionary if dynamic content is found.
    """
    matches = re.findall(r'\{([^{}]*)\}', value)
    return {'placeholders': {match: {}} for match in matches} if matches else {}

def process_csv():
    """
    Process the CSV file to read and update language-specific ARB files.
    """
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            lang_codes = headers[1:]

            lang_data = {lang: load_language_data(lang) for lang in lang_codes}

            for row in reader:
                key = row[0]
               
                for lang, value in zip(lang_codes, row[1:]):
                    dynamic_content = extract_dynamic_value(value)
                    if dynamic_content:
                        lang_data[lang].setdefault(f'@{key}', dynamic_content)
                    lang_data[lang][key] = value

            for lang, data in lang_data.items():
                write_language_data(lang, data)

    except Exception as e:
        print(f"Failed to process CSV file: {e}")

if __name__ == "__main__":
    process_csv()
