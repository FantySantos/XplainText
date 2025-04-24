from view import ExplanationWindow
from PyQt5.QtWidgets import QApplication
import sys, os
from joblib import load
from preprocess import preprocess

basedir = os.path.dirname(__file__)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = load(os.path.join(basedir, f"models/rf.joblib"))
    
    window = ExplanationWindow(model)
    window.showMaximized()

    sys.exit(app.exec_())