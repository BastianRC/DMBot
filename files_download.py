from sys import stdout
from Data_Folder.config_bot import Config as cg
import os, subprocess, shutil

class FilesDownloaded: 
    def GetFile(self):
        self.dir = os.listdir(cg.PATH_TEMP_SAVE)[0]
        list_files = os.listdir(cg.PATH_TEMP_SAVE + "/" + str(self.dir))
        self.extractOn = False

        if(len(list_files) > 1):
            file_allow = ""

            for files in list_files:
                if(files.endswith("part1.zip") or files.endswith("part1.rar")):
                    file_allow = files
                    self.extractOn = True

                    return file_allow
                    
                elif(files.endswith(".mkv") or files.endswith(".mp4") or files.endswith(".avi")):
                    return files
        else:
            return list_files[0]
    
    def ExtractMovie(self, name, year):
        try:
            file = self.GetFile()

            if(self.extractOn):
                try:
                    print("Extrayendo datos...")
                    subprocess.call(['unrar', 'x', '-kb', cg.PATH_TEMP_SAVE + "/" + str(self.dir) + "/" + file, 
                    cg.PATH_TEMP_SAVE + "/" + str(os.listdir(cg.PATH_TEMP_SAVE)[0])], 
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                except:
                    print("Error al extraer la pelicula")

            self.UpdateMovieDownloaded(name, year)
            self.DeleteFilesNotUtils()

        except:
            pass
    
    def UpdateMovieDownloaded(self, new_name, year):
        list_files = os.listdir(cg.PATH_TEMP_SAVE + "/" + str(os.listdir(cg.PATH_TEMP_SAVE)[0]))

        self.nFileName = ""
        for file in list_files:
            if(file.endswith(".mkv") or file.endswith(".mp4") or file.endswith(".avi")):
                path_nFileName = "{}/{} ({}){}".format(cg.PATH_SAVE, new_name, year, os.path.splitext(file)[1])
                self.nFileName = "{} ({}){}".format(new_name, year, os.path.splitext(file)[1])

                os.rename(cg.PATH_TEMP_SAVE + "/" + str(os.listdir(cg.PATH_TEMP_SAVE)[0]) + "/" + file, path_nFileName)
                os.chmod(path_nFileName, 0o644)
                #os.chown(path_nFileName, 0, 0)

    def DeleteFilesNotUtils(self):
        try:
            shutil.rmtree(cg.PATH_TEMP_SAVE + "/" + str(os.listdir(cg.PATH_TEMP_SAVE)[0]))
        except:
            print("Error al eliminar la carpeta")

if __name__ == "__main__": 
    urlMovies = FilesDownloaded()
    urlMovies.ExtractMovie("Prueba2", 2021)