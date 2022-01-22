from Data_Folder.config_bot import Config as cg
from qbittorrent import Client
import time, os

class ConnectQB:
    def __init__(self):
        self.qb = Client(cg.HOST)
        self.qb.login("admin", "adminadmin")
    
    def Download(self, torrent, pSave):
        #torrent_file = open(torrent, "rb")
        self.qb.download_from_link(torrent, save_path=pSave)

        count = 0
        first = False

        while(True):
            time.sleep(10)
            tr = self.qb.torrents()[len(self.qb.torrents()) - 1]["state"]
            self.nameFile = ""

            if(tr == "downloading" or tr == "stalledUP" or tr == "uploading"): # stalledUP -> Finalizado | pausedDL -> Empezando | downloading -> Descargando | uploading -> Subiendo

                if(not first):
                    print("Descarga iniciada...")
                    first = True
                
                if(tr == "stalledUP" or tr == "uploading"):
                    print("Descarga finalizada.")
                    self.nameFile = self.qb.torrents()[len(self.qb.torrents()) - 1]["name"]
                    
                    return True

            elif(tr != "downloading"):
                time.sleep(cg.TIME_LIMIT)
                print("Tiempo limite superado. Volviento a intentarlo.")

                if(count != cg.TRIES):
                    count += 1
                else:
                    print("Intentos superados. Error en la descarga.")
                    break