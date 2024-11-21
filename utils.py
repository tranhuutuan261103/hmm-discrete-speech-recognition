import json

def get_word_by_id(word_id):
    try:
        with open('./words.json', encoding='utf-8') as f:
            data = json.load(f)
        
        # Search for the word and return it
        for entry in data["words"]:
            if entry["id"] == word_id:
                return entry["word"]
            
        # If word not found, return None or raise an exception
        return None  # Word not found
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_id_by_word(word: str) -> int:
    try:
        with open('./words.json', encoding='utf-8') as f:
            data = json.load(f)

        # Search for the word and return its ID
        for entry in data["words"]:
            if entry["word"] == word:
                return entry["id"]

        # If word not found, return -1 or raise an exception
        return -1  # Word not found
    except Exception as e:
        print(f"Error: {e}")
        return -1

def get_all_words():
    try:
        with open('./words.json', encoding='utf-8') as f:
            data = json.load(f)
        
        # Return a list of all words
        return [entry["word"] for entry in data["words"]]
    except Exception as e:
        print(f"Error: {e}")
        return None