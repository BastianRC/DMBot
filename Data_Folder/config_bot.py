class Config:
    #download_movie
    PATH_SAVE = "/home/Familia/Peliculas"
    TIME_SEARCH = 3600

    #connect_qtorrent
    HOST = "IP_HOST"
    TIME_LIMIT = 60
    TRIES = 3

    #get_torrent_web
    PAGE_MOVIE = "https://elitetorrent.app/estrenos-23/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    YEAR_SEARCH = 2021
    AMOUNT_SEARCH = 18

    #save_torrents
    PATH_DATA_FOLDER = "Data_Folder/"
    FILE_NAME = "data_movies.txt"