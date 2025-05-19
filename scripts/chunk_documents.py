# Placeholder chunk script
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

INPUT_DIR = "data/raw/"
OUTPUT_DIR = "data/processed/"

def chunk_docs():
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)

    for file_name in os.listdir(INPUT_DIR):
        with open(os.path.join(INPUT_DIR, file_name), "r") as f:
            text = f.read()
        chunks = splitter.split_text(text)
        out_file = os.path.join(OUTPUT_DIR, file_name.replace(".txt", "_chunks.txt"))
        with open(out_file, "w") as f:
            f.write("\n---\n".join(chunks))
        print(f"Chunked {file_name}")

if __name__ == "__main__":
    chunk_docs()
