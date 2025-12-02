import json
import os
from transformers import pipeline

def teor (pasta, arquivo):
    
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

    #exemplos de teores:
    labels = [
        "teor terrorista",
        "teor preconceituoso",
        "teor conspiração política", 
        "teor crítica política", 
        "teor sensacionalista", 
        "teor religioso", 
        "teor científico", 
    ]

    resultados = []

    for msg in dados:
        result = classifier(
            msg["message"],
            candidate_labels=labels,
            hypothesis_template="Esse texto possui {}."
        )

        distribuicao = {label: round(score, 2) for label, score in zip(result['labels'], result['scores'])}

        resultado_msg = {
            "message_id": msg["message_id"],
            "date": msg["date"],
            "forwards": msg["forwards"],
            "views": msg["views"],
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

pasta = r"C:\sua\pasta\aqui"
arquivo = "seu_arquivo.json"

result = teor(pasta,arquivo)

