# SDAIA Capstone Requirement Matrix

| Requirement | Status | Evidence |
|---|---|---|
| Multi-step agent | PASS | Notebook 03 and final UI workflow |
| At least 3 tools | PASS | Identity, order, product, policy tools |
| At least 1 MCP tool | PASS | `backend/retail_mcp.py`, Notebook 04 |
| Context file / spec | PASS | `AGENTS.md`, Notebook 05 |
| Memory or retrieval | PASS | BM25 policy retrieval, Notebook 02 |
| Compaction or budget rule | PASS | Context compaction + tool-result cap, Notebook 05 |
| Permission policy | PASS | Read allow / write approval, Notebooks 04–05 |
| Human approval for write | PASS | `cancel_pending_order`, Notebook 04 and UI demo |
| Step/cost budgets | PASS | 8 steps / $0.05, Notebook 05 |
| Eval suite >= 15 | PASS | 30 tasks in `evals/tasks.jsonl` |
| Automatic graders | PASS | Notebook 06 |
| Two configurations | PASS | A = 70%, B = 80% |
| Error analysis | PASS | Notebook 06 |
| Lethal Trifecta analysis | PASS | Notebook 07 |
| Attack tried | PASS | Four adversarial security cases |
| Defence stopped attack | PASS | Defended attack success = 0% |
| Public/synthetic data | PASS | τ²-Bench Retail |
| Reproducible environment | PASS | `pyproject.toml`, `.env.example`, prebuilt `dist/`, `uv` run path, CI workflow, local smoke test |
| Final UI/demo | PASS | Connected UI + FastAPI backend, Notebook 08, `artifacts/demo.png` |

## Submission artifacts

- `README.md`
- `AGENTS.md`
- `server.py`
- `backend/retail_mcp.py`
- `evals/tasks.jsonl`
- `evals/eval_A.csv`
- `evals/eval_B.csv`
- eight development notebooks
- security CSVs
- demo screenshot
- GitHub Actions CI workflow
- `.env.example` (contains placeholders only)

- `slides/RetailX_Capstone_Presentation.pptx`
- `slides/SPEAKER_NOTES.md`
- `artifacts/SMOKE_TEST.txt`