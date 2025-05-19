# Placeholder embeddings generation script
from transformers import AutoTokenizer, AutoModel
import torch
import os

MODEL_NAME = "path/to/your/finetuned/pubmedbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

PROCESSED_DIR = "data/processed/"
EMBEDDINGS_OUTPUT = "data/synthetic/embeddings.pt"

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze()

def generate_all_embeddings():
    embeddings = {}
    for fname in os.listdir(PROCESSED_DIR):
        with open(os.path.join(PROCESSED_DIR, fname), "r") as f:
            text = f.read()
        chunks = text.split("\n---\n")
        for i, chunk in enumerate(chunks):
            emb = get_embedding(chunk)
            embeddings[f"{fname}_{i}"] = emb
    torch.save(embeddings, EMBEDDINGS_OUTPUT)
    print(f"Saved embeddings to {EMBEDDINGS_OUTPUT}")

if __name__ == "__main__":
    generate_all_embeddings()
