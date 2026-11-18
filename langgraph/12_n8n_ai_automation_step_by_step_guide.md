# Week 22: AI Automations in n8n - Step-by-Step Canvas Guide

This guide gives you exact click-by-click instructions to build the AI automations covered in Week 22 from an empty n8n canvas.

---

## 🏗️ Overview of What You Will Build

```
[Trigger Node] ────────► [Ingest Document / Email] ────────► [AI Agent Node] ────────► [Send Response / Email]
                                                                 │   │
                                    ┌────────────────────────────┘   └────────────────────────────┐
                                    ▼                                                             ▼
                    [Chat Model: OpenAI / Ollama]                                    [LangChain Memory]
```

We will build this in 3 clear milestones:
1. **Lab 1:** Setting up the AI Agent with LangChain + OpenAI & Ollama.
2. **Lab 2:** Ingesting & Processing Documents (Invoices/Text).
3. **Lab 3:** Complete End-to-End Email Automation with AI Drafting.

---

# 🧪 Lab 1: AI Agent with OpenAI, Ollama & LangChain Memory

### Step 1.1: Start with a Fresh Canvas & Manual Trigger
1. In n8n, click **+ Add Workflow** (top right).
2. Click **Add first step...** or press the **`+`** button.
3. Search for **Manual Trigger** (node name: `n8n-nodes-base.manualTrigger`).
4. Click it to place it on the canvas. This allows you to test on demand without waiting for external webhooks.

---

### Step 1.2: Add the LangChain AI Agent Node
1. Drag the connection line out from the right handle of **Manual Trigger**, or click **`+`** on the canvas.
2. In the search box, search for **AI Agent** (under *Advanced AI*).
3. Select **AI Agent**.
4. Double-click the **AI Agent** node to configure:
   - **Prompt Type**: Select `Define below`.
   - **Text (User Prompt)**:
     ```text
     Hello! Please introduce yourself, summarize what your core capabilities are, and tell me today's date if provided.
     ```
   - Click **Add Option** $\to$ **System Message**:
     ```text
     You are a helpful, professional Enterprise AI Operations Assistant. Always be concise, polite, and structure your responses with clean bullet points.
     ```
5. Notice the bottom ports of the node:
   - You will see labels like **Model**, **Memory**, **Tool**. In LangChain, these are **sub-nodes** that plug into the agent's bottom sockets.

---

### Step 1.3: Connect the Model Sub-Node (Option A: OpenAI)
1. Look at the bottom port labeled **Model** on the **AI Agent** node.
2. Drag out from that **Model** port, or click **`+`** right below it.
3. Search for **OpenAI Chat Model** (`@n8n/n8n-nodes-langchain.lmChatOpenAi`).
4. Double-click **OpenAI Chat Model**:
   - **Credential for OpenAI**: Select your OpenAI API credential.
   - **Model**: Select `gpt-4o-mini` (or type it in).
   - Click **Add Option** $\to$ **Temperature**: Set to `0.2` (lower temperature = more deterministic and factual).

> [!TIP]
> **Free Alternative (OpenRouter):**
> If you don't have an OpenAI credit balance:
> 1. In **OpenAI Chat Model**, select your OpenRouter API key credential.
> 2. Click **Add Option** $\to$ **Base URL**.
> 3. Enter: `https://openrouter.ai/api/v1`
> 4. Set **Model**: `openrouter/free` or `meta-llama/llama-3-8b-instruct:free`.

---

### Step 1.4: Connect the Model Sub-Node (Option B: Local Ollama)
If you want to run completely free and 100% offline:
1. Open your terminal on your computer and start a local model:
   ```bash
   ollama run llama3.2
   ```
2. In n8n, delete or disconnect the OpenAI node.
3. From the **Model** socket of the **AI Agent**, drag out and search for **Ollama Chat Model**.
4. Double-click **Ollama Chat Model**:
   - **Base URL**:
     - `http://localhost:11434` *(if running n8n directly on Windows/Mac)*
     - `http://host.docker.internal:11434` *(if running n8n inside Docker)*
   - **Model**: `llama3.2` (or `phi3:mini`).
   - Click **Add Option** $\to$ **Temperature**: `0.2`.

