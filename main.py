import sys
import json
import random
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFrame, QStackedWidget,
    QProgressBar, QSplitter, QScrollArea, QLineEdit, QComboBox, QDialog
)
from PyQt6.QtCore import Qt, QTimer, QProcess, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QPixmap, QIcon, QPen, QBrush

PROJECT_ROOT = Path(__file__).parent
PROJECTS_JSON = PROJECT_ROOT / "projects.json"
PYTHON_BIN = PROJECT_ROOT / ".venv" / "bin" / "python3"
RUN_SCRIPT  = PROJECT_ROOT / "run.py"

# ---------------------------------------------------------
# QSS Stylesheet matching Guava Skin CLI / TUI Theme
# ---------------------------------------------------------
STYLE_SHEET = """
QMainWindow {
    background-color: #0B130C;
}

QWidget {
    font-family: "Courier New", "Consolas", "Monospace", monospace;
    color: #E2ECE3;
    background-color: transparent;
}

/* Sidebar Navigation Frame */
QFrame#SidebarFrame {
    background-color: #121E14;
    border-right: 1px solid #3A6B3E;
    min-width: 260px;
    max-width: 260px;
}

QLabel#SidebarLogo {
    font-size: 10px;
    line-height: 1.1;
    font-weight: bold;
    color: #7CD982;
    padding: 15px 5px 5px 25px;
}

QLabel#SidebarSubtitle {
    font-size: 20px;
    color: #FFFFFF;
    font-weight: bold;
    padding: 5px 10px 20px 25px;
}

/* Sidebar Buttons */
QPushButton.SidebarBtn {
    background-color: transparent;
    border: 1px solid transparent;
    color: #8EAE91;
    font-size: 13px;
    text-align: left;
    padding: 10px 15px;
    margin: 4px 10px;
}

QPushButton.SidebarBtn:hover {
    border: 1px dashed #3A6B3E;
    color: #7CD982;
}

QPushButton.SidebarBtn:checked {
    background-color: #1E4221;
    border: 1px solid #7CD982;
    color: #7CD982;
    font-weight: bold;
}

/* Content Area Header */
QFrame#HeaderFrame {
    background-color: #121E14;
    border-bottom: 1px solid #3A6B3E;
    min-height: 60px;
    max-height: 60px;
}

QLabel#HeaderTitle {
    font-size: 14px;
    font-weight: bold;
    color: #7CD982;
}

/* TUI Stat Box */
QFrame.StatCard {
    background-color: #121E14;
    border: 1px solid #3A6B3E;
    padding: 8px 12px;
}

QLabel.StatCardVal {
    font-size: 20px;
    font-weight: bold;
    color: #E2ECE3;
}

QLabel.StatCardTitle {
    font-size: 10px;
    font-weight: bold;
    color: #FFA39E;
    text-transform: uppercase;
}

/* Content Pane Containers */
QFrame.ContentCard {
    background-color: #121E14;
    border: none;
    border-radius: 0px;
    padding: 20px;
    margin-bottom: 15px;
}

QLabel.SectionTitle {
    font-size: 13px;
    font-weight: bold;
    color: #7CD982;
    margin-bottom: 5px;
}

/* Row blocks with highlight indicators */
QFrame.ConfigRow {
    background-color: #111E13;
    border: none;
    border-left: 3px solid #3A6B3E;
    margin-bottom: 8px;
}

QFrame.ConfigRow:hover {
    border-left: 3px solid #7CD982;
    background-color: #152518;
}

/* Inputs and Forms - Sleek bottom-border look */
QLineEdit, QComboBox {
    background-color: #050A05;
    border: none;
    border-bottom: 1px solid #3A6B3E;
    color: #7CD982;
    font-family: "Courier New", "Consolas", monospace;
    font-size: 12px;
    padding: 4px 8px;
    border-radius: 0px;
}

QLineEdit:focus, QComboBox:focus {
    border-bottom: 1px solid #7CD982;
    color: #E2ECE3;
}

QComboBox::drop-down {
    border: none;
    background-color: transparent;
    width: 20px;
}

/* Simulated Terminal View and Inputs */
QTextEdit#ConsoleView, QTextEdit#ProjectDescInput {
    background-color: #050A05;
    color: #7CD982;
    font-family: "Courier New", "Consolas", monospace;
    font-size: 12px;
    border: 1px solid #3A6B3E;
    padding: 10px;
}

QTextEdit#ProjectDescInput:focus {
    border: 1px solid #7CD982;
    color: #E2ECE3;
}

/* Action Buttons */
QPushButton.PrimaryBtn {
    background-color: transparent;
    color: #7CD982;
    border: 1px solid #3A6B3E;
    padding: 6px 12px;
    font-weight: bold;
    font-size: 11px;
    border-radius: 0px;
}

QPushButton.PrimaryBtn:hover {
    background-color: #1E4221;
    border-color: #7CD982;
    color: #7CD982;
}

QPushButton.SecondaryBtn {
    background-color: transparent;
    color: #8EAE91;
    border: 1px solid #223F25;
    padding: 6px 12px;
    font-weight: bold;
    font-size: 11px;
    border-radius: 0px;
}

QPushButton.SecondaryBtn:hover {
    border: 1px solid #3A6B3E;
    color: #7CD982;
}

QPushButton.DestructiveBtn {
    background-color: transparent;
    color: #FFA39E;
    border: 1px solid #5A2E2C;
    padding: 6px 12px;
    font-size: 11px;
    font-weight: bold;
    border-radius: 0px;
}

QPushButton.DestructiveBtn:hover {
    background-color: #2D1413;
    border-color: #FFA39E;
    color: #FFA39E;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #3A6B3E;
    border-radius: 0px;
    text-align: center;
    background-color: #050A05;
    font-weight: bold;
    color: #E2ECE3;
    height: 18px;
}

QProgressBar::chunk {
    background-color: #1E4221;
    border-right: 1px solid #7CD982;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background: #0B130C;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #3A6B3E;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #7CD982;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
"""

