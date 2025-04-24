def gerar_html(text, words_highlights, framework):
    highlights = []
    for word in words_highlights:
        highlights.extend(word.upper().split() if len(word.split()) != 1 else [word.upper().strip()])

    html = "<html><body><p>"
    if framework == "LIME":
        color = "#90ee90"
    elif framework == "SHAP":
        color = "#ffb6c1"
    else:
        color = "yellow"

    for word in text.upper().split():
        if word in highlights:
            html += f"<span style='background-color: {color}'>{word}</span> "
        else:
            html += f"{word} "
    html += "</p></body></html>"
    return html