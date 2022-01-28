# DMBot v2.0
Install Requirements

* beautifulsoup4==4.10.0
* bs4==0.0.1
* certifi==2021.10.8
* charset-normalizer==2.0.10
* env==0.1.0
* idna==3.3
* lxml==4.7.1
* python-qbittorrent==0.3.1
* requests==2.27.1
* soupsieve==2.3.1
* urllib3==1.26.8
* selenium==3.141.0

Google Chrome Install | Selenium | Linux

* wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
* sudo dpkg -i google-chrome-stable_current_amd64.deb

Create Torrents and Temp Folder

* sudo mkdir /path/DMBot/Data_Folder/Torrents
* sudo mkdir /path/DMBot/Data_Folder/Temp

Edit Config File

* sudo nano /path/DMBot/Data_Folder/config_bot.py
* PATH_TEMP_SAVE = "/path/DMBot/Data_Folder/Temp"
* HOST = "IP_HOST_QB"

Run Bot

* Create a new screen with screen command
* python3 download_movie.py
