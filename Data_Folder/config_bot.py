class Config:
    #download_movie
    PATH_SAVE = "/home/Familia/Peliculas"
    PATH_TEMP_SAVE = "PATH_ABSOLUTE_TEMP"
    TIME_SEARCH = 3600

    #connect_qtorrent
    HOST = "IP_HOST"
    TIME_LIMIT = 120
    TRIES = 3

    #get_torrent_web
    PAGE_MOVIE = "https://www.pelitorrent.com/peliculas/estrenos/?type=movies"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    YEAR_SEARCH = 2021
    PATH_SAVE_TORRENTS = "Data_Folder/Torrents/"
    PATH_DATA_FOLDER = "Data_Folder/"