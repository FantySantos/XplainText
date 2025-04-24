from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
)
from PyQt5.QtGui import QFont, QPixmap, QFontDatabase, QIcon
from PyQt5.QtCore import Qt
import os
from view_report import ViewReport
from view_batch import ViewBatch
from view_export import ViewExport
from view_dashboard import ViewDashboard
from explaining import Explainer

basedir = os.path.dirname(__file__)

class ExplanationWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.title = "XplainText"
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(os.path.join(basedir, "assets/logo-labit.jpg")))
        self.explainer = Explainer(model)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        tab_widget = QTabWidget()

        font_id = QFontDatabase.addApplicationFont(os.path.join(basedir, "assets/ttf/Unageo-Medium.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        title = QLabel(self.title)
        title.setFont(QFont(font_family, 35))
        title.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        title_layout = QHBoxLayout()
        title_layout.addWidget(title)
        title_layout.setAlignment(Qt.AlignCenter)

        siac_logo = QLabel()
        siac_logo.setPixmap(QPixmap(os.path.join(basedir, "assets/logo-siac.png")).scaledToWidth(95))
        siac_logo.setAlignment(Qt.AlignCenter)

        ppgsp_logo = QLabel()
        ppgsp_logo.setPixmap(QPixmap(os.path.join(basedir, "assets/logo-ppgsp.png")).scaledToWidth(95))
        ppgsp_logo.setAlignment(Qt.AlignCenter)

        ufpa_logo = QLabel()
        ufpa_logo.setPixmap(QPixmap(os.path.join(basedir, "assets/logo-ufpa.png")).scaledToWidth(85))
        ufpa_logo.setAlignment(Qt.AlignCenter)

        mppa_logo = QLabel()
        mppa_logo.setPixmap(QPixmap(os.path.join(basedir, "assets/logo-mppa.png")).scaledToWidth(110))
        mppa_logo.setAlignment(Qt.AlignCenter)

        propesp_logo = QLabel()
        propesp_logo.setPixmap(QPixmap(os.path.join(basedir, "assets/logo-propesp.png")).scaledToWidth(170))
        propesp_logo.setAlignment(Qt.AlignCenter)

        layout_logo = QHBoxLayout()
        layout_logo.addWidget(ppgsp_logo)
        layout_logo.addWidget(propesp_logo)
        layout_logo.addWidget(ufpa_logo)
        layout_logo.addWidget(mppa_logo)
        layout_logo.addWidget(siac_logo)

        view_report = ViewReport(self.explainer)
        view_batch = ViewBatch(self.explainer)
        view_export = ViewExport(self.explainer)
        view_dashboard = ViewDashboard(self.explainer)

        tab_widget.addTab(view_report, "Por relato")
        tab_widget.addTab(view_batch, "Por lote")
        tab_widget.addTab(view_export, "Exportar por lote")
        tab_widget.addTab(view_dashboard, "Dashboard")

        tab_widget.setFont(QFont("Robot", 12))
        main_layout.addLayout(title_layout)
        main_layout.addWidget(tab_widget)
        main_layout.addLayout(layout_logo)
        self.central_widget.setLayout(main_layout)