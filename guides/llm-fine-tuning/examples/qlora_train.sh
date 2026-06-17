#!/usr/bin/env bash
# QLoRA one-liner via HuggingFace TRL (requires bitsandbytes + CUDA)
set -euo pipefail

MODEL="${MODEL:-meta-llama/Llama-3.2-3B-Instruct}"
DATA="${DATA:-yahma/alpaca-cleaned}"

trl sft \
  --model_name_or_path "$MODEL" \
  --dataset_name "$DATA" \
  --dataset_train_split train[:1000] \
  --load_in_4bit \
  --bnb_4bit_quant_type nf4 \
  --bnb_4bit_compute_dtype bfloat16 \
  --use_peft \
  --lora_r 16 \
  --lora_alpha 32 \
  --target_modules q_proj v_proj \
  --output_dir ./qlora-out \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 16 \
  --num_train_epochs 1 \
  --bf16
