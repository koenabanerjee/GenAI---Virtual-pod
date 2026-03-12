# Enhanced Streamlit UI - Quick Start Guide

## Getting Started

### Step 1: Launch the App
```bash
cd /path/to/GenAI---Virtual-pod
streamlit run app/streamlit_app.py
```

Open browser to: `http://localhost:8501`

---

## What You'll See

### Layout: Three Main Areas

```
┌─────────────────────────────────────────────────────────────┐
│                  AI Virtual Development Pod                 │
└─────────────────────────────────────────────────────────────┘
┌──────────────────────────┬──────────────────────────────────┐
│                          │                                  │
│   LEFT PANEL             │    RIGHT PANEL                   │
│   • Settings             │    • Progress Bar (0-100%)       │
│   • Project Name         │    • Stage Status (completed/in_progress/pending)     │
│   • Requirements         │    • Artifact Counts             │
│   • Upload RFI           │    • Test Results                │
│   • Run Button           │    • Run ID                      │
│                          │                                  │
└──────────────────────────┴──────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  7 TABS: User Stories | UI | Design | Code | Tests | Report│
│  Full interactive artifact display with expandable sections │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  PM Chatbot: Ask questions about quality, risks, progress   │
└─────────────────────────────────────────────────────────────┘
```

---

## Tab 1: User Stories

**What you see:**
```
Generated User Stories

[1. User Can Create Tasks] (ID: US-001)
  ▼ Persona: Developer
    Priority: High
    Goal: Create new tasks quickly
    Benefit: Organize work effectively
    Acceptance Criteria:
    • User can input task title and description
    • Task is saved in the system
    • User receives confirmation

[2. User Can Set Reminders] (ID: US-002)
  ...
```

**Features:**
- Expandable cards (first expanded by default)
- Persona, priority, goal, benefit visible
- Full acceptance criteria listed
- Full markdown export available

---

## Tab 2: UI Mockups

**What you see:**
```
Generated UI Mockups & Wireframes

┌─ UI Design Specification ─────────────────────┐
│ # UI Specification                            │
│ ## Navigation                                 │
│ Top navbar links to main pages...             │
│ ## Color Scheme                               │
│ #007bff (primary), #6c757d (secondary)...     │
└───────────────────────────────────────────────┘

Dashboard    List View    Task Form

┌─ Dashboard ─────────────────────────────────┐
│ Components:                   Layout:        │
│ • Navigation Bar             Left sidebar    │
│ • Header                     Main content    │
│ • Main Content Area          on right        │
│ • Sidebar                                    │
│ ┌─ Interactive HTML Preview ──────────────┐ │
│ │ [Live HTML Mockup Rendered Here]        │ │
│ │ • Full CSS styling applied              │ │
│ │ • Responsive design                     │ │
│ │ • Interactive on hover                  │ │
│ └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Features:**
- Full UI specification document
- Multiple pages in tabs
- Interactive HTML preview (800px height)
- Layout descriptions
- Component lists

---

## Tab 3: Design Specifications

**What you see:**
```
Architecture & Design Specifications

[1. System Architecture for Task Management] (Story: US-001)
  ▼
  Summary: Scalable architecture supporting multi-user task management
  
  # System Design
  ## Components
  - TaskController: Handles CRUD operations
  - TaskRepository: Database abstraction
  - NotificationService: Handles reminders
  
  ## Database Schema
  CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    ...
  )
```

**Features:**
- Markdown-formatted design documents
- Architecture diagrams and schemas
- Design patterns and best practices
- Story-linked to understand context

---

## Tab 4: Generated Code

**What you see:**
```
Generated Python Source Code

┌─ task_management_system.py ─────────────────┐
│ Story ID: US-001                            │
│ Summary: Core task management module        │
│                                             │
│ class TaskController:                       │
│     """Handles task CRUD operations."""     │
│     def create_task(self, title, desc):     │
│         ...                                 │
│     def get_tasks(self):                    │
│         ...                                 │
│     def update_task(self, task_id, data):   │
│         ...                                 │
│     def delete_task(self, task_id):         │
│         ...                                 │
└─────────────────────────────────────────────┘

