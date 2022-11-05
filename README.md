# gc_dwnld
A General Conference Downloader and Scraper complete with a csv file containing information on the talks

## scraper.py
  takes a filepath, language, start_year, and end_year and exports the information to the csv file
  
## information.csv
  a csv file that follows this format
  `<title>,<speaker>,<month_year><download_link>`

## downloader.py
  takes in a filepath to the csv file, and downloads the talk.mp3 in a directory called Speakers following this convention:
  
 ` Speakers
     └───speaker_name1
      |          └───talk1
      |          └───talk2
      |
      └─── speaker_name2
      |          └───talk1`
      
## driver.py
  this connects scraper.py and downloader.py to do it all in one program
  

Recommended Usage, I would recommend just using the csv file and the downloader.py file. You can remove entries from the csv file to not download them.
