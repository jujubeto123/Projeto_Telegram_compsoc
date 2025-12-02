import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("="*70)
print("ANALISE DE CLASSIFICACAO - GERANDO RELATORIOS TXT")
print("="*70)

# Lista de arquivos
arquivos = [
    "teste_cientifico_classificacao_cientifico",
    "teste_sensacionalista_classificacao_sensacionalista", 
    "teste_preconceito_classificacao_preconceito",
    "teste_consp_classificacao_consp",
    "teste_terrorista_classificacao_terrorista",
    "teste_critica_classificacao_critica",
    "teste_religioso_classificacao_religioso"
]

# Preparar resultados
resultados = []

for arquivo in arquivos:
    print(f"\nAnalisando: {arquivo}")
    
    # Tentar ler o arquivo
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except:
        try:
            with open(arquivo + '.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except:
            print(f"  ERRO: Arquivo não encontrado")
            continue
    
    df = pd.DataFrame(dados)
    
    # Nome do tipo
    tipo = arquivo.split('_')[1]
    
    # Encontrar coluna de confianca
    col_conf = None
    for col in df.columns:
        if 'confian' in col.lower():
            col_conf = col
            break
    
    if not col_conf:
        print(f"  ERRO: Coluna de confiança não encontrada")
        continue
    
    # Estatísticas básicas
    total = len(df)
    confianca_media = df[col_conf].mean()
    confianca_min = df[col_conf].min()
    confianca_max = df[col_conf].max()
    confianca_std = df[col_conf].std()
    
    # Verificar acertos (simplificado)
    acertos = 0
    if 'Teor_mais_provavel' in df.columns:
        # Contar quantas vezes o tipo aparece no nome da classificação
        for classif in df['Teor_mais_provavel']:
            if tipo.lower() in str(classif).lower():
                acertos += 1
    
    taxa_acerto = (acertos / total * 100) if total > 0 else 0
    
    # Score para o tipo (simplificado)
    score_medio = 0
    if 'Distribuicao' in df.columns:
        scores = []
        for dist in df['Distribuicao']:
            if isinstance(dist, dict):
                # Procurar por chaves que contenham o tipo
                for chave, valor in dist.items():
                    if tipo.lower() in chave.lower():
                        scores.append(valor)
                        break
        if scores:
            score_medio = np.mean(scores)
    
    resultados.append({
        'tipo': tipo,
        'total': total,
        'acertos': acertos,
        'taxa_acerto': taxa_acerto,
        'confianca_media': confianca_media,
        'confianca_min': confianca_min,
        'confianca_max': confianca_max,
        'confianca_std': confianca_std,
        'score_medio': score_medio
    })
    
    print(f"  Mensagens: {total}")
    print(f"  Acertos: {acertos}/{total} ({taxa_acerto:.1f}%)")
    print(f"  Confiança média: {confianca_media:.2%}")

# Salvar relatório em TXT
print(f"\n{'='*70}")
print("SALVANDO RELATORIOS...")
print("="*70)

# 1. RELATORIO PRINCIPAL
with open('relatorio_principal.txt', 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("RELATORIO DE ANALISE DE CLASSIFICACAO\n")
    f.write("="*70 + "\n\n")
    
    f.write(f"Data: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    f.write(f"Arquivos analisados: {len(resultados)}\n")
    f.write(f"Mensagens totais: {sum(r['total'] for r in resultados)}\n\n")
    
    f.write("RESUMO POR TIPO:\n")
    f.write("-"*70 + "\n\n")
    
    # Ordenar por taxa de acerto
    resultados_ordenados = sorted(resultados, key=lambda x: x['taxa_acerto'], reverse=True)
    
    for i, res in enumerate(resultados_ordenados, 1):
        f.write(f"{i}. {res['tipo'].upper()}\n")
        f.write(f"   Mensagens: {res['total']}\n")
        f.write(f"   Acertos: {res['acertos']} ({res['taxa_acerto']:.1f}%)\n")
        f.write(f"   Confiança média: {res['confianca_media']:.2%}\n")
        f.write(f"   Variação: {res['confianca_min']:.2%} a {res['confianca_max']:.2%}\n")
        f.write(f"   Score médio para tipo: {res['score_medio']:.2%}\n")
        f.write(f"   Desvio padrão da confiança: {res['confianca_std']:.2%}\n\n")
    
    # Estatísticas gerais
    if resultados:
        taxa_media = np.mean([r['taxa_acerto'] for r in resultados])
        confianca_geral = np.mean([r['confianca_media'] for r in resultados])
        score_geral = np.mean([r['score_medio'] for r in resultados])
        
        f.write("="*70 + "\n")
        f.write("ESTATISTICAS GERAIS\n")
        f.write("-"*70 + "\n\n")
        
        f.write(f"Taxa média de acerto: {taxa_media:.1f}%\n")
        f.write(f"Confiança média geral: {confianca_geral:.2%}\n")
        f.write(f"Score médio geral: {score_geral:.2%}\n\n")
        
        # Melhor e pior
        melhor = max(resultados, key=lambda x: x['taxa_acerto'])
        pior = min(resultados, key=lambda x: x['taxa_acerto'])
        
        f.write("MELHOR DESEMPENHO:\n")
        f.write(f"  {melhor['tipo'].upper()}: {melhor['taxa_acerto']:.1f}% de acerto\n")
        f.write(f"  Confiança: {melhor['confianca_media']:.2%}\n\n")
        
        f.write("PIOR DESEMPENHO:\n")
        f.write(f"  {pior['tipo'].upper()}: {pior['taxa_acerto']:.1f}% de acerto\n")
        f.write(f"  Confiança: {pior['confianca_media']:.2%}\n\n")
        
        # Recomendações
        f.write("="*70 + "\n")
        f.write("RECOMENDACOES\n")
        f.write("-"*70 + "\n\n")
        
        tipos_baixos = [r for r in resultados if r['taxa_acerto'] < 70]
        if tipos_baixos:
            f.write("TIPOS QUE PRECISAM DE ATENCAO (taxa < 70%):\n")
            for res in tipos_baixos:
                f.write(f"  • {res['tipo'].upper()}: {res['taxa_acerto']:.1f}%\n")
                if res['score_medio'] < 0.4:
                    f.write(f"    - Score baixo para o tipo correto\n")
                if res['confianca_media'] < 0.4:
                    f.write(f"    - Confiança baixa nas classificações\n")
            f.write("\n")
        
        tipos_altos = [r for r in resultados if r['taxa_acerto'] >= 85]
        if tipos_altos:
            f.write("TIPOS COM BOM DESEMPENHO (taxa >= 85%):\n")
            for res in tipos_altos:
                f.write(f"  • {res['tipo'].upper()}: {res['taxa_acerto']:.1f}%\n")

print("✓ Relatório principal salvo em 'relatorio_principal.txt'")

# 2. DADOS TABULARES
with open('dados_formatados.txt', 'w', encoding='utf-8') as f:
    f.write("DADOS FORMATADOS PARA ANALISE\n")
    f.write("="*60 + "\n\n")
    
    f.write(f"{'TIPO':<15} {'ACERTOS':<10} {'TAXA':<10} {'CONFIANÇA':<12} {'SCORE':<10}\n")
    f.write("-"*60 + "\n")
    
    for res in resultados_ordenados:
        f.write(f"{res['tipo']:<15} "
               f"{res['acertos']}/{res['total']:<9} "
               f"{res['taxa_acerto']:>6.1f}%   "
               f"{res['confianca_media']:>10.2%}   "
               f"{res['score_medio']:>8.2%}\n")

print("✓ Dados formatados salvos em 'dados_formatados.txt'")

# 3. RESUMO EXECUTIVO
with open('resumo_executivo.txt', 'w', encoding='utf-8') as f:
    f.write("RESUMO EXECUTIVO\n")
    f.write("="*50 + "\n\n")
    
    if resultados:
        melhor = max(resultados, key=lambda x: x['taxa_acerto'])
        pior = min(resultados, key=lambda x: x['taxa_acerto'])
        taxa_media = np.mean([r['taxa_acerto'] for r in resultados])
        confianca_geral = np.mean([r['confianca_media'] for r in resultados])
        
        f.write("PRINCIPAIS RESULTADOS:\n\n")
        f.write(f"• Taxa média de acerto: {taxa_media:.1f}%\n")
        f.write(f"• Confiança média da IA: {confianca_geral:.2%}\n\n")
        
        f.write("MELHOR DESEMPENHO:\n")
        f.write(f"  Tipo: {melhor['tipo'].upper()}\n")
        f.write(f"  Acerto: {melhor['taxa_acerto']:.1f}%\n")
        f.write(f"  Confiança: {melhor['confianca_media']:.2%}\n\n")
        
        f.write("PIOR DESEMPENHO:\n")
        f.write(f"  Tipo: {pior['tipo'].upper()}\n")
        f.write(f"  Acerto: {pior['taxa_acerto']:.1f}%\n")
        f.write(f"  Confiança: {pior['confianca_media']:.2%}\n\n")
        
        # Contar tipos problemáticos
        problematicos = len([r for r in resultados if r['taxa_acerto'] < 70])
        bons = len([r for r in resultados if r['taxa_acerto'] >= 85])
        
        f.write("DISTRIBUICAO DE DESEMPENHO:\n")
        f.write(f"  • Tipos com bom desempenho (≥85%): {bons}\n")
        f.write(f"  • Tipos com desempenho médio: {len(resultados) - problematicos - bons}\n")
        f.write(f"  • Tipos problemáticos (<70%): {problematicos}\n")

print("✓ Resumo executivo salvo em 'resumo_executivo.txt'")

# 4. VERIFICAR SE OS ARQUIVOS FORAM CRIADOS
print(f"\n{'='*70}")
print("VERIFICACAO DOS ARQUIVOS GERADOS")
print("="*70)

arquivos_gerados = ['relatorio_principal.txt', 'dados_formatados.txt', 'resumo_executivo.txt']
for arquivo in arquivos_gerados:
    if os.path.exists(arquivo):
        tamanho = os.path.getsize(arquivo)
        print(f"✓ {arquivo} - {tamanho} bytes")
    else:
        print(f"✗ {arquivo} - NÃO ENCONTRADO")

print(f"\n{'='*70}")
print("ANALISE CONCLUIDA!")
print("="*70)