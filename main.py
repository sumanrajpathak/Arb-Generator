import os
import csv
import json
import re
from config import CSV_FILE, ARB_DIR, ARB_FILE_PREFIX, ARB_FILE_EXT
from re import search



def get_arb_file_name(lang):
    """
    Get the arb filename using the lang code
    :param lang: Language code (str)
    :return: Full file name with arb file prefix and extension joined with lang code (str)
    """
    return f"{ARB_FILE_PREFIX}{lang}{ARB_FILE_EXT}"


def get_existing_lang_data(lang):
    """
    Read existing arb file for the provided language if available
    :param lang: Language code (str)
    :return: Content of the file if available or empty dict
    """
    lang_file = ARB_DIR.joinpath(get_arb_file_name(lang))

    if os.path.isfile(lang_file):
        try:
            with open(lang_file, 'r+') as fp:
                return json.load(fp)
        except Exception as e:
            print(f"Error while loading existing arb file: {lang_file}, Error: {e}")
            return {}
    else:
        return {}


def write_to_file(lang, lang_data):
    """
    Create or override an existing lang file with the lang data as json
    :param lang: language code (str)
    :param lang_data: Updated language data (dict)
    :return: Boolean true/false as per the written status
    """
    lang_file = ARB_DIR.joinpath(get_arb_file_name(lang))

    try:
        with open(lang_file, 'w+', encoding="utf-8") as fp:
            fp.seek(0)
            fp.write(json.dumps(lang_data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Exception occurred while writing language, {lang} to file: {lang_file}")
        return False
    else:
        return True


def map_row_to_lang(found_lang, row):
    """
    Map each row of the csv file according to the languages
    :param found_lang: languages string (list)
    :param row: Csv row (list)
    :return: Tuple containing language and its mapped value from the csv
    """
    lang_dict_key = row[0]
    mapped_lang_value = {}
    for lang_pos, lang in enumerate(found_lang, start=1):
        try:
            mapped_lang_value[lang] = row[lang_pos]
            # mapped_lang_value[lang] = f'@{row[lang_pos]}'
           
        except IndexError:
            mapped_lang_value[lang] = ""
   
    return lang_dict_key, mapped_lang_value

def get_lang_value(lang_values):
    """
    Check if the provided value is Dynamic
    :param lang_value: string
    :return: tuple with placeholders
    """
    result = re.search('\\{.*\\}',lang_values)
    
    if result:
        return {'placeholders': { lang_values[result.start()+1:result.end()-1]:{}} }
    else:
        return ''

def main():
    """
    Main method that is being executed while running this file.
    :return: None
    """
    num_lang = 0
    found_lang = []
    lang_dict = None

    with open(CSV_FILE, 'r') as csv_fp:
        csv_reader = csv.reader(csv_fp, delimiter=',')

        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                num_lang = len(row) - 1
                if num_lang < 1:
                    raise Exception("There is less than or a single column. Column should be at least 2."
                                    " 1 for key another for language")
                lang_dict = {}
                found_lang = row[1:]
                for lang in found_lang:
                    lang_dict[lang] = get_existing_lang_data(lang)

            else:

                lang_dict_key, mapped_lang_value = map_row_to_lang(found_lang, row)
                for lang_key, lang_values in mapped_lang_value.items():
                    lang_dict[lang_key][lang_dict_key] = lang_values
                    if  get_lang_value(lang_values):
                        lang_dict[lang_key][f'@{lang_dict_key}'] = get_lang_value(lang_values)

            line_count += 1
        # print(lang_dict)
        if not num_lang:
            raise Exception("There is less than or a single column. Column should be at least 2."
                            " 1 for key another for language")

        for lang_key, lang_values in lang_dict.items():
            write_to_file(lang_key, lang_values)


if __name__ == "__main__":
    main()
