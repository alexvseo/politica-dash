# Dashboard de Anúncios (Sintético) — Ceará

Dashboard feito em **Streamlit** com **dados sintéticos** para simular o desempenho de campanhas
(alcance, tráfego, engajamento e leads) em cidades do Ceará.

## 📦 Estrutura
```
streamlit_political_ads_dashboard/
├─ app.py
├─ dados_sinteticos_anuncios.csv
└─ requirements.txt
```

## ▶️ Rodando localmente
```bash
# 1) Clonar o repositório
git clone <SEU_REPO_GITHUB_URL>.git
cd streamlit_political_ads_dashboard

# 2) Criar venv (opcional)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Instalar dependências
pip install -r requirements.txt

# 4) Rodar
streamlit run app.py
```

## 🚀 Publicando no Streamlit Community Cloud
1. Faça um **fork** ou suba estes arquivos em um repositório público no GitHub.
2. Acesse **https://share.streamlit.io** e conecte sua conta ao GitHub.
3. Em **New app**, selecione o repositório e a branch.
4. **Main file path**: `app.py`
5. Deploy. (O Streamlit vai instalar o `requirements.txt` automaticamente.)

## 🧪 Ajustes rápidos
- Para mudar cidades/objetivos/criativos ou o período, edite a geração de dados no script que criou o CSV original.
- Se quiser usar **dados reais**, basta substituir `dados_sinteticos_anuncios.csv` mantendo as colunas:
  `data, cidade, objetivo, criativo, impressoes, cliques, gastos, leads`.

## ✍️ Observações
- Este projeto é educacional. Os dados não representam uma campanha real.
- KPIs: **CTR = cliques/impressoes**, **CPC = gastos/cliques**, **CPL = gastos/leads**.