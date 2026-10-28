#!/usr/bin/env python3
"""
Retail X final demo server.

- Serves the React frontend from ./dist when present.
- Uses the public τ²-Bench Retail domain.
- Uses OpenRouter for request understanding and grounded response wording.
- Enforces identity, ownership, policy checks and human approval in code.
"""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import uuid
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
try:
    from openai import OpenAI
except ImportError:  # deterministic fallback still works without the SDK
    OpenAI = None  # type: ignore[assignment]
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

TAU_DIR = Path(os.getenv("TAU2_DIR", ROOT / "tau2-bench"))
RETAIL_DIR = TAU_DIR / "data" / "tau2" / "domains" / "retail"
DIST_DIR = ROOT / "dist"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemma-4-31b-it:free").strip()

LLM_CLIENT = (
    OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )
    if OPENROUTER_API_KEY and OpenAI is not None
    else None
)


def ensure_tau2() -> None:
    if RETAIL_DIR.exists():
        return
    subprocess.run(
        [
            "git",
            "clone",
            "-q",
            "https://github.com/sierra-research/tau2-bench.git",
            str(TAU_DIR),
        ],
        check=True,
    )


ensure_tau2()

with open(RETAIL_DIR / "db.json", "r", encoding="utf-8") as f:
    SOURCE_DB = json.load(f)

POLICY_TEXT = (RETAIL_DIR / "policy.md").read_text(encoding="utf-8")
WORKING_DB = copy.deepcopy(SOURCE_DB)


def normalize_records(raw: Any, id_name: str) -> dict[str, dict]:
    if isinstance(raw, dict):
        out = {}
        for key, value in raw.items():
            row = dict(value)
            row.setdefault(id_name, key)
            out[str(key)] = row
        return out
    return {str(row[id_name]): dict(row) for row in raw}


USERS = normalize_records(WORKING_DB["users"], "user_id")
ORDERS = normalize_records(WORKING_DB["orders"], "order_id")
PRODUCTS = normalize_records(WORKING_DB.get("products", {}), "product_id")

ITEM_INDEX: dict[str, dict] = {}
for product_id, product in PRODUCTS.items():
    product_name = product.get("name", product_id)
    variants = product.get("variants", {})
    if isinstance(variants, dict):
        variants = list(variants.values())

    for variant in variants:
        item_id = variant.get("item_id") or variant.get("variant_id") or variant.get("id")
        if item_id:
            ITEM_INDEX[str(item_id)] = {
                "name": product_name,
                "price": float(variant.get("price") or 0),
                "options": variant.get("options", {}),
            }

POLICY_SECTIONS = [
    section.strip()
    for section in re.split(r"\n(?=#{1,3}\s)", POLICY_TEXT)
    if section.strip()
]

PENDING_ACTIONS: dict[str, dict] = {}
AUDIT_LOG: list[dict] = []


def audit(event: str, **payload: Any) -> None:
    AUDIT_LOG.append({"event": event, **payload})


def find_user_by_email(email: str) -> tuple[str | None, dict | None]:
    wanted = email.strip().lower()
    for user_id, user in USERS.items():
        if str(user.get("email", "")).strip().lower() == wanted:
            audit("find_user_by_email", email=wanted, found=True, user_id=user_id)
            return user_id, user

    audit("find_user_by_email", email=wanted, found=False)
    return None, None


def get_order(order_id: str) -> tuple[str | None, dict | None]:
    raw = order_id.strip()
    candidates = [raw, "#" + raw.lstrip("#"), raw.lstrip("#")]
    for candidate in candidates:
        if candidate in ORDERS:
            audit("get_order_details", order_id=candidate)
            return candidate, ORDERS[candidate]
    return None, None


def retrieve_policy(query: str) -> str:
    terms = set(re.findall(r"[a-zA-Z]+", query.lower()))
    ranked: list[tuple[int, str]] = []

    for section in POLICY_SECTIONS:
        section_terms = set(re.findall(r"[a-zA-Z]+", section.lower()))
        ranked.append((len(terms & section_terms), section))

    ranked.sort(key=lambda x: x[0], reverse=True)
    selected = [section for score, section in ranked[:3] if score > 0]
    result = "\n\n".join(selected)[:3500]
    audit("retrieve_policy", query=query, chars=len(result))
    return result


