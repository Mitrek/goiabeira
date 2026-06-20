# 🌸 Goiabeira - Multi-Agent Control Terminal

Goiabeira is a lightweight, responsive desktop GUI control panel built with Python and PyQt6. It provides a retro terminal-themed dashboard (inspired by the Guava Skin TUI theme) for configuring, monitoring, and simulating multi-agent thread pipelines.

---

## 🗺️ Rationale for Other Agents

If you are an agent tasked with maintaining or extending this repository, here is what you need to know:

### 1. Key Architectural Concepts
- **Frontend-Only Simulation**: No real AI agents are invoked. Instead, it simulates execution step-by-step using a QTimer to show thread lifecycle transitions, token cost generation, and Definition of Done (DoD) verification checklist statuses.
- **Projects Local Storage (`projects.json`)**:
  - The application saves all projects, descriptions, agent rosters, and DoD checklists inside `projects.json` in the root workspace folder.
  - State is loaded dynamically on startup and auto-saved in real-time.
- **Role Constraints**:
  - The topmost agent in the roster is always forced to have the role **`Orchestrator`** (read-only).
  - The Orchestrator defaults to the standard Tech Lead description: `"Coordinates agent threads, architectural design, and system DoD validation checks."`
  - Any subsequent agents spawned have editable roles and descriptions.

### 2. Styling System (QSS)
- Visual styling is strictly managed via the `STYLE_SHEET` QSS string in `main.py`.
- Theme colors match a custom forest dark / guava skin theme:
  - Background: `#0B130C` (Dark forest green-black)
  - Card Panels: `#121E14` (Guava peel panel)
  - Glowing Accents/Borders: `#7CD982` (Guava light green)
  - Text Field Bottom Border: `#3A6B3E` (Leafy green)
  - Highlights: `#1E4221` (Guava dark accent)
  - Subtitles/Alerts: `#FFA39E` (Inner flesh accent)
- Avoid adding standard window borders or default widgets. Use bottom-border inputs and borderless cards.

---

## 🛠️ Repository Layout

- **[main.py](file:///home/mitrek/Desktop/Goiabeira/main.py)**: Monolithic application file containing style definitions, custom PyQt widgets (`AgentConfigRow`, `DodConfigRow`, `TuiStatBox`), dialog modals, and the simulation controller.
- **`projects.json`**: Dynamic monolithic configuration storage. (Generated on first run).
- **`.venv/`**: Local Python virtual environment containing PyQt6 and dependencies.

---

## 🚀 Running the Application

Ensure the virtual environment is used to run the PyQt application:

```bash
.venv/bin/python3 main.py
```

### Managing Projects
- You can create projects using the **`[ + NEW PROJECT ]`** button in the top header.
- You can rename the currently active project directly by editing the text inside the **`PROJECT:`** dropdown box in the header and pressing Enter or clicking away.
