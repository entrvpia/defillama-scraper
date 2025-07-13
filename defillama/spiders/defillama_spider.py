import scrapy
from defillama.items import DefillamaItem

class DefillamaSpider(scrapy.Spider):
    name = "defillama_spider"
    allowed_domains = ["defillama.com"]

    def __init__(self, protocol="hyperliquid", *args, **kwargs):
        super(DefillamaSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://defillama.com/protocol/{protocol}"]
        self.protocol = protocol

    def parse(self, response):
        item = DefillamaItem()
        item["protocol"] = self.protocol

        # Extract Market Cap using provided XPath
        market_cap = response.xpath('/html/body/div/main/div/div[2]/div[1]/div/div/p[1]/span[2]/text()').get()
        item["market_cap"] = market_cap.strip() if market_cap else "Not found"

        # Extract Annual Revenue using provided XPath
        annual_revenue = response.xpath('/html/body/div/main/div/div[2]/div[1]/div/div/details[2]/summary/span[2]/text()').get()
        item["annual_revenue"] = annual_revenue.strip() if annual_revenue else "Not found"

        yield item

    def _convert_to_number(self, value_str):
        """Convert string with 'b' or 'm' suffix to number"""
        try:
            if 'b' in value_str.lower():
                return float(value_str.lower().replace('b', '')) * 1_000_000_000
            elif 'm' in value_str.lower():
                return float(value_str.lower().replace('m', '')) * 1_000_000
            else:
                return float(value_str)
        except (ValueError, AttributeError):
            return None