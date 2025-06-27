from bs4 import BeautifulSoup
import pandas as pd
import requests
from rich.table import Table
from src.log_config import setup_logger
from typing import List


# Configuração do logger
logger = setup_logger()

# Processo de coleta dos dados de notícias do G1
def get_last_news(limit: int = 7) -> List:

    logger.info("Iniciando a coleta de últimas notícias do G1")
    
    url = "https://g1.globo.com/ultimas-noticias/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0"
    }
    
    news_list = []
    
    try:
    
        while len(news_list) < limit:
            logger.debug(f"Requisitando a URL: {url}")
            response = requests.get(url=url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Encontrar as seções de notícias no arquivo HTML
            posts = soup.find_all("div", class_="bastian-feed-item")
            logger.debug(f"Encontradas {len(posts)} seções de notícia na página")
            
            for post in posts:
                news_title = post.find("a", class_="feed-post-link")
                news_description = post.find("div", class_="feed-post-body-resumo")
                news_link = post.find("a", class_="feed-post-link")
                news_image = post.find("img", class_="bstn-fd-picture-image")
                
                if all([news_title, news_description, news_link, news_image]):
                    title = news_title.get_text(strip=True, separator=" ")
                    description = news_description.get_text(strip=True, separator=" ")
                    link = news_link["href"]
                    image = news_image["src"]
                    
                    # Adiciona os dados da notícia à lista
                    news_list.append({
                        "title": title,
                        "description": description,
                        "link": link,
                        "image": image
                    })
                    
                    logger.info(f"Notícia coletada: {title}")

                    if len(news_list) >= limit:
                        break
                
                # Buscar o botão de "Veja Mais" em busca de mais notícias
                load_more_bt = soup.find("div", class_="load-more gui-color-primary-bg")
                if load_more_bt and load_more_bt.find("a"):
                    next_page_url = load_more_bt.find("a")["href"]
                    logger.debug(f"Próxima página encontrada: {next_page_url}")
                    url = next_page_url
                else:
                    logger.debug("Nenhuma página adicional encontrada. Finalizando a coleta.")
                    break
        
        logger.info(f"Coleta finalizada. Total de notícias coletadas: {len(news_list)}")
        return news_list

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erro HTTP ao coletar notícias: {http_err}")
        raise RuntimeError(f"Ocorreu um erro durante a captura das notícias") from http_err
    except Exception as e:
        logger.error(f"Erro inesperado ao coletar notícias: {e}")
        raise Exception("Ocorreu um erro inesperado no processo de coleta de notícias") from e

# Função para exibir as notícias coletadas através da biblioteca Rich
def display_news(news_list: List) -> None:
    table = Table(title="G1 - Últimas Notícias")
    
    table.add_column("Título", style="cyan", highlight=True, justify="center", no_wrap=False)
    table.add_column("Descrição", style="cyan", highlight=True, justify="center", no_wrap=False)
    table.add_column("Link da Notícia", style="cyan", highlight=True, justify="center", no_wrap=False)
    table.add_column("Link da Imagem", style="cyan", highlight=True, justify="center", no_wrap=False)
    
    for news in news_list:
        table.add_row(
            news['title'],
            news['description'] + '\n',
            news['link'],
            news['image'],
        )
        table.add_row('-----------------------')
        
    logger.debug(f"Gerada tabela de notícias com {len(news_list)} entradas.")
    return table

def save_news_to_txt_file(news_list: List, filepath: str) -> None:
    try:
        with open(file=filepath, mode="w", encoding="utf-8") as file:
            for news in news_list:
                file.write(f"Título: {news['title']}\n")
                file.write(f"Descrição: {news['description']}\n")
                file.write(f"Link da Notícia: {news['link']}\n")
                file.write(f"Link da Imagem: {news['image']}\n")
                file.write("\n\n")

        logger.info(f"Notícias salvas no arquivo {filepath} com sucesso.")
    
    except Exception as e:
        logger.error(f"Erro ao salvar notícias no arquivo {filepath}: {e}")
        raise RuntimeError(f"Ocorreu um erro ao salvar as notícias no arquivo {filepath}") from e

def save_news_to_csv_file(news_list: List, filepath: str) -> None:
    try:
        df = pd.DataFrame(news_list)
        df.to_csv(filepath, index=False, encoding="utf-8")
        
        logger.info(f"Notícias salvas no arquivo CSV {filepath} com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao salvar notícias no arquivo CSV {filepath}: {e}")
        raise RuntimeError(f"Ocorreu um erro ao salvar as notícias no arquivo CSV {filepath}") from e
    