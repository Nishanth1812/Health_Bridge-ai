from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from huggingface_hub import login
login("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")
model_id = "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract"  # Replace with your fine-tuned model ID

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForQuestionAnswering.from_pretrained(model_id)
