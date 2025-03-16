from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

token = ""
MODEL_NAME = "Qwen/Qwen1.5-1.3B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=token)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto", torch_dtype=torch.float16, token=token)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