TREE_ASCII = """\
       _-_
     /~~   ~~\\
  /~~         ~~\\
 {               }
  \\  _-     -_  /
    ~  \\\\ //  ~
        | |
        | |
       // \\\\
"""

# Helper to create programmatic pixel art icons for sources
def make_source_icon(char, color_hex):
    pix = QPixmap(18, 18)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    
    # Draw simple retro frame
    painter.setPen(QPen(QColor("#3A6B3E"), 1))
    painter.setBrush(QBrush(QColor("#050A05")))
    painter.drawRect(0, 0, 17, 17)
    
    # Draw character symbol
    painter.setPen(QColor(color_hex))
    painter.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
    painter.drawText(pix.rect(), Qt.AlignmentFlag.AlignCenter, char)
    painter.end()
    return QIcon(pix)

# ---------------------------------------------------------
# Dynamic Configuration Forms Widgets
# ---------------------------------------------------------
class RetroAvatar(QWidget):
    """Draws a monospaced ASCII-style avatar."""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = f"[{text[:2].upper()}]"
        self.setFixedSize(50, 30)

    def paintEvent(self, event):
        painter = QPainter(self)
        font = QFont("Courier New", 12, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#7CD982"))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text)

class AgentSpawnDialog(QDialog):
    def __init__(self, parent=None, is_first=False):
        super().__init__(parent)
        self.setWindowTitle("SPAWN THREAD DAEMON")
        self.setMinimumWidth(450)
        
        self.setStyleSheet(STYLE_SHEET + "\nQDialog { background-color: #0B130C; border: 1px solid #3A6B3E; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        title_lbl = QLabel("[SPAWN AGENT THREAD METADATA]")
        title_lbl.setStyleSheet("color: #7CD982; font-weight: bold; font-size: 13px;")
        layout.addWidget(title_lbl)
        
        layout.addWidget(QLabel("AGENT NAME:"))
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("e.g. Goiaba-1")
        layout.addWidget(self.txt_name)
        
        layout.addWidget(QLabel("SOURCE/MODEL:"))
        self.cmb_source = QComboBox()
        self.cmb_source.addItem(make_source_icon("C", "#FFA39E"), "Claude")
        self.cmb_source.addItem(make_source_icon("X", "#7CD982"), "Codex")
        self.cmb_source.addItem(make_source_icon("A", "#E2ECE3"), "Antigravity")
        layout.addWidget(self.cmb_source)
        
        layout.addWidget(QLabel("AGENT ROLE:"))
        self.txt_role = QLineEdit()
        if is_first:
            self.txt_role.setText("Orchestrator")
            self.txt_role.setReadOnly(True)
        else:
            self.txt_role.setPlaceholderText("e.g. Developer")
        layout.addWidget(self.txt_role)
        
        layout.addWidget(QLabel("ROLE DESCRIPTION:"))
        self.txt_desc = QLineEdit()
        if is_first:
            self.txt_desc.setText("Coordinates agent threads, architectural design, and system DoD validation checks.")
        else:
            self.txt_desc.setPlaceholderText("Writes software modules...")
        layout.addWidget(self.txt_desc)
        
        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("[ SUBMIT ]")
        self.btn_submit.setProperty("class", "PrimaryBtn")
        self.btn_submit.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("[ CANCEL ]")
        self.btn_cancel.setProperty("class", "SecondaryBtn")
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_submit)
        layout.addLayout(btn_layout)

class AgentConfigRow(QFrame):
    removed = pyqtSignal(QWidget)
    name_changed = pyqtSignal()
    changed = pyqtSignal()
    
    def __init__(self, name="", source="Codex", role="", desc="", session_id=None, parent=None):
        super().__init__(parent)
        import uuid
        self.session_id = session_id or str(uuid.uuid4())
        self.setProperty("class", "ConfigRow")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        self.avatar = RetroAvatar(role if role else "AG")
        layout.addWidget(self.avatar)
        
        layout.addWidget(QLabel("NAME:"))
        self.txt_name = QLineEdit(name)
        self.txt_name.setPlaceholderText("Name")
        self.txt_name.setFixedWidth(120)
        self.txt_name.textChanged.connect(lambda: self.name_changed.emit())
        self.txt_name.textChanged.connect(lambda: self.changed.emit())
        layout.addWidget(self.txt_name)
        
        layout.addWidget(QLabel("SOURCE:"))
        self.cmb_source = QComboBox()
        self.cmb_source.addItem(make_source_icon("C", "#FFA39E"), "Claude")
        self.cmb_source.addItem(make_source_icon("X", "#7CD982"), "Codex")
        self.cmb_source.addItem(make_source_icon("A", "#E2ECE3"), "Antigravity")
        self.cmb_source.setCurrentText(source)
        self.cmb_source.setFixedWidth(110)
        self.cmb_source.currentIndexChanged.connect(lambda: self.changed.emit())
        layout.addWidget(self.cmb_source)
        
        layout.addWidget(QLabel("ROLE:"))
        self.txt_role = QLineEdit(role)
        self.txt_role.setPlaceholderText("Role")
        self.txt_role.setFixedWidth(120)
        self.txt_role.textChanged.connect(self.update_avatar_tag)
        self.txt_role.textChanged.connect(lambda: self.changed.emit())
        layout.addWidget(self.txt_role)
        
        layout.addWidget(QLabel("DESC:"))
        self.txt_desc = QLineEdit(desc)
        self.txt_desc.setPlaceholderText("Description of duties")
        self.txt_desc.textChanged.connect(lambda: self.changed.emit())
        layout.addWidget(self.txt_desc)
        
        btn_del = QPushButton("[ KILL ]")
        btn_del.setProperty("class", "DestructiveBtn")
        btn_del.clicked.connect(lambda: self.removed.emit(self))
        layout.addWidget(btn_del)

    def update_avatar_tag(self, text):
        tag = text.strip()[:2].upper() if text.strip() else "AG"
        self.avatar.text = f"[{tag}]"
        self.avatar.update()



class TuiStatBox(QFrame):
    def __init__(self, title, val, parent=None):
        super().__init__(parent)
        self.setProperty("class", "StatCard")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setProperty("class", "StatCardTitle")
        self.val_lbl = QLabel(str(val))
        self.val_lbl.setProperty("class", "StatCardVal")
        
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.val_lbl)

    def update_value(self, new_val):
        self.val_lbl.setText(str(new_val))

