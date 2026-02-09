import os
import faiss
import numpy as np
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_knowledge_base(file_path):
    with open(file_path,'r',encoding='utf-8') as file:
        return file.read()
    
def chunk_text(text, chunk_size=200, overlap=30):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

text = load_knowledge_base("/data/company_docs.txt")
chunks = chunk_text(text)
# print(f"Loaded {len(chunks)} chunks")

if not chunks:
    raise ValueError("No chunks created")

embeddings= []

for chunk in chunks:
    response = client.embeddings.create(
        input=chunk,
        model="text-embedding-3-small"
    )
    embeddings.append(response.data[0].embedding)

vectors = np.array(embeddings).astype('float32')
faiss.normalize_L2(vectors)

index = faiss.IndexFlatIP(len(vectors[0]))
index.add(vectors)

print("index chunks added to faiss index",index.ntotal)

query = input("Enter your query: ")
response = client.embeddings.create(input=query, model = "text-embedding-3-small")
query_vector = np.array(response.data[0].embedding).astype('float32').reshape(1, -1)
faiss.normalize_L2(query_vector)
k=3
distances, indices = index.search(query_vector, k)

print("Top 3 relevant chunks:")
context = "\n".join([chunks[i] for i in indices[0]])
print(context)

prompt = f"Answer the question based on the following context:\n{context}\nQuestion: {query}\nAnswer:"
response= client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role":"system","content":"You are a helpful assistant that answers questions based on the provided context."},
        {"role":"user","content":prompt}
    ])

print("Answer:",response.choices[0].message.content.strip())