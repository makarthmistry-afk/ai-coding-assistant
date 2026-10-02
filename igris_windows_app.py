import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class IgrisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Igris")
        self.resize(1100, 700)
        self.setStyleSheet("""
            QWidget {
                background: #05070d;
                color: #edf6ff;
                font-family: "Segoe UI";
            }
            QLabel {
                color: #9bb4d4;
                font-size: 11px;
                letter-spacing: 2px;
                text-transform: uppercase;
                font-weight: 700;
            }
            QTextEdit, QComboBox, QPushButton {
                border: 1px solid rgba(125, 211, 252, 0.4);
                border-radius: 12px;
                background: #0b1220;
                color: #edf6ff;
            }
            QTextEdit {
                padding: 14px;
                font-size: 14px;
            }
            QComboBox {
                padding: 12px 14px;
                font-size: 14px;
            }
            QPushButton {
                padding: 14px 18px;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                cursor: pointer;
            }
            QPushButton:hover {
                border-color: rgba(103, 232, 249, 0.8);
            }
            #planBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f2030, stop:1 #143052);
                color: #67e8f9;
            }
            #generateBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #111f30, stop:1 #1d2d43);
                color: #b6f2ff;
            }
            #fixBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #201218, stop:1 #3a1e2b);
                color: #fda4af;
            }
        """)

        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        topbar = QHBoxLayout()
        topbar.setContentsMargins(0, 0, 0, 0)

        brand = QLabel("Igris")
        brand_font = QFont()
        brand_font.setBold(True)
        brand_font.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        brand.setFont(brand_font)
        brand.setStyleSheet("color: #67e8f9; font-size: 22px; letter-spacing: 4px; text-transform: uppercase;")

        status = QLabel("System Online")
        status.setStyleSheet("""
            color: #b6f2ff;
            background: rgba(103, 232, 249, 0.08);
            border: 1px solid rgba(103, 232, 249, 0.45);
            border-radius: 12px;
            padding: 8px 12px;
            font-size: 10px;
        """)
        status.setAlignment(Qt.AlignCenter)

        topbar.addWidget(brand)
        topbar.addStretch()
        topbar.addWidget(status)

        main = QHBoxLayout()
        main.setSpacing(18)

        left = QVBoxLayout()
        left.setSpacing(14)

        prompt_label = QLabel("Initiate Task")
        prompt_label.setStyleSheet("color: #9bb4d4; font-size: 11px; letter-spacing: 2px;")

        self.prompt_box = QTextEdit()
        self.prompt_box.setPlaceholderText("Describe the task, bug, or feature you want Igris to handle...")
        self.prompt_box.setStyleSheet("min-height: 190px;")

        options = QHBoxLayout()
        options.setSpacing(12)

        lang_label = QLabel("Language")
        self.language_box = QComboBox()
        self.language_box.addItems(["Python", "JavaScript"])
        self.language_box.setFixedHeight(46)

        type_label = QLabel("Project Type")
        self.project_type = QComboBox()
        self.project_type.addItems(["CLI", "API", "Web"])
        self.project_type.setFixedHeight(46)

        options.addWidget(self.language_box)
        options.addWidget(self.project_type)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)

        self.plan_btn = QPushButton("Plan")
        self.plan_btn.setObjectName("planBtn")
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.setObjectName("generateBtn")
        self.fix_btn = QPushButton("Fix")
        self.fix_btn.setObjectName("fixBtn")

        buttons.addWidget(self.plan_btn)
        buttons.addWidget(self.generate_btn)
        buttons.addWidget(self.fix_btn)

        left.addWidget(prompt_label)
        left.addWidget(self.prompt_box)
        left.addWidget(options)
        left.addWidget(buttons)

        right = QVBoxLayout()
        right.setSpacing(14)

        output_label = QLabel("Response Console")
        output_label.setStyleSheet("color: #9bb4d4; font-size: 11px; letter-spacing: 2px;")

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Igris output will appear here...")
        self.output_box.setStyleSheet("min-height: 420px;")

        right.addWidget(output_label)
        right.addWidget(self.output_box)

        main.addLayout(left, 2)
        main.addLayout(right, 1)

        root.addLayout(topbar)
        root.addLayout(main)

        self.plan_btn.clicked.connect(self.plan_task)
        self.generate_btn.clicked.connect(self.generate_task)
        self.fix_btn.clicked.connect(self.fix_task)

    def plan_task(self):
        prompt = self.prompt_box.toPlainText().strip()
        if not prompt:
            self.output_box.setPlainText("Please enter a task prompt first.")
            return

        result = self._mock_plan(prompt)
        self.output_box.setPlainText(json.dumps(result, indent=2))

    def generate_task(self):
        prompt = self.prompt_box.toPlainText().strip()
        if not prompt:
            self.output_box.setPlainText("Please enter a task prompt first.")
            return

        result = self._mock_generate(prompt)
        self.output_box.setPlainText(json.dumps(result, indent=2))

    def fix_task(self):
        prompt = self.prompt_box.toPlainText().strip()
        if not prompt:
            self.output_box.setPlainText("Please enter a bug description first.")
            return

        result = self._mock_fix(prompt)
        self.output_box.setPlainText(json.dumps(result, indent=2))

    def _mock_plan(self, prompt):
        return {
            "objective": prompt,
            "steps": [
                "Analyze the user requirement and identify the real goal.",
                "Inspect the project structure and relevant files.",
                "Implement the smallest valid solution.",
                "Validate behavior and edge cases.",
                "Summarize the final change and assumptions."
            ],
            "risks": [
                "Ambiguous requirements may require clarification.",
                "Missing edge cases can cause regressions."
            ],
            "deliverables": [
                "Working implementation",
                "Validation summary",
                "Short change log"
            ]
        }

    def _mock_generate(self, prompt):
        lang = self.language_box.currentText().lower()
        project_type = self.project_type.currentText().lower()

        code = (
            "def main():\n"
            f"    print('Igris generated this {project_type} project for: {prompt}')\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        ) if lang == "python" else (
            "function main() {\n"
            f"  console.log('Igris generated this {project_type} project for: {prompt}');\n"
            "}\n\n"
            "main();\n"
        )

        return {
            "status": "ok",
            "language": lang,
            "project_type": project_type,
            "summary": f"Generated starter code for: {prompt}",
            "files": {
                "main.py" if lang == "python" else "main.js": code
            },
            "note": "Local fallback mode is active."
        }

    def _mock_fix(self, prompt):
        return {
            "status": "ok",
            "language": self.language_box.currentText().lower(),
            "summary": "Bug-fix workflow prepared.",
            "patch": """
# Fix strategy
# 1. Validate inputs before using them.
# 2. Guard optional values and empty collections.
# 3. Add a focused regression test.
# 4. Keep the fix minimal and explicit.

try:
    value = data["key"]
except KeyError:
    value = None

if value is None:
    return "safe fallback"

return value
""",
            "note": "No external model connected. This is a safe local-ready template."
        }

def main():
    app = QApplication([])
    window = IgrisApp()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
