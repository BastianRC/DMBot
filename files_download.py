from sys import stdout
from Data_Folder.config_bot import Config as cg
import os, subprocess, sys

class FilesDownloaded: 
    def GetFile(self):
        self.dir = os.listdir(cg.PATH_TEMP_SAVE)[0]
        list_files = os.listdir(cg.PATH_TEMP_SAVE + "/" + str(self.dir))
        self.filename = ""

        if(len(list_files) > 1):
            file_allow = ""

            for files in list_files:
                if(files.endswith("part1.zip") or files.endswith("part1.rar")):
                    file_allow = files
                    return file_allow
                    
                elif(files.endswith(".mkv") or files.endswith(".mp4") or files.endswith(".avi")):
                    os.rename(cg.PATH_TEMP_SAVE + "/" + str(self.dir) + "/" + files, cg.PATH_SAVE + "/" + files)
                    self.filename = files

                    return None
        else:
            os.rename(cg.PATH_TEMP_SAVE + "/" + str(self.dir) + "/" + list_files[0], cg.PATH_SAVE + "/" + list_files[0])
            self.filename = list_files[0]

            return None
    
    def ExtractMovie(self):
        try:
            file = self.GetFile()

            if(file is not None):
                try:
                    list_old_files = os.listdir(cg.PATH_SAVE)

                    print("Extrayendo datos...")
                    subprocess.call(['unrar', 'x', '-kb', cg.PATH_TEMP_SAVE + "/" + str(self.dir) + "/" + file, cg.PATH_SAVE], 
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    list_new_files = os.listdir(cg.PATH_SAVE)

                    if(len(list_new_files) > 1):
                        for nm_New in list_new_files:
                            for nm_Old in list_old_files:
                                if(nm_New != nm_Old):
                                    self.filename = nm_New
                    else:
                        self.filename = list_new_files[0]
                    
                except:
                    print("Error al extraer la pelicula")

            self.DeleteFilesNotUtils()

        except:
            pass

    def DeleteFilesNotUtils(self):
        try:
            subprocess.call(['rm', '-r', cg.PATH_TEMP_SAVE + "/" + str(self.dir)], stdout=subprocess.DEVNULL)
        except:
            print("Error al eliminar la carpeta")

if __name__ == "__main__": 
    urlMovies = FilesDownloaded()
    urlMovies.ExtractMovie()