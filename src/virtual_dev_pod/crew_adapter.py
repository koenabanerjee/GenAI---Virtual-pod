from __future__ import annotations

import os


class CrewAIPlanner:
    def __init__(self, enabled: bool):
        self.enabled = enabled
        self._available = self._check_crewai()

    def create_handoff_plan(self, requirements: str) -> str:
        if not self.enabled:
            return "CrewAI handoff planning is disabled."
        if not self._available:
            return "CrewAI is not installed; native orchestrator was used."

        if not _has_any_llm_key():
            return "CrewAI enabled but no provider API key found; planning skipped."

        try:  # pragma: no cover - dependency boundary
            from crewai import Agent, Crew, Process, Task

            ba = Agent(
                role="Business Analyst Agent",
                goal="Structure business requirements into actionable user stories",
                backstory="Senior BA used to enterprise templates",
                verbose=False,
            )
            dev = Agent(
                role="Developer Agent",
                goal="Translate stories into implementation-ready modules",
                backstory="Backend engineer focused on traceability and quality",
                verbose=False,
            )
            qa = Agent(
                role="Testing Agent",
                goal="Design robust tests and risk-based validation",
                backstory="Quality engineer specializing in automation",
                verbose=False,
            )
            pm = Agent(
                role="Project Manager Agent",
                goal="Create execution handoff plan and stage controls",
                backstory="Project lead who tracks SDLC quality gates",
                verbose=False,
            )

            task = Task(
                description=(
                    "Create a concise SDLC handoff plan for BA->DEV->QA->PM. "
                    "Reference this requirement:\n"
                    f"{requirements}"
                ),
                expected_output=(
                    "Markdown handoff checklist with stage goals, inputs, outputs, and risks."
                ),
                agent=pm,
            )
            crew = Crew(
                agents=[ba, dev, qa, pm],
                tasks=[task],
                process=Process.sequential,
                verbose=False,
            )
            result = crew.kickoff()
            return str(result)
        except Exception as exc:
            return f"CrewAI planning failed: {exc}"

    def _check_crewai(self) -> bool:
        try:
            import crewai  # noqa: F401

            return True
        except Exception:
            return False


def _has_any_llm_key() -> bool:
    return any(
        [
            os.getenv("OPENAI_API_KEY"),
            os.getenv("ANTHROPIC_API_KEY"),
            os.getenv("GROQ_API_KEY"),
            os.getenv("MISTRAL_API_KEY"),
            os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        ]
    )
