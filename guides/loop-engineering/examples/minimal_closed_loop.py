#!/usr/bin/env python3
"""Minimal closed-loop coding agent — act, observe, retry until tests pass."""
from __future__ import annotations

MAX_ITER = 8

GOAL = "All unit tests pass with zero lint errors."

def run_tests() -> tuple[bool, str]:
    """Replace with pytest/subprocess in real projects."""
    import random
    ok = random.random() > 0.6  # demo: flaky until loop converges
    return ok, "FAILED: test_addition expected 4 got 3" if not ok else "OK: 12 passed"

def agent_step(iteration: int, last_error: str | None) -> str:
    """One LLM turn: propose a fix given feedback."""
    if last_error:
        return f"# iter {iteration}: patch based on → {last_error[:60]}"
    return f"# iter {iteration}: initial implementation"

def loop() -> None:
    error: str | None = None
    for i in range(1, MAX_ITER + 1):
        patch = agent_step(i, error)
        print(patch)
        passed, feedback = run_tests()
        print(f"  eval: {feedback}")
        if passed:
            print(f"✓ {GOAL} (stopped at iteration {i})")
            return
        error = feedback
    print(f"✗ Escalate to human — no progress in {MAX_ITER} iterations")

if __name__ == "__main__":
    loop()
