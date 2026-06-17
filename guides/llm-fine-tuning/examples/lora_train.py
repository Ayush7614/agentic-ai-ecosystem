#!/usr/bin/env python3
"""Minimal LoRA SFT example — Llama-class model + PEFT."""
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

BASE = "meta-llama/Llama-3.2-1B-Instruct"  # swap for your model
DATA = "yahma/alpaca-cleaned"              # instruction dataset

tokenizer = AutoTokenizer.from_pretrained(BASE)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype="auto", device_map="auto")

lora = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora)
model.print_trainable_parameters()  # ~0.1–1% of base

ds = load_dataset(DATA, split="train[:2000]")

def format_row(row):
    text = f"### Instruction:\n{row['instruction']}\n\n### Response:\n{row['output']}"
    return tokenizer(text, truncation=True, max_length=512)

ds = ds.map(format_row, remove_columns=ds.column_names)

args = TrainingArguments(
    output_dir="./lora-out",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    num_train_epochs=1,
    learning_rate=2e-4,
    logging_steps=10,
    save_strategy="epoch",
    bf16=True,
)

Trainer(model=model, args=args, train_dataset=ds, data_collator=lambda b: tokenizer.pad(
    b, return_tensors="pt", padding=True
)).train()

model.save_pretrained("./lora-out/adapter")
