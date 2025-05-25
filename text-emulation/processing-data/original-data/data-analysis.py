import json


def load_json_or_jsonl(file_path):
    # Determine the file type based on the extension
    if file_path.endswith('.json'):
        # Load JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    elif file_path.endswith('.jsonl'):
        # Load JSONL file
        with open(file_path, 'r', encoding='utf-8') as file:
            return [json.loads(line) for line in file]

    else:
        raise ValueError("Unsupported file type. Please provide a '.json' or '.jsonl' file.")


def document_count(data):
    return len(data)


def averge(data):
    total = 0
    for item in data:
        total += len(item.split(" "))
    print(f"total word: {total}")
    return total / len(data)


def bookInfor(data):
    allpara = data.values()
    return allpara


data_json = load_json_or_jsonl('AllData/HackerNews.json')
print(f"have average: {averge(data_json)}")
print(f"have document: {document_count(data_json)}")

data_json = load_json_or_jsonl('AllData/PUBMED_title_abstracts_2019_baseline.jsonl')
print(f"have average: {averge(data_json)}")
print(f"have document: {document_count(data_json)}")

data_json = load_json_or_jsonl('AllData/wiki.json')
print(f"have average: {averge(data_json)}")
print(f"have document: {document_count(data_json)}")

data_json = load_json_or_jsonl('AllData/wiki.json')
data_json = bookInfor(data_json)
print(f"have average: {averge(data_json)}")
print(f"have document: {document_count(data_json)}")