def regex_intent(message: str) -> dict[str, Any]:
    email_match = re.search(
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
        message,
        flags=re.I,
    )
    order_match = re.search(
        r"#?[A-Z]\d{6,}",
        message,
        flags=re.I,
    )

    lower = message.lower()
    wants_cancel = any(
        phrase in lower
        for phrase in ["cancel", "cancellation", "إلغاء", "الغي", "الغاء"]
    )

    reason = None
    if "ordered by mistake" in lower:
        reason = "ordered by mistake"
    elif "no longer needed" in lower:
        reason = "no longer needed"

    return {
        "email": email_match.group(0) if email_match else None,
        "order_id": order_match.group(0) if order_match else None,
        "intent": "cancel" if wants_cancel else "status",
        "reason": reason,
    }


def parse_json_object(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if not match:
            raise ValueError("No JSON object found.")
        return json.loads(match.group(0))


def analyze_request(message: str) -> dict[str, Any]:
    """Use OpenRouter when configured, with deterministic fallback."""
    fallback = regex_intent(message)

    if not LLM_CLIENT:
        audit("llm_fallback", reason="OPENROUTER_API_KEY not configured")
        return fallback

    try:
        response = LLM_CLIENT.chat.completions.create(
            model=OPENROUTER_MODEL,
            temperature=0,
            max_tokens=180,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract a retail customer-service request into JSON only. "
                        "Return keys: email, order_id, intent, reason. "
                        "intent must be one of: status, cancel, policy, other. "
                        "Keep an order ID exactly as written, including a leading #. "
                        "Valid cancellation reasons are 'ordered by mistake' or "
                        "'no longer needed'; otherwise reason must be null. "
                        "Do not invent values."
                    ),
                },
                {"role": "user", "content": message},
            ],
        )
        data = parse_json_object(response.choices[0].message.content or "")

        parsed = {
            "email": data.get("email") or fallback["email"],
            "order_id": data.get("order_id") or fallback["order_id"],
            "intent": str(data.get("intent") or fallback["intent"]).lower(),
            "reason": data.get("reason") or fallback["reason"],
        }

        if parsed["intent"] not in {"status", "cancel", "policy", "other"}:
            parsed["intent"] = fallback["intent"]

        audit("openrouter_request_analysis", model=OPENROUTER_MODEL)
        return parsed

    except Exception as exc:
        audit("llm_fallback", reason=f"{type(exc).__name__}: {exc}")
        return fallback


def grounded_reply(facts: str, fallback: str) -> str:
    if not LLM_CLIENT:
        return fallback

    try:
        response = LLM_CLIENT.chat.completions.create(
            model=OPENROUTER_MODEL,
            temperature=0,
            max_tokens=150,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Retail X. Write one concise customer-service reply "
                        "using only the supplied verified facts. Never add private data, "
                        "policy rules, or actions that are not present in the facts."
                    ),
                },
                {"role": "user", "content": facts},
            ],
        )
        text = (response.choices[0].message.content or "").strip()
        return text or fallback
    except Exception as exc:
        audit("llm_reply_fallback", reason=f"{type(exc).__name__}: {exc}")
        return fallback


def item_view(order: dict) -> list[dict]:
    rows = []
    for raw_item in order.get("items", []):
        if not isinstance(raw_item, dict):
            continue

        item_id = (
            raw_item.get("item_id")
            or raw_item.get("variant_id")
            or raw_item.get("product_id")
            or "Unknown item"
        )
        quantity = int(raw_item.get("quantity") or 1)
        catalog = ITEM_INDEX.get(str(item_id), {})
        price = float(raw_item.get("price") or catalog.get("price") or 0)

        rows.append(
            {
                "name": catalog.get("name", str(item_id)),
                "quantity": quantity,
                "price": price,
            }
        )
    return rows


def order_view(order_id: str, order: dict) -> dict:
    items = item_view(order)
    total = sum(row["price"] * row["quantity"] for row in items)

    if total == 0:
        for payment in order.get("payment_history", []):
            if isinstance(payment, dict):
                amount = payment.get("amount")
                if isinstance(amount, (int, float)):
                    total += abs(float(amount))

    return {
        "order_id": order_id,
        "status": str(order.get("status", "unknown")),
        "items": items,
        "total": round(total, 2),
    }


def step(title: str, icon: str, tone: str, text: str, state: str) -> dict:
    return {
        "title": title,
        "icon": icon,
        "tone": tone,
        "text": text,
        "state": state,
    }


