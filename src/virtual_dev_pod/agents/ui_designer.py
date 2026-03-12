from __future__ import annotations

import json
from pathlib import Path

from virtual_dev_pod.agents.base import BaseAgent
from virtual_dev_pod.models import UserStory
from virtual_dev_pod.utils import slugify, extract_json_payload


class UIArtifact:
    """Represents a generated UI page/mockup."""

    def __init__(
        self,
        page_name: str,
        components: list[str],
        layout_description: str,
        html_content: str,
        story_id: str | None = None,
    ):
        self.page_name = page_name
        self.components = components
        self.layout_description = layout_description
        self.html_content = html_content
        self.story_id = story_id

    def to_dict(self) -> dict:
        return {
            "page_name": self.page_name,
            "components": self.components,
            "layout_description": self.layout_description,
            "story_id": self.story_id,
        }


class UIDesignerAgent(BaseAgent):
    """Generates UI mockups and wireframes from user stories."""

    def generate_ui_artifacts(
        self, stories: list[UserStory], *, output_dir: Path
    ) -> list[UIArtifact]:
        """Generate UI specs and HTML mockups for user stories.

        Args:
            stories: List of user stories from Business Analyst
            output_dir: Directory to save UI artifacts

        Returns:
            List of UIArtifact objects
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate UI specification and page list
        ui_spec, pages_data = self._generate_ui_spec(stories)

        # some LLM responses (or legacy fallbacks) may return a single page
        # without wrapping it in a `pages` array.  normalize to always have
        # a top‑level `pages` key so downstream code can iterate safely.
        if isinstance(pages_data, dict) and "pages" not in pages_data:
            # assume the dict itself describes one page
            single = pages_data.copy()
            # retain any navigation/color/typography if present
            pages_data = {
                "pages": [
                    {
                        "name": single.get("name"),
                        "story_id": single.get("story_id"),
                        "components": single.get("components", []),
                        "layout": single.get("layout", ""),
                        "description": single.get("description", ""),
                    }
                ],
                "navigation": single.get("navigation", ""),
                "color_scheme": single.get("color_scheme", ""),
                "typography": single.get("typography", ""),
            }

        # Save UI specification
        ui_spec_path = output_dir / "ui_spec.md"
        ui_spec_path.write_text(ui_spec, encoding="utf-8")

        # Save pages JSON
        pages_json_path = output_dir / "pages.json"
        pages_json_path.write_text(
            json.dumps(pages_data, indent=2), encoding="utf-8"
        )

        # Generate HTML mockups for each page
        artifacts: list[UIArtifact] = []
        mockups_dir = output_dir / "mockups"
        mockups_dir.mkdir(parents=True, exist_ok=True)

        for page_info in pages_data.get("pages", []):
            page_name = page_info.get("name", "page")
            components = page_info.get("components", [])
            layout = page_info.get("layout", "")

            # Generate HTML mockup
            html_content = self._generate_html_mockup(
                page_name=page_name,
                components=components,
                layout_description=layout,
            )

            # Save HTML file
            html_filename = f"{slugify(page_name)}.html"
            html_path = mockups_dir / html_filename
            html_path.write_text(html_content, encoding="utf-8")

            # Create artifact
            story_id = page_info.get("story_id")
            artifact = UIArtifact(
                page_name=page_name,
                components=components,
                layout_description=layout,
                html_content=html_content,
                story_id=story_id,
            )
            artifacts.append(artifact)

        return artifacts

    def _generate_ui_spec(
        self, stories: list[UserStory]
    ) -> tuple[str, dict]:
        """Generate UI specification from user stories."""
        stories_text = self._format_stories_for_ui(stories)

        prompt = f"""
You are a professional UI/UX designer specializing in wireframe and mockup generation.

Based on the following user stories, generate a comprehensive UI specification.

User Stories:
{stories_text}

Analyze the stories and determine:
1. What application pages/screens are needed
2. What UI components each page should contain
3. How the pages should be laid out
4. User interaction flows

