# AI-Powered Virtual Development Pod

An **AI-driven multi-agent SDLC automation platform** that simulates a real software development team to transform business requirements into fully functional software artifacts including user stories, UI mockups, design specifications, source code, and test reports.

The system orchestrates multiple AI agents to automate the **entire Software Development Life Cycle (SDLC)** from requirements analysis to testing and project evaluation.

---

# Project Overview

Traditional software development requires collaboration between multiple roles such as business analysts, designers, developers, testers, and project managers. This project simulates these roles using **specialized AI agents** working in a coordinated pipeline.

The platform automatically converts **high-level business requirements into structured development artifacts** while providing a **real-time Streamlit dashboard** to monitor the progress of each development stage.

---

# System Architecture

The system follows a **multi-agent orchestration architecture**.

Requirements Input
↓
Business Analyst Agent → User Stories
↓
UI Designer Agent → UI Mockups
↓
Design Agent → Architecture Specifications
↓
Developer Agent → Source Code
↓
Testing Agent → Test Cases & Reports
↓
Product Manager Agent → Project Summary & Quality Analysis

All generated artifacts are displayed through a **Streamlit dashboard**.

---

# AI Agents

### Business Analyst Agent

* Analyzes business requirements
* Converts them into structured user stories
* Defines acceptance criteria and priorities

### UI Designer Agent

* Converts user stories into UI wireframes
* Generates HTML mockups and UI specifications

### Design Agent

* Creates system architecture and design documents
* Defines components and module structure

### Developer Agent

* Generates Python source code modules
* Implements functionality based on user stories and design specifications

### Testing Agent

* Creates unit and integration tests
* Executes tests and generates reports

### Product Manager Agent

* Evaluates project artifacts
* Provides quality analysis and project summaries
* Enables chatbot-based project queries

---

# Key Features

* Multi-agent AI-driven SDLC automation
* Automated user story generation
* AI-generated UI wireframes and mockups
* Automatic code generation
* Auto test generation and execution
* Real-time Streamlit dashboard
* RFI / PDF requirement input
* Artifact traceability and storage
* Retrieval-Augmented Generation using vector store
* Interactive Product Manager chatbot

---

# Technology Stack

Language
Python 3.13

Frameworks
Streamlit
LangChain
HuggingFace Transformers

Libraries
PyPDF2
ChromaDB
Pytest

Architecture
Multi-Agent AI Pipeline

---

# Project Structure

```
GenAI---Virtual-pod
│
├── src/
│   └── virtual_dev_pod/
│       ├── agents/
│       ├── workflow.py
│       ├── models.py
│       ├── llm_factory.py
│       ├── vector_store.py
│       └── rfi.py
│
├── app/
│   └── streamlit_app.py
│
├── tests/
│
├── run_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/koenabanerjee/GenAI---Virtual-pod.git
cd GenAI---Virtual-pod
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Streamlit UI

```bash
streamlit run app/streamlit_app.py
```

The dashboard will open in your browser where you can:

* Upload requirement documents
* Run the SDLC pipeline
* Monitor agent progress
* View generated artifacts
* Interact with the Product Manager chatbot

---

# CLI Usage

You can also run the pipeline using the command line:

```bash
python run_pipeline.py \
--rfi-file requirements.pdf \
--project-name my-project
```

---

# Output Artifacts

Each execution generates structured artifacts stored in the **artifacts folder**.

```
artifacts/
  run_id/
    analysis/
    ui_design/
    design/
    development/
    testing/
    reports/
```

Artifacts include:

* User Stories
* UI Mockups
* Design Documents
* Source Code
* Test Suites
* Execution Reports

---

# Future Enhancements

* GitHub repository auto-generation
* CI/CD pipeline integration
* Multi-language code generation
* Deployment automation
* Figma UI design generation
* Advanced project analytics dashboard

---

# Author
Koena Banerjee
Shreyasi Datta
Rohit Roy
Rikta Pati
BTech Computer Science Engineering

---

# License

This project is developed for **academic and research purposes**.


