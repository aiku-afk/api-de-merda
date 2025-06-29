from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/search")
async def search_links(q: str = Query(..., description="Palavra-chave a ser pesquisada")):
    # montar a URL de busca do DuckDuckGo em modo HTML
    search_url = f"https://duckduckgo.com/html/?q={q}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    # fazer a requisição
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return JSONResponse(status_code=500, content={"error": "Erro ao buscar dados"})
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # DuckDuckGo mostra links nos resultados em <a class="result__a">
    links = []
    for a_tag in soup.select("a.result__a"):
        title = a_tag.get_text()
        link = a_tag.get("href")
        links.append({"title": title, "link": link})
    
    return {"results": links}
