import scrapy
from scrapy import Selector
import re
from CL_apt_scraper.items import AptData

class ClScraper(scrapy.Spider):   
    name = "cl_apt"
    allowed_domains = ["http://craigslist.org"]
  
    def __init__(self, regional_url='', metric='median' ,br=1, search_depth=25):   
        self.br = str(br)
        self.metric = metric
        self.start_urls = [regional_url+'?s=%s00&bedrooms=%s' % (str(i), br) for i in range(1, int(search_depth))]

        super(ClScraper, self).__init__()

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//*[@id="searchform"]/div/div/p')
                
        for row in rows: 
            price =  row.xpath('span/span[3]/span[1]/text()').extract()
            room_count = row.xpath('span/span[3]/span[2]/text()').re(r'\d*br')
            area = row.xpath('span/span[3]/span[3]/small/text()').extract()            
            
            all_data_preset = False not in [len(unit) > 0 for unit in [price, room_count, area]]
          
            if all_data_preset:
                if room_count[0] == self.br+'br': 
                    item = AptData()  
                    item['price'] = price[0]
                    item['room_count'] = room_count[0]
                    item['area'] = area[0]
                
                    yield item       