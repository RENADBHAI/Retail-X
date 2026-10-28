from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    ".env.example",
    "pyproject.toml",
    "server.py",
    "backend/retail_mcp.py",
    "AGENTS.md",
    "dist/index.html",
    "evals/tasks.jsonl",
    "evals/eval_A.csv",
    "evals/eval_B.csv",
]
missing = [p for p in required if not (ROOT / p).exists()]
assert not missing, f"Missing required files: {missing}"

lines = [line for line in (ROOT / "evals/tasks.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(lines) >= 15, f"Expected at least 15 eval tasks, found {len(lines)}"
for line in lines:
    json.loads(line)

print("PASS: required files are present")
print(f"PASS: {len(lines)} evaluation tasks found")
print("Next: copy .env.example to .env, add OPENROUTER_API_KEY, then run `uv run server.py`.")