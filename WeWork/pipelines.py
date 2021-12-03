# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from pydispatch import dispatcher

# class WeWorkPipeline:
#     def process_item(self, item, spider):
#         return item

class MultiCSVItemPipeline(object):
    fileNamesCsv = ['WeWorkItem']

    def __init__(self):
        self.files = {}
        self.exporters = {}
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)


    def spider_opened(self, spider):
        self.files = dict([ (name, open(name+'.csv','ab')) for name in self.fileNamesCsv])
        for name in self.fileNamesCsv:
            self.exporters[name] = CsvItemExporter(self.files[name])
            if name == 'WeWorkItem':                    
                self.exporters[name].fields_to_export = ['Name', 'Address', 'Country', 
                    'Locality', 'postalCode', 'Telephone', 'Latitude', 'Longitude', 'Amenities', 
                    'Rating', 'Reviews', 'Transit', 'URL']
            self.exporters[name].start_exporting()

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def item_type(self, item):
        return str(type(item)).split('.')[2].rstrip("'>")

    def process_item(self, item, spider):
        typesItem = self.item_type(item)
        if typesItem in set(self.fileNamesCsv):
            self.exporters[typesItem].export_item(item)
        return item