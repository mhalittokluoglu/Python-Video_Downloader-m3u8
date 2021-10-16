import requests
import sys
import m3u8
from colorama import Fore


fileName = '' # Enter the File Name
filePath = './' # Enter the path

# NOTE: This not the program in the youtube video.
fileCount = 0
with open(filePath + 'url_info.txt', 'r') as urlFile:
    lines = urlFile.readlines()
    for eachLine in lines:
        eachLine = eachLine[0:-1]
        if eachLine[0:3] == "htt":
            fileCount += 1

count = 0
with open(filePath + fileName + '.ts', 'wb') as f:
    for eachLine in lines:
        eachLine = eachLine[0:-1]
        if eachLine[0:3] == "htt":
            while(True):
                try:
                    r = requests.get(eachLine, timeout = 15)
                except:
                    continue
                break
            f.write(r.content)
            count += 1
            percentage = count/fileCount * 100
            print(Fore.GREEN + f"[{(str(percentage))[0:5]} %] ",end = "")
            print(Fore.RED + f"{count} of {fileCount} : ",end="")
            print(Fore.RESET + f"{eachLine}")


print("")
import os
convert_line = "ffmpeg -i '" + filePath + fileName + ".ts' -c copy '" + filePath + fileName + ".mp4'"
os.system(convert_line)
delete_line = "rm -f '" + filePath + fileName + ".ts'"
# print(delete_line)
os.system(delete_line)