┌─ notification_service.py ──────────────────┐
│ Story ID: US-002                            │
│ Summary: Reminder and notification system   │
│ ...                                         │
└─────────────────────────────────────────────┘
```

**Features:**
- Syntax-highlighted Python code
- Code organized by module/story
- Copy-paste ready
- Line numbers and formatting preserved

---

## Tab 5: Tests

**What you see:**
```
Generated Unit & Integration Tests

┌─ test_task_management_system.py ───────────┐
│ Story ID: US-001                            │
│ Focus: Task creation, retrieval, deletion   │
│                                             │
│ def test_create_task():                     │
│     controller = TaskController()           │
│     task = controller.create_task(          │
│         "Buy groceries", "For dinner"       │
│     )                                       │
│     assert task.title == "Buy groceries"    │
│     assert task.id is not None              │
│                                             │
│ def test_get_tasks():                       │
│     ...                                     │
└─────────────────────────────────────────────┘

┌─ test_notification_service.py ─────────────┐
│ Story ID: US-002                            │
│ Focus: Reminder scheduling, delivery       │
│ ...                                         │
└─────────────────────────────────────────────┘
```

**Features:**
- Full test code with setup and assertions
- Coverage focus documented
- Integration tests included
- Ready to run with pytest

---

## Tab 6: Test Report

**What you see:**
```
Test Execution Results

┌──────────┬────────┬──────────┬──────────┐
│ Passed   │ Failed │ Skipped  │ Status   │
├──────────┼────────┼──────────┼──────────┤
│    12    │   0    │    2     │ Success  │
└──────────┴────────┴──────────┴──────────┘

┌─ Full Test Report ───────────────────────┐
│ ============ test session starts ==========  │
│ collected 14 items                        │
│                                           │
│ tests/test_task_mgmt.py .............  [100%]│
│                                           │
│ ============= 12 passed, 2 skipped ======== │
│ ============== in 2.34s ================   │
└─────────────────────────────────────────────┘

┌─ Bug Summary ────────────────────────────┐
│ No critical bugs found                    │
│ Minor issues:                             │
│ • Consider adding input validation       │
│ • Add logging to notification service    │
└─────────────────────────────────────────────┘

┌─ Test Output (stdout) ───────────────────┐
│ Running tests with coverage...            │
│ Coverage: 87% lines, 92% branches        │
└─────────────────────────────────────────────┘
```

**Features:**
- Test statistics as metrics (Passed, Failed, Skipped)
- Full test report text
- Bug summary extracted
- stdout/stderr logs
- Return code displayed

---

## Tab 7: Summary

**What you see:**
```
SDLC Run Summary

┌──────────────────┬──────────────────┬──────────────────┐
│ Run ID           │ Project          │ Status           │
├──────────────────┼──────────────────┼──────────────────┤
│ 20260311_193643_ │ task-mgmt-system │ Completed    │
│ enhanced_ui_test │                  │                  │
└──────────────────┴──────────────────┴──────────────────┘

Run Details:
  Stories: 1              UI Pages: 1
  Designs: 1              Tests: 5
│  Code: 1                 Passed: 12

LLM Configuration:
  Provider: langchain_hf_endpoint
  Model: mistralai/Mistral-7B-Instruct-v0.2
  Mock: false

Artifacts: /artifacts/20260311_193643.../
```

**Features:**
- Run metadata and identifiers
- Artifact count summary
- LLM configuration details
- Link to artifacts directory

---

## Right Panel: Real-Time Progress

**During Execution:**
```
🚀 Pipeline Progress

████████░░░░░░░░░░░░░░░░░░░░ 35%

Stage Status:
📝 analysis        → ✅ completed
ui_design       → in_progress
design          → pending
development     → pending
testing         → pending
management       → pending

📦 Generated Artifacts:
  📝 Stories: 1       💻 Code: 0
  🏗️ Designs: 0       🧪 Tests: 0
  🎨 UI Pages: 0

Run ID: 20260311_193643_enhanced_ui_test
```

**After Completion:**
```
🚀 Pipeline Progress

████████████████████████████████ 100%

Stage Status:
📝 analysis        → ✅ completed
🎨 ui_design       → ✅ completed
🏗️ design          → ✅ completed
💻 development     → ✅ completed
🧪 testing         → ✅ completed
👨‍💼 management       → ✅ completed

📦 Generated Artifacts:
  📝 Stories: 1       💻 Code: 1
  🏗️ Designs: 1       🧪 Tests: 5
  🎨 UI Pages: 1      ✅ Passed: 12