Return ONLY valid JSON (no markdown, no code blocks) with this exact structure:
{{
  "pages": [
    {{
      "name": "Page Name",
      "story_id": "US-001",
      "components": ["Component 1", "Component 2"],
      "layout": "Description of layout and positioning",
      "description": "Brief page description"
    }}
  ],
  "navigation": "Description of how users navigate between pages",
  "color_scheme": "Suggested colors",
  "typography": "Font suggestions"
}}

Return ONLY the JSON, nothing else.
"""
        llm_output = self._call_llm(prompt).strip()

        # Try to extract JSON from output
        if llm_output and llm_output != "MOCK_PROVIDER_ACTIVE":
            parsed = extract_json_payload(llm_output)
            if isinstance(parsed, dict):
                pages_data = parsed
            else:
                pages_data = self._fallback_ui_spec(stories)
        else:
            pages_data = self._fallback_ui_spec(stories)

        # Generate markdown spec from pages data
        ui_spec = self._format_ui_spec_markdown(stories, pages_data)

        return ui_spec, pages_data

    def _format_stories_for_ui(self, stories: list[UserStory]) -> str:
        """Format user stories for UI generation prompt."""
        lines = []
        for story in stories:
            lines.append(f"Story ID: {story.story_id}")
            lines.append(f"Title: {story.title}")
            lines.append(f"Persona: {story.persona}")
            lines.append(f"Goal: {story.goal}")
            lines.append(f"Acceptance Criteria:")
            for criterion in story.acceptance_criteria:
                lines.append(f"  - {criterion}")
            lines.append("")
        return "\n".join(lines)

    def _fallback_ui_spec(self, stories: list[UserStory]) -> dict:
        """Generate fallback UI specification when LLM output is unavailable."""
        pages = []
        page_titles = {"login", "dashboard", "profile", "settings", "home"}

        # Create a dashboard page as default
        pages.append(
            {
                "name": "Dashboard",
                "story_id": stories[0].story_id if stories else None,
                "components": [
                    "Navigation Bar",
                    "Header",
                    "Main Content Area",
                    "Sidebar",
                ],
                "layout": "Top navigation bar, left sidebar (navigation), main content area on right",
                "description": "Main dashboard showing overview and key information",
            }
        )

        # Create a list/table page for data
        if len(stories) > 1:
            pages.append(
                {
                    "name": "Items List",
                    "story_id": stories[1].story_id if len(stories) > 1 else None,
                    "components": [
                        "Search Bar",
                        "Filter Panel",
                        "Data Table",
                        "Pagination",
                    ],
                    "layout": "Header with search, left sidebar with filters, main table in center",
                    "description": "Display list of items with filtering and pagination",
                }
            )

        # Create a detail/form page
        if len(stories) > 2:
            pages.append(
                {
                    "name": "Create Item",
                    "story_id": stories[2].story_id if len(stories) > 2 else None,
                    "components": [
                        "Form Fields",
                        "Submit Button",
                        "Cancel Button",
                        "Validation Messages",
                    ],
                    "layout": "Centered form with vertical alignment, buttons at bottom",
                    "description": "Form to create or edit items",
                }
            )

        return {
            "pages": pages,
            "navigation": "Top navbar links to main pages, breadcrumb navigation on detail pages",
            "color_scheme": "#007bff (primary), #6c757d (secondary), #ff6b6b (danger)",
            "typography": "Sans-serif (Arial/Helvetica), 16px base font size",
        }

    def _format_ui_spec_markdown(self, stories: list[UserStory], pages_data: dict) -> str:
        """Format UI specification as markdown."""
        lines = [
            "# UI Specification",
            "",
            "## Overview",
            f"Generated UI specification for {len(stories)} user stories.",
            "",
        ]

        # Navigation section
        lines.append("## Navigation")
        lines.append(pages_data.get("navigation", "TBD"))
        lines.append("")

        # Color scheme
        lines.append("## Color Scheme")
        lines.append(pages_data.get("color_scheme", "TBD"))
        lines.append("")

        # Typography
        lines.append("## Typography")
        lines.append(pages_data.get("typography", "TBD"))
        lines.append("")

        # Pages section
        lines.append("## Pages")
        lines.append("")

        for page in pages_data.get("pages", []):
            lines.append(f"### {page.get('name', 'Untitled Page')}")
            lines.append("")
            lines.append(f"**Description:** {page.get('description', 'N/A')}")
            lines.append("")

            if page.get("story_id"):
                lines.append(f"**Related Story:** {page.get('story_id')}")
                lines.append("")

            lines.append("**Components:**")
            for component in page.get("components", []):
                lines.append(f"- {component}")
            lines.append("")

            lines.append("**Layout:**")
            lines.append(page.get("layout", "N/A"))
            lines.append("")

        return "\n".join(lines)

    def _generate_html_mockup(
        self,
        page_name: str,
        components: list[str],
        layout_description: str,
    ) -> str:
        """Generate a simple HTML mockup for a page."""
        safe_page_name = page_name.replace('"', "&quot;").replace("<", "&lt;")
        safe_layout = layout_description.replace(
            '"', "&quot;"
        ).replace("<", "&lt;")

        # Create a sensible layout based on component count and type
        component_html_list = "\n          ".join(
            f'<div class="component">{comp}</div>'
            for comp in components[:5]  # Limit to 5 components in mockup
        )

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_page_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}

        .navbar {{
            background-color: #007bff;
            color: white;
            padding: 15px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .navbar h1 {{
            font-size: 24px;
            font-weight: 600;
        }}

        .navbar-links {{
            display: flex;
            gap: 20px;
        }}

        .navbar-links a {{
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }}

        .navbar-links a:hover {{
            background-color: rgba(255,255,255,0.2);
        }}

        .container {{
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }}

        .page-title {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
            color: #222;
        }}

        .page-subtitle {{
            font-size: 16px;
            color: #666;
            margin-bottom: 30px;
        }}

        .layout-info {{
            background-color: #e7f3ff;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin-bottom: 30px;
            border-radius: 4px;
        }}

        .layout-info strong {{
            color: #004085;
        }}

        .components-section {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .components-section h2 {{
            font-size: 20px;
            margin-bottom: 20px;
            color: #222;
        }}

        .component {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            margin: 15px 0;
            border-radius: 8px;
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            min-height: 90px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
        }}

        .component:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}

        .component:nth-child(2n) {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}

        .component:nth-child(3n) {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}

        .footer {{
            background-color: #333;
            color: white;
            padding: 20px;
            text-align: center;
            margin-top: 40px;
            border-radius: 4px;
        }}

        .form-demo {{
            max-width: 500px;
            margin: 0 auto;
        }}

        .form-group {{
            margin-bottom: 20px;
        }}

        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #333;
        }}

        .form-group input,
        .form-group textarea,
        .form-group select {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.3s;
        }}

        .form-group input:focus,
        .form-group textarea:focus,
        .form-group select:focus {{
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
        }}

        .btn {{
            display: inline-block;
            padding: 12px 24px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-right: 10px;
        }}

        .btn:hover {{
            background-color: #0056b3;
        }}

        .btn-secondary {{
            background-color: #6c757d;
        }}

        .btn-secondary:hover {{
            background-color: #545b62;
        }}

        .wireframe-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .wireframe-item {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 2px dashed #ddd;
            text-align: center;
            min-height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        @media (max-width: 768px) {{
            .navbar {{
                flex-direction: column;
                gap: 15px;
            }}

            .navbar-links {{
                flex-direction: column;
                width: 100%;
            }}

            .page-title {{
                font-size: 24px;
            }}

            .components-section {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar">
        <h1>Virtual Dev Pod</h1>
        <div class="navbar-links">
            <a href="#home">Home</a>
            <a href="#features">Features</a>
            <a href="#profile">Profile</a>
            <a href="#logout">Logout</a>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container">
        <h1 class="page-title">{safe_page_name}</h1>
        <p class="page-subtitle">UI Wireframe & Mockup Preview</p>

        <!-- Layout Description -->
        <div class="layout-info">
            <strong>Layout:</strong> {safe_layout}
        </div>

        <!-- Components Section -->
        <div class="components-section">
            <h2>Page Components</h2>
            <div class="wireframe-grid">
                {component_html_list}
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>&copy; 2026 AI-Powered Virtual Development Pod. Auto-generated UI Mockup.</p>
        </div>
    </div>
</body>
</html>"""

        return html_template
