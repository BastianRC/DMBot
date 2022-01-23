import datetime
from Data_Folder.config_bot import Config as cg
from qbittorrent import Client
import time, sys

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
            time.sleep(1)
            
            try:
                tr = self.qb.torrents()[len(self.qb.torrents()) - 1]
            except:
                pass

            progress = int(float("{:.2f}".format(tr["progress"])) * 100)
            state = tr["state"]
            self.nameFile = tr["name"]

            #if(state == "downloading" or state == "stalledUP" or state == "uploading"): # stalledUP -> Finalizado | pausedDL -> Empezando | downloading -> Descargando | uploading -> Subiendo
            if(progress != 101):    
                if(not first):
                    print("\nDescarga iniciada...")
                    first = True

                #char = "=" * progress + "-" * (100 - progress)
                
                #print("\r{}: [{}] {}{}".format(self.nameFile, char, progress, ("%")), end="", flush=True)

                #Only Python 2.x
                #sys.stdout.write("\r%s: [%s] %s%s" % (self.nameFile, char, progress, "%"))
                #sys.stdout.flush()

                #if(state == "stalledUP" or state == "uploading"):
                if(progress == 100):
                    print("\nDescarga finalizada.\nNombre: " + self.nameFile + "\nFecha: " + str(datetime.datetime.now()))
                    return True

            elif(state != "downloading"):
                time.sleep(cg.TIME_LIMIT)
                print("Tiempo limite superado. Volviento a intentarlo.")

                if(count != cg.TRIES):
                    count += 1
                else:
                    print("Intentos superados. Error en la descarga.")
                    break