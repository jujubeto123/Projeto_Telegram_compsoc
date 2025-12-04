# Projeto_Telegram_compsoc

<p>
  Esse projeto de monitoramento de desinformação no Telegram brasileiro foi realizado por 3 alunos de Engenharia de Computação e Informação da UFRJ, em parceria da University of Virginia, mediada pela disciplina de Computador e Sociedade. Os estudantes são Igor Valamiel, Davi William e Júlia Rocha, e o facilitador é André Sobral.
  O principal objetivo desse trabalho foi desenvolver um produto (código) que pode ser usada como um método para analisar semanticamente e categorizar mansagens coletadas, buscando identificar quais os ideias por trás de mensagens enviadas a respeito de tópicos específicos.
</p>

## Tutorial de uso

1. Organização esperada dos dados de entrada
- Estrutura geral:
  - Cada arquivo de teste representa um label (teor) e contém uma coleção de mensagens consideradas manualmente majoritariamente daquele teor.
  - Os arquivos devem misturar mensagens geradas por IA e mensagens do banco de dados original, conforme a metodologia usada.
- Formato recomendado: JSON (arquivo contendo um array de objetos).
- Campos mínimos por mensagem:
  - id (string ou inteiro)
  - date (timestamp ou string ISO 8601)
  - text (conteúdo da mensagem)
  - shares (inteiro, opcional)
  - views (inteiro, opcional)
- Exemplo (arquivo tests/teor_exemplo.json):
```json
[
  {
    "id": "12345",
    "date": "2024-11-20T12:34:56Z",
    "text": "Mensagem de exemplo pertencente ao teor X.",
    "shares": 3,
    "views": 120
  },
  {
    "id": "12346",
    "date": "2024-11-21T08:12:00Z",
    "text": "Outro exemplo de mensagem do mesmo teor.",
    "shares": 1,
    "views": 45
  }
]
```

2. Analisador de Teores — como usar (fluxo geral)
- Objetivo: processar mensagens e gerar, para cada uma, o teor mais provável, a confiança e a distribuição de probabilidades entre labels.
- CLI (exemplo genérico — ajuste conforme nomes reais no repositório):
  - python analisador_teores.py --input tests/ --output results/analisador_result.json
  - Parâmetros úteis: --input (arquivo ou pasta), --model (caminho do modelo), --output (arquivo .json), --batch-size, --workers.
- Uso como biblioteca (exemplo Python):
```python
from analisador_teores import Analyzer

analyzer = Analyzer(model_path="models/mymodel")
analyzer.process_folder("tests/", "results/analisador_result.json")
```
- Recomendações:
  - Use batch processing e múltiplos workers para diretórios grandes.
  - Valide caminhos de modelos e parâmetros antes de rodar em todo o conjunto.

3. Teste de Confiança dos Labels
- Objetivo: verificar se o label manual atribuído a cada arquivo de teste está coerente com as previsões do Analisador.
- Entrada: arquivos de teste (cada um representando um label esperado) e o resultado do Analisador (ou processar os testes diretamente pelo Analisador).
- Saída típica: relatório por arquivo/label contendo:
  - porcentagem de mensagens com predição igual ao label esperado,
  - média/mediana de confiança para mensagens correspondentes e não correspondentes,
  - recomendação (manter ou revisar o label) baseada em thresholds configuráveis.
- Execução (exemplo genérico):
  - python teste_confianca_labels.py --tests tests/ --results results/analisador_result.json --output results/teste_confianca_summary.csv --threshold 0.6
- Interpretação rápida:
  - alta taxa de discordância com alta confiança → revisar o label do arquivo de teste;
  - alto número de previsões com baixa confiança → aumentar amostragem e revisar exemplos.

4. Formato de saída do Analisador (.json)
- O arquivo de saída é um JSON contendo um array de objetos, um por mensagem, com campos informativos e probabilísticos.
- Esquema recomendado:
```json
[
  {
    "id": "12345",
    "date": "2024-11-20T12:34:56Z",
    "text": "Mensagem de exemplo",
    "shares": 3,
    "views": 120,
    "predicted_label": "teor_X",
    "confidence": 0.83,
    "distribution": {
      "teor_X": 0.83,
      "teor_Y": 0.12,
      "teor_Z": 0.05
    }
  }
]
```
- Observações:
  - "confidence" é a probabilidade associada ao label predito.
  - "distribution" fornece as probabilidades para todas as classes consideradas.

5. Análise Estatística — uso do script que consome o .json
- Objetivo: agregar estatísticas sobre quantidade, engajamento e distribuição das labels em todo o conjunto.
- Métricas típicas geradas:
  - contagem de mensagens por label,
  - média/mediana/desvio de confiança por label,
  - soma/ média de shares e views por label,
  - matriz de confusão entre label esperado (quando disponível) e label predito.
- Execução (exemplo genérico):
  - python analise_estatistica.py --input results/analisador_result.json --output results/estatisticas.csv --min_confidence 0.5
- Colunas do CSV de saída sugeridas:
  - label, count, mean_confidence, sd_confidence, total_shares, total_views, avg_shares_per_message

6. Exemplos rápidos de código para exploração (ler JSON e agrupar)
- Leitura e agrupamento básico com pandas:
```python
import json
import pandas as pd

with open("results/analisador_result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

summary = df.groupby("predicted_label").agg(
    count=("id", "count"),
    mean_confidence=("confidence", "mean"),
    sd_confidence=("confidence", "std"),
    total_shares=("shares", "sum"),
    total_views=("views", "sum")
).reset_index()

print(summary)
```
- Visualizações rápidas (exemplos):
  - barras: df['predicted_label'].value_counts().plot(kind='bar')
  - boxplot de confidências: sns.boxplot(x='predicted_label', y='confidence', data=df)

7. Boas práticas para preparação de arquivos de teste e validação
- Balanceamento: busque amostras representativas; se necessário, registre pesos por classe.
- Mistura de origens: mantenha a mistura IA/humano em cada arquivo para reduzir viés de origem.
- Tamanho mínimo: prefira dezenas/hundreds de exemplos por label para avaliações estáveis.
- Metadados: registre quem rotulou, data, e versão do modelo usada para gerar resultados.
- Thresholds de confiança: defina e documente thresholds claros (ex.: <0.5 indeterminado, 0.5–0.75 fraco, >0.75 confiável).
- Revisão iterativa: reavalie e ajuste labels conforme os resultados do Teste de Confiança; automatize sugestões de re-rotulagem quando confiança for alta.
- Reprodutibilidade: versionar scripts, modelos e arquivos de teste (use nomes com versão ou tags de commit).
