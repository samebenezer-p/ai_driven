
import ollama
import re


def generate_function():
    prompt = """
    Write a Python function named count_vowels(s).
    It should count the number of vowels in a given string.
    Return only the Python function.
    """

    response = ollama.generate(
        model="qwen2.5-coder:7b",
        prompt=prompt
    )

    code = response["response"].strip()
    code = re.sub(r"```python|```", "", code).strip()
    code = code[code.find("def count_vowels("):]
    code = code.split("\nThis function")[0].strip()
    return code


def test_function(code):
    namespace = {}

    try:
        exec(code, namespace)
        count_vowels = namespace["count_vowels"]

        test_cases = [
            ("hello", 2),
            ("python", 1),
            ("education", 5),
            ("apple", 2),
            ("sky", 0)
        ]

        passed = 0

        print("\nTesting Vowel Count")
        print("-------------------------")

        for s, expected in test_cases:
            result = count_vowels(s)

            if result == expected:
                print("PASS")
                passed += 1
            else:
                print("FAIL")

        print("\nTest Cases Passed:", passed, "/", len(test_cases))

    except Exception as e:
        print("Error:", e)


print("Count Vowels Ollama Code Generator")

generated_code = generate_function()

print("\nGenerated Function:")
print(generated_code)

test_function(generated_code)