def default_workflow() -> list[dict]:
    return [
        step("Identity Verification", "shield", "mint", "Waiting for customer identity.", "waiting"),
        step("Retrieve Order", "package", "lavender", "Waiting for order retrieval.", "waiting"),
        step("Policy Check", "file", "amber", "Waiting for policy retrieval.", "waiting"),
        step("Decision", "gavel", "blue", "Waiting for a grounded decision.", "waiting"),
        step("Human Approval", "user", "coral", "No write action pending.", "waiting"),
    ]


class AgentRequest(BaseModel):
    message: str


class ApprovalRequest(BaseModel):
    action_id: str
    decision: str


app = FastAPI(title="Retail X API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "users": len(USERS),
        "orders": len(ORDERS),
        "pending_actions": len(PENDING_ACTIONS),
        "openrouter_configured": bool(OPENROUTER_API_KEY),
        "model": OPENROUTER_MODEL,
    }


@app.get("/api/demo-case")
def demo_case() -> dict:
    for order_id, order in ORDERS.items():
        if str(order.get("status", "")).lower() != "pending":
            continue

        user = USERS.get(str(order.get("user_id")))
        if not user or not user.get("email"):
            continue

        return {
            "email": user["email"],
            "order_id": order_id,
            "prompt": (
                f"My email is {user['email']}. "
                f"Please check order {order_id}. "
                "I ordered it by mistake and want to cancel it."
            ),
        }

    raise HTTPException(status_code=404, detail="No pending demo order found.")


@app.post("/api/agent")
def run_agent(req: AgentRequest) -> dict:
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    parsed = analyze_request(message)
    workflow = default_workflow()

    email = parsed.get("email")
    if not email:
        workflow[0]["state"] = "blocked"
        workflow[0]["text"] = "Identity not provided. Ask for the customer's email."
        return {
            "answer": "Please provide the email address associated with your account first.",
            "workflow": workflow,
            "order": None,
            "requires_approval": False,
            "action_id": None,
            "approval_summary": None,
        }

    user_id, _user = find_user_by_email(email)

    if not user_id:
        workflow[0]["state"] = "blocked"
        workflow[0]["text"] = f"No customer matched {email}."
        return {
            "answer": "I could not verify that email in the retail database.",
            "workflow": workflow,
            "order": None,
            "requires_approval": False,
            "action_id": None,
            "approval_summary": None,
        }

    workflow[0]["state"] = "done"
    workflow[0]["text"] = f"Verified {email} as customer {user_id}."

    order_token = parsed.get("order_id")
    if not order_token:
        workflow[1]["state"] = "blocked"
        workflow[1]["text"] = "No order ID was provided."
        return {
            "answer": "Your identity is verified. Please provide the order ID you want me to check.",
            "workflow": workflow,
            "order": None,
            "requires_approval": False,
            "action_id": None,
            "approval_summary": None,
        }

    order_id, order = get_order(str(order_token))

    if not order:
        workflow[1]["state"] = "blocked"
        workflow[1]["text"] = f"Order {order_token} was not found."
        return {
            "answer": f"I could not find order {order_token}.",
            "workflow": workflow,
            "order": None,
            "requires_approval": False,
            "action_id": None,
            "approval_summary": None,
        }

    # Code-enforced ownership boundary.
    if str(order.get("user_id")) != str(user_id):
        audit(
            "security_block",
            reason="ownership_mismatch",
            requested_order=order_id,
            verified_user=user_id,
        )
        workflow[1]["state"] = "blocked"
        workflow[1]["text"] = "SECURITY BLOCK: order ownership does not match the verified customer."
        workflow[4]["text"] = "No action can proceed after an ownership failure."

        return {
            "answer": (
                "I can't provide private information for an order that is not "
                "associated with the verified customer."
            ),
            "workflow": workflow,
            "order": None,
            "requires_approval": False,
            "action_id": None,
            "approval_summary": None,
        }

    status = str(order.get("status", "")).lower()
    workflow[1]["state"] = "done"
    workflow[1]["text"] = (
        f"Retrieved {order_id}. Status: {status}. Ownership verified for {email}."
    )

    intent = parsed.get("intent", "status")
    wants_cancel = intent == "cancel"

    policy_query = "cancel pending order" if wants_cancel else "order information authentication"
    _policy = retrieve_policy(policy_query)
    workflow[2]["state"] = "done"
    workflow[2]["text"] = (
        "Policy retrieved: pending orders may be cancelled only after status, reason "
        "and explicit confirmation checks."
        if wants_cancel
        else "Policy retrieved: authenticated customers may access their own order information."
    )

    view = order_view(order_id, order)

    if not wants_cancel:
        workflow[3]["state"] = "done"
        workflow[3]["text"] = f"Read-only request approved. Order status is {status}."
        workflow[4]["text"] = "No approval needed for this read-only request."

        fallback = (
            f"Order {order_id} belongs to your verified account and its current status is {status}."
        )
        answer = grounded_reply(
            f"Verified order ID: {order_id}\nVerified status: {status}\n"
            "The customer owns this order. This is a read-only request.",
            fallback,
        )

        return {
            "answer": answer,
            "workflow": workflow,
            "order": view,
            "requires_approval": False,
            "action_id": None,
            "approval_summary": None,
        }

    if status != "pending":
        workflow[3]["state"] = "done"
        workflow[3]["text"] = f"Cancellation denied by policy because status is {status}."
        workflow[4]["text"] = "No approval requested because the action is not policy-eligible."

        return {
            "answer": (
                f"Order {order_id} cannot be cancelled because its status is {status}; "
                "the policy only allows cancellation of pending orders."
            ),
            "workflow": workflow,
            "order": view,
            "requires_approval": False,
            "action_id": None,
            "approval_summary": None,
        }

    reason = parsed.get("reason") or "ordered by mistake"
    if reason not in {"no longer needed", "ordered by mistake"}:
        reason = "ordered by mistake"

    workflow[3]["state"] = "done"
    workflow[3]["text"] = f"Cancellation is eligible. Reason: {reason}."

    action_id = str(uuid.uuid4())
    PENDING_ACTIONS[action_id] = {
        "type": "cancel_order",
        "order_id": order_id,
        "user_id": user_id,
        "reason": reason,
    }

    audit(
        "approval_requested",
        action_id=action_id,
        order_id=order_id,
        action="cancel_order",
    )

    workflow[4]["state"] = "active"
    workflow[4]["text"] = "Sensitive write action is paused until a human explicitly approves it."

    return {
        "answer": (
            f"Order {order_id} is pending and is eligible for cancellation. "
            "I have paused the write action for human approval."
        ),
        "workflow": workflow,
        "order": view,
        "requires_approval": True,
        "action_id": action_id,
        "approval_summary": (
            f"Cancel order {order_id} for verified customer {email}. "
            f"Reason: {reason}. This will change the working order status to cancelled."
        ),
    }


