import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from pyod.models.iforest import IForest

# Configuração da página do Streamlit
st.set_page_config(page_title="Detector de Fraudes", layout="wide")
st.title("🚨 Detector Inteligente de Fraudes com IA")

st.markdown("Carregue um arquivo CSV com os dados de transações para identificar padrões anômalos automaticamente.")

# Componente para upload do arquivo CSV
uploaded_file = st.file_uploader("📁 Escolha o arquivo CSV", type="csv")

if uploaded_file is not None:
    # Leitura do arquivo carregado
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Amostra dos Dados Carregados")
    st.dataframe(df.head())

    # Define a lista de colunas que o modelo e as regras esperam
    colunas_necessarias = [
        'valor',
        'tempo_empresa_anos',
        'tipo_transacao',
        'segmento',
        'pico_horario_transacoes',
        'porte_empresa'
    ]

    # Verifica se todas as colunas necessárias existem no DataFrame
    if all(col in df.columns for col in colunas_necessarias):
        
        # Converte colunas categóricas para o tipo 'category' para manipulação
        # Isso não altera os dados, apenas a forma como o pandas os armazena
        for col in ['tipo_transacao', 'segmento', 'pico_horario_transacoes', 'porte_empresa']:
            if col in df.columns:
                df[col] = df[col].astype('category')

        # Cria uma cópia do DataFrame para o pré-processamento do modelo
        # Isso garante que o DataFrame original (usado para exibição) não seja alterado
        df_modelo = df.copy()

        # Codifica as variáveis categóricas para formato numérico para o modelo
        for col in ['tipo_transacao', 'segmento', 'pico_horario_transacoes', 'porte_empresa']:
            if col in df_modelo.columns:
                df_modelo[col] = df_modelo[col].cat.codes

        # Seleciona as colunas para o modelo de IA
        X = df_modelo[colunas_necessarias]

        # Padroniza os dados (coloca tudo na mesma escala)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # --- CORREÇÃO DO ERRO 'EVAL' ---
        # O parâmetro 'contamination' foi trocado de 'auto' para um valor numérico (0.1)
        # para garantir a compatibilidade com diferentes versões da biblioteca PyOD.
        modelo = IForest(contamination=0.1, random_state=42)
        
        # Treina o modelo e faz a predição
        modelo.fit(X_scaled)
        df['anomaly'] = modelo.predict(X_scaled)  # Resultado: 0 = normal, 1 = suspeita

        # --- REGRAS DE NEGÓCIO ADICIONAIS ---
        st.subheader("🔍 Critérios Adicionais para Transações Suspeitas")
        st.markdown("Além da detecção por IA, as transações também são marcadas como suspeitas se atenderem a regras de negócio específicas:")
        st.markdown("- **Alto Valor**: Transações cujo valor está entre os 1% maiores valores do conjunto de dados.")
        st.markdown("- **Empresa Nova e Alto Valor**: Transações de empresas com menos de 2 anos e com valor acima do percentil 90.")
        st.markdown("- **Transações Noturnas Anômalas**: Transações (se houver data/hora) realizadas entre 00:00 e 06:00 com valor acima de R$ 500.")

        # Regra 1: Transações de altíssimo valor
        df.loc[df['valor'] > df['valor'].quantile(0.99), 'anomaly'] = 1

        # Regra 2: Empresas novas com transações de alto valor
        df.loc[(df['tempo_empresa_anos'] < 2) & (df['valor'] > df['valor'].quantile(0.90)), 'anomaly'] = 1

        # Regra 3: Transações noturnas anômalas (se a coluna 'data_hora' existir)
        if 'data_hora' in df.columns:
            df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
            df['hora'] = df['data_hora'].dt.hour
            df.loc[(df['hora'] >= 0) & (df['hora'] < 6) & (df['valor'] > 500), 'anomaly'] = 1

        # Cria um DataFrame final apenas com as transações suspeitas
        suspeitas = df[df['anomaly'] == 1].copy()

        # --- MÉTRICAS ---
        total = len(df)
        total_suspeitas = len(suspeitas)
        porcentagem = (total_suspeitas / total) * 100 if total > 0 else 0

        st.subheader("📈 Métricas da Análise")
        col1, col2, col3 = st.columns(3)
        col1.metric("Transações Totais", f"{total:,}")
        col2.metric("Suspeitas Detectadas", f"{total_suspeitas:,}")
        col3.metric("Porcentagem de Suspeitas", f"{porcentagem:.2f}%")

        # --- GRÁFICOS ---
        
        # Gráfico 1: Quantidade de Fraudes por Segmento
        st.subheader("📊 Quantidade de Possíveis Fraudes por Segmento")
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if not suspeitas.empty and 'segmento' in suspeitas.columns:
            # A contagem é feita diretamente nos nomes dos segmentos, que já estão corretos
            fraudes_por_segmento = suspeitas['segmento'].value_counts().reset_index()
            fraudes_por_segmento.columns = ['segmento', 'quantidade_fraudes']
            
            sns.barplot(data=fraudes_por_segmento, x='segmento', y='quantidade_fraudes', palette='viridis', ax=ax)
            ax.set_xlabel("Segmento", fontsize=12)
            ax.set_ylabel("Quantidade de Fraudes", fontsize=12)
            ax.set_title("Distribuição de Fraudes por Segmento", fontsize=14)
            plt.xticks(rotation=45, ha='right')
            ax.grid(axis='y', linestyle='--', alpha=0.7)
        else:
            ax.text(0.5, 0.5, "Nenhuma fraude detectada para exibir por segmento.",
                      horizontalalignment='center', verticalalignment='center',
                      transform=ax.transAxes, fontsize=14, color='gray')
            ax.set_xticks([])
            ax.set_yticks([])
        st.pyplot(fig)

        # Gráfico 2: Dispersão para visualizar anomalias
        st.subheader("🧮 Mapa de Transações: Tempo de Empresa vs. Valor")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.scatterplot(data=df, x="tempo_empresa_anos", y="valor", hue="anomaly", palette={0: "#2196F3", 1: "#FF5722"}, s=80, alpha=0.7, ax=ax2)
        ax2.set_xlabel("Tempo de Empresa (anos)", fontsize=12)
        ax2.set_ylabel("Valor da Transação (R$)", fontsize=12)
        ax2.set_title("Transações Suspeitas (Laranja) vs. Normais (Azul)", fontsize=14)
        ax2.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig2)

        # --- TABELA DE TRANSAÇÕES SUSPEITAS ---
        st.subheader("🚨 Tabela de Transações Suspeitas Detectadas")
        
        # O DataFrame 'suspeitas' já contém os nomes corretos para as categorias
        # Não é necessário nenhum mapeamento adicional.
        st.dataframe(suspeitas)

        # Botão para baixar o resultado
        csv_suspeitas = suspeitas.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Baixar transações suspeitas como CSV",
            data=csv_suspeitas,
            file_name='transacoes_suspeitas.csv',
            mime='text/csv',
        )
    else:
        # Mensagem de erro se o arquivo CSV não tiver as colunas corretas
        st.error(f"❌ ERRO: O arquivo CSV carregado não contém todas as colunas necessárias. Verifique se o seu arquivo possui as seguintes colunas: {', '.join(colunas_necessarias)}")