---

### Step 1.5: Add LangChain Memory (Simple Memory)
1. Look at the bottom port labeled **Memory** on the **AI Agent** node.
2. Drag out from the **Memory** port.
3. Select **Simple Memory** (in n8n, this is the `Window Buffer Memory` node: `@n8n/n8n-nodes-langchain.memoryBufferWindow`).
4. Double-click **Simple Memory**:
   - **Session ID / Session Key**:
     - By default, n8n writes `={{ $json.sessionId }}` which shows `undefined` if your input node hasn't passed a session ID yet.
     - Click **Fixed** (or delete the expression) and type a static string: `session_1` (or use `={{ $json.sessionId || 'session_1' }}`).
   - **Context Window Length**: Set to `5` (keeps the last 5 conversation exchanges in RAM).

---

### Step 1.6: Test Lab 1
1. Click **Test Step** on the **AI Agent** node.
2. Watch the execution complete. Inspect the output window on the right. You should see a formatted response from the LLM via LangChain!

---

# 📄 Lab 2: Document Ingestion & Structured Processing

Now we will add document parsing so the AI can extract data from invoices, receipts, or contracts.

### Step 2.1: Add Document Payload (Set / Edit Fields Node)
1. Hover between the **Manual Trigger** and the **AI Agent**. Click the **`+`** on the connection line (or insert a node after Manual Trigger).
2. Search for **Edit Fields (Set)** (`n8n-nodes-base.set`).
3. Name this node: `Incoming Document Payload`.
4. Under **Fields to Set**, click **Add Field**:
   - **Field 1:**
     - **Name**: `sender_name`
     - **Type**: `String`
     - **Value**: `Sarah Connor`
   - **Field 2:**
     - **Name**: `document_type`
     - **Type**: `String`
     - **Value**: `Invoice`
   - **Field 3:**
     - **Name**: `document_content`
     - **Type**: `String`
     - **Value**:
       ```text
       INVOICE #INV-2026-881
       Date: 2026-10-15
       Client: Cyberdyne Defense Systems

       Line Items:
       1. Dedicated Cloud Cluster (30 Days) - $2,500.00
       2. Enterprise Support Plan - $800.00
       3. Overcharge / Unscheduled Maintenance Fee - $650.00

       Subtotal: $3,950.00
       Tax (10%): $395.00
       Total Due: $4,345.00

       Customer Note: We dispute Line Item #3 ($650.00). Our Enterprise SLA guarantees zero maintenance fees.
       ```

---

### Step 2.2: Pass Document Variables into the AI Agent
1. Connect `Incoming Document Payload` $\to$ `AI Agent`.
2. Double-click the **AI Agent** node.
3. Replace the **Text (User Prompt)** with this dynamic expression (switch to **Expression** mode by clicking the `fx` button or starting with `=`):
   ```javascript
   =You have received the following {{ $json.document_type }} from client "{{ $json.sender_name }}":

   --- DOCUMENT START ---
   {{ $json.document_content }}
   --- DOCUMENT END ---

   Tasks:
   1. Extract the Invoice Number, Total Due, and any Disputed Line Item.
   2. Determine if the customer complaint is valid based on the document note.
   3. Provide a structured summary in clean JSON format:
   {
     "invoice_number": "string",
     "total_due": "string",
     "disputed_amount": "string",
     "dispute_reason": "string",
     "action_required": "string"
   }
   ```
4. Click **Test Step** on the AI Agent.
5. Notice how the AI reads the raw invoice text, extracts the $650 dispute, and returns valid structured JSON.

---

# 📬 Lab 3: End-to-End Email Automation Pipeline

Now we connect the entire pipeline: Inbound Trigger $\to$ Document Analysis $\to$ AI Draft Generation $\to$ Outbound Email Dispatch.

