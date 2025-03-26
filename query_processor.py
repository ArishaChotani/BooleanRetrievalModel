import json
import re
from nltk.stem import PorterStemmer

# Initialize Stemmer
stemmer = PorterStemmer()

def load_index(file_name):
    # Load an index (inverted or positional) from a JSON file
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            index = json.load(f)
            print(f"📌 Loaded {file_name} with {len(index)} terms.")
            return index
    except FileNotFoundError:
        print(f"❌ Error: {file_name} not found.")
        return {}

# Boolean Query Processing
def process_query(query, index, positional_index):
   #Process queries: Boolean (AND, OR, NOT) and Proximity ('word1 word2 /n')
    print(f"\n🔍 Processing Query: {query}")

    query = query.lower().strip()

    # Handle Proximity Search (e.g., "word1 word2 /3")
    # Check if the query matches a proximity search pattern
    match = re.search(r'(\w+)\s+(\w+)\s*/\s*(\d+)', query)
    if match:
        term1, term2, distance = match.groups()
        return proximity_search(term1, term2, int(distance))


    # Normalize Boolean operators
    query = query.replace(" not ", " NOT ").replace(" and ", " AND ").replace(" or ", " OR ")
    
    # tokenize & Stem query terms (excluding operators)
    tokens = [stemmer.stem(word) if word not in {"AND", "OR", "NOT"} else word for word in query.split()]
    
    print(f"📌 Tokenized Query: {tokens}")
    
    return evaluate_boolean_expression(tokens, index)
def evaluate_boolean_expression(tokens, index):
    """
    Precedence Order:
    1. NOT (Highest precedence, applied first)
    2. AND (Processed before OR)
    3. OR (Lowest precedence, applied last)
    """
    result_stack = []  # Holds sets of document results
    operator_stack = []  # Holds Boolean operators

    def apply_operator():
        #Applies the top operator from operator_stack to result_stack
        if not result_stack or not operator_stack:
            return
        
        operator = operator_stack.pop()
        
        if operator == "NOT":
            # NOT operator negates the top operand
            term_docs = result_stack.pop()
            all_docs = {doc for docs in index.values() for doc in docs}  
            result_stack.append(all_docs - term_docs)
        else:
            # AND / OR requires two operands
            right_docs = result_stack.pop()
            left_docs = result_stack.pop()
            
            if operator == "AND":
                result_stack.append(left_docs & right_docs)  # Intersection
            else:  # OR
                result_stack.append(left_docs | right_docs)  # Union

    for token in tokens:
        if token == "NOT":
            operator_stack.append(token)
        elif token == "AND":
            # Process previous AND before pushing a new AND if two and
            while operator_stack and operator_stack[-1] == "AND":
                apply_operator()
            operator_stack.append(token)
        elif token == "OR":
            # Apply previous AND/OR operators before pushing OR (since AND has higher precedence)
            while operator_stack and operator_stack[-1] in {"AND", "OR"}:
                apply_operator()
            operator_stack.append(token)
        else:
            #documents set for a term
            result_stack.append(set(index.get(token, {}).keys()))
    
    # Apply remaining operators in stack
    while operator_stack:
        apply_operator()
    
    return sorted(result_stack[0]) if result_stack else []

def proximity_search(term1, term2, max_distance):
    #Find documents where term1 and term2 appear 
    # within max_distance words of each other
    
    # Load positional index
    with open("positional_index.json", "r", encoding="utf-8") as f:
        positional_index = json.load(f)

    if term1 not in positional_index or term2 not in positional_index:
        print(f"❌ One or both terms ('{term1}', '{term2}') not found in index.")
        return []

    docs_with_term1 = set(positional_index[term1].keys())
    docs_with_term2 = set(positional_index[term2].keys())

    common_docs = docs_with_term2.intersection(docs_with_term1)

    if not common_docs:
        print(f"❌ No documents contain both '{term1}' and '{term2}'.")
        return []

    results = []
    
    for doc in common_docs:
        positions1 = positional_index[term1][doc]
        positions2 = positional_index[term2][doc]
        # Check for proximity
        for pos1 in positions1:
            for pos2 in positions2:
                distance = abs(pos1 - pos2)  # Calculate distance
                if distance <= max_distance + 1:  # Adjust for 1-based index
                    results.append((doc))

    if results:
        formatted_results = [f"Doc: {doc}" 
                     for doc in results] 
        print("\n✅ Matches found :\n{}".format( "\n".join(formatted_results)))
    else:
        print(f"\n❌ No matches found within {max_distance} words.")

    return results

 #this part is for debugging purposes only
if __name__ == "__main__":
   
    inverted_index = load_index("inverted_index.json")
    positional_index = load_index("positional_index.json")

    while True:
        query = input("\nEnter query (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("👋 Exiting.")
            break
        result = process_query(query, inverted_index, positional_index)
        print(f"✅ Documents Found: {result}" if result else "❌ No matches.")
    def check_term_existence(term, positional_index):

     if term in positional_index:
        print(f"✅ Term '{term}' exists in positional index.")
        print(f"📌 Found in Documents: {list(positional_index[term].keys())}")
        for doc, positions in positional_index[term].items():
            print(f"   📄 Doc: {doc} → Positions: {positions}")
     else:
        print(f"❌ Term '{term}' NOT found in positional index.")
