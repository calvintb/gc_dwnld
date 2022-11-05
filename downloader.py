import wget, os, time
from mutagen.easyid3 import EasyID3
import mutagen
from urllib import error

def main():
    file_path = input("Where is the main directory of the information.csv and Speakers directory ?: ")
    download(file_path)

def download(file_path="./"):
    file = open(file_path + "information.csv")
    for line in file:
        line = line.rsplit(",", maxsplit=3)
        title = line[0].replace("?", "")
        title = title.replace(":", "")
        speaker = line[1]
        session = line[2]
        dwnld = line[3]
        if dwnld == "None\n":
            continue
        createDirectory(file_path + "Speakers/" + speaker)
        filePath = file_path + 'Speakers/' + speaker + '/' + title + '.mp3'
        if not os.path.isfile(filePath):
            try:
                wget.download(dwnld, filePath)
            except error.URLError:
                time.sleep(2)
                wget.download(dwnld, filePath)


            print("Downloaded " + title + " by " + speaker)
        try:
            audio = EasyID3(filePath)
        except mutagen.id3.ID3NoHeaderError:
            try:
                audio = mutagen.File(filePath, easy=True)
                audio.add_tags()
            except:
                continue
        audio["title"] = title
        audio["artist"] = speaker
        audio["album"] = session
        audio["genre"] = "General Conference"
        audio.save()


def createDirectory(path):
    if not os.path.isdir(path):
        os.mkdir(path)


if __name__ == "__main__":
    main()
