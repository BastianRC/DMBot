from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from Data_Folder.config_bot import Config as cg
import requests, os, subprocess

class GetDataMovies:
    def __init__(self):
        r = requests.get(cg.PAGE_MOVIE, cg.HEADERS)
        self.soup = bs(r.text, 'lxml')

        if(r.status_code == 200):
            print("\nLa web se ha cargado correctamente.")
        else:
            print("Error al cargar la web: " + r.status_code)
    
    def GetUrlMovie(self):
        data = self.soup.find_all("ul", attrs={"class":"post-lst rw sm rcl2 rcl3a rcl4b rcl3c rcl4d rcl6e"})[0].find_all("li")

        self.name = []
        self.year = []
        self.quality = []
        self.lang = []
        self.url_info = []

        for info in data:
            yr = int(info.find("span", attrs={"class":"year"}).get_text())
            qt = info.find("span", attrs={"class":"Qlty"}).get_text()
            lg = info.find("span", attrs={"class":"lang"}).find("img")["src"]

            if(lg == "https://www.pelitorrent.com/wp-content/uploads/2017/06/spanish.png"):
                lg = "Español"
            
            if(yr >= cg.YEAR_SEARCH):
                if(str(lg) == "Español" and qt == "MicroHD" or qt == "BluRayRip"):
                    self.name.append(info.h2.get_text())
                    self.year.append(yr)
                    self.quality.append(qt)
                    self.lang.append(lg)
                    self.url_info.append(info.a["href"])

        return self.url_info

    def GetUrlDownload(self):
        url_info_final = self.GetUrlMovie()
        chromeOptions = Options()
        chromeOptions.headless = True
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        
        os.chmod(cg.PATH_DATA_FOLDER + "chromedriver", 0o755)
        
        driver = webdriver.Chrome(executable_path=r"{}{}".format(cg.PATH_DATA_FOLDER, "chromedriver"), options=chromeOptions)

        url_download = []
        for url in url_info_final:
            driver.get(url)

            container = driver.find_element_by_id("mdl-download")
            driver.execute_script("arguments[0].style.display = 'block';", container)

            quality = driver.find_elements_by_xpath("/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr/td[3]/span")
            torrent = driver.find_elements_by_xpath("/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr/td[4]/a")

            findFndQT = ""
            findSndQT = ""
            findTndQT = ""
            for qt, count in zip(quality, range(len(torrent))):
                if(qt.text == "BDremux" or qt.text == "4K UHDrip"):
                    findFndQT = torrent[count].get_attribute("href")
                    break
                elif(qt.text == "Bluray Microhd"):
                    findSndQT = torrent[count].get_attribute("href")

                elif (qt.text == "MicroHD"):
                    findTndQT = torrent[count].get_attribute("href")

            if(findFndQT != ""):
                url_download.append(findFndQT)
            elif(findSndQT != ""):
                url_download.append(findSndQT)
            else:
                url_download.append(findTndQT)
        
        return url_download
    
    def GetTorrents(self):
        urls_down = self.GetUrlDownload()
        self.nameGTorrent = []
        self.yearGTorrent = []

        list_torrents = []
        for url, count in zip(urls_down, range(len(urls_down))):
            if(not os.path.exists("{}.torrent".format(cg.PATH_SAVE_TORRENTS + str(self.name[count])))):
                r = requests.get(url, cg.HEADERS)
                open("{}.torrent".format(cg.PATH_SAVE_TORRENTS + str(self.name[count])), "wb").write(r.content)

                list_torrents.append("{}.torrent".format(cg.PATH_SAVE_TORRENTS + str(self.name[count])))
                self.nameGTorrent.append(str(self.name[count]))
                self.yearGTorrent.append(str(self.year[count]))

                print("\nEstreno encontrado: " + str(self.name[count]))

        return list_torrents

    def UpdateMovieDownloaded(self, name, format, index):
        try:
            index += len(self.rData)
        except:
            pass

        subprocess.call(["mv", cg.PATH_SAVE + "/" + name, cg.PATH_SAVE + "/" + self.nameGTorrent[index] + " (" + str(self.yearGTorrent[index]) + ")." + format])
        #os.rename(cg.PATH_SAVE + "/" + name, cg.PATH_SAVE + "/" + self.nameGTorrent[index] + " (" + str(self.yearGTorrent[index]) + ")." + format)
        os.chmod(cg.PATH_SAVE + "/" + self.nameGTorrent[index] + " (" + str(self.yearGTorrent[index]) + ")." + format, 0o644)
        os.chown(cg.PATH_SAVE + "/" + self.nameGTorrent[index] + " (" + str(self.yearGTorrent[index]) + ")." + format, 0, 0)

if __name__ == "__main__": 
    urlMovies = GetDataMovies()
    print(urlMovies.GetTorrents())