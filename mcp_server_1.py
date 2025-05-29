from mcp.server.fastmcp import FastMCP
from typing import Dict, Optional
import uuid
import datetime
import os
import csv
import sqlite3

# === Setup DB File Path ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "llm_traces.db")
TABLE_NAME = "traces"

# Ensure DB directory exists (if using subdirectories)
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

# Initialize FastMCP server
mcp = FastMCP("LLM Trace Server")

# === DB Initialization ===
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                trace_id TEXT PRIMARY KEY,
                prompt TEXT,
                response TEXT,
                meta TEXT,
                timestamp TEXT
            )
        """)
    print("[init_db] Database initialized at", DB_FILE)

init_db()

# === Tool: Store Trace ===
@mcp.tool()
def store_trace(prompt: str, response: str, meta: Optional[Dict] = None) -> Dict:
    """Store an LLM trace in the system."""
    trace_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    metadata_str = str(meta or {})

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            f"INSERT INTO {TABLE_NAME} (trace_id, prompt, response, meta, timestamp) VALUES (?, ?, ?, ?, ?)",
            (trace_id, prompt, response, metadata_str, timestamp)
        )

    print(f"[store_trace] Stored trace_id: {trace_id}")
    return {
        "trace_id": trace_id,
        "prompt": prompt,
        "response": response,
        "metadata": meta or {},
        "timestamp": timestamp
    }

# === Tool: Search Traces ===
@mcp.tool()
def search_traces(query: str, limit: int = 10) -> Dict:
    """Search through stored LLM traces."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            f"SELECT trace_id, prompt, response, meta, timestamp FROM {TABLE_NAME} WHERE prompt LIKE ? OR response LIKE ?",
            (f"%{query}%", f"%{query}%")
        )
        results = cursor.fetchall()

    print(f"[search_traces] Found {len(results)} matches for query: {query}")
    return {
        "results": [
            {
                "trace_id": row[0],
                "prompt": row[1],
                "response": row[2],
                "metadata": row[3],
                "timestamp": row[4]
            }
            for row in results[:limit]
        ]
    }

# === Tool: Get Trace by ID ===
@mcp.tool()
def get_trace(trace_id: str) -> Dict:
    """Retrieve a specific LLM trace by ID."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            f"SELECT prompt, response, meta, timestamp FROM {TABLE_NAME} WHERE trace_id = ?",
            (trace_id,)
        )
        row = cursor.fetchone()

    if row is None:
        return {"error": "Trace not found"}

    print(f"[get_trace] Retrieved trace_id: {trace_id}")
    return {
        "trace_id": trace_id,
        "prompt": row[0],
        "response": row[1],
        "metadata": row[2],
        "timestamp": row[3]
    }

# === Tool: Export Traces to CSV ===
@mcp.tool()
def export_traces_to_csv() -> Dict:
    """Export all traces to a CSV file."""
    csv_file = os.path.join(BASE_DIR, "traces_export.csv")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(f"SELECT trace_id, prompt, response, meta, timestamp FROM {TABLE_NAME}")
        rows = cursor.fetchall()

    with open(csv_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["trace_id", "prompt", "response", "metadata", "timestamp"])
        writer.writerows(rows)

    print(f"[export_traces_to_csv] Exported {len(rows)} traces to {csv_file}")
    return {"exported_file": csv_file, "count": len(rows)}

# === Run MCP Server ===
if __name__ == "__main__":
    mcp.run()
