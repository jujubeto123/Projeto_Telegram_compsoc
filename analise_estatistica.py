import pandas as pd
import numpy as np
import json

# NOME DO ARQUIVO
nome_arquivo = "filteredJSONmensages_classificacao"

# CARREGAR DADOS
try:
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
except:
    try:
        with open(nome_arquivo + '.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar: {e}")
        exit()

df = pd.DataFrame(dados)
total_mensagens = len(df)

if 'forwards' in df.columns and 'views' in df.columns:
    df = df.rename(columns={'forwards': 'Forwards', 'views': 'Views'})

# Iniciar conteúdo do arquivo TXT
conteudo_txt = []

# Função para adicionar linhas ao conteúdo
def add_line(text="", separator=False):
    if separator:
        conteudo_txt.append("=" * 70)
    else:
        conteudo_txt.append(text)

# 1. CABEÇALHO
add_line("=" * 70, separator=True)
add_line(f"ANÁLISE DE ENGRAJAMENTO POR TEOR")
add_line(f"Arquivo: {nome_arquivo}")
add_line(f"Data: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
add_line("=" * 70, separator=True)
add_line("")

# 2. DADOS GERAIS
add_line("1. DADOS GERAIS")
add_line("-" * 70, separator=False)
add_line(f" Total de mensagens: {total_mensagens:,}")
if 'Forwards' in df.columns and 'Views' in df.columns:
    total_views_real = df['Views'].sum()
    total_forwards_real = df['Forwards'].sum()
    add_line(f" Views totais: {total_views_real:,.0f}")
    add_line(f" Forwards totais: {total_forwards_real:,.0f}")
    add_line(f" Views/média: {df['Views'].mean():.0f}")
    add_line(f" Forwards/média: {df['Forwards'].mean():.1f}")
add_line("")

# 3. ENGRAJAMENTO POR TEOR
add_line("2. ENGRAJAMENTO POR TEOR")
add_line("-" * 70, separator=False)
add_line("")

if 'Forwards' in df.columns and 'Views' in df.columns and 'Teor_mais_provavel' in df.columns:
    # Calcular por teor
    engajamento_por_teor = []
    
    for teor in df['Teor_mais_provavel'].unique():
        mensagens_teor = df[df['Teor_mais_provavel'] == teor]
        quantidade = len(mensagens_teor)
        porcentagem = (quantidade / total_mensagens) * 100
        
        # Views
        total_views = mensagens_teor['Views'].sum()
        media_views = mensagens_teor['Views'].mean()
        
        # Forwards
        total_forwards = mensagens_teor['Forwards'].sum()
        media_forwards = mensagens_teor['Forwards'].mean()
        
        engajamento_por_teor.append({
            'Teor': teor,
            'Quantidade': quantidade,
            'Porcentagem': porcentagem,
            'Total_Views': total_views,
            'Media_Views': media_views,
            'Total_Forwards': total_forwards,
            'Media_Forwards': media_forwards
        })
    
    # Converter para DataFrame e ordenar
    df_engajamento = pd.DataFrame(engajamento_por_teor)
    df_engajamento = df_engajamento.sort_values('Quantidade', ascending=False)
    
    # Tabela formatada
    add_line(f"{'TEOR':<30} {'QTD':<6} {'%':<6} {'VIEWS TOTAL':<12} {'VIEWS/MED':<10} {'FORW TOTAL':<12} {'FORW/MED':<10}")
    add_line("-" * 90)
    
    for _, row in df_engajamento.iterrows():
        add_line(f"{row['Teor']:<30} "
                f"{row['Quantidade']:<6} "
                f"{row['Porcentagem']:>5.1f}% "
                f"{row['Total_Views']:>12,.0f} "
                f"{row['Media_Views']:>10.0f} "
                f"{row['Total_Forwards']:>12,.0f} "
                f"{row['Media_Forwards']:>10.1f}")
    
    add_line("")
    
    # 4. ANÁLISE DETALHADA POR TEOR
    add_line("3. ANÁLISE DETALHADA POR TEOR")
    add_line("-" * 70, separator=False)
    add_line("")
    
    for _, row in df_engajamento.iterrows():
        teor = row['Teor']
        add_line(f"{teor.upper()}:")
        add_line(f"  • Quantidade: {row['Quantidade']:,} mensagens ({row['Porcentagem']:.1f}% do total)")
        add_line(f"  • Views total: {row['Total_Views']:,.0f}")
        add_line(f"  • Views média: {row['Media_Views']:.0f} por mensagem")
        add_line(f"  • Forwards total: {row['Total_Forwards']:,.0f}")
        add_line(f"  • Forwards média: {row['Media_Forwards']:.1f} por mensagem")
        add_line("")
    
    add_line("4. RESUMO")
    add_line("-" * 70, separator=False)
    add_line("")
    
    if len(df_engajamento) > 0:
        # Teor mais prevalente
        teor_mais_prevalente = df_engajamento.iloc[0]
        add_line(" TEOR MAIS PREVALENTE:")
        add_line(f"   {teor_mais_prevalente['Teor']}")
        add_line(f"   • {teor_mais_prevalente['Quantidade']:,} mensagens ({teor_mais_prevalente['Porcentagem']:.1f}% do total)")
        add_line(f"   • {teor_mais_prevalente['Total_Views']:,.0f} views totais")
        add_line(f"   • {teor_mais_prevalente['Total_Forwards']:,.0f} forwards totais")
        add_line("")
        
        # Teor com mais views
        teor_mais_views = df_engajamento.loc[df_engajamento['Total_Views'].idxmax()]
        add_line(" TEOR COM MAIS VIEWS:")
        add_line(f"   {teor_mais_views['Teor']}")
        add_line(f"   • {teor_mais_views['Total_Views']:,.0f} views totais")
        add_line(f"   • {teor_mais_views['Media_Views']:.0f} views/mensagem")
        add_line("")
        
        # Teor com mais forwards
        teor_mais_forwards = df_engajamento.loc[df_engajamento['Total_Forwards'].idxmax()]
        add_line(" TEOR COM MAIS FORWARDS:")
        add_line(f"   {teor_mais_forwards['Teor']}")
        add_line(f"   • {teor_mais_forwards['Total_Forwards']:,.0f} forwards totais")
        add_line(f"   • {teor_mais_forwards['Media_Forwards']:.1f} forwards/mensagem")
        add_line("")
        
        # Teor com maior média de views
        if df_engajamento['Media_Views'].max() > 0:
            teor_maior_media_views = df_engajamento.loc[df_engajamento['Media_Views'].idxmax()]
            add_line(" TEOR COM MAIOR MÉDIA DE VIEWS:")
            add_line(f"   {teor_maior_media_views['Teor']}")
            add_line(f"   • {teor_maior_media_views['Media_Views']:.0f} views/mensagem")
            add_line("")
        
        # Teor com maior média de forwards
        if df_engajamento['Media_Forwards'].max() > 0:
            teor_maior_media_forwards = df_engajamento.loc[df_engajamento['Media_Forwards'].idxmax()]
            add_line(" TEOR COM MAIOR MÉDIA DE FORWARDS:")
            add_line(f"   {teor_maior_media_forwards['Teor']}")
            add_line(f"   • {teor_maior_media_forwards['Media_Forwards']:.1f} forwards/mensagem")
            add_line("")
        
        # Comparação entre teores
        add_line(" COMPARAÇÃO ENTRE TEORES:")
        add_line(f"   • Teores analisados: {len(df_engajamento)}")
        add_line(f"   • Views por teor (média): {df_engajamento['Total_Views'].mean():,.0f}")
        add_line(f"   • Forwards por teor (média): {df_engajamento['Total_Forwards'].mean():,.0f}")
        add_line("")
    
else:
    add_line("❌ Colunas necessárias não encontradas no DataFrame")
    add_line("Colunas disponíveis:")
    for col in df.columns:
        add_line(f"  - {col}")

# 6. RODAPÉ
add_line("=" * 70, separator=True)
add_line("ANÁLISE CONCLUÍDA!")
add_line("=" * 70, separator=True)

# SALVAR TUDO EM UM ARQUIVO TXT
nome_arquivo_saida = f"resultado_analise_{nome_arquivo}.txt"

try:
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(conteudo_txt))
    print(f" Análise salva com sucesso em: {nome_arquivo_saida}")
    print(f" Total de linhas: {len(conteudo_txt)}")
    
except Exception as e:
    print(f"❌ Erro ao salvar arquivo: {e}")

# Mostrar preview no console
print("\n" + "=" * 70)
print("PRÉVIA DOS RESULTADOS:")
print("=" * 70)
for i, linha in enumerate(conteudo_txt[:20]):  # Mostra as primeiras 20 linhas
    print(linha)
print("...\n")
print(f"(Arquivo completo salvo em {nome_arquivo_saida})")