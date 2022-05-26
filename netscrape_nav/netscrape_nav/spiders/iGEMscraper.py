'''
SAMARA iGEM Research Assistant
iGEMScraper.py

A web scraper created using python and scrapy in order to automatically visit, parse, and extract 
information from iGEM wiki pages. In order to run, run the following commands from the terminal while
the terminal directory points to the project directory:

cd ./netscrape_nav

scrapy crawl tomholland --logfile scraper.log

Created by Ahmed Almousawi for the 2022 iGEM Calgary Team
For inquiries or questions, email igemcalgary@ucalgary.ca or ahmed.almousawi1@ucalgary.ca

Requried Packages:
scrapy
re
lxml
parsel
'''

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import re
from lxml import html
from lxml.html.clean import Cleaner
from parsel import Selector
from netscrape_nav.items import WikiPage


def getTeamname(url):
    '''
    Extracts the Team name from the url of an iGEM wiki page
    
    Arguments:
        url (str): the url of a wiki page

    Returns:
        teamname (str): the name of the team that created the page
    '''
    
    teamname = re.search('Team:(.+?)/', url).group()    # Extracts the teamname from the url
    teamname = teamname.replace('Team:', '')    # Cleans the fluff from the extracted name
    teamname = teamname.replace('/', '')        # Remove the / at the end
    teamname = teamname.replace('_', ' ')       # Replace '_' with a ' '

    return teamname

def getYear(url):
    '''
    Extracts the year from the url of an iGEM wiki page
    
    Arguments:
        url (str): the url of a wiki page

    Returns:
        year (str): the year of competition for the team 
    '''
    
    year = re.search('//(.+?).igem', url).group()   # Extracts the year from the URL
    year = year.replace('//', '')                   # Removes the '//'
    year = year.replace('.igem', '')                # Removes the '.igem'

    return year

def cleanHTML(page_html):
    '''
    Processes and cleans the HTML from the scraped page, removing any Javascript, style, or scripts
    
    Arguments:
        page_html (str): the full HTML content of the scraped page

    Returns:
        clean_page (str): the processed version of the page with JS, style, and scripts removed 
    '''
    
    page = html.fromstring(page_html)   # Turns the HTML string into an lxml HTML Element in order to use the Cleaner object

    cleaner = Cleaner(style=True, javascript=True, scripts=True)   # Creates an lxml Cleaner class to remove JS, styles, and scripts

    clean_page = cleaner.clean_html(page)   # Cleans the page according to the parameters above

    tags_to_remove = ['nav', 'footer', 'header', 'h1', 'h2', 'h3', 'ul', 'li', 'table']
    for tag in tags_to_remove:  # Adapted from https://stackoverflow.com/a/63386884
        for node in clean_page.xpath(f'.//{tag}'):
            node.getparent().remove(node)

    clean_page = html.tostring(clean_page, encoding='UTF-8').decode()    # Converts it back into a string in order to use it later on

    return clean_page
    
def getPagetext(clean_page):
    '''
    Gets the text content from the body of a wiki page and cleans it from
    newlines, tabs, and excessive whitespace

    Arguments:
        clean_page (str): the processed HTML version of the page (see cleanHTML)

    Returns:
        pagetext (str): the raw text from the body of a wiki page
    '''

    selector = Selector(text=clean_page)    # Creates a Selector class to use CSS selectors (scrapy can do some by default but it was buggy)
    page_body = selector.css('div#bodyContent *::text').getall()    # Gets a list of divs with the id "bodyContent". Most iGEM pages only have one div

    pagetext = ' '.join(str(div) for div in page_body)    # Turns the text in bodyContent into a string

    
    
    pagetext = pagetext.replace('"', "'")   # Replaces the '"' characters with ''' in order to avoid premature closing of the string in the export file.


    chars_to_remove = [r'\\n', r'\n', r'\t', r'\\t']    # List of newline and tab chars that I observed during testing that needed to be removed

    for char in chars_to_remove:    # Iterates through chars_to_remove and removes the chars from the pagetext
        pagetext = pagetext.replace(char, '')

    pagetext = ' '.join(pagetext.split())  # Cleans weird spacing and newlines 
    
    return pagetext

