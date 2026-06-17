#!/usr/bin/env python3
"""Minimal DPO alignment — preference pairs without a separate reward model."""
from datasets import load_dataset
from peft import LoraConfig
from trl import DPOConfig, DPOTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE = "meta-llama/Llama-3.2-1B-Instruct"
DATA = "Anthropic/hh-rlhf"  # chosen / rejected columns

tokenizer = AutoTokenizer.from_pretrained(BASE)
model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype="auto", device_map="auto")
ref = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype="auto", device_map="auto")

peft = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM")

ds = load_dataset(DATA, split="train[:500]")

cfg = DPOConfig(
    output_dir="./dpo-out",
    beta=0.1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=1,
    learning_rate=5e-5,
    bf16=True,
)

trainer = DPOTrainer(
    model=model,
    ref_model=ref,
    args=cfg,
    train_dataset=ds,
    processing_class=tokenizer,
    peft_config=peft,
)
trainer.train()
