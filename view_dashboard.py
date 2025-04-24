from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy as np
from collections import Counter
from wordcloud import WordCloud
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QFrame,
    QFileDialog
)

class ViewDashboard(QWidget):
    def __init__(self, explainer):
        super().__init__()
        self.explainer = explainer
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        card_layout = QHBoxLayout()

        self.card_qtd_bop = self.create_card("Quantidade de BOPs", "--")
        self.card_qtd_consolidado = self.create_card("Quantidade de consolidados únicos", "--")
        self.card_qtd_tokens_max = self.create_card("Maior quantidade de tokens em um BO", "--")
        self.card_qtd_tokens_min = self.create_card("Menor quantidade de tokens em um BO", "--")

        card_layout.addWidget(self.card_qtd_bop)
        card_layout.addWidget(self.card_qtd_consolidado)
        card_layout.addWidget(self.card_qtd_tokens_max)
        card_layout.addWidget(self.card_qtd_tokens_min)

        self.file_path = QLabel("Nenhum arquivo selecionado.")
        self.file_path.setFont(QFont("Robot", 11))

        browse_btn = QPushButton("Selecionar arquivo...")
        browse_btn.setFont(QFont("Arial", 11))
        browse_btn.setFixedHeight(40)
        browse_btn.setFixedWidth(400)
        browse_btn.setStyleSheet("background-color: #de0a26; color: white; font-weight: bold; border : 2px solid black; border-radius : 20px;")
        browse_btn.clicked.connect(self.browse_file)

        self.consolidado = QComboBox()
        self.consolidado.addItem("Consolidado - Sem filtro")
        self.consolidado.setFixedWidth(250)
        self.consolidado.currentIndexChanged.connect(self.generate_dashboard)

        self.predicao = QComboBox()
        self.predicao.addItem("Predição - Sem filtro")
        self.predicao.setFixedWidth(250)
        self.predicao.currentIndexChanged.connect(self.generate_dashboard)

        self.avaliacao = QComboBox()
        self.avaliacao.addItems(["Avaliação - Sem filtro", "Divergência", "Sem Divergência"])
        self.avaliacao.setFixedWidth(250)
        self.avaliacao.currentIndexChanged.connect(self.generate_dashboard)

        self.framework = QComboBox()
        self.framework.addItems(["LIME", "SHAP", "ELI5"])
        self.framework.setFixedWidth(100)
        self.framework.currentIndexChanged.connect(self.generate_dashboard)

        layout_select_file = QHBoxLayout()
        layout_select_file.addWidget(browse_btn)
        layout_select_file.addWidget(self.file_path)
        layout_select_file.addWidget(self.consolidado)
        layout_select_file.addWidget(self.predicao)
        layout_select_file.addWidget(self.avaliacao)
        layout_select_file.addWidget(self.framework)

        layout.addLayout(layout_select_file)
        layout.addSpacing(10)
        layout.addLayout(card_layout)
        layout.addSpacing(10)
        layout.addWidget(self.create_graph_widget())
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
    def create_card(self, title, value):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 5px; border: 2px solid black;")
        card.setFixedHeight(105)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; border: none;")

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; border: none;")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)

        return card

    def create_graph_widget(self):
        graph_widget = QWidget()
        layout = QVBoxLayout(graph_widget)
        
        graph_layout = QHBoxLayout()

        self.figures = []
        self.canvases = []

        for _ in range(3):
            fig, ax = plt.subplots()
            fig.tight_layout()
            canvas = FigureCanvas(fig)
            self.figures.append(fig)
            self.canvases.append(canvas)
            graph_layout.addWidget(canvas)
            graph_layout.setAlignment(Qt.AlignCenter)
            graph_layout.setContentsMargins(0, 0, 0, 0)

        layout.addLayout(graph_layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        return graph_widget

    def generate_dashboard(self):
        selected_framework = self.framework.currentText()
        selected_consolidado = self.consolidado.currentText()
        selected_predicao = self.predicao.currentText()
        selected_avaliacao = self.avaliacao.currentText()

        if selected_consolidado[-10:] == "Sem filtro":
            selected_consolidado = None
        if selected_predicao[-10:] == "Sem filtro":
            selected_predicao = None
        if selected_avaliacao[-10:] == "Sem filtro":
            selected_avaliacao = None
        
        if not self.df.empty:
            df = self.df.copy()

            if selected_consolidado:
                df = df[df["consolidado"] == selected_consolidado]
            if selected_predicao and selected_predicao in df["predicao"].unique() and not df.empty:
                df = df[df["predicao"] == selected_predicao]
            if selected_avaliacao and not df.empty:
                av = False if selected_avaliacao == 'Divergência' else True
                df = df[df["avaliacao"] == av]
            
            df = df.reset_index(drop=True)
            df['consolidado'] = df['consolidado'].apply(lambda x: x[:10] + '...' if len(x) > 10 else x)

            if "qtd" not in df.columns and not df.empty:
                df["qtd"] = 1
            if "qtd_words" not in df.columns and not df.empty:
                df["qtd_words"] = df["relato"].apply(lambda x: len(x.split()))

            num_bops = df.shape[0] if not df.empty else 0
            num_unique_consolidados = len(df['consolidado'].unique()) if not df.empty else 0
            max_tokens = df['qtd_words'].max() if not df.empty else 0
            min_tokens = df['qtd_words'].min() if not df.empty else 0

            self.card_qtd_bop.layout().itemAt(1).widget().setText(str(num_bops))
            self.card_qtd_consolidado.layout().itemAt(1).widget().setText(str(num_unique_consolidados))
            self.card_qtd_tokens_max.layout().itemAt(1).widget().setText(str(max_tokens))
            self.card_qtd_tokens_min.layout().itemAt(1).widget().setText(str(min_tokens))

            if df.empty:
                for i in range(3):
                    ax = self.figures[i].gca()
                    ax.clear()
                    self.canvases[i].draw()
                return

            ax = self.figures[0].gca()
            ax.clear()
            df.groupby("consolidado")["qtd"].count().plot.bar(ax=ax, rot=0)
            ax.set_title("Quantidade de Linhas por Consolidado", fontsize=11)
            ax.set_ylabel('')
            ax.set_xlabel('')
            self.canvases[0].draw()

            word_cloud_image = self.word_cloud_relato(df)
            if word_cloud_image:
                self.update_word_cloud_canvas(word_cloud_image, selected_consolidado, selected_framework, 1)
            else:
                ax = self.figures[1].gca()
                ax.clear()
                self.canvases[1].draw()

            word_cloud_explicabilidade = self.word_cloud_explicabilidade(df, selected_framework)
            if word_cloud_explicabilidade:
                self.update_word_cloud_canvas(word_cloud_explicabilidade, selected_consolidado, selected_framework, 2)
            else:
                ax = self.figures[2].gca()
                ax.clear()
                self.canvases[2].draw()
    
    def word_cloud(self, words):
        long_string = ' '.join(words)

        wordcloud = WordCloud(background_color="white", max_words=100, stopwords=stopwords.words('portuguese'), max_font_size=40, random_state=42)
        wordcloud.generate(long_string)
        return wordcloud.to_image()
    
    def word_cloud_relato(self, df):
        if df.empty:
            return
        
        words = [word for relato in df['relato'] for word in relato.split()]
        most_common = dict(Counter(words).most_common(15))
        words = [word for word in words if word not in most_common.keys()]
        return self.word_cloud(words)
    
    def word_cloud_explicabilidade(self, df, framework):
        if f"{framework} Words" not in self.df.columns or df.empty:
            return

        if type(df[f'{framework} Words'][0]) != list:
            df[f'{framework} Words'] = df[f'{framework} Words'].replace(r"[\[\]'']", "", regex=True).apply(lambda x: x.split(", "))
            df[f'{framework} Weights'] = df[f'{framework} Weights'].replace(r"[\[\]'']", "", regex=True).apply(lambda x: x.split(", "))
        
        words = []

        for _, row in df.iterrows():
            words_with_weights = zip(row[f'{framework} Words'], row[f'{framework} Weights'])
            words_with_weights = sorted(words_with_weights, key=lambda x: x[1], reverse=True)
            top_10_words = [word for word, weight in words_with_weights[:10]]
            words.extend(top_10_words)

        return self.word_cloud(words)

    def update_word_cloud_canvas(self, image, consolidado, framework, index):
        if consolidado:
            consolidado = consolidado[:10] + '...' if len(consolidado) > 10 else consolidado

        if index == 1:
            if consolidado:
                title = f"Nuvem de Palavras dos Relatos de {consolidado}"
            else:
                title = "Nuvem de Palavras dos Relatos"
        else:
            if consolidado and framework:
                title = f"Nuvem de Palavras da Explicabilidade\n dos Relatos de {consolidado} do {framework}"
            elif consolidado:
                title = f"Nuvem de Palavras da Explicabilidade\n dos Relatos de {consolidado}"
            else:
                title = f"Nuvem de Palavras da Explicabilidade do {framework}"

        ax = self.figures[index].gca()
        ax.clear()
        ax.imshow(np.array(image), interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=11)
        self.canvases[index].draw()
    
    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione um arquivo", "", "Excel Files (*.xlsx);;All Files (*)")
        
        if file_path:
            self.df = pd.read_excel(file_path)
            self.file_path.setText(file_path)
            self.consolidado.addItems(sorted(self.df["consolidado"].unique()))
            self.df["predicao"] = self.df["predicao"].astype(str)
            self.predicao.addItems(sorted(self.df["predicao"].unique()))
            self.generate_dashboard()