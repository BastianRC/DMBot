from Data_Folder.config_bot import Config as cg
import os

class SaveMovieData:
    def WriteData(self, file_path, data):
        if(not os.path.exists(file_path)):
            file = open(file_path, "w")
            print("Archivo creado y editado.")
        else:
            file = open(file_path, "a")
            print("Archivo editado.")

        for i in data:
            if(i != data[len(data) - 1]):
                file.write(i + ",")
            else:
                file.write(i)

        file.write(os.linesep)
    
    def ReadData(self, file_path):
        if(os.path.exists(file_path)):
            file = open(file_path, "r")
            data = file.readlines()

            all_data = []
            for iter in data:
                all_data.append(iter.replace("\n", "").split(","))
        
        try:
            return all_data[0]
        except:
            return None


if __name__ == "__main__":
    save = SaveMovieData()
    #save.WriteData(["Nombre", "Calidad", "Idioma", "Año"])
    save.ReadData(cg.PATH_DATA_FOLDER + cg.FILE_NAME)