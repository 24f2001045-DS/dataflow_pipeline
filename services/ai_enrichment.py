from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enrich_uuid(uuid_value):
    prompt = f"""
    Analyze this UUID: {uuid_value}.
    Provide 2-3 observations.
    Classify sentiment as positive, negative, or neutral.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = response.choices[0].message.content

    sentiment = "neutral"
    if "positive" in text.lower():
        sentiment = "positive"
    elif "negative" in text.lower():
        sentiment = "negative"

    return text, sentiment
