import scraper, downloader
from scraper import createDirectory, PATH

if __name__ == "__main__":
    file_path = input("Where is the main directory of the information.csv and Speakers directory ?: ")
    new_file = open(PATH + "information.csv", "a")
    createDirectory(PATH + 'Conferences')
    createDirectory(PATH + 'Speakers')
    lang = str(input("Download Language: "))
    start = int(input("Start Year: "))
    end = int(input("End Year: "))
    scraper.main(end, start, lang, new_file)
    downloader.download(file_path)
