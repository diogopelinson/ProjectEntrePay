# 🚨 Detector Inteligente de Fraudes com IA  

Este projeto apresenta um **protótipo interativo** para **detecção de transações suspeitas** em bancos digitais e tradicionais, unindo **Inteligência Artificial** e **regras de negócio**.  

---

## 💼 Por que esse projeto?  

O setor bancário enfrenta diariamente:  
- Uso indevido de cartões e contas;  
- Chargebacks recorrentes;  
- Transações fora do perfil esperado (horário, valor, histórico da empresa).  

Esses problemas afetam tanto **bancos digitais** (com alto volume de operações em tempo real) quanto **bancos tradicionais**, que precisam lidar com diferentes canais (agência, internet banking, POS).  

**Consequências:**  
- 📉 Perdas financeiras significativas  
- ❌ Queda na confiança do cliente  
- 💸 Aumento do custo operacional  

---

## 🧠 O que o sistema faz  

- **Carregamento de dados (CSV)** de transações  
- **Detecção de anomalias via IA** com Isolation Forest (PyOD)  
- **Regras adicionais de negócio**:  
  - Transações acima do percentil 99 (altíssimo valor)  
  - Empresas novas (< 2 anos) com valores elevados  
  - Transações noturnas (> R$ 500 entre 00:00–06:00)  
- **Visualizações interativas**:  
  - Distribuição de fraudes por segmento  
  - Dispersão entre valor da transação e tempo de empresa  
- **Exportação das suspeitas em CSV**  

---

## 📊 Impacto esperado  

- 🔐 Redução de perdas com fraudes e chargebacks  
- 🤝 Maior segurança e confiança para clientes  
- ⚡ Agilidade para times de risco, com foco nos casos críticos  
- 🎯 Menos falsos positivos, melhorando a experiência do usuário  

---

## ⚙️ Tecnologias utilizadas  

- **Python**  
- **Streamlit** (dashboard interativo)  
- **PyOD (Isolation Forest)**  
- **Pandas**, **Scikit-Learn**  
- **Seaborn**, **Matplotlib**  

---

💡 Este projeto mostra como **IA aliada a regras inteligentes** pode apoiar bancos a **prevenir fraudes em tempo real**, equilibrando **segurança, eficiência operacional e experiência do cliente**.  
