import datetime
from Data_Folder.config_bot import Config as cg
from qbittorrent import Client
import time, sys

class ConnectQB:
    def __init__(self):
        self.qb = Client(cg.HOST)
        self.qb.login("admin", "adminadmin")
    
    def Download(self, torrent, pSave):
        torrent_file = open(torrent, "rb")
        self.qb.download_from_file(torrent_file, save_path=pSave)

        count = 0
        seg = 0
        first = False

        while(True):
            time.sleep(1)
            seg += 1

            try:
                tr = self.qb.torrents()[0]
            except:
                pass

            progress = int(float("{:.2f}".format(tr["progress"])) * 100)
            state = tr["state"]
            self.nameFile = tr["name"]

            if(progress != 101):    
                if(not first):
                    print("\nDescarga iniciada...")
                    first = True

                #char = "=" * progress + "-" * (100 - progress)
                
                #print("\r{}: [{}] {}{}".format(self.nameFile, char, progress, ("%")), end="", flush=True)

                #Only Python 2.x
                #sys.stdout.write("\r%s: [%s] %s%s" % (self.nameFile, char, progress, "%"))
                #sys.stdout.flush()

                if(progress == 100):
                    print("\nDescarga finalizada.\nNombre: " + self.nameFile + "\nFecha: " + str(datetime.datetime.now()))
                    self.qb.delete(tr["hash"])

                    return True
                elif(seg >= cg.TIME_LIMIT and progress == 0):
                    print("\nTiempo de inicio de descarga superado.\nNombre: " + self.nameFile + "\nFecha: " + str(datetime.datetime.now()))
                    self.qb.delete(tr["hash"])
                    return False

            elif(state != "downloading"):
                time.sleep(cg.TIME_LIMIT)
                print("Tiempo limite superado. Volviento a intentarlo.")

                if(count != cg.TRIES):
                    count += 1
                else:
                    print("Intentos superados. Error en la descarga.")
                    break