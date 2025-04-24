from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils import gerar_html
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QComboBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QApplication
)

class ViewReport(QWidget):
    def __init__(self, explainer):
        super().__init__()
        self.explainer = explainer
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        report_label = QLabel("Insira o relato:")
        report_label.setFont(QFont("Robot", 14))

        self.report = QTextEdit()
        self.report.setFont(QFont("Arial", 11))
        self.report.setFixedHeight(130)

        framework_label = QLabel("Selecione o framework:")
        framework_label.setFont(QFont("Robot", 14))

        self.framework = QComboBox()
        self.framework.setFont(QFont("Arial", 13))
        self.framework.addItems(['  LIME', '  SHAP', '  ELI5'])
        self.framework.setFixedHeight(50)

        self.explain_btn = QPushButton('Explique!')
        self.explain_btn.setFont(QFont("Arial", 11))
        self.explain_btn.setFixedHeight(50)
        self.explain_btn.setStyleSheet("background-color: #de0a26; color: white; font-weight: bold; border : 2px solid black; border-radius : 20px;")
        self.explain_btn.clicked.connect(self.explain)

        self.scroll_area = QScrollArea()
        widget = QWidget()
        layout_label = QVBoxLayout(widget)
        self.label = QLabel()
        self.label.setFont(QFont("Arial", 11))
        self.label.setOpenExternalLinks(True)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)
        layout_label.addWidget(self.label)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(widget)
        self.scroll_area.setVisible(False)

        self.label_pred = QLabel()
        self.label_pred.setVisible(False)

        layout.addStretch()
        layout.addWidget(report_label)
        layout.addWidget(self.report)
        layout.addSpacing(10)
        layout.addWidget(framework_label)
        layout.addWidget(self.framework)
        layout.addSpacing(10)
        layout.addWidget(self.explain_btn)
        layout.addSpacing(10)
        layout.addWidget(self.label_pred)
        layout.addWidget(self.scroll_area)
        layout.addStretch()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(350, 50, 350, 50)

        self.setLayout(layout)
    
    def explain(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        report = self.report.toPlainText()
        framework_name = self.framework.currentText()
        
        if report and framework_name:
            words, weights = self.explainer.explain(framework_name, report)
            word_weights = dict(zip(words, weights))
            sorted_words = dict(sorted(word_weights.items(), key=lambda x: float(x[1]), reverse=True)[:11])
            self.label.setText(gerar_html(self.report.toPlainText(), sorted_words.keys(), framework_name.strip()))
            self.label_pred.setText(f"Predição: {self.explainer.name_class}")
            self.scroll_area.setVisible(True)
            self.label_pred.setVisible(True)
            QApplication.restoreOverrideCursor()
            return
        
        QMessageBox.warning(self, "Aviso", "Por favor, insira um relato.")
        return