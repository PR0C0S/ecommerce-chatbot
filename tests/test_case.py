import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import chromadb
import time
from chatbot_test import chatbot_test
from sklearn.metrics.pairwise import cosine_similarity
import json


# Configuration
host = os.environ.get('HOST')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
database = os.environ.get('DATABASE')
DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# Initialize SentenceTransformer and Chroma
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
CHROMA_PATH = "chroma"  # Specify the directory for Chroma persistence

# Use PersistentClient for the updated Chroma configuration
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
chroma_collection = chroma_client.get_or_create_collection("test_results", embedding_function=embedding_function)

def connect_to_db():
    try:
        engine = create_engine(DATABASE_URI, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Database connection successful.")
        return session, engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None, None

def store_in_chroma(test_name, result):
    # Convert the result to a string and create an embedding
    result_str = json.dumps(result, default=str)
    embeddings = embedding_function([result_str])
    
    # Generate a unique ID using test_name and timestamp
    unique_id = f"{test_name}_{int(time.time())}"
    
    # Store the result in Chroma with the unique ID
    chroma_collection.add(
        embeddings=embeddings,
        metadatas=[{"test_name": test_name}],
        ids=[unique_id]
    )
    print(f"Stored in Chroma with ID: {unique_id}")

def calculate_similarity(expected_result, generated_result):
    # Convert both expected and generated result to string and create embeddings
    expected_str = json.dumps(expected_result, default=str)
    generated_str = json.dumps(generated_result, default=str)
    
    embeddings = embedding_function([expected_str, generated_str])
    
    # Calculate cosine similarity
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return similarity

def run_tests(json_file, session, engine):
    similarity_scores = []  # List to store similarity scores for each test

    with open(json_file, 'r') as f:
        test_cases = json.load(f)

    for test in test_cases:
        question = test['question']
        expected_answer = test['expected_answer']
        print(f"\nQuestion: {question}")
        print(f"Expected SQL: {expected_answer}")

        try:
            # Execute the expected SQL query and fetch the result
            with engine.connect() as conn:
                result = conn.execute(text(expected_answer)).fetchall()
                print(f"Result from DB: {result}")

                # Store the result in Chroma (you can customize this storage if necessary)
                store_in_chroma(test['question'], result)

                # Generate SQL using the chatbot_test function and capture the raw result (including query)
                generated_response = chatbot_test(f"Question: {question}")

                # Extract the SQL query from the generated response
                generated_sql = json.loads(generated_response).get("captured_query")
                print(f"Generated SQL by chatbot_test: {generated_sql}")

                if generated_sql:
                    # Execute the generated SQL query and get the result
                    generated_result = conn.execute(text(generated_sql)).fetchall()
                    print(f"Generated Result: {generated_result}")

                    # Calculate similarity between expected and generated results
                    similarity = calculate_similarity(result, generated_result)
                    print(f"Similarity Score: {similarity:.2f}")

                    # Store the similarity score for calculating the grand global score
                    similarity_scores.append(similarity)
                else:
                    print("❌ No valid SQL query generated.")

        except Exception as e:
            print(f"❌ Test failed. Query execution error: {e}")

    # Calculate and print the grand global score (average similarity score)
    if similarity_scores:
        grand_global_score = sum(similarity_scores) / len(similarity_scores)
        print(f"\nGrand Global Score (Average Similarity): {grand_global_score:.2f}")
    else:
        print("\nNo similarity scores to calculate.")

def main():
    # Connect to the database
    session, engine = connect_to_db()
    if not session or not engine:
        print("Skipping tests due to database connection failure.")
        return

    # Run tests from JSON file
    json_file = "tests/test_cases.json"
    run_tests(json_file, session, engine)

if __name__ == "__main__":
    main()
