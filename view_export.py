from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSizePolicy,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QApplication
)

class ViewExport(QWidget):
    def __init__(self, explainer):
        super().__init__()
        self.explainer = explainer
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
        self.framework.addItems(['  LIME', '  SHAP', '  ELI5', '  TODOS'])
        self.framework.setFixedHeight(50)
        self.framework.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.explain_btn = QPushButton('Explique!')
        self.explain_btn.setFont(QFont("Arial", 11))
        self.explain_btn.setFixedHeight(50)
        self.explain_btn.setStyleSheet("background-color: #de0a26; color: white; font-weight: bold; border : 2px solid black; border-radius : 20px;")
        self.explain_btn.clicked.connect(self.explain)

        layout_select_file = QHBoxLayout()
        layout_select_file.addWidget(browse_btn)
        layout_select_file.addWidget(self.file_path)

        layout.addWidget(file_label)
        layout.addLayout(layout_select_file)
        layout.addSpacing(10)
        layout.addWidget(framework_label)
        layout.addWidget(self.framework)
        layout.addSpacing(10)
        layout.addWidget(self.explain_btn)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(350, 50, 350, 50)

        self.setLayout(layout)
    
    def explain(self):
        if self.df.empty:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um arquivo.")
            return
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        framework_name = self.framework.currentText()
        
        if framework_name:
            if framework_name == '  TODOS':
                for name in ['LIME', 'SHAP', 'ELI5']:
                    self.df[f'{name} Words'], self.df[f'{name} Weights'] = zip(*self.df['relato'].apply(lambda report: self.explainer.explain(name, report)))
                file_path, _ = QFileDialog.getSaveFileName(self, "Salvar arquivo", "", "Excel Files (*.xlsx)")
                if file_path:
                    self.df.to_excel(file_path, index=False)
                QApplication.restoreOverrideCursor()
                return
        
        self.df[f'{framework_name.strip()} Words'], self.df[f'{framework_name.strip()} Weights'] = zip(*self.df['relato'].apply(lambda report: self.explainer.explain(framework_name, report)))
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar arquivo", "", "Excel Files (*.xlsx)")
        if file_path:
            self.df.to_excel(file_path, index=False)
        QApplication.restoreOverrideCursor()

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione um arquivo", "", "Excel Files (*.xlsx);;All Files (*)")
        
        if file_path:
            self.df = pd.read_excel(file_path)
            self.df.columns = self.df.columns.str.lower()
            self.file_path.setText(file_path)