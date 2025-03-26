import preprocessing # Module for preprocessing text data
import index         # Module to create the inverted index
import positional_index  # Module to build the positional index


#directory path where the abstract documents are stored
#DATA_DIR = r"C:/Users/HP/IR_A1/Abstracts/Abstracts"

def main():
    print("\n📌 Starting Information Retrieval System...\n")
    # Step 1: Preprocessing documents
    try:
        print("🔹 Preprocessing abstracts...")
        preprocessing.main() #Pass DATA_DIR
        print("✅ Preprocessing complete!\n")
    except Exception as e:
        print(f"❌ Error in preprocessing: {e}")
        return
    # Step 2: Building the inverted index
    try:
        print("🔹 Building inverted index...")
        index.main()
        print("✅ Indexing complete!\n")
    except Exception as e:
        print(f"❌ Error in indexing: {e}")
        return
     # Step 3: Building the positional index
    try:
        #print("🔹 Checking DATA_DIR:", DATA_DIR)  # Debugging print
        print("🔹 Building positional index...")
        positional_index.main() 
        print("✅ Positional indexing complete!\n")
    except Exception as e:
        print(f"❌ Error in positional indexing: {e}")
        return
#def main1():
if __name__ == "__main__":
    main()
