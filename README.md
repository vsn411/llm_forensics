# LLM Trace Server (MCP Server)

This is a lightweight, fast Model Context Protocol (MCP) server to store, search, retrieve, and export LLM traces. Ideal for audit logging and forensic analysis of AI interactions.

---

## 🛠️ Installation Steps

### Step 1: Clone the GitHub Repository

```bash
git clone https://github.com/vsn411/llm_forensics.git
cd llm_forensics
```

### Step 2: Create and Activate a Virtual Environment

```bash
python -m venv venvmcp
source venvmcp/bin/activate  # On Windows use: venvmcp\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Claude Desktop Client Setup (Optional for GUI Testing)

1. Download the [Claude Desktop Client](https://claude.ai/download) or any LLM desktop interface that supports tool plugins.
2. Ensure the client is allowed to use local tool endpoints.

---

## 🚀 Run the MCP Server

```bash
python mcp_server.py
```

or
```bash
mcp install mcp_server.py
```

> The server will initialize an SQLite database named `llm_traces.db` and expose tools via MCP.

---

## 🧪 Example Usage with Claude Desktop Client

### 📝 Example 1: Store a Trace

Prompt:

```text
how to make pasta sauce
```

Response:

```text
- Tomatoes
- Olive oil
- Garlic
- Basil
- Salt
- Pepper
```

Tool call (automatically handled if integrated via Claude Desktop):

```json
{
  "tool": "store_trace",
  "args": {
    "prompt": "how to make pasta sauce",
    "response": "Tomatoes, olive oil, garlic, basil, salt, pepper"
  }
}
```

### 🔍 Example 2: Search Traces

```json
{
  "tool": "search_traces",
  "args": {
    "query": "pasta sauce"
  }
}
```

### 📄 Example 3: Export Traces to CSV

```json
{
  "tool": "export_traces_to_csv",
  "args": {}
}
```

---

