import json
import os
import re

def preprocess(text):
    #Lowercase, preserve hyphenated words, remove special characters, and tokenize.
    text = text.lower()
    words = re.findall(r"\b\w+(?:-\w+)?\b", text)  # Matches words with optional hyphenation
    return words

def build_positional_index(data_dir):
    #Builds and saves a positional index from text documents
    if not os.path.exists(data_dir):
        print(f"❌ Error: Directory '{data_dir}' not found.")
        return

    positional_index = {}

    for root, _, files in os.walk(data_dir):  # Ensure all files are read
        for filename in files:
            file_path = os.path.join(root, filename)
            if not filename.endswith(".txt"):  # Ensure it's a text file
                continue

            content = None  # Ensure variable exists outside the try blocks

            # Try reading with UTF-8, fall back to ISO-8859-1 (Windows encoding)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
            except UnicodeDecodeError:
                print(f"⚠️ UTF-8 failed for {filename}, trying ISO-8859-1...")
                try:
                    with open(file_path, "r", encoding="ISO-8859-1") as file:
                        content = file.read().strip()
                except Exception as e:
                    print(f"❌ Skipping {filename}: {e}")
                    continue  # Skip this file

            # if not content:  # Debugging skipped files
            #     print(f"⚠️ Skipped empty file: {filename}")
            #     continue

            words = preprocess(content)
            doc_id = filename.replace(".txt", "")

            print(f"📄 Processing {filename} → Words: {len(words)}")  # Debugging output

            for position, word in enumerate(words, start=1):  #Start from 1
                if word not in positional_index:
                    positional_index[word] = {}
                if doc_id not in positional_index[word]:
                    positional_index[word][doc_id] = []
                positional_index[word][doc_id].append(position)  # Now positions start from 1

    # Save positional index
    with open("positional_index.json", "w", encoding="utf-8") as f:
        json.dump(positional_index, f, indent=4)

    print("✅ Positional Indexing complete! Saved in positional_index.json.")
def main():
    if __name__ == "__main__":
       data_dir = r"C:/Users/HP/IR_A1/Abstracts/Abstracts"  