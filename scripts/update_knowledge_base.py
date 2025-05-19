# Placeholder KB update script
import torch
import os
import faiss

EMBEDDING_FILE = "data/synthetic/embeddings.pt"

def update_vector_store():
    embeddings = torch.load(EMBEDDING_FILE)
    dim = next(iter(embeddings.values())).shape[0]
    index = faiss.IndexFlatL2(dim)

    id_map = []
    for i, (k, emb) in enumerate(embeddings.items()):
        index.add(emb.unsqueeze(0).numpy())
        id_map.append(k)

    faiss.write_index(index, "data/synthetic/knowledge_base.index")
    with open("data/synthetic/id_map.txt", "w") as f:
        for id in id_map:
            f.write(id + "\n")
    print("Knowledge base updated")

if __name__ == "__main__":
    update_vector_store()
