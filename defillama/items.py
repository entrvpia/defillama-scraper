import scrapy

class DefillamaItem(scrapy.Item):
    protocol = scrapy.Field()
    market_cap = scrapy.Field()
    annual_revenue = scrapy.Field()
    pe_ratio = scrapy.Field()