class iGEMSpider(CrawlSpider):
    '''
    A scrapy CrawlSpider that will automatically folow every link it finds on a page,
    starting with the 2021 iGEM teamlist. If the link matches certain rules, it will 
    automatically parse it, scrape it, process it, and output it to the file you select.
    
    Inputs:
        start_urls [list of str]: the starting url for the scraper to begin

    Yields:
        WikiPage Item -> file (see initial documentation, items.py, pipelines.py):
            url (str): the url of the software/modelling page
            pagetype (str): a string identifying if the page is a software or modelling page
                            in order to help filter them down the line
            teamname (str): identifies the team that created the page (see getTeamname)
            year (str): identifies the year of competition of the team (see getYear)
            pagetext (str): the body content of the wiki page (see getPagetext)

    '''
    name = 'tomholland'     # I'm a comedian
    allowed_domains = ['igem.org']  # You need an allowed domains list to get the CrawlScraper to work and I'd rather not have the bot scrape the entirety of the internet.
    rules = (
        
        # First rule looks for pages with the word Mode + following characters in the URL in order to get pages with Model, Modelling, and Modelling. The pages that match the criteria get callbacked to parse_model_page
        Rule(LinkExtractor(allow=(r'Mode\w+')), callback='parse_model_page'), 
        
        # Second rule looks for pages with the word /Software in the URL in order to to avoid teams with software in the name. The pages that match the criteria get callbacked to parse_soft_page
        Rule(LinkExtractor(allow=(r'/Software')), callback='parse_soft_page'),

        # Final rule looks for pages with the word Team: in the URL, while denying pages that got the crawler in an infinite loop. There is no callback, allowing the crawler to use these pages to find new links.
        # We've also excluded pages that we don't want to scrape (to decrease scaping times). If modifying, ensure that the pages you want aren't included in this list.
        # Theoretically, there is no issue with keeping it if you've created a rule to get the pages above because the rules are checked top-down, but I wouldn't personally risk it.
        Rule(LinkExtractor(allow=('Team:', ), deny=('oldid=', 'Login', 'action=history', 'wiki', 'Special', 'Journal', 'Notebook', r'Protocol\w+', 'Safety', 'Results', 'Parts', 'Description', 'Judging', r'Sustainab\w+', 'Sponsers', 'Partnership', 'Education'))),
    )

    custom_settings = { 
        # This is 30 to allow much faster scraping. It was 100 once, but the iGEM servers didn't like that 
        # and nearly banned me so the theoretical maximum limit is somewhere in between.
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 30,
        'CONCURRENT_REQUESTS' : 60
    }

    start_urls = [
        'https://old.igem.org/Team_List?year=2021&name=Championship&division=igem'
    ]

    def parse_model_page(self, response):
        '''
        Function called when a page matches rule 1 of the CrawlSpider rules
        Parses the model page.
        
        Arguments:
            response (Response): the response given by the Scrapy request

        Yields:
            WikiPage Item -> file (see initial documentation, items.py, pipelines.py):
                url (str): the url of the software/modelling page
                pagetype (str): a string identifying if the page is a software or modelling page
                                in order to help filter them down the line
                teamname (str): identifies the team that created the page (see getTeamname)
                year (str): identifies the year of competition of the team (see getYear)
                pagetext (str): the body content of the wiki page (see getPagetext)
        '''
        page = WikiPage()   # Use scrapy item objects to more accurately follow established standards 
                            # For more info, see the items.py file or the scrapy documentation
        
        page['url'] = str(response.url)
        page['pagetype'] = 'Model'
        page['teamname'] = getTeamname(page['url'])
        page['year'] = getYear(page['url'])
        clean_html = cleanHTML(str(response.text))
        page['pagetext'] = getPagetext(clean_html)

        yield page
    def parse_soft_page(self, response):
        '''
        Function called when a page matches rule 2 of the CrawlSpider rules
        Parses the software page
        
        Arguments:
            response (Response): the response given by the Scrapy request

        Yields:
            WikiPage Item -> file (see initial documentation, items.py, pipelines.py):
                    url (str): the url of the software/modelling page
                    pagetype (str): a string identifying if the page is a software or modelling page
                                    in order to help filter them down the line
                    teamname (str): identifies the team that created the page (see getTeamname)
                    year (str): identifies the year of competition of the team (see getYear)
                    pagetext (str): the body content of the wiki page (see getPagetext)
        '''
        page = WikiPage()   # Use scrapy item objects to more accurately follow existing convention 
                            # For more info, see the items.py file or review the scrapy documentation
        
        page['url'] = str(response.url)
        page['pagetype'] = 'Software'
        page['teamname'] = getTeamname(page['url'])
        page['year'] = getYear(page['url'])
        clean_html = cleanHTML(str(response.text))
        page['pagetext'] = getPagetext(clean_html)

        yield page


