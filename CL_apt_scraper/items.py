import scrapy
 
class AptData(scrapy.Item):
	price = scrapy.Field()
	room_count = scrapy.Field()
	area = scrapy.Field() 
