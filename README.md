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
  
`scrapy crawl tomholland --logfile scraper.log`  

This command can be somewhat modified to suit your needs and documentation to do so is available on the [Scrapy docs](https://docs.scrapy.org/en/latest/index.html). By default, the project will output to a file named samara.jl, located in the first netscrape_nav folder.

## Modification

### Page Selection
  
As a default, the program scrapes any page that contains Software or Mode* in the URL. To change the pages scraped, you must first create a Link Extractor rule (in iGEMScraper.py) to parse the URL for certain keywords. Certain pages are standardized amongst iGEM teams and thus, are simpler to create rules for. Regular Expressions may be used to create wildcard rules to help increase the scope of the scraper for more inconsistant page namings (see rule #2 and the [RegularExpressions documentation](https://docs.python.org/3/library/re.html) for more information and examples of their usage). 

### Item Processing
  
Item processing begins in the items.py file, with the defining of a WikiPage Item object. An Item object is a dictionary-like object that allows for information to remain organized and catagorized. The existing WikiPage Item *should* be sufficent for scraping iGEM wiki pages, but if necessary, it can be easily modified to accept different parameters.

The second step involves post processing in the pipelines.py file. While some preliminary processing is done before creating a WikiPage Item (in iGEMScraper.py), we further process it here to remove unwanted characteristics from the scraped text. This step is easily expanded on, with additional processing steps being a few lines of code away.
  
This step also includes the removal of default or unpopulated wiki pages, pages that do not follow standard iGEM convention, and other broken or otherwise unusable pages. 

### Exporting
  
Exporting is also done through the pipelines.py file. By default, the scraper will use the JsonLinesItemExporter provided by Scrapy. This will export the pages as a .jl file. If changing the export format is desired or if the existing functionality is simply not enough, one may use the Scrapy [Item Exporters](https://docs.scrapy.org/en/latest/topics/exporters.html) and the [Item Pipeline](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) docs to customize the functionality of the exporter.