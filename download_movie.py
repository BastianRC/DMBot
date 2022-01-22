from unicodedata import name
from connect_qtorrent import ConnectQB
from get_torrent_web import GetDataMovies
from Data_Folder.config_bot import Config as cg
import time, asyncio

class Download_MBot:
    def __init__(self):
        while(True):
            gm = GetDataMovies()
            url_data = gm.GetUrlDownload()
            
            for url in url_data:
                if(url != None):
                    qb = ConnectQB()

                    if(qb.Download(url, cg.PATH_SAVE)):
                        gm.UpdateMovieDownloaded(qb.nameFile, qb.nameFile[len(qb.nameFile) - 3:len(qb.nameFile)])
                        print("Información cambiada.")
                else:
                    print("Estrenos no actualizados.")
                    time.sleep(cg.TIME_SEARCH)

try:
    dmBot = Download_MBot()
except KeyboardInterrupt:
    print("Bot apagado.")