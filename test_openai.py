from openai_service import generate_test_cases

result = generate_test_cases(
    "User login using email and password."
)

print(result)