```

---

## 💬 PM Chatbot (Bottom)

**Ask questions like:**

```
User: "How many tests passed?"
→ PM: "Tests executed: 12 passed, 0 failed, 2 skipped."

User: "Are there any quality issues?"
→ PM: "Overall code quality is good. Minor issues found in 
      error handling. Test coverage is at 87%."

User: "What's the project status?"
→ PM: "All 6 SDLC stages completed successfully. Artifacts 
      are ready for deployment."

User: "Can you explain the architecture?"
→ PM: "The system uses a controller-repository pattern for 
      task management with a separate notification service..."
```

---

## ⚙️ Settings Panel (Left Sidebar)

```
LLM Settings
  Provider: [Dropdown]
  - langchain_hf_endpoint
  - langchain_hf_local
  - mock
  
  Model ID: mistralai/Mistral-7B-Instruct-v0.2
  HF API Token: [Masked password input]
  Require Real LLM: [Checkbox]
  
  [Apply LLM Settings]

Execution Settings
  ☑ Fast Mode (reduced latency)
  ☑ Execute Tests
  ☐ Use ChromaDB Embeddings
  Max User Stories: [Slider 1-8] → 5
```

---

## 🎬 Full Example Walkthrough

### Scenario: Build a Weather Tracking App

**1. Start app**
```bash
streamlit run app/streamlit_app.py
```

**2. Enter requirements**
```
Project Name: weather-tracker-app
Requirements: 
  Build a real-time weather tracking application that:
  - Displays current weather for user's location
  - Shows 7-day forecast
  - Sends alerts for severe weather
  - Allows users to bookmark favorite locations
  - Provides historical weather data
```

**3. Click "Run End-to-End SDLC"**
- Progress bar appears (0%)
- Stage status shows: analysis → ⏳ in_progress

**4. Watch in real-time:**
- ✅ Analysis complete → User stories appear in Tab 1
- ✅ UI Design complete → Mockups appear in Tab 2
- ✅ Design complete → Architecture appears in Tab 3
- ✅ Development complete → Code appears in Tab 4
- ✅ Testing complete → Tests appear in Tab 5
- ✅ Report complete → Results appear in Tab 6
- Progress bar reaches 100%

**5. Explore artifacts:**
- Review user stories for requirements coverage
- Look at UI mockups to visualize the app
- Study design patterns and architecture
- Read generated Python code
- Run tests mentally or copy to your IDE
- Check test report for quality metrics

**6. Chat with PM:**
```
"What's the code quality?"
→ "87% test coverage, all tests passing, 0 critical bugs."

"Can you summarize the API endpoints?"
→ "GET /weather/{location} - Current weather
   GET /weather/{location}/forecast - 7-day forecast
   POST /alerts - Create weather alert
   ..."
```

**7. Download artifacts**
```
Click on "Artifacts: /artifacts/20260311_193643_..." 
to access directory with:
- Generated source code
- Test files
- Design documents
- Full documentation
```

---

## 🔧 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Refresh UI | `R` (Streamlit) |
| Clear cache | `C` (Streamlit) |
| Expand all | N/A (use expanders) |
| Copy code block | Click copy icon (top-right of code) |

---

## 💡 Tips & Tricks

1. **Large Runs:** Use "Fast Mode" to reduce latency
2. **PDF Upload:** Automatically extracts requirements
3. **Code Reuse:** Copy generated code directly into IDEs
4. **Testing:** Generated tests are production-ready
5. **Debugging:** Check agent activity log for execution flow
6. **Loop Back:** Create new run using generated code as spec

---

## 🆘 Common Questions

**Q: Why is a tab empty?**
A: That stage hasn't completed yet. Wait or check agent logs.

**Q: Can I download all artifacts?**
A: Yes! Access the artifacts directory shown in Summary tab.

**Q: Is the generated code production-ready?**
A: It's a solid foundation. Review, test, and customize for your needs.

**Q: Can I modify the requirements and re-run?**
A: Yes! Edit text and click "Run End-to-End SDLC" again.

**Q: How do I use this in CI/CD?**
A: Use `run_pipeline.py` CLI instead of Streamlit for automation.

---

## 🎉 You're Ready!

Start exploring the enhanced UI now. Happy developing! 🚀
