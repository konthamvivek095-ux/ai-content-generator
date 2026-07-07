def build_prompt(title, content, audience, style, word_count):
    prompt = f"""
You are a professional content writer.

Write a blog article based on the information below.

Target Audience: {audience}
Writing Style: {style}
Word Count: {word_count}

Article Title:
{title}

Source Content:
{content}

Requirements:
- Use clear headings.
- Keep the content engaging.
- Do not copy the source content word-for-word.
- Create an original article.
"""

    return prompt
if __name__ == "__main__":
    prompt = build_prompt(
        "Artificial Intelligence",
        "Artificial intelligence is transforming industries.",
        "Data Scientists",
        "Professional",
        500
    )

    print(prompt)