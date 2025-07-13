BOT_NAME = "defillama"

SPIDER_MODULES = ["defillama.spiders"]
NEWSPIDER_MODULE = "defillama.spiders"

# Obey robots.txt rules (set to False if necessary, but check DefiLlama's robots.txt first)
ROBOTSTXT_OBEY = True

# Configure a delay to avoid overloading the server
DOWNLOAD_DELAY = 2

# Identify your scraper politely
USER_AGENT = "defillama-scraper/1.0 (+your.email@example.com)"

# Enable or disable extensions
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

# Configure item pipelines
ITEM_PIPELINES = {
    "defillama.pipelines.DefillamaPipeline": 300,
}