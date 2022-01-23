from operator import le
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

        self.name = []
        self.lang = []
        self.quality = []
        self.final_data = []

        for i in range(5):
            self.name.append(str(data[i].find("div", attrs={"class":"meta"}).get_text()).replace("\n", ""))

            self.lang.append(str(data[i].find("div", attrs={"class":"imagen"}).find("span", attrs={"id":"idiomacio"}).find("img")["title"]))
            self.quality.append(data[i].find("div", attrs={"class":"imagen"}).find("span", attrs={"style":"right: 0px;left: auto;max-width: 60%;"}).i.get_text())

            if(self.lang[i].endswith("VOSE") or self.lang[i].endswith("Castellano") and self.quality[i] == "HDTV" or self.quality[i] == "DVDrip"):
                self.final_data.append(data[i].find("div", attrs={"class":"meta"}).a.get("href"))

        return self.final_data
    
    def GetUrlDownload(self):
        url_info = self.GetUrlInfo()
        list_torrents = []

        count = 0
        rData = self.mdt.ReadData(cg.PATH_DATA_FOLDER + cg.FILE_NAME)

        for url in url_info:
            r = requests.get(url, cg.HEADERS)

            soup = bs(r.text, 'lxml')

            self.year = soup.find("p", attrs={"class":"descrip"}).find("span").get_text().replace("Fecha: ", "").split("-")[0]
            torrent = soup.find("div", attrs={"class":"enlace_descarga"}).find_all("a", attrs={"class":"enlace_torrent degradado1"})[1].get('href')
            
            if(int(self.year) >= cg.YEAR_SEARCH):
                if(rData is None):
                    self.mdt.WriteData(cg.PATH_DATA_FOLDER + cg.FILE_NAME,[url, self.name[count], self.quality[count], self.lang[count], self.year])

                    print("\nEstreno encontrado: " + self.name[count])
                    list_torrents.append(str(torrent))
                elif(not rData[count][0] == url and not rData[count][2] == self.quality[count] and not rData[count][4] == self.year):
                    self.mdt.WriteData(cg.PATH_DATA_FOLDER + cg.FILE_NAME,[url, self.name[count], self.quality[count], self.lang[count], self.year])

                    print("\nEstreno encontrado: " + self.name[count])
                    list_torrents.append(str(torrent))
                else:
                    list_torrents.append(None)
            else:
                list_torrents.append(None)
            
            count += 1
        
        return list_torrents
    
    def UpdateMovieDownloaded(self, name, format, index):
        subprocess.call(["mv", cg.PATH_SAVE + "/" + name, cg.PATH_SAVE + "/" + self.name[index] + " (" + self.year[index] + ")." + format])
        os.chmod(cg.PATH_SAVE + "/" + self.name[index] + " (" + self.year[index] + ")." + format, 0o644)
        os.chown(cg.PATH_SAVE + "/" + self.name[index] + " (" + self.year[index] + ")." + format, 0, 0)

if __name__ == "__main__":
    urlMovies = GetDataMovies()
    print(urlMovies.GetUrlDownload())