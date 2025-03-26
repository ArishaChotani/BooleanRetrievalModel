import json

def load_preprocessed_data():
    with open("preprocessed.json", "r") as f:
        return json.load(f)

def build_index():
    #Build an inverted index
    # Load the preprocessed data (word lists for each document)
    data = load_preprocessed_data()
    index = {}
    #Iterate over each document
    for doc_id, words in data.items():
        for word in words: # iterating all words in the document
            #If word is not in index, initialize it
            if word not in index:
                index[word] = {}
            if doc_id not in index[word]: # If doc_id not in word's dictionary in index
                index[word][doc_id] = 0
            index[word][doc_id] += 1  # increases the count of the word in the document.

    # Save inverted index
    with open("inverted_index.json", "w") as f:
        json.dump(index, f, indent=4)

    print("✅ Inverted Indexing complete! Saved in inverted_index.json.")
def main():
    if __name__ == "__main__":
       build_index()