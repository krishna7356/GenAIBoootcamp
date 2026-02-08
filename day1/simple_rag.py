import faiss
from openai import OpenAI
import os
import numpy as np
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

try:
    with open("data.txt","r",encoding="utf-8") as file:
        data = file.read()
    # print(data)
except FileNotFoundError:
    print("data.txt not found. Please make sure the file exists in the same directory as this script.")

data = data.replace("\n", " ")

def chunk_text(text, size=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size):
        chunks.append(" ".join(words[i:i+size]))
    return chunks


chunked_data = chunk_text(data, size=200)

embeddings = []

for idx, chunk in enumerate(chunked_data):
      response = client.embeddings.create(
           input=chunk,
           model="text-embedding-3-small"
      )
      embedding = response.data[0].embedding
      embeddings.append(embedding)

if not embeddings:
    raise ValueError("No embeddings created")


dimensions = len(embeddings[0])


vectors  = np.array(embeddings).astype("float32")

faiss.normalize_L2(vectors)

index = index = faiss.IndexFlatIP(dimensions)

index.add(vectors)

print("vectors in faiss index:", index.ntotal)


user_input = input("Enter your query: ")

response = client.embeddings.create(
    input=user_input,
    model="text-embedding-3-small"
)
query_embedding =  response.data[0].embedding

k = 3

query_vector = np.array([query_embedding]).astype("float32")



distances, indices = index.search(query_vector,k)

retrived_chunks = [chunked_data[i] for i in indices[0]]

for i,chunks in enumerate(retrived_chunks):
    print(f"Chunk {i+1}: {chunks}\n")


context = "\n".join(retrived_chunks)

prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{user_input}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You answer using only the given context."},
        {"role": "user", "content": prompt}
    ]
)

print("Answer:", response.choices[0].message.content)