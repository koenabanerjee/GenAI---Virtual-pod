# Enhanced Streamlit UI - Real-Time SDLC Artifact Display

## Overview

The Virtual Development Pod's Streamlit UI has been enhanced to display **all generated outputs in real-time** as the SDLC pipeline executes. Instead of artifacts being saved only to disk, they are now rendered interactively in the browser for immediate viewing and analysis.

---

## Architecture

### Components

#### 1. **streamlit_app.py** - Main UI Application
- **Purpose**: Orchestrates the entire Streamlit interface
- **Features**:
  - Real-time progress tracking with visual indicators
  - File upload for RFI/PDF documents
  - SDLC pipeline execution
  - Interactive artifact display

#### 2. **ui_helpers.py** - Display Functions
- **Purpose**: Modular helper functions for rendering artifacts
- **Functions**:
  - `display_user_stories()` - Render user stories with acceptance criteria
  - `display_ui_mockups()` - Show wireframes and HTML mockups
  - `display_design_specifications()` - Render architecture documents
  - `display_generated_code()` - Show Python source code with syntax highlighting
  - `display_generated_tests()` - Display test suites
  - `display_test_execution_report()` - Show test results and metrics
  - `display_run_summary()` - Summary statistics and metadata

### Data Flow

```
User Input (Requirements)
    ↓
[Click: Run End-to-End SDLC]
    ↓
VirtualDevelopmentPod.run_sdlc()
    ├─ Business Analyst → User Stories (saved + returned)
    ├─ UI Designer → Mockups (saved + returned)
    ├─ Designer → Design Specs (saved + returned)
    ├─ Developer → Code (saved + returned)
    ├─ Tester → Tests (saved + returned)
    └─ PM → Summary (saved + returned)
    ↓
RunResult object with all artifacts
    ↓
Streamlit displays all artifacts in real-time
```

---

## UI Layout

### Main Sections

#### 1. **Left Panel: Input**
- Project name input
- Requirements textarea (or upload RFI/PDF)
- "Run End-to-End SDLC" button
- LLM configuration options

#### 2. **Right Panel: Progress**
- Pipeline progress bar (0-100%)
- Stage status with indicators (completed/in_progress/pending)
- Artifact count metrics (Stories, Designs, Code, Tests, UI Pages)
- Test pass rate
- Run ID and artifacts directory

#### 3. **Main Content: Tabbed Artifacts View**

Seven organized tabs display all outputs:

| Tab | Content | Features |
|-----|---------|----------|
| **User Stories** | Generated requirements | Expandable cards, persona, acceptance criteria |
| **UI Mockups** | Wireframes & design | Specification document, interactive HTML preview |
| **Design Specs** | Architecture document | Components, design patterns, system design |
| **Generated Code** | Python source code | Syntax highlighting, module organization |
| **Tests** | Test suites | Test cases, coverage focus, test code |
| **Test Report** | Test results & metrics | Pass/fail statistics, bug summary, error logs |
| **Summary** | Run overview | Artifact counts, LLM config, run metadata |

#### 4. **Bottom: Agent Activity Log**
- Collapsible view of live agent execution steps
- Useful for debugging and monitoring

#### 5. **Chat Interface: PM Chatbot**
- Ask questions about the SDLC run
- Get insights on quality, risks, and progress

---

## Key Features

### 1. Real-Time Display
- **Event Callback System**: As each agent completes a stage, outputs are immediately displayed
- **Live Progress**: Progress bar updates as stages complete
- **Streaming Updates**: Agent activity logs appear in real-time

### 2. Rich Content Rendering
- **Markdown**: Design specifications and user stories
- **Code Syntax Highlighting**: Python code with color coding
- **Interactive HTML**: UI mockups with full interactivity
- **Metrics & Cards**: Statistics displayed as visual widgets
- **Expandable Sections**: Detailed content hidden by default, expandable on demand

### 3. File Access
- **Direct File Reading**: All content read from artifact directories
- **Graceful Fallback**: Displays "file not found" messages if paths are missing
- **Encoded Paths**: Handles special characters in filenames

### 4. Responsive Design
- **Multi-column layouts**: Organize content efficiently
- **Tabbed interface**: Organize related artifacts
- **Collapsible sections**: Progressive disclosure of details
- **Metrics dashboard**: Visual summaries

---

## Usage Example

### 1. Start the Streamlit App
```bash
cd GenAI---Virtual-pod
streamlit run app/streamlit_app.py
```

### 2. Enter Requirements
```
Project Name: task-management-app
Requirements: Create a task management system with todo list, 
             reminders, and progress tracking features.
             Users should be able to create, edit, delete tasks.
             Each task has priority, due date, and status.
```

### 3. (Optional) Upload RFI Document
- Click "Upload requirement document"
- Select PDF, TXT, or MD file
- System auto-extracts requirements
- Pre-fills the requirements text area

### 4. Run Pipeline
- Click "Run End-to-End SDLC"
- Monitor progress bar in real-time
- Watch stage status update from pending → in_progress → completed
- View agent activity log for execution details

