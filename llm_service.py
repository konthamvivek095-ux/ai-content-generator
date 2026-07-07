import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_content(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    prompt = "Write a 150-word blog about Artificial Intelligence."

    result = generate_content(prompt)

    print(result)