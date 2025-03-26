import os
import json
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources
nltk.download("punkt")

# Initialize Stemmer
stemmer = PorterStemmer()

def load_stopwords(filename="Stopword-List.txt"):
    #Load stopwords from a file
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return set(f.read().split())
    except FileNotFoundError:
        print(f"⚠️ Warning: {filename} not found. Using an empty stopword list.")
        return set()

def preprocess_text(text, stopwords):
    #Tokenize, lowercase, remove stopwords, and apply stemming
    if not text:  # Handle cases where text is None or empty
       return []
    words = word_tokenize(text.lower())  # Tokenize & convert to lowercase only keeps alphanumeric words
    processed_words = [stemmer.stem(word) for word in words if word.isalnum() and word not in stopwords] #remove stopwords
    return processed_words

def preprocess_documents(input_dir="Abstracts", output_file="preprocessed.json"):
    #Preprocess all documents
    if not os.path.exists(input_dir):
        print(f"❌ Error: Directory '{input_dir}' not found.")
        return

    stopwords = load_stopwords()
    preprocessed_data = {}
    # go through all files in the directory
    # root is The current directory path
    # _  stores subdirectories here used as a throw away
    #files stores a list of file names directory.
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            #if file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read().strip() # Read file content
                        # if not content: #skip empty files
                        #     print(f"⚠️ Skipping empty file: {file_name}")
                        #     continue
                        doc_id = file_name.replace(".txt", "")  # Use filename (without .txt) as document ID
                        preprocessed_data[doc_id] = preprocess_text(content, stopwords)
                except Exception as e:
                    print(f"⚠️ Error processing {file_name}: {e}")

    # Save preprocessed data
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(preprocessed_data, f, indent=4)

    print(f"✅ Preprocessing complete! Data saved in {output_file}.")

def main():
   if __name__ == "__main__":
       preprocess_documents()
