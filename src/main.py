from Scraper import ScraperGOV

def main():
    scraper = ScraperGOV("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
    scraper.start()

if __name__ == "__main__":
    main()