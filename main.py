from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

headers= {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}

CDN_BASE_URL = "https://comdotcdn.com/games/files/"
SEARCH_URL = "https://www.comdotgame.com/recent/"


def downloadGame(url, filename):
    file_size = int(requests.head(url).headers["Content-Length"])
    
    pbar = tqdm(total=file_size, initial=0, unit="B", unit_scale=True, desc=filename)
    
    req = requests.get(url, headers=headers, stream=True)
    
    with(open(filename+".swf", "wb")) as f:
        for chunck in req.iter_content(chunk_size=1024):
            if chunck:
                size = f.write(chunck)
                pbar.update(size)

    pbar.close()



def scrapGames(url):
    src = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

    listgame = src.find("ul", {"class":"games with-top"}).find_all("li", {"class":"game left"})

    for game in listgame:
        thumb = game.find("span", {"class":"thumb"})
        style = thumb["style"] 
        style = style[style.rfind("/")+1:style.rfind(")")].replace(".jpg", ".swf")
        
        game_url = CDN_BASE_URL + style
        name= game.find("a")["href"]
        name = name[name.rfind("/")+1:]

        downloadGame(game_url, name)

if __name__ == "__main__": 
    for i in range(1, 103):
        scrapGames(SEARCH_URL + str(i))