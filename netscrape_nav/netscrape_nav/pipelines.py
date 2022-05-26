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

    def open_spider(self, spider):
        self.file = open('samara.jl', 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    
    def process_item(self, item, spider):
        
        scraped_data = ItemAdapter(item)

        strings_to_check_for = ['No Page Text', 
                            'The requested page title was invalid', 
                            'This page is used by the judges to evaluate your team',
                            'This is a template page',
                            'There is currently no text',
                            'In order to be considered for the',
                            ]
        
        if any(bad_string in scraped_data['pagetext'] for bad_string in strings_to_check_for) == True:
            raise DropItem('Invalid Page Removed!')
        
        if len(scraped_data['pagetext']) < 100:
            raise DropItem('Page too short')
        
        scraped_data['pagetext'] = re.sub(r'\$\$.+?\$\$', '', scraped_data['pagetext'])

        self.exporter.export_item(item)
        return item 