@app.post("/api/approval")
def approve(req: ApprovalRequest) -> dict:
    action = PENDING_ACTIONS.get(req.action_id)

    if not action:
        raise HTTPException(
            status_code=404,
            detail="Approval action was not found or already resolved.",
        )

    decision = req.decision.strip().lower()
    if decision not in {"approve", "reject"}:
        raise HTTPException(status_code=400, detail="Decision must be approve or reject.")

    order_id = action["order_id"]
    order = ORDERS[order_id]

    if decision == "reject":
        PENDING_ACTIONS.pop(req.action_id, None)
        audit("approval_rejected", action_id=req.action_id, order_id=order_id)
        return {
            "message": f"Cancellation of order {order_id} was rejected. No database change was made.",
            "order": order_view(order_id, order),
        }

    # Re-check the protected conditions immediately before the write.
    if str(order.get("user_id")) != str(action["user_id"]):
        raise HTTPException(status_code=403, detail="Ownership changed; write blocked.")

    if str(order.get("status", "")).lower() != "pending":
        raise HTTPException(status_code=409, detail="Order is no longer pending; cancellation blocked.")

    order["status"] = "cancelled"
    order["cancellation_reason"] = action["reason"]

    PENDING_ACTIONS.pop(req.action_id, None)
    audit("approval_approved", action_id=req.action_id, order_id=order_id)
    audit("cancel_pending_order", order_id=order_id, new_status="cancelled")

    return {
        "message": f"Approved. Order {order_id} was cancelled in the Retail X working database.",
        "order": order_view(order_id, order),
    }


@app.get("/api/audit")
def audit_log() -> dict:
    return {"events": AUDIT_LOG[-100:]}


# Serve the built React app when dist/ is present.
if DIST_DIR.exists():
    assets_dir = DIST_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend(full_path: str):
        requested = DIST_DIR / full_path
        if full_path and requested.exists() and requested.is_file():
            return FileResponse(requested)
        return FileResponse(DIST_DIR / "index.html")


def main() -> None:
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )


if __name__ == "__main__":
    main()