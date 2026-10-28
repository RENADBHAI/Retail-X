# Retail X — Presentation Slides

These are the source slides for the 8-minute capstone presentation. The editable PPTX is kept in the final submission package.

## Slide 1 — Retail X
**Policy-aware Retail Operations Agent**

Retail X handles retail order requests as a controlled workflow rather than a single chatbot response.

**SDAIA Academy — Agentic AI Systems Engineering Capstone · Track 2**

---

## Slide 2 — Problem and target user

A cancellation request is not just “change the order status.”

Before acting, the system should verify:
- who the customer is
- whether the order belongs to that customer
- the current order status
- what the store policy allows
- whether a human approved the write

**Target user:** retail customer-service teams.

---

## Slide 3 — Architecture and design ladder

Customer → Retail X UI → harness → tools / MCP → τ²-Bench Retail data

**Prompt**
- baseline vs engineered system specification

**Context**
- AGENTS.md
- policy retrieval
- history compaction
- tool-result limits

**Harness**
- permissions
- step and cost budgets
- audit log
- ownership guard
- human approval

**Loop**
- multi-step tool execution with stop conditions

A separate graph was not needed because the workflow is small and controlled by the harness.

---

## Slide 4 — Live demo

1. Load a real pending order from `/api/demo-case`.
2. Submit the cancellation request.
3. Show the five workflow stages:
   - Identity Verification
   - Retrieve Order
   - Policy Check
   - Decision
   - Human Approval
4. Before approval, no write has happened.
5. Approve the action.
6. Show the order status changing to `cancelled`.

---

## Slide 5 — Context and harness decisions

Important controls are enforced outside the model.

- private order data is protected by an ownership check
- write actions are paused behind a human approval gate
- malicious user instructions cannot directly bypass those guards
- step and cost budgets limit agent execution
- audit events record important actions

---

## Slide 6 — Evaluation

**Same 30 tasks, same evaluation suite, two configurations**

| Config | Passed | Pass rate |
|---|---:|---:|
| A — baseline prompt | 21 / 30 | 70% |
| B — engineered prompt | 24 / 30 | 80% |

**Improvement: +10 percentage points**

Configuration B especially improved invalid-identity and adversarial cases.

The remaining ownership/privacy failures motivated the code-enforced security guard in Notebook 07.

---

## Slide 7 — Security and close

Retail X contains all three Lethal Trifecta legs:
- untrusted customer input
- private order data
- response egress

**Baseline:** unauthorized reads occurred.

**Defended configuration:**
- attack success rate: 0%
- attack block rate: 100%
- benign success rate: 100%

**Main lesson:** automate useful retail work, but keep private data and write actions controlled by the harness and a human.
