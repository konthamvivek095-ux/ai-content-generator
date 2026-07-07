from scraper import extract_content
from prompt_builder import build_prompt
from llm_service import generate_content

url = input("Enter URL: ")

print("\nExtracting content...")

data = extract_content(url)

title = data["title"]
content = data["content"]

print("Content extracted successfully!")
print(f"Title: {title}")

print("\nBuilding prompt...")

prompt = build_prompt(
    title=title,
    content=content[:5000],  # Limit content size
    audience="Data Scientists",
    style="Professional",
    word_count=500
)

print("Prompt created!")

print("\nGenerating article with Gemini...")

article = generate_content(prompt)

print("\n" + "=" * 60)
print("GENERATED ARTICLE")
print("=" * 60)
print(article)