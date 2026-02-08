from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

while True:
    query = input("you: ")

    if query.lower() in ["exit", "quit"]:
        print("Exiting the chat")
        break
    
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role":"system","content":"your helpfull and wise assistant and always answer in a concise manner"},
            {"role":"user","content":query}
        ]
    )
    print("bot:", response.choices[0].message.content)