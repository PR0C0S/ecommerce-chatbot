# Test Methodology for Chatbot SQL Query Generation

This document outlines the methodology for testing the chatbot's ability to generate correct SQL queries based on user-provided questions. The methodology includes test dataset preparation, execution, evaluation, and performance measurement.

## Table of Contents
1. [Objective](#objective)
2. [Test Dataset With Query Result Similarity](#test-dataset-with-query-result-similarity)
3. [Testing Workflow With Query Result Similarity](#testing-workflow-with-query-result-similarity)
4. [Evaluation Metrics With Query Result Similarity](#evaluation-metrics-with-query-result-similarity)
5. [Execution Steps With Query Result Similarity](#execution-steps-with-query-result-similarity)
6. [Expected Output With Query Result Similarity](#expected-output-with-query-result-similarity)
7. [Test Dataset With Query Similarity](#test-dataset-with-query-similarity)
8. [Testing Workflow With Query Similarity](#testing-workflow)
9. [Evaluation Metrics With Query Similarity](#evaluation-metrics)
10. [Execution Steps With Query Similarity](#execution-steps)
11. [Expected Output With Query Similarity](#expected-output)

---

## Objective

To validate the chatbot's SQL query generation by comparing its outputs with predefined expected SQL queries output and also the similarity of queries themselves for a given set of test questions.

---

## Test Dataset With Query Result Similarity
The test dataset is stored in a JSON file (`tests/test_cases.json`) with the following structure:

```json
[
    {
        "question": "What is the total revenue in the last quarter?",
        "expected_answer": "SELECT SUM(revenue) FROM sales WHERE quarter = 'last';"
    },
    {
        "question": "List all customers who made purchases in January.",
        "expected_answer": "SELECT customer_name FROM purchases WHERE month = 'January';"
    }
]
```

- **Fields**:
  - `question`: The natural language question to be input into the chatbot.
  - `expected_answer`: The expected SQL query corresponding to the question.

---

## Testing Workflow With Query Result Similarity

1. **Test Dataset Loading**:
   - Load the JSON dataset containing test cases.
   - Each test case consists of a user question and the expected SQL query.

2. **Chatbot Invocation**:
   - Pass the question from the test dataset to the chatbot (chatbot_test function).
   - Capture the SQL query generated by the chatbot and execute it on the database.

3. **Similarity Check**:
   - Compare the results of the expected and generated SQL queries by:
     - Converting both results to JSON strings.
     - Generating embeddings using the `SentenceTransformer` model.
     - Calculating `cosine-similarity` between the embeddings.
   - If the cosine similarity score exceeds the threshold (default: 0.8 or 80%), the generated query result is considered correct.

4. **Results Aggregation**:
   - Record the question, expected query, generated query, similarity score, and correctness in the results.

---

## Evaluation Metrics With Query Result Similarity

1. **Similarity Threshold**:
   - A threshold of 0.8 (80%) is used to determine if the generated query result matches the expected query result.

2. **Accuracy**:
   - The percentage of test cases where the similarity score meets or exceeds the threshold:
     Accuracy = ( Number of Correct Cases / Total Test Cases ) × 100

3. **Execution Time**:
   - Measure the total time taken to execute each test case and the overall execution.

---

## Execution Steps With Query Result Similarity

1. **Setup**:
   - Install necessary requirements:
      ```bash
     pip install -r requirements.txt
     ```
   - Export the required API keys:
     ```bash
     export OPENAI_API_KEY=<your_openai_api_key>
     export OPENAI_EMBEDDING_KEY=<your_openai_embedding_key>
     ```

2. **Run the Tests**:
   - Execute the script using:
     ```bash
     python -m tests.test_case
     ```

3. **Observe the Results**:
   - View the results printed in the console.
   - The results include details for each test case and overall accuracy.

---

## Expected Output With Query Result Similarity

1. **Console Output**:
   - Test case results for each question:
     ```
     Test Case 1:
       Question: What is the total revenue in the last quarter?
       Expected SQL: SELECT SUM(revenue) FROM sales WHERE quarter = 'last';
       Generated SQL: SELECT SUM(revenue) FROM sales WHERE quarter = 'last';
       Similarity Score: 0.89
       Total Time Taken for test 1: 22.64 seconds
     ------------------------------------------------------------

2. **Elapsed Time**:
   - Total time taken to execute the tests:
     ```
     Grand Global Score (Average Similarity): 0.86
     Total Time Taken for run_tests: 1912.84 seconds
     ```

---

## Test Dataset With Query Similarity
The test dataset is stored in a JSON file (`test.json`) with the following structure:

```json
[
    {
        "question": "What is the total revenue in the last quarter?",
        "query": "SELECT SUM(revenue) FROM sales WHERE quarter = 'last';"
    },
    {
        "question": "List all customers who made purchases in January.",
        "query": "SELECT customer_name FROM purchases WHERE month = 'January';"
    }
]
```

- **Fields**:
  - `question`: The natural language question to be input into the chatbot.
  - `query`: The expected SQL query corresponding to the question.

---

## Testing Workflow

1. **Test Dataset Loading**:
   - Load the JSON dataset containing test cases.
   - Each test case consists of a user question and the expected SQL query.

2. **Chatbot Invocation**:
   - Pass the question from the test dataset to the chatbot.
   - Capture the SQL query generated by the chatbot.

3. **Similarity Check**:
   - Normalize both the generated and expected queries by:
     - Converting to lowercase.
     - Removing extra whitespace.
     - Appending a semicolon if missing.
   - Use the `SequenceMatcher` library to calculate the similarity ratio between the two queries.
   - If the similarity ratio is above the threshold (default: 80%), the query is considered correct.

4. **Results Aggregation**:
   - Record the question, expected query, generated query, and correctness in the results.

---

## Evaluation Metrics

1. **Similarity Threshold**:
   - A threshold of 0.8 (80%) is used to determine if the generated query matches the expected query.

2. **Accuracy**:
   - The percentage of test cases where the generated query is correct:
     \[
     \text{Accuracy} = \left( \frac{\text{Number of Correct Cases}}{\text{Total Test Cases}} \right) \times 100
     \]

3. **Execution Time**:
   - Measure the total time taken to execute all test cases.

---

## Execution Steps

1. **Setup**:
   - Install necessary requirements:
      ```bash
     pip install -r requirements.txt
     ```
   - Export the required API keys:
     ```bash
     export OPENAI_API_KEY=<your_openai_api_key>
     export OPENAI_EMBEDDING_KEY=<your_openai_embedding_key>
     ```

2. **Run the Tests**:
   - Execute the script using:
     ```bash
     python test.py
     ```

3. **Observe the Results**:
   - View the results printed in the console.
   - The results include details for each test case and overall accuracy.

---

## Expected Output

1. **Console Output**:
   - Test case results:
     ```
     Test Case 1:
       Question: What is the total revenue in the last quarter?
       Expected Query: SELECT SUM(revenue) FROM sales WHERE quarter = 'last';
       Generated Query: SELECT SUM(revenue) FROM sales WHERE quarter = 'last';
       Is Correct: Yes
     ------------------------------------------------------------
     ```
   - Final accuracy:
     ```
     Accuracy: 95.00% (19/20 correct cases)
     ```

2. **Elapsed Time**:
   - Total time taken to execute the tests:
     ```
     Elapsed Time: 12.45 seconds
     ```

---

### Test Accuracy

| Metric               | Description                                      | Average Similarity (%) | Notes                                |
|----------------------|--------------------------------------------------|--------------|--------------------------------------|
| **Vector Similarity** | Measures the cosine similarity between embeddings generated for query results. | 86%       | Indicates the closeness of responses based on vector representations. |
| **Text Similarity**   | Evaluates the textual overlap and semantic closeness between the expected and actual query using `SequenceMatcher`. | 75%       | Uses the `SequenceMatcher` library to calculate similarity ratios. |

### Notes:
- **Vector Similarity**: High accuracy here implies the model effectively understands and matches the contextual meaning of user queries.
- **Text Similarity**: Calculated using Python's `difflib.SequenceMatcher` library, which computes a similarity ratio by comparing the sequence alignment of the expected and actual text.
- Results were generated using a test set containing 50 diverse queries.