### 5. View Artifacts as They're Generated
As pipeline runs, tabs populate with:
- User stories appear first (Analysis stage)
- Design specs appear (Design stage)
- Code appears (Development stage)
- Tests appear (Testing stage)
- Test results & report appear (after execution)

### 6. Interact with Results
- **Expand/collapse** any section for more/less detail
- **Copy code** from syntax-highlighted blocks
- **Link to artifacts** directory for file access
- **Ask PM** questions about quality and risks

---

## File Structure

### Artifact Directories

```
artifacts/{run_id}/
├── analysis/
│   ├── user_stories.md              # All user stories
│   └── original_input/              # Original uploaded RFI (if provided)
├── ui/
│   ├── ui_spec.md                   # UI specification
│   ├── pages.json                   # Page hierarchy
│   └── mockups/
│       └── {page_name}.html         # Interactive mockup
├── design/
│   └── {story_name}_design.md       # Design document
├── development/
│   └── generated_app/
│       ├── __init__.py
│       └── {story_name}.py          # Generated module
├── testing/
│   └── tests/
│       ├── test_{story_name}.py     # Unit tests
│       └── test_integration_generated_app.py
├── reports/
│   ├── test_report.txt              # Test summary
│   └── bug_summary.txt              # Issues found
└── run_metadata.json                # Complete run metadata
```

---

## Code Organization

### streamlit_app.py Structure
```python
# 1. Imports and setup
# 2. Configuration functions (progress, env vars, etc.)
# 3. Pod initialization and session state setup
# 4. Settings sidebar (left panel)
# 5. Input and progress panels (left + right)
# 6. Main artifact display (tabbed interface)
# 7. PM chatbot (bottom section)
```

### ui_helpers.py Functions
```python
display_user_stories()              # Tab 1
display_ui_mockups()                # Tab 2
display_design_specifications()     # Tab 3
display_generated_code()            # Tab 4
display_generated_tests()           # Tab 5
display_test_execution_report()     # Tab 6
display_run_summary()               # Tab 7
```

---

## Customization

### Add New Display Section

1. **Create a helper function** in `ui_helpers.py`:
```python
def display_custom_artifact(artifacts: list[CustomArtifact]) -> None:
    """Display custom artifacts."""
    for artifact in artifacts:
        st.write(f"Custom: {artifact.name}")
```

2. **Add a new tab** in `streamlit_app.py`:
```python
artifact_tabs = st.tabs([
    # ... existing tabs ...
    "🎯 Custom"
])

with artifact_tabs[7]:
    st.subheader("Custom Artifacts")
    display_custom_artifact(run_result.custom_artifacts)
```

### Modify Styling

- **Colors**: Edit CSS in HTML mockups (in `ui_designer.py`)
- **Icons**: Replace emoji in tab names
- **Layout**: Adjust column widths and expanders
- **Themes**: Use `st.set_page_config(theme="...")`

---

## Performance Considerations

### Efficient File Reading
- Files are read **only when tab is opened** (lazy loading)
- Large files displayed in **collapsible sections**
- Syntax highlighting handled by Streamlit (optimized)

### Caching (Optional)
To improve performance with large runs, add caching:
```python
@st.cache_data
def load_artifact_file(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")
```

### Streaming Updates
- Event callback system prevents UI blocking
- Agent activity updates in real-time
- Progress uses `st.progress()` for smooth rendering

---

## Troubleshooting

### Issue: Empty Tab
**Cause**: No artifacts generated for that stage
**Solution**: Check agent logs, ensure requirements are specific

### Issue: File Not Found
**Cause**: Agent generated artifact metadata but file missing
**Solution**: Verify artifact directory permissions and disk space

### Issue: HTML Mockup Not Rendering
**Cause**: Invalid HTML or special characters
**Solution**: Check HTML file manually, regenerate if needed

### Issue: UI Freezes During Run
**Cause**: Long-running agents blocking main thread
**Solution**: Already handled! Uses threading - check agent logs if stuck

---

## Integration with Existing System

### Compatible With:
- Workflow.py (6-stage SDLC pipeline)
- All 6 agents (BA, UI Designer, Designer, Developer, Tester, PM)
- Mock LLM (for development/testing)
- HuggingFace LLM (for production)
- ChromaDB embeddings (optional)
- RFI parsing (PDF/TXT/MD upload)
- Test execution & reporting

### No Breaking Changes
- All existing functionality preserved
- Backward compatible with previous runs
- No changes to core agent logic or data structures

---

## Future Enhancements

Potential additions (not yet implemented):
- Real-time code diff viewer
- Interactive component library explorer
- Dependency graph visualization
- Test coverage heatmap
- Cost estimation for LLM usage
- Dark mode toggle
- Export entire run as PDF report
- Side-by-side diff of multiple runs

---

## Summary

The enhanced Streamlit UI provides a **complete, interactive view of the SDLC pipeline** with:

Real-time artifact display as generated
Organized tabbed interface with 7 sections
Live progress visualization
Rich content rendering (markdown, code, HTML, metrics)
Modular helper functions for easy customization
Direct artifact file access
PM chatbot for insights

Users can now experience the entire software development process **visually** from requirements to deployed code, all within a single unified interface.
