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

        for i in range(cg.AMOUNT_SEARCH):
            lg = str(data[i].find("div", attrs={"class":"imagen"}).find("span", attrs={"id":"idiomacio"}).find("img")["title"])
            qt = data[i].find("div", attrs={"class":"imagen"}).find("span", attrs={"style":"right: 0px;left: auto;max-width: 60%;"}).i.get_text()

            if(lg.endswith("VOSE") or lg.endswith("Castellano") and qt == "HDTV" or qt == "DVDrip"):
                self.name.append(str(data[i].find("div", attrs={"class":"meta"}).get_text()).replace("\n", ""))
                self.lang.append(lg)
                self.quality.append(qt)

                self.final_data.append(data[i].find("div", attrs={"class":"meta"}).a.get("href"))

        return self.final_data
    
    def GetUrlDownload(self):
        url_info = self.GetUrlInfo()
        list_torrents = []

        countTwo = 0
        self.countThree = 0

        self.rData = self.mdt.ReadData(cg.PATH_DATA_FOLDER + cg.FILE_NAME)
        self.year = []      

        for url, count in zip(url_info, range(len(url_info))):
            r = requests.get(url, cg.HEADERS)

            soup = bs(r.text, 'lxml')

            self.year.append(soup.find("p", attrs={"class":"descrip"}).find("span").get_text().replace("Fecha: ", "").split("-")[0])
            torrent = soup.find("div", attrs={"class":"enlace_descarga"}).find_all("a", attrs={"class":"enlace_torrent degradado1"})[1].get('href')

            if(int(self.year[count]) >= cg.YEAR_SEARCH):       
                if(self.rData is None or not self.rData):
                    print("\nEstreno encontrado: " + self.name[count])

                    self.mdt.WriteData(cg.PATH_DATA_FOLDER + cg.FILE_NAME,[url, self.name[count], self.quality[count], self.lang[count], self.year[count]])
                    list_torrents.append(str(torrent))
                
                elif(not self.rData[countTwo][0] == url and not self.rData[countTwo][1] == self.name[count]):
                    print("\nEstreno encontrado: " + self.name[count])

                    self.mdt.WriteData(cg.PATH_DATA_FOLDER + cg.FILE_NAME,[url, self.name[count], self.quality[count], self.lang[count], self.year[count]])
                    list_torrents.append(str(torrent))

                    self.countThree += 1
                else:
                    pass
            else:
                pass
            
            try:
                if((len(self.rData) - 1) == countTwo):
                    countTwo = (len(self.rData) - 1)
                else:
                    countTwo += 1
            except:
                pass
        
        return list_torrents
    
    def UpdateMovieDownloaded(self, name, format, index):
        try:
            index += len(self.rData)
        except:
            pass

        subprocess.call(["mv", cg.PATH_SAVE + "/" + name, cg.PATH_SAVE + "/" + self.name[index] + " (" + self.year[index] + ")." + format])
        os.chmod(cg.PATH_SAVE + "/" + self.name[index] + " (" + self.year[index] + ")." + format, 0o644)
        #os.chown(cg.PATH_SAVE + "/" + self.name[index] + " (" + self.year[index] + ")." + format, 0, 0)

if __name__ == "__main__":
    urlMovies = GetDataMovies()
    print(urlMovies.GetUrlDownload())