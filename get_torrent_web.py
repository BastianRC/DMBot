import time
from bs4 import BeautifulSoup as bs
from Data_Folder.config_bot import Config as cg
from save_torrents import SaveMovieData
import requests, subprocess, os

class GetDataMovies:
    def __init__(self):
        r = requests.get(cg.PAGE_MOVIE, cg.HEADERS)
        self.soup = bs(r.text, 'lxml')

        if(r.status_code == 200):
            print("\nLa web se ha cargado correctamente.")
            self.mdt = SaveMovieData()
        else:
            print("Error al cargar la web: " + r.status_code)
    
    def GetUrlInfo(self):
        data = self.soup.find("ul", attrs={"class":"miniboxs miniboxs-ficha"}).find_all("li")
        self.name = str(data[0].find("div", attrs={"class":"meta"}).get_text()).replace("\n", "")

        self.lang = str(data[0].find("div", attrs={"class":"imagen"}).find("span", attrs={"id":"idiomacio"}).find("img")["title"])
        self.quality = data[0].find("div", attrs={"class":"imagen"}).find("span", attrs={"style":"right: 0px;left: auto;max-width: 60%;"}).i.get_text()
        
        final_data = None

        if(self.lang.endswith("VOSE") or self.lang.endswith("Castellano") and self.quality == "HDTV" or self.quality == "DVDrip"):
            final_data = data[0].find("div", attrs={"class":"meta"}).a.get("href")

        return final_data
    
    def GetUrlDownload(self):
        url_info = self.GetUrlInfo()
        r = requests.get(url_info, cg.HEADERS)

        soup = bs(r.text, 'lxml')

        self.year = soup.find("p", attrs={"class":"descrip"}).find("span").get_text().replace("Fecha: ", "").split("-")[0]
        torrent = soup.find("div", attrs={"class":"enlace_descarga"}).find_all("a", attrs={"class":"enlace_torrent degradado1"})[1].get('href')
        
        rData = self.mdt.ReadData(cg.PATH_DATA_FOLDER + cg.FILE_NAME)

        if(int(self.year) >= cg.YEAR_SEARCH):
            if(rData is None):
                self.mdt.WriteData(cg.PATH_DATA_FOLDER + cg.FILE_NAME,[url_info, self.name, self.quality, self.lang, self.year])

                print("Estreno encontrado.")
                return str(torrent)
            elif(not rData[0] == url_info and not rData[2] == self.quality and not rData[4] == self.year):
                self.mdt.WriteData(cg.PATH_DATA_FOLDER + cg.FILE_NAME,[url_info, self.name, self.quality, self.lang, self.year])

                print("Estreno encontrado.")
                return str(torrent)
            else:
                return None
        else:
            return None
    
    def UpdateMovieDownloaded(self, name, format):
        subprocess.call(["mv", cg.PATH_SAVE + "/" + name, cg.PATH_SAVE + "/" + self.name + " (" + self.year + ")." + format])
        os.chmod(cg.PATH_SAVE + "/" + self.name + " (" + self.year + ")." + format, 0o644)
        os.chown(cg.PATH_SAVE + "/" + self.name + " (" + self.year + ")." + format, 0, 0)

if __name__ == "__main__":
    urlMovies = GetDataMovies()
    print(urlMovies.GetUrlDownload())