### Step 3.1: Configure the AI Agent for Email Drafting
1. Open the **AI Agent** node.
2. In **System Message**, update it to:
   ```text
   You are an Executive Customer Relations & Billing Resolution AI. You read disputed client invoices, verify the claims against SLA policies, and draft courteous, professional, and actionable email replies.
   ```
3. In **Text (User Prompt)**, update the prompt to instruct the AI to generate the email reply body:
   ```javascript
   =Incoming Client Communication:
   Sender: {{ $json.sender_name }}
   Type: {{ $json.document_type }}

   Document Content:
   """
   {{ $json.document_content }}
   """

   Please execute:
   1. Analyze the disputed charge in the document.
   2. Draft a formal, empathetic response to {{ $json.sender_name }}.
   3. State that the $650 unscheduled maintenance surcharge has been temporarily frozen for investigation under the Enterprise SLA policy.
   4. Inform them the adjusted payable amount is $3,695.00 ($4,345 - $650).
   5. Output your response as a JSON object:
   {
     "recipient_name": "{{ $json.sender_name }}",
     "invoice_number": "INV-2026-881",
     "urgency": "High",
     "email_subject": "Update on Invoice #INV-2026-881 Dispute - Cyberdyne",
     "email_body": "Full body text of your reply..."
   }
   ```

---

### Step 3.2: Add the Outbound Email / HTTP Dispatch Node
1. From the output handle of the **AI Agent**, drag out and add an action node.
2. **Choice 1: Using the Gmail Node**
   - Search for **Gmail** $\to$ Resource: **Message** $\to$ Operation: **Send**.
   - **To**: `sarah.connor@cyberdyne.org`
   - **Subject**: `={{ $json.output.email_subject || 'Update on Your Invoice' }}`
   - **Message**: `={{ $json.output.email_body || $json.output }}`
3. **Choice 2: Using the Generic HTTP Request Node (No Email Account Needed)**
   - Search for **HTTP Request** (`n8n-nodes-base.httpRequest`).
   - **Method**: `POST`
   - **URL**: `https://jsonplaceholder.typicode.com/posts`
   - **Send Body**: Toggle **ON**
   - **Body Content Type**: `JSON`
   - **Specify Body**: `Using JSON`
   - **JSON**:
     ```javascript
     ={
       "to": "{{ $('Incoming Document Payload').item.json.sender_name }}",
       "subject": "Resolution for Invoice #INV-2026-881",
       "ai_generated_reply": {{ JSON.stringify($json.output) }},
       "dispatched_at": "{{ $now.format('yyyy-MM-dd HH:mm:ss') }}"
     }
     ```

---

## ⚡ Step 3.3: Run & Verify the Entire Pipeline
1. Click **Test Workflow** at the bottom of the canvas.
2. Watch the execution sequence:
   - `Manual Trigger` fires.
   - `Incoming Document Payload` supplies the customer invoice.
   - `AI Agent` reads the invoice, checks memory, and prompts the LLM (`OpenAI` or `Ollama`).
   - The LLM drafts the resolution email with accurate amounts ($3,695 adjusted balance).
   - `HTTP Request` (or Gmail) dispatches the payload.
3. Click on the final node $\to$ inspect the **Output** tab to view the live result!

---

## 🛠️ Summary of Common Gotchas to Warn Students About

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| **Connection refuses on Ollama** | n8n is running in Docker, Ollama is on host machine | Change Base URL from `localhost:11434` to `http://host.docker.internal:11434`. |
| **Model not found in Ollama** | Model hasn't been downloaded locally yet | Run `ollama pull llama3.2` or `ollama run llama3.2` in terminal first. |
| **Wrong Date Format in n8n** | Using uppercase `YYYY` or `DD` | n8n uses Luxon tokens: use lowercase `yyyy` and `dd` (e.g., `$now.format('yyyy-MM-dd')`). |
| **Cannot connect Model to Agent** | Trying to connect main execution port to bottom port | In n8n, sub-nodes must connect from their top output into the **bottom socket** of the parent node. |
| **OpenAI Quota Error** | Account has zero balance | Use OpenRouter free endpoint (`https://openrouter.ai/api/v1` with model `openrouter/free`) or switch to Ollama. |
