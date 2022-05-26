# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter
import re


class KeystoneXL:
    '''
    The primary item pipeline for the WikiPage objects. Conditionally extracts the scraped information
    into the file specified in the self.file variable.
    
    Must also be specified in the settings.py file under ITEM_PIPELINES in order to function.
    '''

    def open_spider(self, spider): # Runs when the spider starts
        self.file = open('samara.jl', 'wb') # Opens the file specified. wb is necessary for the JsonLinesItemExporter and will overwrite the file each run
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8')  # Uses the built in JsonLineItemExporter class to export the file
        self.exporter.start_exporting() # Starts the exporter and waits for an item

    
    def close_spider(self, spider): # Runs when the spider ends
        self.exporter.finish_exporting()    # Ends the exporter
        self.file.close()   # Closes the file
    
    def process_item(self, item, spider):   # Runs when an item is yielded in iGEMScraper.py
        
        scraped_data = ItemAdapter(item)    # Adapts the item into a dict-like ItemAdapter object

        strings_to_check_for = ['No Page Text', # A list of strings found in false-positive, empty pages
                            'The requested page title was invalid', 
                            'This page is used by the judges to evaluate your team',
                            'This is a template page',
                            'There is currently no text',
                            'In order to be considered for the',
                            ]
        
        if any(bad_string in scraped_data['pagetext'] for bad_string in strings_to_check_for) == True:  # Checks if any of the false positive strings exists
            raise DropItem('Invalid Page Removed!') # If any string exists, drop the item, stop processing, and do not export
        
        if len(scraped_data['pagetext']) < 100: # Checks to ensure the page has sufficient content
            raise DropItem('Page too short')    # If any pagetext too short, drop the item, stop processing, and do not export
        
        
        scraped_data['pagetext'] = re.sub(r'\$\$.+?\$\$', '', scraped_data['pagetext']) # Removes equations from the exported data
        
        self.exporter.export_item(item) # Exports the item to the file specified
        return item 