# ---------------------------------------------------------
# Main Logic & App Window
# ---------------------------------------------------------
class GoiabeiraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goiabeira - Multi-Agent Control Terminal")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(STYLE_SHEET)
        
        # State Data
        self.agent_config_widgets = []
        self.project_description = ""
        
        # Default state values
        self.agent_roles = []
        self.agent_models = {}
        self.agents_data = []
        self.dod_list = []
        
        # Placeholders
        self.lbl_agent_placeholder = None
        
        # Bridge process + live-tail state
        self._process: QProcess | None = None
        self._log_file_offset = 0
        self._poll_timer = QTimer(self)
        self._poll_timer.timeout.connect(self._poll_run_state)

        # Legacy sim state (kept so sim_cost refs elsewhere don't crash)
        self.sim_step = 0
        self.sim_cost = 0.0
        self.sim_tokens = 0
        
        # Projects Dictionary
        self.active_project_name = "Default Project"
        self.projects_dict = {}
        self.loading_project = False
        
        self.init_ui()
        
        # Load local storage
        self.load_projects_from_file()
        
        # Build UI from selected project
        self.load_project_to_ui(self.active_project_name)
        
        # Connect text changed signals to save configuration
        self.txt_project_desc.textChanged.connect(self.on_project_desc_changed)
        self.txt_dod_rules.textChanged.connect(self.on_dod_text_changed)
        
        # Sync vertical scroll bars of DoD rules editor and line numbers
        self.txt_dod_rules.verticalScrollBar().valueChanged.connect(
            self.txt_dod_numbers.verticalScrollBar().setValue
        )
        
        self.sync_monitor_tab()
        self.switch_tab(0)

    def init_ui(self):
        # Central Widget & Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ----------------- SIDEBAR -----------------
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title/Logo ASCII Tree
        logo_lbl = QLabel(TREE_ASCII)
        logo_lbl.setObjectName("SidebarLogo")
        subtitle_lbl = QLabel("GOIABEIRA")
        subtitle_lbl.setObjectName("SidebarSubtitle")
        sidebar_layout.addWidget(logo_lbl)
        sidebar_layout.addWidget(subtitle_lbl)
        
        # Navigation Buttons (Only 2 Tabs)
        self.nav_buttons = []
        navs = [
            (">[01] CONFIGURATION", 0),
            (">[02] MONITOR PANEL", 1)
        ]
        
        for name, idx in navs:
            btn = QPushButton(name)
            btn.setProperty("class", "SidebarBtn")
            btn.setCheckable(True)
            if idx == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, i=idx: self.switch_tab(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        sidebar_layout.addStretch()
        
        # Sidebar Footer
        footer_lbl = QLabel("GOIABEIRA-OS v1.2.0")
        footer_lbl.setStyleSheet("color: #3A6B3E; font-size: 11px; padding: 15px; font-weight: bold;")
        sidebar_layout.addWidget(footer_lbl)
        
        main_layout.addWidget(sidebar)
        
        # ----------------- RIGHT VIEW CONTAINER -----------------
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Top Header
        header = QFrame()
        header.setObjectName("HeaderFrame")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 10, 25, 10)
        header_layout.setSpacing(15)
        
        self.header_title = QLabel("SYSTEM LIVE MONITOR")
        self.header_title.setObjectName("HeaderTitle")
        header_layout.addWidget(self.header_title)
        header_layout.addStretch()
        
        # Project Selector Combobox and New Project button
        lbl_proj = QLabel("PROJECT:")
        lbl_proj.setStyleSheet("font-weight: bold; color: #8EAE91;")
        header_layout.addWidget(lbl_proj)
        
        self.cmb_project = QComboBox()
        self.cmb_project.setFixedWidth(200)
        self.cmb_project.setEditable(True)
        self.cmb_project.currentIndexChanged.connect(self.switch_project)
        self.cmb_project.lineEdit().editingFinished.connect(self.rename_current_project)
        header_layout.addWidget(self.cmb_project)
        
        self.btn_new_project = QPushButton("[ + NEW PROJECT ]")
        self.btn_new_project.setProperty("class", "PrimaryBtn")
        self.btn_new_project.clicked.connect(self.prompt_create_project)
        header_layout.addWidget(self.btn_new_project)
        
        right_layout.addWidget(header)
        
        # Stacked Main Area
        self.stacked_widget = QStackedWidget()
        
        # Tab 0: Configuration
        self.stacked_widget.addWidget(self.build_config_tab())
        # Tab 1: Monitor
        self.stacked_widget.addWidget(self.build_monitor_tab())
        
        # Connect signal after child widgets are fully constructed to prevent early triggering
        self.stacked_widget.currentChanged.connect(self.tab_index_changed)
        
        right_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(right_panel)

    def switch_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)
        for idx, btn in enumerate(self.nav_buttons):
            btn.setChecked(idx == index)
        
        titles = [
            "CONFIGURATIONS BUFFER",
            "SYSTEM LIVE MONITOR"
        ]
        self.header_title.setText(titles[index])

    def tab_index_changed(self, index):
        if index == 1:
            # Re-read and apply config when shifting back to Monitor Tab
            self.read_config_from_ui()
            self.sync_monitor_tab()

    # ---------------------------------------------------------
    # TAB 0: Monitor View Builder (Dashboard + Logs)
    # ---------------------------------------------------------
    def build_monitor_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Stat cards (TUI boxes)
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        self.stat_agents = TuiStatBox("ACTIVE AGENTS", "0")
        self.stat_tasks = TuiStatBox("PROJECT DESCRIPTION", "EMPTY")
        self.stat_dod = TuiStatBox("DoD VERIFIED RATE", "0%")
        
        stats_layout.addWidget(self.stat_agents)
        stats_layout.addWidget(self.stat_tasks)
        stats_layout.addWidget(self.stat_dod)
        
        layout.addLayout(stats_layout)
        
        # Splitter to allow resizing of daemon status vs log terminal
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Middle panel - System and progress stats
        system_stats_card = QFrame()
        system_stats_card.setProperty("class", "ContentCard")
        sys_layout = QHBoxLayout(system_stats_card)
        sys_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left status pane
        status_left = QVBoxLayout()
        status_h = QHBoxLayout()
        status_lbl = QLabel("Operational State:")
        status_lbl.setStyleSheet("font-weight: bold; color: #8EAE91;")
        self.lbl_status_val = QLabel("[IDLE]")
        self.lbl_status_val.setStyleSheet("color: #FFA39E; font-weight: bold;")
        status_h.addWidget(status_lbl)
        status_h.addWidget(self.lbl_status_val)
        status_h.addStretch()
        status_left.addLayout(status_h)
        
        self.progress_bar = QProgressBar()
        status_left.addWidget(self.progress_bar)
        
        # Cost counters
        cost_layout = QHBoxLayout()
        cost_layout.addWidget(QLabel("Simulated Session Tokens: "))
        self.lbl_tokens = QLabel("0 tkn")
        self.lbl_tokens.setStyleSheet("color: #7CD982; font-weight: bold;")
        cost_layout.addWidget(self.lbl_tokens)
        cost_layout.addStretch()
        status_left.addLayout(cost_layout)
        
        # Right roster process list
        self.txt_roster_status = QTextEdit()
        self.txt_roster_status.setReadOnly(True)
        self.txt_roster_status.setStyleSheet("background-color: #050A05; border: 1px solid #3A6B3E; color: #7CD982; font-size: 11px;")
        
        sys_layout.addLayout(status_left, 3)
        sys_layout.addWidget(self.txt_roster_status, 2)
        
        splitter.addWidget(system_stats_card)
        
        # Bottom terminal console panel
        terminal_card = QFrame()
        terminal_card.setProperty("class", "ContentCard")
        term_layout = QVBoxLayout(terminal_card)
        term_layout.setContentsMargins(10, 10, 10, 10)
        
        # Control Buttons toolbar
        ctrls = QHBoxLayout()
        
        self.btn_stop = QPushButton("[ SIGINT STOP ]")
        self.btn_stop.setProperty("class", "SecondaryBtn")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_orchestration_run)
        
        self.btn_clear = QPushButton("[ CLEAR TTY ]")
        self.btn_clear.setProperty("class", "SecondaryBtn")
        self.btn_clear.clicked.connect(self.clear_console_logs)
        
        ctrls.addWidget(self.btn_stop)
        ctrls.addWidget(self.btn_clear)
        ctrls.addStretch()
        
        term_layout.addLayout(ctrls)
        
        self.txt_console = QTextEdit()
        self.txt_console.setObjectName("ConsoleView")
        self.txt_console.setReadOnly(True)
        self.txt_console.append("goiabeira@os-tty:~$ system_ready --state=idle")
        term_layout.addWidget(self.txt_console)
        
        splitter.addWidget(terminal_card)
        
        splitter.setSizes([180, 470])
        layout.addWidget(splitter)
        
        return widget

    def sync_monitor_tab(self):
        # Stat box sync
        self.stat_agents.update_value(len(self.agent_roles))
        desc_status = "LOADED" if self.project_description.strip() else "EMPTY"
        self.stat_tasks.update_value(desc_status)
        
        checked_dod = sum(1 for d in self.dod_list if d["checked"])
        total_dod = len(self.dod_list)
        dod_pct = int((checked_dod / total_dod) * 100) if total_dod > 0 else 0
        self.stat_dod.update_value(f"{dod_pct}%")
        
        # Process preview sync
        self.rebuild_roster_status_text("STANDBY")

    def rebuild_roster_status_text(self, default_state="STANDBY", active_idx=-1, detail=""):
        lines = ["[DAEMON THREAD MONITOR]"]
        for idx, item in enumerate(self.agents_data):
            name = item["name"]
            role = item["role"]
            source = item["source"]
            pid = 4100 + idx
            
            if idx == active_idx:
                status = f"[ACTIVE] ({detail})"
            else:
                status = f"[{default_state}]"
                
            lines.append(f"PID {pid} | {name:<10} ({role:<10}) -> {status:<25} ({source})")
            
        self.txt_roster_status.setPlainText("\n".join(lines))

    # ---------------------------------------------------------
    # TAB 1: Configuration View Builder (Structured inputs)
    # ---------------------------------------------------------
    def build_config_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        container = QWidget()
        self.scroll_layout = QVBoxLayout(container)
        self.scroll_layout.setContentsMargins(0, 0, 10, 0)
        self.scroll_layout.setSpacing(15)
        
        # Section 1: Agents
        self.agents_section = QFrame()
        self.agents_section.setProperty("class", "ContentCard")
        ag_layout = QVBoxLayout(self.agents_section)
        
        title_ag = QLabel("[01] ACTIVE AGENT THREAD ROSTER")
        title_ag.setProperty("class", "SectionTitle")
        ag_layout.addWidget(title_ag)
        
        self.agents_list_layout = QVBoxLayout()
        ag_layout.addLayout(self.agents_list_layout)
        
        btn_add_agent = QPushButton("[ + SPAWN NEW THREAD AGENT ]")
        btn_add_agent.setProperty("class", "PrimaryBtn")
        btn_add_agent.clicked.connect(lambda: self.prompt_spawn_agent())
        ag_layout.addWidget(btn_add_agent)
        
        self.scroll_layout.addWidget(self.agents_section)
        
        # Section 2: DoD Checks
        self.dod_section = QFrame()
        self.dod_section.setProperty("class", "ContentCard")
        dod_layout = QVBoxLayout(self.dod_section)
        
        title_dod = QLabel("[02] SYSTEM DEFINITION OF DONE RULES")
        title_dod.setProperty("class", "SectionTitle")
        dod_layout.addWidget(title_dod)
        
        desc_dod = QLabel("Specify one verification rule per line. The daemon validates each entry dynamically.")
        desc_dod.setStyleSheet("color: #8EAE91; font-size: 11px; padding-bottom: 8px;")
        desc_dod.setWordWrap(True)
        dod_layout.addWidget(desc_dod)
        
        dod_edit_layout = QHBoxLayout()
        dod_edit_layout.setSpacing(5)
        
        self.txt_dod_numbers = QTextEdit("1")
        self.txt_dod_numbers.setReadOnly(True)
        self.txt_dod_numbers.setFixedWidth(30)
        self.txt_dod_numbers.setFrameStyle(QFrame.Shape.NoFrame)
        self.txt_dod_numbers.setStyleSheet(
            "background-color: transparent; color: #3A6B3E; "
            "font-family: 'Courier New', 'Consolas', monospace; font-size: 12px; "
            "padding: 10px 0px 10px 0px; text-align: right;"
        )
        self.txt_dod_numbers.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.txt_dod_numbers.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.txt_dod_rules = QTextEdit()
        self.txt_dod_rules.setObjectName("ProjectDescInput")
        self.txt_dod_rules.setMinimumHeight(150)
        self.txt_dod_rules.setPlaceholderText("Enter system verification metrics...")
        
        dod_edit_layout.addWidget(self.txt_dod_numbers)
        dod_edit_layout.addWidget(self.txt_dod_rules)
        dod_layout.addLayout(dod_edit_layout)
        
        self.scroll_layout.addWidget(self.dod_section)
        
        # Section 3: Overall Project Description
        self.tasks_section = QFrame()
        self.tasks_section.setProperty("class", "ContentCard")
        tasks_layout = QVBoxLayout(self.tasks_section)
        
        title_tasks = QLabel("[03] OVERALL PROJECT DESCRIPTION")
        title_tasks.setProperty("class", "SectionTitle")
        tasks_layout.addWidget(title_tasks)
        
        self.txt_project_desc = QTextEdit()
        self.txt_project_desc.setObjectName("ProjectDescInput")
        self.txt_project_desc.setMinimumHeight(150)
        self.txt_project_desc.setPlaceholderText("Enter the overall project description here...")
        tasks_layout.addWidget(self.txt_project_desc)
        
        self.scroll_layout.addWidget(self.tasks_section)
        
        self.btn_run = QPushButton("[ RUN PROJECT ]")
        self.btn_run.setProperty("class", "PrimaryBtn")
        self.btn_run.clicked.connect(self.run_project_from_config)
        self.scroll_layout.addWidget(self.btn_run)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    # ---------------------------------------------------------
    # Row Spawning / Deleting Controllers
    # ---------------------------------------------------------
    def prompt_spawn_agent(self):
        is_first = (len(self.agent_config_widgets) == 0)
        dialog = AgentSpawnDialog(parent=self, is_first=is_first)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.txt_name.text().strip()
            source = dialog.cmb_source.currentText()
            role = dialog.txt_role.text().strip()
            desc = dialog.txt_desc.text().strip()
            self.add_agent_row(name, source, role, desc)

    def add_agent_row(self, name="", source="Codex", role="", desc="", session_id=None):
        if isinstance(name, bool):
            name = ""
        if not name:
            name = f"Goiaba-{len(self.agent_config_widgets) + 1}"
        is_first = (len(self.agent_config_widgets) == 0)
        if is_first:
            role = "Orchestrator"
        elif not role:
            role = "Worker"
        row = AgentConfigRow(name, source, role, desc, session_id=session_id)
        row.removed.connect(self.remove_agent_row)
        row.changed.connect(self.save_config_to_file)
        self.agents_list_layout.addWidget(row)
        self.agent_config_widgets.append(row)
        self.sync_agent_roles()
        self.sync_placeholders()
        if not getattr(self, "loading_project", False):
            self.save_config_to_file()

    def remove_agent_row(self, widget):
        widget.setParent(None)
        if widget in self.agent_config_widgets:
            self.agent_config_widgets.remove(widget)
        self.sync_agent_roles()
        self.sync_placeholders()
        if not getattr(self, "loading_project", False):
            self.save_config_to_file()


    def sync_agent_roles(self):
        for idx, row in enumerate(self.agent_config_widgets):
            if idx == 0:
                row.txt_role.blockSignals(True)
                row.txt_role.setText("Orchestrator")
                row.txt_role.setReadOnly(True)
                row.txt_role.blockSignals(False)
                row.update_avatar_tag("Orchestrator")
                
                # Standard one-liner description of the job of a Tech Lead for the Orchestrator
                curr_desc = row.txt_desc.text().strip()
                default_tech_lead_desc = "Coordinates agent threads, architectural design, and system DoD validation checks."
                if not curr_desc or curr_desc == "Description of duties" or curr_desc.lower() == "worker":
                    row.txt_desc.blockSignals(True)
                    row.txt_desc.setText(default_tech_lead_desc)
                    row.txt_desc.blockSignals(False)
            else:
                row.txt_role.setReadOnly(False)

    def sync_placeholders(self):
        # 1. Agents Placeholder
        if len(self.agent_config_widgets) == 0:
            if not hasattr(self, "lbl_agent_placeholder") or self.lbl_agent_placeholder is None:
                self.lbl_agent_placeholder = QLabel(" -[ No agent thread processes spawned. Spawner below. ]-")
                self.lbl_agent_placeholder.setStyleSheet("color: #3A6B3E; font-style: italic; padding: 10px;")
                self.agents_list_layout.addWidget(self.lbl_agent_placeholder)
        else:
            if hasattr(self, "lbl_agent_placeholder") and self.lbl_agent_placeholder is not None:
                self.lbl_agent_placeholder.setParent(None)
                self.lbl_agent_placeholder = None

    # ---------------------------------------------------------
    # Sync Configuration from GUI inputs to Model State variables
    # ---------------------------------------------------------
    def read_config_from_ui(self):
        # 1. Read Agents
        self.agent_roles = []
        self.agent_models = {}
        self.agents_data = []
        
        for w in self.agent_config_widgets:
            name = w.txt_name.text().strip()
            source = w.cmb_source.currentText()
            role = w.txt_role.text().strip()
            desc = w.txt_desc.text().strip()
            
            if not name:
                name = "Goiaba-Anon"
            if not role:
                role = "Worker"
                
            self.agent_roles.append(role)
            self.agent_models[role] = f"{source} ({name})"
            self.agents_data.append({
                "name": name,
                "source": source,
                "role": role,
                "desc": desc,
                "session_id": getattr(w, "session_id", None)
            })
            
        self.num_agents = len(self.agent_roles)
        
        # 2. Read DoD Checklist Rules
        self.dod_list = []
        dod_text = self.txt_dod_rules.toPlainText()
        for line in dod_text.split("\n"):
            rule = line.strip()
            if rule:
                self.dod_list.append({"text": rule, "checked": False})
                
        # 3. Read Project Description
        self.project_description = self.txt_project_desc.toPlainText().strip()

    # ---------------------------------------------------------
    # Projects Local Storage persistence (load/save/create)
    # ---------------------------------------------------------
    def on_project_desc_changed(self):
        if not getattr(self, "loading_project", False):
            self.project_description = self.txt_project_desc.toPlainText().strip()
            self.save_config_to_file()

    def on_dod_text_changed(self):
        if getattr(self, "loading_project", False):
            return
            
        text = self.txt_dod_rules.toPlainText()
        lines = text.split("\n")
        num_lines = len(lines)
        numbers_str = "\n".join(str(i + 1) for i in range(num_lines))
        self.txt_dod_numbers.setPlainText(numbers_str)
        
        self.save_config_to_file()

    def load_projects_from_file(self):
        import os
        import json
        self.config_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects.json")
        
        if os.path.exists(self.config_filepath):
            try:
                with open(self.config_filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                project_arg = None
                for arg in sys.argv[1:]:
                    if arg.startswith("-p=") or arg.startswith("--project="):
                        project_arg = arg.split("=", 1)[1]
                        break
                if not project_arg:
                    for i in range(len(sys.argv) - 1):
                        if sys.argv[i] in ("-p", "--project"):
                            val = sys.argv[i + 1]
                            if not val.startswith("-"):
                                project_arg = val
                                break
                
                if project_arg:
                    self.active_project_name = project_arg
                else:
                    self.active_project_name = data.get("active_project", "Default Project")
                self.projects_dict = data.get("projects", {})
            except Exception as e:
                print(f"Error reading projects.json: {e}")
                self.projects_dict = {}
        
        if not self.projects_dict:
            # Create a default project entry
            self.projects_dict = {
                "Default Project": {
                    "description": (
                        "Configure a multi-agent system to build a web application using Python and PyQt6.\n"
                        "The system should implement a terminal user interface (TUI) matching the Guava Skin theme."
                    ),
                    "agents": [],
                    "dod": []
                }
            }
            self.active_project_name = "Default Project"
            
        # Re-populate project selector dropdown
        self.cmb_project.blockSignals(True)
        self.cmb_project.clear()
        self.cmb_project.addItems(list(self.projects_dict.keys()))
        if self.active_project_name in self.projects_dict:
            self.cmb_project.setCurrentText(self.active_project_name)
        else:
            self.active_project_name = list(self.projects_dict.keys())[0]
            self.cmb_project.setCurrentText(self.active_project_name)
        self.cmb_project.blockSignals(False)

    def save_config_to_file(self):
        import json
        # Update current active project settings in the local dictionary first
        self.read_config_from_ui()
        
        # Serialize active project settings to the dictionary
        self.projects_dict[self.active_project_name] = {
            "description": self.project_description,
            "agents": self.agents_data,
            "dod": self.dod_list
        }
        
        data = {
            "active_project": self.active_project_name,
            "projects": self.projects_dict
        }
        
        try:
            with open(self.config_filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving to projects.json: {e}")

    def load_project_to_ui(self, project_name):
        if project_name not in self.projects_dict:
            return
            
        self.loading_project = True
        self.active_project_name = project_name
        proj = self.projects_dict[project_name]
        
        # Clear existing agent config widgets from layout and list
        for w in list(self.agent_config_widgets):
            w.setParent(None)
        self.agent_config_widgets.clear()
        
        # Set description
        self.txt_project_desc.setPlainText(proj.get("description", ""))
        
        # Add agents rows
        for ag in proj.get("agents", []):
            self.add_agent_row(
                name=ag.get("name", ""),
                source=ag.get("source", "Codex"),
                role=ag.get("role", ""),
                desc=ag.get("desc", ""),
                session_id=ag.get("session_id", None)
            )
            
        # Set DoD checks multiline text
        dod_rules = [item.get("text", "") for item in proj.get("dod", [])]
        self.txt_dod_rules.setPlainText("\n".join(dod_rules))
            
        self.sync_agent_roles()
        self.sync_placeholders()
        self.read_config_from_ui()
        self.loading_project = False

    def switch_project(self, index):
        if index < 0 or index >= self.cmb_project.count():
            return
            
        new_project_name = self.cmb_project.itemText(index)
        if new_project_name == self.active_project_name:
            return
            
        # Save current project before switching
        self.save_config_to_file()
        
        # Load new project
        self.load_project_to_ui(new_project_name)
        self.sync_monitor_tab()

    def prompt_create_project(self):
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        text, ok = QInputDialog.getText(self, "CREATE NEW PROJECT", "ENTER PROJECT NAME:")
        if ok and text.strip():
            project_name = text.strip()
            if project_name in self.projects_dict:
                QMessageBox.warning(self, "DUPLICATE NAME", "A project with this name already exists.")
                return
                
            # Save the active project configuration first
            self.save_config_to_file()
            
            # Create new project dictionary entry
            self.projects_dict[project_name] = {
                "description": "",
                "agents": [],
                "dod": []
            }
            
            # Add to combobox and switch to it
            self.cmb_project.blockSignals(True)
            self.cmb_project.addItem(project_name)
            self.cmb_project.setCurrentText(project_name)
            self.cmb_project.blockSignals(False)
            
            # Load project UI
            self.load_project_to_ui(project_name)
            self.save_config_to_file()
            self.sync_monitor_tab()

    def rename_current_project(self):
        new_name = self.cmb_project.currentText().strip()
        if not new_name or new_name == self.active_project_name:
            return
            
        if new_name in self.projects_dict:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "DUPLICATE NAME", "A project with this name already exists.")
            self.cmb_project.blockSignals(True)
            self.cmb_project.setCurrentText(self.active_project_name)
            self.cmb_project.blockSignals(False)
            return
            
        # Update project dict mapping
        self.projects_dict[new_name] = self.projects_dict.pop(self.active_project_name)
        self.active_project_name = new_name
        
        # Update combobox item text
        idx = self.cmb_project.currentIndex()
        if idx >= 0:
            self.cmb_project.blockSignals(True)
            self.cmb_project.setItemText(idx, new_name)
            self.cmb_project.blockSignals(False)
            
        self.save_config_to_file()

    def closeEvent(self, event):
        self.save_config_to_file()
        event.accept()

    # ---------------------------------------------------------
    # Simulator Run Cycle
    # ---------------------------------------------------------
    def clear_console_logs(self):
        self.txt_console.clear()
        self.txt_console.append("goiabeira@os-tty:~$ tty_cleared")

    def _log_path(self) -> Path:
        slug = self.active_project_name.lower().replace(" ", "_")
        return PROJECT_ROOT / f"{slug}.log"

    def run_project_from_config(self):
        self.switch_tab(1)
        self.start_orchestration_run()

    def start_orchestration_run(self):
        self.read_config_from_ui()
        if not self.agents_data:
            self.txt_console.append("\n[ERROR] Thread orchestration aborting. Agent roster is empty.")
            return

        self.btn_run.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.lbl_status_val.setText("[RUNNING]")
        self.lbl_status_val.setStyleSheet("color: #7CD982; font-weight: bold;")
        self.progress_bar.setValue(0)

        # record where the log file ends NOW so we only tail new lines
        log = self._log_path()
        self._log_file_offset = log.stat().st_size if log.exists() else 0

        self.txt_console.append("\n" + "=" * 70)
        self.txt_console.append(f"[SYSTEM] Launching run.py for project: {self.active_project_name}")
        self.txt_console.append("=" * 70)

        self._process = QProcess(self)
        self._process.finished.connect(self._on_process_finished)
        self._process.start(str(PYTHON_BIN), [str(RUN_SCRIPT)])

        self._poll_timer.start(500)

    def stop_orchestration_run(self):
        self._poll_timer.stop()
        if self._process and self._process.state() != QProcess.ProcessState.NotRunning:
            self._process.terminate()
            self._process.waitForFinished(3000)
            if self._process.state() != QProcess.ProcessState.NotRunning:
                self._process.kill()
        self.btn_run.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.lbl_status_val.setText("[ABORTED]")
        self.lbl_status_val.setStyleSheet("color: #FFA39E; font-weight: bold;")
        self.rebuild_roster_status_text("HALTED")
        self.txt_console.append("\n[WARN] SIGINT received. Halting threads.")

    def _on_process_finished(self, exit_code, _exit_status):
        self._poll_timer.stop()
        self._poll_run_state()  # flush any remaining log lines
        self.btn_run.setEnabled(True)
        self.btn_stop.setEnabled(False)
        label = "[DONE]" if exit_code == 0 else f"[ERROR exit={exit_code}]"
        color = "#7CD982" if exit_code == 0 else "#FFA39E"
        self.lbl_status_val.setText(label)
        self.lbl_status_val.setStyleSheet(f"color: {color}; font-weight: bold;")

    def _poll_run_state(self):
        # --- tail the log file ---
        log = self._log_path()
        if log.exists():
            size = log.stat().st_size
            if size > self._log_file_offset:
                with open(log, "rb") as f:
                    f.seek(self._log_file_offset)
                    new_bytes = f.read(size - self._log_file_offset)
                self._log_file_offset = size
                for line in new_bytes.decode("utf-8", errors="replace").splitlines():
                    self.txt_console.append(line)
                sb = self.txt_console.verticalScrollBar()
                sb.setValue(sb.maximum())

        # --- poll projects.json run_state ---
        try:
            data = json.loads(PROJECTS_JSON.read_text(encoding="utf-8"))
            proj = data.get("projects", {}).get(self.active_project_name, {})
            rs = proj.get("run_state", {})
        except Exception:
            return

        # update roster panel
        agents = rs.get("agents", [])
        if agents:
            lines = ["[DAEMON THREAD MONITOR]"]
            for i, a in enumerate(agents):
                status = a.get("status", "STANDBY")
                detail = a.get("detail", "")
                tag = f"[{status}]" + (f" ({detail})" if detail else "")
                lines.append(f"PID {4100+i} | {a['name']:<10} ({a['role']:<12}) -> {tag:<30}")
            self.txt_roster_status.setPlainText("\n".join(lines))

        # update DoD list + progress bar
        dod = rs.get("dod", [])
        if dod:
            for i, item in enumerate(dod):
                if i < len(self.dod_list):
                    self.dod_list[i]["checked"] = item.get("checked", False)
            checked = sum(1 for d in self.dod_list if d["checked"])
            total = len(self.dod_list)
            pct = int(checked / total * 100) if total else 0
            self.progress_bar.setValue(pct)
            self.stat_dod.update_value(f"{pct}%")
            self.sync_monitor_tab()


# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoiabeiraApp()
    window.show()
    sys.exit(app.exec())
