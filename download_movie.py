from unicodedata import name
from connect_qtorrent import ConnectQB
from get_torrent_web import GetDataMovies
from Data_Folder.config_bot import Config as cg
import time

class Download_MBot:
    def __init__(self):
        while(True):
            gm = GetDataMovies()
            url = gm.GetUrlDownload() # Aqui se comprobara cada x tiempo si hay una pelicula nueva en la posicion 0. Si la hay, se pasa a descargar, si no, sigue esperando.
            
            if(url != None):
                qb = ConnectQB()
                if(qb.Download(url, cg.PATH_SAVE)):
                    gm.UpdateMovieDownloaded(qb.nameFile, qb.nameFile[len(qb.nameFile) - 3:len(qb.nameFile)])
                    print("Información cambiada")
            else:
                print("Estrenos no actualizados.")
                time.sleep(cg.TIME_SEARCH)

dmBot = Download_MBot()