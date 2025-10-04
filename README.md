# SmartSorter - Organizador Inteligente de Arquivos

## Visão Geral

SmartSorter é um organizador de arquivos modular e inteligente, desenvolvido em Python com interface Tkinter, que permite:

- Organizar arquivos automaticamente por categorias padrão ou personalizadas
- Aprendizado incremental com prioridade do usuário
- Integração opcional com IA para classificação inteligente
- Processamento de PDFs, DOCX e imagens com OCR
- Função desfazer última organização

O projeto é totalmente configurável, permitindo ao usuário criar, editar e remover categorias e confirmar/alterar a classificação antes da movimentação.

---

## Recursos

- Classificação automática por extensão e conteúdo
- Categorias personalizadas controladas pelo usuário
- Correção manual de cada arquivo com atualização da memória
- Aprendizado incremental com prioridade para escolhas do usuário
- Integração opcional com IA (OpenAI GPT)
- OCR para imagens e PDFs
- Desfazer última organização
- Interface intuitiva com log detalhado

---

## Requisitos

- Python 3.10 ou superior
- Bibliotecas Python:

```bash
pip install tkinter pillow python-docx PyPDF2 pytesseract openai
```

- Tesseract OCR (necessário para OCR):

```bash
sudo apt install tesseract-ocr
```

- Se for no Windows: Instalar Tesseract OCR e adicionar ao PATH do sistema.

---

## Estrutura do Projeto

```bash
SmartSorter/
│
├─ src/
│   ├─ smart_sorter.py         # Interface Tkinter principal
│   ├─ organizador.py          # Funções para organizar arquivos
│   ├─ classificador.py        # Classificação, IA opcional, memória e prioridade
│   ├─ desfazer.py             # Função para desfazer a última organização
│   └─ utils.py                # Funções auxiliares (PDF, DOCX, imagens, OCR)
│
├─ data/
│   ├─ categorias.json         # Categorias personalizadas
│   ├─ memoria.json            # Memória incremental com prioridade
│   └─ historico_organizacao.json  # Histórico da última organização (desfazer)
│
├─ requirements.txt            # Dependências do projeto
└─ README.md                   # Documentação do projeto
```
---

## Como Usar

- Executando a Interface

```bash
python3 smart_sorter.py
```

Passos:

Selecione a pasta que deseja organizar

Ative ou desative:

IA para classificação (opcional)

Correção manual antes de mover cada arquivo

Adicione, edite ou remova categorias personalizadas conforme necessário

Clique em Organizar para iniciar

Para desfazer, clique em Desfazer Última Organização

Durante a correção manual, você pode confirmar a categoria sugerida ou escolher/criar uma nova, que será salva na memória com prioridade.

---

## Memória Incremental e Prioridade do Usuário

- Cada arquivo organizado tem peso na memória

- Correções manuais aumentam o peso, garantindo que suas escolhas tenham prioridade

- IA e classificação automática respeitam essa prioridade

Exemplo de entrada em memoria.json:

```json
{
  "/home/user/Downloads/arquivo.pdf": {
    "categoria": "Documentos",
    "peso": 3
  }
}

```

---

## Integração com IA

- Opcional, usando OpenAI GPT
- Necessário informar a API key em smart_sorter.py:

```python
openai.api_key = "SUA_CHAVE_AQUI"
```

- A IA sugere categorias para PDFs, DOCX e imagens
- Respeita a prioridade do usuário quando existente

--- 

## OCR

- Extração de texto de imagens e PDFs
- Requer pytesseract e Tesseract OCR instalado
- Permite IA ou busca de palavras-chave para classificação

---

## Desfazer Última Organização

- Salva histórico em historico_organizacao.json
- Permite restaurar arquivos à pasta original
- Mantém memória incremental

---

## Como Expandir

- Adicionar suporte a mais tipos de arquivos
- Melhorar integração com IA para classificação mais precisa
- Implementar regras personalizadas por usuário
- Criar interface web usando Flask ou Streamlit

## Licença

Projeto livre para uso pessoal e comercial. Sinta-se à vontade para adaptar, modificar ou integrar em outros projetos.

## Contato

- Desenvolvedor: João Miguel Almeida
- Email: [seu_email@exemplo.com]