# ⚽ Fine-Tuning e Avaliação de LLMs para Análise de Futebol

Este repositório contém um pipeline completo para treinamento, inferência e avaliação de modelos de linguagem (LLMs) adaptados ao domínio futebolístico. O projeto utiliza dados reais extraídos da API do [Sofascore](https://www.sofascore.com), organizados para tarefas supervisionadas de classificação e question answering (QA) no estilo Alpaca.

## 📂 Estrutura do Repositório

```
├── get_players.ipynb      # Extrai estatísticas individuais de jogadores
├── get_teams.ipynb        # Extrai estatísticas agregadas por time
├── get_tables.ipynb       # Extrai e converte tabelas de classificação por campeonato
├── train_model.ipynb      # Realiza o fine-tuning supervisionado com Unsloth (LoRA 4-bit)
├── evaluate_model.ipynb   # Avalia os modelos (fine-tuned, base e GPT-4o) com métricas automáticas
├── /dados_rag_new         # Pasta com os arquivos CSV gerados (Google Drive ou local)
└── README.md              # Este arquivo
```

## 🚀 Visão Geral das Etapas

### 1. `get_players.ipynb` – Coleta de Dados de Jogadores

- Extrai estatísticas individuais por jogador em partidas encerradas.
- Filtra jogadores com base em posição e estatísticas mínimas.
- Gera um dataset para classificação de desempenho: **bom**, **mediano** ou **ruim**.
- Salva os dados como CSVs para cada campeonato e um consolidado para fine-tuning.

### 2. `get_teams.ipynb` – Coleta de Dados de Times

- Coleta estatísticas de time por evento (posse, finalizações, precisão de passes etc.).
- Classifica o desempenho de cada time por critérios heurísticos (xG, posse, chutes).
- Gera dataset supervisionado para classificação do time por partida.

### 3. `get_tables.ipynb` – Extração de Tabelas Hierárquicas

- Acessa diretamente endpoints da Sofascore para obter as classificações por temporada.
- Gera exemplos de QA baseados em tabelas: 
  - Cell selection, Superlative, Aggregation, Difference, Average, Thresholds.
- Salva exemplos balanceados para uso no fine-tuning multitarefa.

### 4. `train_model.ipynb` – Fine-Tuning Supervisionado

- Usa o framework [Unsloth](https://github.com/unslothai/unsloth) com LLaMA 3.1 8B quantizado (4bit).
- Aplica LoRA para ajuste eficiente com baixo uso de memória.
- Treina com `SFTTrainer` por 60 steps (ajustável).
- Salva e publica os adaptadores LoRA no Hugging Face Hub.

### 5. `evaluate_model.ipynb` – Avaliação Comparativa de Modelos

- Compara 3 modelos: `Fine-Tuned`, `Base` (LLaMA 3.1) e `GPT-4o`.
- Métricas usadas:
  - **BLEU**, **ROUGE**, **BERTScore**, **METEOR**, **GPT-4 Score**
- Gera gráfico comparativo de desempenho entre os modelos.
- Exibe outputs lado a lado para análise qualitativa.

## 🛠️ Requisitos

- Python 3.10+
- GPU com suporte a CUDA (mínimo: 12 GB VRAM para fine-tuning)
- Pacotes principais:
  - `unsloth`, `transformers`, `peft`, `trl`, `datasets`, `huggingface_hub`
  - `sacrebleu`, `rouge-score`, `bert-score`, `nltk`, `playwright`, `cloudscraper`

## 💾 Dados

Os datasets gerados estão estruturados em CSVs:

- `processed_player_data_multi_championship.csv`
- `team_performance_<campeonato>.csv`
- `hierarchical_qa_dataset_balanced_all_seasons.csv`
- `player_performance_analysis_dataset.csv`

Você pode adaptar o script para salvar os dados localmente ou em um diretório montado do Google Drive.

## 📊 Exemplo de Métricas Comparativas

| Modelo       | BLEU | ROUGE-L | BERT-F1 | METEOR | GPT-4 Score |
|--------------|------|----------|---------|--------|--------------|
| Fine-Tuned   | 71.3 | 77.4     | 84.2    | 68.1   | 88.5         |
| Base         | 59.2 | 64.8     | 75.6    | 58.7   | 71.2         |
| GPT-4o       | 84.1 | 82.3     | 89.3    | 72.9   | 93.4         |

## 📤 Publicação no Hugging Face Hub

O modelo fine-tuned é publicado em:

👉 [`guilhermemoraisr/llama3-1-8B-4bit-lora-football-low-steps`](https://huggingface.co/guilhermemoraisr/llama3-1-8B-4bit-lora-football-low-steps)

## 📚 Referências

- [Unsloth: LLaMA Fine-Tuning Framework](https://github.com/unslothai/unsloth)
- [Sofascore Public API](https://www.sofascore.com)
- [Alpaca Format - Stanford CRFM](https://crfm.stanford.edu/2023/03/13/alpaca.html)
- [BERTScore](https://github.com/Tiiiger/bert_score)
- [GPT-4o API - OpenAI](https://platform.openai.com/docs/guides/gpt)