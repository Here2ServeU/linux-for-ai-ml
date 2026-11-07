#!/usr/bin/env python3
"""
Module 1 lab: build a small, realistic AI model server you've never seen.

    python3 make_server.py            # build ~/ai-server
    python3 make_server.py --reset    # wipe and rebuild it (practice again)
    python3 make_server.py --dir /tmp/ai-server   # build somewhere else

Sizes are scaled: 1 MB here stands for 1 GB on a real server.
Everything is deterministic, so every student sees the same numbers.

The server hides three problems:
  1. Disk     - something is eating the disk
  2. Startup  - the LLM server won't start (a path typo in a config)
  3. Duplicate - a full copy of a model file is wasting space
"""
import argparse
import random
import shutil
import sys
from pathlib import Path

KiB = 1024
MiB = 1024 * KiB
SEED = 20261101  # fixed seed -> same bytes -> same sha256 for everyone

HERE = Path(__file__).resolve().parent


def blob(path: Path, size: int, seed: int) -> None:
    """Write `size` deterministic pseudo-random bytes (fully allocated on disk)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(random.Random(seed).randbytes(size))


def text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.lstrip("\n"))


def jsonl(path: Path, size: int, seed: int) -> None:
    """A fake training dataset: one JSON record per line, about `size` bytes."""
    rng = random.Random(seed)
    words = ("linux model gpu disk file process memory token train serve "
             "loss batch epoch weight layer cuda kernel path log config").split()
    lines, total, i = [], 0, 0
    while total < size:
        sent = " ".join(rng.choice(words) for _ in range(rng.randint(8, 24)))
        line = f'{{"id": {i}, "text": "{sent}"}}\n'
        lines.append(line)
        total += len(line)
        i += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines)[:size])


def build(root: Path) -> None:
    llm_cfg = '{\n  "architecture": "LlamaForCausalLM",\n  "params": "8B",\n  "dtype": "bfloat16"\n}\n'
    tok_cfg = '{\n  "tokenizer": "bpe",\n  "vocab_size": 128256\n}\n'

    # --- models/ ------------------------------------------------------------
    # The real model (stands in for a ~17 GB bf16 checkpoint).
    model_size = 17 * MiB - 16 * KiB
    real = root / "models/llama-3-8b/model.safetensors"
    blob(real, model_size, SEED)
    text(root / "models/llama-3-8b/config.json", llm_cfg)
    text(root / "models/llama-3-8b/tokenizer.json", tok_cfg)

    # PROBLEM 3: a forgotten, byte-for-byte backup copy.
    backup = root / "models/old/llama-3-8b-backup/model.safetensors"
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(real, backup)
    text(root / "models/old/llama-3-8b-backup/config.json", llm_cfg)
    text(root / "models/old/llama-3-8b-backup/tokenizer.json", tok_cfg)

    # A small, legit embedding model (different bytes).
    blob(root / "models/embed-mini/model.safetensors", 5 * MiB - 16 * KiB, SEED + 1)
    text(root / "models/embed-mini/config.json",
         '{\n  "architecture": "BertModel",\n  "params": "33M"\n}\n')

    # --- checkpoints/ (training snapshots) ----------------------------------
    for n, step in enumerate(range(1000, 6000, 1000)):
        blob(root / f"checkpoints/run-07/step-{step}.pt", 5 * MiB - 4 * KiB, SEED + 10 + n)

    # --- datasets/ ----------------------------------------------------------
    jsonl(root / "datasets/train.jsonl", 8 * MiB, SEED + 20)
    jsonl(root / "datasets/eval.jsonl", 900 * KiB, SEED + 21)

    # --- configs/ -----------------------------------------------------------
    # PROBLEM 2: line 3 says llama3-8b, but the folder is llama-3-8b.
    text(root / "configs/serve.yaml", """
# LLM inference server
server: llm-serve
model_path: models/llama3-8b/model.safetensors
port: 8000
max_batch_size: 8
gpu: 0
""")
    text(root / "configs/train.yaml", """
# Fine-tuning job
base_model: models/llama-3-8b/model.safetensors
dataset: datasets/train.jsonl
checkpoint_dir: checkpoints/run-07
save_every: 1000
""")

    # --- logs/ --------------------------------------------------------------
    text(root / "logs/server.log", """
2026-11-01 09:14:02 INFO  llm-serve starting (pid 4182)
2026-11-01 09:14:02 INFO  reading config configs/serve.yaml
2026-11-01 09:14:02 INFO  device cuda:0 selected
2026-11-01 09:14:03 WARN  max_batch_size=8 may exceed GPU memory on small cards
2026-11-01 09:14:03 INFO  loading model weights
2026-11-01 09:14:03 ERROR model file not found: models/llama3-8b/model.safetensors
2026-11-01 09:14:03 INFO  llm-serve exited with code 1
""")

    # --- the briefing + the grader -------------------------------------------
    text(root / "README-FIRST.txt", """
Welcome to ai-server. You've never seen this machine before.

Three things are wrong. Find them before you change anything.

  Mission 1 - Disk:      What is eating the disk?        (which top-level folder?)
  Mission 2 - Startup:   Why won't the LLM server start? (which config file is wrong?)
  Mission 3 - Duplicate: Which model file is wasted space? (full path to the copy)

Rule of the house: measure, prove, then act.

When you're done, score yourself:
  bash check_answers.sh <folder> <config-file> <duplicate-file>

Sizes are scaled: 1 MB here stands for 1 GB on a real server.
""")
    shutil.copyfile(HERE / "check_answers.sh", root / "check_answers.sh")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the Module 1 practice server.")
    ap.add_argument("--dir", default=str(Path.home() / "ai-server"),
                    help="where to build it (default: ~/ai-server)")
    ap.add_argument("--reset", action="store_true",
                    help="delete the existing server and rebuild it")
    args = ap.parse_args()
    root = Path(args.dir).expanduser().resolve()

    if root.exists():
        if not args.reset:
            print(f"{root} already exists. Use --reset to rebuild it.")
            return 1
        if not (root / "README-FIRST.txt").exists():
            print(f"Refusing to delete {root}: it doesn't look like a lab server.")
            return 1
        shutil.rmtree(root)

    build(root)
    print(f"Built your server at {root}")
    print(f"Next:  cd {root} && cat README-FIRST.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
