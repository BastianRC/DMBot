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
            
            count = 0

            if(url_data != []):
                for url in url_data:
                    qb = ConnectQB()

                    if(qb.Download(url, cg.PATH_SAVE)):
                        gm.UpdateMovieDownloaded(qb.nameFile, qb.nameFile[len(qb.nameFile) - 3:len(qb.nameFile)], count)
                        print("Información cambiada.")

                        count += 1
                    else:
                        count += 1
            else:
                print("\nEstrenos no actualizados.\nTiempo de espera: {} minutos.".format(int(cg.TIME_SEARCH / 60)))
                time.sleep(cg.TIME_SEARCH)

try:
    dmBot = Download_MBot()
except KeyboardInterrupt:
    print("\nBot apagado.")