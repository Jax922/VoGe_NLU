import json
import os

prefix = """
version: "3.1"

nlu:
- intent: {}
  examples: |
"""

def load_data_from_json_by_line(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return data

def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    return data


def save_to_file(cat_text_content, prefix):
    output_dir = './data/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_paths = {}
    for category, texts in cat_text_content.items():
        file_name = os.path.join(output_dir, f'{category}.yml')
        with open(file_name, 'w') as file:
            file.write(prefix.format(category))
            for text in texts:
                file.write("\t\t" + "- " + text + '\n')
        file_paths[category] = file_name

    return file_paths

def highlight_handler():
    json_file_path = './train_data/hightlight_zoom_nextpage.json'
    data = load_data_from_json_by_line(json_file_path)

    cats_files = {}
    for item in data:
        if item["cats"]:
            cat = item["cats"][0]  
            text = item["text"]
            for start, end, entity in sorted(item["entities"], reverse=True):
                text = text[:start] + "[" + text[start:end] + "]" + "(" + entity + ")" + text[end:]
            if cat not in cats_files:
                cats_files[cat] = []
            cats_files[cat].append(text)
    file_paths = save_to_file(cats_files, prefix)
    print("Files saved to: ", file_paths)

def play_handler():
    json_file_path = './train_data/play_processing.json'
    data = load_data_from_json(json_file_path)["rasa_nlu_data"]["common_examples"]
    cats_files = {}

    for item in data:
        cat = item["intent"]
        text = item["text"]
        if cat not in cats_files:
            cats_files[cat] = []
        cats_files[cat].append(text)

    file_paths = save_to_file(cats_files, prefix)
    print("Files saved to: ", file_paths)


if __name__ == "__main__":
    # highlight_handler()
    play_handler()