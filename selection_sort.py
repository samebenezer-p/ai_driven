

import ollama
import ast
import re

# 1. REAL CODE DATASET
real_code_dataset = [
"""def selection_sort(arr):
    for i in range(len(arr)):
        m = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[m]:
                m = j
        arr[i], arr[m] = arr[m], arr[i]
    return arr"""
] * 10


# 2. GENERATOR
def generate_code():

    prompt = """
    Write a Python function named selection_sort(arr).
    Implement Selection Sort in ascending order.
    Find the minimum element and swap it.
    Do not use sort() or sorted().
    Return only Python code.
    """

    response = ollama.chat(
        model="codegemma:2b",
        messages=[{"role": "user", "content": prompt}]
    )

    code = response["message"]["content"].strip()
    code = re.sub(r"```python|```", "", code).strip()

    start = code.find("def selection_sort")

    if start == -1:
        return ""

    code = code[start:]

    # Remove explanation after function
    lines = code.splitlines()

    for i in range(len(lines), 0, -1):
        candidate = "\n".join(lines[:i]).strip()
        try:
            ast.parse(candidate)
            return candidate
        except SyntaxError:
            continue

    return ""


# 3. SYNTAX CHECK
def check_syntax(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


# 4. FUNCTIONAL TEST
def test_code(code):

    namespace = {}

    try:
        exec(code, namespace)
        selection_sort = namespace["selection_sort"]

        tests = [
            ([5, 3, 8, 4, 2], [2, 3, 4, 5, 8]),
            ([10, 1, 7, 3], [1, 3, 7, 10]),
            ([5, 5, 2, 1], [1, 2, 5, 5]),
            ([9, 8, 7, 6], [6, 7, 8, 9]),
            ([1], [1]),
            ([], [])
        ]

        for arr, expected in tests:
            if selection_sort(arr.copy()) != expected:
                return False

        return True

    except Exception as e:
        print("Execution Error:", e)
        return False


# 5. ALGORITHM CHECK
def check_algorithm(code):

    code = code.lower()

    return (
        "def selection_sort" in code
        and ("for" in code or "while" in code)
        and "if" in code
        and ("<" in code or ">" in code)
        and any(x in code for x in ["min", "minimum", "smallest"])
        and ".sort(" not in code
        and "sorted(" not in code
    )


# 6. SIMILARITY CHECK
def calculate_similarity(code):

    tokens = set(re.findall(r"\w+", code.lower()))
    best = 0

    for real in real_code_dataset:
        real_tokens = set(re.findall(r"\w+", real.lower()))
        union = tokens | real_tokens

        if union:
            similarity = len(tokens & real_tokens) / len(union)
            best = max(best, similarity)

    return round(best * 100, 2)


# 7. DISCRIMINATOR
def discriminator(code):

    syntax = check_syntax(code)

    if not syntax:
        return 0

    functional = test_code(code)
    algorithm = check_algorithm(code)
    similarity = calculate_similarity(code)

    score = (
        20
        + (40 if functional else 0)
        + (20 if algorithm else 0)
        + (similarity * 0.20)
    )

    print("\nDISCRIMINATOR RESULT")
    print("Syntax:", syntax)
    print("Functional:", functional)
    print("Algorithm:", algorithm)
    print("Similarity:", similarity, "%")
    print("Final Score:", round(score, 2), "/ 100")

    return score


# 8. MAIN PROGRAM
print("=" * 50)
print("CODEGEMMA - SELECTION SORT")
print("=" * 50)

print("Real Dataset Size:", len(real_code_dataset))

generated_code = generate_code()

print("\nGENERATED CODE:")
print(generated_code)

if generated_code:
    score = discriminator(generated_code)

    if score >= 80:
        print("\nRESULT: ACCEPTED")
    else:
        print("\nRESULT: REJECTED")
else:
    print("\nCodeGemma failed to generate valid code.")

#Exercise 2 – GAN Implementation (CodeGemma)
#ollama pull codegemma:2b
#pip install ollama
#python selection_sort.py
#python insertion_sort.py