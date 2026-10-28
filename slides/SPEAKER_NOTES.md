# Retail X — 8-minute speaker notes

## Slide 1 — Retail X (0:00–0:35)
Retail X is a policy-aware retail operations agent. It handles order requests as a controlled workflow instead of answering immediately like a normal chatbot.

## Slide 2 — Problem and user (0:35–1:15)
A cancellation request looks simple, but the agent should not change an order until it knows who the customer is, whether the order belongs to them, what the policy allows, and whether a human approved the write. The target user is a retail customer-service team.

## Slide 3 — Architecture and design ladder (1:15–2:35)
Walk through customer → interface → harness → tools/MCP → public τ²-Bench data. Mention `AGENTS.md`, policy retrieval, compaction, tool-result limits, permission policy, step/cost budgets, audit log, and human approval. A separate graph was not necessary because the workflow is small and controlled by the harness loop.

## Slide 4 — Live demo (2:35–4:35)
Use a real pending order from `/api/demo-case`. Submit the cancellation request. Point to the five cards: identity, retrieve order, policy check, decision, human approval. Before approval, explain that no database write has happened. Click Approve, then show that the working order status becomes cancelled.

## Slide 5 — Context and harness decisions (4:35–5:25)
Explain why important controls are outside the model: the ownership check and write approval are code-enforced. The model cannot bypass them by following a malicious user instruction.

## Slide 6 — Evaluation (5:25–6:40)
Same 30 tasks, same model, two configurations. A scored 70%; B scored 80%. B especially improved invalid identity and adversarial cases. The remaining ownership/privacy failures motivated the security guard in Notebook 07.

## Slide 7 — Security and close (6:40–8:00)
Retail X has all three Lethal Trifecta legs: untrusted customer input, private order data, and response egress. Baseline attacks produced unauthorized reads; after the code-enforced ownership and egress guards, attack success dropped from 100% to 0% while defended benign requests succeeded. Close with the main lesson: useful automation, but private data and writes remain controlled by the harness and a human.

## Backup recording checklist
Record a 60–90 second screen capture before presentation day:
1. Open Retail X.
2. Load a pending demo order.
3. Send the cancellation request.
4. Show the workflow cards reaching Human Approval.
5. Click Approve.
6. Show the order status changing to `cancelled`.
7. Keep the video locally so it does not depend on Cloudflare, Colab, or model quota during the presentation.