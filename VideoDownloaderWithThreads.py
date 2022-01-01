import threading
import requests
import m3u8


class UrlParser:
    def __init__(self, threadCount, m3u8_master, urlInfo, fileNumber):
        self.__partNumber = threadCount
        tempUrlList = []
        self.listOfUrlLists = []
        partConstant = int(fileNumber / self.__partNumber)
        print(f'Total Number Of Files: {fileNumber}')
        for i in range(0, self.__partNumber):
            lowerLimit = i * partConstant + 1
            if i == self.__partNumber - 1:
                upperLimit = fileNumber
            else:
                upperLimit = (i+1) * partConstant + 1
            for j in range(lowerLimit, upperLimit):
                url = urlInfo + m3u8_master.data['segments'][j]['uri']
                tempUrlList.append(url)
            tempList = tempUrlList.copy()
            self.listOfUrlLists.append(tempList)
            tempUrlList.clear()


class DisplayPercentage:
    def __init__(self, partCount):
        self.__partCount = partCount
        self.percentageList = []
        self.__displayFlag = True
        self.endFlag = False
        for i in range(0, self.__partCount):
            percentage = 0.0
            self.percentageList.append(percentage)

    def UpdatePercentage(self, percentage, partNumber):
        self.percentageList[partNumber] = percentage
        self.__displayFlag = True

    def UpdateDisplay(self):
        while (self.endFlag == False):
            if self.__displayFlag == True:
                print('\r', end = '')
                overall = 0
                for i in range(0, self.__partCount):
                    overall += self.percentageList[i]
                    # print(f'Part{i}:{str(self.percentageList[i])[0:6]}%   ', end = '')
                overall /= self.__partCount
                print(f'Downloading:{str(overall)[0:6]}%',end = '')
                self.__displayFlag = False



class PartDownloader:
    def __init__(self, urlList, fileName, number, percentageMutex, displayPercentage):
        self.__fileName = fileName
        self.__fileNumber = number
        self.__urlList = urlList
        self.percentage = 0
        self.__prevPercent = 0
        self.percentageMutex = percentageMutex
        self.__displayPercentage = displayPercentage

    def StartDownloading(self):
        with open(self.__fileName + '.ts', 'wb') as f:
            i = 0
            for url in self.__urlList:
                while (True):
                    try:
                        r = requests.get(url, timeout=15)
                    except:
                        continue
                    break
                f.write(r.content)
                i += 1
                self.percentage = i / len(self.__urlList) * 100
                self.__prevPercent = self.percentage
                self.percentageMutex.acquire()
                self.__displayPercentage.UpdatePercentage(
                    self.percentage, self.__fileNumber)
                self.percentageMutex.release()

# _______________________ MODIFY HERE ____________________________________

fileName = 'VideoName'
threadCount = 5 # 32 can be written if your system is good
threadCount -= 1 # 1 for display
urlInfo = ''
urlCompletion = 'index.m3u8'

# ________________________________________________________________________

masterUrl = urlInfo + urlCompletion
r_1 = requests.get(masterUrl)
m3u8_master = m3u8.loads(r_1.text)
# print(m3u8_master.data['segments'][0]['uri'])
fileNumber = 0
for segment in m3u8_master.data['segments']:
    fileNumber += 1

urlParser = UrlParser(threadCount, m3u8_master, urlInfo, fileNumber)

displayMutex = threading.Lock()
displayMutex.acquire()
displayPercentage = DisplayPercentage(threadCount)
displayMutex.release()
partDownloaderList = []
partDownloaderThreadsList = []
fileNameList = []
for i in range(0, threadCount):
    fileNameWithPartCount = 'temp/' + fileName + '_Part' + str(i)
    fileNameList.append(fileNameWithPartCount)
    partDownloader = PartDownloader(urlParser.listOfUrlLists[i],
                                    fileNameWithPartCount, i, displayMutex, displayPercentage)
    partDownloaderThread = threading.Thread(
        target=partDownloader.StartDownloading)
    partDownloaderList.append(partDownloader)
    partDownloaderThreadsList.append(partDownloaderThread)


displayThread = threading.Thread(target = displayPercentage.UpdateDisplay)
displayThread.start()


import os
if not os.path.exists('./temp'):
    os.mkdir('temp')


for i in range(0, threadCount):
    partDownloaderThreadsList[i].start()


for i in range(0, threadCount):
    partDownloaderThreadsList[i].join()

displayPercentage.endFlag = True


with open(fileName + '.ts', 'wb') as f:
    for eachFileName in fileNameList:
        with open(eachFileName + '.ts', 'rb') as eachTsFile:
            fileContent = eachTsFile.read()
            f.write(fileContent)


convert_line = 'ffmpeg -i "./' + fileName + '.ts" -c copy -strict -2 -bsf:a aac_adtstoasc "./' + fileName + '.mp4"'
print(convert_line)
invalidFlag = False
try:
    os.system(convert_line)
except:
    invalidFlag = True


if invalidFlag == False:
    import shutil
    shutil.rmtree('temp')
    os.remove(fileName + '.ts')