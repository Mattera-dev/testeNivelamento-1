import requests
from bs4 import BeautifulSoup
import re
import os
import zipfile



class ScraperGOV:
    def __init__(self, url: str):
        self.url = url
        
    def __getPage(self) -> str:
        res = requests.get(self.url)
        if res.status_code != 200:
            raise Exception(f"Error trying to get page content in {self.url}")
        return res.text

    def __extractData(self) -> dict[str]:
        content: str = self.__getPage()
        if not content:
            raise Exception("Content is missing and cant be parsed")
        soup = BeautifulSoup(content, "html.parser")
        links: list[dict[str, str]] = []
        for link in soup.find_all("a", class_="internal-link", string=re.compile(r"anexo", re.IGNORECASE)):
            url = link.get("href") 
            if url.endswith(".pdf"):
                links.append({"name": link.string, "url": url})
        if len(links) != 0:
            return links
        else:
            raise Exception(f"Not found links in this page {self.url}")
    
    def __downloadData(self):
        links = self.__extractData()
        baseDir = os.path.dirname(os.path.abspath(__file__))

        for data in links:
            try:
                res = requests.get(data.get("url"))
                if res.status_code != 200:
                    raise Exception(f"Failed downloading file {data.name}, code {res.status_code}")
                filePath = os.path.join(baseDir, "data", f'{data.get("name")}pdf')
                os.makedirs(os.path.dirname(filePath), exist_ok=True)
                with open(filePath, "wb") as pdf:
                    pdf.write(res.content)
                    print(f"Downloaded {pdf.name}")
            except Exception as e:
                raise e
        return True
    
    def __compactData(self):
        baseDir = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(baseDir, "output", "anexos.zip")
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        if self.__downloadData():
            try:
                with zipfile.ZipFile(filePath, "w") as fileZip:
                    for fileName in os.listdir(os.path.join(baseDir, "data")):
                        pdfPath = os.path.join(baseDir, "data", fileName )
                        
                        fileZip.write(pdfPath, arcname=fileName) if os.path.isfile(pdfPath) else print(f"File need to be an archive not a directory, {pdfPath}")
            except Exception as e:
                raise e
        else:
            print("Aborting data compression due to an error during download") 
    
    def start(self):
        print(f"Started scraping for pdf files in:\n{self.url}\n")
        try:
            self.__compactData()
            print("\nScrapped with success!")
        except Exception as e:
            raise e
        
            
