
import ollama
import re


def generate_function():
    prompt = """
    Write a Python function named is_palindrome(n).
    It should check whether a given number is a palindrome or not.
    Return only the Python function.
    """

    response = ollama.generate(
        model="qwen2.5-coder:7b",
        prompt=prompt
    )

    code = response["response"].strip()
    code = re.sub(r"```python|```", "", code).strip()
    code = code[code.find("def is_palindrome("):]
    code = code.split("\n\nThis function")[0].strip()
    return code

def test_function(code):
    namespace = {}

    try:
        exec(code, namespace)
        is_palindrome = namespace["is_palindrome"]

        test_cases = [
            (121, True),
            (123, False),
            (1221, True),
            (0, True),
            (12321, True)
        ]

        passed = 0

        print("\nTesting Palindrome Numbers")
        print("-------------------------")

        for n, expected in test_cases:
            result = is_palindrome(n)

            if result == expected:
                print("PASS")
                passed += 1
            else:
                print("FAIL")

        print("\nTest Cases Passed:", passed, "/", len(test_cases))

    except Exception as e:
        print("Error:", e)


print("Palindrome Number Ollama Code Generator")

generated_code = generate_function()

print("\nGenerated Function:")
print(generated_code)

test_function(generated_code)
