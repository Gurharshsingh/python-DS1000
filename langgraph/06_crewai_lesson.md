# Lesson 6: CrewAI Fundamentals (Agents, Tasks, Processes)

---

## 🧠 The 4 Core Pillars of CrewAI

```
┌────────────────────────────────────────────────────────────────────────┐
│                                 CREW                                   │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                            PROCESS                               │  │
│  │              (Process.sequential or Process.hierarchical)         │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                        │
│       ┌──────────────────────┐          ┌──────────────────────┐       │
│       │        AGENTS        │          │        TASKS         │       │
│       │  • Role              │ ───────> │  • Description       │       │
│       │  • Goal              │ (Assigned│  • Expected Output   │       │
│       │  • Backstory         │    To)   │  • Agent             │       │
│       └──────────────────────┘          └──────────────────────┘       │
└────────────────────────────────────────────────────────────────────────┘
```

| Pillar | What it is | Key Parameters | Real-World Analogy |
| :--- | :--- | :--- | :--- |
| **1. Agent** | An autonomous team member with a specialized persona | `role`, `goal`, `backstory`, `llm`, `verbose` | The Employee (e.g. Senior Researcher) |
| **2. Task** | A specific assignment with a clear goal and expected deliverable | `description`, `expected_output`, `agent` | The Ticket / Work Order |
| **3. Process** | The workflow execution strategy | `Process.sequential` or `Process.hierarchical` | Company Operating Procedure |
| **4. Crew** | The container coordinating all agents and tasks together | `agents=[...]`, `tasks=[...]`, `process=...` | The Project Team / Squad |

---

## 🥊 CrewAI vs. LangGraph: What's the Difference?

| Feature | LangGraph | CrewAI |
| :--- | :--- | :--- |
| **Mental Model** | State Machine & Workflow Graph | Autonomous Role-Playing Organization |
| **Level of Control** | Low-level (Nodes, Edges, State Dicts) | High-level (Roles, Goals, Backstories) |
| **When to use?** | Exact branching, custom logic, strict state manipulation | Multi-agent collaboration, delegation, and role-driven problem solving |

---

## ⚙️ How Processes Work in CrewAI

### 1. `Process.sequential` (Default)
Tasks are executed one after the other in linear order:
$$\text{Task 1 (Researcher)} \longrightarrow \text{Task 2 (Writer)} \longrightarrow \text{Task 3 (Editor)}$$
- The output of Task 1 is automatically passed as context to Task 2!

### 2. `Process.hierarchical`
A manager agent automatically coordinates the team, decides who executes which subtask, and validates outputs before finishing.

---

## 💻 Starter Code Structure (`08_crewai_intro.py`)

### Step 1: Define the LLM (OpenRouter)
```python
from crewai import LLM

llm = LLM(
    model="openrouter/openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_API_KEY"),
)
```

### Step 2: Define Agents
```python
from crewai import Agent

researcher = Agent(
    role="Senior AI Researcher",
    goal="Discover the latest facts and breakthrough trends in AI",
    backstory="You are an expert researcher known for finding actionable tech insights.",
    llm=llm,
    verbose=True
)
```

### Step 3: Define Tasks
```python
from crewai import Task

research_task = Task(
    description="Research 3 major trends in Multi-Agent AI in 2026 for {topic}.",
    expected_output="A bullet-point summary of 3 key trends with short explanations.",
    agent=researcher
)
```

### Step 4: Assemble the Crew and Run
```python
from crewai import Crew, Process

my_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)

result = my_crew.kickoff(inputs={"topic": "Agentic AI"})
print(result)
```

---

## 🛠️ Advanced CrewAI Topics & Code Examples

### 1. Agents with Custom Tools ([09_crewai_tools.py])
- **Concept**: Equipping agents with Python functions decorated with `@tool` to perform calculations, database queries, or API calls instead of hallucinating.
- **Key Code**:
  ```python
  from crewai.tools import tool

  @tool("Stock Return Calculator")
  def calculate_roi(initial_investment: float, years: int, annual_rate: float) -> str:
      """Calculates future value and total ROI of an investment."""
      ...

  quant_analyst = Agent(..., tools=[calculate_roi])
  ```

---

### 2. Structured Pydantic Output ([10_crewai_structured_output.py])
- **Concept**: Instead of unstructured Markdown strings, force tasks to return validated Pydantic models with `output_pydantic`.
- **Key Code**:
  ```python
  from pydantic import BaseModel

  class FeedbackAnalysis(BaseModel):
      product_name: str
      sentiment: str
      satisfaction_score: int
      key_highlights: list[str]
      recommended_action: str

  analysis_task = Task(..., output_pydantic=FeedbackAnalysis)
  result = crew.kickoff(...)
  parsed_data = result.pydantic  # Access as Python object or result.pydantic.model_dump_json()
  ```

---

### 3. Human-in-the-Loop ([11_crewai_human_in_the_loop.py])
- **Concept**: Enable `human_input=True` on critical tasks to pause execution and prompt the human reviewer in the terminal for feedback or approval before completing.
- **Key Code**:
  ```python
  draft_task = Task(
      description="Write an engaging LinkedIn announcement...",
      expected_output="A ready-to-publish post...",
      agent=copywriter,
      human_input=True  # Pauses in terminal for human feedback!
  )
  ```

---

### 4. Hierarchical Process with Manager ([12_crewai_hierarchical.py])
- **Concept**: Instead of linear step-by-step handoffs, a Manager LLM coordinates the crew, decides who executes what, evaluates quality, and delivers the final synthesis.
- **Key Code**:
  ```python
  crew = Crew(
      agents=[architect, security_specialist],
      tasks=[architecture_task, security_task],
      process=Process.hierarchical,  # Manager coordinates
      manager_llm=llm,               # Manager model
  )
  ```


