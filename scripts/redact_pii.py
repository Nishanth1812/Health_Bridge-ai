# Placeholder PII redaction script
import re
import os

INPUT_DIR = "data/processed/"
OUTPUT_DIR = "data/processed/"

def redact_text(text):
    text = re.sub(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b", "[REDACTED_NAME]", text)
    text = re.sub(r"\b[\w.-]+@[\w.-]+\.\w+\b", "[REDACTED_EMAIL]", text)
    return text

def redact_files():
    for file_name in os.listdir(INPUT_DIR):
        with open(os.path.join(INPUT_DIR, file_name), "r") as f:
            text = f.read()
        redacted = redact_text(text)
        with open(os.path.join(OUTPUT_DIR, file_name), "w") as f:
            f.write(redacted)
        print(f"Redacted {file_name}")

if __name__ == "__main__":
    redact_files()
