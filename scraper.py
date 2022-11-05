import os, requests
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
X_PATH_FIRST_BUTTON = '/html/body/div[1]/div[2]/div/main/div/div[2]/header/div[2]/button[3]'
X_PATH_SECOND_BUTTON = '/html/body/div[1]/div[2]/div/main/div/div[2]/aside/div/div[3]/label/div/span/button'
X_PATH_DOWNLOAD_BUTTON = '/html/body/div[1]/div[2]/div/main/div/div[2]/aside/div/a'
PATH = input("Where do you want your files saved to?: ")
CONF_URL = "https://www.churchofjesuschrist.org"
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)


def createDirectory(path):
    if not os.path.isdir(path):
        os.mkdir(path)

# def createFile(path):
#     if not os.path.isfile(path):
#         os.mkfifo(path)


# def downloadTalk(link, speaker="Unknown", title="Unknown"):
#     if type(link) != type(None):
#         filePath = PATH + 'Speakers/' + speaker + '/' + title + '.mp3'
#         createDirectory(PATH + 'Speakers/' + speaker)
#         if not os.path.isfile(filePath):
#             print("\nDownloaded " + title + " by " + speaker)
#         else:
#             print("You already downloaded " + title + " by " + speaker)
#     else:
#         print("Oh no! We couldn't find a download link for " + title + " by " + speaker)


def generateLinks(end, start, lang="eng", file=open("./information.csv")):
    for year in range(start, end + 1):
        print(f"Starting to print the year {year}")
        (generateTalkLinks(generateSessionLinks(year, '04', lang), year, '04', file))
        (generateTalkLinks(generateSessionLinks(year, '10', lang), year, '10', file))

def generateSessionLinks(year='2012', month="04", lang='eng'):
    return CONF_URL + '/study/general-conference/' + str(year) + "/" + month + "?lang=" + lang


def generateTalkLinks(sessionurl, year, month, file):
    html_text = requests.get(sessionurl).content.decode("utf8")
    soup = BeautifulSoup(html_text, 'html.parser')
    for i, link in enumerate(soup.find_all('a', attrs={"class": "item-U_5Ca"})):
        talk = link.get('href')
        talk = CONF_URL + talk
        if scrapeGoodOnes(talk, year, month):
            driver.get(talk)
            title = (grabTitle(link))
            speaker = (grabSpeaker(link))
            session = (grabSession(year, month))
            downloadLink = grabDownloadLink(talk)
            print(title, speaker, session, downloadLink, sep=",", file=sys.stderr)
            print(title, speaker, session, downloadLink, sep=",", file=file)


def scrapeGoodOnes(str1, year, month):
    year = str(year)
    month = str(month)
    if "session" not in str1:
        if year in str1:
            if str1 != CONF_URL + '/study/general-conference/' + year + '/' + month + '?lang=eng':
                return True
    return False


def grabDownloadLink(url):

    try:
        element = driver.find_element('xpath', X_PATH_FIRST_BUTTON)
        element.click()
        element1 = driver.find_element('xpath', X_PATH_SECOND_BUTTON)
        element1.click()
        element2 = driver.find_element('xpath', X_PATH_DOWNLOAD_BUTTON)
        link = element2.get_attribute('href')
        return link
    except:
        return None


def grabSession(year, month):
    if month == '04':
        return "April " + str(year)
    return "October " + str(year)


def grabSpeaker(link):
    speaker = link.find_next("p")
    speaker = speaker.find_next("p")
    if type(speaker) == type(None):
        return "Unknown"
    return speaker.string


def grabTitle(link):
    # title = link.p.string
    # if type(title) == type(None):
    #     return "Unknown"
    # return title
    return driver.title


def main(end, start, lang, new_file):
    generateLinks(end, start, lang, new_file)
    driver.quit()


if __name__ == "__main__":
    new_file = open(PATH + "information.csv", "a")
    createDirectory(PATH + 'Conferences')
    createDirectory(PATH + 'Speakers')
    lang = str(input("Download Language: "))
    start = int(input("Start Year: "))
    end = int(input("End Year: "))
    main(end, start, lang, new_file)


