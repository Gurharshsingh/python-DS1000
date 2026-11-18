# Lesson: Simple AI Agent in n8n with Manual Trigger

---

## 🧠 Understanding the n8n AI Agent Node

In n8n, the **AI Agent** node is powered directly by **LangChain** under the hood. 

Unlike regular n8n nodes that only connect left-to-right, the AI Agent node has **special connection ports at the bottom**:

```
┌────────────────────────────────────────────────────────┐
│                        AI AGENT                        │
│                                                        │
│  [Main Input] ───>  🤖 AI Agent Node  ───> [Output]   │
│                          │        │                    │
│                 (Model)  │        │ (Tools)            │
│                          ▼        ▼                    │
│                 ┌──────────┐    ┌──────────┐           │
│                 │ Chat     │    │Calculator│           │
│                 │ Model    │    │Tool      │           │
│                 └──────────┘    └──────────┘           │
└────────────────────────────────────────────────────────┘
```

1. **Main Input (Left port):** The prompt / question text sent to the agent.
2. **Model Input (Bottom port `ai_languageModel`):** The LLM brain (OpenAI, OpenRouter, Anthropic, Ollama).
3. **Tools Input (Bottom port `ai_tool`):** External abilities (Calculator, Google Search, Custom Code Tool, Wikipedia).
4. **Memory Input (Bottom port `ai_memory`):** Optional chat history (Window Buffer Memory).

---

## 🛠️ Step-by-Step: How to Build It Manually in n8n

### Step 1: Add Node 1 — The Manual Trigger
1. On an empty canvas, click **Add first step...**
2. Search for: **`Manual`** $\to$ select **When clicking 'Test workflow'** (`Manual Trigger`).
3. This node allows you to run and debug the agent on demand with one click.

---

### Step 2: Add Node 2 — Edit Fields (Set Your Prompt)
1. Click the **+** on the right of the Manual Trigger.
2. Search for: **`Edit Fields`** (or **`Set`**).
3. Click **Add Field**:
   - **Name:** `prompt`
   - **Value:**  
     `What is the 18% tax on an order of $3,450, and what is the final total? Also write a 1-sentence friendly confirmation.`
4. Click **Test step** to ensure the string passes through.

---

### Step 3: Add Node 3 — The AI Agent Node
1. Click the **+** on the right of the Edit Fields node.
2. Search for: **`AI Agent`** (under Advanced AI).
3. In the AI Agent settings:
   - **Prompt Type:** `Define below`
   - **User Message (Prompt):** Switch to the **Expression** tab and write:
     ```javascript
     {{ $json.prompt }}
     ```
   - **System Message (Optional):**  
     `You are a helpful business assistant. Whenever a calculation is requested, ALWAYS use the Calculator tool to guarantee 100% mathematical accuracy.`

---

### Step 4: Attach the Chat Model (Sub-node at bottom)
1. Look at the **bottom of the AI Agent node** $\to$ click the small **+** under the **Model** connector.
2. Search for: **`OpenAI Chat Model`**.
3. In its settings:
   - **Credential:** Select your OpenAI / OpenRouter credential.  
     *(If using OpenRouter: Under options, set Base URL to `https://openrouter.ai/api/v1` and Model to `openrouter/free`)*
   - **Temperature:** `0.2`

---

### Step 5: Attach the Calculator Tool (Sub-node at bottom)
1. Look at the bottom of the AI Agent node $\to$ click the small **+** under the **Tool** connector.
2. Search for: **`Calculator`** $\to$ select **Calculator** (`@n8n/n8n-nodes-langchain.toolCalculator`).
3. No configuration needed! The agent will now automatically call the calculator whenever math is involved.

---

## 🚀 How to Run and Test

1. Click the big orange button at the bottom: **Test workflow** (or click the Manual Trigger).
2. Watch the execution:
   - The prompt flows into the **AI Agent**.
   - The AI Agent realizes it needs to compute `3450 * 0.18`.
   - It **invokes the Calculator sub-node** autonomously.
   - It computes `$621.00` tax and `$4,071.00` total.
   - It writes the final friendly confirmation.
3. In the output panel, inspect the final agent response:
   ```json
   {
     "output": "The 18% tax on an order of $3,450 is $621.00, bringing the final total to $4,071.00.\n\nThank you for your order, and please let us know if you need any further assistance!"
   }
   ```

---

## 📦 Instant Import

You can also import the pre-built workflow directly:
- File: **[n8n_ai_agent_workflow.json](file:///e:/python-DS1000/langgraph/n8n_ai_agent_workflow.json)**
- In n8n: Click `...` (top right) $\to$ **Import from File** $\to$ select `n8n_ai_agent_workflow.json`.
