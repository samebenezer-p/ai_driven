
import ollama
import ast
import re
import sys

# ============================================================
# 1. REAL CODE DATASET
# ============================================================

selection_dataset = [
"""def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr""",

"""def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):
        minimum = i
        for j in range(i+1, n):
            if arr[j] < arr[minimum]:
                minimum = j
        arr[i], arr[minimum] = arr[minimum], arr[i]
    return arr""",

"""def selection_sort(arr):
    for i in range(len(arr)-1):
        smallest = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[smallest]:
                smallest = j
        arr[i], arr[smallest] = arr[smallest], arr[i]
    return arr""",

"""def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr""",

"""def selection_sort(arr):
    for i in range(len(arr)):
        minimum = arr[i]
        index = i
        for j in range(i+1, len(arr)):
            if arr[j] < minimum:
                minimum = arr[j]
                index = j
        arr[i], arr[index] = arr[index], arr[i]
    return arr""",

"""def selection_sort(arr):
    n = len(arr)
    i = 0
    while i < n-1:
        min_idx = i
        j = i+1
        while j < n:
            if arr[j] < arr[min_idx]:
                min_idx = j
            j += 1
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        i += 1
    return arr""",

"""def selection_sort(arr):
    for i in range(len(arr)-1):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr""",

"""def selection_sort(arr):
    result = arr.copy()
    for i in range(len(result)):
        m = i
        for j in range(i+1, len(result)):
            if result[j] < result[m]:
                m = j
        result[i], result[m] = result[m], result[i]
    return result""",

"""def selection_sort(arr):
    for i in range(len(arr)):
        min_pos = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_pos]:
                min_pos = j
        arr[i], arr[min_pos] = arr[min_pos], arr[i]
    return arr""",

"""def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if i != min_idx:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr"""
]

insertion_dataset = [
"""def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr""",

"""def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        current = arr[i]
        j = i-1
        while j >= 0 and arr[j] > current:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = current
    return arr""",

"""def insertion_sort(arr):
    for i in range(1, len(arr)):
        value = arr[i]
        j = i-1
        while j >= 0:
            if arr[j] > value:
                arr[j+1] = arr[j]
                j -= 1
            else:
                break
        arr[j+1] = value
    return arr""",

"""def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i
        while j > 0 and arr[j-1] > key:
            arr[j] = arr[j-1]
            j -= 1
        arr[j] = key
    return arr""",

"""def insertion_sort(arr):
    n = len(arr)
    i = 1
    while i < n:
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
        i += 1
    return arr""",

"""def insertion_sort(arr):
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i-1
        while j >= 0 and result[j] > key:
            result[j+1] = result[j]
            j -= 1
        result[j+1] = key
    return result""",

"""def insertion_sort(arr):
    for i in range(1, len(arr)):
        temp = arr[i]
        j = i-1
        while j >= 0:
            if arr[j] <= temp:
                break
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = temp
    return arr""",

"""def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0:
            if arr[j] > key:
                arr[j+1] = arr[j]
                j -= 1
            else:
                break
        arr[j+1] = key
    return arr""",

"""def insertion_sort(arr):
    for i in range(1, len(arr)):
        current = arr[i]
        position = i
        while position > 0 and arr[position-1] > current:
            arr[position] = arr[position-1]
            position -= 1
        arr[position] = current
    return arr""",

"""def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        item = arr[i]
        j = i-1
        while j >= 0 and arr[j] > item:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = item
    return arr"""
]


# ============================================================
# 2. CODEGEMMA GENERATOR
# ============================================================

