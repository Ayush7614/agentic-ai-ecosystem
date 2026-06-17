# LLM Fine-Tuning — Visual Guide

Original guide to **adapting language models** — when to fine-tune, parameter-efficient methods (LoRA, QLoRA), alignment (RLHF, DPO, GRPO), and hands-on HuggingFace walkthroughs.

**References (not copies):** [Daily Dose of Data — LLMOps Part 12](https://www.dailydoseofds.com/) · [Cloud Girl — 15 techniques](https://priyankavergadia.substack.com/p/15-llm-fine-tuning-techniques-you)

## What you'll learn

- **Adaptation ladder** — prompt → RAG → fine-tune → align  
- **Five families** — full SFT, soft prompts, PEFT, alignment, federated  
- **LoRA & QLoRA** — math intuition, NF4, merge vs hot-swap  
- **RLHF, DPO, GRPO** — when each fits  
- Runnable **PEFT + TRL** examples

![Fine-tuning landscape](./assets/diagram-landscape.gif)

**Blog mega-GIF:** [mega-finetune-everything.gif](./assets/mega-finetune-everything.gif)

## Quick start

```bash
pip install "transformers>=4.44" peft accelerate datasets bitsandbytes trl
cd guides/llm-fine-tuning
python examples/lora_train.py   # LoRA SFT (GPU recommended)
```

## Guide map

- **[Full tutorial](./TUTORIAL.md)** — Parts 1–17 with GIFs  
- **[Examples](./examples/)** — LoRA, QLoRA shell, DPO scripts  
- **[Assets](./assets/)** — diagram + terminal GIFs, blog poster  

## Related guides

- [ML Model 10 Steps](../ml-model-6-steps/) — classical ML lifecycle visuals  
- [OpenClaw](../openclaw/) · [Hermes masterclass](../hermes-agent-masterclass/) — agent deployment after you have a model  
- [Gemma 4 12B](../gemma-4-12b/) — open-weight model + agent frameworks  

**Blog header:** `assets/blog-poster-1200x600.png` · Regenerate: `cd assets && python3 render_blog_poster.py`

## License

Guide: MIT · Upstream libraries: respective licenses
