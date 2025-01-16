import os
from gradio_client import Client
import json
from chatbot_test import chatbot


embedding_key=os.environ.get('OPENAI_EMBEDDING_KEY')
api_key=os.environ.get('OPENAI_API_KEY')


def load_test_dataset(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)


def test_chatbot_with_gradio(client, api_name, test_dataset):
    results = []
    for test_case in test_dataset:
        try: 
            question = test_case["question"]
            expected_query = test_case["query"]

            # Invoke the chatbot using the Gradio client
            # response = client.predict(
            #     query_text=question,
            #     api_name=api_name
            # )
            response=chatbot(question)

            response_dict = json.loads(response) 
            print(response_dict)
            captured_queries = response_dict.get("captured_queries", "")
          
            # Compare with the expected query
            is_correct = captured_queries == expected_query
            results.append({
                "question": question,
                "expected_query": expected_query,
                "generated_query": captured_queries,
                "is_correct": is_correct
            })
        except Exception as e:
            print(f"ERROR:{e}")
    return results

# Function to print the test results
def print_test_results(results):
    for i, result in enumerate(results, start=1):
        print(f"Test Case {i}:")
        print(f"  Question: {result['question']}")
        print(f"  Expected Query: {result['expected_query']}")
        print(f"  Generated Query: {result['generated_query']}")
        print(f"  Is Correct: {'Yes' if result['is_correct'] else 'No'}")
        print("-" * 60)

def calculate_accuracy(results):
    total_cases = len(results)
    correct_cases = sum(result["is_correct"] for result in results)
    accuracy = (correct_cases / total_cases) * 100 if total_cases > 0 else 0
    print(f"Accuracy: {accuracy:.2f}% ({correct_cases}/{total_cases} correct cases)")
    return accuracy

# Main execution
if __name__ == "__main__":
    # Load the test dataset from a JSON file
    test_dataset_path = "test.json"  # Replace with the actual path to your JSON file
    test_dataset = load_test_dataset(test_dataset_path)

    # # Initialize the Gradio client
    gradio_url = "http://127.0.0.1:7860/"  # Replace with your Gradio app's URL
    client = Client(gradio_url)

    # Test the chatbot with the dataset
    test_results = test_chatbot_with_gradio(
        client=client,
        api_name="/predict",  # Replace with your Gradio app's API name
        test_dataset=test_dataset
    )

    # Print the results
    print_test_results(test_results)
    calculate_accuracy(test_results)
