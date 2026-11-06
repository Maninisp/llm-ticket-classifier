import ollama
import json

user_text = input("Enter a customer complaint: ")

prompt = """
You are a customer-support text analyzer.

Analyze the customer's complaint and return JSON with exactly these fields:
category, priority, sentiment, summary.

Be concise and do not invent information.
"""

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": user_text,
        },
    ],
)

content = response.message.content
print(type(content))

# print(content)
content = content.replace("```json", "").replace("```", "").strip()

data = json.loads(content)

print(type(data))
# print("\n--- Ticket Analysis ---")
# print(f"Category: {data['category']}")
# print(f"Priority: {data['priority']}")
# print(f"Sentiment: {data['sentiment']}")
# print(f"Summary: {data['summary']}")

# required_fields = ["category", "priority", "sentiment", "summary"]

# missing_fields = []

# for field in required_fields:
#     if field not in data:
#         missing_fields.append(field)

# if missing_fields:
#     print("Missing fields:", missing_fields)
# else:
#     pass

# if data["priority"].lower() == "high":
#     print("⚠️ Action: Escalate this ticket.")
# else:
#     print("Action: Normal processing.")

# print(data)