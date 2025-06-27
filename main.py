import argparse
from datetime import datetime
import os
from rich.console import Console
from rich.live import Live
from src.scraper import (
    get_last_news,
    display_news,
    save_news_to_txt_file,
    save_news_to_csv_file,
)
import time


def run_once(console: Console) -> None:
    # Coleta as últimas 40 notícias do G1
    news = get_last_news(limit=40)
    
    # Exibe as notícias coletadas
    console.print(display_news(news))
    
    # Salva as notícias em um arquivo de texto
    save_news_to_txt_file(news, filepath="data/one_time/datanews.txt")
    
    # Salva as notícias em um arquivo CSV
    save_news_to_csv_file(news, filepath="data/one_time/datanews.csv")

def run_in_loop(console: Console) -> None:
    while True:
        
        console.clear()
        
        # Coleta as últimas 40 notícias do G1
        news = get_last_news(limit=40)
    
        display_list = []
        
        with Live(display_news(display_list), console=console, refresh_per_second=1, vertical_overflow='visible') as live:
            for _, article in enumerate(news, start=1):
                display_list.append(article)
                # Atualiza a exibição com uma nova notícia coletada
                live.update(display_news(display_list)) 
                # Espera 3 segundos antes de adicionar a próxima notícia na tabela
                time.sleep(3)
                
                if len(display_list) % 5 == 0:
                    console.clear()
        
        # Gera timestamp para o nome do arquivo
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        txt_filepath = f"data/loop/txt/datanews_{timestamp}.txt"
        csv_filepath = f"data/loop/csv/datanews_{timestamp}.csv"
        
        save_news_to_txt_file(news, txt_filepath)
        save_news_to_csv_file(news, csv_filepath)
        
        console.print(f"[bold green]Arquivos salvos: {txt_filepath}, {csv_filepath}[/]")
        console.print("[bold yellow]Aguardando 10 minutos para nova coleta...[/]")
        
        # Aguarda 10 minutos antes de coletar novamente
        time.sleep(600) 

def main():
    
    console = Console()
    
    parser = argparse.ArgumentParser(description="Script de coleta de notícias do G1")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Executa o script em loop, coletando notícias a cada 30 minutos.",
    )
    
    args = parser.parse_args()
    
    os.makedirs("data/one_time", exist_ok=True)
    os.makedirs("data/loop", exist_ok=True)
    if os.path.exists("data/loop"):
        os.makedirs("data/loop/txt", exist_ok=True)
        os.makedirs("data/loop/csv", exist_ok=True)
    
    if args.loop:
        console.print("[bold blue]Iniciando coleta de notícias em loop...[/]")
        run_in_loop(console)
    else:
        console.print("[bold blue]Iniciando coleta de notícias uma vez...[/]")
        run_once(console)

if __name__ == "__main__":
    main()
