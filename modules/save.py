import json

def save_to_json(data, file_name='data.json'):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
    print(f"Data scraped and saved to '{file_name}'.")