def generate_code(algorithm):

    function_name = algorithm + "_sort"

    if algorithm == "selection":

        instructions = """
Implement SELECTION SORT:
1. Use an outer loop to select each position.
2. Find the smallest element in the remaining unsorted list.
3. Use an inner loop to find its index.
4. Swap the smallest element into the selected position.
"""

    else:

        instructions = """
Implement INSERTION SORT:
1. Start the outer loop from index 1.
2. Store the current element in a variable named key.
3. Compare key with previous elements.
4. Shift larger elements one position to the right.
5. Insert key into its correct position.
"""

    prompt = f"""
Write a complete and correct Python function.

The function MUST be named exactly:
def {function_name}(arr):

{instructions}

Requirements:
- Sort numbers in ascending order.
- Return the sorted list.
- Do not use sort() or sorted().
- Do not import modules.
- Do not write explanations.
- Do not write Markdown.
- Output only executable Python code.

Example output format:

def {function_name}(arr):
    # implementation
    return arr

Now generate the complete function.
"""

    for attempt in range(1, 4):

        try:

            print(f"\nGeneration attempt: {attempt}/3")

            response = ollama.chat(
                model="codegemma:2b",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                options={
                    "temperature": 0,
                    "num_predict": 400
                }
            )

            raw_code = response["message"]["content"]

            print("CodeGemma response received.")

            # Remove Markdown
            code = re.sub(
                r"```(?:python)?",
                "",
                raw_code,
                flags=re.IGNORECASE
            )

            # Find a Python function
            match = re.search(
                r"(?m)^def\s+([a-zA-Z_]\w*)\s*\(",
                code
            )

            if not match:

                print("No Python function found. Retrying...")
                continue

            original_name = match.group(1)

            # Extract function from response
            code = code[match.start():]

            lines = code.splitlines()
            cleaned_lines = []

            for line in lines:

                if not cleaned_lines:
                    cleaned_lines.append(line)
                    continue

                if line.startswith((" ", "\t")) or line.strip() == "":
                    cleaned_lines.append(line)
                else:
                    break

            code = "\n".join(cleaned_lines).strip()

            # Correct function name
            code = re.sub(
                r"(?m)^def\s+" + re.escape(original_name) + r"\s*\(",
                "def " + function_name + "(",
                code,
                count=1
            )

            # Validate syntax
            try:

                ast.parse(code)

                print("Valid Python function generated.")
                return code

            except SyntaxError:

                print("Invalid syntax. Retrying...")

        except Exception as e:

            print("CodeGemma Error:", e)
            break

    print("CodeGemma could not generate a valid function.")
    return ""


# ============================================================
# 3. SYNTAX CHECK
# ============================================================

def check_syntax(code):

    try:
        ast.parse(code)
        return True

    except SyntaxError:
        return False


# ============================================================
# 4. FUNCTIONAL TEST
# ============================================================

def test_sort(code, algorithm):

    namespace = {}

    try:

        exec(code, namespace)

        function_name = algorithm + "_sort"

        if function_name not in namespace:
            return False

        sorting_function = namespace[function_name]

        test_cases = [
            ([5, 3, 8, 4, 2], [2, 3, 4, 5, 8]),
            ([10, 1, 7, 3], [1, 3, 7, 10]),
            ([5, 5, 2, 1], [1, 2, 5, 5]),
            ([9, 8, 7, 6], [6, 7, 8, 9]),
            ([1], [1]),
            ([], []),
            ([3, -1, 0, -5], [-5, -1, 0, 3]),
            ([2, 1, 2, 1], [1, 1, 2, 2])
        ]

        for data, expected in test_cases:

            result = sorting_function(data.copy())

            if result != expected:
                return False

        return True

    except Exception:
        return False


# ============================================================
# 5. ALGORITHM CHECK
# ============================================================

