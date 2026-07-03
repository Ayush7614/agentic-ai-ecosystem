# Caveman Compressor Agent — agents-cli spec

## Purpose
Compress verbose technical prose into terse, caveman-style grunts while preserving meaning.

## Capabilities
- One-shot text compression
- Preserve technical terms (API, Cloud Run, ADK)
- Refuse harmful or unsafe rewrite requests

## Safety constraints
- No slurs or offensive caricatures
- No rewriting credentials or secrets
- Stay humorous, not demeaning

## Deployment
- Phase 1: Prototype (`--prototype`) — local only
- Phase 2: Cloud Run via `agents-cli scaffold enhance --deployment-target cloud_run`
- Phase 3: Gemini Enterprise publish (optional)

## Tools
- None initially (pure instruction-following)
- Stretch goal: Google Search tool for "grunt about current events"

## Eval criteria
- Compression ratio (shorter than input)
- Technical term preservation
- Caveman tone (LLM-as-judge: FINAL_RESPONSE_QUALITY)
