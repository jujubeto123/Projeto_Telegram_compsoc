import json
import os
from transformers import pipeline

def teor (pasta, arquivo):
    
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

    labels = [
        "teor terrorista",
        "teor preconceituoso",
        "teor de conspiração política",
        "teor de crítica política",
        "teor sensacionalista",
        "teor neutro",
        "teor revolucionário"
    ]

    resultados = []

    for msg in dados:
        result = classifier(
            msg["Message"],
            candidate_labels=labels,
            hypothesis_template="Esse texto possui {}."
        )

        distribuicao = {label: round(score, 2) for label, score in zip(result['labels'], result['scores'])}

        resultado_msg = {
            "Message_ID": msg["Message_ID"],
            "Date": msg["Date"],
            "Forwards": msg["Forwards"],
            "Views": msg["Views"],
            "Teor_mais_provavel": result['labels'][0],
            "Confiança": round(result['scores'][0], 2),
            "Distribuicao": distribuicao
        }

        resultados.append(resultado_msg)

    nome_saida = os.path.splitext(arquivo)[0] + "_classificacao.json"
    caminho_saida = os.path.join(pasta, nome_saida)

    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    return caminho_saida

#exemplo de como colocar
#pasta = r"C:\Users\Davi\Desktop\faculdade\comp soc\Projeto certo\projeto_telegram\pasta_nova\resultados"
#arquivo = "group_457_filtered-JSON.json"

#result = teor(pasta,arquivo)

