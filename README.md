# G1 Web Scraper

Este projeto é um **web scraper** desenvolvido em Python para coletar, exibir e salvar as últimas notícias publicadas no portal [G1 - Globo](https://g1.globo.com/ultimas-noticias/). Utiliza bibliotecas modernas como `BeautifulSoup`, `Rich` e `Pandas` para parsing de HTML, visualização no terminal e persistência dos dados coletados.

---

## Funcionalidades

- 🔍 Coleta automatizada das últimas notícias do G1
- 📊 Exibição interativa e colorida no terminal via `rich`
- 💾 Salvamento em arquivos `.txt` e `.csv`
- 🔁 Execução contínua (modo loop) com salvamento periódico
- 📦 Estrutura organizada e com logging em tempo real

---

## Estrutura do Projeto

```bash
g1-scraper/
│
├── data/                  # Diretório de saída dos dados salvos
│   ├── loop/              # Arquivos salvos em modo loop
│   │   ├── csv/
│   │   └── txt/
│   └── one_time/          # Arquivos salvos em execução única
│
├── src/
│   ├── __init__.py
│   ├── scraper.py         # Script principal de scraping, exibição e salvamento
│   └── log_config.py      # Configuração centralizada de logging
│
├── main.py                # Ponto de entrada do projeto
├── .gitignore
├── requirements.txt
└── README.md              # Este arquivo
```

---

## Requisitos

- Python 3.8+
- Terminal compatível com `UTF-8` (para renderização com a biblioteca `rich`)

---

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/JoseGayosoNeto/G1-web-scrapper.git
cd G1-web-scrapper
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o script

- **Execução única:**
    - Coleta as últimas 40 notícias do G1, exibe no terminal e salva os dados nos arquivos:
        - <code>data/one_time/datanews.txt</code>
        - <code>data/one_time/datanews.csv</code>

    ```bash
    python main.py
    ```

- **Execução contínua (loop):**
    - Coleta as notícias a cada 10 minutos, exibe dinamicamente no terminal e salva com timestamp nos diretórios:
        - <code>data/loop/txt/</code>
        - <code>data/loop/csv/</code>
    ```bash
    python main.py --loop
    ```
    - Durante a execução em loop, as notícias são exibidas em tempo real usando `rich.Live` com atualização gradual, e os arquivos são salvos automaticamente a cada ciclo.

---

## Observações Técnicas

- A tabela de exibição é atualizada notícia por notícia com `rich.live`, criando uma experiência fluida no terminal.
- O sistema de logs exibe mensagens em tempo real no console com diferentes níveis: `INFO`, `DEBUG` e `ERROR`.
- Os arquivos de saída são organizados conforme o modo de execução:
    - `one_time/`: salvamento único e sobrescrito.
    - `loop/`: salvamentos periódicos com nome baseado no horário da coleta.
- O número de notícias coletadas pode ser facilmente ajustado modificando o valor do parâmetro limit nas chamadas da função `get_last_news(limit=40)`, localizadas nos arquivos `main.py`.

---

## Tipos de Dados Coletados

Durante o processo de scraping do portal [G1 - Últimas Notícias](https://g1.globo.com/ultimas-noticias/), os seguintes dados são extraídos para cada notícia:

| Campo              | Descrição                                                                 |
|-------------------|---------------------------------------------------------------------------|
| **Título**         | O título principal da notícia.                                            |
| **Descrição**      | Um breve resumo ou subtítulo da notícia.                                 |
| **Link da Notícia**| URL direta para a notícia completa no portal G1.                         |
| **Link da Imagem** | URL da imagem associada à notícia, normalmente exibida como thumbnail.   |

Esses dados são exibidos no terminal em formato de tabela e também salvos nos arquivos `.txt` e `.csv`, organizados de acordo com o modo de execução escolhido.

---

## Aviso Legal

- Os dados são extraídos de uma página pública do G1 e não devem ser usados para fins comerciais. Respeite os Termos de Uso do site original.

---

## Autor

- Desenvolvido por José Gayoso Neto
    - Github: [@JoseGayosoNeto](https://github.com/JoseGayosoNeto)
    - Linkedin: [www.linkedin.com/in/josegayosoneto/](https://www.linkedin.com/in/josegayosoneto/)