def check_algorithm(code, algorithm):

    code_lower = code.lower()

    if ".sort(" in code_lower or "sorted(" in code_lower:
        return False

    try:

        tree = ast.parse(code)

        function_name = algorithm + "_sort"

        functions = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
            and node.name == function_name
        ]

        if not functions:
            return False

        function = functions[0]

        loops = [
            node for node in ast.walk(function)
            if isinstance(node, (ast.For, ast.While))
        ]

        comparisons = [
            node for node in ast.walk(function)
            if isinstance(node, ast.Compare)
        ]

        assignments = [
            node for node in ast.walk(function)
            if isinstance(node, (ast.Assign, ast.AugAssign))
        ]

        if algorithm == "selection":

            nested_loops = False

            for outer in loops:

                for inner in ast.walk(outer):

                    if inner is not outer and isinstance(
                        inner, (ast.For, ast.While)
                    ):
                        nested_loops = True
                        break

                if nested_loops:
                    break

            return nested_loops and len(comparisons) > 0

        else:

            has_key = any(
                isinstance(node, ast.Name)
                and node.id.lower() in
                ["key", "current", "value", "item", "temp"]
                for node in ast.walk(function)
            )

            return (
                len(loops) >= 2
                and len(comparisons) > 0
                and len(assignments) >= 2
                and has_key
            )

    except Exception:
        return False


# ============================================================
# 6. SIMILARITY CALCULATION
# ============================================================

def calculate_similarity(generated_code, dataset):

    generated_tokens = set(
        re.findall(r"[a-zA-Z_]+", generated_code.lower())
    )

    if not generated_tokens:
        return 0

    best_similarity = 0

    for real_code in dataset:

        real_tokens = set(
            re.findall(r"[a-zA-Z_]+", real_code.lower())
        )

        common = generated_tokens.intersection(real_tokens)
        union = generated_tokens.union(real_tokens)

        similarity = len(common) / len(union) if union else 0

        best_similarity = max(best_similarity, similarity)

    return round(best_similarity * 100, 2)


# ============================================================
# 7. DISCRIMINATOR
# ============================================================

def discriminator(code, algorithm, dataset):

    syntax = check_syntax(code)

    if not syntax:

        return {
            "syntax": False,
            "functional": False,
            "algorithm": False,
            "similarity": 0,
            "score": 0
        }

    functional = test_sort(code, algorithm)

    algorithm_check = check_algorithm(code, algorithm)

    similarity = calculate_similarity(code, dataset)

    score = 0

    if syntax:
        score += 20

    if functional:
        score += 40

    if algorithm_check:
        score += 20

    score += similarity * 0.20

    return {
        "syntax": syntax,
        "functional": functional,
        "algorithm": algorithm_check,
        "similarity": similarity,
        "score": round(score, 2)
    }


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

if len(sys.argv) < 2 or sys.argv[1].lower() not in [
    "selection", "insertion"
]:

    print("Usage: python gan_sort.py selection")
    print("       python gan_sort.py insertion")
    sys.exit(1)


algorithm = sys.argv[1].lower()

if algorithm == "selection":
    dataset = selection_dataset
else:
    dataset = insertion_dataset


print("\nCODEGEMMA SORT GENERATION")
print("Algorithm:", algorithm.title(), "Sort")
print("Real Dataset Size:", len(dataset))


generated_code = generate_code(algorithm)


print("\nGENERATED PYTHON CODE")
print("-" * 35)

if generated_code:
    print(generated_code)
else:
    print("No valid function generated.")


# Discriminator evaluation

if generated_code:

    result = discriminator(
        generated_code,
        algorithm,
        dataset
    )

else:

    result = {
        "syntax": False,
        "functional": False,
        "algorithm": False,
        "similarity": 0,
        "score": 0
    }


print("\nDISCRIMINATOR RESULT")
print("Syntax     :", result["syntax"])
print("Functional :", result["functional"])
print("Algorithm  :", result["algorithm"])
print("Similarity :", result["similarity"], "%")
print("Final Score:", result["score"], "/ 100")


if result["score"] >= 80:
    print("\nRESULT: ACCEPTED")
else:
    print("\nRESULT: REJECTED")


#ollama pull codegemma:2b
#pip install ollama
#ollama list
# python gan_sort.py selection
# python gan_sort.py insertion    
