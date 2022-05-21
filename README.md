# SAMARA iGEM Research Assistant
## iGEMScraper

A web scraper created using python and scrapy in order to automatically visit, parse, and extract information from iGEM wiki pages. The scraper
was designed as the first component of the larger SAMARA Research Assistant project. However, in order to keep it accessible to other teams, it
has also been released as a standalone module, allowing other teams to  easily scrape iGEM wiki pages using their own parameters.

### Installation

1. Download the files from the repository
2. Create a virtual environment and run the following command from inside the virtual environment to install the required packages:  
`pip install -r requirements.txt`  
  
A brief overview of the packages installed and their usage in the progream are listed below:

| Library/Module | Usage |
| -------------- | ----- |
| Scrapy | Creates the CrawlSpider used to parse and scrape iGEM wiki pages. |
| RegEx | Allows for string processing and the usage of wildcard text patterns. |
| lxml | Allows for HTML processing and cleaning to help sanitize scraping outcomes. |
| parsel | Adds CSS selectors to extract text from the html page body. |

## Usage

The program is run through the terminal. In order to do so, we must first navigate to the first netscrape_nav folder. If inside the project folder, the command to do so is as follows:
  
`cd ./netscrape_nav`  
  
We can then run the scraper itself using the following command:  
  
`scrapy crawl tomholland -O samara.csv --logfile scraper.log`  

This command can be modified to suit your needs and documentation to do so is available on the [Scrapy docs](https://docs.scrapy.org/en/latest/index.html). By default, the program is set to overwrite the samara.csv file. Supported filetypes and storage options can also be found in the Scrapy documentation. CSV files, while smaller in size than the alternatives, do come with some issues. Namely, the presence of commas in the extracted text annoys CSV editing software. However, slight post-processing should be sufficient to overcome these obstacles.

## Modification
  
As a default, the program scrapes any page that contains Software or Mode* in the URL. To change the pages scraped, you must first create a Link Extractor rule to parse the URL for certain keywords. Certain pages are standardized amongst iGEM teams and thus, are simpler to create rules for. Regular Expressions may be used to create wildcard rules to help increase the scope of the scraper for more inconsistant page namings(see rule #2 and the [RegularExpressions documentation](https://docs.python.org/3/library/re.html) for more information and examples of their usage). 


