import requests
import sys
import m3u8
from colorama import Fore


file_name = 'Video 1'
file_path = './'

# Paste the url which ends with index.m3u8. After that delete the index.m3u8 from the url
url_info = ''

url_cmp = 'index.m3u8'


url_1 = url_info + url_cmp

r_1 = requests.get(url_1)

m3u8_master = m3u8.loads(r_1.text)

# Here you can investigate the m3u8_master segments
# print(m3u8_master.data['segments'][0])
file_number = 0
i = 0
percentage = 0.0
print(f'Downloading {file_name}')
print('')
for segment in m3u8_master.data['segments']:
    file_number += 1

with open(file_path + file_name + '.ts', 'wb') as f:
    for segment in m3u8_master.data['segments']:
        url = url_info + segment['uri']
        while(True):
            try:
                r = requests.get(url,timeout = 15)
            except:
                continue
            break
        f.write(r.content)
        i += 1
        percentage = i/file_number * 100
        #print(f"\033[F{url}")
        #print("")
        print(Fore.RESET + "[",end = "")
        print(Fore.GREEN + f"{(str(percentage))[0:5]} %",end = "")
        print(Fore.RESET + "]",end = "")
        print(Fore.RESET + "\r\x1b[20C[",end = "")
        print(Fore.CYAN + f"="*int(percentage/2),end = "")
        print(Fore.RESET + f"\r\x1b[71C]",end = "")
        print(Fore.RED + f"\t {i} of {file_number}",end ="")
        print(Fore.RESET + "\r",end = "")
print("")
import os
convert_line = "ffmpeg -i './" + file_name + ".ts' -c copy './" + file_name + ".mp4'"
os.system(convert_line)
delete_line = "rm -f './" + file_name + ".ts'"
os.system(delete_line)
