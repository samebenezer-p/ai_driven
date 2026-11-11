
import ollama
import re


def generate_function():
    prompt = """
    Write a Python function named sum_even(arr).
    It should find the sum of all even numbers in a given array.
    Return only the Python function.
    """

    response = ollama.generate(
        model="qwen2.5-coder:7b",
        prompt=prompt
    )

    code = response["response"].strip()
    code = re.sub(r"```python|```", "", code).strip()
    code = code[code.find("def sum_even("):]
    code = code.split("\nThis function")[0].strip()
    return code


def test_function(code):
    namespace = {}

    try:
        exec(code, namespace)
        sum_even = namespace["sum_even"]

        test_cases = [
            ([1, 2, 3, 4, 5, 6], 12),
            ([2, 4, 6, 8], 20),
            ([1, 3, 5], 0),
            ([10, 15, 20], 30),
            ([0, 2, 4], 6)
        ]

        passed = 0

        print("\nTesting Sum of Even Numbers")
        print("-------------------------")

        for arr, expected in test_cases:
            result = sum_even(arr)

            if result == expected:
                print("PASS")
                passed += 1
            else:
                print("FAIL")

        print("\nTest Cases Passed:", passed, "/", len(test_cases))

    except Exception as e:
        print("Error:", e)


print("Sum of Even Numbers Ollama Code Generator")

generated_code = generate_function()

print("\nGenerated Function:")
print(generated_code)

test_function(generated_code)
