#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=2.3"]
# ///

import json
import os
import shutil
import subprocess
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

ROOT = Path(__file__).resolve().parents[1]
TAU_DIR = Path(os.getenv("TAU2_DIR", ROOT / "tau2-bench"))
SOURCE_DB = TAU_DIR / "data" / "tau2" / "domains" / "retail" / "db.json"
WORK_DB = Path(os.getenv("RETAILX_DB_PATH", ROOT / "data" / "retail_working_db.json"))

server = MCPServer(
    "retail-x",
    title="Retail X MCP Server",
    instructions="Retail order tools over the public tau2-bench retail dataset.",
    version="1.0.0",
    log_level="WARNING",
)


def ensure_work_db() -> None:
    if not SOURCE_DB.exists():
        subprocess.run(
            ["git", "clone", "-q", "https://github.com/sierra-research/tau2-bench.git", str(TAU_DIR)],
            check=True,
        )
    WORK_DB.parent.mkdir(parents=True, exist_ok=True)
    if not WORK_DB.exists():
        shutil.copy2(SOURCE_DB, WORK_DB)


def load_db() -> dict:
    ensure_work_db()
    return json.loads(WORK_DB.read_text(encoding="utf-8"))


def save_db(db: dict) -> None:
    WORK_DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


@server.tool()
def get_order_details(order_id: str, user_id: str) -> dict:
    """Read an order only when it belongs to the identified customer."""
    db = load_db()
    order = db["orders"].get(order_id)
    if not order:
        raise ToolError("Order not found")
    if order["user_id"] != user_id:
        raise ToolError("Order does not belong to this customer")
    return {
        "order_id": order_id,
        "user_id": order["user_id"],
        "status": order["status"],
        "items": order["items"],
        "cancel_reason": order.get("cancel_reason"),
    }


@server.tool()
def cancel_pending_order(order_id: str, user_id: str, reason: str) -> dict:
    """Cancel a pending order. Host-side human approval is required before this write tool is called."""
    db = load_db()
    order = db["orders"].get(order_id)
    if not order:
        raise ToolError("Order not found")
    if order["user_id"] != user_id:
        raise ToolError("Order does not belong to this customer")
    if order["status"] != "pending":
        raise ToolError("Only pending orders can be cancelled")
    if reason not in {"no longer needed", "ordered by mistake"}:
        raise ToolError("Invalid cancellation reason")

    order["status"] = "cancelled"
    order["cancel_reason"] = reason
    save_db(db)

    return {
        "order_id": order_id,
        "status": "cancelled",
        "cancel_reason": reason,
    }


if __name__ == "__main__":
    server.run()