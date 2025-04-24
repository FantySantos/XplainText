from lime.lime_text import LimeTextExplainer
import shap
shap.initjs()
from eli5.formatters import as_dataframe
from eli5.lime import TextExplainer

class_names = ['Outro contexto', 'LGBT']

class Explainer:
    def __init__(self, model):
        self.model = model

    def explain(self, framework_name, report):
        self.report = report
        self.index_class = self.model.predict([self.report])[0]
        self.name_class = class_names[self.index_class]

        if framework_name.strip() == "LIME":
            return self.explaining_lime()
        if framework_name.strip() == "SHAP":
            return self.explaining_shap()
        
        return self.explaining_eli5()

    def explaining_lime(self):
        explainer = LimeTextExplainer(random_state=42, class_names=class_names)
        explain = explainer.explain_instance(self.report, self.model.predict_proba, top_labels=1, num_features=len(self.report.split()))
        lime_list = explain.as_list(self.index_class)
        lime_words = [i[0] for i in lime_list]
        lime_weights = [i[1] for i in lime_list]
        return lime_words, lime_weights

    def explaining_shap(self):
        masker = shap.maskers.Text(tokenizer=r"\W+")
        explainer = shap.Explainer(self.model.predict_proba, masker=masker, output_names=class_names, seed=42)
        shap_values = explainer([self.report],)
        self.index_class = self.model.predict([self.report])[0]
        shap_words = shap_values[0, :, self.index_class].data.tolist()
        shap_weights = shap_values[0, :, self.index_class].values.tolist()
        return shap_words, shap_weights

    def explaining_eli5(self):
        te = TextExplainer(random_state=42)
        te.fit(self.report, self.model.predict_proba)
        df_eli5 = as_dataframe.format_as_dataframe(te.explain_prediction(target_names=class_names, targets=[self.name_class]))
        df_eli5 = df_eli5[df_eli5['feature'] != '<BIAS>']
        eli5_words = df_eli5['feature'].to_list()
        eli5_weights = df_eli5['weight'].to_list()
        return eli5_words, eli5_weights