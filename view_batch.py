from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils import gerar_html
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox,
    QApplication,
    QSizePolicy,
    QScrollArea,
    QFileDialog
)
import pandas as pd

class ViewBatch(QWidget):
    def __init__(self, explainer):
        super().__init__()
        self.explainer = explainer
        self.index = 0
        self.df = pd.DataFrame()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        file_label = QLabel("Selecione um arquivo:")
        file_label.setFont(QFont("Robot", 14))

        self.file_path = QLabel("Nenhum arquivo selecionado.")
        self.file_path.setFont(QFont("Robot", 11))

        browse_btn = QPushButton("Selecionar arquivo...")
        browse_btn.setFont(QFont("Arial", 11))
        browse_btn.setFixedHeight(50)
        browse_btn.setFixedWidth(400)
        browse_btn.setStyleSheet("background-color: #de0a26; color: white; font-weight: bold; border : 2px solid black; border-radius : 20px;")
        browse_btn.clicked.connect(self.browse_file)

        framework_label = QLabel("Selecione o framework:")
        framework_label.setFont(QFont("Robot", 14))

        self.framework = QComboBox()
        self.framework.setFont(QFont("Arial", 13))
        self.framework.addItems(['  LIME', '  SHAP', '  ELI5'])
        self.framework.setFixedHeight(50)
        self.framework.currentIndexChanged.connect(self.explain)
        self.framework.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.next_btn = QPushButton("Próximo")
        self.next_btn.setFont(QFont("Arial", 11))
        self.next_btn.setFixedHeight(50)
        self.next_btn.setStyleSheet("background-color: #de0a26; color: white; font-weight: bold; border : 2px solid black; border-radius : 20px;")
        self.next_btn.clicked.connect(self.explain_next)
        self.next_btn.setVisible(False)

        self.previous_btn = QPushButton("Anterior")
        self.previous_btn.setFont(QFont("Arial", 11))
        self.previous_btn.setFixedHeight(50)
        self.previous_btn.setStyleSheet("background-color: #de0a26; color: white; font-weight: bold; border : 2px solid black; border-radius : 20px;")
        self.previous_btn.clicked.connect(self.explain_previous)
        self.previous_btn.setVisible(False)

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

        layout_select_file = QHBoxLayout()
        layout_select_file.addWidget(browse_btn)
        layout_select_file.addWidget(self.file_path)

        layout_directions_btns = QHBoxLayout()
        layout_directions_btns.addWidget(self.previous_btn)
        layout_directions_btns.addWidget(self.next_btn)

        layout.addWidget(file_label)
        layout.addLayout(layout_select_file)
        layout.addSpacing(10)
        layout.addWidget(framework_label)
        layout.addWidget(self.framework)
        layout.addSpacing(10)
        layout.addWidget(self.label_pred)
        layout.addWidget(self.scroll_area)
        layout.addSpacing(10)
        layout.addLayout(layout_directions_btns)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(350, 50, 350, 50)

        self.setLayout(layout)

    def explain(self):
        if self.df.empty:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um arquivo.")
            return
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        framework_name = self.framework.currentText()
        report = self.df['relato'][self.index]

        if report and framework_name:
            words, weights = self.explainer.explain(framework_name, report)
            word_weights = dict(zip(words, weights))
            sorted_words = dict(sorted(word_weights.items(), key=lambda x: float(x[1]), reverse=True)[:11])
            self.label_pred.setText(f"Predição: {self.explainer.name_class}")
            self.label.setText(gerar_html(report, sorted_words.keys(), framework_name.strip()))
            self.label_pred.setVisible(True)
            self.scroll_area.setVisible(True)
            self.next_btn.setVisible(True)
            self.previous_btn.setVisible(True)
            QApplication.restoreOverrideCursor()
    
    def explain_next(self):
        self.index += 1
        self.explain()

    def explain_previous(self):
        if self.index == 0:
            return
        
        self.index -= 1
        self.explain()
    
    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione um arquivo", "", "Excel Files (*.xlsx);;All Files (*)")
        
        if file_path:
            self.df = pd.read_excel(file_path)
            self.df.columns = self.df.columns.str.lower()
            self.file_path.setText(file_path)
            self.indice = 0
            self.explain()