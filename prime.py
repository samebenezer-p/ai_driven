
import ollama
import re


def generate_function():
    prompt = """
    Write a Python function named is_prime(n).
    It should check whether a given number is prime or not.
    Return only the Python function.
    """

    response = ollama.generate(
        model="qwen2.5-coder:7b",
        prompt=prompt
    )

    code = response["response"].strip()
    code = re.sub(r"```python|```", "", code).strip()
    code = code[code.find("def is_prime("):]
    return code


def test_function(code):
    namespace = {}

    try:
        exec(code, namespace)
        is_prime = namespace["is_prime"]

        test_cases = [
            (7, True),
            (4, False),
            (13, True),
            (1, False),
            (2, True)
        ]

        passed = 0

        print("\nTesting Prime Numbers")
        print("-------------------------")

        for n, expected in test_cases:
            result = is_prime(n)

            if result == expected:
                print("PASS")
                passed += 1
            else:
                print("FAIL")

        print("\nTest Cases Passed:", passed, "/", len(test_cases))

    except Exception as e:
        print("Error:", e)


print("Prime Number Ollama Code Generator")

generated_code = generate_function()

print("\nGenerated Function:")
print(generated_code)

test_function(generated_code)
