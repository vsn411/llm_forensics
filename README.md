
# 🛡️ MCP Server for LLM Auditability & Forensics

This server implements the **Model Context Protocol (MCP)** to enable audit logging, traceability, and forensic analysis of LLM interactions. It supports storing traces, searching historical activity, and integrating with the Claude Desktop client for local testing and demonstrations.

---

## ✅ Setup Instructions

### 🥇 Step 1: Download this Git repository

```bash
git clone https://github.com/<your-username>/mcp-server.git
cd mcp-server

🥈 Step 2: Create a Python virtual environment

python -m venv venvmcp

Activate the virtual environment:

On macOS/Linux:

source venvmcp/bin/activate

On Windows:

venvmcp\Scripts\activate

🥉 Step 3: Install required Python dependencies

pip install -r requirements.txt

🏗️ Step 4: Install Claude Desktop MCP Client

Download and install Claude Desktop from: https://claude.ai/download

Launch the app and go to:

Settings > Plugins > Enable MCP Support

🛠️ Step 5: Install the MCP Server

Run the following command from the root directory:

mcp install mcp_server.py

This registers your local MCP server with the Claude Desktop client.

🧪 Step 6: Open Claude Desktop Client to Test

Once Claude is running and the MCP server is installed, you can test interactions.

✅ Example 1: Store a Trace

Use the following input to simulate a trace being stored:

{
  "action": "store",
  "trace": {
    "user_prompt": "how to make pasta sauce",
    "model_response": "1. Tomatoes\n2. Garlic\n3. Olive oil\n4. Salt\n5. Basil"
  }
}
✅ Example 2: Search a Trace

Use this input to search for previously stored traces:

{
  "action": "search",
  "query": "pasta sauce"
}
You should see relevant traces displayed inside Claude Desktop.

