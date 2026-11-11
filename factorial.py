
import ollama
import re


def generate_function():
    prompt = """
    Write a Python function named factorial(n).
    It should calculate the factorial of a number.
    Return only the Python function.
    """

    response = ollama.generate(
        model="qwen2.5-coder:7b",
        prompt=prompt
    )

    code = response["response"].strip()
    code = re.sub(r"```python|```", "", code).strip()
    code = code[code.find("def factorial("):]
    return code


def test_function(code):
    namespace = {}

    try:
        exec(code, namespace)
        factorial = namespace["factorial"]

        test_cases = [
            (5, 120),
            (4, 24),
            (3, 6),
            (0, 1),
            (1, 1)
        ]

        passed = 0

        print("\nTesting Factorial Numbers")
        print("-------------------------")

        for n, expected in test_cases:
            result = factorial(n)

            if result == expected:
                print("PASS")
                passed += 1
            else:
                print("FAIL")

        print("\nTest Cases Passed:", passed, "/", len(test_cases))

    except Exception as e:
        print("Error:", e)


print("Factorial Ollama Code Generator")

generated_code = generate_function()

print("\nGenerated Function:")
print(generated_code)

test_function(generated_code)
