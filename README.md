# Python-Video_Downloader-m3u8
This programs downloads videos which is encoded with m3u8 format.


### Install the requirements:
- If you're using a virtual environment or windows: 
```bash
$ pip install -r requirements.txt
``` 
- If you're not using virtual environment and you're using linux and did not specify any alias for pip 
```bash
$ pip3 install -r requirements.txt
```
---------------------------------------

- Find the url of the video from your web browser (by inspecting element). 
- The url must end with index.m3u8 
- After the paste it to the url_info variable and delete the 'index.m3u8' part. 
- Write the name of the file without format. Do not write 'Video1.mp4'. Instead of this you should write 'Video1' 

- You can adjust the path. 
- At the end it uses ffmpeg so make sure you installed ffmpeg 
- In linux you can do it by typing: 
```bash
$ sudo apt install ffmpeg -y
# And run the program by typing:
# (Virtual environment and windows)
$ python Video_Downloader.py
``` 
or 
```bash
$ python3 Video_Downloader.py
``` 
- The [youtube video](https://youtu.be/kMX8wW0rdkY) which I made for this:
https://youtu.be/kMX8wW0rdkY



